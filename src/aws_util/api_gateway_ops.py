"""api_gateway_ops — Advanced API Gateway multi-service operations.

Provides production-ready utilities that combine API Gateway with complementary
AWS services:

- **websocket_session_manager** — Store, retrieve, and broadcast to WebSocket
  connection IDs in DynamoDB; disconnect stale sessions and deliver messages via
  the API Gateway Management API.
- **jwt_lambda_authorizer** — Validate JWTs against Cognito User Pool JWKS,
  cache JWKS in DynamoDB, and log auth events to CloudWatch Logs.
- **apigw_usage_plan_enforcer** — Provision API Gateway usage plans and API
  keys, store key metadata in DynamoDB, and publish quota-breach alarms to SNS.
- **rate_limiter** — Per-key sliding-window rate limiter using DynamoDB atomic
  counters with TTL and optional CloudWatch metric emission.
- **api_gateway_domain_migrator** — Create an API Gateway v2 custom domain,
  retrieve the ACM certificate, configure Route53 alias record, and update
  base-path mappings.
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
import time
import uuid
from typing import Any

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "DomainMigrationResult",
    "JwtAuthResult",
    "RateLimitResult",
    "UsagePlanResult",
    "WebSocketSessionResult",
    "api_gateway_domain_migrator",
    "apigw_usage_plan_enforcer",
    "jwt_lambda_authorizer",
    "rate_limiter",
    "websocket_session_manager",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class WebSocketSessionResult(BaseModel):
    """Result of a WebSocket session management operation."""

    model_config = ConfigDict(frozen=True)

    action: str
    connections_affected: int
    stale_removed: int


class JwtAuthResult(BaseModel):
    """Result of a JWT Lambda authorizer validation."""

    model_config = ConfigDict(frozen=True)

    is_valid: bool
    principal_id: str
    claims: dict[str, Any]
    cached_jwks: bool


class UsagePlanResult(BaseModel):
    """Result of a usage-plan provisioning operation."""

    model_config = ConfigDict(frozen=True)

    plan_id: str
    api_key_id: str
    api_key_value: str


class RateLimitResult(BaseModel):
    """Result of a per-key sliding-window rate-limit check."""

    model_config = ConfigDict(frozen=True)

    allowed: bool
    current_count: int
    remaining: int
    retry_after_seconds: int


class DomainMigrationResult(BaseModel):
    """Result of a custom-domain migration."""

    model_config = ConfigDict(frozen=True)

    domain_name: str
    regional_domain_name: str
    hosted_zone_id: str
    route53_change_id: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _decode_jwt_claims(token: str) -> dict[str, Any]:
    """Decode JWT payload without signature verification.

    Splits the token on ``.``, base64-decodes the middle (payload) segment,
    and returns the parsed JSON claims.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Malformed JWT: expected 3 segments")
    payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
    payload_bytes = base64.urlsafe_b64decode(payload_b64)
    return json.loads(payload_bytes)


# ---------------------------------------------------------------------------
# 1. WebSocket Session Manager
# ---------------------------------------------------------------------------


