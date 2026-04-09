"""Native async API Gateway utilities using :mod:`aws_util.aio._engine`.

Provides async helpers for API Gateway patterns: JWT authorizer, API key
authorizer, request validator, throttle guard, and WebSocket connection
management.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from pydantic import BaseModel

from aws_util.aio._engine import async_client
from aws_util.api_gateway import (
    APIKeyRecord,
    AuthPolicy,
    CreateApiKeyResult,
    CreateAuthorizerResult,
    CreateBasePathMappingResult,
    CreateDeploymentResult,
    CreateDocumentationPartResult,
    CreateDocumentationVersionResult,
    CreateDomainNameAccessAssociationResult,
    CreateDomainNameResult,
    CreateModelResult,
    CreateRequestValidatorResult,
    CreateResourceResult,
    CreateRestApiResult,
    CreateStageResult,
    CreateUsagePlanKeyResult,
    CreateUsagePlanResult,
    CreateVpcLinkResult,
    DeleteApiKeyResult,
    DeleteAuthorizerResult,
    DeleteBasePathMappingResult,
    DeleteClientCertificateResult,
    DeleteDeploymentResult,
    DeleteDocumentationPartResult,
    DeleteDocumentationVersionResult,
    DeleteDomainNameAccessAssociationResult,
    DeleteDomainNameResult,
    DeleteGatewayResponseResult,
    DeleteIntegrationResponseResult,
    DeleteIntegrationResult,
    DeleteMethodResponseResult,
    DeleteMethodResult,
    DeleteModelResult,
    DeleteRequestValidatorResult,
    DeleteResourceResult,
    DeleteRestApiResult,
    DeleteStageResult,
    DeleteUsagePlanKeyResult,
    DeleteUsagePlanResult,
    DeleteVpcLinkResult,
    FlushStageAuthorizersCacheResult,
    FlushStageCacheResult,
    GenerateClientCertificateResult,
    GetAccountResult,
    GetApiKeyResult,
    GetApiKeysResult,
    GetAuthorizerResult,
    GetAuthorizersResult,
    GetBasePathMappingResult,
    GetBasePathMappingsResult,
    GetClientCertificateResult,
    GetClientCertificatesResult,
    GetDeploymentResult,
    GetDeploymentsResult,
    GetDocumentationPartResult,
    GetDocumentationPartsResult,
    GetDocumentationVersionResult,
    GetDocumentationVersionsResult,
    GetDomainNameAccessAssociationsResult,
    GetDomainNameResult,
    GetDomainNamesResult,
    GetExportResult,
    GetGatewayResponseResult,
    GetGatewayResponsesResult,
    GetIntegrationResponseResult,
    GetIntegrationResult,
    GetMethodResponseResult,
    GetMethodResult,
    GetModelResult,
    GetModelsResult,
    GetModelTemplateResult,
    GetRequestValidatorResult,
    GetRequestValidatorsResult,
    GetResourceResult,
    GetResourcesResult,
    GetRestApiResult,
    GetRestApisResult,
    GetSdkResult,
    GetSdkTypeResult,
    GetSdkTypesResult,
    GetStageResult,
    GetStagesResult,
    GetTagsResult,
    GetUsagePlanKeyResult,
    GetUsagePlanKeysResult,
    GetUsagePlanResult,
    GetUsagePlansResult,
    GetUsageResult,
    GetVpcLinkResult,
    GetVpcLinksResult,
    ImportApiKeysResult,
    ImportDocumentationPartsResult,
    ImportRestApiResult,
    PutGatewayResponseResult,
    PutIntegrationResponseResult,
    PutIntegrationResult,
    PutMethodResponseResult,
    PutMethodResult,
    PutRestApiResult,
    RejectDomainNameAccessAssociationResult,
    RunInvokeAuthorizerResult,
    RunInvokeMethodResult,
    TagResourceResult,
    ThrottleResult,
    UntagResourceResult,
    UpdateAccountResult,
    UpdateApiKeyResult,
    UpdateAuthorizerResult,
    UpdateBasePathMappingResult,
    UpdateClientCertificateResult,
    UpdateDeploymentResult,
    UpdateDocumentationPartResult,
    UpdateDocumentationVersionResult,
    UpdateDomainNameResult,
    UpdateGatewayResponseResult,
    UpdateIntegrationResponseResult,
    UpdateIntegrationResult,
    UpdateMethodResponseResult,
    UpdateMethodResult,
    UpdateModelResult,
    UpdateRequestValidatorResult,
    UpdateResourceResult,
    UpdateRestApiResult,
    UpdateStageResult,
    UpdateUsagePlanResult,
    UpdateUsageResult,
    UpdateVpcLinkResult,
    ValidationResult,
    WebSocketConnection,
    _build_auth_response,
    _decode_jwt_payload,
)
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "APIKeyRecord",
    "AuthPolicy",
    "CreateApiKeyResult",
    "CreateAuthorizerResult",
    "CreateBasePathMappingResult",
    "CreateDeploymentResult",
    "CreateDocumentationPartResult",
    "CreateDocumentationVersionResult",
    "CreateDomainNameAccessAssociationResult",
    "CreateDomainNameResult",
    "CreateModelResult",
    "CreateRequestValidatorResult",
    "CreateResourceResult",
    "CreateRestApiResult",
    "CreateStageResult",
    "CreateUsagePlanKeyResult",
    "CreateUsagePlanResult",
    "CreateVpcLinkResult",
    "DeleteApiKeyResult",
    "DeleteAuthorizerResult",
    "DeleteBasePathMappingResult",
    "DeleteClientCertificateResult",
    "DeleteDeploymentResult",
    "DeleteDocumentationPartResult",
    "DeleteDocumentationVersionResult",
    "DeleteDomainNameAccessAssociationResult",
    "DeleteDomainNameResult",
    "DeleteGatewayResponseResult",
    "DeleteIntegrationResponseResult",
    "DeleteIntegrationResult",
    "DeleteMethodResponseResult",
    "DeleteMethodResult",
    "DeleteModelResult",
    "DeleteRequestValidatorResult",
    "DeleteResourceResult",
    "DeleteRestApiResult",
    "DeleteStageResult",
    "DeleteUsagePlanKeyResult",
    "DeleteUsagePlanResult",
    "DeleteVpcLinkResult",
    "FlushStageAuthorizersCacheResult",
    "FlushStageCacheResult",
    "GenerateClientCertificateResult",
    "GetAccountResult",
    "GetApiKeyResult",
    "GetApiKeysResult",
    "GetAuthorizerResult",
    "GetAuthorizersResult",
    "GetBasePathMappingResult",
    "GetBasePathMappingsResult",
    "GetClientCertificateResult",
    "GetClientCertificatesResult",
    "GetDeploymentResult",
    "GetDeploymentsResult",
    "GetDocumentationPartResult",
    "GetDocumentationPartsResult",
    "GetDocumentationVersionResult",
    "GetDocumentationVersionsResult",
    "GetDomainNameAccessAssociationsResult",
    "GetDomainNameResult",
    "GetDomainNamesResult",
    "GetExportResult",
    "GetGatewayResponseResult",
    "GetGatewayResponsesResult",
    "GetIntegrationResponseResult",
    "GetIntegrationResult",
    "GetMethodResponseResult",
    "GetMethodResult",
    "GetModelResult",
    "GetModelTemplateResult",
    "GetModelsResult",
    "GetRequestValidatorResult",
    "GetRequestValidatorsResult",
    "GetResourceResult",
    "GetResourcesResult",
    "GetRestApiResult",
    "GetRestApisResult",
    "GetSdkResult",
    "GetSdkTypeResult",
    "GetSdkTypesResult",
    "GetStageResult",
    "GetStagesResult",
    "GetTagsResult",
    "GetUsagePlanKeyResult",
    "GetUsagePlanKeysResult",
    "GetUsagePlanResult",
    "GetUsagePlansResult",
    "GetUsageResult",
    "GetVpcLinkResult",
    "GetVpcLinksResult",
    "ImportApiKeysResult",
    "ImportDocumentationPartsResult",
    "ImportRestApiResult",
    "PutGatewayResponseResult",
    "PutIntegrationResponseResult",
    "PutIntegrationResult",
    "PutMethodResponseResult",
    "PutMethodResult",
    "PutRestApiResult",
    "RejectDomainNameAccessAssociationResult",
    "RunInvokeAuthorizerResult",
    "RunInvokeMethodResult",
    "TagResourceResult",
    "ThrottleResult",
    "UntagResourceResult",
    "UpdateAccountResult",
    "UpdateApiKeyResult",
    "UpdateAuthorizerResult",
    "UpdateBasePathMappingResult",
    "UpdateClientCertificateResult",
    "UpdateDeploymentResult",
    "UpdateDocumentationPartResult",
    "UpdateDocumentationVersionResult",
    "UpdateDomainNameResult",
    "UpdateGatewayResponseResult",
    "UpdateIntegrationResponseResult",
    "UpdateIntegrationResult",
    "UpdateMethodResponseResult",
    "UpdateMethodResult",
    "UpdateModelResult",
    "UpdateRequestValidatorResult",
    "UpdateResourceResult",
    "UpdateRestApiResult",
    "UpdateStageResult",
    "UpdateUsagePlanResult",
    "UpdateUsageResult",
    "UpdateVpcLinkResult",
    "ValidationResult",
    "WebSocketConnection",
    "api_key_authorizer",
    "create_api_key",
    "create_authorizer",
    "create_base_path_mapping",
    "create_deployment",
    "create_documentation_part",
    "create_documentation_version",
    "create_domain_name",
    "create_domain_name_access_association",
    "create_model",
    "create_request_validator",
    "create_resource",
    "create_rest_api",
    "create_stage",
    "create_usage_plan",
    "create_usage_plan_key",
    "create_vpc_link",
    "delete_api_key",
    "delete_authorizer",
    "delete_base_path_mapping",
    "delete_client_certificate",
    "delete_deployment",
    "delete_documentation_part",
    "delete_documentation_version",
    "delete_domain_name",
    "delete_domain_name_access_association",
    "delete_gateway_response",
    "delete_integration",
    "delete_integration_response",
    "delete_method",
    "delete_method_response",
    "delete_model",
    "delete_request_validator",
    "delete_resource",
    "delete_rest_api",
    "delete_stage",
    "delete_usage_plan",
    "delete_usage_plan_key",
    "delete_vpc_link",
    "flush_stage_authorizers_cache",
    "flush_stage_cache",
    "generate_client_certificate",
    "get_account",
    "get_api_key",
    "get_api_keys",
    "get_authorizer",
    "get_authorizers",
    "get_base_path_mapping",
    "get_base_path_mappings",
    "get_client_certificate",
    "get_client_certificates",
    "get_deployment",
    "get_deployments",
    "get_documentation_part",
    "get_documentation_parts",
    "get_documentation_version",
    "get_documentation_versions",
    "get_domain_name",
    "get_domain_name_access_associations",
    "get_domain_names",
    "get_export",
    "get_gateway_response",
    "get_gateway_responses",
    "get_integration",
    "get_integration_response",
    "get_method",
    "get_method_response",
    "get_model",
    "get_model_template",
    "get_models",
    "get_request_validator",
    "get_request_validators",
    "get_resource",
    "get_resources",
    "get_rest_api",
    "get_rest_apis",
    "get_sdk",
    "get_sdk_type",
    "get_sdk_types",
    "get_stage",
    "get_stages",
    "get_tags",
    "get_usage",
    "get_usage_plan",
    "get_usage_plan_key",
    "get_usage_plan_keys",
    "get_usage_plans",
    "get_vpc_link",
    "get_vpc_links",
    "import_api_keys",
    "import_documentation_parts",
    "import_rest_api",
    "jwt_authorizer",
    "put_gateway_response",
    "put_integration",
    "put_integration_response",
    "put_method",
    "put_method_response",
    "put_rest_api",
    "reject_domain_name_access_association",
    "request_validator",
    "run_invoke_authorizer",
    "run_invoke_method",
    "tag_resource",
    "throttle_guard",
    "untag_resource",
    "update_account",
    "update_api_key",
    "update_authorizer",
    "update_base_path_mapping",
    "update_client_certificate",
    "update_deployment",
    "update_documentation_part",
    "update_documentation_version",
    "update_domain_name",
    "update_gateway_response",
    "update_integration",
    "update_integration_response",
    "update_method",
    "update_method_response",
    "update_model",
    "update_request_validator",
    "update_resource",
    "update_rest_api",
    "update_stage",
    "update_usage",
    "update_usage_plan",
    "update_vpc_link",
    "websocket_broadcast",
    "websocket_connect",
    "websocket_disconnect",
    "websocket_list_connections",
]

# ---------------------------------------------------------------------------
# 1. JWT authorizer
# ---------------------------------------------------------------------------


async def jwt_authorizer(
    token: str,
    resource: str,
    user_pool_id: str | None = None,
    required_claims: dict[str, str] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Lambda authorizer that validates a JWT and returns an IAM policy.

    If *user_pool_id* is provided, the token's ``iss`` claim is verified
    against the Cognito user pool URL.

    Args:
        token: The JWT bearer token (without the ``Bearer `` prefix).
        resource: The API Gateway method ARN to authorize against.
        user_pool_id: Optional Cognito User Pool ID for issuer validation.
        required_claims: Optional dict of claim name -> expected value.
        region_name: AWS region override.

    Returns:
        An API Gateway authorizer policy document (Allow or Deny).
    """
    # JWT decoding is purely local -- no AWS call needed
    try:
        claims = _decode_jwt_payload(token)
    except ValueError:
        return _build_auth_response("unknown", "Deny", resource)

    if user_pool_id is not None:
        region = region_name or "us-east-1"
        expected_iss = f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
        if claims.get("iss") != expected_iss:
            return _build_auth_response(
                "unknown",
                "Deny",
                resource,
            )

    if required_claims:
        for claim_name, expected_value in required_claims.items():
            if claims.get(claim_name) != expected_value:
                return _build_auth_response(
                    claims.get("sub", "unknown"),
                    "Deny",
                    resource,
                )

    exp = claims.get("exp")
    if exp is not None:
        try:
            if int(exp) < int(time.time()):
                return _build_auth_response(
                    claims.get("sub", "unknown"),
                    "Deny",
                    resource,
                )
        except (ValueError, TypeError):
            return _build_auth_response(
                claims.get("sub", "unknown"),
                "Deny",
                resource,
            )

    principal_id = claims.get(
        "sub",
        claims.get("client_id", "unknown"),
    )
    context = {
        k: str(v)
        for k, v in claims.items()
        if k
        in (
            "sub",
            "email",
            "cognito:username",
            "scope",
            "client_id",
        )
    }

    return _build_auth_response(
        principal_id,
        "Allow",
        resource,
        context,
    )


