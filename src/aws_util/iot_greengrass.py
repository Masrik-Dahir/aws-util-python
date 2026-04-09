"""aws_util.iot_greengrass — AWS IoT Greengrass V2 utilities.

Create, describe, list, and delete Greengrass components and deployments.
Manage component versions, inspect effective deployments, and handle
resource tagging.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

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
# Models
# ---------------------------------------------------------------------------


class ComponentResult(BaseModel):
    """Metadata for a Greengrass component."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    arn: str | None = None
    component_name: str | None = None
    component_version: str | None = None
    status: str | None = None
    description: str | None = None
    extra: dict[str, Any] = {}


class DeploymentResult(BaseModel):
    """Metadata for a Greengrass deployment."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    deployment_id: str
    deployment_name: str | None = None
    deployment_status: str | None = None
    target_arn: str | None = None
    revision_id: str | None = None
    extra: dict[str, Any] = {}


class InstalledComponentResult(BaseModel):
    """Metadata for an installed Greengrass component on a core device."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    component_name: str
    component_version: str | None = None
    lifecycle_state: str | None = None
    is_root: bool = False
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_component(raw: dict[str, Any]) -> ComponentResult:
    """Convert a raw Greengrass component dict."""
    status = raw.get("status")
    status_str: str | None = None
    if isinstance(status, dict):
        status_str = status.get("componentState")
    elif isinstance(status, str):
        status_str = status
    return ComponentResult(
        arn=raw.get("arn"),
        component_name=raw.get("componentName"),
        component_version=(
            raw.get("componentVersion") or raw.get("latestVersion", {}).get("componentVersion")
        ),
        status=status_str,
        description=raw.get("description"),
        extra={
            k: v
            for k, v in raw.items()
            if k
            not in {
                "arn",
                "componentName",
                "componentVersion",
                "status",
                "description",
                "latestVersion",
            }
        },
    )


def _parse_deployment(raw: dict[str, Any]) -> DeploymentResult:
    """Convert a raw Greengrass deployment dict."""
    return DeploymentResult(
        deployment_id=raw["deploymentId"],
        deployment_name=raw.get("deploymentName"),
        deployment_status=raw.get("deploymentStatus"),
        target_arn=raw.get("targetArn"),
        revision_id=raw.get("revisionId"),
        extra={
            k: v
            for k, v in raw.items()
            if k
            not in {
                "deploymentId",
                "deploymentName",
                "deploymentStatus",
                "targetArn",
                "revisionId",
            }
        },
    )


def _parse_installed_component(
    raw: dict[str, Any],
) -> InstalledComponentResult:
    """Convert a raw installed-component dict."""
    return InstalledComponentResult(
        component_name=raw["componentName"],
        component_version=raw.get("componentVersion"),
        lifecycle_state=raw.get("lifecycleState"),
        is_root=raw.get("isRoot", False),
        extra={
            k: v
            for k, v in raw.items()
            if k
            not in {
                "componentName",
                "componentVersion",
                "lifecycleState",
                "isRoot",
            }
        },
    )


# ---------------------------------------------------------------------------
# Component operations
# ---------------------------------------------------------------------------