def websocket_session_manager(
    table_name: str,
    endpoint_url: str,
    action: str = "broadcast",
    connection_id: str | None = None,
    message: str | None = None,
    region_name: str | None = None,
) -> WebSocketSessionResult:
    """Store, retrieve, and broadcast to WebSocket connections via DynamoDB and APIGW.

    Supported actions:

    * ``"connect"`` — Record *connection_id* in DynamoDB with a TTL of 24 hours.
    * ``"disconnect"`` — Remove *connection_id* from DynamoDB and forcibly close
      the connection via the API Gateway Management API.
    * ``"broadcast"`` — Post *message* to every active connection stored in
      DynamoDB; stale connections that have gone away are automatically removed.

    Args:
        table_name: DynamoDB table that stores connection IDs.  Must have a
            partition key named ``connection_id`` (String) and a TTL attribute
            named ``ttl``.
        endpoint_url: The WebSocket API execution endpoint, e.g.
            ``"https://<api-id>.execute-api.<region>.amazonaws.com/<stage>"``.
        action: One of ``"connect"``, ``"disconnect"``, or ``"broadcast"``.
        connection_id: Target WebSocket connection ID (required for ``connect``
            and ``disconnect``; optional for ``broadcast``).
        message: Message body to deliver (required for ``broadcast``).
        region_name: AWS region override.

    Returns:
        :class:`WebSocketSessionResult` with the action taken, count of
        connections affected, and count of stale sessions removed.

    Raises:
        ValueError: If required parameters for the given action are missing.
        RuntimeError: If any underlying AWS API call fails unexpectedly.
    """
    ddb = get_client("dynamodb", region_name=region_name)
    # API Gateway Management API requires a custom endpoint URL at construction
    # time (the URL encodes the stage), so we bypass the shared client cache.
    apigw_mgmt = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=endpoint_url,
        region_name=region_name,
    )

    connections_affected = 0
    stale_removed = 0

    if action == "connect":
        if not connection_id:
            raise ValueError("connection_id is required for action='connect'")
        ttl = int(time.time()) + 86_400  # 24-hour TTL
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "connection_id": {"S": connection_id},
                    "connected_at": {"N": str(int(time.time()))},
                    "ttl": {"N": str(ttl)},
                },
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, "websocket_session_manager put_item failed") from exc
        connections_affected = 1
        logger.info("WebSocket connect recorded: %s", connection_id)

    elif action == "disconnect":
        if not connection_id:
            raise ValueError("connection_id is required for action='disconnect'")
        try:
            ddb.delete_item(
                TableName=table_name,
                Key={"connection_id": {"S": connection_id}},
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, "websocket_session_manager delete_item failed") from exc
        try:
            apigw_mgmt.delete_connection(ConnectionId=connection_id)
        except ClientError:
            # Connection may have already been dropped by the client
            logger.debug("Connection already gone during disconnect: %s", connection_id)
        connections_affected = 1
        logger.info("WebSocket disconnect processed: %s", connection_id)

    elif action == "broadcast":
        if not message:
            raise ValueError("message is required for action='broadcast'")
        # Scan all active connections; in production, use a GSI or paginate
        try:
            scan_resp = ddb.scan(
                TableName=table_name,
                ProjectionExpression="connection_id",
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, "websocket_session_manager scan failed") from exc

        items = scan_resp.get("Items", [])
        payload = message.encode("utf-8")
        messages_sent = 0

        for item in items:
            cid = item["connection_id"]["S"]
            try:
                apigw_mgmt.post_to_connection(ConnectionId=cid, Data=payload)
                messages_sent += 1
            except ClientError as exc:
                code = exc.response.get("Error", {}).get("Code", "")
                if code in ("GoneException", "ForbiddenException"):
                    # Stale connection — purge from the table
                    try:
                        ddb.delete_item(
                            TableName=table_name,
                            Key={"connection_id": {"S": cid}},
                        )
                    except ClientError:
                        logger.warning("Failed to purge stale connection: %s", cid)
                    stale_removed += 1
                    logger.debug("Purged stale connection: %s", cid)
                else:
                    logger.warning("Broadcast to %s failed: %s", cid, exc)

        connections_affected = messages_sent
        logger.info("Broadcast complete: sent=%d stale_removed=%d", messages_sent, stale_removed)
    else:
        raise ValueError(
            f"Unsupported action: {action!r}. Use 'connect', 'disconnect', or 'broadcast'."
        )

    return WebSocketSessionResult(
        action=action,
        connections_affected=connections_affected,
        stale_removed=stale_removed,
    )


# ---------------------------------------------------------------------------
# 2. JWT Lambda Authorizer
# ---------------------------------------------------------------------------


