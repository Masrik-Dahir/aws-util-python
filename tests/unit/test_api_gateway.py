"""Tests for aws_util.api_gateway module."""
from __future__ import annotations

import base64
import json
import time
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util.api_gateway import (
    APIKeyRecord,
    AuthPolicy,
    ThrottleResult,
    ValidationResult,
    WebSocketConnection,
    _build_auth_response,
    _decode_jwt_payload,
    api_key_authorizer,
    jwt_authorizer,
    request_validator,
    throttle_guard,
    websocket_broadcast,
    websocket_connect,
    websocket_disconnect,
    websocket_list_connections,
)

REGION = "us-east-1"
RESOURCE_ARN = "arn:aws:execute-api:us-east-1:123456789:api/*/GET/resource"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_jwt(claims: dict, header: dict | None = None) -> str:
    """Build a fake JWT token with the given claims (no real signature)."""
    hdr = header or {"alg": "RS256", "typ": "JWT"}
    h = base64.urlsafe_b64encode(json.dumps(hdr).encode()).rstrip(b"=").decode()
    p = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    s = base64.urlsafe_b64encode(b"fakesignature").rstrip(b"=").decode()
    return f"{h}.{p}.{s}"


def _make_api_key_table(name: str = "api-keys") -> str:
    client = boto3.client("dynamodb", region_name=REGION)
    client.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "api_key", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "api_key", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    return name


def _make_throttle_table(name: str = "throttle") -> str:
    client = boto3.client("dynamodb", region_name=REGION)
    client.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "throttle_key", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "throttle_key", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    return name


def _make_ws_table(name: str = "ws-connections") -> str:
    client = boto3.client("dynamodb", region_name=REGION)
    client.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": "connection_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "connection_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    return name


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_auth_policy(self) -> None:
        p = AuthPolicy(principal_id="user1", effect="Allow", resource="*")
        assert p.principal_id == "user1"
        assert p.effect == "Allow"
        assert p.context == {}

    def test_api_key_record(self) -> None:
        r = APIKeyRecord(api_key="abc", owner="team-a")
        assert r.enabled is True
        assert r.rate_limit == 100
        assert r.description == ""

    def test_throttle_result(self) -> None:
        r = ThrottleResult(allowed=True, current_count=5, limit=100, ttl=9999)
        assert r.allowed is True

    def test_websocket_connection(self) -> None:
        c = WebSocketConnection(connection_id="conn1", connected_at=1000)
        assert c.connection_id == "conn1"
        assert c.metadata == {}

    def test_validation_result(self) -> None:
        r = ValidationResult(valid=True)
        assert r.errors == []

    def test_validation_result_with_errors(self) -> None:
        r = ValidationResult(valid=False, errors=["field required"])
        assert not r.valid


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------


class TestDecodeJWTPayload:
    def test_valid_token(self) -> None:
        claims = {"sub": "user1", "email": "user@example.com"}
        token = _make_jwt(claims)
        decoded = _decode_jwt_payload(token)
        assert decoded["sub"] == "user1"
        assert decoded["email"] == "user@example.com"

    def test_invalid_format_no_dots(self) -> None:
        with pytest.raises(ValueError, match="Invalid JWT format"):
            _decode_jwt_payload("notavalidtoken")

    def test_invalid_format_two_parts(self) -> None:
        with pytest.raises(ValueError, match="Invalid JWT format"):
            _decode_jwt_payload("header.payload")

    def test_invalid_base64_payload(self) -> None:
        with pytest.raises(ValueError, match="Failed to decode JWT payload"):
            _decode_jwt_payload("header.!!!invalid!!!.signature")


class TestBuildAuthResponse:
    def test_allow_response(self) -> None:
        resp = _build_auth_response("user1", "Allow", RESOURCE_ARN)
        assert resp["principalId"] == "user1"
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"
        assert stmt["Resource"] == RESOURCE_ARN
        assert "context" not in resp

    def test_deny_response(self) -> None:
        resp = _build_auth_response("unknown", "Deny", RESOURCE_ARN)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_with_context(self) -> None:
        resp = _build_auth_response("user1", "Allow", "*", context={"email": "a@b.com"})
        assert resp["context"]["email"] == "a@b.com"


# ---------------------------------------------------------------------------
# 1. JWT authorizer
# ---------------------------------------------------------------------------


