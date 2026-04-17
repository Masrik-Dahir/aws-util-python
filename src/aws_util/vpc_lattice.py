"""aws_util.vpc_lattice -- Amazon VPC Lattice utilities.

Provides high-level helpers for managing VPC Lattice service networks,
services, target groups, and target registration.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchUpdateRuleResult",
    "CreateAccessLogSubscriptionResult",
    "CreateListenerResult",
    "CreateResourceConfigurationResult",
    "CreateResourceGatewayResult",
    "CreateRuleResult",
    "CreateServiceNetworkResourceAssociationResult",
    "CreateServiceNetworkServiceAssociationResult",
    "CreateServiceNetworkVpcAssociationResult",
    "DeleteResourceEndpointAssociationResult",
    "DeleteResourceGatewayResult",
    "DeleteServiceNetworkResourceAssociationResult",
    "DeleteServiceNetworkServiceAssociationResult",
    "DeleteServiceNetworkVpcAssociationResult",
    "DeleteTargetGroupResult",
    "GetAccessLogSubscriptionResult",
    "GetAuthPolicyResult",
    "GetDomainVerificationResult",
    "GetListenerResult",
    "GetResourceConfigurationResult",
    "GetResourceGatewayResult",
    "GetResourcePolicyResult",
    "GetRuleResult",
    "GetServiceNetworkResourceAssociationResult",
    "GetServiceNetworkServiceAssociationResult",
    "GetServiceNetworkVpcAssociationResult",
    "ListAccessLogSubscriptionsResult",
    "ListDomainVerificationsResult",
    "ListListenersResult",
    "ListResourceConfigurationsResult",
    "ListResourceEndpointAssociationsResult",
    "ListResourceGatewaysResult",
    "ListRulesResult",
    "ListServiceNetworkResourceAssociationsResult",
    "ListServiceNetworkServiceAssociationsResult",
    "ListServiceNetworkVpcAssociationsResult",
    "ListServiceNetworkVpcEndpointAssociationsResult",
    "ListTagsForResourceResult",
    "PutAuthPolicyResult",
    "ServiceNetworkResult",
    "ServiceResult",
    "StartDomainVerificationResult",
    "TargetGroupResult",
    "TargetResult",
    "UpdateAccessLogSubscriptionResult",
    "UpdateListenerResult",
    "UpdateResourceConfigurationResult",
    "UpdateResourceGatewayResult",
    "UpdateRuleResult",
    "UpdateServiceNetworkVpcAssociationResult",
    "UpdateTargetGroupResult",
    "batch_update_rule",
    "create_access_log_subscription",
    "create_listener",
    "create_resource_configuration",
    "create_resource_gateway",
    "create_rule",
    "create_service",
    "create_service_network",
    "create_service_network_resource_association",
    "create_service_network_service_association",
    "create_service_network_vpc_association",
    "create_target_group",
    "delete_access_log_subscription",
    "delete_auth_policy",
    "delete_domain_verification",
    "delete_listener",
    "delete_resource_configuration",
    "delete_resource_endpoint_association",
    "delete_resource_gateway",
    "delete_resource_policy",
    "delete_rule",
    "delete_service",
    "delete_service_network",
    "delete_service_network_resource_association",
    "delete_service_network_service_association",
    "delete_service_network_vpc_association",
    "delete_target_group",
    "deregister_targets",
    "get_access_log_subscription",
    "get_auth_policy",
    "get_domain_verification",
    "get_listener",
    "get_resource_configuration",
    "get_resource_gateway",
    "get_resource_policy",
    "get_rule",
    "get_service",
    "get_service_network",
    "get_service_network_resource_association",
    "get_service_network_service_association",
    "get_service_network_vpc_association",
    "get_target_group",
    "list_access_log_subscriptions",
    "list_domain_verifications",
    "list_listeners",
    "list_resource_configurations",
    "list_resource_endpoint_associations",
    "list_resource_gateways",
    "list_rules",
    "list_service_network_resource_associations",
    "list_service_network_service_associations",
    "list_service_network_vpc_associations",
    "list_service_network_vpc_endpoint_associations",
    "list_service_networks",
    "list_services",
    "list_tags_for_resource",
    "list_target_groups",
    "list_targets",
    "put_auth_policy",
    "put_resource_policy",
    "register_targets",
    "start_domain_verification",
    "tag_resource",
    "untag_resource",
    "update_access_log_subscription",
    "update_listener",
    "update_resource_configuration",
    "update_resource_gateway",
    "update_rule",
    "update_service",
    "update_service_network",
    "update_service_network_vpc_association",
    "update_target_group",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ServiceNetworkResult(BaseModel):
    """Metadata for a VPC Lattice service network."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str
    auth_type: str | None = None
    status: str | None = None
    extra: dict[str, Any] = {}


class ServiceResult(BaseModel):
    """Metadata for a VPC Lattice service."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str
    status: str | None = None
    dns_entry: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


class TargetGroupResult(BaseModel):
    """Metadata for a VPC Lattice target group."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str
    type: str | None = None
    status: str | None = None
    extra: dict[str, Any] = {}


class TargetResult(BaseModel):
    """Metadata for a registered VPC Lattice target."""

    model_config = ConfigDict(frozen=True)

    id: str
    port: int | None = None
    status: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SN_KEYS = {"id", "arn", "name", "authType", "status"}
_SVC_KEYS = {"id", "arn", "name", "status", "dnsEntry"}
_TG_KEYS = {"id", "arn", "name", "type", "status"}
_TGT_KEYS = {"id", "port", "status"}


def _parse_sn(data: dict[str, Any]) -> ServiceNetworkResult:
    """Parse a raw service-network description into a model."""
    return ServiceNetworkResult(
        id=data.get("id", ""),
        arn=data.get("arn", ""),
        name=data.get("name", ""),
        auth_type=data.get("authType"),
        status=data.get("status"),
        extra={k: v for k, v in data.items() if k not in _SN_KEYS},
    )


def _parse_svc(data: dict[str, Any]) -> ServiceResult:
    """Parse a raw service description into a model."""
    return ServiceResult(
        id=data.get("id", ""),
        arn=data.get("arn", ""),
        name=data.get("name", ""),
        status=data.get("status"),
        dns_entry=data.get("dnsEntry"),
        extra={k: v for k, v in data.items() if k not in _SVC_KEYS},
    )


def _parse_tg(data: dict[str, Any]) -> TargetGroupResult:
    """Parse a raw target-group description into a model."""
    return TargetGroupResult(
        id=data.get("id", ""),
        arn=data.get("arn", ""),
        name=data.get("name", ""),
        type=data.get("type"),
        status=data.get("status"),
        extra={k: v for k, v in data.items() if k not in _TG_KEYS},
    )


def _parse_target(data: dict[str, Any]) -> TargetResult:
    """Parse a raw target description into a model."""
    return TargetResult(
        id=data.get("id", ""),
        port=data.get("port"),
        status=data.get("status"),
        extra={k: v for k, v in data.items() if k not in _TGT_KEYS},
    )


# ---------------------------------------------------------------------------
# Service Network operations
# ---------------------------------------------------------------------------


