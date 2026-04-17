"""Integration tests for aws_util.api_gateway_ops against LocalStack."""
from __future__ import annotations

import base64
import json
import time

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _create_ddb_table(name: str, pk_name: str = "pk", pk_type: str = "S") -> str:
    """Create a DynamoDB table with a single partition key and return its name."""
    client = ls_client("dynamodb")
    try:
        client.create_table(
            TableName=name,
            KeySchema=[{"AttributeName": pk_name, "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": pk_name, "AttributeType": pk_type}],
            BillingMode="PAY_PER_REQUEST",
        )
        client.get_waiter("table_exists").wait(TableName=name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceInUseException":
            raise
    return name


def _build_jwt(claims: dict, secret: str = "test-secret") -> str:
    """Build a fake unsigned JWT with the given claims payload."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "none", "typ": "JWT"}).encode()).rstrip(b"=")
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=")
    sig = base64.urlsafe_b64encode(b"fakesig").rstrip(b"=")
    return f"{header.decode()}.{payload.decode()}.{sig.decode()}"


# ---------------------------------------------------------------------------
# 1. websocket_session_manager
# ---------------------------------------------------------------------------


class TestWebsocketSessionManager:
    """Test connect, disconnect, and broadcast actions.

    The function requires an ``apigatewaymanagementapi`` endpoint which only
    exists when a WebSocket API stage is deployed.  For connect/disconnect we
    can test the DynamoDB side; broadcast will fail on the APIGW post because
    there is no real WebSocket API deployed, but the DynamoDB scan still works.
    """

    @pytest.fixture()
    def ws_table(self):
        """Table with partition key ``connection_id``."""
        name = f"ws-sessions-{int(time.time())}"
        client = ls_client("dynamodb")
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "connection_id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "connection_id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            client.get_waiter("table_exists").wait(TableName=name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                raise
        yield name
        try:
            client.delete_table(TableName=name)
        except Exception:
            pass

    def test_connect_stores_connection_id(self, ws_table):
        from aws_util.api_gateway_ops import websocket_session_manager

        # We pass a dummy endpoint URL; the connect action only touches DynamoDB
        # so the management API client is constructed but never called.
        result = websocket_session_manager(
            table_name=ws_table,
            endpoint_url="http://localhost:4566",
            action="connect",
            connection_id="conn-001",
            region_name=REGION,
        )
        assert result.action == "connect"
        assert result.connections_affected == 1

        # Verify item exists in DynamoDB
        ddb = ls_client("dynamodb")
        resp = ddb.get_item(
            TableName=ws_table,
            Key={"connection_id": {"S": "conn-001"}},
        )
        assert "Item" in resp
        assert resp["Item"]["connection_id"]["S"] == "conn-001"

    def test_disconnect_removes_connection_id(self, ws_table):
        from aws_util.api_gateway_ops import websocket_session_manager

        # Pre-populate a connection
        ddb = ls_client("dynamodb")
        ddb.put_item(
            TableName=ws_table,
            Item={
                "connection_id": {"S": "conn-002"},
                "connected_at": {"N": str(int(time.time()))},
                "ttl": {"N": str(int(time.time()) + 86400)},
            },
        )

        result = websocket_session_manager(
            table_name=ws_table,
            endpoint_url="http://localhost:4566",
            action="disconnect",
            connection_id="conn-002",
            region_name=REGION,
        )
        assert result.action == "disconnect"
        assert result.connections_affected == 1

        # Verify item was deleted
        resp = ddb.get_item(
            TableName=ws_table,
            Key={"connection_id": {"S": "conn-002"}},
        )
        assert "Item" not in resp

    def test_connect_raises_without_connection_id(self, ws_table):
        from aws_util.api_gateway_ops import websocket_session_manager

        with pytest.raises(ValueError, match="connection_id is required"):
            websocket_session_manager(
                table_name=ws_table,
                endpoint_url="http://localhost:4566",
                action="connect",
                connection_id=None,
                region_name=REGION,
            )

    def test_broadcast_raises_without_message(self, ws_table):
        from aws_util.api_gateway_ops import websocket_session_manager

        with pytest.raises(ValueError, match="message is required"):
            websocket_session_manager(
                table_name=ws_table,
                endpoint_url="http://localhost:4566",
                action="broadcast",
                message=None,
                region_name=REGION,
            )

    def test_invalid_action_raises(self, ws_table):
        from aws_util.api_gateway_ops import websocket_session_manager

        with pytest.raises(ValueError, match="Unsupported action"):
            websocket_session_manager(
                table_name=ws_table,
                endpoint_url="http://localhost:4566",
                action="invalid",
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# 2. jwt_lambda_authorizer
# ---------------------------------------------------------------------------


class TestJwtLambdaAuthorizer:
    """Test JWT validation, JWKS caching in DynamoDB, and CloudWatch logging.

    Cognito ``GetUser`` is available in LocalStack but will reject our
    synthetic tokens.  We test that the claim validation logic fires correctly
    and that DynamoDB caching + CloudWatch logging work.
    """

    @pytest.fixture()
    def cache_table(self):
        """Table with partition key ``cache_key``."""
        name = f"jwks-cache-{int(time.time())}"
        client = ls_client("dynamodb")
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "cache_key", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "cache_key", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            client.get_waiter("table_exists").wait(TableName=name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                raise
        yield name
        try:
            client.delete_table(TableName=name)
        except Exception:
            pass

    def test_invalid_jwt_expired(self, cache_table, logs_group):
        from aws_util.api_gateway_ops import jwt_lambda_authorizer

        user_pool_id = "us-east-1_TestPool"
        client_id = "test-client-id"

        # Build a JWT with expired exp
        claims = {
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
            "aud": client_id,
            "exp": int(time.time()) - 3600,  # expired
            "token_use": "id",
            "sub": "user-expired",
        }
        token = _build_jwt(claims)

        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id=user_pool_id,
            client_id=client_id,
            table_name=cache_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert result.is_valid is False
        assert result.principal_id == "user-expired"

    def test_invalid_jwt_wrong_issuer(self, cache_table, logs_group):
        from aws_util.api_gateway_ops import jwt_lambda_authorizer

        user_pool_id = "us-east-1_TestPool"
        client_id = "test-client-id"

        claims = {
            "iss": "https://evil.example.com",
            "aud": client_id,
            "exp": int(time.time()) + 3600,
            "token_use": "id",
            "sub": "user-wrong-iss",
        }
        token = _build_jwt(claims)

        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id=user_pool_id,
            client_id=client_id,
            table_name=cache_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert result.is_valid is False

    def test_valid_id_token_populates_cache(self, cache_table, logs_group):
        """An ``id`` token with correct iss/aud/exp skips Cognito GetUser and returns valid.

        The JWKS cache should be populated in DynamoDB after this call.
        """
        from aws_util.api_gateway_ops import jwt_lambda_authorizer

        user_pool_id = "us-east-1_TestPool"
        client_id = "test-client-id"

        claims = {
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
            "aud": client_id,
            "exp": int(time.time()) + 3600,
            "token_use": "id",
            "sub": "user-valid-id",
            "cognito:username": "validuser",
        }
        token = _build_jwt(claims)

        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id=user_pool_id,
            client_id=client_id,
            table_name=cache_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert result.is_valid is True
        assert result.principal_id in ("user-valid-id", "validuser")

        # Verify JWKS was written to cache
        ddb = ls_client("dynamodb")
        resp = ddb.get_item(
            TableName=cache_table,
            Key={"cache_key": {"S": f"jwks:{user_pool_id}"}},
        )
        assert "Item" in resp

    def test_access_token_cognito_rejected(self, cache_table, logs_group):
        """An ``access`` token will try Cognito GetUser which rejects our fake token."""
        from aws_util.api_gateway_ops import jwt_lambda_authorizer

        user_pool_id = "us-east-1_TestPool"
        client_id = "test-client-id"

        claims = {
            "iss": f"https://cognito-idp.us-east-1.amazonaws.com/{user_pool_id}",
            "client_id": client_id,
            "exp": int(time.time()) + 3600,
            "token_use": "access",
            "sub": "user-access",
        }
        token = _build_jwt(claims)

        result = jwt_lambda_authorizer(
            token=token,
            user_pool_id=user_pool_id,
            client_id=client_id,
            table_name=cache_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        # Cognito will reject the token, so is_valid should be False
        assert result.is_valid is False

    def test_malformed_jwt(self, cache_table, logs_group):
        from aws_util.api_gateway_ops import jwt_lambda_authorizer

        result = jwt_lambda_authorizer(
            token="not.a.valid.jwt.token",
            user_pool_id="us-east-1_TestPool",
            client_id="test-client-id",
            table_name=cache_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert result.is_valid is False


# ---------------------------------------------------------------------------
# 3. apigw_usage_plan_enforcer
# ---------------------------------------------------------------------------


class TestApigwUsagePlanEnforcer:
    """Test usage plan and API key provisioning.

    API Gateway is available in LocalStack community, so these are real tests.
    """

    @pytest.fixture()
    def rest_api(self):
        """Create a REST API and stage in LocalStack."""
        apigw = ls_client("apigateway")
        api = apigw.create_rest_api(name=f"test-api-{int(time.time())}", description="test")
        api_id = api["id"]

        # Get root resource
        resources = apigw.get_resources(restApiId=api_id)
        root_id = resources["items"][0]["id"]

        # Create a GET method on root
        apigw.put_method(
            restApiId=api_id,
            resourceId=root_id,
            httpMethod="GET",
            authorizationType="NONE",
        )
        apigw.put_method_response(
            restApiId=api_id,
            resourceId=root_id,
            httpMethod="GET",
            statusCode="200",
        )
        apigw.put_integration(
            restApiId=api_id,
            resourceId=root_id,
            httpMethod="GET",
            type="MOCK",
            requestTemplates={"application/json": '{"statusCode": 200}'},
        )
        apigw.put_integration_response(
            restApiId=api_id,
            resourceId=root_id,
            httpMethod="GET",
            statusCode="200",
            responseTemplates={"application/json": "{}"},
        )

        # Deploy to a stage
        apigw.create_deployment(restApiId=api_id, stageName="test")

        yield api_id

        try:
            apigw.delete_rest_api(restApiId=api_id)
        except Exception:
            pass

    @pytest.fixture()
    def plan_table(self):
        """Table with partition key ``plan_name``."""
        name = f"usage-plans-{int(time.time())}"
        client = ls_client("dynamodb")
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "plan_name", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "plan_name", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            client.get_waiter("table_exists").wait(TableName=name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                raise
        yield name
        try:
            client.delete_table(TableName=name)
        except Exception:
            pass

    def test_provisions_usage_plan_and_key(self, rest_api, plan_table, sns_topic):
        from aws_util.api_gateway_ops import apigw_usage_plan_enforcer

        plan_name = f"test-plan-{int(time.time())}"
        result = apigw_usage_plan_enforcer(
            rest_api_id=rest_api,
            stage_name="test",
            plan_name=plan_name,
            rate_limit=10.0,
            burst_limit=5,
            quota_limit=1000,
            quota_period="MONTH",
            table_name=plan_table,
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.plan_id, str)
        assert len(result.plan_id) > 0
        assert isinstance(result.api_key_id, str)
        assert len(result.api_key_id) > 0
        assert isinstance(result.api_key_value, str)

        # Verify DynamoDB metadata
        ddb = ls_client("dynamodb")
        resp = ddb.get_item(
            TableName=plan_table,
            Key={"plan_name": {"S": plan_name}},
        )
        assert "Item" in resp
        assert resp["Item"]["plan_id"]["S"] == result.plan_id

    def test_provisions_without_dynamodb(self, rest_api):
        from aws_util.api_gateway_ops import apigw_usage_plan_enforcer

        plan_name = f"test-plan-nodb-{int(time.time())}"
        result = apigw_usage_plan_enforcer(
            rest_api_id=rest_api,
            stage_name="test",
            plan_name=plan_name,
            rate_limit=5.0,
            burst_limit=2,
            quota_limit=500,
            quota_period="DAY",
            table_name="",
            sns_topic_arn=None,
            region_name=REGION,
        )
        assert isinstance(result.plan_id, str)
        assert isinstance(result.api_key_id, str)


# ---------------------------------------------------------------------------
# 4. rate_limiter
# ---------------------------------------------------------------------------


class TestRateLimiter:
    """Test sliding-window rate limiter using DynamoDB atomic counters.

    DynamoDB is available in LocalStack community, so these are real tests.
    """

    @pytest.fixture()
    def rate_table(self):
        """Table with partition key ``rate_key``."""
        name = f"rate-limits-{int(time.time())}"
        client = ls_client("dynamodb")
        try:
            client.create_table(
                TableName=name,
                KeySchema=[{"AttributeName": "rate_key", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "rate_key", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )
            client.get_waiter("table_exists").wait(TableName=name)
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                raise
        yield name
        try:
            client.delete_table(TableName=name)
        except Exception:
            pass

    def test_allows_under_limit(self, rate_table):
        from aws_util.api_gateway_ops import rate_limiter

        result = rate_limiter(
            table_name=rate_table,
            key="user-001",
            max_requests=10,
            window_seconds=60,
            metric_namespace=None,
            region_name=REGION,
        )
        assert result.allowed is True
        assert result.current_count == 1
        assert result.remaining == 9
        assert result.retry_after_seconds == 0

    def test_denies_over_limit(self, rate_table):
        from aws_util.api_gateway_ops import rate_limiter

        key = f"user-over-{int(time.time())}"

        # Fire max_requests + 1 calls
        max_req = 3
        for _ in range(max_req):
            rate_limiter(
                table_name=rate_table,
                key=key,
                max_requests=max_req,
                window_seconds=60,
                region_name=REGION,
            )

        # The next call should be denied
        result = rate_limiter(
            table_name=rate_table,
            key=key,
            max_requests=max_req,
            window_seconds=60,
            region_name=REGION,
        )
        assert result.allowed is False
        assert result.current_count > max_req
        assert result.remaining == 0
        assert result.retry_after_seconds > 0

    def test_increments_counter(self, rate_table):
        from aws_util.api_gateway_ops import rate_limiter

        key = f"user-inc-{int(time.time())}"

        r1 = rate_limiter(
            table_name=rate_table,
            key=key,
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        r2 = rate_limiter(
            table_name=rate_table,
            key=key,
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        assert r2.current_count == r1.current_count + 1

    def test_different_keys_isolated(self, rate_table):
        from aws_util.api_gateway_ops import rate_limiter

        ts = int(time.time())
        r1 = rate_limiter(
            table_name=rate_table,
            key=f"key-a-{ts}",
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        r2 = rate_limiter(
            table_name=rate_table,
            key=f"key-b-{ts}",
            max_requests=100,
            window_seconds=60,
            region_name=REGION,
        )
        assert r1.current_count == 1
        assert r2.current_count == 1


# ---------------------------------------------------------------------------
# 5. api_gateway_domain_migrator
# ---------------------------------------------------------------------------


class TestApiGatewayDomainMigrator:
    """Test custom domain creation with ACM + Route53."""

    @pytest.fixture()
    def acm_certificate(self):
        """Request an ACM certificate in LocalStack and return its ARN."""
        acm = ls_client("acm")
        resp = acm.request_certificate(
            DomainName="api.example.com",
            ValidationMethod="DNS",
        )
        cert_arn = resp["CertificateArn"]
        yield cert_arn

    @pytest.fixture()
    def hosted_zone(self):
        """Create a Route53 hosted zone and return its ID."""
        r53 = ls_client("route53")
        resp = r53.create_hosted_zone(
            Name="example.com",
            CallerReference=f"test-{int(time.time())}",
        )
        zone_id = resp["HostedZone"]["Id"].split("/")[-1]
        yield zone_id
        try:
            r53.delete_hosted_zone(Id=zone_id)
        except Exception:
            pass

    @pytest.fixture()
    def http_api(self):
        """Create an HTTP API (apigatewayv2) in LocalStack."""
        apigwv2 = ls_client("apigatewayv2")
        resp = apigwv2.create_api(
            Name=f"test-http-api-{int(time.time())}",
            ProtocolType="HTTP",
        )
        api_id = resp["ApiId"]

        # Create a default stage
        try:
            apigwv2.create_stage(
                ApiId=api_id,
                StageName="prod",
                AutoDeploy=True,
            )
        except ClientError:
            pass

        yield api_id

        try:
            apigwv2.delete_api(ApiId=api_id)
        except Exception:
            pass

    @pytest.mark.skip(reason="apigatewayv2 CreateApi not available in LocalStack 4.4.0 community")
    def test_creates_custom_domain(self, acm_certificate, hosted_zone, http_api):
        from aws_util.api_gateway_ops import api_gateway_domain_migrator

        result = api_gateway_domain_migrator(
            domain_name="api.example.com",
            certificate_arn=acm_certificate,
            hosted_zone_id=hosted_zone,
            rest_api_id=http_api,
            stage_name="prod",
            base_path="/",
            region_name=REGION,
        )
        assert result.domain_name == "api.example.com"
        assert isinstance(result.regional_domain_name, str)
        assert isinstance(result.hosted_zone_id, str)
        assert isinstance(result.route53_change_id, str)

    @pytest.mark.skip(reason="apigatewayv2 CreateApi not available in LocalStack 4.4.0 community")
    def test_idempotent_domain_creation(self, acm_certificate, hosted_zone, http_api):
        from aws_util.api_gateway_ops import api_gateway_domain_migrator

        # First call creates the domain
        result1 = api_gateway_domain_migrator(
            domain_name="api2.example.com",
            certificate_arn=acm_certificate,
            hosted_zone_id=hosted_zone,
            rest_api_id=http_api,
            stage_name="prod",
            base_path="/",
            region_name=REGION,
        )
        assert result1.domain_name == "api2.example.com"

        # Second call should handle ConflictException gracefully
        result2 = api_gateway_domain_migrator(
            domain_name="api2.example.com",
            certificate_arn=acm_certificate,
            hosted_zone_id=hosted_zone,
            rest_api_id=http_api,
            stage_name="prod",
            base_path="/",
            region_name=REGION,
        )
        assert result2.domain_name == "api2.example.com"
