"""aws_util.app_runner -- AWS App Runner utilities.

Provides high-level helpers for managing App Runner services, auto-scaling
configurations, connections, observability configurations, deployments,
and operations.
"""

from __future__ import annotations

import time as _time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AppRunnerAutoScalingConfig",
    "AppRunnerConnection",
    "AppRunnerObservabilityConfig",
    "AppRunnerOperation",
    "AppRunnerService",
    "AppRunnerServiceSummary",
    "AssociateCustomDomainResult",
    "CreateVpcConnectorResult",
    "CreateVpcIngressConnectionResult",
    "DeleteAutoScalingConfigurationResult",
    "DeleteConnectionResult",
    "DeleteObservabilityConfigurationResult",
    "DeleteVpcConnectorResult",
    "DeleteVpcIngressConnectionResult",
    "DescribeAutoScalingConfigurationResult",
    "DescribeCustomDomainsResult",
    "DescribeObservabilityConfigurationResult",
    "DescribeVpcConnectorResult",
    "DescribeVpcIngressConnectionResult",
    "DisassociateCustomDomainResult",
    "ListObservabilityConfigurationsResult",
    "ListServicesForAutoScalingConfigurationResult",
    "ListTagsForResourceResult",
    "ListVpcConnectorsResult",
    "ListVpcIngressConnectionsResult",
    "UpdateDefaultAutoScalingConfigurationResult",
    "UpdateVpcIngressConnectionResult",
    "associate_custom_domain",
    "create_auto_scaling_configuration",
    "create_connection",
    "create_observability_configuration",
    "create_service",
    "create_vpc_connector",
    "create_vpc_ingress_connection",
    "delete_auto_scaling_configuration",
    "delete_connection",
    "delete_observability_configuration",
    "delete_service",
    "delete_vpc_connector",
    "delete_vpc_ingress_connection",
    "describe_auto_scaling_configuration",
    "describe_custom_domains",
    "describe_observability_configuration",
    "describe_service",
    "describe_vpc_connector",
    "describe_vpc_ingress_connection",
    "disassociate_custom_domain",
    "list_auto_scaling_configurations",
    "list_connections",
    "list_observability_configurations",
    "list_operations",
    "list_services",
    "list_services_for_auto_scaling_configuration",
    "list_tags_for_resource",
    "list_vpc_connectors",
    "list_vpc_ingress_connections",
    "pause_service",
    "resume_service",
    "start_deployment",
    "tag_resource",
    "untag_resource",
    "update_default_auto_scaling_configuration",
    "update_service",
    "update_vpc_ingress_connection",
    "wait_for_service",
]

# ---------------------------------------------------------------------------
# Terminal statuses used by wait_for_service
# ---------------------------------------------------------------------------

_TERMINAL_STATUSES: frozenset[str] = frozenset(
    {
        "RUNNING",
        "CREATE_FAILED",
        "DELETE_FAILED",
        "DELETED",
        "PAUSED",
    }
)

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AppRunnerService(BaseModel):
    """Full description of an App Runner service."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    service_arn: str
    service_name: str
    service_id: str
    service_url: str | None = None
    status: str
    auto_scaling_configuration_arn: str | None = None
    source_type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AppRunnerServiceSummary(BaseModel):
    """Lightweight service summary returned by ``list_services``."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    service_arn: str
    service_name: str
    service_id: str
    status: str
    service_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AppRunnerAutoScalingConfig(BaseModel):
    """Auto-scaling configuration summary."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    auto_scaling_configuration_arn: str
    auto_scaling_configuration_name: str
    auto_scaling_configuration_revision: int
    max_concurrency: int | None = None
    max_size: int | None = None
    min_size: int | None = None
    status: str | None = None


class AppRunnerConnection(BaseModel):
    """Source connection summary."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    connection_arn: str
    connection_name: str
    provider_type: str
    status: str
    created_at: str | None = None