def create_service_network(
    name: str,
    *,
    auth_type: str = "NONE",
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ServiceNetworkResult:
    """Create a VPC Lattice service network.

    Args:
        name: Service network name.
        auth_type: Authentication type (``NONE`` or ``AWS_IAM``).
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`ServiceNetworkResult` for the new service network.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {"name": name, "authType": auth_type}
    if tags:
        kwargs["tags"] = tags
    try:
        resp = client.create_service_network(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_service_network failed for {name!r}") from exc
    return _parse_sn(resp)


def get_service_network(
    identifier: str,
    *,
    region_name: str | None = None,
) -> ServiceNetworkResult:
    """Get details of a VPC Lattice service network.

    Args:
        identifier: Service network ID or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ServiceNetworkResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.get_service_network(serviceNetworkIdentifier=identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_service_network failed for {identifier!r}") from exc
    return _parse_sn(resp)


def list_service_networks(
    *,
    region_name: str | None = None,
) -> list[ServiceNetworkResult]:
    """List all VPC Lattice service networks.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ServiceNetworkResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    results: list[ServiceNetworkResult] = []
    try:
        paginator = client.get_paginator("list_service_networks")
        for page in paginator.paginate():
            for item in page.get("items", []):
                results.append(_parse_sn(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_service_networks failed") from exc
    return results


def update_service_network(
    identifier: str,
    *,
    auth_type: str,
    region_name: str | None = None,
) -> ServiceNetworkResult:
    """Update a VPC Lattice service network.

    Args:
        identifier: Service network ID or ARN.
        auth_type: New authentication type.
        region_name: AWS region override.

    Returns:
        The updated :class:`ServiceNetworkResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.update_service_network(
            serviceNetworkIdentifier=identifier,
            authType=auth_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_service_network failed for {identifier!r}") from exc
    return _parse_sn(resp)


def delete_service_network(
    identifier: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a VPC Lattice service network.

    Args:
        identifier: Service network ID or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        client.delete_service_network(serviceNetworkIdentifier=identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_service_network failed for {identifier!r}") from exc


# ---------------------------------------------------------------------------
# Service operations
# ---------------------------------------------------------------------------


def create_service(
    name: str,
    *,
    auth_type: str = "NONE",
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ServiceResult:
    """Create a VPC Lattice service.

    Args:
        name: Service name.
        auth_type: Authentication type (``NONE`` or ``AWS_IAM``).
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`ServiceResult` for the new service.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {"name": name, "authType": auth_type}
    if tags:
        kwargs["tags"] = tags
    try:
        resp = client.create_service(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_service failed for {name!r}") from exc
    return _parse_svc(resp)


def get_service(
    identifier: str,
    *,
    region_name: str | None = None,
) -> ServiceResult:
    """Get details of a VPC Lattice service.

    Args:
        identifier: Service ID or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ServiceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.get_service(serviceIdentifier=identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_service failed for {identifier!r}") from exc
    return _parse_svc(resp)


def list_services(
    *,
    region_name: str | None = None,
) -> list[ServiceResult]:
    """List all VPC Lattice services.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ServiceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    results: list[ServiceResult] = []
    try:
        paginator = client.get_paginator("list_services")
        for page in paginator.paginate():
            for item in page.get("items", []):
                results.append(_parse_svc(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_services failed") from exc
    return results


def update_service(
    identifier: str,
    *,
    auth_type: str,
    region_name: str | None = None,
) -> ServiceResult:
    """Update a VPC Lattice service.

    Args:
        identifier: Service ID or ARN.
        auth_type: New authentication type.
        region_name: AWS region override.

    Returns:
        The updated :class:`ServiceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.update_service(
            serviceIdentifier=identifier,
            authType=auth_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_service failed for {identifier!r}") from exc
    return _parse_svc(resp)


def delete_service(
    identifier: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a VPC Lattice service.

    Args:
        identifier: Service ID or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        client.delete_service(serviceIdentifier=identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_service failed for {identifier!r}") from exc


# ---------------------------------------------------------------------------
# Target Group operations
# ---------------------------------------------------------------------------


def create_target_group(
    name: str,
    *,
    type: str = "INSTANCE",
    config: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> TargetGroupResult:
    """Create a VPC Lattice target group.

    Args:
        name: Target group name.
        type: Target group type (``INSTANCE``, ``IP``, ``LAMBDA``, ``ALB``).
        config: Target group configuration dict.
        tags: Optional key-value tags.
        region_name: AWS region override.

    Returns:
        A :class:`TargetGroupResult` for the new target group.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {"name": name, "type": type}
    if config is not None:
        kwargs["config"] = config
    if tags:
        kwargs["tags"] = tags
    try:
        resp = client.create_target_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_target_group failed for {name!r}") from exc
    return _parse_tg(resp)


def get_target_group(
    identifier: str,
    *,
    region_name: str | None = None,
) -> TargetGroupResult:
    """Get details of a VPC Lattice target group.

    Args:
        identifier: Target group ID or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`TargetGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.get_target_group(targetGroupIdentifier=identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_target_group failed for {identifier!r}") from exc
    return _parse_tg(resp)


def list_target_groups(
    *,
    region_name: str | None = None,
) -> list[TargetGroupResult]:
    """List all VPC Lattice target groups.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`TargetGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    results: list[TargetGroupResult] = []
    try:
        paginator = client.get_paginator("list_target_groups")
        for page in paginator.paginate():
            for item in page.get("items", []):
                results.append(_parse_tg(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_target_groups failed") from exc
    return results


# ---------------------------------------------------------------------------
# Target registration
# ---------------------------------------------------------------------------


def register_targets(
    target_group_identifier: str,
    *,
    targets: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Register targets with a VPC Lattice target group.

    Args:
        target_group_identifier: Target group ID or ARN.
        targets: List of target dicts with ``id`` and optional ``port``.
        region_name: AWS region override.

    Returns:
        List of successful target registrations.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.register_targets(
            targetGroupIdentifier=target_group_identifier,
            targets=targets,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "register_targets failed") from exc
    return resp.get("successful", [])


def deregister_targets(
    target_group_identifier: str,
    *,
    targets: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Deregister targets from a VPC Lattice target group.

    Args:
        target_group_identifier: Target group ID or ARN.
        targets: List of target dicts with ``id`` and optional ``port``.
        region_name: AWS region override.

    Returns:
        List of successful target deregistrations.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    try:
        resp = client.deregister_targets(
            targetGroupIdentifier=target_group_identifier,
            targets=targets,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "deregister_targets failed") from exc
    return resp.get("successful", [])


def list_targets(
    target_group_identifier: str,
    *,
    region_name: str | None = None,
) -> list[TargetResult]:
    """List targets registered with a VPC Lattice target group.

    Args:
        target_group_identifier: Target group ID or ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`TargetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    results: list[TargetResult] = []
    try:
        paginator = client.get_paginator("list_targets")
        for page in paginator.paginate(targetGroupIdentifier=target_group_identifier):
            for item in page.get("items", []):
                results.append(_parse_target(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_targets failed") from exc
    return results


class BatchUpdateRuleResult(BaseModel):
    """Result of batch_update_rule."""

    model_config = ConfigDict(frozen=True)

    successful: list[dict[str, Any]] | None = None
    unsuccessful: list[dict[str, Any]] | None = None


class CreateAccessLogSubscriptionResult(BaseModel):
    """Result of create_access_log_subscription."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    resource_id: str | None = None
    resource_arn: str | None = None
    service_network_log_type: str | None = None
    destination_arn: str | None = None


class CreateListenerResult(BaseModel):
    """Result of create_listener."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    protocol: str | None = None
    port: int | None = None
    service_arn: str | None = None
    service_id: str | None = None
    default_action: dict[str, Any] | None = None


class CreateResourceConfigurationResult(BaseModel):
    """Result of create_resource_configuration."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    resource_gateway_id: str | None = None
    resource_configuration_group_id: str | None = None
    type_value: str | None = None
    port_ranges: list[str] | None = None
    protocol: str | None = None
    status: str | None = None
    resource_configuration_definition: dict[str, Any] | None = None
    allow_association_to_shareable_service_network: bool | None = None
    created_at: str | None = None
    failure_reason: str | None = None
    custom_domain_name: str | None = None
    domain_verification_id: str | None = None
    group_domain: str | None = None
    domain_verification_arn: str | None = None


class CreateResourceGatewayResult(BaseModel):
    """Result of create_resource_gateway."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    vpc_identifier: str | None = None
    subnet_ids: list[str] | None = None
    security_group_ids: list[str] | None = None
    ip_address_type: str | None = None
    ipv4_addresses_per_eni: int | None = None


class CreateRuleResult(BaseModel):
    """Result of create_rule."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    match: dict[str, Any] | None = None
    priority: int | None = None
    action: dict[str, Any] | None = None


class CreateServiceNetworkResourceAssociationResult(BaseModel):
    """Result of create_service_network_resource_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_by: str | None = None
    private_dns_enabled: bool | None = None


class CreateServiceNetworkServiceAssociationResult(BaseModel):
    """Result of create_service_network_service_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None
    created_by: str | None = None
    custom_domain_name: str | None = None
    dns_entry: dict[str, Any] | None = None


class CreateServiceNetworkVpcAssociationResult(BaseModel):
    """Result of create_service_network_vpc_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None
    created_by: str | None = None
    security_group_ids: list[str] | None = None
    private_dns_enabled: bool | None = None
    dns_options: dict[str, Any] | None = None


class DeleteResourceEndpointAssociationResult(BaseModel):
    """Result of delete_resource_endpoint_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    resource_configuration_id: str | None = None
    resource_configuration_arn: str | None = None
    vpc_endpoint_id: str | None = None


class DeleteResourceGatewayResult(BaseModel):
    """Result of delete_resource_gateway."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    name: str | None = None
    status: str | None = None


class DeleteServiceNetworkResourceAssociationResult(BaseModel):
    """Result of delete_service_network_resource_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    status: str | None = None


class DeleteServiceNetworkServiceAssociationResult(BaseModel):
    """Result of delete_service_network_service_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None


class DeleteServiceNetworkVpcAssociationResult(BaseModel):
    """Result of delete_service_network_vpc_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None


class DeleteTargetGroupResult(BaseModel):
    """Result of delete_target_group."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    status: str | None = None


class GetAccessLogSubscriptionResult(BaseModel):
    """Result of get_access_log_subscription."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    resource_id: str | None = None
    resource_arn: str | None = None
    destination_arn: str | None = None
    service_network_log_type: str | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


class GetAuthPolicyResult(BaseModel):
    """Result of get_auth_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None
    state: str | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


class GetDomainVerificationResult(BaseModel):
    """Result of get_domain_verification."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    domain_name: str | None = None
    status: str | None = None
    txt_method_config: dict[str, Any] | None = None
    created_at: str | None = None
    last_verified_time: str | None = None
    tags: dict[str, Any] | None = None


class GetListenerResult(BaseModel):
    """Result of get_listener."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    protocol: str | None = None
    port: int | None = None
    service_arn: str | None = None
    service_id: str | None = None
    default_action: dict[str, Any] | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


class GetResourceConfigurationResult(BaseModel):
    """Result of get_resource_configuration."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    resource_gateway_id: str | None = None
    resource_configuration_group_id: str | None = None
    type_value: str | None = None
    allow_association_to_shareable_service_network: bool | None = None
    port_ranges: list[str] | None = None
    protocol: str | None = None
    custom_domain_name: str | None = None
    status: str | None = None
    resource_configuration_definition: dict[str, Any] | None = None
    created_at: str | None = None
    amazon_managed: bool | None = None
    failure_reason: str | None = None
    last_updated_at: str | None = None
    domain_verification_id: str | None = None
    domain_verification_arn: str | None = None
    domain_verification_status: str | None = None
    group_domain: str | None = None


class GetResourceGatewayResult(BaseModel):
    """Result of get_resource_gateway."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    vpc_id: str | None = None
    subnet_ids: list[str] | None = None
    security_group_ids: list[str] | None = None
    ip_address_type: str | None = None
    ipv4_addresses_per_eni: int | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None


class GetRuleResult(BaseModel):
    """Result of get_rule."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    is_default: bool | None = None
    match: dict[str, Any] | None = None
    priority: int | None = None
    action: dict[str, Any] | None = None
    created_at: str | None = None
    last_updated_at: str | None = None


class GetServiceNetworkResourceAssociationResult(BaseModel):
    """Result of get_service_network_resource_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_by: str | None = None
    created_at: str | None = None
    resource_configuration_id: str | None = None
    resource_configuration_arn: str | None = None
    resource_configuration_name: str | None = None
    service_network_id: str | None = None
    service_network_arn: str | None = None
    service_network_name: str | None = None
    failure_reason: str | None = None
    failure_code: str | None = None
    last_updated_at: str | None = None
    private_dns_entry: dict[str, Any] | None = None
    private_dns_enabled: bool | None = None
    dns_entry: dict[str, Any] | None = None
    is_managed_association: bool | None = None
    domain_verification_status: str | None = None


class GetServiceNetworkServiceAssociationResult(BaseModel):
    """Result of get_service_network_service_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None
    created_by: str | None = None
    created_at: str | None = None
    service_id: str | None = None
    service_name: str | None = None
    service_arn: str | None = None
    service_network_id: str | None = None
    service_network_name: str | None = None
    service_network_arn: str | None = None
    dns_entry: dict[str, Any] | None = None
    custom_domain_name: str | None = None
    failure_message: str | None = None
    failure_code: str | None = None


class GetServiceNetworkVpcAssociationResult(BaseModel):
    """Result of get_service_network_vpc_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    status: str | None = None
    arn: str | None = None
    created_by: str | None = None
    created_at: str | None = None
    service_network_id: str | None = None
    service_network_name: str | None = None
    service_network_arn: str | None = None
    vpc_id: str | None = None
    security_group_ids: list[str] | None = None
    private_dns_enabled: bool | None = None
    failure_message: str | None = None
    failure_code: str | None = None
    last_updated_at: str | None = None
    dns_options: dict[str, Any] | None = None


class ListAccessLogSubscriptionsResult(BaseModel):
    """Result of list_access_log_subscriptions."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDomainVerificationsResult(BaseModel):
    """Result of list_domain_verifications."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListListenersResult(BaseModel):
    """Result of list_listeners."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceConfigurationsResult(BaseModel):
    """Result of list_resource_configurations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceEndpointAssociationsResult(BaseModel):
    """Result of list_resource_endpoint_associations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceGatewaysResult(BaseModel):
    """Result of list_resource_gateways."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRulesResult(BaseModel):
    """Result of list_rules."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServiceNetworkResourceAssociationsResult(BaseModel):
    """Result of list_service_network_resource_associations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServiceNetworkServiceAssociationsResult(BaseModel):
    """Result of list_service_network_service_associations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServiceNetworkVpcAssociationsResult(BaseModel):
    """Result of list_service_network_vpc_associations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServiceNetworkVpcEndpointAssociationsResult(BaseModel):
    """Result of list_service_network_vpc_endpoint_associations."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class PutAuthPolicyResult(BaseModel):
    """Result of put_auth_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None
    state: str | None = None


class StartDomainVerificationResult(BaseModel):
    """Result of start_domain_verification."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    domain_name: str | None = None
    status: str | None = None
    txt_method_config: dict[str, Any] | None = None


class UpdateAccessLogSubscriptionResult(BaseModel):
    """Result of update_access_log_subscription."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    resource_id: str | None = None
    resource_arn: str | None = None
    destination_arn: str | None = None


class UpdateListenerResult(BaseModel):
    """Result of update_listener."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    protocol: str | None = None
    port: int | None = None
    service_arn: str | None = None
    service_id: str | None = None
    default_action: dict[str, Any] | None = None


class UpdateResourceConfigurationResult(BaseModel):
    """Result of update_resource_configuration."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    resource_gateway_id: str | None = None
    resource_configuration_group_id: str | None = None
    type_value: str | None = None
    port_ranges: list[str] | None = None
    allow_association_to_shareable_service_network: bool | None = None
    protocol: str | None = None
    status: str | None = None
    resource_configuration_definition: dict[str, Any] | None = None


class UpdateResourceGatewayResult(BaseModel):
    """Result of update_resource_gateway."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    id: str | None = None
    arn: str | None = None
    status: str | None = None
    vpc_id: str | None = None
    subnet_ids: list[str] | None = None
    security_group_ids: list[str] | None = None
    ip_address_type: str | None = None


class UpdateRuleResult(BaseModel):
    """Result of update_rule."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    is_default: bool | None = None
    match: dict[str, Any] | None = None
    priority: int | None = None
    action: dict[str, Any] | None = None


class UpdateServiceNetworkVpcAssociationResult(BaseModel):
    """Result of update_service_network_vpc_association."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    status: str | None = None
    created_by: str | None = None
    security_group_ids: list[str] | None = None


class UpdateTargetGroupResult(BaseModel):
    """Result of update_target_group."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None
    name: str | None = None
    type_value: str | None = None
    config: dict[str, Any] | None = None
    status: str | None = None


def batch_update_rule(
    service_identifier: str,
    listener_identifier: str,
    rules: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchUpdateRuleResult:
    """Batch update rule.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        rules: Rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["rules"] = rules
    try:
        resp = client.batch_update_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update rule") from exc
    return BatchUpdateRuleResult(
        successful=resp.get("successful"),
        unsuccessful=resp.get("unsuccessful"),
    )


def create_access_log_subscription(
    resource_identifier: str,
    destination_arn: str,
    *,
    client_token: str | None = None,
    service_network_log_type: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAccessLogSubscriptionResult:
    """Create access log subscription.

    Args:
        resource_identifier: Resource identifier.
        destination_arn: Destination arn.
        client_token: Client token.
        service_network_log_type: Service network log type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceIdentifier"] = resource_identifier
    kwargs["destinationArn"] = destination_arn
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if service_network_log_type is not None:
        kwargs["serviceNetworkLogType"] = service_network_log_type
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_access_log_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create access log subscription") from exc
    return CreateAccessLogSubscriptionResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        resource_id=resp.get("resourceId"),
        resource_arn=resp.get("resourceArn"),
        service_network_log_type=resp.get("serviceNetworkLogType"),
        destination_arn=resp.get("destinationArn"),
    )


def create_listener(
    service_identifier: str,
    name: str,
    protocol: str,
    default_action: dict[str, Any],
    *,
    port: int | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateListenerResult:
    """Create listener.

    Args:
        service_identifier: Service identifier.
        name: Name.
        protocol: Protocol.
        default_action: Default action.
        port: Port.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["name"] = name
    kwargs["protocol"] = protocol
    kwargs["defaultAction"] = default_action
    if port is not None:
        kwargs["port"] = port
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_listener(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create listener") from exc
    return CreateListenerResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        protocol=resp.get("protocol"),
        port=resp.get("port"),
        service_arn=resp.get("serviceArn"),
        service_id=resp.get("serviceId"),
        default_action=resp.get("defaultAction"),
    )


def create_resource_configuration(
    name: str,
    type_value: str,
    *,
    port_ranges: list[str] | None = None,
    protocol: str | None = None,
    resource_gateway_identifier: str | None = None,
    resource_configuration_group_identifier: str | None = None,
    resource_configuration_definition: dict[str, Any] | None = None,
    allow_association_to_shareable_service_network: bool | None = None,
    custom_domain_name: str | None = None,
    group_domain: str | None = None,
    domain_verification_identifier: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateResourceConfigurationResult:
    """Create resource configuration.

    Args:
        name: Name.
        type_value: Type value.
        port_ranges: Port ranges.
        protocol: Protocol.
        resource_gateway_identifier: Resource gateway identifier.
        resource_configuration_group_identifier: Resource configuration group identifier.
        resource_configuration_definition: Resource configuration definition.
        allow_association_to_shareable_service_network: Allow association to shareable service network.
        custom_domain_name: Custom domain name.
        group_domain: Group domain.
        domain_verification_identifier: Domain verification identifier.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["type"] = type_value
    if port_ranges is not None:
        kwargs["portRanges"] = port_ranges
    if protocol is not None:
        kwargs["protocol"] = protocol
    if resource_gateway_identifier is not None:
        kwargs["resourceGatewayIdentifier"] = resource_gateway_identifier
    if resource_configuration_group_identifier is not None:
        kwargs["resourceConfigurationGroupIdentifier"] = resource_configuration_group_identifier
    if resource_configuration_definition is not None:
        kwargs["resourceConfigurationDefinition"] = resource_configuration_definition
    if allow_association_to_shareable_service_network is not None:
        kwargs["allowAssociationToShareableServiceNetwork"] = (
            allow_association_to_shareable_service_network
        )
    if custom_domain_name is not None:
        kwargs["customDomainName"] = custom_domain_name
    if group_domain is not None:
        kwargs["groupDomain"] = group_domain
    if domain_verification_identifier is not None:
        kwargs["domainVerificationIdentifier"] = domain_verification_identifier
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_resource_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create resource configuration") from exc
    return CreateResourceConfigurationResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        resource_gateway_id=resp.get("resourceGatewayId"),
        resource_configuration_group_id=resp.get("resourceConfigurationGroupId"),
        type_value=resp.get("type"),
        port_ranges=resp.get("portRanges"),
        protocol=resp.get("protocol"),
        status=resp.get("status"),
        resource_configuration_definition=resp.get("resourceConfigurationDefinition"),
        allow_association_to_shareable_service_network=resp.get(
            "allowAssociationToShareableServiceNetwork"
        ),
        created_at=resp.get("createdAt"),
        failure_reason=resp.get("failureReason"),
        custom_domain_name=resp.get("customDomainName"),
        domain_verification_id=resp.get("domainVerificationId"),
        group_domain=resp.get("groupDomain"),
        domain_verification_arn=resp.get("domainVerificationArn"),
    )


def create_resource_gateway(
    name: str,
    *,
    client_token: str | None = None,
    vpc_identifier: str | None = None,
    subnet_ids: list[str] | None = None,
    security_group_ids: list[str] | None = None,
    ip_address_type: str | None = None,
    ipv4_addresses_per_eni: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateResourceGatewayResult:
    """Create resource gateway.

    Args:
        name: Name.
        client_token: Client token.
        vpc_identifier: Vpc identifier.
        subnet_ids: Subnet ids.
        security_group_ids: Security group ids.
        ip_address_type: Ip address type.
        ipv4_addresses_per_eni: Ipv4 addresses per eni.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if vpc_identifier is not None:
        kwargs["vpcIdentifier"] = vpc_identifier
    if subnet_ids is not None:
        kwargs["subnetIds"] = subnet_ids
    if security_group_ids is not None:
        kwargs["securityGroupIds"] = security_group_ids
    if ip_address_type is not None:
        kwargs["ipAddressType"] = ip_address_type
    if ipv4_addresses_per_eni is not None:
        kwargs["ipv4AddressesPerEni"] = ipv4_addresses_per_eni
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_resource_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create resource gateway") from exc
    return CreateResourceGatewayResult(
        name=resp.get("name"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        vpc_identifier=resp.get("vpcIdentifier"),
        subnet_ids=resp.get("subnetIds"),
        security_group_ids=resp.get("securityGroupIds"),
        ip_address_type=resp.get("ipAddressType"),
        ipv4_addresses_per_eni=resp.get("ipv4AddressesPerEni"),
    )


def create_rule(
    service_identifier: str,
    listener_identifier: str,
    name: str,
    match: dict[str, Any],
    priority: int,
    action: dict[str, Any],
    *,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateRuleResult:
    """Create rule.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        name: Name.
        match: Match.
        priority: Priority.
        action: Action.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["name"] = name
    kwargs["match"] = match
    kwargs["priority"] = priority
    kwargs["action"] = action
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create rule") from exc
    return CreateRuleResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        match=resp.get("match"),
        priority=resp.get("priority"),
        action=resp.get("action"),
    )


def create_service_network_resource_association(
    resource_configuration_identifier: str,
    service_network_identifier: str,
    *,
    client_token: str | None = None,
    private_dns_enabled: bool | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateServiceNetworkResourceAssociationResult:
    """Create service network resource association.

    Args:
        resource_configuration_identifier: Resource configuration identifier.
        service_network_identifier: Service network identifier.
        client_token: Client token.
        private_dns_enabled: Private dns enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if private_dns_enabled is not None:
        kwargs["privateDnsEnabled"] = private_dns_enabled
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_service_network_resource_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create service network resource association") from exc
    return CreateServiceNetworkResourceAssociationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_by=resp.get("createdBy"),
        private_dns_enabled=resp.get("privateDnsEnabled"),
    )


def create_service_network_service_association(
    service_identifier: str,
    service_network_identifier: str,
    *,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateServiceNetworkServiceAssociationResult:
    """Create service network service association.

    Args:
        service_identifier: Service identifier.
        service_network_identifier: Service network identifier.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_service_network_service_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create service network service association") from exc
    return CreateServiceNetworkServiceAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
        created_by=resp.get("createdBy"),
        custom_domain_name=resp.get("customDomainName"),
        dns_entry=resp.get("dnsEntry"),
    )


def create_service_network_vpc_association(
    service_network_identifier: str,
    vpc_identifier: str,
    *,
    client_token: str | None = None,
    private_dns_enabled: bool | None = None,
    security_group_ids: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    dns_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateServiceNetworkVpcAssociationResult:
    """Create service network vpc association.

    Args:
        service_network_identifier: Service network identifier.
        vpc_identifier: Vpc identifier.
        client_token: Client token.
        private_dns_enabled: Private dns enabled.
        security_group_ids: Security group ids.
        tags: Tags.
        dns_options: Dns options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkIdentifier"] = service_network_identifier
    kwargs["vpcIdentifier"] = vpc_identifier
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if private_dns_enabled is not None:
        kwargs["privateDnsEnabled"] = private_dns_enabled
    if security_group_ids is not None:
        kwargs["securityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["tags"] = tags
    if dns_options is not None:
        kwargs["dnsOptions"] = dns_options
    try:
        resp = client.create_service_network_vpc_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create service network vpc association") from exc
    return CreateServiceNetworkVpcAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
        created_by=resp.get("createdBy"),
        security_group_ids=resp.get("securityGroupIds"),
        private_dns_enabled=resp.get("privateDnsEnabled"),
        dns_options=resp.get("dnsOptions"),
    )


def delete_access_log_subscription(
    access_log_subscription_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete access log subscription.

    Args:
        access_log_subscription_identifier: Access log subscription identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessLogSubscriptionIdentifier"] = access_log_subscription_identifier
    try:
        client.delete_access_log_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete access log subscription") from exc
    return None


def delete_auth_policy(
    resource_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete auth policy.

    Args:
        resource_identifier: Resource identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceIdentifier"] = resource_identifier
    try:
        client.delete_auth_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete auth policy") from exc
    return None


def delete_domain_verification(
    domain_verification_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete domain verification.

    Args:
        domain_verification_identifier: Domain verification identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainVerificationIdentifier"] = domain_verification_identifier
    try:
        client.delete_domain_verification(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete domain verification") from exc
    return None


def delete_listener(
    service_identifier: str,
    listener_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete listener.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    try:
        client.delete_listener(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete listener") from exc
    return None


def delete_resource_configuration(
    resource_configuration_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete resource configuration.

    Args:
        resource_configuration_identifier: Resource configuration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    try:
        client.delete_resource_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource configuration") from exc
    return None


def delete_resource_endpoint_association(
    resource_endpoint_association_identifier: str,
    region_name: str | None = None,
) -> DeleteResourceEndpointAssociationResult:
    """Delete resource endpoint association.

    Args:
        resource_endpoint_association_identifier: Resource endpoint association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceEndpointAssociationIdentifier"] = resource_endpoint_association_identifier
    try:
        resp = client.delete_resource_endpoint_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource endpoint association") from exc
    return DeleteResourceEndpointAssociationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        resource_configuration_id=resp.get("resourceConfigurationId"),
        resource_configuration_arn=resp.get("resourceConfigurationArn"),
        vpc_endpoint_id=resp.get("vpcEndpointId"),
    )


def delete_resource_gateway(
    resource_gateway_identifier: str,
    region_name: str | None = None,
) -> DeleteResourceGatewayResult:
    """Delete resource gateway.

    Args:
        resource_gateway_identifier: Resource gateway identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceGatewayIdentifier"] = resource_gateway_identifier
    try:
        resp = client.delete_resource_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource gateway") from exc
    return DeleteResourceGatewayResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        name=resp.get("name"),
        status=resp.get("status"),
    )


def delete_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def delete_rule(
    service_identifier: str,
    listener_identifier: str,
    rule_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete rule.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        rule_identifier: Rule identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["ruleIdentifier"] = rule_identifier
    try:
        client.delete_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete rule") from exc
    return None


def delete_service_network_resource_association(
    service_network_resource_association_identifier: str,
    region_name: str | None = None,
) -> DeleteServiceNetworkResourceAssociationResult:
    """Delete service network resource association.

    Args:
        service_network_resource_association_identifier: Service network resource association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkResourceAssociationIdentifier"] = (
        service_network_resource_association_identifier
    )
    try:
        resp = client.delete_service_network_resource_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete service network resource association") from exc
    return DeleteServiceNetworkResourceAssociationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
    )


def delete_service_network_service_association(
    service_network_service_association_identifier: str,
    region_name: str | None = None,
) -> DeleteServiceNetworkServiceAssociationResult:
    """Delete service network service association.

    Args:
        service_network_service_association_identifier: Service network service association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkServiceAssociationIdentifier"] = (
        service_network_service_association_identifier
    )
    try:
        resp = client.delete_service_network_service_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete service network service association") from exc
    return DeleteServiceNetworkServiceAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
    )


def delete_service_network_vpc_association(
    service_network_vpc_association_identifier: str,
    region_name: str | None = None,
) -> DeleteServiceNetworkVpcAssociationResult:
    """Delete service network vpc association.

    Args:
        service_network_vpc_association_identifier: Service network vpc association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkVpcAssociationIdentifier"] = service_network_vpc_association_identifier
    try:
        resp = client.delete_service_network_vpc_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete service network vpc association") from exc
    return DeleteServiceNetworkVpcAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
    )


def delete_target_group(
    target_group_identifier: str,
    region_name: str | None = None,
) -> DeleteTargetGroupResult:
    """Delete target group.

    Args:
        target_group_identifier: Target group identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetGroupIdentifier"] = target_group_identifier
    try:
        resp = client.delete_target_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete target group") from exc
    return DeleteTargetGroupResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
    )


def get_access_log_subscription(
    access_log_subscription_identifier: str,
    region_name: str | None = None,
) -> GetAccessLogSubscriptionResult:
    """Get access log subscription.

    Args:
        access_log_subscription_identifier: Access log subscription identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessLogSubscriptionIdentifier"] = access_log_subscription_identifier
    try:
        resp = client.get_access_log_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get access log subscription") from exc
    return GetAccessLogSubscriptionResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        resource_id=resp.get("resourceId"),
        resource_arn=resp.get("resourceArn"),
        destination_arn=resp.get("destinationArn"),
        service_network_log_type=resp.get("serviceNetworkLogType"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_auth_policy(
    resource_identifier: str,
    region_name: str | None = None,
) -> GetAuthPolicyResult:
    """Get auth policy.

    Args:
        resource_identifier: Resource identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceIdentifier"] = resource_identifier
    try:
        resp = client.get_auth_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get auth policy") from exc
    return GetAuthPolicyResult(
        policy=resp.get("policy"),
        state=resp.get("state"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_domain_verification(
    domain_verification_identifier: str,
    region_name: str | None = None,
) -> GetDomainVerificationResult:
    """Get domain verification.

    Args:
        domain_verification_identifier: Domain verification identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainVerificationIdentifier"] = domain_verification_identifier
    try:
        resp = client.get_domain_verification(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get domain verification") from exc
    return GetDomainVerificationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        domain_name=resp.get("domainName"),
        status=resp.get("status"),
        txt_method_config=resp.get("txtMethodConfig"),
        created_at=resp.get("createdAt"),
        last_verified_time=resp.get("lastVerifiedTime"),
        tags=resp.get("tags"),
    )


def get_listener(
    service_identifier: str,
    listener_identifier: str,
    region_name: str | None = None,
) -> GetListenerResult:
    """Get listener.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    try:
        resp = client.get_listener(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get listener") from exc
    return GetListenerResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        protocol=resp.get("protocol"),
        port=resp.get("port"),
        service_arn=resp.get("serviceArn"),
        service_id=resp.get("serviceId"),
        default_action=resp.get("defaultAction"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_resource_configuration(
    resource_configuration_identifier: str,
    region_name: str | None = None,
) -> GetResourceConfigurationResult:
    """Get resource configuration.

    Args:
        resource_configuration_identifier: Resource configuration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    try:
        resp = client.get_resource_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource configuration") from exc
    return GetResourceConfigurationResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        resource_gateway_id=resp.get("resourceGatewayId"),
        resource_configuration_group_id=resp.get("resourceConfigurationGroupId"),
        type_value=resp.get("type"),
        allow_association_to_shareable_service_network=resp.get(
            "allowAssociationToShareableServiceNetwork"
        ),
        port_ranges=resp.get("portRanges"),
        protocol=resp.get("protocol"),
        custom_domain_name=resp.get("customDomainName"),
        status=resp.get("status"),
        resource_configuration_definition=resp.get("resourceConfigurationDefinition"),
        created_at=resp.get("createdAt"),
        amazon_managed=resp.get("amazonManaged"),
        failure_reason=resp.get("failureReason"),
        last_updated_at=resp.get("lastUpdatedAt"),
        domain_verification_id=resp.get("domainVerificationId"),
        domain_verification_arn=resp.get("domainVerificationArn"),
        domain_verification_status=resp.get("domainVerificationStatus"),
        group_domain=resp.get("groupDomain"),
    )


def get_resource_gateway(
    resource_gateway_identifier: str,
    region_name: str | None = None,
) -> GetResourceGatewayResult:
    """Get resource gateway.

    Args:
        resource_gateway_identifier: Resource gateway identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceGatewayIdentifier"] = resource_gateway_identifier
    try:
        resp = client.get_resource_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource gateway") from exc
    return GetResourceGatewayResult(
        name=resp.get("name"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        vpc_id=resp.get("vpcId"),
        subnet_ids=resp.get("subnetIds"),
        security_group_ids=resp.get("securityGroupIds"),
        ip_address_type=resp.get("ipAddressType"),
        ipv4_addresses_per_eni=resp.get("ipv4AddressesPerEni"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy=resp.get("policy"),
    )


def get_rule(
    service_identifier: str,
    listener_identifier: str,
    rule_identifier: str,
    region_name: str | None = None,
) -> GetRuleResult:
    """Get rule.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        rule_identifier: Rule identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["ruleIdentifier"] = rule_identifier
    try:
        resp = client.get_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get rule") from exc
    return GetRuleResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        is_default=resp.get("isDefault"),
        match=resp.get("match"),
        priority=resp.get("priority"),
        action=resp.get("action"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


def get_service_network_resource_association(
    service_network_resource_association_identifier: str,
    region_name: str | None = None,
) -> GetServiceNetworkResourceAssociationResult:
    """Get service network resource association.

    Args:
        service_network_resource_association_identifier: Service network resource association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkResourceAssociationIdentifier"] = (
        service_network_resource_association_identifier
    )
    try:
        resp = client.get_service_network_resource_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get service network resource association") from exc
    return GetServiceNetworkResourceAssociationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_by=resp.get("createdBy"),
        created_at=resp.get("createdAt"),
        resource_configuration_id=resp.get("resourceConfigurationId"),
        resource_configuration_arn=resp.get("resourceConfigurationArn"),
        resource_configuration_name=resp.get("resourceConfigurationName"),
        service_network_id=resp.get("serviceNetworkId"),
        service_network_arn=resp.get("serviceNetworkArn"),
        service_network_name=resp.get("serviceNetworkName"),
        failure_reason=resp.get("failureReason"),
        failure_code=resp.get("failureCode"),
        last_updated_at=resp.get("lastUpdatedAt"),
        private_dns_entry=resp.get("privateDnsEntry"),
        private_dns_enabled=resp.get("privateDnsEnabled"),
        dns_entry=resp.get("dnsEntry"),
        is_managed_association=resp.get("isManagedAssociation"),
        domain_verification_status=resp.get("domainVerificationStatus"),
    )


def get_service_network_service_association(
    service_network_service_association_identifier: str,
    region_name: str | None = None,
) -> GetServiceNetworkServiceAssociationResult:
    """Get service network service association.

    Args:
        service_network_service_association_identifier: Service network service association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkServiceAssociationIdentifier"] = (
        service_network_service_association_identifier
    )
    try:
        resp = client.get_service_network_service_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get service network service association") from exc
    return GetServiceNetworkServiceAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
        created_by=resp.get("createdBy"),
        created_at=resp.get("createdAt"),
        service_id=resp.get("serviceId"),
        service_name=resp.get("serviceName"),
        service_arn=resp.get("serviceArn"),
        service_network_id=resp.get("serviceNetworkId"),
        service_network_name=resp.get("serviceNetworkName"),
        service_network_arn=resp.get("serviceNetworkArn"),
        dns_entry=resp.get("dnsEntry"),
        custom_domain_name=resp.get("customDomainName"),
        failure_message=resp.get("failureMessage"),
        failure_code=resp.get("failureCode"),
    )


def get_service_network_vpc_association(
    service_network_vpc_association_identifier: str,
    region_name: str | None = None,
) -> GetServiceNetworkVpcAssociationResult:
    """Get service network vpc association.

    Args:
        service_network_vpc_association_identifier: Service network vpc association identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkVpcAssociationIdentifier"] = service_network_vpc_association_identifier
    try:
        resp = client.get_service_network_vpc_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get service network vpc association") from exc
    return GetServiceNetworkVpcAssociationResult(
        id=resp.get("id"),
        status=resp.get("status"),
        arn=resp.get("arn"),
        created_by=resp.get("createdBy"),
        created_at=resp.get("createdAt"),
        service_network_id=resp.get("serviceNetworkId"),
        service_network_name=resp.get("serviceNetworkName"),
        service_network_arn=resp.get("serviceNetworkArn"),
        vpc_id=resp.get("vpcId"),
        security_group_ids=resp.get("securityGroupIds"),
        private_dns_enabled=resp.get("privateDnsEnabled"),
        failure_message=resp.get("failureMessage"),
        failure_code=resp.get("failureCode"),
        last_updated_at=resp.get("lastUpdatedAt"),
        dns_options=resp.get("dnsOptions"),
    )


def list_access_log_subscriptions(
    resource_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAccessLogSubscriptionsResult:
    """List access log subscriptions.

    Args:
        resource_identifier: Resource identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceIdentifier"] = resource_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_access_log_subscriptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list access log subscriptions") from exc
    return ListAccessLogSubscriptionsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_domain_verifications(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDomainVerificationsResult:
    """List domain verifications.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_domain_verifications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list domain verifications") from exc
    return ListDomainVerificationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_listeners(
    service_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListListenersResult:
    """List listeners.

    Args:
        service_identifier: Service identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_listeners(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list listeners") from exc
    return ListListenersResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_resource_configurations(
    *,
    resource_gateway_identifier: str | None = None,
    resource_configuration_group_identifier: str | None = None,
    domain_verification_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceConfigurationsResult:
    """List resource configurations.

    Args:
        resource_gateway_identifier: Resource gateway identifier.
        resource_configuration_group_identifier: Resource configuration group identifier.
        domain_verification_identifier: Domain verification identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if resource_gateway_identifier is not None:
        kwargs["resourceGatewayIdentifier"] = resource_gateway_identifier
    if resource_configuration_group_identifier is not None:
        kwargs["resourceConfigurationGroupIdentifier"] = resource_configuration_group_identifier
    if domain_verification_identifier is not None:
        kwargs["domainVerificationIdentifier"] = domain_verification_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_resource_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource configurations") from exc
    return ListResourceConfigurationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_resource_endpoint_associations(
    resource_configuration_identifier: str,
    *,
    resource_endpoint_association_identifier: str | None = None,
    vpc_endpoint_id: str | None = None,
    vpc_endpoint_owner: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceEndpointAssociationsResult:
    """List resource endpoint associations.

    Args:
        resource_configuration_identifier: Resource configuration identifier.
        resource_endpoint_association_identifier: Resource endpoint association identifier.
        vpc_endpoint_id: Vpc endpoint id.
        vpc_endpoint_owner: Vpc endpoint owner.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    if resource_endpoint_association_identifier is not None:
        kwargs["resourceEndpointAssociationIdentifier"] = resource_endpoint_association_identifier
    if vpc_endpoint_id is not None:
        kwargs["vpcEndpointId"] = vpc_endpoint_id
    if vpc_endpoint_owner is not None:
        kwargs["vpcEndpointOwner"] = vpc_endpoint_owner
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_resource_endpoint_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource endpoint associations") from exc
    return ListResourceEndpointAssociationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_resource_gateways(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceGatewaysResult:
    """List resource gateways.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_resource_gateways(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource gateways") from exc
    return ListResourceGatewaysResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_rules(
    service_identifier: str,
    listener_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRulesResult:
    """List rules.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rules") from exc
    return ListRulesResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_service_network_resource_associations(
    *,
    service_network_identifier: str | None = None,
    resource_configuration_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    include_children: bool | None = None,
    region_name: str | None = None,
) -> ListServiceNetworkResourceAssociationsResult:
    """List service network resource associations.

    Args:
        service_network_identifier: Service network identifier.
        resource_configuration_identifier: Resource configuration identifier.
        max_results: Max results.
        next_token: Next token.
        include_children: Include children.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if service_network_identifier is not None:
        kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if resource_configuration_identifier is not None:
        kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if include_children is not None:
        kwargs["includeChildren"] = include_children
    try:
        resp = client.list_service_network_resource_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list service network resource associations") from exc
    return ListServiceNetworkResourceAssociationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_service_network_service_associations(
    *,
    service_network_identifier: str | None = None,
    service_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListServiceNetworkServiceAssociationsResult:
    """List service network service associations.

    Args:
        service_network_identifier: Service network identifier.
        service_identifier: Service identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if service_network_identifier is not None:
        kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if service_identifier is not None:
        kwargs["serviceIdentifier"] = service_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_service_network_service_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list service network service associations") from exc
    return ListServiceNetworkServiceAssociationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_service_network_vpc_associations(
    *,
    service_network_identifier: str | None = None,
    vpc_identifier: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListServiceNetworkVpcAssociationsResult:
    """List service network vpc associations.

    Args:
        service_network_identifier: Service network identifier.
        vpc_identifier: Vpc identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    if service_network_identifier is not None:
        kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if vpc_identifier is not None:
        kwargs["vpcIdentifier"] = vpc_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_service_network_vpc_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list service network vpc associations") from exc
    return ListServiceNetworkVpcAssociationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_service_network_vpc_endpoint_associations(
    service_network_identifier: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListServiceNetworkVpcEndpointAssociationsResult:
    """List service network vpc endpoint associations.

    Args:
        service_network_identifier: Service network identifier.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkIdentifier"] = service_network_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_service_network_vpc_endpoint_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list service network vpc endpoint associations"
        ) from exc
    return ListServiceNetworkVpcEndpointAssociationsResult(
        items=resp.get("items"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def put_auth_policy(
    resource_identifier: str,
    policy: str,
    region_name: str | None = None,
) -> PutAuthPolicyResult:
    """Put auth policy.

    Args:
        resource_identifier: Resource identifier.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceIdentifier"] = resource_identifier
    kwargs["policy"] = policy
    try:
        resp = client.put_auth_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put auth policy") from exc
    return PutAuthPolicyResult(
        policy=resp.get("policy"),
        state=resp.get("state"),
    )


def put_resource_policy(
    resource_arn: str,
    policy: str,
    region_name: str | None = None,
) -> None:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["policy"] = policy
    try:
        client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return None


def start_domain_verification(
    domain_name: str,
    *,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartDomainVerificationResult:
    """Start domain verification.

    Args:
        domain_name: Domain name.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainName"] = domain_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.start_domain_verification(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start domain verification") from exc
    return StartDomainVerificationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        domain_name=resp.get("domainName"),
        status=resp.get("status"),
        txt_method_config=resp.get("txtMethodConfig"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_access_log_subscription(
    access_log_subscription_identifier: str,
    destination_arn: str,
    region_name: str | None = None,
) -> UpdateAccessLogSubscriptionResult:
    """Update access log subscription.

    Args:
        access_log_subscription_identifier: Access log subscription identifier.
        destination_arn: Destination arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessLogSubscriptionIdentifier"] = access_log_subscription_identifier
    kwargs["destinationArn"] = destination_arn
    try:
        resp = client.update_access_log_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update access log subscription") from exc
    return UpdateAccessLogSubscriptionResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        resource_id=resp.get("resourceId"),
        resource_arn=resp.get("resourceArn"),
        destination_arn=resp.get("destinationArn"),
    )


def update_listener(
    service_identifier: str,
    listener_identifier: str,
    default_action: dict[str, Any],
    region_name: str | None = None,
) -> UpdateListenerResult:
    """Update listener.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        default_action: Default action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["defaultAction"] = default_action
    try:
        resp = client.update_listener(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update listener") from exc
    return UpdateListenerResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        protocol=resp.get("protocol"),
        port=resp.get("port"),
        service_arn=resp.get("serviceArn"),
        service_id=resp.get("serviceId"),
        default_action=resp.get("defaultAction"),
    )


def update_resource_configuration(
    resource_configuration_identifier: str,
    *,
    resource_configuration_definition: dict[str, Any] | None = None,
    allow_association_to_shareable_service_network: bool | None = None,
    port_ranges: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateResourceConfigurationResult:
    """Update resource configuration.

    Args:
        resource_configuration_identifier: Resource configuration identifier.
        resource_configuration_definition: Resource configuration definition.
        allow_association_to_shareable_service_network: Allow association to shareable service network.
        port_ranges: Port ranges.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceConfigurationIdentifier"] = resource_configuration_identifier
    if resource_configuration_definition is not None:
        kwargs["resourceConfigurationDefinition"] = resource_configuration_definition
    if allow_association_to_shareable_service_network is not None:
        kwargs["allowAssociationToShareableServiceNetwork"] = (
            allow_association_to_shareable_service_network
        )
    if port_ranges is not None:
        kwargs["portRanges"] = port_ranges
    try:
        resp = client.update_resource_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update resource configuration") from exc
    return UpdateResourceConfigurationResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        resource_gateway_id=resp.get("resourceGatewayId"),
        resource_configuration_group_id=resp.get("resourceConfigurationGroupId"),
        type_value=resp.get("type"),
        port_ranges=resp.get("portRanges"),
        allow_association_to_shareable_service_network=resp.get(
            "allowAssociationToShareableServiceNetwork"
        ),
        protocol=resp.get("protocol"),
        status=resp.get("status"),
        resource_configuration_definition=resp.get("resourceConfigurationDefinition"),
    )


def update_resource_gateway(
    resource_gateway_identifier: str,
    *,
    security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateResourceGatewayResult:
    """Update resource gateway.

    Args:
        resource_gateway_identifier: Resource gateway identifier.
        security_group_ids: Security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceGatewayIdentifier"] = resource_gateway_identifier
    if security_group_ids is not None:
        kwargs["securityGroupIds"] = security_group_ids
    try:
        resp = client.update_resource_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update resource gateway") from exc
    return UpdateResourceGatewayResult(
        name=resp.get("name"),
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        vpc_id=resp.get("vpcId"),
        subnet_ids=resp.get("subnetIds"),
        security_group_ids=resp.get("securityGroupIds"),
        ip_address_type=resp.get("ipAddressType"),
    )


def update_rule(
    service_identifier: str,
    listener_identifier: str,
    rule_identifier: str,
    *,
    match: dict[str, Any] | None = None,
    priority: int | None = None,
    action: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateRuleResult:
    """Update rule.

    Args:
        service_identifier: Service identifier.
        listener_identifier: Listener identifier.
        rule_identifier: Rule identifier.
        match: Match.
        priority: Priority.
        action: Action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceIdentifier"] = service_identifier
    kwargs["listenerIdentifier"] = listener_identifier
    kwargs["ruleIdentifier"] = rule_identifier
    if match is not None:
        kwargs["match"] = match
    if priority is not None:
        kwargs["priority"] = priority
    if action is not None:
        kwargs["action"] = action
    try:
        resp = client.update_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update rule") from exc
    return UpdateRuleResult(
        arn=resp.get("arn"),
        id=resp.get("id"),
        name=resp.get("name"),
        is_default=resp.get("isDefault"),
        match=resp.get("match"),
        priority=resp.get("priority"),
        action=resp.get("action"),
    )


def update_service_network_vpc_association(
    service_network_vpc_association_identifier: str,
    security_group_ids: list[str],
    region_name: str | None = None,
) -> UpdateServiceNetworkVpcAssociationResult:
    """Update service network vpc association.

    Args:
        service_network_vpc_association_identifier: Service network vpc association identifier.
        security_group_ids: Security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceNetworkVpcAssociationIdentifier"] = service_network_vpc_association_identifier
    kwargs["securityGroupIds"] = security_group_ids
    try:
        resp = client.update_service_network_vpc_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update service network vpc association") from exc
    return UpdateServiceNetworkVpcAssociationResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        created_by=resp.get("createdBy"),
        security_group_ids=resp.get("securityGroupIds"),
    )


def update_target_group(
    target_group_identifier: str,
    health_check: dict[str, Any],
    region_name: str | None = None,
) -> UpdateTargetGroupResult:
    """Update target group.

    Args:
        target_group_identifier: Target group identifier.
        health_check: Health check.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("vpc-lattice", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetGroupIdentifier"] = target_group_identifier
    kwargs["healthCheck"] = health_check
    try:
        resp = client.update_target_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update target group") from exc
    return UpdateTargetGroupResult(
        id=resp.get("id"),
        arn=resp.get("arn"),
        name=resp.get("name"),
        type_value=resp.get("type"),
        config=resp.get("config"),
        status=resp.get("status"),
    )