# ---------------------------------------------------------------------------
# 2. API key authorizer
# ---------------------------------------------------------------------------


async def api_key_authorizer(
    api_key: str,
    table_name: str,
    resource: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Lambda authorizer that validates an API key stored in DynamoDB.

    Args:
        api_key: The API key from the request header.
        table_name: DynamoDB table storing API key records.
        resource: The API Gateway method ARN.
        region_name: AWS region override.

    Returns:
        An API Gateway authorizer policy document (Allow or Deny).
    """
    client = async_client("dynamodb", region_name)
    try:
        resp = await client.call(
            "GetItem",
            TableName=table_name,
            Key={"api_key": {"S": api_key}},
        )
    except Exception as exc:
        logger.error("API key lookup failed: %s", exc)
        return _build_auth_response(
            "unknown",
            "Deny",
            resource,
        )

    item = resp.get("Item")
    if not item:
        return _build_auth_response(
            "unknown",
            "Deny",
            resource,
        )

    enabled = item.get("enabled", {}).get("BOOL", False)
    if not enabled:
        return _build_auth_response(
            "unknown",
            "Deny",
            resource,
        )

    owner = item.get("owner", {}).get("S", "unknown")
    context = {"owner": owner}
    description = item.get("description", {}).get("S")
    if description:
        context["description"] = description

    return _build_auth_response(
        owner,
        "Allow",
        resource,
        context,
    )


# ---------------------------------------------------------------------------
# 3. Request validator
# ---------------------------------------------------------------------------


async def request_validator(
    body: str | None,
    model: type[BaseModel],
) -> ValidationResult:
    """Validate an API Gateway request body against a Pydantic model.

    Args:
        body: The raw request body string (JSON).
        model: A Pydantic ``BaseModel`` subclass to validate against.

    Returns:
        A :class:`ValidationResult` indicating whether validation passed.
    """
    # Validation is purely local -- no AWS call needed
    if body is None:
        return ValidationResult(
            valid=False,
            errors=["Request body is required"],
        )

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        return ValidationResult(
            valid=False,
            errors=[f"Invalid JSON: {exc}"],
        )

    try:
        model.model_validate(data)
        return ValidationResult(valid=True)
    except Exception as exc:
        errors = []
        if hasattr(exc, "errors"):
            for err in exc.errors():
                loc = ".".join(str(x) for x in err.get("loc", []))
                msg = err.get("msg", str(err))
                errors.append(f"{loc}: {msg}" if loc else msg)
        else:
            errors.append(str(exc))
        return ValidationResult(
            valid=False,
            errors=errors,
        )


# ---------------------------------------------------------------------------
# 4. Throttle guard
# ---------------------------------------------------------------------------


async def throttle_guard(
    key: str,
    table_name: str,
    limit: int = 100,
    window_seconds: int = 60,
    region_name: str | None = None,
) -> ThrottleResult:
    """Per-user/per-IP rate limiter using DynamoDB atomic counters.

    Args:
        key: The throttle key (e.g. user ID, IP address, API key).
        table_name: DynamoDB table for throttle counters.
        limit: Maximum requests allowed per window (default ``100``).
        window_seconds: TTL window in seconds (default ``60``).
        region_name: AWS region override.

    Returns:
        A :class:`ThrottleResult` with the decision and current count.
    """
    client = async_client("dynamodb", region_name)
    ttl = int(time.time()) + window_seconds

    try:
        resp = await client.call(
            "UpdateItem",
            TableName=table_name,
            Key={"throttle_key": {"S": key}},
            UpdateExpression=("ADD request_count :inc SET #t = if_not_exists(#t, :ttl)"),
            ExpressionAttributeNames={"#t": "ttl"},
            ExpressionAttributeValues={
                ":inc": {"N": "1"},
                ":ttl": {"N": str(ttl)},
            },
            ReturnValues="ALL_NEW",
        )
    except Exception as exc:
        logger.error("Throttle guard update failed: %s", exc)
        return ThrottleResult(
            allowed=True,
            current_count=0,
            limit=limit,
            ttl=ttl,
        )

    attrs = resp.get("Attributes", {})
    current_count = int(attrs.get("request_count", {}).get("N", "0"))
    record_ttl = int(attrs.get("ttl", {}).get("N", str(ttl)))

    return ThrottleResult(
        allowed=current_count <= limit,
        current_count=current_count,
        limit=limit,
        ttl=record_ttl,
    )


# ---------------------------------------------------------------------------
# 5. WebSocket connection manager
# ---------------------------------------------------------------------------


async def websocket_connect(
    connection_id: str,
    table_name: str,
    metadata: dict[str, str] | None = None,
    region_name: str | None = None,
) -> None:
    """Store a new WebSocket connection in DynamoDB.

    Args:
        connection_id: The API Gateway WebSocket connection ID.
        table_name: DynamoDB table for connection records.
        metadata: Optional metadata to store with the connection.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the DynamoDB put fails.
    """
    client = async_client("dynamodb", region_name)
    item: dict[str, Any] = {
        "connection_id": {"S": connection_id},
        "connected_at": {"N": str(int(time.time()))},
    }
    if metadata:
        for k, v in metadata.items():
            item[k] = {"S": v}

    try:
        await client.call(
            "PutItem",
            TableName=table_name,
            Item=item,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to store WebSocket connection {connection_id!r}"
        ) from exc


async def websocket_disconnect(
    connection_id: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Remove a WebSocket connection from DynamoDB.

    Args:
        connection_id: The API Gateway WebSocket connection ID.
        table_name: DynamoDB table for connection records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the DynamoDB delete fails.
    """
    client = async_client("dynamodb", region_name)
    try:
        await client.call(
            "DeleteItem",
            TableName=table_name,
            Key={"connection_id": {"S": connection_id}},
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to remove WebSocket connection {connection_id!r}"
        ) from exc


async def websocket_list_connections(
    table_name: str,
    region_name: str | None = None,
) -> list[WebSocketConnection]:
    """List all active WebSocket connections from DynamoDB.

    Args:
        table_name: DynamoDB table for connection records.
        region_name: AWS region override.

    Returns:
        A list of :class:`WebSocketConnection` objects.

    Raises:
        RuntimeError: If the DynamoDB scan fails.
    """
    client = async_client("dynamodb", region_name)
    connections: list[WebSocketConnection] = []

    try:
        items = await client.paginate(
            "Scan",
            "Items",
            token_input="ExclusiveStartKey",
            token_output="LastEvaluatedKey",
            TableName=table_name,
        )
        for item in items:
            conn_id = item.get("connection_id", {}).get("S", "")
            connected_at = int(item.get("connected_at", {}).get("N", "0"))
            meta = {
                k: v["S"]
                for k, v in item.items()
                if k not in ("connection_id", "connected_at") and "S" in v
            }
            connections.append(
                WebSocketConnection(
                    connection_id=conn_id,
                    connected_at=connected_at,
                    metadata=meta,
                )
            )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to list WebSocket connections from {table_name!r}"
        ) from exc

    return connections


async def websocket_broadcast(
    table_name: str,
    endpoint_url: str,
    message: str | dict | list,
    region_name: str | None = None,
) -> dict[str, int]:
    """Broadcast a message to all connected WebSocket clients.

    Args:
        table_name: DynamoDB table for connection records.
        endpoint_url: The API Gateway WebSocket management endpoint.
        message: The message to send.  Dicts/lists are JSON-serialised.
        region_name: AWS region override.

    Returns:
        A dict with ``sent`` and ``stale`` counts.
    """
    import boto3

    connections = await websocket_list_connections(
        table_name,
        region_name=region_name,
    )
    data = json.dumps(message, default=str) if isinstance(message, (dict, list)) else message

    # The management API requires a custom endpoint_url,
    # so we use boto3 via asyncio.to_thread
    apigw = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=endpoint_url,
        region_name=region_name,
    )

    sent = 0
    stale = 0

    async def _post(conn: WebSocketConnection) -> tuple[int, int]:
        _sent = 0
        _stale = 0
        try:
            await asyncio.to_thread(
                apigw.post_to_connection,
                ConnectionId=conn.connection_id,
                Data=data.encode("utf-8"),
            )
            _sent = 1
        except Exception as exc:
            error_code = ""
            if hasattr(exc, "response"):
                error_code = (
                    exc.response.get("Error", {}).get("Code", "")  # type: ignore[union-attr]
                )
            if error_code == "GoneException":
                await websocket_disconnect(
                    conn.connection_id,
                    table_name,
                    region_name=region_name,
                )
                _stale = 1
            else:
                logger.warning(
                    "Failed to send to connection %s: %s",
                    conn.connection_id,
                    exc,
                )
        return _sent, _stale

    results = await asyncio.gather(
        *[_post(conn) for conn in connections],
    )
    for s, st in results:
        sent += s
        stale += st

    return {"sent": sent, "stale": stale}


# ---------------------------------------------------------------------------
# Generated async boto3 method wrappers
# ---------------------------------------------------------------------------