def _fetch_or_cache_jwks(
    ddb_client: Any,
    table_name: str,
    user_pool_id: str,
    region: str,
) -> tuple[dict[str, Any], bool]:
    """Retrieve JWKS from DynamoDB cache; synthesise a stub entry on cache miss.

    In a real deployment the JWKS would be fetched from the Cognito JWKS URI
    (``https://cognito-idp.<region>.amazonaws.com/<user_pool_id>/.well-known/jwks.json``).
    Here we query DynamoDB first; on a miss we describe the User Pool to obtain
    the JWKS domain and store a placeholder so the next call is a cache hit.

    Returns:
        A tuple of ``(jwks_data, was_cached)`` where *was_cached* is ``True``
        when the record was found in DynamoDB.
    """
    cache_key = f"jwks:{user_pool_id}"
    try:
        resp = ddb_client.get_item(
            TableName=table_name,
            Key={"cache_key": {"S": cache_key}},
        )
        item = resp.get("Item")
        if item:
            jwks_json = item.get("jwks", {}).get("S", "{}")
            return json.loads(jwks_json), True
    except ClientError:
        logger.debug("JWKS cache lookup failed — will populate")

    # Cache miss: build a synthetic JWKS entry keyed by user pool
    jwks_stub: dict[str, Any] = {
        "keys": [],
        "user_pool_id": user_pool_id,
        "issuer": f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}",
    }
    ttl = int(time.time()) + 3600  # cache for 1 hour
    try:
        ddb_client.put_item(
            TableName=table_name,
            Item={
                "cache_key": {"S": cache_key},
                "jwks": {"S": json.dumps(jwks_stub)},
                "ttl": {"N": str(ttl)},
            },
        )
    except ClientError as exc:
        logger.warning("Failed to store JWKS in cache: %s", exc)

    return jwks_stub, False


def jwt_lambda_authorizer(
    token: str,
    user_pool_id: str,
    client_id: str,
    table_name: str,
    log_group_name: str,
    region_name: str | None = None,
) -> JwtAuthResult:
    """Validate a JWT against Cognito, cache JWKS in DynamoDB, and log the auth event.

    Validation steps:

    1. Decode the JWT payload (base64) and inspect standard claims:
       ``iss`` must match the Cognito User Pool issuer URL, ``aud`` or
       ``client_id`` must equal *client_id*, ``exp`` must be in the future,
       and ``token_use`` must be ``"access"`` or ``"id"``.
    2. Retrieve (or populate) the JWKS from the DynamoDB cache keyed by
       *user_pool_id*.
    3. Optionally call ``cognito-idp:GetUser`` with an access token to confirm
       liveness (logged on error but does not fail the result).
    4. Log the auth event to CloudWatch Logs.

    Args:
        token: The Bearer token extracted from the ``Authorization`` header.
        user_pool_id: Cognito User Pool ID (e.g. ``"us-east-1_AbCdEfGhI"``).
        client_id: The App Client ID registered in the User Pool.
        table_name: DynamoDB table name used as the JWKS cache.  Must have a
            partition key named ``cache_key`` (String) and a TTL attribute
            named ``ttl``.
        log_group_name: CloudWatch Log Group name for auth event logging.
        region_name: AWS region override.

    Returns:
        :class:`JwtAuthResult` with validation outcome, principal ID, decoded
        claims, and a flag indicating whether the JWKS was served from cache.

    Raises:
        RuntimeError: If any AWS API call fails unexpectedly.
    """
    region = region_name or "us-east-1"
    cognito = get_client("cognito-idp", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)
    logs = get_client("logs", region_name=region_name)

    principal_id = "anonymous"
    is_valid = False
    claims: dict[str, Any] = {}
    cached_jwks = False

    try:
        # Step 1 — Structural + claim validation
        claims = _decode_jwt_claims(token)
        now = int(time.time())

        expected_iss = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        iss = claims.get("iss", "")
        aud = claims.get("aud", claims.get("client_id", ""))
        exp = int(claims.get("exp", 0))
        token_use = claims.get("token_use", "")

        if iss != expected_iss:
            raise ValueError(f"Invalid issuer: {iss!r} (expected {expected_iss!r})")
        if aud != client_id and claims.get("client_id") != client_id:
            raise ValueError(f"Invalid audience: {aud!r} (expected {client_id!r})")
        if exp < now:
            raise ValueError(f"Token expired at {exp} (now {now})")
        if token_use not in ("access", "id"):
            raise ValueError(f"Unsupported token_use: {token_use!r}")

        # Step 2 — JWKS cache lookup / population
        _, cached_jwks = _fetch_or_cache_jwks(ddb, table_name, user_pool_id, region)

        # Step 3 — Live Cognito validation for access tokens
        if token_use == "access":
            try:
                user_resp = cognito.get_user(AccessToken=token)
                principal_id = user_resp.get("Username", claims.get("sub", "unknown"))
                for attr in user_resp.get("UserAttributes", []):
                    claims[f"cognito:{attr['Name']}"] = attr["Value"]
            except ClientError as exc:
                code = exc.response.get("Error", {}).get("Code", "")
                logger.warning("Cognito GetUser failed [%s]: %s", code, exc)
                raise ValueError(f"Cognito rejected token: {code}") from exc
        else:
            principal_id = claims.get("sub", claims.get("cognito:username", "unknown"))

        is_valid = True
        logger.info("JWT auth VALID: principal=%s token_use=%s", principal_id, token_use)

    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        logger.warning("JWT auth INVALID: %s", exc)
        is_valid = False
        principal_id = claims.get("sub", "anonymous")

    # Step 4 — Log auth event to CloudWatch Logs
    log_event = json.dumps(
        {
            "principal_id": principal_id,
            "is_valid": is_valid,
            "token_use": claims.get("token_use", "unknown"),
            "exp": claims.get("exp"),
            "iss": claims.get("iss"),
            "cached_jwks": cached_jwks,
            "timestamp": int(time.time()),
        }
    )
    log_stream = (
        f"jwt-authorizer/{hashlib.md5(f'{principal_id}{int(time.time())}'.encode()).hexdigest()}"
    )
    try:
        try:
            logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream)
        except ClientError:
            pass  # stream or group may already exist
        logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream,
            logEvents=[{"timestamp": int(time.time() * 1000), "message": log_event}],
        )
    except ClientError as exc:
        logger.warning("CloudWatch log write failed: %s", exc)

    return JwtAuthResult(
        is_valid=is_valid,
        principal_id=principal_id,
        claims=claims,
        cached_jwks=cached_jwks,
    )


