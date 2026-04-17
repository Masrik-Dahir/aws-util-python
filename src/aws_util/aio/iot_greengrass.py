"""Native async IoT Greengrass V2 utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.iot_greengrass import (
    AssociateServiceRoleToAccountResult,
    BatchAssociateClientDeviceWithCoreDeviceResult,
    BatchDisassociateClientDeviceFromCoreDeviceResult,
    ComponentResult,
    DeploymentResult,
    DisassociateServiceRoleFromAccountResult,
    GetComponentVersionArtifactResult,
    GetConnectivityInfoResult,
    GetCoreDeviceResult,
    GetServiceRoleForAccountResult,
    InstalledComponentResult,
    ListClientDevicesAssociatedWithCoreDeviceResult,
    ListComponentVersionsResult,
    ListCoreDevicesResult,
    ResolveComponentCandidatesResult,
    UpdateConnectivityInfoResult,
    _parse_component,
    _parse_deployment,
    _parse_installed_component,
)

__all__ = [
    "AssociateServiceRoleToAccountResult",
    "BatchAssociateClientDeviceWithCoreDeviceResult",
    "BatchDisassociateClientDeviceFromCoreDeviceResult",
    "ComponentResult",
    "DeploymentResult",
    "DisassociateServiceRoleFromAccountResult",
    "GetComponentVersionArtifactResult",
    "GetConnectivityInfoResult",
    "GetCoreDeviceResult",
    "GetServiceRoleForAccountResult",
    "InstalledComponentResult",
    "ListClientDevicesAssociatedWithCoreDeviceResult",
    "ListComponentVersionsResult",
    "ListCoreDevicesResult",
    "ResolveComponentCandidatesResult",
    "UpdateConnectivityInfoResult",
    "associate_service_role_to_account",
    "batch_associate_client_device_with_core_device",
    "batch_disassociate_client_device_from_core_device",
    "cancel_deployment",
    "create_component_version",
    "create_deployment",
    "delete_component",
    "delete_core_device",
    "delete_deployment",
    "describe_component",
    "disassociate_service_role_from_account",
    "get_component",
    "get_component_version_artifact",
    "get_connectivity_info",
    "get_core_device",
    "get_deployment",
    "get_service_role_for_account",
    "list_client_devices_associated_with_core_device",
    "list_component_versions",
    "list_components",
    "list_core_devices",
    "list_deployments",
    "list_effective_deployments",
    "list_installed_components",
    "list_tags_for_resource",
    "resolve_component_candidates",
    "tag_resource",
    "untag_resource",
    "update_connectivity_info",
]


# ---------------------------------------------------------------------------
# Component operations
# ---------------------------------------------------------------------------


async def create_component_version(
    *,
    inline_recipe: str | None = None,
    lambda_function_recipe_source: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ComponentResult:
    """Create a new Greengrass component version.

    Args:
        inline_recipe: A YAML or JSON recipe as a string.
        lambda_function_recipe_source: Lambda recipe source dict.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`ComponentResult` for the new component version.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    if inline_recipe is not None:
        kwargs["inlineRecipe"] = inline_recipe.encode()
    if lambda_function_recipe_source is not None:
        kwargs["lambdaFunction"] = lambda_function_recipe_source
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateComponentVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_component_version failed") from exc
    return _parse_component(resp)


