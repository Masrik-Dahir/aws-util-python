"""Tests for aws_util.aio.api_gateway — 100% line coverage."""
from __future__ import annotations

import asyncio
import base64
import boto3
import json
import time
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel

from aws_util.aio import api_gateway as mod
from aws_util.api_gateway import (
    ThrottleResult,
    ValidationResult,
    WebSocketConnection,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_mock_client(**overrides):
    client = AsyncMock()
    client.call = AsyncMock(**overrides)
    return client


def _make_jwt(payload: dict, header: dict | None = None) -> str:
    """Build a fake JWT (no signature verification)."""
    h = header or {"alg": "RS256", "typ": "JWT"}
    h_enc = base64.urlsafe_b64encode(json.dumps(h).encode()).rstrip(b"=").decode()
    p_enc = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
    return f"{h_enc}.{p_enc}.fake_signature"


RESOURCE = "arn:aws:execute-api:us-east-1:123:api/*/GET/resource"


# ---------------------------------------------------------------------------
# jwt_authorizer
# ---------------------------------------------------------------------------


class TestJwtAuthorizer:
    async def test_valid_token_allow(self):
        payload = {"sub": "user-1", "email": "u@x.com"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"
        assert result["principalId"] == "user-1"

    async def test_invalid_token_format(self):
        result = await mod.jwt_authorizer("not.a.valid", RESOURCE)
        # _decode_jwt_payload should fail with invalid base64
        # Actually, "not.a.valid" has 3 parts but may fail on decode
        # Let's test with truly invalid format
        result = await mod.jwt_authorizer("bad_token", RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_issuer_mismatch(self):
        payload = {"sub": "user-1", "iss": "https://wrong-issuer.com"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            user_pool_id="us-east-1_ABC123",
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_issuer_match(self):
        pool_id = "us-east-1_ABC123"
        payload = {
            "sub": "user-1",
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{pool_id}",
        }
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            user_pool_id=pool_id,
            region_name="us-east-1",
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    async def test_issuer_match_default_region(self):
        """user_pool_id provided without region_name => defaults to us-east-1."""
        pool_id = "us-east-1_ABC123"
        payload = {
            "sub": "user-1",
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{pool_id}",
        }
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            user_pool_id=pool_id,
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    async def test_required_claims_match(self):
        payload = {"sub": "user-1", "scope": "admin"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            required_claims={"scope": "admin"},
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    async def test_required_claims_mismatch(self):
        payload = {"sub": "user-1", "scope": "read"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            required_claims={"scope": "admin"},
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_required_claims_missing(self):
        """Claim is missing from token entirely."""
        payload = {"sub": "user-1"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(
            token, RESOURCE,
            required_claims={"scope": "admin"},
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_expired_token(self):
        payload = {"sub": "user-1", "exp": int(time.time()) - 3600}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_future_exp(self):
        payload = {"sub": "user-1", "exp": int(time.time()) + 3600}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"

    async def test_invalid_exp_type(self):
        """exp is not a valid int => Deny."""
        payload = {"sub": "user-1", "exp": "not-a-number"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_context_fields(self):
        """Only specific fields should be in context."""
        payload = {
            "sub": "user-1",
            "email": "u@x.com",
            "cognito:username": "uname",
            "scope": "admin",
            "client_id": "cid",
            "extra": "should-not-appear",
        }
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        ctx = result.get("context", {})
        assert "sub" in ctx
        assert "email" in ctx
        assert "cognito:username" in ctx
        assert "scope" in ctx
        assert "client_id" in ctx
        assert "extra" not in ctx

    async def test_principal_fallback_to_client_id(self):
        """When sub is missing, principal_id falls back to client_id."""
        payload = {"client_id": "my-client"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        assert result["principalId"] == "my-client"

    async def test_principal_fallback_to_unknown(self):
        """When both sub and client_id are missing, principal_id is 'unknown'."""
        payload = {"email": "test@x.com"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        assert result["principalId"] == "unknown"

    async def test_exp_none_not_checked(self):
        """When exp is not present, token is not expired."""
        payload = {"sub": "user-1"}
        token = _make_jwt(payload)

        result = await mod.jwt_authorizer(token, RESOURCE)
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"


# ---------------------------------------------------------------------------
# api_key_authorizer
# ---------------------------------------------------------------------------


class TestApiKeyAuthorizer:
    async def test_valid_key_with_description(self, monkeypatch):
        mock_client = _make_mock_client(
            return_value={
                "Item": {
                    "api_key": {"S": "key-123"},
                    "enabled": {"BOOL": True},
                    "owner": {"S": "owner-1"},
                    "description": {"S": "My key"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "key-123", "keys-table", RESOURCE,
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Allow"
        assert result["principalId"] == "owner-1"
        assert result["context"]["description"] == "My key"

    async def test_valid_key_no_description(self, monkeypatch):
        mock_client = _make_mock_client(
            return_value={
                "Item": {
                    "api_key": {"S": "key-123"},
                    "enabled": {"BOOL": True},
                    "owner": {"S": "owner-1"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "key-123", "keys-table", RESOURCE,
        )
        assert "description" not in result.get("context", {})

    async def test_key_not_found(self, monkeypatch):
        mock_client = _make_mock_client(return_value={})
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "missing", "keys-table", RESOURCE,
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_key_disabled(self, monkeypatch):
        mock_client = _make_mock_client(
            return_value={
                "Item": {
                    "api_key": {"S": "key-123"},
                    "enabled": {"BOOL": False},
                    "owner": {"S": "owner-1"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "key-123", "keys-table", RESOURCE,
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_lookup_exception(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=RuntimeError("db error")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "key-123", "keys-table", RESOURCE,
        )
        stmt = result["policyDocument"]["Statement"][0]
        assert stmt["Effect"] == "Deny"

    async def test_missing_owner(self, monkeypatch):
        """Owner missing from item => defaults to 'unknown'."""
        mock_client = _make_mock_client(
            return_value={
                "Item": {
                    "api_key": {"S": "key-123"},
                    "enabled": {"BOOL": True},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.api_key_authorizer(
            "key-123", "keys-table", RESOURCE,
        )
        assert result["principalId"] == "unknown"


# ---------------------------------------------------------------------------
# request_validator
# ---------------------------------------------------------------------------


class TestRequestValidator:
    async def test_none_body(self):
        result = await mod.request_validator(None, BaseModel)
        assert result.valid is False
        assert "required" in result.errors[0]

    async def test_invalid_json(self):
        result = await mod.request_validator("{bad", BaseModel)
        assert result.valid is False
        assert "Invalid JSON" in result.errors[0]

    async def test_valid_model(self):
        class MyModel(BaseModel):
            name: str
            age: int

        result = await mod.request_validator(
            '{"name": "Alice", "age": 30}', MyModel,
        )
        assert result.valid is True
        assert result.errors == []

    async def test_validation_error_with_loc(self):
        class MyModel(BaseModel):
            name: str
            age: int

        result = await mod.request_validator(
            '{"name": 123}', MyModel,
        )
        assert result.valid is False
        assert len(result.errors) > 0

    async def test_validation_error_without_errors_method(self, monkeypatch):
        """Covers the branch where exc has no 'errors' attribute."""

        class BadModel(BaseModel):
            value: int

        # Patch model_validate to raise a plain Exception (no .errors())
        monkeypatch.setattr(
            BadModel, "model_validate",
            staticmethod(lambda data: (_ for _ in ()).throw(Exception("custom error"))),
        )

        result = await mod.request_validator('{"value": 1}', BadModel)
        assert result.valid is False
        assert "custom error" in result.errors[0]


# ---------------------------------------------------------------------------
# throttle_guard
# ---------------------------------------------------------------------------


class TestThrottleGuard:
    async def test_under_limit(self, monkeypatch):
        mock_client = _make_mock_client(
            return_value={
                "Attributes": {
                    "request_count": {"N": "5"},
                    "ttl": {"N": "9999999999"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard("user-1", "throttle-table")
        assert result.allowed is True
        assert result.current_count == 5

    async def test_over_limit(self, monkeypatch):
        mock_client = _make_mock_client(
            return_value={
                "Attributes": {
                    "request_count": {"N": "101"},
                    "ttl": {"N": "9999999999"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard(
            "user-1", "throttle-table", limit=100,
        )
        assert result.allowed is False
        assert result.current_count == 101

    async def test_at_limit(self, monkeypatch):
        """Exactly at the limit should be allowed (<=)."""
        mock_client = _make_mock_client(
            return_value={
                "Attributes": {
                    "request_count": {"N": "100"},
                    "ttl": {"N": "9999999999"},
                },
            }
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard(
            "user-1", "throttle-table", limit=100,
        )
        assert result.allowed is True

    async def test_dynamo_error_allows(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=RuntimeError("dynamo down")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard("user-1", "throttle-table")
        assert result.allowed is True
        assert result.current_count == 0

    async def test_missing_attributes(self, monkeypatch):
        """Empty Attributes should default to 0."""
        mock_client = _make_mock_client(
            return_value={"Attributes": {}}
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard("user-1", "throttle-table")
        assert result.current_count == 0
        assert result.allowed is True

    async def test_no_attributes_key(self, monkeypatch):
        """Missing Attributes key entirely."""
        mock_client = _make_mock_client(return_value={})
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        result = await mod.throttle_guard("user-1", "throttle-table")
        assert result.current_count == 0


# ---------------------------------------------------------------------------
# websocket_connect
# ---------------------------------------------------------------------------


class TestWebsocketConnect:
    async def test_success(self, monkeypatch):
        mock_client = _make_mock_client(return_value={})
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        await mod.websocket_connect("conn-1", "ws-table")
        mock_client.call.assert_awaited_once()

    async def test_with_metadata(self, monkeypatch):
        mock_client = _make_mock_client(return_value={})
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        await mod.websocket_connect(
            "conn-1", "ws-table",
            metadata={"user_id": "u1"},
        )
        call_kwargs = mock_client.call.call_args.kwargs
        assert "user_id" in call_kwargs["Item"]

    async def test_runtime_error(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=RuntimeError("put fail")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="put fail"):
            await mod.websocket_connect("conn-1", "ws-table")

    async def test_generic_error(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=ValueError("bad put")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to store WebSocket"):
            await mod.websocket_connect("conn-1", "ws-table")


# ---------------------------------------------------------------------------
# websocket_disconnect
# ---------------------------------------------------------------------------


class TestWebsocketDisconnect:
    async def test_success(self, monkeypatch):
        mock_client = _make_mock_client(return_value={})
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        await mod.websocket_disconnect("conn-1", "ws-table")

    async def test_runtime_error(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=RuntimeError("del fail")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="del fail"):
            await mod.websocket_disconnect("conn-1", "ws-table")

    async def test_generic_error(self, monkeypatch):
        mock_client = _make_mock_client(
            side_effect=TypeError("bad del")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to remove WebSocket"):
            await mod.websocket_disconnect("conn-1", "ws-table")


# ---------------------------------------------------------------------------
# websocket_list_connections
# ---------------------------------------------------------------------------


class TestWebsocketListConnections:
    async def test_success(self, monkeypatch):
        mock_client = AsyncMock()
        mock_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                    "user": {"S": "u1"},
                },
                {
                    "connection_id": {"S": "c2"},
                    "connected_at": {"N": "2000"},
                },
            ]
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        conns = await mod.websocket_list_connections("ws-table")
        assert len(conns) == 2
        assert conns[0].connection_id == "c1"
        assert conns[0].metadata == {"user": "u1"}
        assert conns[1].connected_at == 2000

    async def test_empty(self, monkeypatch):
        mock_client = AsyncMock()
        mock_client.paginate = AsyncMock(return_value=[])
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        conns = await mod.websocket_list_connections("ws-table")
        assert conns == []

    async def test_runtime_error(self, monkeypatch):
        mock_client = AsyncMock()
        mock_client.paginate = AsyncMock(
            side_effect=RuntimeError("scan fail")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="scan fail"):
            await mod.websocket_list_connections("ws-table")

    async def test_generic_error(self, monkeypatch):
        mock_client = AsyncMock()
        mock_client.paginate = AsyncMock(
            side_effect=ValueError("bad scan")
        )
        monkeypatch.setattr(mod, "async_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to list WebSocket"):
            await mod.websocket_list_connections("ws-table")


# ---------------------------------------------------------------------------
# websocket_broadcast
# ---------------------------------------------------------------------------


class TestWebsocketBroadcast:
    async def test_send_string_message(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        # Mock boto3.client for apigatewaymanagementapi
        mock_apigw = MagicMock()
        mock_apigw.post_to_connection = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(return_value=None),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com/stage",
            "hello world",
        )
        assert result["sent"] == 1
        assert result["stale"] == 0

    async def test_send_dict_message(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(return_value=None),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com",
            {"type": "update", "data": [1, 2]},
        )
        assert result["sent"] == 1

    async def test_send_list_message(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(return_value=None),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com",
            [1, 2, 3],
        )
        assert result["sent"] == 1

    async def test_gone_exception_removes_stale(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        # For disconnect call
        mock_paginate_client.call = AsyncMock(return_value={})
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )

        # Simulate GoneException
        gone_exc = Exception("GoneException")
        gone_exc.response = {"Error": {"Code": "GoneException"}}
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(side_effect=gone_exc),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com", "hello",
        )
        assert result["stale"] == 1
        assert result["sent"] == 0

    async def test_other_exception_logged(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )

        # Exception without .response attribute
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(side_effect=RuntimeError("network")),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com", "hello",
        )
        assert result["sent"] == 0
        assert result["stale"] == 0

    async def test_exception_with_non_gone_code(self, monkeypatch):
        """Exception with .response but not GoneException."""
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(
            return_value=[
                {
                    "connection_id": {"S": "c1"},
                    "connected_at": {"N": "1000"},
                },
            ]
        )
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )

        exc = Exception("LimitExceededException")
        exc.response = {"Error": {"Code": "LimitExceededException"}}
        monkeypatch.setattr(
            asyncio, "to_thread",
            AsyncMock(side_effect=exc),
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com", "hello",
        )
        assert result["sent"] == 0
        assert result["stale"] == 0

    async def test_no_connections(self, monkeypatch):
        mock_paginate_client = AsyncMock()
        mock_paginate_client.paginate = AsyncMock(return_value=[])
        monkeypatch.setattr(
            mod, "async_client",
            lambda *a, **kw: mock_paginate_client,
        )

        mock_apigw = MagicMock()
        monkeypatch.setattr(
            boto3, "client",
            lambda *a, **kw: mock_apigw,
        )

        result = await mod.websocket_broadcast(
            "ws-table", "https://ws.example.com", "hello",
        )
        assert result["sent"] == 0
        assert result["stale"] == 0
# Generated async tests for boto3 wrapper methods
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.api_gateway import (
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


async def test_create_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_api_key(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_api_key(region_name="us-east-1")


async def test_create_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_authorizer("test-rest_api_id", "test-name", "test-type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_authorizer("test-rest_api_id", "test-name", "test-type", region_name="us-east-1")


async def test_create_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_base_path_mapping("test-domain_name", "test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_base_path_mapping("test-domain_name", "test-rest_api_id", region_name="us-east-1")


async def test_create_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_deployment("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_deployment("test-rest_api_id", region_name="us-east-1")


async def test_create_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_documentation_part("test-rest_api_id", {}, "test-properties", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_documentation_part("test-rest_api_id", {}, "test-properties", region_name="us-east-1")


async def test_create_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


async def test_create_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_domain_name("test-domain_name", region_name="us-east-1")


async def test_create_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", region_name="us-east-1")


async def test_create_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_model("test-rest_api_id", "test-name", "test-content_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_model("test-rest_api_id", "test-name", "test-content_type", region_name="us-east-1")


async def test_create_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_request_validator("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_request_validator("test-rest_api_id", region_name="us-east-1")


async def test_create_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_resource("test-rest_api_id", "test-parent_id", "test-path_part", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_resource("test-rest_api_id", "test-parent_id", "test-path_part", region_name="us-east-1")


async def test_create_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_rest_api("test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_rest_api("test-name", region_name="us-east-1")


async def test_create_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", region_name="us-east-1")


async def test_create_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_usage_plan("test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_usage_plan("test-name", region_name="us-east-1")


async def test_create_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_usage_plan_key("test-usage_plan_id", "test-key_id", "test-key_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_usage_plan_key("test-usage_plan_id", "test-key_id", "test-key_type", region_name="us-east-1")


async def test_create_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_vpc_link("test-name", [], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await create_vpc_link("test-name", [], region_name="us-east-1")


async def test_delete_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_api_key("test-api_key", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_api_key("test-api_key", region_name="us-east-1")


async def test_delete_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


async def test_delete_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


async def test_delete_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_client_certificate("test-client_certificate_id", region_name="us-east-1")


async def test_delete_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


async def test_delete_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


async def test_delete_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


async def test_delete_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_domain_name("test-domain_name", region_name="us-east-1")


async def test_delete_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_domain_name_access_association("test-domain_name_access_association_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_domain_name_access_association("test-domain_name_access_association_arn", region_name="us-east-1")


async def test_delete_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


async def test_delete_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_delete_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_delete_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_delete_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_delete_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


async def test_delete_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


async def test_delete_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


async def test_delete_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_rest_api("test-rest_api_id", region_name="us-east-1")


async def test_delete_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


async def test_delete_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_usage_plan("test-usage_plan_id", region_name="us-east-1")


async def test_delete_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")


async def test_delete_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await delete_vpc_link("test-vpc_link_id", region_name="us-east-1")


async def test_flush_stage_authorizers_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await flush_stage_authorizers_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_flush_stage_authorizers_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await flush_stage_authorizers_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")


async def test_flush_stage_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await flush_stage_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_flush_stage_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await flush_stage_cache("test-rest_api_id", "test-stage_name", region_name="us-east-1")


async def test_generate_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await generate_client_certificate(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_generate_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await generate_client_certificate(region_name="us-east-1")


async def test_get_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_account(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_account(region_name="us-east-1")


async def test_get_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_api_key("test-api_key", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_api_key("test-api_key", region_name="us-east-1")


async def test_get_api_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_api_keys(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_api_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_api_keys(region_name="us-east-1")


async def test_get_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


async def test_get_authorizers(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_authorizers("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_authorizers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_authorizers("test-rest_api_id", region_name="us-east-1")


async def test_get_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


async def test_get_base_path_mappings(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_base_path_mappings("test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_base_path_mappings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_base_path_mappings("test-domain_name", region_name="us-east-1")


async def test_get_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_client_certificate("test-client_certificate_id", region_name="us-east-1")


async def test_get_client_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_client_certificates(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_client_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_client_certificates(region_name="us-east-1")


async def test_get_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


async def test_get_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_deployments("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_deployments("test-rest_api_id", region_name="us-east-1")


async def test_get_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


async def test_get_documentation_parts(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_parts("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_parts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_documentation_parts("test-rest_api_id", region_name="us-east-1")


async def test_get_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


async def test_get_documentation_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_versions("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_documentation_versions("test-rest_api_id", region_name="us-east-1")


async def test_get_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_domain_name("test-domain_name", region_name="us-east-1")


async def test_get_domain_name_access_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_name_access_associations(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_name_access_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_domain_name_access_associations(region_name="us-east-1")


async def test_get_domain_names(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_names(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_names_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_domain_names(region_name="us-east-1")


async def test_get_export(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_export("test-rest_api_id", "test-stage_name", "test-export_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_export_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_export("test-rest_api_id", "test-stage_name", "test-export_type", region_name="us-east-1")


async def test_get_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


async def test_get_gateway_responses(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_gateway_responses("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_gateway_responses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_gateway_responses("test-rest_api_id", region_name="us-east-1")


async def test_get_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_get_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_get_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_get_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_get_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


async def test_get_model_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_model_template("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_model_template("test-rest_api_id", "test-model_name", region_name="us-east-1")


async def test_get_models(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_models("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_models_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_models("test-rest_api_id", region_name="us-east-1")


async def test_get_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


async def test_get_request_validators(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_request_validators("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_request_validators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_request_validators("test-rest_api_id", region_name="us-east-1")


async def test_get_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


async def test_get_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_resources("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_resources("test-rest_api_id", region_name="us-east-1")


async def test_get_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_rest_api("test-rest_api_id", region_name="us-east-1")


async def test_get_rest_apis(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_rest_apis(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_rest_apis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_rest_apis(region_name="us-east-1")


async def test_get_sdk(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_sdk_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", region_name="us-east-1")


async def test_get_sdk_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_sdk_type("test-id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_sdk_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_sdk_type("test-id", region_name="us-east-1")


async def test_get_sdk_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_sdk_types(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_sdk_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_sdk_types(region_name="us-east-1")


async def test_get_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


async def test_get_stages(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_stages("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_stages_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_stages("test-rest_api_id", region_name="us-east-1")


async def test_get_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_tags("test-resource_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_tags("test-resource_arn", region_name="us-east-1")


async def test_get_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage("test-usage_plan_id", "test-start_date", "test-end_date", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_usage("test-usage_plan_id", "test-start_date", "test-end_date", region_name="us-east-1")


async def test_get_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_usage_plan("test-usage_plan_id", region_name="us-east-1")


async def test_get_usage_plan_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plan_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_usage_plan_key("test-usage_plan_id", "test-key_id", region_name="us-east-1")


async def test_get_usage_plan_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plan_keys("test-usage_plan_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plan_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_usage_plan_keys("test-usage_plan_id", region_name="us-east-1")


async def test_get_usage_plans(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plans(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plans_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_usage_plans(region_name="us-east-1")


async def test_get_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_vpc_link("test-vpc_link_id", region_name="us-east-1")


async def test_get_vpc_links(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_vpc_links(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_vpc_links_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await get_vpc_links(region_name="us-east-1")


async def test_import_api_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_api_keys("test-body", "test-format", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_api_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await import_api_keys("test-body", "test-format", region_name="us-east-1")


async def test_import_documentation_parts(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_documentation_parts("test-rest_api_id", "test-body", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_documentation_parts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await import_documentation_parts("test-rest_api_id", "test-body", region_name="us-east-1")


async def test_import_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_rest_api("test-body", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await import_rest_api("test-body", region_name="us-east-1")


async def test_put_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


async def test_put_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", region_name="us-east-1")


async def test_put_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_put_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", region_name="us-east-1")


async def test_put_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_put_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_rest_api("test-rest_api_id", "test-body", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await put_rest_api("test-rest_api_id", "test-body", region_name="us-east-1")


async def test_reject_domain_name_access_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await reject_domain_name_access_association("test-domain_name_access_association_arn", "test-domain_name_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_reject_domain_name_access_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await reject_domain_name_access_association("test-domain_name_access_association_arn", "test-domain_name_arn", region_name="us-east-1")


async def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await tag_resource("test-resource_arn", {}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await tag_resource("test-resource_arn", {}, region_name="us-east-1")


async def test_run_invoke_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_run_invoke_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


async def test_run_invoke_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_run_invoke_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await untag_resource("test-resource_arn", [], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await untag_resource("test-resource_arn", [], region_name="us-east-1")


async def test_update_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_account(region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_account(region_name="us-east-1")


async def test_update_api_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_api_key("test-api_key", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_api_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_api_key("test-api_key", region_name="us-east-1")


async def test_update_authorizer(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_authorizer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_authorizer("test-rest_api_id", "test-authorizer_id", region_name="us-east-1")


async def test_update_base_path_mapping(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_base_path_mapping_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_base_path_mapping("test-domain_name", "test-base_path", region_name="us-east-1")


async def test_update_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_client_certificate("test-client_certificate_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_client_certificate("test-client_certificate_id", region_name="us-east-1")


async def test_update_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_deployment("test-rest_api_id", "test-deployment_id", region_name="us-east-1")


async def test_update_documentation_part(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_documentation_part_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_documentation_part("test-rest_api_id", "test-documentation_part_id", region_name="us-east-1")


async def test_update_documentation_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_documentation_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_documentation_version("test-rest_api_id", "test-documentation_version", region_name="us-east-1")


async def test_update_domain_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_domain_name("test-domain_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_domain_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_domain_name("test-domain_name", region_name="us-east-1")


async def test_update_gateway_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_gateway_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_gateway_response("test-rest_api_id", "test-response_type", region_name="us-east-1")


async def test_update_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_integration("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_update_integration_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_integration_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_update_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_method("test-rest_api_id", "test-resource_id", "test-http_method", region_name="us-east-1")


async def test_update_method_response(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_method_response_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", region_name="us-east-1")


async def test_update_model(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_model("test-rest_api_id", "test-model_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_model_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_model("test-rest_api_id", "test-model_name", region_name="us-east-1")


async def test_update_request_validator(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_request_validator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_request_validator("test-rest_api_id", "test-request_validator_id", region_name="us-east-1")


async def test_update_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_resource("test-rest_api_id", "test-resource_id", region_name="us-east-1")


async def test_update_rest_api(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_rest_api("test-rest_api_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_rest_api_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_rest_api("test-rest_api_id", region_name="us-east-1")


async def test_update_stage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_stage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_stage("test-rest_api_id", "test-stage_name", region_name="us-east-1")


async def test_update_usage(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_usage("test-usage_plan_id", "test-key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_usage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_usage("test-usage_plan_id", "test-key_id", region_name="us-east-1")


async def test_update_usage_plan(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_usage_plan("test-usage_plan_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_usage_plan_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_usage_plan("test-usage_plan_id", region_name="us-east-1")


async def test_update_vpc_link(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_vpc_link("test-vpc_link_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_vpc_link_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(side_effect=RuntimeError("fail"))
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError):
        await update_vpc_link("test-vpc_link_id", region_name="us-east-1")


async def test_create_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_api_key(name="test-name", description="test-description", enabled=True, generate_distinct_id=True, value="test-value", stage_keys=[], customer_id="test-customer_id", tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_authorizer("test-rest_api_id", "test-name", "test-type", provider_ar_ns=[], auth_type="test-auth_type", authorizer_uri="test-authorizer_uri", authorizer_credentials="test-authorizer_credentials", identity_source="test-identity_source", identity_validation_expression="test-identity_validation_expression", authorizer_result_ttl_in_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_base_path_mapping("test-domain_name", "test-rest_api_id", domain_name_id="test-domain_name_id", base_path="test-base_path", stage="test-stage", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_deployment("test-rest_api_id", stage_name="test-stage_name", stage_description="test-stage_description", description="test-description", cache_cluster_enabled=True, cache_cluster_size="test-cache_cluster_size", variables={}, canary_settings={}, tracing_enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_documentation_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_documentation_version("test-rest_api_id", "test-documentation_version", stage_name="test-stage_name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_domain_name("test-domain_name", certificate_name="test-certificate_name", certificate_body="test-certificate_body", certificate_private_key="test-certificate_private_key", certificate_chain="test-certificate_chain", certificate_arn="test-certificate_arn", regional_certificate_name="test-regional_certificate_name", regional_certificate_arn="test-regional_certificate_arn", endpoint_configuration={}, tags={}, security_policy="test-security_policy", mutual_tls_authentication={}, ownership_verification_certificate_arn="test-ownership_verification_certificate_arn", policy="test-policy", routing_mode="test-routing_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_domain_name_access_association_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_domain_name_access_association("test-domain_name_arn", "test-access_association_source_type", "test-access_association_source", tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_model("test-rest_api_id", "test-name", "test-content_type", description="test-description", model_schema="test-model_schema", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_request_validator_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_request_validator("test-rest_api_id", name="test-name", validate_request_body=True, validate_request_parameters=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_rest_api("test-name", description="test-description", version="test-version", clone_from="test-clone_from", binary_media_types=[], minimum_compression_size=1, api_key_source="test-api_key_source", endpoint_configuration={}, policy="test-policy", tags={}, disable_execute_api_endpoint=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_stage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_stage("test-rest_api_id", "test-stage_name", "test-deployment_id", description="test-description", cache_cluster_enabled=True, cache_cluster_size="test-cache_cluster_size", variables={}, documentation_version="test-documentation_version", canary_settings={}, tracing_enabled=True, tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_usage_plan_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_usage_plan("test-name", description="test-description", api_stages=[], throttle={}, quota={}, tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_create_vpc_link_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await create_vpc_link("test-name", [], description="test-description", tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_delete_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_domain_name("test-domain_name", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_generate_client_certificate_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await generate_client_certificate(description="test-description", tags={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_api_key("test-api_key", include_value=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_api_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_api_keys(position="test-position", limit=1, name_query="test-name_query", customer_id="test-customer_id", include_values=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_authorizers_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_authorizers("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_base_path_mappings_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_base_path_mappings("test-domain_name", domain_name_id="test-domain_name_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_client_certificates_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_client_certificates(position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_deployment("test-rest_api_id", "test-deployment_id", embed=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_deployments_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_deployments("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_parts_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_parts("test-rest_api_id", type="test-type", name_query="test-name_query", path="test-path", position="test-position", limit=1, location_status="test-location_status", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_documentation_versions_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_documentation_versions("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_name("test-domain_name", domain_name_id="test-domain_name_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_name_access_associations_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_name_access_associations(position="test-position", limit=1, resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_domain_names_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_domain_names(position="test-position", limit=1, resource_owner="test-resource_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_export_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_export("test-rest_api_id", "test-stage_name", "test-export_type", parameters={}, accepts="test-accepts", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_gateway_responses_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_gateway_responses("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_model("test-rest_api_id", "test-model_name", flatten=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_models_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_models("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_request_validators_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_request_validators("test-rest_api_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_resource_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_resource("test-rest_api_id", "test-resource_id", embed=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_resources_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_resources("test-rest_api_id", position="test-position", limit=1, embed=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_rest_apis_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_rest_apis(position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_sdk_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_sdk("test-rest_api_id", "test-stage_name", "test-sdk_type", parameters={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_sdk_types_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_sdk_types(position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_stages_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_stages("test-rest_api_id", deployment_id="test-deployment_id", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_tags_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_tags("test-resource_arn", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage("test-usage_plan_id", "test-start_date", "test-end_date", key_id="test-key_id", position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plan_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plan_keys("test-usage_plan_id", position="test-position", limit=1, name_query="test-name_query", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_usage_plans_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_usage_plans(position="test-position", key_id="test-key_id", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_get_vpc_links_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await get_vpc_links(position="test-position", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_api_keys_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_api_keys("test-body", "test-format", fail_on_warnings=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_documentation_parts_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_documentation_parts("test-rest_api_id", "test-body", mode="test-mode", fail_on_warnings=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_import_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await import_rest_api("test-body", fail_on_warnings=True, parameters={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_gateway_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_gateway_response("test-rest_api_id", "test-response_type", status_code="test-status_code", response_parameters={}, response_templates={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_integration_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_integration("test-rest_api_id", "test-resource_id", "test-http_method", "test-type", integration_http_method="test-integration_http_method", uri="test-uri", connection_type="test-connection_type", connection_id="test-connection_id", credentials="test-credentials", request_parameters={}, request_templates={}, passthrough_behavior="test-passthrough_behavior", cache_namespace="test-cache_namespace", cache_key_parameters=[], content_handling="test-content_handling", timeout_in_millis=1, tls_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_integration_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", selection_pattern="test-selection_pattern", response_parameters={}, response_templates={}, content_handling="test-content_handling", region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_method("test-rest_api_id", "test-resource_id", "test-http_method", "test-authorization_type", authorizer_id="test-authorizer_id", api_key_required=True, operation_name="test-operation_name", request_parameters={}, request_models={}, request_validator_id="test-request_validator_id", authorization_scopes=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_method_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", response_parameters={}, response_models={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_put_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await put_rest_api("test-rest_api_id", "test-body", mode="test-mode", fail_on_warnings=True, parameters={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_run_invoke_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await run_invoke_authorizer("test-rest_api_id", "test-authorizer_id", headers={}, multi_value_headers={}, path_with_query_string="test-path_with_query_string", body="test-body", stage_variables={}, additional_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_run_invoke_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await run_invoke_method("test-rest_api_id", "test-resource_id", "test-http_method", path_with_query_string="test-path_with_query_string", body="test-body", headers={}, multi_value_headers={}, client_certificate_id="test-client_certificate_id", stage_variables={}, region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_account_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_account(patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_api_key_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_api_key("test-api_key", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_authorizer_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_authorizer("test-rest_api_id", "test-authorizer_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_base_path_mapping_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_base_path_mapping("test-domain_name", "test-base_path", domain_name_id="test-domain_name_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_client_certificate_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_client_certificate("test-client_certificate_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_deployment_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_deployment("test-rest_api_id", "test-deployment_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_documentation_part_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_documentation_part("test-rest_api_id", "test-documentation_part_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_documentation_version_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_documentation_version("test-rest_api_id", "test-documentation_version", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_domain_name_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_domain_name("test-domain_name", domain_name_id="test-domain_name_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_gateway_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_gateway_response("test-rest_api_id", "test-response_type", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_integration_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_integration("test-rest_api_id", "test-resource_id", "test-http_method", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_integration_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_integration_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_method_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_method("test-rest_api_id", "test-resource_id", "test-http_method", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_method_response_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_method_response("test-rest_api_id", "test-resource_id", "test-http_method", "test-status_code", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_model_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_model("test-rest_api_id", "test-model_name", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_request_validator_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_request_validator("test-rest_api_id", "test-request_validator_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_resource_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_resource("test-rest_api_id", "test-resource_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_rest_api_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_rest_api("test-rest_api_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_stage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_stage("test-rest_api_id", "test-stage_name", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_usage_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_usage("test-usage_plan_id", "test-key_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_usage_plan_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_usage_plan("test-usage_plan_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()


async def test_update_vpc_link_with_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.api_gateway.async_client", lambda *a, **kw: mock_client)
    await update_vpc_link("test-vpc_link_id", patch_operations=[], region_name="us-east-1")
    mock_client.call.assert_called_once()