async def create_api_key(
    *,
    name: str | None = None,
    description: str | None = None,
    enabled: bool | None = None,
    generate_distinct_id: bool | None = None,
    value: str | None = None,
    stage_keys: list[Any] | None = None,
    customer_id: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateApiKeyResult:
    """Create api key.

    Args:
        name: Name.
        description: Description.
        enabled: Enabled.
        generate_distinct_id: Generate distinct id.
        value: Value.
        stage_keys: Stage keys.
        customer_id: Customer id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if enabled is not None:
        kwargs["enabled"] = enabled
    if generate_distinct_id is not None:
        kwargs["generateDistinctId"] = generate_distinct_id
    if value is not None:
        kwargs["value"] = value
    if stage_keys is not None:
        kwargs["stageKeys"] = stage_keys
    if customer_id is not None:
        kwargs["customerId"] = customer_id
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateApiKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create api key") from exc
    return CreateApiKeyResult(
        id=resp.get("id"),
        value=resp.get("value"),
        name=resp.get("name"),
        customer_id=resp.get("customerId"),
        description=resp.get("description"),
        enabled=resp.get("enabled"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
        stage_keys=resp.get("stageKeys"),
        tags=resp.get("tags"),
    )


async def create_authorizer(
    rest_api_id: str,
    name: str,
    type: str,
    *,
    provider_ar_ns: list[Any] | None = None,
    auth_type: str | None = None,
    authorizer_uri: str | None = None,
    authorizer_credentials: str | None = None,
    identity_source: str | None = None,
    identity_validation_expression: str | None = None,
    authorizer_result_ttl_in_seconds: int | None = None,
    region_name: str | None = None,
) -> CreateAuthorizerResult:
    """Create authorizer.

    Args:
        rest_api_id: Rest api id.
        name: Name.
        type: Type.
        provider_ar_ns: Provider ar ns.
        auth_type: Auth type.
        authorizer_uri: Authorizer uri.
        authorizer_credentials: Authorizer credentials.
        identity_source: Identity source.
        identity_validation_expression: Identity validation expression.
        authorizer_result_ttl_in_seconds: Authorizer result ttl in seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["name"] = name
    kwargs["type"] = type
    if provider_ar_ns is not None:
        kwargs["providerARNs"] = provider_ar_ns
    if auth_type is not None:
        kwargs["authType"] = auth_type
    if authorizer_uri is not None:
        kwargs["authorizerUri"] = authorizer_uri
    if authorizer_credentials is not None:
        kwargs["authorizerCredentials"] = authorizer_credentials
    if identity_source is not None:
        kwargs["identitySource"] = identity_source
    if identity_validation_expression is not None:
        kwargs["identityValidationExpression"] = identity_validation_expression
    if authorizer_result_ttl_in_seconds is not None:
        kwargs["authorizerResultTtlInSeconds"] = authorizer_result_ttl_in_seconds
    try:
        resp = await client.call("CreateAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create authorizer") from exc
    return CreateAuthorizerResult(
        id=resp.get("id"),
        name=resp.get("name"),
        type=resp.get("type"),
        provider_ar_ns=resp.get("providerARNs"),
        auth_type=resp.get("authType"),
        authorizer_uri=resp.get("authorizerUri"),
        authorizer_credentials=resp.get("authorizerCredentials"),
        identity_source=resp.get("identitySource"),
        identity_validation_expression=resp.get("identityValidationExpression"),
        authorizer_result_ttl_in_seconds=resp.get("authorizerResultTtlInSeconds"),
    )


async def create_base_path_mapping(
    domain_name: str,
    rest_api_id: str,
    *,
    domain_name_id: str | None = None,
    base_path: str | None = None,
    stage: str | None = None,
    region_name: str | None = None,
) -> CreateBasePathMappingResult:
    """Create base path mapping.

    Args:
        domain_name: Domain name.
        rest_api_id: Rest api id.
        domain_name_id: Domain name id.
        base_path: Base path.
        stage: Stage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["restApiId"] = rest_api_id
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    if base_path is not None:
        kwargs["basePath"] = base_path
    if stage is not None:
        kwargs["stage"] = stage
    try:
        resp = await client.call("CreateBasePathMapping", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create base path mapping") from exc
    return CreateBasePathMappingResult(
        base_path=resp.get("basePath"),
        rest_api_id=resp.get("restApiId"),
        stage=resp.get("stage"),
    )


async def create_deployment(
    rest_api_id: str,
    *,
    stage_name: str | None = None,
    stage_description: str | None = None,
    description: str | None = None,
    cache_cluster_enabled: bool | None = None,
    cache_cluster_size: str | None = None,
    variables: dict[str, Any] | None = None,
    canary_settings: dict[str, Any] | None = None,
    tracing_enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateDeploymentResult:
    """Create deployment.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        stage_description: Stage description.
        description: Description.
        cache_cluster_enabled: Cache cluster enabled.
        cache_cluster_size: Cache cluster size.
        variables: Variables.
        canary_settings: Canary settings.
        tracing_enabled: Tracing enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if stage_name is not None:
        kwargs["stageName"] = stage_name
    if stage_description is not None:
        kwargs["stageDescription"] = stage_description
    if description is not None:
        kwargs["description"] = description
    if cache_cluster_enabled is not None:
        kwargs["cacheClusterEnabled"] = cache_cluster_enabled
    if cache_cluster_size is not None:
        kwargs["cacheClusterSize"] = cache_cluster_size
    if variables is not None:
        kwargs["variables"] = variables
    if canary_settings is not None:
        kwargs["canarySettings"] = canary_settings
    if tracing_enabled is not None:
        kwargs["tracingEnabled"] = tracing_enabled
    try:
        resp = await client.call("CreateDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create deployment") from exc
    return CreateDeploymentResult(
        id=resp.get("id"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        api_summary=resp.get("apiSummary"),
    )


async def create_documentation_part(
    rest_api_id: str,
    location: dict[str, Any],
    properties: str,
    *,
    region_name: str | None = None,
) -> CreateDocumentationPartResult:
    """Create documentation part.

    Args:
        rest_api_id: Rest api id.
        location: Location.
        properties: Properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["location"] = location
    kwargs["properties"] = properties
    try:
        resp = await client.call("CreateDocumentationPart", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create documentation part") from exc
    return CreateDocumentationPartResult(
        id=resp.get("id"),
        location=resp.get("location"),
        properties=resp.get("properties"),
    )


async def create_documentation_version(
    rest_api_id: str,
    documentation_version: str,
    *,
    stage_name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateDocumentationVersionResult:
    """Create documentation version.

    Args:
        rest_api_id: Rest api id.
        documentation_version: Documentation version.
        stage_name: Stage name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationVersion"] = documentation_version
    if stage_name is not None:
        kwargs["stageName"] = stage_name
    if description is not None:
        kwargs["description"] = description
    try:
        resp = await client.call("CreateDocumentationVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create documentation version") from exc
    return CreateDocumentationVersionResult(
        version=resp.get("version"),
        created_date=resp.get("createdDate"),
        description=resp.get("description"),
    )


async def create_domain_name(
    domain_name: str,
    *,
    certificate_name: str | None = None,
    certificate_body: str | None = None,
    certificate_private_key: str | None = None,
    certificate_chain: str | None = None,
    certificate_arn: str | None = None,
    regional_certificate_name: str | None = None,
    regional_certificate_arn: str | None = None,
    endpoint_configuration: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    security_policy: str | None = None,
    mutual_tls_authentication: dict[str, Any] | None = None,
    ownership_verification_certificate_arn: str | None = None,
    policy: str | None = None,
    routing_mode: str | None = None,
    region_name: str | None = None,
) -> CreateDomainNameResult:
    """Create domain name.

    Args:
        domain_name: Domain name.
        certificate_name: Certificate name.
        certificate_body: Certificate body.
        certificate_private_key: Certificate private key.
        certificate_chain: Certificate chain.
        certificate_arn: Certificate arn.
        regional_certificate_name: Regional certificate name.
        regional_certificate_arn: Regional certificate arn.
        endpoint_configuration: Endpoint configuration.
        tags: Tags.
        security_policy: Security policy.
        mutual_tls_authentication: Mutual tls authentication.
        ownership_verification_certificate_arn: Ownership verification certificate arn.
        policy: Policy.
        routing_mode: Routing mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if certificate_name is not None:
        kwargs["certificateName"] = certificate_name
    if certificate_body is not None:
        kwargs["certificateBody"] = certificate_body
    if certificate_private_key is not None:
        kwargs["certificatePrivateKey"] = certificate_private_key
    if certificate_chain is not None:
        kwargs["certificateChain"] = certificate_chain
    if certificate_arn is not None:
        kwargs["certificateArn"] = certificate_arn
    if regional_certificate_name is not None:
        kwargs["regionalCertificateName"] = regional_certificate_name
    if regional_certificate_arn is not None:
        kwargs["regionalCertificateArn"] = regional_certificate_arn
    if endpoint_configuration is not None:
        kwargs["endpointConfiguration"] = endpoint_configuration
    if tags is not None:
        kwargs["tags"] = tags
    if security_policy is not None:
        kwargs["securityPolicy"] = security_policy
    if mutual_tls_authentication is not None:
        kwargs["mutualTlsAuthentication"] = mutual_tls_authentication
    if ownership_verification_certificate_arn is not None:
        kwargs["ownershipVerificationCertificateArn"] = ownership_verification_certificate_arn
    if policy is not None:
        kwargs["policy"] = policy
    if routing_mode is not None:
        kwargs["routingMode"] = routing_mode
    try:
        resp = await client.call("CreateDomainName", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create domain name") from exc
    return CreateDomainNameResult(
        domain_name=resp.get("domainName"),
        domain_name_id=resp.get("domainNameId"),
        domain_name_arn=resp.get("domainNameArn"),
        certificate_name=resp.get("certificateName"),
        certificate_arn=resp.get("certificateArn"),
        certificate_upload_date=resp.get("certificateUploadDate"),
        regional_domain_name=resp.get("regionalDomainName"),
        regional_hosted_zone_id=resp.get("regionalHostedZoneId"),
        regional_certificate_name=resp.get("regionalCertificateName"),
        regional_certificate_arn=resp.get("regionalCertificateArn"),
        distribution_domain_name=resp.get("distributionDomainName"),
        distribution_hosted_zone_id=resp.get("distributionHostedZoneId"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        domain_name_status=resp.get("domainNameStatus"),
        domain_name_status_message=resp.get("domainNameStatusMessage"),
        security_policy=resp.get("securityPolicy"),
        tags=resp.get("tags"),
        mutual_tls_authentication=resp.get("mutualTlsAuthentication"),
        ownership_verification_certificate_arn=resp.get("ownershipVerificationCertificateArn"),
        management_policy=resp.get("managementPolicy"),
        policy=resp.get("policy"),
        routing_mode=resp.get("routingMode"),
    )


async def create_domain_name_access_association(
    domain_name_arn: str,
    access_association_source_type: str,
    access_association_source: str,
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDomainNameAccessAssociationResult:
    """Create domain name access association.

    Args:
        domain_name_arn: Domain name arn.
        access_association_source_type: Access association source type.
        access_association_source: Access association source.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainNameArn"] = domain_name_arn
    kwargs["accessAssociationSourceType"] = access_association_source_type
    kwargs["accessAssociationSource"] = access_association_source
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDomainNameAccessAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create domain name access association") from exc
    return CreateDomainNameAccessAssociationResult(
        domain_name_access_association_arn=resp.get("domainNameAccessAssociationArn"),
        domain_name_arn=resp.get("domainNameArn"),
        access_association_source_type=resp.get("accessAssociationSourceType"),
        access_association_source=resp.get("accessAssociationSource"),
        tags=resp.get("tags"),
    )


async def create_model(
    rest_api_id: str,
    name: str,
    content_type: str,
    *,
    description: str | None = None,
    model_schema: str | None = None,
    region_name: str | None = None,
) -> CreateModelResult:
    """Create model.

    Args:
        rest_api_id: Rest api id.
        name: Name.
        content_type: Content type.
        description: Description.
        model_schema: Schema.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["name"] = name
    kwargs["contentType"] = content_type
    if description is not None:
        kwargs["description"] = description
    if model_schema is not None:
        kwargs["schema"] = model_schema
    try:
        resp = await client.call("CreateModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create model") from exc
    return CreateModelResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        model_schema=resp.get("schema"),
        content_type=resp.get("contentType"),
    )


async def create_request_validator(
    rest_api_id: str,
    *,
    name: str | None = None,
    validate_request_body: bool | None = None,
    validate_request_parameters: bool | None = None,
    region_name: str | None = None,
) -> CreateRequestValidatorResult:
    """Create request validator.

    Args:
        rest_api_id: Rest api id.
        name: Name.
        validate_request_body: Validate request body.
        validate_request_parameters: Validate request parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if name is not None:
        kwargs["name"] = name
    if validate_request_body is not None:
        kwargs["validateRequestBody"] = validate_request_body
    if validate_request_parameters is not None:
        kwargs["validateRequestParameters"] = validate_request_parameters
    try:
        resp = await client.call("CreateRequestValidator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create request validator") from exc
    return CreateRequestValidatorResult(
        id=resp.get("id"),
        name=resp.get("name"),
        validate_request_body=resp.get("validateRequestBody"),
        validate_request_parameters=resp.get("validateRequestParameters"),
    )


async def create_resource(
    rest_api_id: str,
    parent_id: str,
    path_part: str,
    *,
    region_name: str | None = None,
) -> CreateResourceResult:
    """Create resource.

    Args:
        rest_api_id: Rest api id.
        parent_id: Parent id.
        path_part: Path part.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["parentId"] = parent_id
    kwargs["pathPart"] = path_part
    try:
        resp = await client.call("CreateResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create resource") from exc
    return CreateResourceResult(
        id=resp.get("id"),
        parent_id=resp.get("parentId"),
        path_part=resp.get("pathPart"),
        path=resp.get("path"),
        resource_methods=resp.get("resourceMethods"),
    )


async def create_rest_api(
    name: str,
    *,
    description: str | None = None,
    version: str | None = None,
    clone_from: str | None = None,
    binary_media_types: list[Any] | None = None,
    minimum_compression_size: int | None = None,
    api_key_source: str | None = None,
    endpoint_configuration: dict[str, Any] | None = None,
    policy: str | None = None,
    tags: dict[str, Any] | None = None,
    disable_execute_api_endpoint: bool | None = None,
    region_name: str | None = None,
) -> CreateRestApiResult:
    """Create rest api.

    Args:
        name: Name.
        description: Description.
        version: Version.
        clone_from: Clone from.
        binary_media_types: Binary media types.
        minimum_compression_size: Minimum compression size.
        api_key_source: Api key source.
        endpoint_configuration: Endpoint configuration.
        policy: Policy.
        tags: Tags.
        disable_execute_api_endpoint: Disable execute api endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if version is not None:
        kwargs["version"] = version
    if clone_from is not None:
        kwargs["cloneFrom"] = clone_from
    if binary_media_types is not None:
        kwargs["binaryMediaTypes"] = binary_media_types
    if minimum_compression_size is not None:
        kwargs["minimumCompressionSize"] = minimum_compression_size
    if api_key_source is not None:
        kwargs["apiKeySource"] = api_key_source
    if endpoint_configuration is not None:
        kwargs["endpointConfiguration"] = endpoint_configuration
    if policy is not None:
        kwargs["policy"] = policy
    if tags is not None:
        kwargs["tags"] = tags
    if disable_execute_api_endpoint is not None:
        kwargs["disableExecuteApiEndpoint"] = disable_execute_api_endpoint
    try:
        resp = await client.call("CreateRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create rest api") from exc
    return CreateRestApiResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        version=resp.get("version"),
        warnings=resp.get("warnings"),
        binary_media_types=resp.get("binaryMediaTypes"),
        minimum_compression_size=resp.get("minimumCompressionSize"),
        api_key_source=resp.get("apiKeySource"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        policy=resp.get("policy"),
        tags=resp.get("tags"),
        disable_execute_api_endpoint=resp.get("disableExecuteApiEndpoint"),
        root_resource_id=resp.get("rootResourceId"),
    )


async def create_stage(
    rest_api_id: str,
    stage_name: str,
    deployment_id: str,
    *,
    description: str | None = None,
    cache_cluster_enabled: bool | None = None,
    cache_cluster_size: str | None = None,
    variables: dict[str, Any] | None = None,
    documentation_version: str | None = None,
    canary_settings: dict[str, Any] | None = None,
    tracing_enabled: bool | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateStageResult:
    """Create stage.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        deployment_id: Deployment id.
        description: Description.
        cache_cluster_enabled: Cache cluster enabled.
        cache_cluster_size: Cache cluster size.
        variables: Variables.
        documentation_version: Documentation version.
        canary_settings: Canary settings.
        tracing_enabled: Tracing enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    kwargs["deploymentId"] = deployment_id
    if description is not None:
        kwargs["description"] = description
    if cache_cluster_enabled is not None:
        kwargs["cacheClusterEnabled"] = cache_cluster_enabled
    if cache_cluster_size is not None:
        kwargs["cacheClusterSize"] = cache_cluster_size
    if variables is not None:
        kwargs["variables"] = variables
    if documentation_version is not None:
        kwargs["documentationVersion"] = documentation_version
    if canary_settings is not None:
        kwargs["canarySettings"] = canary_settings
    if tracing_enabled is not None:
        kwargs["tracingEnabled"] = tracing_enabled
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateStage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create stage") from exc
    return CreateStageResult(
        deployment_id=resp.get("deploymentId"),
        client_certificate_id=resp.get("clientCertificateId"),
        stage_name=resp.get("stageName"),
        description=resp.get("description"),
        cache_cluster_enabled=resp.get("cacheClusterEnabled"),
        cache_cluster_size=resp.get("cacheClusterSize"),
        cache_cluster_status=resp.get("cacheClusterStatus"),
        method_settings=resp.get("methodSettings"),
        variables=resp.get("variables"),
        documentation_version=resp.get("documentationVersion"),
        access_log_settings=resp.get("accessLogSettings"),
        canary_settings=resp.get("canarySettings"),
        tracing_enabled=resp.get("tracingEnabled"),
        web_acl_arn=resp.get("webAclArn"),
        tags=resp.get("tags"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
    )


async def create_usage_plan(
    name: str,
    *,
    description: str | None = None,
    api_stages: list[Any] | None = None,
    throttle: dict[str, Any] | None = None,
    quota: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUsagePlanResult:
    """Create usage plan.

    Args:
        name: Name.
        description: Description.
        api_stages: Api stages.
        throttle: Throttle.
        quota: Quota.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if description is not None:
        kwargs["description"] = description
    if api_stages is not None:
        kwargs["apiStages"] = api_stages
    if throttle is not None:
        kwargs["throttle"] = throttle
    if quota is not None:
        kwargs["quota"] = quota
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateUsagePlan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create usage plan") from exc
    return CreateUsagePlanResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        api_stages=resp.get("apiStages"),
        throttle=resp.get("throttle"),
        quota=resp.get("quota"),
        product_code=resp.get("productCode"),
        tags=resp.get("tags"),
    )


async def create_usage_plan_key(
    usage_plan_id: str,
    key_id: str,
    key_type: str,
    *,
    region_name: str | None = None,
) -> CreateUsagePlanKeyResult:
    """Create usage plan key.

    Args:
        usage_plan_id: Usage plan id.
        key_id: Key id.
        key_type: Key type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    kwargs["keyId"] = key_id
    kwargs["keyType"] = key_type
    try:
        resp = await client.call("CreateUsagePlanKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create usage plan key") from exc
    return CreateUsagePlanKeyResult(
        id=resp.get("id"),
        type=resp.get("type"),
        value=resp.get("value"),
        name=resp.get("name"),
    )


async def create_vpc_link(
    name: str,
    target_arns: list[Any],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateVpcLinkResult:
    """Create vpc link.

    Args:
        name: Name.
        target_arns: Target arns.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["targetArns"] = target_arns
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateVpcLink", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc link") from exc
    return CreateVpcLinkResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        target_arns=resp.get("targetArns"),
        status=resp.get("status"),
        status_message=resp.get("statusMessage"),
        tags=resp.get("tags"),
    )