class TestJWTAuthorizer:
    def test_valid_token_allows(self) -> None:
        claims = {"sub": "user123", "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        assert resp["principalId"] == "user123"
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    def test_expired_token_denies(self) -> None:
        claims = {"sub": "user123", "exp": int(time.time()) - 100}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_invalid_token_denies(self) -> None:
        resp = jwt_authorizer("not.a.valid-token", RESOURCE_ARN)
        assert resp["principalId"] == "unknown"
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_cognito_issuer_validation_pass(self) -> None:
        pool_id = "us-east-1_ABC123"
        iss = f"https://cognito-idp.us-east-1.amazonaws.com/{pool_id}"
        claims = {"sub": "user1", "iss": iss, "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(
            token, RESOURCE_ARN, user_pool_id=pool_id, region_name="us-east-1"
        )
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    def test_cognito_issuer_validation_fail(self) -> None:
        claims = {"sub": "user1", "iss": "https://other-issuer.com", "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(
            token, RESOURCE_ARN, user_pool_id="us-east-1_ABC123", region_name="us-east-1"
        )
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_required_claims_pass(self) -> None:
        claims = {"sub": "user1", "scope": "admin", "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN, required_claims={"scope": "admin"})
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    def test_required_claims_fail(self) -> None:
        claims = {"sub": "user1", "scope": "read", "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN, required_claims={"scope": "admin"})
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_no_exp_allows(self) -> None:
        claims = {"sub": "user1"}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    def test_invalid_exp_type_denies(self) -> None:
        claims = {"sub": "user1", "exp": "not-a-number"}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_context_includes_standard_claims(self) -> None:
        claims = {
            "sub": "user1",
            "email": "user@example.com",
            "scope": "read write",
            "client_id": "abc",
            "cognito:username": "jdoe",
            "custom:tenant": "acme",
            "exp": int(time.time()) + 3600,
        }
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        ctx = resp["context"]
        assert ctx["sub"] == "user1"
        assert ctx["email"] == "user@example.com"
        assert ctx["scope"] == "read write"
        assert ctx["client_id"] == "abc"
        assert ctx["cognito:username"] == "jdoe"
        assert "custom:tenant" not in ctx

    def test_client_id_as_principal_when_no_sub(self) -> None:
        claims = {"client_id": "my-client", "exp": int(time.time()) + 3600}
        token = _make_jwt(claims)
        resp = jwt_authorizer(token, RESOURCE_ARN)
        assert resp["principalId"] == "my-client"

    def test_completely_malformed_token(self) -> None:
        resp = jwt_authorizer("garbage", RESOURCE_ARN)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"


# ---------------------------------------------------------------------------
# 2. API key authorizer
# ---------------------------------------------------------------------------


class TestAPIKeyAuthorizer:
    def test_valid_key_allows(self) -> None:
        table = _make_api_key_table()
        client = boto3.client("dynamodb", region_name=REGION)
        client.put_item(
            TableName=table,
            Item={
                "api_key": {"S": "key-123"},
                "owner": {"S": "team-a"},
                "enabled": {"BOOL": True},
                "description": {"S": "Test key"},
            },
        )
        resp = api_key_authorizer("key-123", table, RESOURCE_ARN, region_name=REGION)
        assert resp["principalId"] == "team-a"
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"
        assert resp["context"]["owner"] == "team-a"
        assert resp["context"]["description"] == "Test key"

    def test_missing_key_denies(self) -> None:
        table = _make_api_key_table()
        resp = api_key_authorizer("nonexistent", table, RESOURCE_ARN, region_name=REGION)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_disabled_key_denies(self) -> None:
        table = _make_api_key_table()
        client = boto3.client("dynamodb", region_name=REGION)
        client.put_item(
            TableName=table,
            Item={
                "api_key": {"S": "key-disabled"},
                "owner": {"S": "team-b"},
                "enabled": {"BOOL": False},
            },
        )
        resp = api_key_authorizer("key-disabled", table, RESOURCE_ARN, region_name=REGION)
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_dynamo_error_denies(self) -> None:
        resp = api_key_authorizer(
            "key-123", "nonexistent-table", RESOURCE_ARN, region_name=REGION
        )
        stmt = resp["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    def test_key_without_description(self) -> None:
        table = _make_api_key_table()
        client = boto3.client("dynamodb", region_name=REGION)
        client.put_item(
            TableName=table,
            Item={
                "api_key": {"S": "key-nodesc"},
                "owner": {"S": "team-c"},
                "enabled": {"BOOL": True},
            },
        )
        resp = api_key_authorizer("key-nodesc", table, RESOURCE_ARN, region_name=REGION)
        assert resp["principalId"] == "team-c"
        assert "description" not in resp["context"]


# ---------------------------------------------------------------------------
# 3. Request validator
# ---------------------------------------------------------------------------


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    email: str
    age: int


class TestRequestValidator:
    def test_valid_body(self) -> None:
        body = json.dumps({"name": "Alice", "email": "alice@example.com", "age": 30})
        result = request_validator(body, CreateUserRequest)
        assert result.valid is True
        assert result.errors == []

    def test_none_body(self) -> None:
        result = request_validator(None, CreateUserRequest)
        assert result.valid is False
        assert "required" in result.errors[0].lower()

    def test_invalid_json(self) -> None:
        result = request_validator("{not json}", CreateUserRequest)
        assert result.valid is False
        assert any("Invalid JSON" in e for e in result.errors)

    def test_missing_required_field(self) -> None:
        body = json.dumps({"name": "Alice"})
        result = request_validator(body, CreateUserRequest)
        assert result.valid is False
        assert len(result.errors) > 0

    def test_wrong_type(self) -> None:
        body = json.dumps({"name": "Alice", "email": "a@b.com", "age": "not-a-number"})
        result = request_validator(body, CreateUserRequest)
        assert result.valid is False

    def test_extra_fields_allowed_by_default(self) -> None:
        body = json.dumps({"name": "Bob", "email": "b@c.com", "age": 25, "extra": "ok"})
        result = request_validator(body, CreateUserRequest)
        assert result.valid is True

    def test_model_validate_generic_exception(self) -> None:
        """Cover the else branch when exception lacks .errors()."""
        with patch.object(
            CreateUserRequest, "model_validate", side_effect=TypeError("unexpected")
        ):
            result = request_validator('{"name":"A","email":"a@b","age":1}', CreateUserRequest)
            assert result.valid is False
            assert "unexpected" in result.errors[0]


# ---------------------------------------------------------------------------
# 4. Throttle guard
# ---------------------------------------------------------------------------


class TestThrottleGuard:
    def test_first_request_allowed(self) -> None:
        table = _make_throttle_table()
        result = throttle_guard("user1", table, limit=10, region_name=REGION)
        assert result.allowed is True
        assert result.current_count == 1
        assert result.limit == 10

    def test_under_limit_allowed(self) -> None:
        table = _make_throttle_table()
        for _ in range(5):
            throttle_guard("user2", table, limit=10, region_name=REGION)
        result = throttle_guard("user2", table, limit=10, region_name=REGION)
        assert result.allowed is True
        assert result.current_count == 6

    def test_at_limit_still_allowed(self) -> None:
        table = _make_throttle_table()
        for _ in range(9):
            throttle_guard("user3", table, limit=10, region_name=REGION)
        result = throttle_guard("user3", table, limit=10, region_name=REGION)
        assert result.allowed is True
        assert result.current_count == 10

    def test_over_limit_denied(self) -> None:
        table = _make_throttle_table()
        for _ in range(10):
            throttle_guard("user4", table, limit=10, region_name=REGION)
        result = throttle_guard("user4", table, limit=10, region_name=REGION)
        assert result.allowed is False
        assert result.current_count == 11

    def test_different_keys_independent(self) -> None:
        table = _make_throttle_table()
        for _ in range(10):
            throttle_guard("ip-1.2.3.4", table, limit=10, region_name=REGION)
        result = throttle_guard("ip-5.6.7.8", table, limit=10, region_name=REGION)
        assert result.allowed is True
        assert result.current_count == 1

    def test_dynamo_error_allows_by_default(self) -> None:
        result = throttle_guard(
            "user-err", "nonexistent-table", limit=5, region_name=REGION
        )
        assert result.allowed is True
        assert result.current_count == 0


# ---------------------------------------------------------------------------
# 5. WebSocket connection manager
# ---------------------------------------------------------------------------


class TestWebSocketConnect:
    def test_connect(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)

        client = boto3.client("dynamodb", region_name=REGION)
        resp = client.get_item(
            TableName=table, Key={"connection_id": {"S": "conn-1"}}
        )
        assert resp["Item"]["connection_id"]["S"] == "conn-1"
        assert "connected_at" in resp["Item"]

    def test_connect_with_metadata(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-2", table, metadata={"user_id": "u1"}, region_name=REGION)

        client = boto3.client("dynamodb", region_name=REGION)
        resp = client.get_item(
            TableName=table, Key={"connection_id": {"S": "conn-2"}}
        )
        assert resp["Item"]["user_id"]["S"] == "u1"

    def test_connect_failure_raises(self) -> None:
        with pytest.raises(RuntimeError, match="Failed to store WebSocket"):
            websocket_connect("conn-x", "nonexistent-table", region_name=REGION)


class TestWebSocketDisconnect:
    def test_disconnect(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)
        websocket_disconnect("conn-1", table, region_name=REGION)

        client = boto3.client("dynamodb", region_name=REGION)
        resp = client.get_item(
            TableName=table, Key={"connection_id": {"S": "conn-1"}}
        )
        assert "Item" not in resp

    def test_disconnect_nonexistent_ok(self) -> None:
        table = _make_ws_table()
        # Should not raise
        websocket_disconnect("nonexistent", table, region_name=REGION)

    def test_disconnect_failure_raises(self) -> None:
        with pytest.raises(RuntimeError, match="Failed to remove WebSocket"):
            websocket_disconnect("conn-x", "nonexistent-table", region_name=REGION)


class TestWebSocketListConnections:
    def test_list_empty(self) -> None:
        table = _make_ws_table()
        conns = websocket_list_connections(table, region_name=REGION)
        assert conns == []

    def test_list_multiple(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-a", table, region_name=REGION)
        websocket_connect("conn-b", table, metadata={"room": "lobby"}, region_name=REGION)

        conns = websocket_list_connections(table, region_name=REGION)
        assert len(conns) == 2
        ids = {c.connection_id for c in conns}
        assert ids == {"conn-a", "conn-b"}

        lobby_conn = next(c for c in conns if c.connection_id == "conn-b")
        assert lobby_conn.metadata.get("room") == "lobby"

    def test_list_failure_raises(self) -> None:
        with pytest.raises(RuntimeError, match="Failed to list WebSocket"):
            websocket_list_connections("nonexistent-table", region_name=REGION)


class TestWebSocketBroadcast:
    def test_broadcast_sends_to_all(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)
        websocket_connect("conn-2", table, region_name=REGION)

        mock_apigw = MagicMock()
        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table,
                "https://api.example.com/prod",
                {"message": "hello"},
                region_name=REGION,
            )

        assert result["sent"] == 2
        assert result["stale"] == 0
        assert mock_apigw.post_to_connection.call_count == 2

    def test_broadcast_string_message(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)

        mock_apigw = MagicMock()
        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table,
                "https://api.example.com/prod",
                "plain text",
                region_name=REGION,
            )

        assert result["sent"] == 1
        call_args = mock_apigw.post_to_connection.call_args
        assert call_args.kwargs["Data"] == b"plain text"

    def test_broadcast_list_message(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)

        mock_apigw = MagicMock()
        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table,
                "https://api.example.com/prod",
                [1, 2, 3],
                region_name=REGION,
            )

        assert result["sent"] == 1

    def test_broadcast_removes_stale_connections(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)
        websocket_connect("conn-stale", table, region_name=REGION)

        mock_apigw = MagicMock()
        gone_error = ClientError(
            {"Error": {"Code": "GoneException", "Message": "gone"}},
            "PostToConnection",
        )

        def side_effect(**kwargs: object) -> None:
            if kwargs.get("ConnectionId") == "conn-stale":
                raise gone_error

        mock_apigw.post_to_connection.side_effect = side_effect

        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table, "https://api.example.com/prod", "hi", region_name=REGION
            )

        assert result["sent"] == 1
        assert result["stale"] == 1

        # Verify stale connection was removed
        conns = websocket_list_connections(table, region_name=REGION)
        assert len(conns) == 1
        assert conns[0].connection_id == "conn-1"

    def test_broadcast_other_error_logged(self) -> None:
        table = _make_ws_table()
        websocket_connect("conn-1", table, region_name=REGION)

        mock_apigw = MagicMock()
        other_error = ClientError(
            {"Error": {"Code": "InternalServerError", "Message": "oops"}},
            "PostToConnection",
        )
        mock_apigw.post_to_connection.side_effect = other_error

        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table, "https://api.example.com/prod", "hi", region_name=REGION
            )

        assert result["sent"] == 0
        assert result["stale"] == 0

    def test_broadcast_empty_table(self) -> None:
        table = _make_ws_table()
        mock_apigw = MagicMock()
        with patch("boto3.client", return_value=mock_apigw):
            result = websocket_broadcast(
                table, "https://api.example.com/prod", "hi", region_name=REGION
            )
        assert result["sent"] == 0
        assert result["stale"] == 0
        mock_apigw.post_to_connection.assert_not_called()
# Generated tests for boto3 wrapper methods
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from aws_util.api_gateway import (
    create_api_key,
    create_authorizer,
    create_base_path_mapping,
    create_deployment,
    create_documentation_part,
    create_documentation_version,
    create_domain_name,
    create_domain_name_access_association,
    create_model,
    create_request_validator,
    create_resource,
    create_rest_api,
    create_stage,
    create_usage_plan,
    create_usage_plan_key,
    create_vpc_link,
    delete_api_key,
    delete_authorizer,
    delete_base_path_mapping,
    delete_client_certificate,
    delete_deployment,
    delete_documentation_part,
    delete_documentation_version,
    delete_domain_name,
    delete_domain_name_access_association,
    delete_gateway_response,
    delete_integration,
    delete_integration_response,
    delete_method,
    delete_method_response,
    delete_model,
    delete_request_validator,
    delete_resource,
    delete_rest_api,
    delete_stage,
    delete_usage_plan,
    delete_usage_plan_key,
    delete_vpc_link,
    flush_stage_authorizers_cache,
    flush_stage_cache,
    generate_client_certificate,
    get_account,
    get_api_key,
    get_api_keys,
    get_authorizer,
    get_authorizers,
    get_base_path_mapping,
    get_base_path_mappings,
    get_client_certificate,
    get_client_certificates,
    get_deployment,
    get_deployments,
    get_documentation_part,
    get_documentation_parts,
    get_documentation_version,
    get_documentation_versions,
    get_domain_name,
    get_domain_name_access_associations,
    get_domain_names,
    get_export,
    get_gateway_response,
    get_gateway_responses,
    get_integration,
    get_integration_response,
    get_method,
    get_method_response,
    get_model,
    get_model_template,
    get_models,
    get_request_validator,
    get_request_validators,
    get_resource,
    get_resources,
    get_rest_api,
    get_rest_apis,
    get_sdk,
    get_sdk_type,
    get_sdk_types,
    get_stage,
    get_stages,
    get_tags,
    get_usage,
    get_usage_plan,
    get_usage_plan_key,
    get_usage_plan_keys,
    get_usage_plans,
    get_vpc_link,
    get_vpc_links,
    import_api_keys,
    import_documentation_parts,
    import_rest_api,
    put_gateway_response,
    put_integration,
    put_integration_response,
    put_method,
    put_method_response,
    put_rest_api,
    reject_domain_name_access_association,
    tag_resource,
    run_invoke_authorizer,
    run_invoke_method,
    untag_resource,
    update_account,
    update_api_key,
    update_authorizer,
    update_base_path_mapping,
    update_client_certificate,
    update_deployment,
    update_documentation_part,
    update_documentation_version,
    update_domain_name,
    update_gateway_response,
    update_integration,
    update_integration_response,
    update_method,
    update_method_response,
    update_model,
    update_request_validator,
    update_resource,
    update_rest_api,
    update_stage,
    update_usage,
    update_usage_plan,
    update_vpc_link,
)


def test_create_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_api_key(region_name="us-east-1")
    mock_client.create_api_key.assert_called_once()


def test_create_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_api_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_api_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_api_key(region_name="us-east-1")


def test_create_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_api_key(name="test-name", description="test-description", enabled=True, generate_distinct_id=True, value="test-value", stage_keys=[], customer_id="test-customer_id", tags={}, region_name="us-east-1")
    mock_client.create_api_key.assert_called_once()


def test_create_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_authorizer("test-rest_api_id", "test-name", "test-type", region_name="us-east-1")
    mock_client.create_authorizer.assert_called_once()


def test_create_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_authorizer",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_authorizer("test-rest_api_id", "test-name", "test-type", region_name="us-east-1")


def test_create_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_authorizer("test-rest_api_id", "test-name", "test-type", provider_ar_ns=[], auth_type="test-auth_type", authorizer_uri="test-authorizer_uri", authorizer_credentials="test-authorizer_credentials", identity_source="test-identity_source", identity_validation_expression="test-identity_validation_expression", authorizer_result_ttl_in_seconds=1, region_name="us-east-1")
    mock_client.create_authorizer.assert_called_once()


def test_create_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_base_path_mapping("test-domain_name", "test-rest_api_id", region_name="us-east-1")
    mock_client.create_base_path_mapping.assert_called_once()


def test_create_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_base_path_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_base_path_mapping",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_base_path_mapping("test-domain_name", "test-rest_api_id", region_name="us-east-1")


def test_create_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_base_path_mapping("test-domain_name", "test-rest_api_id", domain_name_id="test-domain_name_id", base_path="test-base_path", stage="test-stage", region_name="us-east-1")
    mock_client.create_base_path_mapping.assert_called_once()


def test_create_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_deployment("test-rest_api_id", region_name="us-east-1")
    mock_client.create_deployment.assert_called_once()


def test_create_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_deployment",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_deployment("test-rest_api_id", region_name="us-east-1")


def test_create_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_deployment("test-rest_api_id", stage_name="test-stage_name", stage_description="test-stage_description", description="test-description", cache_cluster_enabled=True, cache_cluster_size="test-cache_cluster_size", variables={}, canary_settings={}, tracing_enabled=True, region_name="us-east-1")
    mock_client.create_deployment.assert_called_once()


def test_create_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_documentation_part.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_documentation_part("test-rest_api_id", {}, "test-properties", region_name="us-east-1")
    mock_client.create_documentation_part.assert_called_once()


def test_create_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_documentation_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_documentation_part",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_documentation_part("test-rest_api_id", {}, "test-properties", region_name="us-east-1")


def test_create_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.create_documentation_version.assert_called_once()


def test_create_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_documentation_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_documentation_version",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


def test_create_documentation_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_documentation_version("test-rest_api_id", "test-documentation_version", stage_name="test-stage_name", description="test-description", region_name="us-east-1")
    mock_client.create_documentation_version.assert_called_once()


def test_create_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.create_domain_name.assert_called_once()


def test_create_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_domain_name",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_domain_name("test-domain_name", region_name="us-east-1")


def test_create_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_domain_name("test-domain_name", certificate_name="test-certificate_name", certificate_body="test-certificate_body", certificate_private_key="test-certificate_private_key", certificate_chain="test-certificate_chain", certificate_arn="test-certificate_arn", regional_certificate_name="test-regional_certificate_name", regional_certificate_arn="test-regional_certificate_arn", endpoint_configuration={}, tags={}, security_policy="test-security_policy", mutual_tls_authentication={}, ownership_verification_certificate_arn="test-ownership_verification_certificate_arn", policy="test-policy", routing_mode="test-routing_mode", region_name="us-east-1")
    mock_client.create_domain_name.assert_called_once()


def test_create_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name_access_association.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", region_name="us-east-1")
    mock_client.create_domain_name_access_association.assert_called_once()


def test_create_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name_access_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_domain_name_access_association",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", region_name="us-east-1")