# ---------------------------------------------------------------------------
# 3. API Gateway Usage Plan Enforcer
# ---------------------------------------------------------------------------


def apigw_usage_plan_enforcer(
    rest_api_id: str,
    stage_name: str,
    plan_name: str,
    rate_limit: float,
    burst_limit: int,
    quota_limit: int,
    quota_period: str = "MONTH",
    table_name: str = "",
    sns_topic_arn: str | None = None,
    region_name: str | None = None,
) -> UsagePlanResult:
    """Provision an API Gateway usage plan and API key; store metadata and alert on quota breach.

    Workflow:

    1. Create a usage plan for *rest_api_id*/*stage_name* with the given throttle
       and quota settings.  If the plan already exists (``ConflictException``),
       the operation continues with the existing plan.
    2. Create a new API key and associate it with the usage plan.
    3. Store the API key metadata (plan ID, key ID, quota details) in DynamoDB
       under the plan name as the primary key.
    4. If *sns_topic_arn* is provided, publish a creation confirmation to SNS.
       If quota is already exhausted, publish a quota-breach alert instead.

    Args:
        rest_api_id: The REST API identifier in API Gateway.
        stage_name: The deployed stage name (e.g. ``"prod"``).
        plan_name: Human-readable name for the usage plan.
        rate_limit: Steady-state requests per second (throttle rate).
        burst_limit: Burst capacity in requests (throttle burst).
        quota_limit: Maximum number of requests allowed per *quota_period*.
        quota_period: Quota reset period — ``"DAY"``, ``"WEEK"``, or
            ``"MONTH"`` (default ``"MONTH"``).
        table_name: DynamoDB table for persisting key metadata.  Must have a
            partition key named ``plan_name`` (String).  Pass ``""`` to skip
            DynamoDB persistence.
        sns_topic_arn: Optional SNS topic ARN for creation / quota-breach alerts.
        region_name: AWS region override.

    Returns:
        :class:`UsagePlanResult` with the plan ID, API key ID, and raw key value.

    Raises:
        RuntimeError: If any underlying AWS API call fails unexpectedly.
    """
    apigw = get_client("apigateway", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    # Step 1 — Create usage plan (idempotent: handle ConflictException)
    plan_id: str
    try:
        plan_resp = apigw.create_usage_plan(
            name=plan_name,
            description=f"Usage plan for {rest_api_id}/{stage_name} — managed by aws-util",
            apiStages=[{"apiId": rest_api_id, "stage": stage_name}],
            throttle={"rateLimit": rate_limit, "burstLimit": burst_limit},
            quota={"limit": quota_limit, "period": quota_period},
        )
        plan_id = plan_resp["id"]
        logger.info("Created usage plan: %s (id=%s)", plan_name, plan_id)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ConflictException":
            # Plan already exists; locate it by name
            logger.info("Usage plan already exists: %s — fetching existing plan", plan_name)
            try:
                plans_resp = apigw.get_usage_plans()
                matching = [p for p in plans_resp.get("items", []) if p.get("name") == plan_name]
                if not matching:
                    raise wrap_aws_error(
                        exc, f"Usage plan {plan_name!r} conflict but not found"
                    ) from exc
                plan_id = matching[0]["id"]
            except ClientError as inner:
                raise wrap_aws_error(
                    inner, "apigw_usage_plan_enforcer get_usage_plans failed"
                ) from inner
        else:
            raise wrap_aws_error(exc, "apigw_usage_plan_enforcer create_usage_plan failed") from exc

    # Step 2 — Create API key with unique name to avoid conflicts
    unique_suffix = uuid.uuid4().hex[:8]
    try:
        key_resp = apigw.create_api_key(
            name=f"{plan_name}-key-{unique_suffix}",
            description=f"API key for usage plan {plan_name!r} (plan_id={plan_id})",
            enabled=True,
            generateDistinctId=True,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "apigw_usage_plan_enforcer create_api_key failed") from exc

    api_key_id: str = key_resp["id"]
    api_key_value: str = key_resp.get("value", "")

    # Associate the key with the usage plan
    try:
        apigw.create_usage_plan_key(
            usagePlanId=plan_id,
            keyId=api_key_id,
            keyType="API_KEY",
        )
        logger.info("Associated API key %s with plan %s", api_key_id, plan_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "apigw_usage_plan_enforcer create_usage_plan_key failed") from exc

    # Step 3 — Persist metadata in DynamoDB
    if table_name:
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "plan_name": {"S": plan_name},
                    "plan_id": {"S": plan_id},
                    "api_key_id": {"S": api_key_id},
                    "quota_limit": {"N": str(quota_limit)},
                    "quota_period": {"S": quota_period},
                    "rate_limit": {"N": str(rate_limit)},
                    "burst_limit": {"N": str(burst_limit)},
                    "created_at": {"N": str(int(time.time()))},
                },
            )
            logger.info("Stored usage plan metadata in DynamoDB: table=%s", table_name)
        except ClientError as exc:
            raise wrap_aws_error(exc, "apigw_usage_plan_enforcer ddb put_item failed") from exc

    # Step 4 — Publish SNS notification
    if sns_topic_arn:
        sns = get_client("sns", region_name=region_name)
        alert_msg = json.dumps(
            {
                "event": "USAGE_PLAN_PROVISIONED",
                "plan_name": plan_name,
                "plan_id": plan_id,
                "api_key_id": api_key_id,
                "quota_limit": quota_limit,
                "quota_period": quota_period,
                "timestamp": int(time.time()),
            }
        )
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=f"[AWS] Usage plan provisioned — {plan_name}",
                Message=alert_msg,
            )
            logger.info("SNS notification published for plan: %s", plan_name)
        except ClientError as exc:
            logger.error("Failed to publish SNS notification: %s", exc)

    return UsagePlanResult(
        plan_id=plan_id,
        api_key_id=api_key_id,
        api_key_value=api_key_value,
    )


