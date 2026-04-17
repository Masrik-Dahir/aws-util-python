"""Native async App Runner utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time as _time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.app_runner import (
    _TERMINAL_STATUSES,
    AppRunnerAutoScalingConfig,
    AppRunnerConnection,
    AppRunnerObservabilityConfig,
    AppRunnerOperation,
    AppRunnerService,
    AppRunnerServiceSummary,
    AssociateCustomDomainResult,
    CreateVpcConnectorResult,
    CreateVpcIngressConnectionResult,
    DeleteAutoScalingConfigurationResult,
    DeleteConnectionResult,
    DeleteObservabilityConfigurationResult,
    DeleteVpcConnectorResult,
    DeleteVpcIngressConnectionResult,
    DescribeAutoScalingConfigurationResult,
    DescribeCustomDomainsResult,
    DescribeObservabilityConfigurationResult,
    DescribeVpcConnectorResult,
    DescribeVpcIngressConnectionResult,
    DisassociateCustomDomainResult,
    ListObservabilityConfigurationsResult,
    ListServicesForAutoScalingConfigurationResult,
    ListTagsForResourceResult,
    ListVpcConnectorsResult,
    ListVpcIngressConnectionsResult,
    UpdateDefaultAutoScalingConfigurationResult,
    UpdateVpcIngressConnectionResult,
    _parse_auto_scaling,
    _parse_connection,
    _parse_observability,
    _parse_operation,
    _parse_service,
    _parse_service_summary,
)
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
# Service operations
# ---------------------------------------------------------------------------


async def create_service(
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
    client = async_client("apprunner", region_name)
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
        resp = await client.call("CreateService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_service failed") from exc
    return _parse_service(resp["Service"])


async def describe_service(
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
    client = async_client("apprunner", region_name)
    try:
        resp = await client.call("DescribeService", ServiceArn=service_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


async def list_services(
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
    client = async_client("apprunner", region_name)
    try:
        items = await client.paginate("ListServices", "ServiceSummaryList")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_services failed") from exc
    return [_parse_service_summary(item) for item in items]


async def delete_service(
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
    client = async_client("apprunner", region_name)
    try:
        resp = await client.call("DeleteService", ServiceArn=service_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


async def update_service(
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
    client = async_client("apprunner", region_name)
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
        resp = await client.call("UpdateService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


async def pause_service(
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
    client = async_client("apprunner", region_name)
    try:
        resp = await client.call("PauseService", ServiceArn=service_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"pause_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


async def resume_service(
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
    client = async_client("apprunner", region_name)
    try:
        resp = await client.call("ResumeService", ServiceArn=service_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"resume_service failed for {service_arn!r}") from exc
    return _parse_service(resp["Service"])


# ---------------------------------------------------------------------------
# Auto-scaling configurations
# ---------------------------------------------------------------------------


async def create_auto_scaling_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "AutoScalingConfigurationName": auto_scaling_configuration_name,
        "MaxConcurrency": max_concurrency,
        "MaxSize": max_size,
        "MinSize": min_size,
    }
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateAutoScalingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_auto_scaling_configuration failed") from exc
    return _parse_auto_scaling(resp["AutoScalingConfiguration"])


async def list_auto_scaling_configurations(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if auto_scaling_configuration_name is not None:
        kwargs["AutoScalingConfigurationName"] = auto_scaling_configuration_name
    try:
        items = await client.paginate(
            "ListAutoScalingConfigurations",
            "AutoScalingConfigurationSummaryList",
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "list_auto_scaling_configurations failed") from exc
    return [_parse_auto_scaling(item) for item in items]


# ---------------------------------------------------------------------------
# Connections
# ---------------------------------------------------------------------------


async def create_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "ConnectionName": connection_name,
        "ProviderType": provider_type,
    }
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_connection failed") from exc
    return _parse_connection(resp["Connection"])


async def list_connections(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if connection_name is not None:
        kwargs["ConnectionName"] = connection_name
    try:
        items = await client.paginate("ListConnections", "ConnectionSummaryList", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_connections failed") from exc
    return [_parse_connection(item) for item in items]


# ---------------------------------------------------------------------------
# Observability
# ---------------------------------------------------------------------------


async def create_observability_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {
        "ObservabilityConfigurationName": observability_configuration_name,
    }
    if trace_configuration is not None:
        kwargs["TraceConfiguration"] = trace_configuration
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateObservabilityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_observability_configuration failed") from exc
    return _parse_observability(resp["ObservabilityConfiguration"])


# ---------------------------------------------------------------------------
# Deployments & operations
# ---------------------------------------------------------------------------


async def start_deployment(
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
    client = async_client("apprunner", region_name)
    try:
        resp = await client.call("StartDeployment", ServiceArn=service_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"start_deployment failed for {service_arn!r}") from exc
    return str(resp["OperationId"])


async def list_operations(
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
    client = async_client("apprunner", region_name)
    try:
        items = await client.paginate(
            "ListOperations",
            "OperationSummaryList",
            ServiceArn=service_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"list_operations failed for {service_arn!r}") from exc
    return [_parse_operation(item) for item in items]


# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------


async def wait_for_service(
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
        svc = await describe_service(service_arn, region_name=region_name)
        if svc.status in _TERMINAL_STATUSES:
            return svc
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Service {service_arn!r} did not reach a terminal "
                f"status within {timeout}s (current: {svc.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def associate_custom_domain(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["DomainName"] = domain_name
    if enable_www_subdomain is not None:
        kwargs["EnableWWWSubdomain"] = enable_www_subdomain
    try:
        resp = await client.call("AssociateCustomDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate custom domain") from exc
    return AssociateCustomDomainResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domain=resp.get("CustomDomain"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
    )


async def create_vpc_connector(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorName"] = vpc_connector_name
    kwargs["Subnets"] = subnets
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVpcConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc connector") from exc
    return CreateVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


async def create_vpc_ingress_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["VpcIngressConnectionName"] = vpc_ingress_connection_name
    kwargs["IngressVpcConfiguration"] = ingress_vpc_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVpcIngressConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc ingress connection") from exc
    return CreateVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


async def delete_auto_scaling_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if delete_all_revisions is not None:
        kwargs["DeleteAllRevisions"] = delete_all_revisions
    try:
        resp = await client.call("DeleteAutoScalingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete auto scaling configuration") from exc
    return DeleteAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


async def delete_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionArn"] = connection_arn
    try:
        resp = await client.call("DeleteConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return DeleteConnectionResult(
        connection=resp.get("Connection"),
    )


async def delete_observability_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ObservabilityConfigurationArn"] = observability_configuration_arn
    try:
        resp = await client.call("DeleteObservabilityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete observability configuration") from exc
    return DeleteObservabilityConfigurationResult(
        observability_configuration=resp.get("ObservabilityConfiguration"),
    )


async def delete_vpc_connector(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorArn"] = vpc_connector_arn
    try:
        resp = await client.call("DeleteVpcConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc connector") from exc
    return DeleteVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


async def delete_vpc_ingress_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    try:
        resp = await client.call("DeleteVpcIngressConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc ingress connection") from exc
    return DeleteVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


async def describe_auto_scaling_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    try:
        resp = await client.call("DescribeAutoScalingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe auto scaling configuration") from exc
    return DescribeAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


async def describe_custom_domains(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeCustomDomains", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe custom domains") from exc
    return DescribeCustomDomainsResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domains=resp.get("CustomDomains"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
        next_token=resp.get("NextToken"),
    )


async def describe_observability_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ObservabilityConfigurationArn"] = observability_configuration_arn
    try:
        resp = await client.call("DescribeObservabilityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe observability configuration") from exc
    return DescribeObservabilityConfigurationResult(
        observability_configuration=resp.get("ObservabilityConfiguration"),
    )


async def describe_vpc_connector(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcConnectorArn"] = vpc_connector_arn
    try:
        resp = await client.call("DescribeVpcConnector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc connector") from exc
    return DescribeVpcConnectorResult(
        vpc_connector=resp.get("VpcConnector"),
    )


async def describe_vpc_ingress_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    try:
        resp = await client.call("DescribeVpcIngressConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc ingress connection") from exc
    return DescribeVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )


async def disassociate_custom_domain(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceArn"] = service_arn
    kwargs["DomainName"] = domain_name
    try:
        resp = await client.call("DisassociateCustomDomain", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate custom domain") from exc
    return DisassociateCustomDomainResult(
        dns_target=resp.get("DNSTarget"),
        service_arn=resp.get("ServiceArn"),
        custom_domain=resp.get("CustomDomain"),
        vpc_dns_targets=resp.get("VpcDNSTargets"),
    )


async def list_observability_configurations(
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
    client = async_client("apprunner", region_name)
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
        resp = await client.call("ListObservabilityConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list observability configurations") from exc
    return ListObservabilityConfigurationsResult(
        observability_configuration_summary_list=resp.get("ObservabilityConfigurationSummaryList"),
        next_token=resp.get("NextToken"),
    )


async def list_services_for_auto_scaling_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListServicesForAutoScalingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list services for auto scaling configuration") from exc
    return ListServicesForAutoScalingConfigurationResult(
        service_arn_list=resp.get("ServiceArnList"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_vpc_connectors(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListVpcConnectors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list vpc connectors") from exc
    return ListVpcConnectorsResult(
        vpc_connectors=resp.get("VpcConnectors"),
        next_token=resp.get("NextToken"),
    )


async def list_vpc_ingress_connections(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListVpcIngressConnections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list vpc ingress connections") from exc
    return ListVpcIngressConnectionsResult(
        vpc_ingress_connection_summary_list=resp.get("VpcIngressConnectionSummaryList"),
        next_token=resp.get("NextToken"),
    )


async def tag_resource(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_default_auto_scaling_configuration(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoScalingConfigurationArn"] = auto_scaling_configuration_arn
    try:
        resp = await client.call("UpdateDefaultAutoScalingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update default auto scaling configuration") from exc
    return UpdateDefaultAutoScalingConfigurationResult(
        auto_scaling_configuration=resp.get("AutoScalingConfiguration"),
    )


async def update_vpc_ingress_connection(
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
    client = async_client("apprunner", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VpcIngressConnectionArn"] = vpc_ingress_connection_arn
    kwargs["IngressVpcConfiguration"] = ingress_vpc_configuration
    try:
        resp = await client.call("UpdateVpcIngressConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update vpc ingress connection") from exc
    return UpdateVpcIngressConnectionResult(
        vpc_ingress_connection=resp.get("VpcIngressConnection"),
    )