async def describe_component(
    arn: str,
    *,
    region_name: str | None = None,
) -> ComponentResult:
    """Describe a Greengrass component.

    Args:
        arn: The component version ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ComponentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        resp = await client.call("DescribeComponent", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_component failed") from exc
    return _parse_component(resp)


async def list_components(
    *,
    region_name: str | None = None,
) -> list[ComponentResult]:
    """List all Greengrass components.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ComponentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    results: list[ComponentResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListComponents", **kwargs)
            for comp in resp.get("components", []):
                results.append(_parse_component(comp))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_components failed") from exc
    return results


async def delete_component(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Greengrass component version.

    Args:
        arn: The component version ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        await client.call("DeleteComponent", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_component failed") from exc


async def get_component(
    arn: str,
    *,
    recipe_output_format: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Get the recipe for a Greengrass component version.

    Args:
        arn: The component version ARN.
        recipe_output_format: ``"JSON"`` or ``"YAML"``.
        region_name: AWS region override.

    Returns:
        The full API response dict including ``recipe`` and
        ``recipeOutputFormat``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {"arn": arn}
    if recipe_output_format is not None:
        kwargs["recipeOutputFormat"] = recipe_output_format
    try:
        resp = await client.call("GetComponent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_component failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Deployment operations
# ---------------------------------------------------------------------------


async def create_deployment(
    target_arn: str,
    *,
    deployment_name: str | None = None,
    components: dict[str, Any] | None = None,
    deployment_policies: dict[str, Any] | None = None,
    iot_job_configuration: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DeploymentResult:
    """Create a Greengrass deployment.

    Args:
        target_arn: The target thing or thing-group ARN.
        deployment_name: Human-readable name.
        components: Component configuration map.
        deployment_policies: Deployment policy configuration.
        iot_job_configuration: IoT job configuration.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentResult` for the new deployment.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {"targetArn": target_arn}
    if deployment_name is not None:
        kwargs["deploymentName"] = deployment_name
    if components is not None:
        kwargs["components"] = components
    if deployment_policies is not None:
        kwargs["deploymentPolicies"] = deployment_policies
    if iot_job_configuration is not None:
        kwargs["iotJobConfiguration"] = iot_job_configuration
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_deployment failed") from exc
    return _parse_deployment(resp)


async def get_deployment(
    deployment_id: str,
    *,
    region_name: str | None = None,
) -> DeploymentResult:
    """Get details of a Greengrass deployment.

    Args:
        deployment_id: The deployment ID.
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        resp = await client.call("GetDeployment", deploymentId=deployment_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_deployment failed") from exc
    return _parse_deployment(resp)


async def list_deployments(
    *,
    target_arn: str | None = None,
    region_name: str | None = None,
) -> list[DeploymentResult]:
    """List Greengrass deployments.

    Args:
        target_arn: Optional filter by target ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`DeploymentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    results: list[DeploymentResult] = []
    kwargs: dict[str, Any] = {}
    if target_arn:
        kwargs["targetArn"] = target_arn
    try:
        while True:
            resp = await client.call("ListDeployments", **kwargs)
            for dep in resp.get("deployments", []):
                results.append(_parse_deployment(dep))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_deployments failed") from exc
    return results


async def cancel_deployment(
    deployment_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Cancel a Greengrass deployment.

    Args:
        deployment_id: The deployment ID.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        resp = await client.call("CancelDeployment", deploymentId=deployment_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "cancel_deployment failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Core-device operations
# ---------------------------------------------------------------------------


async def list_effective_deployments(
    core_device_thing_name: str,
    *,
    region_name: str | None = None,
) -> list[DeploymentResult]:
    """List effective deployments on a core device.

    Args:
        core_device_thing_name: The IoT thing name of the core device.
        region_name: AWS region override.

    Returns:
        A list of :class:`DeploymentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    results: list[DeploymentResult] = []
    kwargs: dict[str, Any] = {
        "coreDeviceThingName": core_device_thing_name,
    }
    try:
        while True:
            resp = await client.call("ListEffectiveDeployments", **kwargs)
            for dep in resp.get("effectiveDeployments", []):
                results.append(_parse_deployment(dep))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_effective_deployments failed") from exc
    return results


async def list_installed_components(
    core_device_thing_name: str,
    *,
    region_name: str | None = None,
) -> list[InstalledComponentResult]:
    """List components installed on a core device.

    Args:
        core_device_thing_name: The IoT thing name of the core device.
        region_name: AWS region override.

    Returns:
        A list of :class:`InstalledComponentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    results: list[InstalledComponentResult] = []
    kwargs: dict[str, Any] = {
        "coreDeviceThingName": core_device_thing_name,
    }
    try:
        while True:
            resp = await client.call("ListInstalledComponents", **kwargs)
            for comp in resp.get("installedComponents", []):
                results.append(_parse_installed_component(comp))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_installed_components failed") from exc
    return results


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


async def tag_resource(
    resource_arn: str,
    *,
    tags: dict[str, str],
    region_name: str | None = None,
) -> None:
    """Add or overwrite tags on a Greengrass resource.

    Args:
        resource_arn: The resource ARN.
        tags: Key/value tags to set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        await client.call("TagResource", resourceArn=resource_arn, tags=tags)
    except Exception as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


async def list_tags_for_resource(
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """List tags on a Greengrass resource.

    Args:
        resource_arn: The resource ARN.
        region_name: AWS region override.

    Returns:
        A dict of tag key/value pairs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    try:
        resp = await client.call("ListTagsForResource", resourceArn=resource_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return resp.get("tags", {})


async def associate_service_role_to_account(
    role_arn: str,
    region_name: str | None = None,
) -> AssociateServiceRoleToAccountResult:
    """Associate service role to account.

    Args:
        role_arn: Role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleArn"] = role_arn
    try:
        resp = await client.call("AssociateServiceRoleToAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate service role to account") from exc
    return AssociateServiceRoleToAccountResult(
        associated_at=resp.get("associatedAt"),
    )


async def batch_associate_client_device_with_core_device(
    core_device_thing_name: str,
    *,
    entries: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> BatchAssociateClientDeviceWithCoreDeviceResult:
    """Batch associate client device with core device.

    Args:
        core_device_thing_name: Core device thing name.
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if entries is not None:
        kwargs["entries"] = entries
    try:
        resp = await client.call("BatchAssociateClientDeviceWithCoreDevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch associate client device with core device"
        ) from exc
    return BatchAssociateClientDeviceWithCoreDeviceResult(
        error_entries=resp.get("errorEntries"),
    )


async def batch_disassociate_client_device_from_core_device(
    core_device_thing_name: str,
    *,
    entries: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> BatchDisassociateClientDeviceFromCoreDeviceResult:
    """Batch disassociate client device from core device.

    Args:
        core_device_thing_name: Core device thing name.
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if entries is not None:
        kwargs["entries"] = entries
    try:
        resp = await client.call("BatchDisassociateClientDeviceFromCoreDevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to batch disassociate client device from core device"
        ) from exc
    return BatchDisassociateClientDeviceFromCoreDeviceResult(
        error_entries=resp.get("errorEntries"),
    )


async def delete_core_device(
    core_device_thing_name: str,
    region_name: str | None = None,
) -> None:
    """Delete core device.

    Args:
        core_device_thing_name: Core device thing name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    try:
        await client.call("DeleteCoreDevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete core device") from exc
    return None


async def delete_deployment(
    deployment_id: str,
    region_name: str | None = None,
) -> None:
    """Delete deployment.

    Args:
        deployment_id: Deployment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    try:
        await client.call("DeleteDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete deployment") from exc
    return None


async def disassociate_service_role_from_account(
    region_name: str | None = None,
) -> DisassociateServiceRoleFromAccountResult:
    """Disassociate service role from account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DisassociateServiceRoleFromAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate service role from account") from exc
    return DisassociateServiceRoleFromAccountResult(
        disassociated_at=resp.get("disassociatedAt"),
    )


async def get_component_version_artifact(
    arn: str,
    artifact_name: str,
    *,
    s3_endpoint_type: str | None = None,
    iot_endpoint_type: str | None = None,
    region_name: str | None = None,
) -> GetComponentVersionArtifactResult:
    """Get component version artifact.

    Args:
        arn: Arn.
        artifact_name: Artifact name.
        s3_endpoint_type: S3 endpoint type.
        iot_endpoint_type: Iot endpoint type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    kwargs["artifactName"] = artifact_name
    if s3_endpoint_type is not None:
        kwargs["s3EndpointType"] = s3_endpoint_type
    if iot_endpoint_type is not None:
        kwargs["iotEndpointType"] = iot_endpoint_type
    try:
        resp = await client.call("GetComponentVersionArtifact", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get component version artifact") from exc
    return GetComponentVersionArtifactResult(
        pre_signed_url=resp.get("preSignedUrl"),
    )


async def get_connectivity_info(
    thing_name: str,
    region_name: str | None = None,
) -> GetConnectivityInfoResult:
    """Get connectivity info.

    Args:
        thing_name: Thing name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    try:
        resp = await client.call("GetConnectivityInfo", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connectivity info") from exc
    return GetConnectivityInfoResult(
        connectivity_info=resp.get("connectivityInfo"),
        message=resp.get("message"),
    )


async def get_core_device(
    core_device_thing_name: str,
    region_name: str | None = None,
) -> GetCoreDeviceResult:
    """Get core device.

    Args:
        core_device_thing_name: Core device thing name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    try:
        resp = await client.call("GetCoreDevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get core device") from exc
    return GetCoreDeviceResult(
        core_device_thing_name=resp.get("coreDeviceThingName"),
        core_version=resp.get("coreVersion"),
        platform=resp.get("platform"),
        architecture=resp.get("architecture"),
        runtime=resp.get("runtime"),
        status=resp.get("status"),
        last_status_update_timestamp=resp.get("lastStatusUpdateTimestamp"),
        tags=resp.get("tags"),
    )


async def get_service_role_for_account(
    region_name: str | None = None,
) -> GetServiceRoleForAccountResult:
    """Get service role for account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetServiceRoleForAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get service role for account") from exc
    return GetServiceRoleForAccountResult(
        associated_at=resp.get("associatedAt"),
        role_arn=resp.get("roleArn"),
    )


async def list_client_devices_associated_with_core_device(
    core_device_thing_name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClientDevicesAssociatedWithCoreDeviceResult:
    """List client devices associated with core device.

    Args:
        core_device_thing_name: Core device thing name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListClientDevicesAssociatedWithCoreDevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list client devices associated with core device"
        ) from exc
    return ListClientDevicesAssociatedWithCoreDeviceResult(
        associated_client_devices=resp.get("associatedClientDevices"),
        next_token=resp.get("nextToken"),
    )


async def list_component_versions(
    arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListComponentVersionsResult:
    """List component versions.

    Args:
        arn: Arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListComponentVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list component versions") from exc
    return ListComponentVersionsResult(
        component_versions=resp.get("componentVersions"),
        next_token=resp.get("nextToken"),
    )


async def list_core_devices(
    *,
    thing_group_arn: str | None = None,
    status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    runtime: str | None = None,
    region_name: str | None = None,
) -> ListCoreDevicesResult:
    """List core devices.

    Args:
        thing_group_arn: Thing group arn.
        status: Status.
        max_results: Max results.
        next_token: Next token.
        runtime: Runtime.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    if thing_group_arn is not None:
        kwargs["thingGroupArn"] = thing_group_arn
    if status is not None:
        kwargs["status"] = status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if runtime is not None:
        kwargs["runtime"] = runtime
    try:
        resp = await client.call("ListCoreDevices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list core devices") from exc
    return ListCoreDevicesResult(
        core_devices=resp.get("coreDevices"),
        next_token=resp.get("nextToken"),
    )


async def resolve_component_candidates(
    *,
    platform: dict[str, Any] | None = None,
    component_candidates: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ResolveComponentCandidatesResult:
    """Resolve component candidates.

    Args:
        platform: Platform.
        component_candidates: Component candidates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    if platform is not None:
        kwargs["platform"] = platform
    if component_candidates is not None:
        kwargs["componentCandidates"] = component_candidates
    try:
        resp = await client.call("ResolveComponentCandidates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resolve component candidates") from exc
    return ResolveComponentCandidatesResult(
        resolved_component_versions=resp.get("resolvedComponentVersions"),
    )


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
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_connectivity_info(
    thing_name: str,
    connectivity_info: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateConnectivityInfoResult:
    """Update connectivity info.

    Args:
        thing_name: Thing name.
        connectivity_info: Connectivity info.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    kwargs["connectivityInfo"] = connectivity_info
    try:
        resp = await client.call("UpdateConnectivityInfo", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update connectivity info") from exc
    return UpdateConnectivityInfoResult(
        version=resp.get("version"),
        message=resp.get("message"),
    )