def test_create_domain_name_access_association_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_domain_name_access_association.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", tags={}, region_name="us-east-1")
    mock_client.create_domain_name_access_association.assert_called_once()


def test_create_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_model("test-rest_api_id", "test-name", "test-content_type", region_name="us-east-1")
    mock_client.create_model.assert_called_once()


def test_create_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_model",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_model("test-rest_api_id", "test-name", "test-content_type", region_name="us-east-1")


def test_create_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_model("test-rest_api_id", "test-name", "test-content_type", description="test-description", model_schema="test-model_schema", region_name="us-east-1")
    mock_client.create_model.assert_called_once()


def test_create_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_request_validator("test-rest_api_id", region_name="us-east-1")
    mock_client.create_request_validator.assert_called_once()


def test_create_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_request_validator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_request_validator",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_request_validator("test-rest_api_id", region_name="us-east-1")


def test_create_request_validator_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_request_validator("test-rest_api_id", name="test-name", validate_request_body=True, validate_request_parameters=True, region_name="us-east-1")
    mock_client.create_request_validator.assert_called_once()


def test_create_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_resource("test-rest_api_id", "test-parent_id", "test-path_part", region_name="us-east-1")
    mock_client.create_resource.assert_called_once()


def test_create_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_resource("test-rest_api_id", "test-parent_id", "test-path_part", region_name="us-east-1")