async def delete_api_key(
    api_key: str,
    *,
    region_name: str | None = None,
) -> DeleteApiKeyResult:
    """Delete api key.

    Args:
        api_key: Api key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["apiKey"] = api_key
    try:
        await client.call("DeleteApiKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete api key") from exc
    return DeleteApiKeyResult()


async def delete_authorizer(
    rest_api_id: str,
    authorizer_id: str,
    *,
    region_name: str | None = None,
) -> DeleteAuthorizerResult:
    """Delete authorizer.

    Args:
        rest_api_id: Rest api id.
        authorizer_id: Authorizer id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["authorizerId"] = authorizer_id
    try:
        await client.call("DeleteAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete authorizer") from exc
    return DeleteAuthorizerResult()


async def delete_base_path_mapping(
    domain_name: str,
    base_path: str,
    *,
    domain_name_id: str | None = None,
    region_name: str | None = None,
) -> DeleteBasePathMappingResult:
    """Delete base path mapping.

    Args:
        domain_name: Domain name.
        base_path: Base path.
        domain_name_id: Domain name id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["basePath"] = base_path
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    try:
        await client.call("DeleteBasePathMapping", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete base path mapping") from exc
    return DeleteBasePathMappingResult()


async def delete_client_certificate(
    client_certificate_id: str,
    *,
    region_name: str | None = None,
) -> DeleteClientCertificateResult:
    """Delete client certificate.

    Args:
        client_certificate_id: Client certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientCertificateId"] = client_certificate_id
    try:
        await client.call("DeleteClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete client certificate") from exc
    return DeleteClientCertificateResult()