class AppRunnerObservabilityConfig(BaseModel):
    """Observability configuration summary."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    observability_configuration_arn: str
    observability_configuration_name: str
    observability_configuration_revision: int
    trace_configuration: dict[str, Any] | None = None
    status: str | None = None


class AppRunnerOperation(BaseModel):
    """Summary of an App Runner operation."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    id: str | None = None
    type: str | None = None
    status: str | None = None
    target_arn: str | None = None
    started_at: str | None = None
    ended_at: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_service(data: dict[str, Any]) -> AppRunnerService:
    """Parse a raw service dict into an :class:`AppRunnerService`."""
    return AppRunnerService(
        service_arn=data["ServiceArn"],
        service_name=data["ServiceName"],
        service_id=data["ServiceId"],
        service_url=data.get("ServiceUrl"),
        status=data["Status"],
        auto_scaling_configuration_arn=data.get("AutoScalingConfigurationSummary", {}).get(
            "AutoScalingConfigurationArn"
        ),
        source_type=data.get("SourceConfiguration", {})
        .get("CodeRepository", {})
        .get("SourceCodeVersion", {})
        .get("Type")
        or data.get("SourceConfiguration", {}).get("ImageRepository", {}).get("ImageIdentifier"),
        created_at=str(data["CreatedAt"]) if "CreatedAt" in data else None,
        updated_at=str(data["UpdatedAt"]) if "UpdatedAt" in data else None,
    )


def _parse_service_summary(data: dict[str, Any]) -> AppRunnerServiceSummary:
    """Parse a raw service summary dict."""
    return AppRunnerServiceSummary(
        service_arn=data["ServiceArn"],
        service_name=data["ServiceName"],
        service_id=data["ServiceId"],
        status=data["Status"],
        service_url=data.get("ServiceUrl"),
        created_at=str(data["CreatedAt"]) if "CreatedAt" in data else None,
        updated_at=str(data["UpdatedAt"]) if "UpdatedAt" in data else None,
    )


def _parse_auto_scaling(data: dict[str, Any]) -> AppRunnerAutoScalingConfig:
    """Parse an auto-scaling configuration dict."""
    return AppRunnerAutoScalingConfig(
        auto_scaling_configuration_arn=data["AutoScalingConfigurationArn"],
        auto_scaling_configuration_name=data["AutoScalingConfigurationName"],
        auto_scaling_configuration_revision=data["AutoScalingConfigurationRevision"],
        max_concurrency=data.get("MaxConcurrency"),
        max_size=data.get("MaxSize"),
        min_size=data.get("MinSize"),
        status=data.get("Status"),
    )


def _parse_connection(data: dict[str, Any]) -> AppRunnerConnection:
    """Parse a connection summary dict."""
    return AppRunnerConnection(
        connection_arn=data["ConnectionArn"],
        connection_name=data["ConnectionName"],
        provider_type=data["ProviderType"],
        status=data["Status"],
        created_at=str(data["CreatedAt"]) if "CreatedAt" in data else None,
    )


def _parse_observability(data: dict[str, Any]) -> AppRunnerObservabilityConfig:
    """Parse an observability configuration dict."""
    return AppRunnerObservabilityConfig(
        observability_configuration_arn=data["ObservabilityConfigurationArn"],
        observability_configuration_name=data["ObservabilityConfigurationName"],
        observability_configuration_revision=data["ObservabilityConfigurationRevision"],
        trace_configuration=data.get("TraceConfiguration"),
        status=data.get("Status"),
    )


def _parse_operation(data: dict[str, Any]) -> AppRunnerOperation:
    """Parse an operation summary dict."""
    return AppRunnerOperation(
        id=data.get("Id"),
        type=data.get("Type"),
        status=data.get("Status"),
        target_arn=data.get("TargetArn"),
        started_at=str(data["StartedAt"]) if "StartedAt" in data else None,
        ended_at=str(data["EndedAt"]) if "EndedAt" in data else None,
    )


# ---------------------------------------------------------------------------
# Service operations
# ---------------------------------------------------------------------------