def test_create_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_rest_api("test-name", region_name="us-east-1")
    mock_client.create_rest_api.assert_called_once()


def test_create_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_rest_api("test-name", region_name="us-east-1")


def test_create_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_rest_api("test-name", description="test-description", version="test-version", clone_from="test-clone_from", binary_media_types=[], minimum_compression_size=1, api_key_source="test-api_key_source", endpoint_configuration={}, policy="test-policy", tags={}, disable_execute_api_endpoint=True, region_name="us-east-1")
    mock_client.create_rest_api.assert_called_once()


def test_create_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", region_name="us-east-1")
    mock_client.create_stage.assert_called_once()


def test_create_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", region_name="us-east-1")


def test_create_stage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", description="test-description", cache_cluster_enabled=True, cache_cluster_size="test-cache_cluster_size", variables={}, documentation_version="test-documentation_version", canary_settings={}, tracing_enabled=True, tags={}, region_name="us-east-1")
    mock_client.create_stage.assert_called_once()


def test_create_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_usage_plan("test-name", region_name="us-east-1")
    mock_client.create_usage_plan.assert_called_once()


def test_create_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_plan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_usage_plan",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_usage_plan("test-name", region_name="us-east-1")


def test_create_usage_plan_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_usage_plan("test-name", description="test-description", api_stages=[], throttle={}, quota={}, tags={}, region_name="us-east-1")
    mock_client.create_usage_plan.assert_called_once()


def test_create_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_plan_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_usage_plan_key("test-usage_plan_id", "test-key_id", "test-key_type", region_name="us-east-1")
    mock_client.create_usage_plan_key.assert_called_once()


def test_create_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_plan_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_usage_plan_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_usage_plan_key("test-usage_plan_id", "test-key_id", "test-key_type", region_name="us-east-1")