def create_component_version(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    if inline_recipe is not None:
        kwargs["inlineRecipe"] = inline_recipe.encode()
    if lambda_function_recipe_source is not None:
        kwargs["lambdaFunction"] = lambda_function_recipe_source
    if tags:
        kwargs["tags"] = tags
    try:
        resp = client.create_component_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_component_version failed") from exc
    return _parse_component(resp)


def describe_component(
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
    client = get_client("greengrassv2", region_name)
    try:
        resp = client.describe_component(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_component failed") from exc
    return _parse_component(resp)


def list_components(
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
    client = get_client("greengrassv2", region_name)
    results: list[ComponentResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_components(**kwargs)
            for comp in resp.get("components", []):
                results.append(_parse_component(comp))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_components failed") from exc
    return results


def delete_component(
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
    client = get_client("greengrassv2", region_name)
    try:
        client.delete_component(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_component failed") from exc


def get_component(
    arn: str,
    *,
    recipe_output_format: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Get the recipe for a Greengrass component version.

    Args:
        arn: The component version ARN.
        recipe_output_format: ``"JSON"`` or ``"YAML"`` (default service
            behaviour).
        region_name: AWS region override.

    Returns:
        The full API response dict including ``recipe`` and
        ``recipeOutputFormat``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {"arn": arn}
    if recipe_output_format is not None:
        kwargs["recipeOutputFormat"] = recipe_output_format
    try:
        resp = client.get_component(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_component failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Deployment operations
# ---------------------------------------------------------------------------


def create_deployment(
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
    client = get_client("greengrassv2", region_name)
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
        resp = client.create_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_deployment failed") from exc
    return _parse_deployment(resp)


def get_deployment(
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
    client = get_client("greengrassv2", region_name)
    try:
        resp = client.get_deployment(deploymentId=deployment_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_deployment failed") from exc
    return _parse_deployment(resp)


def list_deployments(
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
    client = get_client("greengrassv2", region_name)
    results: list[DeploymentResult] = []
    kwargs: dict[str, Any] = {}
    if target_arn:
        kwargs["targetArn"] = target_arn
    try:
        while True:
            resp = client.list_deployments(**kwargs)
            for dep in resp.get("deployments", []):
                results.append(_parse_deployment(dep))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_deployments failed") from exc
    return results


def cancel_deployment(
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
    client = get_client("greengrassv2", region_name)
    try:
        resp = client.cancel_deployment(deploymentId=deployment_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "cancel_deployment failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Core-device operations
# ---------------------------------------------------------------------------


def list_effective_deployments(
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
    client = get_client("greengrassv2", region_name)
    results: list[DeploymentResult] = []
    kwargs: dict[str, Any] = {
        "coreDeviceThingName": core_device_thing_name,
    }
    try:
        while True:
            resp = client.list_effective_deployments(**kwargs)
            for dep in resp.get("effectiveDeployments", []):
                results.append(_parse_deployment(dep))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_effective_deployments failed") from exc
    return results


def list_installed_components(
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
    client = get_client("greengrassv2", region_name)
    results: list[InstalledComponentResult] = []
    kwargs: dict[str, Any] = {
        "coreDeviceThingName": core_device_thing_name,
    }
    try:
        while True:
            resp = client.list_installed_components(**kwargs)
            for comp in resp.get("installedComponents", []):
                results.append(_parse_installed_component(comp))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_installed_components failed") from exc
    return results


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


def tag_resource(
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
    client = get_client("greengrassv2", region_name)
    try:
        client.tag_resource(resourceArn=resource_arn, tags=tags)
    except ClientError as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


def list_tags_for_resource(
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
    client = get_client("greengrassv2", region_name)
    try:
        resp = client.list_tags_for_resource(resourceArn=resource_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return resp.get("tags", {})


class AssociateServiceRoleToAccountResult(BaseModel):
    """Result of associate_service_role_to_account."""

    model_config = ConfigDict(frozen=True)

    associated_at: str | None = None


class BatchAssociateClientDeviceWithCoreDeviceResult(BaseModel):
    """Result of batch_associate_client_device_with_core_device."""

    model_config = ConfigDict(frozen=True)

    error_entries: list[dict[str, Any]] | None = None


class BatchDisassociateClientDeviceFromCoreDeviceResult(BaseModel):
    """Result of batch_disassociate_client_device_from_core_device."""

    model_config = ConfigDict(frozen=True)

    error_entries: list[dict[str, Any]] | None = None


class DisassociateServiceRoleFromAccountResult(BaseModel):
    """Result of disassociate_service_role_from_account."""

    model_config = ConfigDict(frozen=True)

    disassociated_at: str | None = None


class GetComponentVersionArtifactResult(BaseModel):
    """Result of get_component_version_artifact."""

    model_config = ConfigDict(frozen=True)

    pre_signed_url: str | None = None


class GetConnectivityInfoResult(BaseModel):
    """Result of get_connectivity_info."""

    model_config = ConfigDict(frozen=True)

    connectivity_info: list[dict[str, Any]] | None = None
    message: str | None = None


class GetCoreDeviceResult(BaseModel):
    """Result of get_core_device."""

    model_config = ConfigDict(frozen=True)

    core_device_thing_name: str | None = None
    core_version: str | None = None
    platform: str | None = None
    architecture: str | None = None
    runtime: str | None = None
    status: str | None = None
    last_status_update_timestamp: str | None = None
    tags: dict[str, Any] | None = None


class GetServiceRoleForAccountResult(BaseModel):
    """Result of get_service_role_for_account."""

    model_config = ConfigDict(frozen=True)

    associated_at: str | None = None
    role_arn: str | None = None


class ListClientDevicesAssociatedWithCoreDeviceResult(BaseModel):
    """Result of list_client_devices_associated_with_core_device."""

    model_config = ConfigDict(frozen=True)

    associated_client_devices: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListComponentVersionsResult(BaseModel):
    """Result of list_component_versions."""

    model_config = ConfigDict(frozen=True)

    component_versions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListCoreDevicesResult(BaseModel):
    """Result of list_core_devices."""

    model_config = ConfigDict(frozen=True)

    core_devices: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ResolveComponentCandidatesResult(BaseModel):
    """Result of resolve_component_candidates."""

    model_config = ConfigDict(frozen=True)

    resolved_component_versions: list[dict[str, Any]] | None = None


class UpdateConnectivityInfoResult(BaseModel):
    """Result of update_connectivity_info."""

    model_config = ConfigDict(frozen=True)

    version: str | None = None
    message: str | None = None


def associate_service_role_to_account(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleArn"] = role_arn
    try:
        resp = client.associate_service_role_to_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate service role to account") from exc
    return AssociateServiceRoleToAccountResult(
        associated_at=resp.get("associatedAt"),
    )


def batch_associate_client_device_with_core_device(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if entries is not None:
        kwargs["entries"] = entries
    try:
        resp = client.batch_associate_client_device_with_core_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to batch associate client device with core device"
        ) from exc
    return BatchAssociateClientDeviceWithCoreDeviceResult(
        error_entries=resp.get("errorEntries"),
    )


def batch_disassociate_client_device_from_core_device(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if entries is not None:
        kwargs["entries"] = entries
    try:
        resp = client.batch_disassociate_client_device_from_core_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to batch disassociate client device from core device"
        ) from exc
    return BatchDisassociateClientDeviceFromCoreDeviceResult(
        error_entries=resp.get("errorEntries"),
    )


def delete_core_device(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    try:
        client.delete_core_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete core device") from exc
    return None


def delete_deployment(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    try:
        client.delete_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete deployment") from exc
    return None


def disassociate_service_role_from_account(
    region_name: str | None = None,
) -> DisassociateServiceRoleFromAccountResult:
    """Disassociate service role from account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.disassociate_service_role_from_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate service role from account") from exc
    return DisassociateServiceRoleFromAccountResult(
        disassociated_at=resp.get("disassociatedAt"),
    )


def get_component_version_artifact(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    kwargs["artifactName"] = artifact_name
    if s3_endpoint_type is not None:
        kwargs["s3EndpointType"] = s3_endpoint_type
    if iot_endpoint_type is not None:
        kwargs["iotEndpointType"] = iot_endpoint_type
    try:
        resp = client.get_component_version_artifact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get component version artifact") from exc
    return GetComponentVersionArtifactResult(
        pre_signed_url=resp.get("preSignedUrl"),
    )


def get_connectivity_info(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    try:
        resp = client.get_connectivity_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get connectivity info") from exc
    return GetConnectivityInfoResult(
        connectivity_info=resp.get("connectivityInfo"),
        message=resp.get("message"),
    )


def get_core_device(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    try:
        resp = client.get_core_device(**kwargs)
    except ClientError as exc:
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


def get_service_role_for_account(
    region_name: str | None = None,
) -> GetServiceRoleForAccountResult:
    """Get service role for account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_service_role_for_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get service role for account") from exc
    return GetServiceRoleForAccountResult(
        associated_at=resp.get("associatedAt"),
        role_arn=resp.get("roleArn"),
    )


def list_client_devices_associated_with_core_device(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["coreDeviceThingName"] = core_device_thing_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_client_devices_associated_with_core_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list client devices associated with core device"
        ) from exc
    return ListClientDevicesAssociatedWithCoreDeviceResult(
        associated_client_devices=resp.get("associatedClientDevices"),
        next_token=resp.get("nextToken"),
    )


def list_component_versions(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_component_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list component versions") from exc
    return ListComponentVersionsResult(
        component_versions=resp.get("componentVersions"),
        next_token=resp.get("nextToken"),
    )


def list_core_devices(
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
    client = get_client("greengrassv2", region_name)
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
        resp = client.list_core_devices(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list core devices") from exc
    return ListCoreDevicesResult(
        core_devices=resp.get("coreDevices"),
        next_token=resp.get("nextToken"),
    )


def resolve_component_candidates(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    if platform is not None:
        kwargs["platform"] = platform
    if component_candidates is not None:
        kwargs["componentCandidates"] = component_candidates
    try:
        resp = client.resolve_component_candidates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to resolve component candidates") from exc
    return ResolveComponentCandidatesResult(
        resolved_component_versions=resp.get("resolvedComponentVersions"),
    )


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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_connectivity_info(
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
    client = get_client("greengrassv2", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    kwargs["connectivityInfo"] = connectivity_info
    try:
        resp = client.update_connectivity_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update connectivity info") from exc
    return UpdateConnectivityInfoResult(
        version=resp.get("version"),
        message=resp.get("message"),
    )