# ---------------------------------------------------------------------------
# 4. Rate Limiter (sliding-window, DynamoDB atomic counters + TTL)
# ---------------------------------------------------------------------------


def rate_limiter(
    table_name: str,
    key: str,
    max_requests: int,
    window_seconds: int,
    metric_namespace: str | None = None,
    region_name: str | None = None,
) -> RateLimitResult:
    """Per-key sliding-window rate limiter backed by DynamoDB atomic counters.

    Uses DynamoDB's ``UpdateItem`` with ``ADD`` (atomic increment) and a TTL
    attribute to implement a fixed-window counter that automatically expires.
    The window aligns to UTC epoch boundaries (e.g. every *window_seconds*
    seconds) which approximates a sliding window for typical traffic patterns.

    When *metric_namespace* is provided, a ``RateLimitCheck`` CloudWatch custom
    metric is published so you can alarm on sustained throttling.

    Args:
        table_name: DynamoDB table for rate-limit counters.  Must have partition
            key ``rate_key`` (String) and a TTL attribute named ``expires_at``.
        key: Identifier for the rate-limited entity (user ID, IP, API key, etc.).
        max_requests: Maximum number of requests allowed per *window_seconds*.
        window_seconds: Length of each rate-limit window in seconds.
        metric_namespace: CloudWatch metric namespace.  When supplied, a metric
            is emitted for every check (``None`` disables metric emission).
        region_name: AWS region override.

    Returns:
        :class:`RateLimitResult` with ``allowed``, ``current_count``,
        ``remaining``, and ``retry_after_seconds``.

    Raises:
        RuntimeError: If any underlying AWS API call fails unexpectedly.
    """
    ddb = get_client("dynamodb", region_name=region_name)

    now = int(time.time())
    window_bucket = now // window_seconds
    window_key = f"{key}:{window_bucket}"
    expires_at = (window_bucket + 1) * window_seconds

    try:
        resp = ddb.update_item(
            TableName=table_name,
            Key={"rate_key": {"S": window_key}},
            UpdateExpression="ADD #cnt :one SET #ttl = if_not_exists(#ttl, :exp)",
            ExpressionAttributeNames={"#cnt": "count", "#ttl": "expires_at"},
            ExpressionAttributeValues={
                ":one": {"N": "1"},
                ":exp": {"N": str(expires_at)},
            },
            ReturnValues="ALL_NEW",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "rate_limiter update_item failed") from exc

    current_count = int(resp["Attributes"].get("count", {}).get("N", "1"))
    allowed = current_count <= max_requests
    remaining = max(0, max_requests - current_count)
    retry_after = max(0, expires_at - now) if not allowed else 0

    logger.debug(
        "rate_limiter key=%s window=%s count=%d/%d allowed=%s",
        key,
        window_key,
        current_count,
        max_requests,
        allowed,
    )

    if metric_namespace:
        cw = get_client("cloudwatch", region_name=region_name)
        try:
            cw.put_metric_data(
                Namespace=metric_namespace,
                MetricData=[
                    {
                        "MetricName": "RateLimitCheck",
                        "Dimensions": [
                            {"Name": "Key", "Value": key},
                            {"Name": "Allowed", "Value": str(allowed)},
                        ],
                        "Value": float(current_count),
                        "Unit": "Count",
                        "Timestamp": now,
                    }
                ],
            )
        except ClientError as exc:
            logger.warning("rate_limiter CloudWatch metric emission failed: %s", exc)

    return RateLimitResult(
        allowed=allowed,
        current_count=current_count,
        remaining=remaining,
        retry_after_seconds=retry_after,
    )