def test_create_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_vpc_link("test-name", [], region_name="us-east-1")
    mock_client.create_vpc_link.assert_called_once()


def test_create_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_link",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        create_vpc_link("test-name", [], region_name="us-east-1")


def test_create_vpc_link_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    create_vpc_link("test-name", [], description="test-description", tags={}, region_name="us-east-1")
    mock_client.create_vpc_link.assert_called_once()


def test_delete_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_api_key("test-api_key", region_name="us-east-1")
    mock_client.delete_api_key.assert_called_once()


def test_delete_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_api_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_api_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_api_key("test-api_key", region_name="us-east-1")


def test_delete_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.delete_authorizer.assert_called_once()


def test_delete_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_authorizer",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


def test_delete_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.delete_base_path_mapping.assert_called_once()


def test_delete_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_base_path_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_base_path_mapping",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


def test_delete_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.delete_base_path_mapping.assert_called_once()


def test_delete_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.delete_client_certificate.assert_called_once()


def test_delete_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_client_certificate",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_client_certificate("test-client_certificate_id", region_name="us-east-1")


def test_delete_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.delete_deployment.assert_called_once()


def test_delete_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_deployment",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


def test_delete_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_documentation_part.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.delete_documentation_part.assert_called_once()


def test_delete_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_documentation_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_documentation_part",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


def test_delete_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.delete_documentation_version.assert_called_once()


def test_delete_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_documentation_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_documentation_version",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


def test_delete_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.delete_domain_name.assert_called_once()


def test_delete_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_name",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_domain_name("test-domain_name", region_name="us-east-1")


