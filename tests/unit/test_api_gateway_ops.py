"""Tests for aws_util.api_gateway_ops module."""
from __future__ import annotations

import base64
import json
import time
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.api_gateway_ops as mod
from aws_util.api_gateway_ops import (
    DomainMigrationResult,
    JwtAuthResult,
    RateLimitResult,
    UsagePlanResult,
    WebSocketSessionResult,
    api_gateway_domain_migrator,
    apigw_usage_plan_enforcer,
    jwt_lambda_authorizer,
    rate_limiter,
    websocket_session_manager,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


def _make_jwt(claims: dict[str, Any]) -> str:
    """Build a fake 3-part JWT from claims dict."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    sig = base64.urlsafe_b64encode(b"fakesig").rstrip(b"=").decode()
    return f"{header}.{payload}.{sig}"


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_websocket_session_result(self) -> None:
        r = WebSocketSessionResult(action="connect", connections_affected=1, stale_removed=0)
        assert r.action == "connect"
        assert r.connections_affected == 1
        assert r.stale_removed == 0

    def test_jwt_auth_result(self) -> None:
        r = JwtAuthResult(is_valid=True, principal_id="user1", claims={"sub": "user1"}, cached_jwks=True)
        assert r.is_valid is True
        assert r.cached_jwks is True

    def test_usage_plan_result(self) -> None:
        r = UsagePlanResult(plan_id="p1", api_key_id="k1", api_key_value="val")
        assert r.plan_id == "p1"

    def test_rate_limit_result(self) -> None:
        r = RateLimitResult(allowed=True, current_count=5, remaining=95, retry_after_seconds=0)
        assert r.allowed is True
        assert r.remaining == 95

    def test_domain_migration_result(self) -> None:
        r = DomainMigrationResult(
            domain_name="api.example.com",
            regional_domain_name="d-abc.execute-api.us-east-1.amazonaws.com",
            hosted_zone_id="Z123",
            route53_change_id="/change/C1",
        )
        assert r.domain_name == "api.example.com"

    def test_frozen_models(self) -> None:
        r = WebSocketSessionResult(action="connect", connections_affected=1, stale_removed=0)
        with pytest.raises(Exception):
            r.action = "disconnect"  # type: ignore[misc]


# ==================================================================
# _decode_jwt_claims
# ==================================================================


class TestDecodeJwtClaims:
    def test_valid_token(self) -> None:
        claims = {"sub": "user1", "exp": 9999999999}
        token = _make_jwt(claims)
        decoded = mod._decode_jwt_claims(token)
        assert decoded["sub"] == "user1"
        assert decoded["exp"] == 9999999999

    def test_malformed_token_too_few_parts(self) -> None:
        with pytest.raises(ValueError, match="Malformed JWT"):
            mod._decode_jwt_claims("only.two")

    def test_malformed_token_too_many_parts(self) -> None:
        with pytest.raises(ValueError, match="Malformed JWT"):
            mod._decode_jwt_claims("a.b.c.d")


# ==================================================================
# websocket_session_manager
# ==================================================================


class TestWebsocketSessionManager:
    def _factory(self, ddb: MagicMock) -> Any:
        def get_client(service, **kw):
            if service == "dynamodb":
                return ddb
            return _mock()
        return get_client

    def test_connect_success(self, monkeypatch) -> None:
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        # Patch boto3.client for apigw_mgmt
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            result = websocket_session_manager(
                table_name="ws-table",
                endpoint_url="https://api.example.com/prod",
                action="connect",
                connection_id="conn-123",
                region_name=REGION,
            )
        assert result.action == "connect"
        assert result.connections_affected == 1
        assert result.stale_removed == 0
        ddb.put_item.assert_called_once()

    def test_connect_missing_connection_id(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: _mock())
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(ValueError, match="connection_id is required"):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x", action="connect",
                )

    def test_connect_ddb_error(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(RuntimeError):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x",
                    action="connect", connection_id="c1",
                )

    def test_disconnect_success(self, monkeypatch) -> None:
        ddb = _mock()
        apigw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="disconnect", connection_id="c1",
            )
        assert result.action == "disconnect"
        assert result.connections_affected == 1
        ddb.delete_item.assert_called_once()
        apigw.delete_connection.assert_called_once_with(ConnectionId="c1")

    def test_disconnect_missing_connection_id(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: _mock())
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(ValueError, match="connection_id is required"):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x", action="disconnect",
                )

    def test_disconnect_ddb_error(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.delete_item.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(RuntimeError):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x",
                    action="disconnect", connection_id="c1",
                )

    def test_disconnect_apigw_already_gone(self, monkeypatch) -> None:
        ddb = _mock()
        apigw = _mock()
        apigw.delete_connection.side_effect = _client_error("GoneException")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="disconnect", connection_id="c1",
            )
        # Should succeed even though the connection was already gone
        assert result.connections_affected == 1

    def test_broadcast_success(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.return_value = {
            "Items": [
                {"connection_id": {"S": "c1"}},
                {"connection_id": {"S": "c2"}},
            ]
        }
        apigw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="broadcast", message="hello",
            )
        assert result.action == "broadcast"
        assert result.connections_affected == 2
        assert result.stale_removed == 0
        assert apigw.post_to_connection.call_count == 2

    def test_broadcast_missing_message(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: _mock())
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(ValueError, match="message is required"):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x",
                    action="broadcast",
                )

    def test_broadcast_stale_connections_purged(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.return_value = {
            "Items": [
                {"connection_id": {"S": "c1"}},
                {"connection_id": {"S": "c2"}},
            ]
        }
        apigw = _mock()
        # c1 succeeds, c2 is stale
        apigw.post_to_connection.side_effect = [
            None,
            _client_error("GoneException"),
        ]
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="broadcast", message="hello",
            )
        assert result.connections_affected == 1
        assert result.stale_removed == 1

    def test_broadcast_stale_purge_fails_gracefully(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.return_value = {"Items": [{"connection_id": {"S": "c1"}}]}
        # delete_item fails when purging stale connection
        ddb.delete_item.side_effect = _client_error("InternalServerError")
        apigw = _mock()
        apigw.post_to_connection.side_effect = _client_error("GoneException")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="broadcast", message="hello",
            )
        assert result.stale_removed == 1

    def test_broadcast_forbidden_connection(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.return_value = {"Items": [{"connection_id": {"S": "c1"}}]}
        apigw = _mock()
        apigw.post_to_connection.side_effect = _client_error("ForbiddenException")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="broadcast", message="hello",
            )
        assert result.stale_removed == 1

    def test_broadcast_other_post_error_logged(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.return_value = {"Items": [{"connection_id": {"S": "c1"}}]}
        apigw = _mock()
        apigw.post_to_connection.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=apigw):
            result = websocket_session_manager(
                table_name="t", endpoint_url="https://x",
                action="broadcast", message="hello",
            )
        assert result.connections_affected == 0
        assert result.stale_removed == 0

    def test_broadcast_scan_error(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.scan.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", self._factory(ddb))
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(RuntimeError):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x",
                    action="broadcast", message="hello",
                )

    def test_unsupported_action(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: _mock())
        with patch("aws_util.api_gateway_ops.boto3.client", return_value=_mock()):
            with pytest.raises(ValueError, match="Unsupported action"):
                websocket_session_manager(
                    table_name="t", endpoint_url="https://x",
                    action="invalid_action",
                )


# ==================================================================
# jwt_lambda_authorizer
# ==================================================================


class TestJwtLambdaAuthorizer:
    def _build_clients(
        self,
        cognito: MagicMock | None = None,
        ddb: MagicMock | None = None,
        logs: MagicMock | None = None,
    ) -> Any:
        _cognito = cognito or _mock()
        _ddb = ddb or _mock()
        _logs = logs or _mock()
        # Default: ddb cache miss
        if not ddb:
            _ddb.get_item.return_value = {}

        def factory(service, **kw):
            if service == "cognito-idp":
                return _cognito
            if service == "dynamodb":
                return _ddb
            if service == "logs":
                return _logs
            return _mock()
        return factory, _cognito, _ddb, _logs

    def _valid_claims(self, user_pool_id: str = "us-east-1_AbCd", client_id: str = "app-client") -> dict:
        return {
            "sub": "user-123",
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
            "aud": client_id,
            "client_id": client_id,
            "exp": int(time.time()) + 3600,
            "token_use": "access",
        }

    def test_valid_access_token(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(time=time.time, sleep=lambda x: None))
        claims = self._valid_claims()
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        cognito.get_user.return_value = {
            "Username": "user-123",
            "UserAttributes": [{"Name": "email", "Value": "a@b.com"}],
        }
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is True
        assert result.principal_id == "user-123"
        assert "cognito:email" in result.claims

    def test_valid_id_token(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "id"
        claims["cognito:username"] = "jdoe"
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is True
        # For id tokens, principal_id comes from sub or cognito:username
        assert result.principal_id in ("user-123", "jdoe")

    def test_expired_token(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["exp"] = int(time.time()) - 100  # expired
        token = _make_jwt(claims)
        factory, *_ = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_wrong_issuer(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["iss"] = "https://evil.example.com"
        token = _make_jwt(claims)
        factory, *_ = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_wrong_audience(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["aud"] = "wrong-client"
        claims["client_id"] = "wrong-client"
        token = _make_jwt(claims)
        factory, *_ = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_unsupported_token_use(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "refresh"
        token = _make_jwt(claims)
        factory, *_ = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_malformed_token(self, monkeypatch) -> None:
        factory, *_ = self._build_clients()
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token="not.a.valid-b64-jwt",
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_cognito_get_user_failure(self, monkeypatch) -> None:
        claims = self._valid_claims()
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        cognito.get_user.side_effect = _client_error("NotAuthorizedException")
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        # Cognito rejection leads to invalid token
        assert result.is_valid is False

    def test_jwks_cache_hit(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "id"
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        ddb.get_item.return_value = {
            "Item": {
                "cache_key": {"S": "jwks:us-east-1_AbCd"},
                "jwks": {"S": json.dumps({"keys": []})},
            }
        }
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is True
        assert result.cached_jwks is True

    def test_cloudwatch_log_failure(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "id"
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        logs.put_log_events.side_effect = _client_error("ResourceNotFoundException")
        monkeypatch.setattr(mod, "get_client", factory)
        # Should not raise — log failure is swallowed
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is True

    def test_jwks_cache_ddb_get_error(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "id"
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        ddb.get_item.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        # Should still succeed — JWKS cache miss is handled gracefully
        assert result.is_valid is True
        assert result.cached_jwks is False

    def test_jwks_cache_put_error(self, monkeypatch) -> None:
        claims = self._valid_claims()
        claims["token_use"] = "id"
        token = _make_jwt(claims)
        factory, cognito, ddb, logs = self._build_clients()
        ddb.get_item.return_value = {}
        ddb.put_item.side_effect = _client_error("InternalServerError")
        monkeypatch.setattr(mod, "get_client", factory)
        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id="us-east-1_AbCd",
            client_id="app-client",
            table_name="cache-table",
            log_group_name="/auth/logs",
            region_name=REGION,
        )
        assert result.is_valid is True
        assert result.cached_jwks is False


# ==================================================================
# apigw_usage_plan_enforcer
# ==================================================================


class TestApigwUsagePlanEnforcer:
    def _build_clients(
        self,
        apigw: MagicMock | None = None,
        ddb: MagicMock | None = None,
        sns: MagicMock | None = None,
    ) -> Any:
        _apigw = apigw or _mock()
        _ddb = ddb or _mock()
        _sns = sns or _mock()

        def factory(service, **kw):
            if service == "apigateway":
                return _apigw
            if service == "dynamodb":
                return _ddb
            if service == "sns":
                return _sns
            return _mock()
        return factory, _apigw, _ddb, _sns

    def test_success_new_plan(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-123"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "secret-key"}
        factory, _, ddb, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        result = apigw_usage_plan_enforcer(
            rest_api_id="api-1",
            stage_name="prod",
            plan_name="gold",
            rate_limit=100.0,
            burst_limit=200,
            quota_limit=10000,
            table_name="meta-table",
            region_name=REGION,
        )
        assert result.plan_id == "plan-123"
        assert result.api_key_id == "key-1"
        assert result.api_key_value == "secret-key"
        ddb.put_item.assert_called_once()

    def test_plan_already_exists(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.side_effect = _client_error("ConflictException")
        apigw.get_usage_plans.return_value = {
            "items": [{"name": "gold", "id": "existing-plan"}]
        }
        apigw.create_api_key.return_value = {"id": "key-2", "value": "val-2"}
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        result = apigw_usage_plan_enforcer(
            rest_api_id="api-1",
            stage_name="prod",
            plan_name="gold",
            rate_limit=100.0,
            burst_limit=200,
            quota_limit=10000,
            region_name=REGION,
        )
        assert result.plan_id == "existing-plan"

    def test_conflict_but_plan_not_found(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.side_effect = _client_error("ConflictException")
        apigw.get_usage_plans.return_value = {"items": [{"name": "other", "id": "x"}]}
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                region_name=REGION,
            )

    def test_conflict_get_plans_error(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.side_effect = _client_error("ConflictException")
        apigw.get_usage_plans.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                region_name=REGION,
            )

    def test_create_plan_other_error(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                region_name=REGION,
            )

    def test_create_api_key_error(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.side_effect = _client_error("LimitExceededException")
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                region_name=REGION,
            )

    def test_create_usage_plan_key_error(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "val"}
        apigw.create_usage_plan_key.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                region_name=REGION,
            )

    def test_ddb_persist_error(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "val"}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(apigw=apigw, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            apigw_usage_plan_enforcer(
                rest_api_id="api-1", stage_name="prod", plan_name="gold",
                rate_limit=100.0, burst_limit=200, quota_limit=10000,
                table_name="meta-table",
                region_name=REGION,
            )

    def test_skip_ddb_when_table_name_empty(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "val"}
        factory, _, ddb, _ = self._build_clients(apigw=apigw)
        monkeypatch.setattr(mod, "get_client", factory)

        result = apigw_usage_plan_enforcer(
            rest_api_id="api-1", stage_name="prod", plan_name="gold",
            rate_limit=100.0, burst_limit=200, quota_limit=10000,
            table_name="",
            region_name=REGION,
        )
        assert result.plan_id == "plan-1"
        ddb.put_item.assert_not_called()

    def test_sns_notification(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "val"}
        sns = _mock()
        factory, _, _, _ = self._build_clients(apigw=apigw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        result = apigw_usage_plan_enforcer(
            rest_api_id="api-1", stage_name="prod", plan_name="gold",
            rate_limit=100.0, burst_limit=200, quota_limit=10000,
            sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
            region_name=REGION,
        )
        assert result.plan_id == "plan-1"
        sns.publish.assert_called_once()

    def test_sns_publish_error_swallowed(self, monkeypatch) -> None:
        apigw = _mock()
        apigw.create_usage_plan.return_value = {"id": "plan-1"}
        apigw.create_api_key.return_value = {"id": "key-1", "value": "val"}
        sns = _mock()
        sns.publish.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(apigw=apigw, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)

        # SNS error should NOT propagate
        result = apigw_usage_plan_enforcer(
            rest_api_id="api-1", stage_name="prod", plan_name="gold",
            rate_limit=100.0, burst_limit=200, quota_limit=10000,
            sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
            region_name=REGION,
        )
        assert result.plan_id == "plan-1"


# ==================================================================
# rate_limiter
# ==================================================================


class TestRateLimiter:
    def _build_clients(
        self, ddb: MagicMock | None = None, cw: MagicMock | None = None
    ) -> Any:
        _ddb = ddb or _mock()
        _cw = cw or _mock()

        def factory(service, **kw):
            if service == "dynamodb":
                return _ddb
            if service == "cloudwatch":
                return _cw
            return _mock()
        return factory, _ddb, _cw

    def test_allowed(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.return_value = {
            "Attributes": {"count": {"N": "5"}}
        }
        factory, _, _ = self._build_clients(ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = rate_limiter(
            table_name="rate-table",
            key="user-1",
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        assert result.allowed is True
        assert result.current_count == 5
        assert result.remaining == 95
        assert result.retry_after_seconds == 0

    def test_denied(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.return_value = {
            "Attributes": {"count": {"N": "101"}}
        }
        factory, _, _ = self._build_clients(ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = rate_limiter(
            table_name="rate-table",
            key="user-1",
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        assert result.allowed is False
        assert result.current_count == 101
        assert result.remaining == 0
        assert result.retry_after_seconds >= 0

    def test_ddb_error(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            rate_limiter(
                table_name="rate-table", key="user-1",
                max_requests=100, window_seconds=60,
                region_name=REGION,
            )

    def test_cloudwatch_metric_emission(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.return_value = {
            "Attributes": {"count": {"N": "10"}}
        }
        cw = _mock()
        factory, _, _ = self._build_clients(ddb=ddb, cw=cw)
        monkeypatch.setattr(mod, "get_client", factory)

        result = rate_limiter(
            table_name="rate-table",
            key="user-1",
            max_requests=100,
            window_seconds=60,
            metric_namespace="MyApp/RateLimit",
            region_name=REGION,
        )
        assert result.allowed is True
        cw.put_metric_data.assert_called_once()

    def test_cloudwatch_metric_error_swallowed(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.return_value = {
            "Attributes": {"count": {"N": "10"}}
        }
        cw = _mock()
        cw.put_metric_data.side_effect = _client_error("InternalError")
        factory, _, _ = self._build_clients(ddb=ddb, cw=cw)
        monkeypatch.setattr(mod, "get_client", factory)

        # Should NOT raise
        result = rate_limiter(
            table_name="rate-table",
            key="user-1",
            max_requests=100,
            window_seconds=60,
            metric_namespace="MyApp/RateLimit",
            region_name=REGION,
        )
        assert result.allowed is True

    def test_no_metric_namespace(self, monkeypatch) -> None:
        ddb = _mock()
        ddb.update_item.return_value = {
            "Attributes": {"count": {"N": "1"}}
        }
        cw = _mock()
        factory, _, _ = self._build_clients(ddb=ddb, cw=cw)
        monkeypatch.setattr(mod, "get_client", factory)

        result = rate_limiter(
            table_name="rate-table",
            key="user-1",
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        assert result.allowed is True
        cw.put_metric_data.assert_not_called()


# ==================================================================
# api_gateway_domain_migrator
# ==================================================================


class TestApiGatewayDomainMigrator:
    def _build_clients(
        self,
        apigwv2: MagicMock | None = None,
        route53: MagicMock | None = None,
    ) -> Any:
        _apigwv2 = apigwv2 or _mock()
        _route53 = route53 or _mock()

        def factory(service, **kw):
            if service == "apigatewayv2":
                return _apigwv2
            if service == "route53":
                return _route53
            return _mock()
        return factory, _apigwv2, _route53

    def test_success_new_domain(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.return_value = {
            "DomainNameConfigurations": [
                {
                    "ApiGatewayDomainName": "d-abc.execute-api.us-east-1.amazonaws.com",
                    "HostedZoneId": "Z123APIGW",
                }
            ]
        }
        route53 = _mock()
        route53.change_resource_record_sets.return_value = {
            "ChangeInfo": {"Id": "/change/C123"}
        }
        factory, _, _ = self._build_clients(apigwv2=apigwv2, route53=route53)
        monkeypatch.setattr(mod, "get_client", factory)

        result = api_gateway_domain_migrator(
            domain_name="api.example.com",
            certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
            hosted_zone_id="Z1HOSTED",
            rest_api_id="api-1",
            stage_name="prod",
            region_name=REGION,
        )
        assert result.domain_name == "api.example.com"
        assert result.regional_domain_name == "d-abc.execute-api.us-east-1.amazonaws.com"
        assert result.hosted_zone_id == "Z123APIGW"
        assert result.route53_change_id == "/change/C123"

    def test_domain_already_exists(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.side_effect = _client_error("ConflictException")
        apigwv2.get_domain_name.return_value = {
            "DomainNameConfigurations": [
                {
                    "ApiGatewayDomainName": "d-existing.execute-api.us-east-1.amazonaws.com",
                    "HostedZoneId": "Z999",
                }
            ]
        }
        route53 = _mock()
        route53.change_resource_record_sets.return_value = {
            "ChangeInfo": {"Id": "/change/C456"}
        }
        factory, _, _ = self._build_clients(apigwv2=apigwv2, route53=route53)
        monkeypatch.setattr(mod, "get_client", factory)

        result = api_gateway_domain_migrator(
            domain_name="api.example.com",
            certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
            hosted_zone_id="Z1HOSTED",
            rest_api_id="api-1",
            stage_name="prod",
            region_name=REGION,
        )
        assert result.regional_domain_name == "d-existing.execute-api.us-east-1.amazonaws.com"

    def test_domain_conflict_get_fails(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.side_effect = _client_error("ConflictException")
        apigwv2.get_domain_name.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(apigwv2=apigwv2)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            api_gateway_domain_migrator(
                domain_name="api.example.com",
                certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
                hosted_zone_id="Z1", rest_api_id="api-1", stage_name="prod",
                region_name=REGION,
            )

    def test_create_domain_other_error(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(apigwv2=apigwv2)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            api_gateway_domain_migrator(
                domain_name="api.example.com",
                certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
                hosted_zone_id="Z1", rest_api_id="api-1", stage_name="prod",
                region_name=REGION,
            )

    def test_api_mapping_conflict(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.return_value = {
            "DomainNameConfigurations": [
                {"ApiGatewayDomainName": "d-abc.execute-api.us-east-1.amazonaws.com", "HostedZoneId": "Z1"}
            ]
        }
        apigwv2.create_api_mapping.side_effect = _client_error("ConflictException")
        route53 = _mock()
        route53.change_resource_record_sets.return_value = {"ChangeInfo": {"Id": "/change/C1"}}
        factory, _, _ = self._build_clients(apigwv2=apigwv2, route53=route53)
        monkeypatch.setattr(mod, "get_client", factory)

        # Conflict on mapping is handled gracefully
        result = api_gateway_domain_migrator(
            domain_name="api.example.com",
            certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
            hosted_zone_id="Z1HOSTED", rest_api_id="api-1", stage_name="prod",
            region_name=REGION,
        )
        assert result.domain_name == "api.example.com"

    def test_api_mapping_other_error(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.return_value = {
            "DomainNameConfigurations": [
                {"ApiGatewayDomainName": "d-abc.execute-api.us-east-1.amazonaws.com", "HostedZoneId": "Z1"}
            ]
        }
        apigwv2.create_api_mapping.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(apigwv2=apigwv2)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            api_gateway_domain_migrator(
                domain_name="api.example.com",
                certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
                hosted_zone_id="Z1", rest_api_id="api-1", stage_name="prod",
                region_name=REGION,
            )

    def test_route53_error(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.return_value = {
            "DomainNameConfigurations": [
                {"ApiGatewayDomainName": "d-abc.execute-api.us-east-1.amazonaws.com", "HostedZoneId": "Z1"}
            ]
        }
        route53 = _mock()
        route53.change_resource_record_sets.side_effect = _client_error("NoSuchHostedZone")
        factory, _, _ = self._build_clients(apigwv2=apigwv2, route53=route53)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            api_gateway_domain_migrator(
                domain_name="api.example.com",
                certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
                hosted_zone_id="Z1", rest_api_id="api-1", stage_name="prod",
                region_name=REGION,
            )

    def test_empty_domain_configs(self, monkeypatch) -> None:
        apigwv2 = _mock()
        apigwv2.create_domain_name.return_value = {"DomainNameConfigurations": []}
        route53 = _mock()
        route53.change_resource_record_sets.return_value = {"ChangeInfo": {"Id": "/change/C1"}}
        factory, _, _ = self._build_clients(apigwv2=apigwv2, route53=route53)
        monkeypatch.setattr(mod, "get_client", factory)

        result = api_gateway_domain_migrator(
            domain_name="api.example.com",
            certificate_arn="arn:aws:acm:us-east-1:123:cert/abc",
            hosted_zone_id="Z1", rest_api_id="api-1", stage_name="prod",
            region_name=REGION,
        )
        assert result.regional_domain_name == ""