async def delete_deployment(
    rest_api_id: str,
    deployment_id: str,
    *,
    region_name: str | None = None,
) -> DeleteDeploymentResult:
    """Delete deployment.

    Args:
        rest_api_id: Rest api id.
        deployment_id: Deployment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["deploymentId"] = deployment_id
    try:
        await client.call("DeleteDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete deployment") from exc
    return DeleteDeploymentResult()


async def delete_documentation_part(
    rest_api_id: str,
    documentation_part_id: str,
    *,
    region_name: str | None = None,
) -> DeleteDocumentationPartResult:
    """Delete documentation part.

    Args:
        rest_api_id: Rest api id.
        documentation_part_id: Documentation part id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationPartId"] = documentation_part_id
    try:
        await client.call("DeleteDocumentationPart", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete documentation part") from exc
    return DeleteDocumentationPartResult()


async def delete_documentation_version(
    rest_api_id: str,
    documentation_version: str,
    *,
    region_name: str | None = None,
) -> DeleteDocumentationVersionResult:
    """Delete documentation version.

    Args:
        rest_api_id: Rest api id.
        documentation_version: Documentation version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationVersion"] = documentation_version
    try:
        await client.call("DeleteDocumentationVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete documentation version") from exc
    return DeleteDocumentationVersionResult()


async def delete_domain_name(
    domain_name: str,
    *,
    domain_name_id: str | None = None,
    region_name: str | None = None,
) -> DeleteDomainNameResult:
    """Delete domain name.

    Args:
        domain_name: Domain name.
        domain_name_id: Domain name id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    try:
        await client.call("DeleteDomainName", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain name") from exc
    return DeleteDomainNameResult()


async def delete_domain_name_access_association(
    domain_name_access_association_arn: str,
    *,
    region_name: str | None = None,
) -> DeleteDomainNameAccessAssociationResult:
    """Delete domain name access association.

    Args:
        domain_name_access_association_arn: Domain name access association arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainNameAccessAssociationArn"] = domain_name_access_association_arn
    try:
        await client.call("DeleteDomainNameAccessAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain name access association") from exc
    return DeleteDomainNameAccessAssociationResult()


async def delete_gateway_response(
    rest_api_id: str,
    response_type: str,
    *,
    region_name: str | None = None,
) -> DeleteGatewayResponseResult:
    """Delete gateway response.

    Args:
        rest_api_id: Rest api id.
        response_type: Response type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["responseType"] = response_type
    try:
        await client.call("DeleteGatewayResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete gateway response") from exc
    return DeleteGatewayResponseResult()


async def delete_integration(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    region_name: str | None = None,
) -> DeleteIntegrationResult:
    """Delete integration.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    try:
        await client.call("DeleteIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete integration") from exc
    return DeleteIntegrationResult()


async def delete_integration_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    region_name: str | None = None,
) -> DeleteIntegrationResponseResult:
    """Delete integration response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    try:
        await client.call("DeleteIntegrationResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete integration response") from exc
    return DeleteIntegrationResponseResult()


async def delete_method(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    region_name: str | None = None,
) -> DeleteMethodResult:
    """Delete method.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    try:
        await client.call("DeleteMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete method") from exc
    return DeleteMethodResult()


async def delete_method_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    region_name: str | None = None,
) -> DeleteMethodResponseResult:
    """Delete method response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    try:
        await client.call("DeleteMethodResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete method response") from exc
    return DeleteMethodResponseResult()


async def delete_model(
    rest_api_id: str,
    model_name: str,
    *,
    region_name: str | None = None,
) -> DeleteModelResult:
    """Delete model.

    Args:
        rest_api_id: Rest api id.
        model_name: Model name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["modelName"] = model_name
    try:
        await client.call("DeleteModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete model") from exc
    return DeleteModelResult()


async def delete_request_validator(
    rest_api_id: str,
    request_validator_id: str,
    *,
    region_name: str | None = None,
) -> DeleteRequestValidatorResult:
    """Delete request validator.

    Args:
        rest_api_id: Rest api id.
        request_validator_id: Request validator id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["requestValidatorId"] = request_validator_id
    try:
        await client.call("DeleteRequestValidator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete request validator") from exc
    return DeleteRequestValidatorResult()


async def delete_resource(
    rest_api_id: str,
    resource_id: str,
    *,
    region_name: str | None = None,
) -> DeleteResourceResult:
    """Delete resource.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    try:
        await client.call("DeleteResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource") from exc
    return DeleteResourceResult()


async def delete_rest_api(
    rest_api_id: str,
    *,
    region_name: str | None = None,
) -> DeleteRestApiResult:
    """Delete rest api.

    Args:
        rest_api_id: Rest api id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    try:
        await client.call("DeleteRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete rest api") from exc
    return DeleteRestApiResult()


async def delete_stage(
    rest_api_id: str,
    stage_name: str,
    *,
    region_name: str | None = None,
) -> DeleteStageResult:
    """Delete stage.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    try:
        await client.call("DeleteStage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete stage") from exc
    return DeleteStageResult()


async def delete_usage_plan(
    usage_plan_id: str,
    *,
    region_name: str | None = None,
) -> DeleteUsagePlanResult:
    """Delete usage plan.

    Args:
        usage_plan_id: Usage plan id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    try:
        await client.call("DeleteUsagePlan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete usage plan") from exc
    return DeleteUsagePlanResult()


async def delete_usage_plan_key(
    usage_plan_id: str,
    key_id: str,
    *,
    region_name: str | None = None,
) -> DeleteUsagePlanKeyResult:
    """Delete usage plan key.

    Args:
        usage_plan_id: Usage plan id.
        key_id: Key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    kwargs["keyId"] = key_id
    try:
        await client.call("DeleteUsagePlanKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete usage plan key") from exc
    return DeleteUsagePlanKeyResult()


async def delete_vpc_link(
    vpc_link_id: str,
    *,
    region_name: str | None = None,
) -> DeleteVpcLinkResult:
    """Delete vpc link.

    Args:
        vpc_link_id: Vpc link id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["vpcLinkId"] = vpc_link_id
    try:
        await client.call("DeleteVpcLink", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc link") from exc
    return DeleteVpcLinkResult()


async def flush_stage_authorizers_cache(
    rest_api_id: str,
    stage_name: str,
    *,
    region_name: str | None = None,
) -> FlushStageAuthorizersCacheResult:
    """Flush stage authorizers cache.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    try:
        await client.call("FlushStageAuthorizersCache", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to flush stage authorizers cache") from exc
    return FlushStageAuthorizersCacheResult()


async def flush_stage_cache(
    rest_api_id: str,
    stage_name: str,
    *,
    region_name: str | None = None,
) -> FlushStageCacheResult:
    """Flush stage cache.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    try:
        await client.call("FlushStageCache", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to flush stage cache") from exc
    return FlushStageCacheResult()


async def generate_client_certificate(
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GenerateClientCertificateResult:
    """Generate client certificate.

    Args:
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("GenerateClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate client certificate") from exc
    return GenerateClientCertificateResult(
        client_certificate_id=resp.get("clientCertificateId"),
        description=resp.get("description"),
        pem_encoded_certificate=resp.get("pemEncodedCertificate"),
        created_date=resp.get("createdDate"),
        expiration_date=resp.get("expirationDate"),
        tags=resp.get("tags"),
    )


async def get_account(
    *,
    region_name: str | None = None,
) -> GetAccountResult:
    """Get account.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    try:
        resp = await client.call("GetAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account") from exc
    return GetAccountResult(
        cloudwatch_role_arn=resp.get("cloudwatchRoleArn"),
        throttle_settings=resp.get("throttleSettings"),
        features=resp.get("features"),
        api_key_version=resp.get("apiKeyVersion"),
    )


async def get_api_key(
    api_key: str,
    *,
    include_value: bool | None = None,
    region_name: str | None = None,
) -> GetApiKeyResult:
    """Get api key.

    Args:
        api_key: Api key.
        include_value: Include value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["apiKey"] = api_key
    if include_value is not None:
        kwargs["includeValue"] = include_value
    try:
        resp = await client.call("GetApiKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get api key") from exc
    return GetApiKeyResult(
        id=resp.get("id"),
        value=resp.get("value"),
        name=resp.get("name"),
        customer_id=resp.get("customerId"),
        description=resp.get("description"),
        enabled=resp.get("enabled"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
        stage_keys=resp.get("stageKeys"),
        tags=resp.get("tags"),
    )


async def get_api_keys(
    *,
    position: str | None = None,
    limit: int | None = None,
    name_query: str | None = None,
    customer_id: str | None = None,
    include_values: bool | None = None,
    region_name: str | None = None,
) -> GetApiKeysResult:
    """Get api keys.

    Args:
        position: Position.
        limit: Limit.
        name_query: Name query.
        customer_id: Customer id.
        include_values: Include values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if name_query is not None:
        kwargs["nameQuery"] = name_query
    if customer_id is not None:
        kwargs["customerId"] = customer_id
    if include_values is not None:
        kwargs["includeValues"] = include_values
    try:
        resp = await client.call("GetApiKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get api keys") from exc
    return GetApiKeysResult(
        warnings=resp.get("warnings"),
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_authorizer(
    rest_api_id: str,
    authorizer_id: str,
    *,
    region_name: str | None = None,
) -> GetAuthorizerResult:
    """Get authorizer.

    Args:
        rest_api_id: Rest api id.
        authorizer_id: Authorizer id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["authorizerId"] = authorizer_id
    try:
        resp = await client.call("GetAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get authorizer") from exc
    return GetAuthorizerResult(
        id=resp.get("id"),
        name=resp.get("name"),
        type=resp.get("type"),
        provider_ar_ns=resp.get("providerARNs"),
        auth_type=resp.get("authType"),
        authorizer_uri=resp.get("authorizerUri"),
        authorizer_credentials=resp.get("authorizerCredentials"),
        identity_source=resp.get("identitySource"),
        identity_validation_expression=resp.get("identityValidationExpression"),
        authorizer_result_ttl_in_seconds=resp.get("authorizerResultTtlInSeconds"),
    )


async def get_authorizers(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetAuthorizersResult:
    """Get authorizers.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetAuthorizers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get authorizers") from exc
    return GetAuthorizersResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_base_path_mapping(
    domain_name: str,
    base_path: str,
    *,
    domain_name_id: str | None = None,
    region_name: str | None = None,
) -> GetBasePathMappingResult:
    """Get base path mapping.

    Args:
        domain_name: Domain name.
        base_path: Base path.
        domain_name_id: Domain name id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["basePath"] = base_path
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    try:
        resp = await client.call("GetBasePathMapping", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get base path mapping") from exc
    return GetBasePathMappingResult(
        base_path=resp.get("basePath"),
        rest_api_id=resp.get("restApiId"),
        stage=resp.get("stage"),
    )


async def get_base_path_mappings(
    domain_name: str,
    *,
    domain_name_id: str | None = None,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetBasePathMappingsResult:
    """Get base path mappings.

    Args:
        domain_name: Domain name.
        domain_name_id: Domain name id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetBasePathMappings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get base path mappings") from exc
    return GetBasePathMappingsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_client_certificate(
    client_certificate_id: str,
    *,
    region_name: str | None = None,
) -> GetClientCertificateResult:
    """Get client certificate.

    Args:
        client_certificate_id: Client certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientCertificateId"] = client_certificate_id
    try:
        resp = await client.call("GetClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get client certificate") from exc
    return GetClientCertificateResult(
        client_certificate_id=resp.get("clientCertificateId"),
        description=resp.get("description"),
        pem_encoded_certificate=resp.get("pemEncodedCertificate"),
        created_date=resp.get("createdDate"),
        expiration_date=resp.get("expirationDate"),
        tags=resp.get("tags"),
    )


async def get_client_certificates(
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetClientCertificatesResult:
    """Get client certificates.

    Args:
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetClientCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get client certificates") from exc
    return GetClientCertificatesResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_deployment(
    rest_api_id: str,
    deployment_id: str,
    *,
    embed: list[Any] | None = None,
    region_name: str | None = None,
) -> GetDeploymentResult:
    """Get deployment.

    Args:
        rest_api_id: Rest api id.
        deployment_id: Deployment id.
        embed: Embed.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["deploymentId"] = deployment_id
    if embed is not None:
        kwargs["embed"] = embed
    try:
        resp = await client.call("GetDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get deployment") from exc
    return GetDeploymentResult(
        id=resp.get("id"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        api_summary=resp.get("apiSummary"),
    )


async def get_deployments(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetDeploymentsResult:
    """Get deployments.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetDeployments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get deployments") from exc
    return GetDeploymentsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_documentation_part(
    rest_api_id: str,
    documentation_part_id: str,
    *,
    region_name: str | None = None,
) -> GetDocumentationPartResult:
    """Get documentation part.

    Args:
        rest_api_id: Rest api id.
        documentation_part_id: Documentation part id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationPartId"] = documentation_part_id
    try:
        resp = await client.call("GetDocumentationPart", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get documentation part") from exc
    return GetDocumentationPartResult(
        id=resp.get("id"),
        location=resp.get("location"),
        properties=resp.get("properties"),
    )


async def get_documentation_parts(
    rest_api_id: str,
    *,
    type: str | None = None,
    name_query: str | None = None,
    path: str | None = None,
    position: str | None = None,
    limit: int | None = None,
    location_status: str | None = None,
    region_name: str | None = None,
) -> GetDocumentationPartsResult:
    """Get documentation parts.

    Args:
        rest_api_id: Rest api id.
        type: Type.
        name_query: Name query.
        path: Path.
        position: Position.
        limit: Limit.
        location_status: Location status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if type is not None:
        kwargs["type"] = type
    if name_query is not None:
        kwargs["nameQuery"] = name_query
    if path is not None:
        kwargs["path"] = path
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if location_status is not None:
        kwargs["locationStatus"] = location_status
    try:
        resp = await client.call("GetDocumentationParts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get documentation parts") from exc
    return GetDocumentationPartsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_documentation_version(
    rest_api_id: str,
    documentation_version: str,
    *,
    region_name: str | None = None,
) -> GetDocumentationVersionResult:
    """Get documentation version.

    Args:
        rest_api_id: Rest api id.
        documentation_version: Documentation version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationVersion"] = documentation_version
    try:
        resp = await client.call("GetDocumentationVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get documentation version") from exc
    return GetDocumentationVersionResult(
        version=resp.get("version"),
        created_date=resp.get("createdDate"),
        description=resp.get("description"),
    )


async def get_documentation_versions(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetDocumentationVersionsResult:
    """Get documentation versions.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetDocumentationVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get documentation versions") from exc
    return GetDocumentationVersionsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_domain_name(
    domain_name: str,
    *,
    domain_name_id: str | None = None,
    region_name: str | None = None,
) -> GetDomainNameResult:
    """Get domain name.

    Args:
        domain_name: Domain name.
        domain_name_id: Domain name id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    try:
        resp = await client.call("GetDomainName", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain name") from exc
    return GetDomainNameResult(
        domain_name=resp.get("domainName"),
        domain_name_id=resp.get("domainNameId"),
        domain_name_arn=resp.get("domainNameArn"),
        certificate_name=resp.get("certificateName"),
        certificate_arn=resp.get("certificateArn"),
        certificate_upload_date=resp.get("certificateUploadDate"),
        regional_domain_name=resp.get("regionalDomainName"),
        regional_hosted_zone_id=resp.get("regionalHostedZoneId"),
        regional_certificate_name=resp.get("regionalCertificateName"),
        regional_certificate_arn=resp.get("regionalCertificateArn"),
        distribution_domain_name=resp.get("distributionDomainName"),
        distribution_hosted_zone_id=resp.get("distributionHostedZoneId"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        domain_name_status=resp.get("domainNameStatus"),
        domain_name_status_message=resp.get("domainNameStatusMessage"),
        security_policy=resp.get("securityPolicy"),
        tags=resp.get("tags"),
        mutual_tls_authentication=resp.get("mutualTlsAuthentication"),
        ownership_verification_certificate_arn=resp.get("ownershipVerificationCertificateArn"),
        management_policy=resp.get("managementPolicy"),
        policy=resp.get("policy"),
        routing_mode=resp.get("routingMode"),
    )


async def get_domain_name_access_associations(
    *,
    position: str | None = None,
    limit: int | None = None,
    resource_owner: str | None = None,
    region_name: str | None = None,
) -> GetDomainNameAccessAssociationsResult:
    """Get domain name access associations.

    Args:
        position: Position.
        limit: Limit.
        resource_owner: Resource owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if resource_owner is not None:
        kwargs["resourceOwner"] = resource_owner
    try:
        resp = await client.call("GetDomainNameAccessAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain name access associations") from exc
    return GetDomainNameAccessAssociationsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_domain_names(
    *,
    position: str | None = None,
    limit: int | None = None,
    resource_owner: str | None = None,
    region_name: str | None = None,
) -> GetDomainNamesResult:
    """Get domain names.

    Args:
        position: Position.
        limit: Limit.
        resource_owner: Resource owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if resource_owner is not None:
        kwargs["resourceOwner"] = resource_owner
    try:
        resp = await client.call("GetDomainNames", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get domain names") from exc
    return GetDomainNamesResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_export(
    rest_api_id: str,
    stage_name: str,
    export_type: str,
    *,
    parameters: dict[str, Any] | None = None,
    accepts: str | None = None,
    region_name: str | None = None,
) -> GetExportResult:
    """Get export.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        export_type: Export type.
        parameters: Parameters.
        accepts: Accepts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    kwargs["exportType"] = export_type
    if parameters is not None:
        kwargs["parameters"] = parameters
    if accepts is not None:
        kwargs["accepts"] = accepts
    try:
        resp = await client.call("GetExport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get export") from exc
    return GetExportResult(
        content_type=resp.get("contentType"),
        content_disposition=resp.get("contentDisposition"),
        body=resp.get("body"),
    )


async def get_gateway_response(
    rest_api_id: str,
    response_type: str,
    *,
    region_name: str | None = None,
) -> GetGatewayResponseResult:
    """Get gateway response.

    Args:
        rest_api_id: Rest api id.
        response_type: Response type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["responseType"] = response_type
    try:
        resp = await client.call("GetGatewayResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get gateway response") from exc
    return GetGatewayResponseResult(
        response_type=resp.get("responseType"),
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        default_response=resp.get("defaultResponse"),
    )


async def get_gateway_responses(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetGatewayResponsesResult:
    """Get gateway responses.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetGatewayResponses", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get gateway responses") from exc
    return GetGatewayResponsesResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_integration(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    region_name: str | None = None,
) -> GetIntegrationResult:
    """Get integration.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    try:
        resp = await client.call("GetIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get integration") from exc
    return GetIntegrationResult(
        type=resp.get("type"),
        http_method=resp.get("httpMethod"),
        uri=resp.get("uri"),
        connection_type=resp.get("connectionType"),
        connection_id=resp.get("connectionId"),
        credentials=resp.get("credentials"),
        request_parameters=resp.get("requestParameters"),
        request_templates=resp.get("requestTemplates"),
        passthrough_behavior=resp.get("passthroughBehavior"),
        content_handling=resp.get("contentHandling"),
        timeout_in_millis=resp.get("timeoutInMillis"),
        cache_namespace=resp.get("cacheNamespace"),
        cache_key_parameters=resp.get("cacheKeyParameters"),
        integration_responses=resp.get("integrationResponses"),
        tls_config=resp.get("tlsConfig"),
    )


async def get_integration_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    region_name: str | None = None,
) -> GetIntegrationResponseResult:
    """Get integration response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    try:
        resp = await client.call("GetIntegrationResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get integration response") from exc
    return GetIntegrationResponseResult(
        status_code=resp.get("statusCode"),
        selection_pattern=resp.get("selectionPattern"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        content_handling=resp.get("contentHandling"),
    )


async def get_method(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    region_name: str | None = None,
) -> GetMethodResult:
    """Get method.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    try:
        resp = await client.call("GetMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get method") from exc
    return GetMethodResult(
        http_method=resp.get("httpMethod"),
        authorization_type=resp.get("authorizationType"),
        authorizer_id=resp.get("authorizerId"),
        api_key_required=resp.get("apiKeyRequired"),
        request_validator_id=resp.get("requestValidatorId"),
        operation_name=resp.get("operationName"),
        request_parameters=resp.get("requestParameters"),
        request_models=resp.get("requestModels"),
        method_responses=resp.get("methodResponses"),
        method_integration=resp.get("methodIntegration"),
        authorization_scopes=resp.get("authorizationScopes"),
    )


async def get_method_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    region_name: str | None = None,
) -> GetMethodResponseResult:
    """Get method response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    try:
        resp = await client.call("GetMethodResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get method response") from exc
    return GetMethodResponseResult(
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_models=resp.get("responseModels"),
    )


async def get_model(
    rest_api_id: str,
    model_name: str,
    *,
    flatten: bool | None = None,
    region_name: str | None = None,
) -> GetModelResult:
    """Get model.

    Args:
        rest_api_id: Rest api id.
        model_name: Model name.
        flatten: Flatten.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["modelName"] = model_name
    if flatten is not None:
        kwargs["flatten"] = flatten
    try:
        resp = await client.call("GetModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get model") from exc
    return GetModelResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        model_schema=resp.get("schema"),
        content_type=resp.get("contentType"),
    )


async def get_model_template(
    rest_api_id: str,
    model_name: str,
    *,
    region_name: str | None = None,
) -> GetModelTemplateResult:
    """Get model template.

    Args:
        rest_api_id: Rest api id.
        model_name: Model name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["modelName"] = model_name
    try:
        resp = await client.call("GetModelTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get model template") from exc
    return GetModelTemplateResult(
        value=resp.get("value"),
    )


async def get_models(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetModelsResult:
    """Get models.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetModels", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get models") from exc
    return GetModelsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_request_validator(
    rest_api_id: str,
    request_validator_id: str,
    *,
    region_name: str | None = None,
) -> GetRequestValidatorResult:
    """Get request validator.

    Args:
        rest_api_id: Rest api id.
        request_validator_id: Request validator id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["requestValidatorId"] = request_validator_id
    try:
        resp = await client.call("GetRequestValidator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get request validator") from exc
    return GetRequestValidatorResult(
        id=resp.get("id"),
        name=resp.get("name"),
        validate_request_body=resp.get("validateRequestBody"),
        validate_request_parameters=resp.get("validateRequestParameters"),
    )


async def get_request_validators(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetRequestValidatorsResult:
    """Get request validators.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetRequestValidators", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get request validators") from exc
    return GetRequestValidatorsResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_resource(
    rest_api_id: str,
    resource_id: str,
    *,
    embed: list[Any] | None = None,
    region_name: str | None = None,
) -> GetResourceResult:
    """Get resource.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        embed: Embed.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    if embed is not None:
        kwargs["embed"] = embed
    try:
        resp = await client.call("GetResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource") from exc
    return GetResourceResult(
        id=resp.get("id"),
        parent_id=resp.get("parentId"),
        path_part=resp.get("pathPart"),
        path=resp.get("path"),
        resource_methods=resp.get("resourceMethods"),
    )


async def get_resources(
    rest_api_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    embed: list[Any] | None = None,
    region_name: str | None = None,
) -> GetResourcesResult:
    """Get resources.

    Args:
        rest_api_id: Rest api id.
        position: Position.
        limit: Limit.
        embed: Embed.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if embed is not None:
        kwargs["embed"] = embed
    try:
        resp = await client.call("GetResources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resources") from exc
    return GetResourcesResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_rest_api(
    rest_api_id: str,
    *,
    region_name: str | None = None,
) -> GetRestApiResult:
    """Get rest api.

    Args:
        rest_api_id: Rest api id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    try:
        resp = await client.call("GetRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get rest api") from exc
    return GetRestApiResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        version=resp.get("version"),
        warnings=resp.get("warnings"),
        binary_media_types=resp.get("binaryMediaTypes"),
        minimum_compression_size=resp.get("minimumCompressionSize"),
        api_key_source=resp.get("apiKeySource"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        policy=resp.get("policy"),
        tags=resp.get("tags"),
        disable_execute_api_endpoint=resp.get("disableExecuteApiEndpoint"),
        root_resource_id=resp.get("rootResourceId"),
    )


async def get_rest_apis(
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetRestApisResult:
    """Get rest apis.

    Args:
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetRestApis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get rest apis") from exc
    return GetRestApisResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_sdk(
    rest_api_id: str,
    stage_name: str,
    sdk_type: str,
    *,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetSdkResult:
    """Get sdk.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        sdk_type: Sdk type.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    kwargs["sdkType"] = sdk_type
    if parameters is not None:
        kwargs["parameters"] = parameters
    try:
        resp = await client.call("GetSdk", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sdk") from exc
    return GetSdkResult(
        content_type=resp.get("contentType"),
        content_disposition=resp.get("contentDisposition"),
        body=resp.get("body"),
    )


async def get_sdk_type(
    id: str,
    *,
    region_name: str | None = None,
) -> GetSdkTypeResult:
    """Get sdk type.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("GetSdkType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sdk type") from exc
    return GetSdkTypeResult(
        id=resp.get("id"),
        friendly_name=resp.get("friendlyName"),
        description=resp.get("description"),
        configuration_properties=resp.get("configurationProperties"),
    )


async def get_sdk_types(
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetSdkTypesResult:
    """Get sdk types.

    Args:
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetSdkTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get sdk types") from exc
    return GetSdkTypesResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_stage(
    rest_api_id: str,
    stage_name: str,
    *,
    region_name: str | None = None,
) -> GetStageResult:
    """Get stage.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    try:
        resp = await client.call("GetStage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get stage") from exc
    return GetStageResult(
        deployment_id=resp.get("deploymentId"),
        client_certificate_id=resp.get("clientCertificateId"),
        stage_name=resp.get("stageName"),
        description=resp.get("description"),
        cache_cluster_enabled=resp.get("cacheClusterEnabled"),
        cache_cluster_size=resp.get("cacheClusterSize"),
        cache_cluster_status=resp.get("cacheClusterStatus"),
        method_settings=resp.get("methodSettings"),
        variables=resp.get("variables"),
        documentation_version=resp.get("documentationVersion"),
        access_log_settings=resp.get("accessLogSettings"),
        canary_settings=resp.get("canarySettings"),
        tracing_enabled=resp.get("tracingEnabled"),
        web_acl_arn=resp.get("webAclArn"),
        tags=resp.get("tags"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
    )


async def get_stages(
    rest_api_id: str,
    *,
    deployment_id: str | None = None,
    region_name: str | None = None,
) -> GetStagesResult:
    """Get stages.

    Args:
        rest_api_id: Rest api id.
        deployment_id: Deployment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if deployment_id is not None:
        kwargs["deploymentId"] = deployment_id
    try:
        resp = await client.call("GetStages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get stages") from exc
    return GetStagesResult(
        item=resp.get("item"),
    )


async def get_tags(
    resource_arn: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetTagsResult:
    """Get tags.

    Args:
        resource_arn: Resource arn.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get tags") from exc
    return GetTagsResult(
        tags=resp.get("tags"),
    )


async def get_usage(
    usage_plan_id: str,
    start_date: str,
    end_date: str,
    *,
    key_id: str | None = None,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetUsageResult:
    """Get usage.

    Args:
        usage_plan_id: Usage plan id.
        start_date: Start date.
        end_date: End date.
        key_id: Key id.
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    kwargs["startDate"] = start_date
    kwargs["endDate"] = end_date
    if key_id is not None:
        kwargs["keyId"] = key_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetUsage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage") from exc
    return GetUsageResult(
        usage_plan_id=resp.get("usagePlanId"),
        start_date=resp.get("startDate"),
        end_date=resp.get("endDate"),
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_usage_plan(
    usage_plan_id: str,
    *,
    region_name: str | None = None,
) -> GetUsagePlanResult:
    """Get usage plan.

    Args:
        usage_plan_id: Usage plan id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    try:
        resp = await client.call("GetUsagePlan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage plan") from exc
    return GetUsagePlanResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        api_stages=resp.get("apiStages"),
        throttle=resp.get("throttle"),
        quota=resp.get("quota"),
        product_code=resp.get("productCode"),
        tags=resp.get("tags"),
    )


async def get_usage_plan_key(
    usage_plan_id: str,
    key_id: str,
    *,
    region_name: str | None = None,
) -> GetUsagePlanKeyResult:
    """Get usage plan key.

    Args:
        usage_plan_id: Usage plan id.
        key_id: Key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    kwargs["keyId"] = key_id
    try:
        resp = await client.call("GetUsagePlanKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage plan key") from exc
    return GetUsagePlanKeyResult(
        id=resp.get("id"),
        type=resp.get("type"),
        value=resp.get("value"),
        name=resp.get("name"),
    )


async def get_usage_plan_keys(
    usage_plan_id: str,
    *,
    position: str | None = None,
    limit: int | None = None,
    name_query: str | None = None,
    region_name: str | None = None,
) -> GetUsagePlanKeysResult:
    """Get usage plan keys.

    Args:
        usage_plan_id: Usage plan id.
        position: Position.
        limit: Limit.
        name_query: Name query.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    if name_query is not None:
        kwargs["nameQuery"] = name_query
    try:
        resp = await client.call("GetUsagePlanKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage plan keys") from exc
    return GetUsagePlanKeysResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_usage_plans(
    *,
    position: str | None = None,
    key_id: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetUsagePlansResult:
    """Get usage plans.

    Args:
        position: Position.
        key_id: Key id.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if key_id is not None:
        kwargs["keyId"] = key_id
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetUsagePlans", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage plans") from exc
    return GetUsagePlansResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def get_vpc_link(
    vpc_link_id: str,
    *,
    region_name: str | None = None,
) -> GetVpcLinkResult:
    """Get vpc link.

    Args:
        vpc_link_id: Vpc link id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["vpcLinkId"] = vpc_link_id
    try:
        resp = await client.call("GetVpcLink", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get vpc link") from exc
    return GetVpcLinkResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        target_arns=resp.get("targetArns"),
        status=resp.get("status"),
        status_message=resp.get("statusMessage"),
        tags=resp.get("tags"),
    )


async def get_vpc_links(
    *,
    position: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> GetVpcLinksResult:
    """Get vpc links.

    Args:
        position: Position.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if position is not None:
        kwargs["position"] = position
    if limit is not None:
        kwargs["limit"] = limit
    try:
        resp = await client.call("GetVpcLinks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get vpc links") from exc
    return GetVpcLinksResult(
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def import_api_keys(
    body: Any,
    format: str,
    *,
    fail_on_warnings: bool | None = None,
    region_name: str | None = None,
) -> ImportApiKeysResult:
    """Import api keys.

    Args:
        body: Body.
        format: Format.
        fail_on_warnings: Fail on warnings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["body"] = body
    kwargs["format"] = format
    if fail_on_warnings is not None:
        kwargs["failOnWarnings"] = fail_on_warnings
    try:
        resp = await client.call("ImportApiKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import api keys") from exc
    return ImportApiKeysResult(
        ids=resp.get("ids"),
        warnings=resp.get("warnings"),
    )


async def import_documentation_parts(
    rest_api_id: str,
    body: Any,
    *,
    mode: str | None = None,
    fail_on_warnings: bool | None = None,
    region_name: str | None = None,
) -> ImportDocumentationPartsResult:
    """Import documentation parts.

    Args:
        rest_api_id: Rest api id.
        body: Body.
        mode: Mode.
        fail_on_warnings: Fail on warnings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["body"] = body
    if mode is not None:
        kwargs["mode"] = mode
    if fail_on_warnings is not None:
        kwargs["failOnWarnings"] = fail_on_warnings
    try:
        resp = await client.call("ImportDocumentationParts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import documentation parts") from exc
    return ImportDocumentationPartsResult(
        ids=resp.get("ids"),
        warnings=resp.get("warnings"),
    )


async def import_rest_api(
    body: Any,
    *,
    fail_on_warnings: bool | None = None,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ImportRestApiResult:
    """Import rest api.

    Args:
        body: Body.
        fail_on_warnings: Fail on warnings.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["body"] = body
    if fail_on_warnings is not None:
        kwargs["failOnWarnings"] = fail_on_warnings
    if parameters is not None:
        kwargs["parameters"] = parameters
    try:
        resp = await client.call("ImportRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import rest api") from exc
    return ImportRestApiResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        version=resp.get("version"),
        warnings=resp.get("warnings"),
        binary_media_types=resp.get("binaryMediaTypes"),
        minimum_compression_size=resp.get("minimumCompressionSize"),
        api_key_source=resp.get("apiKeySource"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        policy=resp.get("policy"),
        tags=resp.get("tags"),
        disable_execute_api_endpoint=resp.get("disableExecuteApiEndpoint"),
        root_resource_id=resp.get("rootResourceId"),
    )


async def put_gateway_response(
    rest_api_id: str,
    response_type: str,
    *,
    status_code: str | None = None,
    response_parameters: dict[str, Any] | None = None,
    response_templates: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutGatewayResponseResult:
    """Put gateway response.

    Args:
        rest_api_id: Rest api id.
        response_type: Response type.
        status_code: Status code.
        response_parameters: Response parameters.
        response_templates: Response templates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["responseType"] = response_type
    if status_code is not None:
        kwargs["statusCode"] = status_code
    if response_parameters is not None:
        kwargs["responseParameters"] = response_parameters
    if response_templates is not None:
        kwargs["responseTemplates"] = response_templates
    try:
        resp = await client.call("PutGatewayResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put gateway response") from exc
    return PutGatewayResponseResult(
        response_type=resp.get("responseType"),
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        default_response=resp.get("defaultResponse"),
    )


async def put_integration(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    type: str,
    *,
    integration_http_method: str | None = None,
    uri: str | None = None,
    connection_type: str | None = None,
    connection_id: str | None = None,
    credentials: str | None = None,
    request_parameters: dict[str, Any] | None = None,
    request_templates: dict[str, Any] | None = None,
    passthrough_behavior: str | None = None,
    cache_namespace: str | None = None,
    cache_key_parameters: list[Any] | None = None,
    content_handling: str | None = None,
    timeout_in_millis: int | None = None,
    tls_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutIntegrationResult:
    """Put integration.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        type: Type.
        integration_http_method: Integration http method.
        uri: Uri.
        connection_type: Connection type.
        connection_id: Connection id.
        credentials: Credentials.
        request_parameters: Request parameters.
        request_templates: Request templates.
        passthrough_behavior: Passthrough behavior.
        cache_namespace: Cache namespace.
        cache_key_parameters: Cache key parameters.
        content_handling: Content handling.
        timeout_in_millis: Timeout in millis.
        tls_config: Tls config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["type"] = type
    if integration_http_method is not None:
        kwargs["integrationHttpMethod"] = integration_http_method
    if uri is not None:
        kwargs["uri"] = uri
    if connection_type is not None:
        kwargs["connectionType"] = connection_type
    if connection_id is not None:
        kwargs["connectionId"] = connection_id
    if credentials is not None:
        kwargs["credentials"] = credentials
    if request_parameters is not None:
        kwargs["requestParameters"] = request_parameters
    if request_templates is not None:
        kwargs["requestTemplates"] = request_templates
    if passthrough_behavior is not None:
        kwargs["passthroughBehavior"] = passthrough_behavior
    if cache_namespace is not None:
        kwargs["cacheNamespace"] = cache_namespace
    if cache_key_parameters is not None:
        kwargs["cacheKeyParameters"] = cache_key_parameters
    if content_handling is not None:
        kwargs["contentHandling"] = content_handling
    if timeout_in_millis is not None:
        kwargs["timeoutInMillis"] = timeout_in_millis
    if tls_config is not None:
        kwargs["tlsConfig"] = tls_config
    try:
        resp = await client.call("PutIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put integration") from exc
    return PutIntegrationResult(
        type=resp.get("type"),
        http_method=resp.get("httpMethod"),
        uri=resp.get("uri"),
        connection_type=resp.get("connectionType"),
        connection_id=resp.get("connectionId"),
        credentials=resp.get("credentials"),
        request_parameters=resp.get("requestParameters"),
        request_templates=resp.get("requestTemplates"),
        passthrough_behavior=resp.get("passthroughBehavior"),
        content_handling=resp.get("contentHandling"),
        timeout_in_millis=resp.get("timeoutInMillis"),
        cache_namespace=resp.get("cacheNamespace"),
        cache_key_parameters=resp.get("cacheKeyParameters"),
        integration_responses=resp.get("integrationResponses"),
        tls_config=resp.get("tlsConfig"),
    )


async def put_integration_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    selection_pattern: str | None = None,
    response_parameters: dict[str, Any] | None = None,
    response_templates: dict[str, Any] | None = None,
    content_handling: str | None = None,
    region_name: str | None = None,
) -> PutIntegrationResponseResult:
    """Put integration response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        selection_pattern: Selection pattern.
        response_parameters: Response parameters.
        response_templates: Response templates.
        content_handling: Content handling.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    if selection_pattern is not None:
        kwargs["selectionPattern"] = selection_pattern
    if response_parameters is not None:
        kwargs["responseParameters"] = response_parameters
    if response_templates is not None:
        kwargs["responseTemplates"] = response_templates
    if content_handling is not None:
        kwargs["contentHandling"] = content_handling
    try:
        resp = await client.call("PutIntegrationResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put integration response") from exc
    return PutIntegrationResponseResult(
        status_code=resp.get("statusCode"),
        selection_pattern=resp.get("selectionPattern"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        content_handling=resp.get("contentHandling"),
    )


async def put_method(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    authorization_type: str,
    *,
    authorizer_id: str | None = None,
    api_key_required: bool | None = None,
    operation_name: str | None = None,
    request_parameters: dict[str, Any] | None = None,
    request_models: dict[str, Any] | None = None,
    request_validator_id: str | None = None,
    authorization_scopes: list[Any] | None = None,
    region_name: str | None = None,
) -> PutMethodResult:
    """Put method.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        authorization_type: Authorization type.
        authorizer_id: Authorizer id.
        api_key_required: Api key required.
        operation_name: Operation name.
        request_parameters: Request parameters.
        request_models: Request models.
        request_validator_id: Request validator id.
        authorization_scopes: Authorization scopes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["authorizationType"] = authorization_type
    if authorizer_id is not None:
        kwargs["authorizerId"] = authorizer_id
    if api_key_required is not None:
        kwargs["apiKeyRequired"] = api_key_required
    if operation_name is not None:
        kwargs["operationName"] = operation_name
    if request_parameters is not None:
        kwargs["requestParameters"] = request_parameters
    if request_models is not None:
        kwargs["requestModels"] = request_models
    if request_validator_id is not None:
        kwargs["requestValidatorId"] = request_validator_id
    if authorization_scopes is not None:
        kwargs["authorizationScopes"] = authorization_scopes
    try:
        resp = await client.call("PutMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put method") from exc
    return PutMethodResult(
        http_method=resp.get("httpMethod"),
        authorization_type=resp.get("authorizationType"),
        authorizer_id=resp.get("authorizerId"),
        api_key_required=resp.get("apiKeyRequired"),
        request_validator_id=resp.get("requestValidatorId"),
        operation_name=resp.get("operationName"),
        request_parameters=resp.get("requestParameters"),
        request_models=resp.get("requestModels"),
        method_responses=resp.get("methodResponses"),
        method_integration=resp.get("methodIntegration"),
        authorization_scopes=resp.get("authorizationScopes"),
    )


async def put_method_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    response_parameters: dict[str, Any] | None = None,
    response_models: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutMethodResponseResult:
    """Put method response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        response_parameters: Response parameters.
        response_models: Response models.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    if response_parameters is not None:
        kwargs["responseParameters"] = response_parameters
    if response_models is not None:
        kwargs["responseModels"] = response_models
    try:
        resp = await client.call("PutMethodResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put method response") from exc
    return PutMethodResponseResult(
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_models=resp.get("responseModels"),
    )


async def put_rest_api(
    rest_api_id: str,
    body: Any,
    *,
    mode: str | None = None,
    fail_on_warnings: bool | None = None,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutRestApiResult:
    """Put rest api.

    Args:
        rest_api_id: Rest api id.
        body: Body.
        mode: Mode.
        fail_on_warnings: Fail on warnings.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["body"] = body
    if mode is not None:
        kwargs["mode"] = mode
    if fail_on_warnings is not None:
        kwargs["failOnWarnings"] = fail_on_warnings
    if parameters is not None:
        kwargs["parameters"] = parameters
    try:
        resp = await client.call("PutRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put rest api") from exc
    return PutRestApiResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        version=resp.get("version"),
        warnings=resp.get("warnings"),
        binary_media_types=resp.get("binaryMediaTypes"),
        minimum_compression_size=resp.get("minimumCompressionSize"),
        api_key_source=resp.get("apiKeySource"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        policy=resp.get("policy"),
        tags=resp.get("tags"),
        disable_execute_api_endpoint=resp.get("disableExecuteApiEndpoint"),
        root_resource_id=resp.get("rootResourceId"),
    )


async def reject_domain_name_access_association(
    domain_name_access_association_arn: str,
    domain_name_arn: str,
    *,
    region_name: str | None = None,
) -> RejectDomainNameAccessAssociationResult:
    """Reject domain name access association.

    Args:
        domain_name_access_association_arn: Domain name access association arn.
        domain_name_arn: Domain name arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainNameAccessAssociationArn"] = domain_name_access_association_arn
    kwargs["domainNameArn"] = domain_name_arn
    try:
        await client.call("RejectDomainNameAccessAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reject domain name access association") from exc
    return RejectDomainNameAccessAssociationResult()


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    *,
    region_name: str | None = None,
) -> TagResourceResult:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return TagResourceResult()


async def run_invoke_authorizer(
    rest_api_id: str,
    authorizer_id: str,
    *,
    headers: dict[str, Any] | None = None,
    multi_value_headers: dict[str, Any] | None = None,
    path_with_query_string: str | None = None,
    body: str | None = None,
    stage_variables: dict[str, Any] | None = None,
    additional_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RunInvokeAuthorizerResult:
    """Test invoke authorizer.

    Args:
        rest_api_id: Rest api id.
        authorizer_id: Authorizer id.
        headers: Headers.
        multi_value_headers: Multi value headers.
        path_with_query_string: Path with query string.
        body: Body.
        stage_variables: Stage variables.
        additional_context: Additional context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["authorizerId"] = authorizer_id
    if headers is not None:
        kwargs["headers"] = headers
    if multi_value_headers is not None:
        kwargs["multiValueHeaders"] = multi_value_headers
    if path_with_query_string is not None:
        kwargs["pathWithQueryString"] = path_with_query_string
    if body is not None:
        kwargs["body"] = body
    if stage_variables is not None:
        kwargs["stageVariables"] = stage_variables
    if additional_context is not None:
        kwargs["additionalContext"] = additional_context
    try:
        resp = await client.call("TestInvokeAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to test invoke authorizer") from exc
    return RunInvokeAuthorizerResult(
        client_status=resp.get("clientStatus"),
        log=resp.get("log"),
        latency=resp.get("latency"),
        principal_id=resp.get("principalId"),
        policy=resp.get("policy"),
        authorization=resp.get("authorization"),
        claims=resp.get("claims"),
    )


async def run_invoke_method(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    path_with_query_string: str | None = None,
    body: str | None = None,
    headers: dict[str, Any] | None = None,
    multi_value_headers: dict[str, Any] | None = None,
    client_certificate_id: str | None = None,
    stage_variables: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RunInvokeMethodResult:
    """Test invoke method.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        path_with_query_string: Path with query string.
        body: Body.
        headers: Headers.
        multi_value_headers: Multi value headers.
        client_certificate_id: Client certificate id.
        stage_variables: Stage variables.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    if path_with_query_string is not None:
        kwargs["pathWithQueryString"] = path_with_query_string
    if body is not None:
        kwargs["body"] = body
    if headers is not None:
        kwargs["headers"] = headers
    if multi_value_headers is not None:
        kwargs["multiValueHeaders"] = multi_value_headers
    if client_certificate_id is not None:
        kwargs["clientCertificateId"] = client_certificate_id
    if stage_variables is not None:
        kwargs["stageVariables"] = stage_variables
    try:
        resp = await client.call("TestInvokeMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to test invoke method") from exc
    return RunInvokeMethodResult(
        status=resp.get("status"),
        body=resp.get("body"),
        headers=resp.get("headers"),
        multi_value_headers=resp.get("multiValueHeaders"),
        log=resp.get("log"),
        latency=resp.get("latency"),
    )


async def untag_resource(
    resource_arn: str,
    tag_keys: list[Any],
    *,
    region_name: str | None = None,
) -> UntagResourceResult:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return UntagResourceResult()


async def update_account(
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateAccountResult:
    """Update account.

    Args:
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account") from exc
    return UpdateAccountResult(
        cloudwatch_role_arn=resp.get("cloudwatchRoleArn"),
        throttle_settings=resp.get("throttleSettings"),
        features=resp.get("features"),
        api_key_version=resp.get("apiKeyVersion"),
    )


async def update_api_key(
    api_key: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateApiKeyResult:
    """Update api key.

    Args:
        api_key: Api key.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["apiKey"] = api_key
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateApiKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update api key") from exc
    return UpdateApiKeyResult(
        id=resp.get("id"),
        value=resp.get("value"),
        name=resp.get("name"),
        customer_id=resp.get("customerId"),
        description=resp.get("description"),
        enabled=resp.get("enabled"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
        stage_keys=resp.get("stageKeys"),
        tags=resp.get("tags"),
    )


async def update_authorizer(
    rest_api_id: str,
    authorizer_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateAuthorizerResult:
    """Update authorizer.

    Args:
        rest_api_id: Rest api id.
        authorizer_id: Authorizer id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["authorizerId"] = authorizer_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update authorizer") from exc
    return UpdateAuthorizerResult(
        id=resp.get("id"),
        name=resp.get("name"),
        type=resp.get("type"),
        provider_ar_ns=resp.get("providerARNs"),
        auth_type=resp.get("authType"),
        authorizer_uri=resp.get("authorizerUri"),
        authorizer_credentials=resp.get("authorizerCredentials"),
        identity_source=resp.get("identitySource"),
        identity_validation_expression=resp.get("identityValidationExpression"),
        authorizer_result_ttl_in_seconds=resp.get("authorizerResultTtlInSeconds"),
    )


async def update_base_path_mapping(
    domain_name: str,
    base_path: str,
    *,
    domain_name_id: str | None = None,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateBasePathMappingResult:
    """Update base path mapping.

    Args:
        domain_name: Domain name.
        base_path: Base path.
        domain_name_id: Domain name id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    kwargs["basePath"] = base_path
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateBasePathMapping", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update base path mapping") from exc
    return UpdateBasePathMappingResult(
        base_path=resp.get("basePath"),
        rest_api_id=resp.get("restApiId"),
        stage=resp.get("stage"),
    )


async def update_client_certificate(
    client_certificate_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateClientCertificateResult:
    """Update client certificate.

    Args:
        client_certificate_id: Client certificate id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientCertificateId"] = client_certificate_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update client certificate") from exc
    return UpdateClientCertificateResult(
        client_certificate_id=resp.get("clientCertificateId"),
        description=resp.get("description"),
        pem_encoded_certificate=resp.get("pemEncodedCertificate"),
        created_date=resp.get("createdDate"),
        expiration_date=resp.get("expirationDate"),
        tags=resp.get("tags"),
    )


async def update_deployment(
    rest_api_id: str,
    deployment_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateDeploymentResult:
    """Update deployment.

    Args:
        rest_api_id: Rest api id.
        deployment_id: Deployment id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["deploymentId"] = deployment_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update deployment") from exc
    return UpdateDeploymentResult(
        id=resp.get("id"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        api_summary=resp.get("apiSummary"),
    )


async def update_documentation_part(
    rest_api_id: str,
    documentation_part_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateDocumentationPartResult:
    """Update documentation part.

    Args:
        rest_api_id: Rest api id.
        documentation_part_id: Documentation part id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationPartId"] = documentation_part_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateDocumentationPart", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update documentation part") from exc
    return UpdateDocumentationPartResult(
        id=resp.get("id"),
        location=resp.get("location"),
        properties=resp.get("properties"),
    )


async def update_documentation_version(
    rest_api_id: str,
    documentation_version: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateDocumentationVersionResult:
    """Update documentation version.

    Args:
        rest_api_id: Rest api id.
        documentation_version: Documentation version.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["documentationVersion"] = documentation_version
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateDocumentationVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update documentation version") from exc
    return UpdateDocumentationVersionResult(
        version=resp.get("version"),
        created_date=resp.get("createdDate"),
        description=resp.get("description"),
    )


async def update_domain_name(
    domain_name: str,
    *,
    domain_name_id: str | None = None,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateDomainNameResult:
    """Update domain name.

    Args:
        domain_name: Domain name.
        domain_name_id: Domain name id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if domain_name_id is not None:
        kwargs["domainNameId"] = domain_name_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateDomainName", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update domain name") from exc
    return UpdateDomainNameResult(
        domain_name=resp.get("domainName"),
        domain_name_id=resp.get("domainNameId"),
        domain_name_arn=resp.get("domainNameArn"),
        certificate_name=resp.get("certificateName"),
        certificate_arn=resp.get("certificateArn"),
        certificate_upload_date=resp.get("certificateUploadDate"),
        regional_domain_name=resp.get("regionalDomainName"),
        regional_hosted_zone_id=resp.get("regionalHostedZoneId"),
        regional_certificate_name=resp.get("regionalCertificateName"),
        regional_certificate_arn=resp.get("regionalCertificateArn"),
        distribution_domain_name=resp.get("distributionDomainName"),
        distribution_hosted_zone_id=resp.get("distributionHostedZoneId"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        domain_name_status=resp.get("domainNameStatus"),
        domain_name_status_message=resp.get("domainNameStatusMessage"),
        security_policy=resp.get("securityPolicy"),
        tags=resp.get("tags"),
        mutual_tls_authentication=resp.get("mutualTlsAuthentication"),
        ownership_verification_certificate_arn=resp.get("ownershipVerificationCertificateArn"),
        management_policy=resp.get("managementPolicy"),
        policy=resp.get("policy"),
        routing_mode=resp.get("routingMode"),
    )


async def update_gateway_response(
    rest_api_id: str,
    response_type: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateGatewayResponseResult:
    """Update gateway response.

    Args:
        rest_api_id: Rest api id.
        response_type: Response type.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["responseType"] = response_type
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateGatewayResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update gateway response") from exc
    return UpdateGatewayResponseResult(
        response_type=resp.get("responseType"),
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        default_response=resp.get("defaultResponse"),
    )


async def update_integration(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateIntegrationResult:
    """Update integration.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update integration") from exc
    return UpdateIntegrationResult(
        type=resp.get("type"),
        http_method=resp.get("httpMethod"),
        uri=resp.get("uri"),
        connection_type=resp.get("connectionType"),
        connection_id=resp.get("connectionId"),
        credentials=resp.get("credentials"),
        request_parameters=resp.get("requestParameters"),
        request_templates=resp.get("requestTemplates"),
        passthrough_behavior=resp.get("passthroughBehavior"),
        content_handling=resp.get("contentHandling"),
        timeout_in_millis=resp.get("timeoutInMillis"),
        cache_namespace=resp.get("cacheNamespace"),
        cache_key_parameters=resp.get("cacheKeyParameters"),
        integration_responses=resp.get("integrationResponses"),
        tls_config=resp.get("tlsConfig"),
    )


async def update_integration_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateIntegrationResponseResult:
    """Update integration response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateIntegrationResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update integration response") from exc
    return UpdateIntegrationResponseResult(
        status_code=resp.get("statusCode"),
        selection_pattern=resp.get("selectionPattern"),
        response_parameters=resp.get("responseParameters"),
        response_templates=resp.get("responseTemplates"),
        content_handling=resp.get("contentHandling"),
    )


async def update_method(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateMethodResult:
    """Update method.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update method") from exc
    return UpdateMethodResult(
        http_method=resp.get("httpMethod"),
        authorization_type=resp.get("authorizationType"),
        authorizer_id=resp.get("authorizerId"),
        api_key_required=resp.get("apiKeyRequired"),
        request_validator_id=resp.get("requestValidatorId"),
        operation_name=resp.get("operationName"),
        request_parameters=resp.get("requestParameters"),
        request_models=resp.get("requestModels"),
        method_responses=resp.get("methodResponses"),
        method_integration=resp.get("methodIntegration"),
        authorization_scopes=resp.get("authorizationScopes"),
    )


async def update_method_response(
    rest_api_id: str,
    resource_id: str,
    http_method: str,
    status_code: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateMethodResponseResult:
    """Update method response.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        http_method: Http method.
        status_code: Status code.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    kwargs["httpMethod"] = http_method
    kwargs["statusCode"] = status_code
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateMethodResponse", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update method response") from exc
    return UpdateMethodResponseResult(
        status_code=resp.get("statusCode"),
        response_parameters=resp.get("responseParameters"),
        response_models=resp.get("responseModels"),
    )


async def update_model(
    rest_api_id: str,
    model_name: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateModelResult:
    """Update model.

    Args:
        rest_api_id: Rest api id.
        model_name: Model name.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["modelName"] = model_name
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update model") from exc
    return UpdateModelResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        model_schema=resp.get("schema"),
        content_type=resp.get("contentType"),
    )


async def update_request_validator(
    rest_api_id: str,
    request_validator_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateRequestValidatorResult:
    """Update request validator.

    Args:
        rest_api_id: Rest api id.
        request_validator_id: Request validator id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["requestValidatorId"] = request_validator_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateRequestValidator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update request validator") from exc
    return UpdateRequestValidatorResult(
        id=resp.get("id"),
        name=resp.get("name"),
        validate_request_body=resp.get("validateRequestBody"),
        validate_request_parameters=resp.get("validateRequestParameters"),
    )


async def update_resource(
    rest_api_id: str,
    resource_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateResourceResult:
    """Update resource.

    Args:
        rest_api_id: Rest api id.
        resource_id: Resource id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["resourceId"] = resource_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update resource") from exc
    return UpdateResourceResult(
        id=resp.get("id"),
        parent_id=resp.get("parentId"),
        path_part=resp.get("pathPart"),
        path=resp.get("path"),
        resource_methods=resp.get("resourceMethods"),
    )


async def update_rest_api(
    rest_api_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateRestApiResult:
    """Update rest api.

    Args:
        rest_api_id: Rest api id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateRestApi", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update rest api") from exc
    return UpdateRestApiResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        created_date=resp.get("createdDate"),
        version=resp.get("version"),
        warnings=resp.get("warnings"),
        binary_media_types=resp.get("binaryMediaTypes"),
        minimum_compression_size=resp.get("minimumCompressionSize"),
        api_key_source=resp.get("apiKeySource"),
        endpoint_configuration=resp.get("endpointConfiguration"),
        policy=resp.get("policy"),
        tags=resp.get("tags"),
        disable_execute_api_endpoint=resp.get("disableExecuteApiEndpoint"),
        root_resource_id=resp.get("rootResourceId"),
    )


async def update_stage(
    rest_api_id: str,
    stage_name: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateStageResult:
    """Update stage.

    Args:
        rest_api_id: Rest api id.
        stage_name: Stage name.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["restApiId"] = rest_api_id
    kwargs["stageName"] = stage_name
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateStage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update stage") from exc
    return UpdateStageResult(
        deployment_id=resp.get("deploymentId"),
        client_certificate_id=resp.get("clientCertificateId"),
        stage_name=resp.get("stageName"),
        description=resp.get("description"),
        cache_cluster_enabled=resp.get("cacheClusterEnabled"),
        cache_cluster_size=resp.get("cacheClusterSize"),
        cache_cluster_status=resp.get("cacheClusterStatus"),
        method_settings=resp.get("methodSettings"),
        variables=resp.get("variables"),
        documentation_version=resp.get("documentationVersion"),
        access_log_settings=resp.get("accessLogSettings"),
        canary_settings=resp.get("canarySettings"),
        tracing_enabled=resp.get("tracingEnabled"),
        web_acl_arn=resp.get("webAclArn"),
        tags=resp.get("tags"),
        created_date=resp.get("createdDate"),
        last_updated_date=resp.get("lastUpdatedDate"),
    )


async def update_usage(
    usage_plan_id: str,
    key_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateUsageResult:
    """Update usage.

    Args:
        usage_plan_id: Usage plan id.
        key_id: Key id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    kwargs["keyId"] = key_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateUsage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update usage") from exc
    return UpdateUsageResult(
        usage_plan_id=resp.get("usagePlanId"),
        start_date=resp.get("startDate"),
        end_date=resp.get("endDate"),
        position=resp.get("position"),
        items=resp.get("items"),
    )


async def update_usage_plan(
    usage_plan_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateUsagePlanResult:
    """Update usage plan.

    Args:
        usage_plan_id: Usage plan id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usagePlanId"] = usage_plan_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateUsagePlan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update usage plan") from exc
    return UpdateUsagePlanResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        api_stages=resp.get("apiStages"),
        throttle=resp.get("throttle"),
        quota=resp.get("quota"),
        product_code=resp.get("productCode"),
        tags=resp.get("tags"),
    )


async def update_vpc_link(
    vpc_link_id: str,
    *,
    patch_operations: list[Any] | None = None,
    region_name: str | None = None,
) -> UpdateVpcLinkResult:
    """Update vpc link.

    Args:
        vpc_link_id: Vpc link id.
        patch_operations: Patch operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("apigateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["vpcLinkId"] = vpc_link_id
    if patch_operations is not None:
        kwargs["patchOperations"] = patch_operations
    try:
        resp = await client.call("UpdateVpcLink", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update vpc link") from exc
    return UpdateVpcLinkResult(
        id=resp.get("id"),
        name=resp.get("name"),
        description=resp.get("description"),
        target_arns=resp.get("targetArns"),
        status=resp.get("status"),
        status_message=resp.get("statusMessage"),
        tags=resp.get("tags"),
    )