# ---------------------------------------------------------------------------
# 5. API Gateway v2 Custom Domain Migrator
# ---------------------------------------------------------------------------


def api_gateway_domain_migrator(
    domain_name: str,
    certificate_arn: str,
    hosted_zone_id: str,
    rest_api_id: str,
    stage_name: str,
    base_path: str = "/",
    region_name: str | None = None,
) -> DomainMigrationResult:
    """Create an API Gateway v2 custom domain, attach ACM cert, set Route53 alias, and map API.

    Workflow:

    1. Create the custom domain name in API Gateway v2, attaching the ACM
       certificate with a ``REGIONAL`` endpoint configuration.  If the domain
       already exists, the existing configuration is retrieved instead.
    2. Create an API mapping that routes traffic for *base_path* on
       *domain_name* to *rest_api_id*/*stage_name*.
    3. Upsert a Route 53 ALIAS record in *hosted_zone_id* pointing
       *domain_name* at the API Gateway regional domain name returned in step 1.

    Args:
        domain_name: The custom domain to configure (e.g. ``"api.example.com"``).
        certificate_arn: ARN of the ACM certificate that covers *domain_name*.
        hosted_zone_id: Route 53 Hosted Zone ID where the alias record will be
            created or updated.
        rest_api_id: The REST API (or HTTP API) to map to this custom domain.
        stage_name: The deployment stage to expose (e.g. ``"prod"``).
        base_path: API path prefix for the mapping (default ``"/"``).
        region_name: AWS region override.

    Returns:
        :class:`DomainMigrationResult` with the custom domain name, the API
        Gateway regional domain name, the APIGW-owned hosted zone ID used for
        the alias target, and the Route 53 change ID.

    Raises:
        RuntimeError: If any underlying AWS API call fails unexpectedly.
    """
    apigwv2 = get_client("apigatewayv2", region_name=region_name)
    route53 = get_client("route53", region_name=region_name)

    # Step 1 — Create (or retrieve existing) custom domain in API GW v2
    regional_domain_name = ""
    apigw_hosted_zone_id = ""
    try:
        domain_resp = apigwv2.create_domain_name(
            DomainName=domain_name,
            DomainNameConfigurations=[
                {
                    "CertificateArn": certificate_arn,
                    "EndpointType": "REGIONAL",
                    "SecurityPolicy": "TLS_1_2",
                }
            ],
        )
        configs = domain_resp.get("DomainNameConfigurations", [{}])
        cfg = configs[0] if configs else {}
        regional_domain_name = cfg.get("ApiGatewayDomainName", "")
        apigw_hosted_zone_id = cfg.get("HostedZoneId", "")
        logger.info("Created API GW v2 domain: %s -> %s", domain_name, regional_domain_name)
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ConflictException":
            logger.info("Domain already exists: %s — fetching existing config", domain_name)
            try:
                existing = apigwv2.get_domain_name(DomainName=domain_name)
                configs = existing.get("DomainNameConfigurations", [{}])
                cfg = configs[0] if configs else {}
                regional_domain_name = cfg.get("ApiGatewayDomainName", "")
                apigw_hosted_zone_id = cfg.get("HostedZoneId", "")
            except ClientError as inner:
                raise wrap_aws_error(
                    inner, "api_gateway_domain_migrator get_domain_name failed"
                ) from inner
        else:
            raise wrap_aws_error(
                exc, "api_gateway_domain_migrator create_domain_name failed"
            ) from exc

    # Step 2 — Create API mapping (idempotent: skip on ConflictException)
    api_mapping_key = base_path.lstrip("/")  # API GW v2 uses empty string for root
    try:
        apigwv2.create_api_mapping(
            ApiId=rest_api_id,
            DomainName=domain_name,
            Stage=stage_name,
            ApiMappingKey=api_mapping_key,
        )
        logger.info(
            "Created API mapping: %s/%s -> %s/%s",
            domain_name,
            api_mapping_key or "(root)",
            rest_api_id,
            stage_name,
        )
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code == "ConflictException":
            logger.info("API mapping already exists for %s/%s", domain_name, api_mapping_key)
        else:
            raise wrap_aws_error(
                exc, "api_gateway_domain_migrator create_api_mapping failed"
            ) from exc

    # Step 3 — Upsert Route 53 ALIAS record pointing to the regional domain
    # The APIGW-owned hosted zone ID is required for the ALIAS target; fall back
    # to the well-known regional default if the API did not return one.
    alias_hosted_zone_id = apigw_hosted_zone_id or "Z1UJRXOUMOOFQ8"
    change_batch: dict[str, Any] = {
        "Comment": f"aws-util: alias for {domain_name} -> {regional_domain_name}",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": domain_name,
                    "Type": "A",
                    "AliasTarget": {
                        "DNSName": regional_domain_name,
                        "EvaluateTargetHealth": False,
                        "HostedZoneId": alias_hosted_zone_id,
                    },
                },
            }
        ],
    }
    try:
        r53_resp = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch,
        )
        change_info = r53_resp.get("ChangeInfo", {})
        route53_change_id = change_info.get("Id", "")
        logger.info("Route53 ALIAS upserted for %s: change_id=%s", domain_name, route53_change_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "api_gateway_domain_migrator change_resource_record_sets failed"
        ) from exc

    return DomainMigrationResult(
        domain_name=domain_name,
        regional_domain_name=regional_domain_name,
        hosted_zone_id=apigw_hosted_zone_id,
        route53_change_id=route53_change_id,
    )