def test_delete_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_domain_name("test-domain_name", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.delete_domain_name.assert_called_once()


def test_delete_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_name_access_association.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_domain_name_access_association("test-domain_name_access_association_arn", region_name="us-east-1")
    mock_client.delete_domain_name_access_association.assert_called_once()


def test_delete_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_domain_name_access_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_name_access_association",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_domain_name_access_association("test-domain_name_access_association_arn", region_name="us-east-1")


def test_delete_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.delete_gateway_response.assert_called_once()


def test_delete_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_gateway_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_gateway_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


def test_delete_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.delete_integration.assert_called_once()


def test_delete_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_delete_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.delete_integration_response.assert_called_once()


def test_delete_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_delete_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.delete_method.assert_called_once()


def test_delete_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_method",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_delete_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.delete_method_response.assert_called_once()


def test_delete_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_method_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_method_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_delete_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.delete_model.assert_called_once()


def test_delete_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_model",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


def test_delete_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.delete_request_validator.assert_called_once()


def test_delete_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_request_validator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_request_validator",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


def test_delete_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.delete_resource.assert_called_once()


def test_delete_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


def test_delete_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.delete_rest_api.assert_called_once()


def test_delete_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_rest_api("test-rest_api_id", region_name="us-east-1")


def test_delete_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.delete_stage.assert_called_once()


def test_delete_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


def test_delete_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.delete_usage_plan.assert_called_once()


def test_delete_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_plan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_usage_plan",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_usage_plan("test-usage_plan_id", region_name="us-east-1")


def test_delete_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_plan_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.delete_usage_plan_key.assert_called_once()


def test_delete_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_plan_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_usage_plan_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")


def test_delete_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    delete_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.delete_vpc_link.assert_called_once()


def test_delete_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_link",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        delete_vpc_link("test-vpc_link_id", region_name="us-east-1")


def test_flush_stage_authorizers_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.flush_stage_authorizers_cache.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    flush_stage_authorizers_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.flush_stage_authorizers_cache.assert_called_once()


def test_flush_stage_authorizers_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.flush_stage_authorizers_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "flush_stage_authorizers_cache",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        flush_stage_authorizers_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")


def test_flush_stage_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.flush_stage_cache.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    flush_stage_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.flush_stage_cache.assert_called_once()


def test_flush_stage_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.flush_stage_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "flush_stage_cache",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        flush_stage_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")


def test_generate_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    generate_client_certificate(region_name="us-east-1")
    mock_client.generate_client_certificate.assert_called_once()


def test_generate_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_client_certificate",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        generate_client_certificate(region_name="us-east-1")


def test_generate_client_certificate_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    generate_client_certificate(description="test-description", tags={}, region_name="us-east-1")
    mock_client.generate_client_certificate.assert_called_once()


def test_get_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_account(region_name="us-east-1")
    mock_client.get_account.assert_called_once()


def test_get_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_account(region_name="us-east-1")


def test_get_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_api_key("test-api_key", region_name="us-east-1")
    mock_client.get_api_key.assert_called_once()


def test_get_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_api_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_api_key("test-api_key", region_name="us-east-1")


def test_get_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_api_key("test-api_key", include_value=True, region_name="us-east-1")
    mock_client.get_api_key.assert_called_once()


def test_get_api_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_api_keys(region_name="us-east-1")
    mock_client.get_api_keys.assert_called_once()


def test_get_api_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_api_keys",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_api_keys(region_name="us-east-1")


def test_get_api_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_api_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_api_keys(position="test-position", limit=1, name_query="test-name_query", customer_id="test-customer_id", include_values=True, region_name="us-east-1")
    mock_client.get_api_keys.assert_called_once()


def test_get_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.get_authorizer.assert_called_once()


def test_get_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_authorizer",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


def test_get_authorizers(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorizers.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_authorizers("test-rest_api_id", region_name="us-east-1")
    mock_client.get_authorizers.assert_called_once()


def test_get_authorizers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorizers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_authorizers",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_authorizers("test-rest_api_id", region_name="us-east-1")


def test_get_authorizers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_authorizers.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_authorizers("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_authorizers.assert_called_once()


def test_get_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.get_base_path_mapping.assert_called_once()


def test_get_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_base_path_mapping",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


def test_get_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.get_base_path_mapping.assert_called_once()


def test_get_base_path_mappings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mappings.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_base_path_mappings("test-domain_name", region_name="us-east-1")
    mock_client.get_base_path_mappings.assert_called_once()


def test_get_base_path_mappings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mappings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_base_path_mappings",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_base_path_mappings("test-domain_name", region_name="us-east-1")


def test_get_base_path_mappings_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_base_path_mappings.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_base_path_mappings("test-domain_name", domain_name_id="test-domain_name_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_base_path_mappings.assert_called_once()


def test_get_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.get_client_certificate.assert_called_once()


def test_get_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_client_certificate",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_client_certificate("test-client_certificate_id", region_name="us-east-1")


def test_get_client_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_client_certificates.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_client_certificates(region_name="us-east-1")
    mock_client.get_client_certificates.assert_called_once()


def test_get_client_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_client_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_client_certificates",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_client_certificates(region_name="us-east-1")


def test_get_client_certificates_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_client_certificates.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_client_certificates(position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_client_certificates.assert_called_once()


def test_get_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.get_deployment.assert_called_once()


def test_get_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deployment",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


def test_get_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_deployment("test-rest_api_id", "test-deployment_id", embed=[], region_name="us-east-1")
    mock_client.get_deployment.assert_called_once()


def test_get_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployments.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_deployments("test-rest_api_id", region_name="us-east-1")
    mock_client.get_deployments.assert_called_once()


def test_get_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_deployments",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_deployments("test-rest_api_id", region_name="us-east-1")


def test_get_deployments_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_deployments.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_deployments("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_deployments.assert_called_once()


def test_get_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_part.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.get_documentation_part.assert_called_once()


def test_get_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_documentation_part",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


def test_get_documentation_parts(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_parts.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_parts("test-rest_api_id", region_name="us-east-1")
    mock_client.get_documentation_parts.assert_called_once()


def test_get_documentation_parts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_parts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_documentation_parts",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_documentation_parts("test-rest_api_id", region_name="us-east-1")


def test_get_documentation_parts_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_parts.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_parts("test-rest_api_id", type="test-type", name_query="test-name_query", path="test-path", position="test-position", limit=1, location_status="test-location_status", region_name="us-east-1")
    mock_client.get_documentation_parts.assert_called_once()


def test_get_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.get_documentation_version.assert_called_once()


def test_get_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_documentation_version",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


def test_get_documentation_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_versions.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_versions("test-rest_api_id", region_name="us-east-1")
    mock_client.get_documentation_versions.assert_called_once()


def test_get_documentation_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_documentation_versions",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_documentation_versions("test-rest_api_id", region_name="us-east-1")


def test_get_documentation_versions_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_documentation_versions.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_documentation_versions("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_documentation_versions.assert_called_once()


def test_get_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.get_domain_name.assert_called_once()


def test_get_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_name",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_domain_name("test-domain_name", region_name="us-east-1")


def test_get_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_name("test-domain_name", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.get_domain_name.assert_called_once()


def test_get_domain_name_access_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name_access_associations.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_name_access_associations(region_name="us-east-1")
    mock_client.get_domain_name_access_associations.assert_called_once()


def test_get_domain_name_access_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name_access_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_name_access_associations",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_domain_name_access_associations(region_name="us-east-1")


def test_get_domain_name_access_associations_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_name_access_associations.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_name_access_associations(position="test-position", limit=1, resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.get_domain_name_access_associations.assert_called_once()


def test_get_domain_names(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_names.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_names(region_name="us-east-1")
    mock_client.get_domain_names.assert_called_once()


def test_get_domain_names_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_names.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_domain_names",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_domain_names(region_name="us-east-1")


def test_get_domain_names_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_domain_names.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_domain_names(position="test-position", limit=1, resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.get_domain_names.assert_called_once()


def test_get_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_export("test-rest_api_id", "test-stage_name", "test-export_type", region_name="us-east-1")
    mock_client.get_export.assert_called_once()


def test_get_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_export",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_export("test-rest_api_id", "test-stage_name", "test-export_type", region_name="us-east-1")


def test_get_export_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_export("test-rest_api_id", "test-stage_name", "test-export_type", parameters={}, accepts="test-accepts", region_name="us-east-1")
    mock_client.get_export.assert_called_once()


def test_get_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.get_gateway_response.assert_called_once()


def test_get_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_gateway_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_gateway_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


def test_get_gateway_responses(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_gateway_responses.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_gateway_responses("test-rest_api_id", region_name="us-east-1")
    mock_client.get_gateway_responses.assert_called_once()


def test_get_gateway_responses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_gateway_responses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_gateway_responses",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_gateway_responses("test-rest_api_id", region_name="us-east-1")


def test_get_gateway_responses_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_gateway_responses.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_gateway_responses("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_gateway_responses.assert_called_once()


def test_get_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.get_integration.assert_called_once()


def test_get_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_integration",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_get_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.get_integration_response.assert_called_once()


def test_get_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_integration_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_integration_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_get_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.get_method.assert_called_once()


def test_get_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_method",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_get_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.get_method_response.assert_called_once()


def test_get_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_method_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_method_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_get_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.get_model.assert_called_once()


def test_get_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


def test_get_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_model("test-rest_api_id", "test-model_name", flatten=True, region_name="us-east-1")
    mock_client.get_model.assert_called_once()


def test_get_model_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_template.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_model_template("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.get_model_template.assert_called_once()


def test_get_model_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_model_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_model_template",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_model_template("test-rest_api_id", "test-model_name", region_name="us-east-1")


def test_get_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_models.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_models("test-rest_api_id", region_name="us-east-1")
    mock_client.get_models.assert_called_once()


def test_get_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_models",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_models("test-rest_api_id", region_name="us-east-1")


def test_get_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_models.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_models("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_models.assert_called_once()


def test_get_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.get_request_validator.assert_called_once()


def test_get_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_request_validator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_request_validator",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


def test_get_request_validators(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_request_validators.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_request_validators("test-rest_api_id", region_name="us-east-1")
    mock_client.get_request_validators.assert_called_once()


def test_get_request_validators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_request_validators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_request_validators",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_request_validators("test-rest_api_id", region_name="us-east-1")


def test_get_request_validators_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_request_validators.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_request_validators("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_request_validators.assert_called_once()


def test_get_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.get_resource.assert_called_once()


def test_get_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


def test_get_resource_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_resource("test-rest_api_id", "test-resource_id", embed=[], region_name="us-east-1")
    mock_client.get_resource.assert_called_once()


def test_get_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_resources("test-rest_api_id", region_name="us-east-1")
    mock_client.get_resources.assert_called_once()


def test_get_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resources",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_resources("test-rest_api_id", region_name="us-east-1")


def test_get_resources_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_resources("test-rest_api_id", position="test-position", limit=1, embed=[], region_name="us-east-1")
    mock_client.get_resources.assert_called_once()


def test_get_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.get_rest_api.assert_called_once()


def test_get_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_rest_api("test-rest_api_id", region_name="us-east-1")


def test_get_rest_apis(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rest_apis.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_rest_apis(region_name="us-east-1")
    mock_client.get_rest_apis.assert_called_once()


def test_get_rest_apis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rest_apis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_rest_apis",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_rest_apis(region_name="us-east-1")


def test_get_rest_apis_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_rest_apis.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_rest_apis(position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_rest_apis.assert_called_once()


def test_get_sdk(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", region_name="us-east-1")
    mock_client.get_sdk.assert_called_once()


def test_get_sdk_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sdk",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", region_name="us-east-1")


def test_get_sdk_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", parameters={}, region_name="us-east-1")
    mock_client.get_sdk.assert_called_once()


def test_get_sdk_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk_type.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_sdk_type("test-id", region_name="us-east-1")
    mock_client.get_sdk_type.assert_called_once()


def test_get_sdk_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sdk_type",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_sdk_type("test-id", region_name="us-east-1")


def test_get_sdk_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk_types.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_sdk_types(region_name="us-east-1")
    mock_client.get_sdk_types.assert_called_once()


def test_get_sdk_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sdk_types",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_sdk_types(region_name="us-east-1")


def test_get_sdk_types_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_sdk_types.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_sdk_types(position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_sdk_types.assert_called_once()


def test_get_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.get_stage.assert_called_once()


def test_get_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_stage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


def test_get_stages(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stages.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_stages("test-rest_api_id", region_name="us-east-1")
    mock_client.get_stages.assert_called_once()


def test_get_stages_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_stages",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_stages("test-rest_api_id", region_name="us-east-1")


def test_get_stages_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stages.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_stages("test-rest_api_id", deployment_id="test-deployment_id", region_name="us-east-1")
    mock_client.get_stages.assert_called_once()


def test_get_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tags.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_tags("test-resource_arn", region_name="us-east-1")
    mock_client.get_tags.assert_called_once()


def test_get_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_tags",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_tags("test-resource_arn", region_name="us-east-1")


def test_get_tags_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tags.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_tags("test-resource_arn", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_tags.assert_called_once()


def test_get_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage("test-usage_plan_id", "test-start_date", "test-end_date", region_name="us-east-1")
    mock_client.get_usage.assert_called_once()


def test_get_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_usage("test-usage_plan_id", "test-start_date", "test-end_date", region_name="us-east-1")


def test_get_usage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage("test-usage_plan_id", "test-start_date", "test-end_date", key_id="test-key_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_usage.assert_called_once()


def test_get_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.get_usage_plan.assert_called_once()


def test_get_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_plan",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_usage_plan("test-usage_plan_id", region_name="us-east-1")


def test_get_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.get_usage_plan_key.assert_called_once()


def test_get_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_plan_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")


def test_get_usage_plan_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plan_keys("test-usage_plan_id", region_name="us-east-1")
    mock_client.get_usage_plan_keys.assert_called_once()


def test_get_usage_plan_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_plan_keys",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_usage_plan_keys("test-usage_plan_id", region_name="us-east-1")


def test_get_usage_plan_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plan_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plan_keys("test-usage_plan_id", position="test-position", limit=1, name_query="test-name_query", region_name="us-east-1")
    mock_client.get_usage_plan_keys.assert_called_once()


def test_get_usage_plans(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plans.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plans(region_name="us-east-1")
    mock_client.get_usage_plans.assert_called_once()


def test_get_usage_plans_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plans.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_usage_plans",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_usage_plans(region_name="us-east-1")


def test_get_usage_plans_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_usage_plans.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_usage_plans(position="test-position", key_id="test-key_id", limit=1, region_name="us-east-1")
    mock_client.get_usage_plans.assert_called_once()


def test_get_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.get_vpc_link.assert_called_once()


def test_get_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpc_link",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_vpc_link("test-vpc_link_id", region_name="us-east-1")


def test_get_vpc_links(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_links.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_vpc_links(region_name="us-east-1")
    mock_client.get_vpc_links.assert_called_once()


def test_get_vpc_links_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_links.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_vpc_links",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        get_vpc_links(region_name="us-east-1")


def test_get_vpc_links_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_vpc_links.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    get_vpc_links(position="test-position", limit=1, region_name="us-east-1")
    mock_client.get_vpc_links.assert_called_once()


def test_import_api_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_api_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_api_keys("test-body", "test-format", region_name="us-east-1")
    mock_client.import_api_keys.assert_called_once()


def test_import_api_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_api_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_api_keys",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        import_api_keys("test-body", "test-format", region_name="us-east-1")


def test_import_api_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_api_keys.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_api_keys("test-body", "test-format", fail_on_warnings=True, region_name="us-east-1")
    mock_client.import_api_keys.assert_called_once()


def test_import_documentation_parts(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_documentation_parts.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_documentation_parts("test-rest_api_id", "test-body", region_name="us-east-1")
    mock_client.import_documentation_parts.assert_called_once()


def test_import_documentation_parts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_documentation_parts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_documentation_parts",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        import_documentation_parts("test-rest_api_id", "test-body", region_name="us-east-1")


def test_import_documentation_parts_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_documentation_parts.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_documentation_parts("test-rest_api_id", "test-body", mode="test-mode", fail_on_warnings=True, region_name="us-east-1")
    mock_client.import_documentation_parts.assert_called_once()


def test_import_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_rest_api("test-body", region_name="us-east-1")
    mock_client.import_rest_api.assert_called_once()


def test_import_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        import_rest_api("test-body", region_name="us-east-1")


def test_import_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    import_rest_api("test-body", fail_on_warnings=True, parameters={}, region_name="us-east-1")
    mock_client.import_rest_api.assert_called_once()


def test_put_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.put_gateway_response.assert_called_once()


def test_put_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_gateway_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_gateway_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


def test_put_gateway_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_gateway_response("test-rest_api_id", "test-response_type", status_code="test-status_code", response_parameters={}, response_templates={}, region_name="us-east-1")
    mock_client.put_gateway_response.assert_called_once()


def test_put_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", region_name="us-east-1")
    mock_client.put_integration.assert_called_once()


def test_put_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_integration",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", region_name="us-east-1")


def test_put_integration_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", integration_http_method="test-integration_http_method", uri="test-uri", connection_type="test-connection_type", connection_id="test-connection_id", credentials="test-credentials", request_parameters={}, request_templates={}, passthrough_behavior="test-passthrough_behavior", cache_namespace="test-cache_namespace", cache_key_parameters=[], content_handling="test-content_handling", timeout_in_millis=1, tls_config={}, region_name="us-east-1")
    mock_client.put_integration.assert_called_once()


def test_put_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.put_integration_response.assert_called_once()


def test_put_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_integration_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_put_integration_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", selection_pattern="test-selection_pattern", response_parameters={}, response_templates={}, content_handling="test-content_handling", region_name="us-east-1")
    mock_client.put_integration_response.assert_called_once()


def test_put_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", region_name="us-east-1")
    mock_client.put_method.assert_called_once()


def test_put_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_method",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", region_name="us-east-1")


def test_put_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", authorizer_id="test-authorizer_id", api_key_required=True, operation_name="test-operation_name", request_parameters={}, request_models={}, request_validator_id="test-request_validator_id", authorization_scopes=[], region_name="us-east-1")
    mock_client.put_method.assert_called_once()


def test_put_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.put_method_response.assert_called_once()


def test_put_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_method_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_put_method_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", response_parameters={}, response_models={}, region_name="us-east-1")
    mock_client.put_method_response.assert_called_once()


def test_put_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_rest_api("test-rest_api_id", "test-body", region_name="us-east-1")
    mock_client.put_rest_api.assert_called_once()


def test_put_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        put_rest_api("test-rest_api_id", "test-body", region_name="us-east-1")


def test_put_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    put_rest_api("test-rest_api_id", "test-body", mode="test-mode", fail_on_warnings=True, parameters={}, region_name="us-east-1")
    mock_client.put_rest_api.assert_called_once()


def test_reject_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_domain_name_access_association.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    reject_domain_name_access_association("test-domain_name_access_association_arn", "test-domain_name_arn", region_name="us-east-1")
    mock_client.reject_domain_name_access_association.assert_called_once()


def test_reject_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_domain_name_access_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_domain_name_access_association",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        reject_domain_name_access_association("test-domain_name_access_association_arn", "test-domain_name_arn", region_name="us-east-1")


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name="us-east-1")
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        tag_resource("test-resource_arn", {}, region_name="us-east-1")


def test_run_invoke_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.test_invoke_authorizer.assert_called_once()


def test_run_invoke_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_invoke_authorizer",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


def test_run_invoke_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", headers={}, multi_value_headers={}, path_with_query_string="test-path_with_query_string", body="test-body", stage_variables={}, additional_context={}, region_name="us-east-1")
    mock_client.test_invoke_authorizer.assert_called_once()


def test_run_invoke_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.test_invoke_method.assert_called_once()


def test_run_invoke_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "run_invoke_method",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_run_invoke_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_invoke_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", path_with_query_string="test-path_with_query_string", body="test-body", headers={}, multi_value_headers={}, client_certificate_id="test-client_certificate_id", stage_variables={}, region_name="us-east-1")
    mock_client.test_invoke_method.assert_called_once()


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        untag_resource("test-resource_arn", [], region_name="us-east-1")


def test_update_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_account(region_name="us-east-1")
    mock_client.update_account.assert_called_once()


def test_update_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_account(region_name="us-east-1")


def test_update_account_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_account(patch_operations=[], region_name="us-east-1")
    mock_client.update_account.assert_called_once()


def test_update_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_api_key("test-api_key", region_name="us-east-1")
    mock_client.update_api_key.assert_called_once()


def test_update_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_api_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_api_key",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_api_key("test-api_key", region_name="us-east-1")


def test_update_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_api_key.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_api_key("test-api_key", patch_operations=[], region_name="us-east-1")
    mock_client.update_api_key.assert_called_once()


def test_update_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.update_authorizer.assert_called_once()


def test_update_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_authorizer",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


def test_update_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_authorizer("test-rest_api_id", "test-authorizer_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_authorizer.assert_called_once()


def test_update_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.update_base_path_mapping.assert_called_once()


def test_update_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_base_path_mapping.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_base_path_mapping",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


def test_update_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_base_path_mapping.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_base_path_mapping.assert_called_once()


def test_update_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.update_client_certificate.assert_called_once()


def test_update_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_client_certificate",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_client_certificate("test-client_certificate_id", region_name="us-east-1")


def test_update_client_certificate_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_client_certificate("test-client_certificate_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_client_certificate.assert_called_once()


def test_update_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.update_deployment.assert_called_once()


def test_update_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_deployment",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


def test_update_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_deployment.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_deployment("test-rest_api_id", "test-deployment_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_deployment.assert_called_once()


def test_update_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_part.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.update_documentation_part.assert_called_once()


def test_update_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_part.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_documentation_part",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


def test_update_documentation_part_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_part.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_documentation_part("test-rest_api_id", "test-documentation_part_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_documentation_part.assert_called_once()


def test_update_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.update_documentation_version.assert_called_once()


def test_update_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_documentation_version",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


def test_update_documentation_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_documentation_version.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_documentation_version("test-rest_api_id", "test-documentation_version", patch_operations=[], region_name="us-east-1")
    mock_client.update_documentation_version.assert_called_once()


def test_update_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.update_domain_name.assert_called_once()


def test_update_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_domain_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_domain_name",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_domain_name("test-domain_name", region_name="us-east-1")


def test_update_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_domain_name.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_domain_name("test-domain_name", domain_name_id="test-domain_name_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_domain_name.assert_called_once()


def test_update_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.update_gateway_response.assert_called_once()


def test_update_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_gateway_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


def test_update_gateway_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_gateway_response("test-rest_api_id", "test-response_type", patch_operations=[], region_name="us-east-1")
    mock_client.update_gateway_response.assert_called_once()


def test_update_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.update_integration.assert_called_once()


def test_update_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_integration",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_update_integration_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_integration("test-rest_api_id", "test-resource_id", "test-http_method", patch_operations=[], region_name="us-east-1")
    mock_client.update_integration.assert_called_once()


def test_update_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.update_integration_response.assert_called_once()


def test_update_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_integration_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_update_integration_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_integration_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", patch_operations=[], region_name="us-east-1")
    mock_client.update_integration_response.assert_called_once()


def test_update_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.update_method.assert_called_once()


def test_update_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_method",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


def test_update_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_method("test-rest_api_id", "test-resource_id", "test-http_method", patch_operations=[], region_name="us-east-1")
    mock_client.update_method.assert_called_once()


def test_update_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.update_method_response.assert_called_once()


def test_update_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method_response.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_method_response",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


def test_update_method_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_method_response.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", patch_operations=[], region_name="us-east-1")
    mock_client.update_method_response.assert_called_once()


def test_update_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.update_model.assert_called_once()


def test_update_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_model",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


def test_update_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_model.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_model("test-rest_api_id", "test-model_name", patch_operations=[], region_name="us-east-1")
    mock_client.update_model.assert_called_once()


def test_update_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.update_request_validator.assert_called_once()


def test_update_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_request_validator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_request_validator",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


def test_update_request_validator_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_request_validator.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_request_validator("test-rest_api_id", "test-request_validator_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_request_validator.assert_called_once()


def test_update_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.update_resource.assert_called_once()


def test_update_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


def test_update_resource_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_resource("test-rest_api_id", "test-resource_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_resource.assert_called_once()


def test_update_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.update_rest_api.assert_called_once()


def test_update_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rest_api.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_rest_api",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_rest_api("test-rest_api_id", region_name="us-east-1")


def test_update_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rest_api.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_rest_api("test-rest_api_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_rest_api.assert_called_once()


def test_update_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.update_stage.assert_called_once()


def test_update_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


def test_update_stage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_stage("test-rest_api_id", "test-stage_name", patch_operations=[], region_name="us-east-1")
    mock_client.update_stage.assert_called_once()


def test_update_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_usage("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.update_usage.assert_called_once()


def test_update_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_usage",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_usage("test-usage_plan_id", "test-key_id", region_name="us-east-1")


def test_update_usage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_usage("test-usage_plan_id", "test-key_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_usage.assert_called_once()


def test_update_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.update_usage_plan.assert_called_once()


def test_update_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_plan.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_usage_plan",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_usage_plan("test-usage_plan_id", region_name="us-east-1")


def test_update_usage_plan_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_usage_plan.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_usage_plan("test-usage_plan_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_usage_plan.assert_called_once()


def test_update_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.update_vpc_link.assert_called_once()


def test_update_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vpc_link",
    )
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        update_vpc_link("test-vpc_link_id", region_name="us-east-1")


def test_update_vpc_link_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_link.return_value = {}
    monkeypatch.setattr("aws_util.api_gateway.get_client", lambda *a, **kw: mock_client)
    update_vpc_link("test-vpc_link_id", patch_operations=[], region_name="us-east-1")
    mock_client.update_vpc_link.assert_called_once()