def create_service(
    service_name: str,
    source_configuration: dict[str, Any],
    instance_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    auto_scaling_configuration_arn: str | None = None,
    health_check_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> AppRunnerService:
    """Create a new App Runner service.

    Args:
        service_name: Human-readable name for the service.
        source_configuration: Source configuration dict (image or code).
        instance_configuration: Optional vCPU / memory settings.
        tags: Optional list of ``{"Key": "...", "Value": "..."}`` dicts.
        auto_scaling_configuration_arn: ARN of an auto-scaling config.
        health_check_configuration: Optional health-check settings.
        region_name: AWS region override.

    Returns:
        The created :class:`AppRunnerService`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "ServiceName": service_name,
        "SourceConfiguration": source_configuration,
    }
    if instance_configuration is not None:
        kwargs["InstanceConfiguration"] = instance_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    if auto_scaling_configuration_arn is not None:
        kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if health_check_configuration is not None:
        kwargs["HealthCheckConfiguration"] = health_check_configuration

    try:
        resp = client.create_service(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_service failed") from exc
    return _parse_service(resp["Service"])


def describe_service(
    service_arn: str,
    region_name: str | None = None,
) -> AppRunnerService:
    """Describe an App Runner service.

    Args:
        service_arn: ARN of the service.
        region_name: AWS region override.

    Returns:
        The :class:`AppRunnerService`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    try:
        resp = client.describe_service(ServiceArn=service_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


def list_services(
    region_name: str | None = None,
) -> list[AppRunnerServiceSummary]:
    """List all App Runner services in the account/region.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`AppRunnerServiceSummary` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    summaries: list[AppRunnerServiceSummary] = []
    try:
        kwargs: dict[str, Any] = {}
        while True:
            resp = client.list_services(**kwargs)
            for item in resp.get("ServiceSummaryList", []):
                summaries.append(_parse_service_summary(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_services failed") from exc
    return summaries


def delete_service(
    service_arn: str,
    region_name: str | None = None,
) -> AppRunnerService:
    """Delete an App Runner service.

    Args:
        service_arn: ARN of the service to delete.
        region_name: AWS region override.

    Returns:
        The :class:`AppRunnerService` in its transitional state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    try:
        resp = client.delete_service(ServiceArn=service_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


def update_service(
    service_arn: str,
    source_configuration: dict[str, Any] | None = None,
    instance_configuration: dict[str, Any] | None = None,
    auto_scaling_configuration_arn: str | None = None,
    health_check_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> AppRunnerService:
    """Update an existing App Runner service.

    Args:
        service_arn: ARN of the service to update.
        source_configuration: Updated source configuration.
        instance_configuration: Updated instance configuration.
        auto_scaling_configuration_arn: Updated auto-scaling ARN.
        health_check_configuration: Updated health-check settings.
        region_name: AWS region override.

    Returns:
        The updated :class:`AppRunnerService`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {"ServiceArn": service_arn}
    if source_configuration is not None:
        kwargs["SourceConfiguration"] = source_configuration
    if instance_configuration is not None:
        kwargs["InstanceConfiguration"] = instance_configuration
    if auto_scaling_configuration_arn is not None:
        kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if health_check_configuration is not None:
        kwargs["HealthCheckConfiguration"] = health_check_configuration

    try:
        resp = client.update_service(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


def pause_service(
    service_arn: str,
    region_name: str | None = None,
) -> AppRunnerService:
    """Pause a running App Runner service.

    Args:
        service_arn: ARN of the service to pause.
        region_name: AWS region override.

    Returns:
        The :class:`AppRunnerService` in its transitional state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    try:
        resp = client.pause_service(ServiceArn=service_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"pause_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


def resume_service(
    service_arn: str,
    region_name: str | None = None,
) -> AppRunnerService:
    """Resume a paused App Runner service.

    Args:
        service_arn: ARN of the service to resume.
        region_name: AWS region override.

    Returns:
        The :class:`AppRunnerService` in its transitional state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    try:
        resp = client.resume_service(ServiceArn=service_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"resume_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


# ---------------------------------------------------------------------------
# Auto-scaling configurations
# ---------------------------------------------------------------------------


def create_auto_scaling_configuration(
    auto_scaling_configuration_name: str,
    max_concurrency: int = 100,
    max_size: int = 25,
    min_size: int = 1,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> AppRunnerAutoScalingConfig:
    """Create an auto-scaling configuration.

    Args:
        auto_scaling_configuration_name: Name for the configuration.
        max_concurrency: Maximum concurrent requests per instance.
        max_size: Maximum number of instances.
        min_size: Minimum number of instances.
        tags: Optional tags.
        region_name: AWS region override.

    Returns:
        The created :class:`AppRunnerAutoScalingConfig`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingConfigurationName": auto_scaling_configuration_name,
        "MaxConcurrency": max_concurrency,
        "MaxSize": max_size,
        "MinSize": min_size,
    }
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = client.create_auto_scaling_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_auto_scaling_configuration failed") from exc
    return _parse_auto_scaling(resp["AutoScalingConfiguration"])


def list_auto_scaling_configurations(
    auto_scaling_configuration_name: str | None = None,
    region_name: str | None = None,
) -> list[AppRunnerAutoScalingConfig]:
    """List auto-scaling configurations.

    Args:
        auto_scaling_configuration_name: Optional name filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`AppRunnerAutoScalingConfig` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    configs: list[AppRunnerAutoScalingConfig] = []
    try:
        kwargs: dict[str, Any] = {}
        if auto_scaling_configuration_name is not None:
            kwargs["AutoScalingConfigurationName"] = auto_scaling_configuration_name
        while True:
            resp = client.list_auto_scaling_configurations(**kwargs)
            for item in resp.get("AutoScalingConfigurationSummaryList", []):
                configs.append(_parse_auto_scaling(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_auto_scaling_configurations failed") from exc
    return configs


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------


def create_connection(
    connection_name: str,
    provider_type: str = "GITHUB",
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> AppRunnerConnection:
    """Create a source connection.

    Args:
        connection_name: Name for the connection.
        provider_type: Provider type (``"GITHUB"`` or ``"BITBUCKET"``).
        tags: Optional tags.
        region_name: AWS region override.

    Returns:
        The created :class:`AppRunnerConnection`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "ConnectionName": connection_name,
        "ProviderType": provider_type,
    }
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = client.create_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_connection failed") from exc
    return _parse_connection(resp["Connection"])


def list_connections(
    connection_name: str | None = None,
    region_name: str | None = None,
) -> list[AppRunnerConnection]:
    """List source connections.

    Args:
        connection_name: Optional name filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`AppRunnerConnection` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    connections: list[AppRunnerConnection] = []
    try:
        kwargs: dict[str, Any] = {}
        if connection_name is not None:
            kwargs["ConnectionName"] = connection_name
        while True:
            resp = client.list_connections(**kwargs)
            for item in resp.get("ConnectionSummaryList", []):
                connections.append(_parse_connection(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_connections failed") from exc
    return connections


# ---------------------------------------------------------------------------
# Observability
# ---------------------------------------------------------------------------


def create_observability_configuration(
    observability_configuration_name: str,
    trace_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> AppRunnerObservabilityConfig:
    """Create an observability configuration.

    Args:
        observability_configuration_name: Name for the configuration.
        trace_configuration: Optional trace settings (e.g. X-Ray vendor).
        tags: Optional tags.
        region_name: AWS region override.

    Returns:
        The created :class:`AppRunnerObservabilityConfig`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "ObservabilityConfigurationName": observability_configuration_name,
    }
    if trace_configuration is not None:
        kwargs["TraceConfiguration"] = trace_configuration
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = client.create_observability_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_observability_configuration failed") from exc
    return _parse_observability(resp["ObservabilityConfiguration"])


# ---------------------------------------------------------------------------
# Deployments & operations
# ---------------------------------------------------------------------------


def start_deployment(
    service_arn: str,
    region_name: str | None = None,
) -> str:
    """Start a manual deployment for the service.

    Args:
        service_arn: ARN of the service.
        region_name: AWS region override.

    Returns:
        The operation ID for the deployment.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    try:
        resp = client.start_deployment(ServiceArn=service_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_deployment failed for {service_arn!r}") from exc
    return str(resp["OperationId"])


def list_operations(
    service_arn: str,
    region_name: str | None = None,
) -> list[AppRunnerOperation]:
    """List operations for an App Runner service.

    Args:
        service_arn: ARN of the service.
        region_name: AWS region override.

    Returns:
        A list of :class:`AppRunnerOperation` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    ops: list[AppRunnerOperation] = []
    try:
        kwargs: dict[str, Any] = {"ServiceArn": service_arn}
        while True:
            resp = client.list_operations(**kwargs)
            for item in resp.get("OperationSummaryList", []):
                ops.append(_parse_operation(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_operations failed for {service_arn!r}") from exc
    return ops


# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------


def wait_for_service(
    service_arn: str,
    timeout: float = 600.0,
    poll_interval: float = 10.0,
    region_name: str | None = None,
) -> AppRunnerService:
    """Poll until an App Runner service reaches a terminal status.

    Terminal statuses: ``RUNNING``, ``CREATE_FAILED``, ``DELETE_FAILED``,
    ``DELETED``, ``PAUSED``.

    Args:
        service_arn: ARN of the service to monitor.
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between polls (default ``10``).
        region_name: AWS region override.

    Returns:
        The :class:`AppRunnerService` in a terminal status.

    Raises:
        TimeoutError: If the service does not reach a terminal status in
            time.
        RuntimeError: If the describe call fails.
    """
    deadline = _time.monotonic() + timeout
    while True:
        svc = describe_service(service_arn, region_name=region_name)
        if svc.status in _TERMINAL_STATUSES:
            return svc
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Service {service_arn!r} did not reach a terminal status "
                f"within {timeout}s (current: {svc.status!r})"
            )
        _time.sleep(poll_interval)


class AssociateCustomDomainResult(BaseModel):
    """Result of associate_custom_domain."""

    model_config = ConfigDict(frozen=True)

    dns_target: str | None = None
    service_arn: str | None = None
    custom_domain: dict[str, Any] | None = None
    vpc_dns_targets: list[dict[str, Any]] | None = None


class CreateVpcConnectorResult(BaseModel):
    """Result of create_vpc_connector."""

    model_config = ConfigDict(frozen=True)

    vpc_connector: dict[str, Any] | None = None


class CreateVpcIngressConnectionResult(BaseModel):
    """Result of create_vpc_ingress_connection."""

    model_config = ConfigDict(frozen=True)

    vpc_ingress_connection: dict[str, Any] | None = None


class DeleteAutoScalingConfigurationResult(BaseModel):
    """Result of delete_auto_scaling_configuration."""

    model_config = ConfigDict(frozen=True)

    auto_scaling_configuration: dict[str, Any] | None = None


class DeleteConnectionResult(BaseModel):
    """Result of delete_connection."""

    model_config = ConfigDict(frozen=True)

    connection: dict[str, Any] | None = None


class DeleteObservabilityConfigurationResult(BaseModel):
    """Result of delete_observability_configuration."""

    model_config = ConfigDict(frozen=True)

    observability_configuration: dict[str, Any] | None = None


class DeleteVpcConnectorResult(BaseModel):
    """Result of delete_vpc_connector."""

    model_config = ConfigDict(frozen=True)

    vpc_connector: dict[str, Any] | None = None


class DeleteVpcIngressConnectionResult(BaseModel):
    """Result of delete_vpc_ingress_connection."""

    model_config = ConfigDict(frozen=True)

    vpc_ingress_connection: dict[str, Any] | None = None


class DescribeAutoScalingConfigurationResult(BaseModel):
    """Result of describe_auto_scaling_configuration."""

    model_config = ConfigDict(frozen=True)

    auto_scaling_configuration: dict[str, Any] | None = None


class DescribeCustomDomainsResult(BaseModel):
    """Result of describe_custom_domains."""

    model_config = ConfigDict(frozen=True)

    dns_target: str | None = None
    service_arn: str | None = None
    custom_domains: list[dict[str, Any]] | None = None
    vpc_dns_targets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeObservabilityConfigurationResult(BaseModel):
    """Result of describe_observability_configuration."""

    model_config = ConfigDict(frozen=True)

    observability_configuration: dict[str, Any] | None = None


class DescribeVpcConnectorResult(BaseModel):
    """Result of describe_vpc_connector."""

    model_config = ConfigDict(frozen=True)

    vpc_connector: dict[str, Any] | None = None


class DescribeVpcIngressConnectionResult(BaseModel):
    """Result of describe_vpc_ingress_connection."""

    model_config = ConfigDict(frozen=True)

    vpc_ingress_connection: dict[str, Any] | None = None


class DisassociateCustomDomainResult(BaseModel):
    """Result of disassociate_custom_domain."""

    model_config = ConfigDict(frozen=True)

    dns_target: str | None = None
    service_arn: str | None = None
    custom_domain: dict[str, Any] | None = None
    vpc_dns_targets: list[dict[str, Any]] | None = None


class ListObservabilityConfigurationsResult(BaseModel):
    """Result of list_observability_configurations."""

    model_config = ConfigDict(frozen=True)

    observability_configuration_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServicesForAutoScalingConfigurationResult(BaseModel):
    """Result of list_services_for_auto_scaling_configuration."""

    model_config = ConfigDict(frozen=True)

    service_arn_list: list[str] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class ListVpcConnectorsResult(BaseModel):
    """Result of list_vpc_connectors."""

    model_config = ConfigDict(frozen=True)

    vpc_connectors: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListVpcIngressConnectionsResult(BaseModel):
    """Result of list_vpc_ingress_connections."""

    model_config = ConfigDict(frozen=True)

    vpc_ingress_connection_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class UpdateDefaultAutoScalingConfigurationResult(BaseModel):
    """Result of update_default_auto_scaling_configuration."""

    model_config = ConfigDict(frozen=True)

    auto_scaling_configuration: dict[str, Any] | None = None


class UpdateVpcIngressConnectionResult(BaseModel):
    """Result of update_vpc_ingress_connection."""

    model_config = ConfigDict(frozen=True)

    vpc_ingress_connection: dict[str, Any] | None = None


def associate_custom_domain(
    service_arn: str,
    domain_name: str,
    *,
    enable_www_subdomain: bool | None = None,
    region_name: str | None = None,
) -> AssociateCustomDomainResult:
    """Associate custom domain.

    Args:
        service_arn: Service arn.
        domain_name: Domain name.
        enable_www_subdomain: Enable www subdomain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["DomainName"] = domain_name
    if enable_www_subdomain is not None:
        kwargs["EnableWWWSubdomain"] = enable_www_subdomain
    try:
        resp = client.associate_custom_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate custom domain") from exc
    return AssociateCustomDomainResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domain=resp.get("CustomDomain"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
    )


def create_vpc_connector(
    vpc_connector_name: str,
    subnets: list[str],
    *,
    security_groups: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateVpcConnectorResult:
    """Create vpc connector.

    Args:
        vpc_connector_name: Vpc connector name.
        subnets: Subnets.
        security_groups: Security groups.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorName"] = vpc_connector_name
    kwargs["Subnets"] = subnets
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_vpc_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vpc connector") from exc
    return CreateVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


def create_vpc_ingress_connection(
    service_arn: str,
    vpc_ingress_connection_name: str,
    ingress_vpc_configuration: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateVpcIngressConnectionResult:
    """Create vpc ingress connection.

    Args:
        service_arn: Service arn.
        vpc_ingress_connection_name: Vpc ingress connection name.
        ingress_vpc_configuration: Ingress vpc configuration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["VpcIngressConnectionName"] = vpc_ingress_connection_name
    kwargs["IngressVpcConfiguration"] = ingress_vpc_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_vpc_ingress_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vpc ingress connection") from exc
    return CreateVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


def delete_auto_scaling_configuration(
    auto_scaling_configuration_arn: str,
    *,
    delete_all_revisions: bool | None = None,
    region_name: str | None = None,
) -> DeleteAutoScalingConfigurationResult:
    """Delete auto scaling configuration.

    Args:
        auto_scaling_configuration_arn: Auto scaling configuration arn.
        delete_all_revisions: Delete all revisions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if delete_all_revisions is not None:
        kwargs["DeleteAllRevisions"] = delete_all_revisions
    try:
        resp = client.delete_auto_scaling_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete auto scaling configuration") from exc
    return DeleteAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


def delete_connection(
    connection_arn: str,
    region_name: str | None = None,
) -> DeleteConnectionResult:
    """Delete connection.

    Args:
        connection_arn: Connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionArn"] = connection_arn
    try:
        resp = client.delete_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return DeleteConnectionResult(
        connection=resp.get("Connection"),
    )


def delete_observability_configuration(
    observability_configuration_arn: str,
    region_name: str | None = None,
) -> DeleteObservabilityConfigurationResult:
    """Delete observability configuration.

    Args:
        observability_configuration_arn: Observability configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ObservabilityConfigurationArn"] = observability_configuration_arn
    try:
        resp = client.delete_observability_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete observability configuration") from exc
    return DeleteObservabilityConfigurationResult(
        observability_configuration=resp.get("ObservabilityConfiguration"),
    )


def delete_vpc_connector(
    vpc_connector_arn: str,
    region_name: str | None = None,
) -> DeleteVpcConnectorResult:
    """Delete vpc connector.

    Args:
        vpc_connector_arn: Vpc connector arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorArn"] = vpc_connector_arn
    try:
        resp = client.delete_vpc_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc connector") from exc
    return DeleteVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


def delete_vpc_ingress_connection(
    vpc_ingress_connection_arn: str,
    region_name: str | None = None,
) -> DeleteVpcIngressConnectionResult:
    """Delete vpc ingress connection.

    Args:
        vpc_ingress_connection_arn: Vpc ingress connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    try:
        resp = client.delete_vpc_ingress_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc ingress connection") from exc
    return DeleteVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


def describe_auto_scaling_configuration(
    auto_scaling_configuration_arn: str,
    region_name: str | None = None,
) -> DescribeAutoScalingConfigurationResult:
    """Describe auto scaling configuration.

    Args:
        auto_scaling_configuration_arn: Auto scaling configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    try:
        resp = client.describe_auto_scaling_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe auto scaling configuration") from exc
    return DescribeAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


def describe_custom_domains(
    service_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeCustomDomainsResult:
    """Describe custom domains.

    Args:
        service_arn: Service arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_custom_domains(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe custom domains") from exc
    return DescribeCustomDomainsResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domains=resp.get("CustomDomains"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
        next_token=resp.get("NextToken"),
    )


def describe_observability_configuration(
    observability_configuration_arn: str,
    region_name: str | None = None,
) -> DescribeObservabilityConfigurationResult:
    """Describe observability configuration.

    Args:
        observability_configuration_arn: Observability configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ObservabilityConfigurationArn"] = observability_configuration_arn
    try:
        resp = client.describe_observability_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe observability configuration") from exc
    return DescribeObservabilityConfigurationResult(
        observability_configuration=resp.get("ObservabilityConfiguration"),
    )


def describe_vpc_connector(
    vpc_connector_arn: str,
    region_name: str | None = None,
) -> DescribeVpcConnectorResult:
    """Describe vpc connector.

    Args:
        vpc_connector_arn: Vpc connector arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorArn"] = vpc_connector_arn
    try:
        resp = client.describe_vpc_connector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc connector") from exc
    return DescribeVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


def describe_vpc_ingress_connection(
    vpc_ingress_connection_arn: str,
    region_name: str | None = None,
) -> DescribeVpcIngressConnectionResult:
    """Describe vpc ingress connection.

    Args:
        vpc_ingress_connection_arn: Vpc ingress connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    try:
        resp = client.describe_vpc_ingress_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc ingress connection") from exc
    return DescribeVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


def disassociate_custom_domain(
    service_arn: str,
    domain_name: str,
    region_name: str | None = None,
) -> DisassociateCustomDomainResult:
    """Disassociate custom domain.

    Args:
        service_arn: Service arn.
        domain_name: Domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["DomainName"] = domain_name
    try:
        resp = client.disassociate_custom_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate custom domain") from exc
    return DisassociateCustomDomainResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domain=resp.get("CustomDomain"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
    )


def list_observability_configurations(
    *,
    observability_configuration_name: str | None = None,
    latest_only: bool | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListObservabilityConfigurationsResult:
    """List observability configurations.

    Args:
        observability_configuration_name: Observability configuration name.
        latest_only: Latest only.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if observability_configuration_name is not None:
        kwargs["ObservabilityConfigurationName"] = observability_configuration_name
    if latest_only is not None:
        kwargs["LatestOnly"] = latest_only
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_observability_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list observability configurations") from exc
    return ListObservabilityConfigurationsResult(
        observability_configuration_summary_list=resp.get("ObservabilityConfigurationSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_services_for_auto_scaling_configuration(
    auto_scaling_configuration_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListServicesForAutoScalingConfigurationResult:
    """List services for auto scaling configuration.

    Args:
        auto_scaling_configuration_arn: Auto scaling configuration arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_services_for_auto_scaling_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list services for auto scaling configuration") from exc
    return ListServicesForAutoScalingConfigurationResult(
        service_arn_list=resp.get("ServiceArnList"),
        next_token=resp.get("NextToken"),
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
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_vpc_connectors(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListVpcConnectorsResult:
    """List vpc connectors.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_vpc_connectors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list vpc connectors") from exc
    return ListVpcConnectorsResult(
        vpc_connectors=resp.get("VpcConnectors"),
        next_token=resp.get("NextToken"),
    )


def list_vpc_ingress_connections(
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListVpcIngressConnectionsResult:
    """List vpc ingress connections.

    Args:
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_vpc_ingress_connections(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list vpc ingress connections") from exc
    return ListVpcIngressConnectionsResult(
        vpc_ingress_connection_summary_list=resp.get("VpcIngressConnectionSummaryList"),
        next_token=resp.get("NextToken"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
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
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
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
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_default_auto_scaling_configuration(
    auto_scaling_configuration_arn: str,
    region_name: str | None = None,
) -> UpdateDefaultAutoScalingConfigurationResult:
    """Update default auto scaling configuration.

    Args:
        auto_scaling_configuration_arn: Auto scaling configuration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    try:
        resp = client.update_default_auto_scaling_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update default auto scaling configuration") from exc
    return UpdateDefaultAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


def update_vpc_ingress_connection(
    vpc_ingress_connection_arn: str,
    ingress_vpc_configuration: dict[str, Any],
    region_name: str | None = None,
) -> UpdateVpcIngressConnectionResult:
    """Update vpc ingress connection.

    Args:
        vpc_ingress_connection_arn: Vpc ingress connection arn.
        ingress_vpc_configuration: Ingress vpc configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    kwargs["IngressVpcConfiguration"] = ingress_vpc_configuration
    try:
        resp = client.update_vpc_ingress_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update vpc ingress connection") from exc
    return UpdateVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )
