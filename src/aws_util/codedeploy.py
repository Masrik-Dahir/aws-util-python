"""aws_util.codedeploy --- AWS CodeDeploy management utilities.

Provides high-level helpers for creating, managing, and monitoring
AWS CodeDeploy applications, deployment groups, deployments, deployment
configs, and application revisions, including polling-based waiters and
a composite ``deploy_and_wait`` convenience function.
"""

from __future__ import annotations

import time as _time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "ApplicationResult",
    "BatchGetApplicationRevisionsResult",
    "BatchGetApplicationsResult",
    "BatchGetDeploymentGroupsResult",
    "BatchGetDeploymentInstancesResult",
    "BatchGetDeploymentTargetsResult",
    "BatchGetDeploymentsResult",
    "BatchGetOnPremisesInstancesResult",
    "DeleteGitHubAccountTokenResult",
    "DeploymentConfigResult",
    "DeploymentGroupResult",
    "DeploymentResult",
    "GetDeploymentInstanceResult",
    "GetDeploymentTargetResult",
    "GetOnPremisesInstanceResult",
    "ListDeploymentConfigsResult",
    "ListDeploymentInstancesResult",
    "ListDeploymentTargetsResult",
    "ListGitHubAccountTokenNamesResult",
    "ListOnPremisesInstancesResult",
    "ListTagsForResourceResult",
    "PutLifecycleEventHookExecutionStatusResult",
    "RevisionResult",
    "UpdateDeploymentGroupResult",
    "add_tags_to_on_premises_instances",
    "batch_get_application_revisions",
    "batch_get_applications",
    "batch_get_deployment_groups",
    "batch_get_deployment_instances",
    "batch_get_deployment_targets",
    "batch_get_deployments",
    "batch_get_on_premises_instances",
    "continue_deployment",
    "create_application",
    "create_deployment",
    "create_deployment_config",
    "create_deployment_group",
    "delete_application",
    "delete_deployment_config",
    "delete_deployment_group",
    "delete_git_hub_account_token",
    "delete_resources_by_external_id",
    "deploy_and_wait",
    "deregister_on_premises_instance",
    "get_application",
    "get_application_revision",
    "get_deployment",
    "get_deployment_config",
    "get_deployment_group",
    "get_deployment_instance",
    "get_deployment_target",
    "get_on_premises_instance",
    "list_application_revisions",
    "list_applications",
    "list_deployment_configs",
    "list_deployment_groups",
    "list_deployment_instances",
    "list_deployment_targets",
    "list_deployments",
    "list_git_hub_account_token_names",
    "list_on_premises_instances",
    "list_tags_for_resource",
    "put_lifecycle_event_hook_execution_status",
    "register_application_revision",
    "register_on_premises_instance",
    "remove_tags_from_on_premises_instances",
    "skip_wait_time_for_instance_termination",
    "stop_deployment",
    "tag_resource",
    "untag_resource",
    "update_application",
    "update_deployment_group",
    "wait_for_deployment",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ApplicationResult(BaseModel):
    """Metadata for a CodeDeploy application."""

    model_config = ConfigDict(frozen=True)

    application_id: str = ""
    application_name: str = ""
    compute_platform: str = ""
    create_time: str | None = None
    linked_to_github: bool = False
    extra: dict[str, Any] = Field(default_factory=dict)


class DeploymentGroupResult(BaseModel):
    """Metadata for a CodeDeploy deployment group."""

    model_config = ConfigDict(frozen=True)

    deployment_group_id: str = ""
    deployment_group_name: str = ""
    application_name: str = ""
    service_role_arn: str = ""
    deployment_config_name: str = ""
    compute_platform: str = ""
    extra: dict[str, Any] = Field(default_factory=dict)


class DeploymentResult(BaseModel):
    """Metadata for a CodeDeploy deployment."""

    model_config = ConfigDict(frozen=True)

    deployment_id: str = ""
    application_name: str = ""
    deployment_group_name: str = ""
    status: str = ""
    revision: dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    create_time: str | None = None
    complete_time: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class DeploymentConfigResult(BaseModel):
    """Metadata for a CodeDeploy deployment configuration."""

    model_config = ConfigDict(frozen=True)

    deployment_config_id: str = ""
    deployment_config_name: str = ""
    compute_platform: str = ""
    minimum_healthy_hosts: dict[str, Any] = Field(
        default_factory=dict,
    )
    create_time: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class RevisionResult(BaseModel):
    """Metadata for an application revision."""

    model_config = ConfigDict(frozen=True)

    application_name: str = ""
    revision: dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    register_time: str | None = None
    first_used_time: str | None = None
    last_used_time: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_APPLICATION_FIELDS = frozenset(
    {
        "applicationId",
        "applicationName",
        "computePlatform",
        "createTime",
        "linkedToGitHub",
    }
)

_DG_FIELDS = frozenset(
    {
        "deploymentGroupId",
        "deploymentGroupName",
        "applicationName",
        "serviceRoleArn",
        "deploymentConfigName",
        "computePlatform",
    }
)

_DEPLOYMENT_FIELDS = frozenset(
    {
        "deploymentId",
        "applicationName",
        "deploymentGroupName",
        "status",
        "revision",
        "description",
        "createTime",
        "completeTime",
    }
)

_CONFIG_FIELDS = frozenset(
    {
        "deploymentConfigId",
        "deploymentConfigName",
        "computePlatform",
        "minimumHealthyHosts",
        "createTime",
    }
)


def _parse_application(info: dict[str, Any]) -> ApplicationResult:
    """Build an :class:`ApplicationResult` from an AWS response."""
    return ApplicationResult(
        application_id=info.get("applicationId", ""),
        application_name=info.get("applicationName", ""),
        compute_platform=info.get("computePlatform", ""),
        create_time=(str(info["createTime"]) if "createTime" in info else None),
        linked_to_github=info.get("linkedToGitHub", False),
        extra={k: v for k, v in info.items() if k not in _APPLICATION_FIELDS},
    )


def _parse_deployment_group(
    info: dict[str, Any],
) -> DeploymentGroupResult:
    """Build a :class:`DeploymentGroupResult` from an AWS response."""
    return DeploymentGroupResult(
        deployment_group_id=info.get("deploymentGroupId", ""),
        deployment_group_name=info.get("deploymentGroupName", ""),
        application_name=info.get("applicationName", ""),
        service_role_arn=info.get("serviceRoleArn", ""),
        deployment_config_name=info.get("deploymentConfigName", ""),
        compute_platform=info.get("computePlatform", ""),
        extra={k: v for k, v in info.items() if k not in _DG_FIELDS},
    )


def _parse_deployment(info: dict[str, Any]) -> DeploymentResult:
    """Build a :class:`DeploymentResult` from an AWS response."""
    return DeploymentResult(
        deployment_id=info.get("deploymentId", ""),
        application_name=info.get("applicationName", ""),
        deployment_group_name=info.get("deploymentGroupName", ""),
        status=info.get("status", ""),
        revision=info.get("revision", {}),
        description=info.get("description", ""),
        create_time=(str(info["createTime"]) if "createTime" in info else None),
        complete_time=(str(info["completeTime"]) if "completeTime" in info else None),
        extra={k: v for k, v in info.items() if k not in _DEPLOYMENT_FIELDS},
    )


def _parse_deployment_config(
    info: dict[str, Any],
) -> DeploymentConfigResult:
    """Build a :class:`DeploymentConfigResult` from an AWS response."""
    return DeploymentConfigResult(
        deployment_config_id=info.get("deploymentConfigId", ""),
        deployment_config_name=info.get("deploymentConfigName", ""),
        compute_platform=info.get("computePlatform", ""),
        minimum_healthy_hosts=info.get("minimumHealthyHosts", {}),
        create_time=(str(info["createTime"]) if "createTime" in info else None),
        extra={k: v for k, v in info.items() if k not in _CONFIG_FIELDS},
    )


def _parse_revision(
    resp: dict[str, Any],
    application_name: str = "",
) -> RevisionResult:
    """Build a :class:`RevisionResult` from an AWS response."""
    info = resp.get("revisionInfo", resp)
    gen_info = info.get("genericRevisionInfo", {})
    return RevisionResult(
        application_name=info.get("applicationName", application_name),
        revision=info.get("revisionLocation", info.get("revision", {})),
        description=gen_info.get("description", ""),
        register_time=(str(gen_info["registerTime"]) if "registerTime" in gen_info else None),
        first_used_time=(str(gen_info["firstUsedTime"]) if "firstUsedTime" in gen_info else None),
        last_used_time=(str(gen_info["lastUsedTime"]) if "lastUsedTime" in gen_info else None),
        extra={
            k: v
            for k, v in gen_info.items()
            if k
            not in {
                "description",
                "registerTime",
                "firstUsedTime",
                "lastUsedTime",
            }
        },
    )


# ---------------------------------------------------------------------------
# Application CRUD
# ---------------------------------------------------------------------------


def create_application(
    application_name: str,
    *,
    compute_platform: str = "Server",
    region_name: str | None = None,
) -> ApplicationResult:
    """Create a new CodeDeploy application.

    Args:
        application_name: Application name.
        compute_platform: Compute platform (``"Server"``,
            ``"Lambda"``, or ``"ECS"``).
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult` describing the created application.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.create_application(
            applicationName=application_name,
            computePlatform=compute_platform,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_application failed for {application_name!r}",
        ) from exc
    return ApplicationResult(
        application_id=resp.get("applicationId", ""),
        application_name=application_name,
        compute_platform=compute_platform,
    )


def get_application(
    application_name: str,
    *,
    region_name: str | None = None,
) -> ApplicationResult:
    """Retrieve a CodeDeploy application.

    Args:
        application_name: Application name.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult` with the application metadata.

    Raises:
        RuntimeError: If the application does not exist or the call
            fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.get_application(
            applicationName=application_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_application failed for {application_name!r}",
        ) from exc
    info = resp.get("application", {})
    return _parse_application(info)


def list_applications(
    *,
    region_name: str | None = None,
) -> list[str]:
    """List all CodeDeploy application names.

    Args:
        region_name: AWS region override.

    Returns:
        A list of application name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    applications: list[str] = []
    try:
        paginator = client.get_paginator("list_applications")
        for page in paginator.paginate():
            applications.extend(page.get("applications", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_applications failed") from exc
    return applications


def delete_application(
    application_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CodeDeploy application.

    Args:
        application_name: Application name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        client.delete_application(
            applicationName=application_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_application failed for {application_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Deployment Group CRUD
# ---------------------------------------------------------------------------


def create_deployment_group(
    application_name: str,
    deployment_group_name: str,
    *,
    service_role_arn: str,
    deployment_config_name: str | None = None,
    ec2_tag_filters: list[dict[str, Any]] | None = None,
    auto_scaling_groups: list[str] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a new deployment group.

    Args:
        application_name: Application name.
        deployment_group_name: Deployment group name.
        service_role_arn: IAM role ARN for CodeDeploy.
        deployment_config_name: Optional deployment configuration name.
        ec2_tag_filters: Optional list of EC2 tag filter dicts.
        auto_scaling_groups: Optional list of Auto Scaling group names.
        region_name: AWS region override.

    Returns:
        The deployment group ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {
        "applicationName": application_name,
        "deploymentGroupName": deployment_group_name,
        "serviceRoleArn": service_role_arn,
    }
    if deployment_config_name is not None:
        kwargs["deploymentConfigName"] = deployment_config_name
    if ec2_tag_filters is not None:
        kwargs["ec2TagFilters"] = ec2_tag_filters
    if auto_scaling_groups is not None:
        kwargs["autoScalingGroups"] = auto_scaling_groups
    try:
        resp = client.create_deployment_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_deployment_group failed for {application_name!r}/{deployment_group_name!r}",
        ) from exc
    return resp.get("deploymentGroupId", "")


def get_deployment_group(
    application_name: str,
    deployment_group_name: str,
    *,
    region_name: str | None = None,
) -> DeploymentGroupResult:
    """Retrieve a deployment group.

    Args:
        application_name: Application name.
        deployment_group_name: Deployment group name.
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentGroupResult` with the group metadata.

    Raises:
        RuntimeError: If the deployment group does not exist or the
            call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.get_deployment_group(
            applicationName=application_name,
            deploymentGroupName=deployment_group_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_deployment_group failed for {application_name!r}/{deployment_group_name!r}",
        ) from exc
    info = resp.get("deploymentGroupInfo", {})
    return _parse_deployment_group(info)


def list_deployment_groups(
    application_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List deployment group names for an application.

    Args:
        application_name: Application name.
        region_name: AWS region override.

    Returns:
        A list of deployment group name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    groups: list[str] = []
    try:
        paginator = client.get_paginator("list_deployment_groups")
        for page in paginator.paginate(
            applicationName=application_name,
        ):
            groups.extend(page.get("deploymentGroups", []))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"list_deployment_groups failed for {application_name!r}",
        ) from exc
    return groups


def delete_deployment_group(
    application_name: str,
    deployment_group_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a deployment group.

    Args:
        application_name: Application name.
        deployment_group_name: Deployment group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        client.delete_deployment_group(
            applicationName=application_name,
            deploymentGroupName=deployment_group_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_deployment_group failed for {application_name!r}/{deployment_group_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Deployment management
# ---------------------------------------------------------------------------


def create_deployment(
    application_name: str,
    *,
    deployment_group_name: str,
    revision: dict[str, Any],
    description: str | None = None,
    deployment_config_name: str | None = None,
    auto_rollback_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a new deployment.

    Args:
        application_name: Application name.
        deployment_group_name: Deployment group name.
        revision: Revision location dict (e.g. S3 or GitHub).
        description: Optional deployment description.
        deployment_config_name: Optional deployment configuration name.
        auto_rollback_configuration: Optional auto-rollback config.
        region_name: AWS region override.

    Returns:
        The deployment ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {
        "applicationName": application_name,
        "deploymentGroupName": deployment_group_name,
        "revision": revision,
    }
    if description is not None:
        kwargs["description"] = description
    if deployment_config_name is not None:
        kwargs["deploymentConfigName"] = deployment_config_name
    if auto_rollback_configuration is not None:
        kwargs["autoRollbackConfiguration"] = auto_rollback_configuration
    try:
        resp = client.create_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_deployment failed for {application_name!r}/{deployment_group_name!r}",
        ) from exc
    return resp.get("deploymentId", "")


def get_deployment(
    deployment_id: str,
    *,
    region_name: str | None = None,
) -> DeploymentResult:
    """Retrieve details for a deployment.

    Args:
        deployment_id: The deployment ID.
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentResult` with the deployment details.

    Raises:
        RuntimeError: If the deployment does not exist or the call
            fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.get_deployment(deploymentId=deployment_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_deployment failed for {deployment_id!r}",
        ) from exc
    info = resp.get("deploymentInfo", {})
    return _parse_deployment(info)


def list_deployments(
    *,
    application_name: str | None = None,
    deployment_group_name: str | None = None,
    include_only_statuses: list[str] | None = None,
    region_name: str | None = None,
) -> list[str]:
    """List deployment IDs, optionally filtered.

    Args:
        application_name: Optional application name filter.
        deployment_group_name: Optional deployment group name filter.
        include_only_statuses: Optional list of status filters.
        region_name: AWS region override.

    Returns:
        A list of deployment ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["applicationName"] = application_name
    if deployment_group_name is not None:
        kwargs["deploymentGroupName"] = deployment_group_name
    if include_only_statuses is not None:
        kwargs["includeOnlyStatuses"] = include_only_statuses
    deployments: list[str] = []
    try:
        paginator = client.get_paginator("list_deployments")
        for page in paginator.paginate(**kwargs):
            deployments.extend(page.get("deployments", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_deployments failed") from exc
    return deployments


def stop_deployment(
    deployment_id: str,
    *,
    auto_rollback_enabled: bool = False,
    region_name: str | None = None,
) -> None:
    """Stop a running deployment.

    Args:
        deployment_id: The deployment ID.
        auto_rollback_enabled: Whether to auto-rollback when stopped.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        client.stop_deployment(
            deploymentId=deployment_id,
            autoRollbackEnabled=auto_rollback_enabled,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"stop_deployment failed for {deployment_id!r}",
        ) from exc


def continue_deployment(
    deployment_id: str,
    *,
    deployment_wait_type: str = "READY_WAIT",
    region_name: str | None = None,
) -> None:
    """Continue a deployment that is waiting for approval.

    Args:
        deployment_id: The deployment ID.
        deployment_wait_type: Type of wait (``"READY_WAIT"`` or
            ``"TERMINATION_WAIT"``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        client.continue_deployment(
            deploymentId=deployment_id,
            deploymentWaitType=deployment_wait_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"continue_deployment failed for {deployment_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Revision management
# ---------------------------------------------------------------------------


def register_application_revision(
    application_name: str,
    *,
    revision: dict[str, Any],
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Register an application revision.

    Args:
        application_name: Application name.
        revision: Revision location dict (e.g. S3 or GitHub).
        description: Optional revision description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {
        "applicationName": application_name,
        "revision": revision,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        client.register_application_revision(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"register_application_revision failed for {application_name!r}",
        ) from exc


def get_application_revision(
    application_name: str,
    *,
    revision: dict[str, Any],
    region_name: str | None = None,
) -> RevisionResult:
    """Retrieve details for a registered application revision.

    Args:
        application_name: Application name.
        revision: Revision location dict.
        region_name: AWS region override.

    Returns:
        A :class:`RevisionResult` with the revision metadata.

    Raises:
        RuntimeError: If the revision does not exist or the call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.get_application_revision(
            applicationName=application_name,
            revision=revision,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_application_revision failed for {application_name!r}",
        ) from exc
    return _parse_revision(resp, application_name=application_name)


def list_application_revisions(
    application_name: str,
    *,
    sort_by: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List application revisions.

    Args:
        application_name: Application name.
        sort_by: Optional sort field (``"registerTime"`` etc.).
        sort_order: Optional sort order (``"ascending"`` or
            ``"descending"``).
        region_name: AWS region override.

    Returns:
        A list of revision location dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {
        "applicationName": application_name,
    }
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    revisions: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("list_application_revisions")
        for page in paginator.paginate(**kwargs):
            revisions.extend(page.get("revisions", []))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"list_application_revisions failed for {application_name!r}",
        ) from exc
    return revisions


# ---------------------------------------------------------------------------
# Deployment config
# ---------------------------------------------------------------------------


def create_deployment_config(
    deployment_config_name: str,
    *,
    minimum_healthy_hosts: dict[str, Any] | None = None,
    compute_platform: str = "Server",
    region_name: str | None = None,
) -> str:
    """Create a deployment configuration.

    Args:
        deployment_config_name: Name of the deployment config.
        minimum_healthy_hosts: Dict with ``type`` and ``value``.
        compute_platform: Compute platform (``"Server"``,
            ``"Lambda"``, or ``"ECS"``).
        region_name: AWS region override.

    Returns:
        The deployment config ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {
        "deploymentConfigName": deployment_config_name,
        "computePlatform": compute_platform,
    }
    if minimum_healthy_hosts is not None:
        kwargs["minimumHealthyHosts"] = minimum_healthy_hosts
    try:
        resp = client.create_deployment_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_deployment_config failed for {deployment_config_name!r}",
        ) from exc
    return resp.get("deploymentConfigId", "")


def get_deployment_config(
    deployment_config_name: str,
    *,
    region_name: str | None = None,
) -> DeploymentConfigResult:
    """Retrieve a deployment configuration.

    Args:
        deployment_config_name: Name of the deployment config.
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentConfigResult` with the config metadata.

    Raises:
        RuntimeError: If the config does not exist or the call fails.
    """
    client = get_client("codedeploy", region_name)
    try:
        resp = client.get_deployment_config(
            deploymentConfigName=deployment_config_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_deployment_config failed for {deployment_config_name!r}",
        ) from exc
    info = resp.get("deploymentConfigInfo", {})
    return _parse_deployment_config(info)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------

_TERMINAL_STATUSES = frozenset({"Succeeded", "Failed", "Stopped", "Ready"})


def wait_for_deployment(
    deployment_id: str,
    *,
    target_statuses: tuple[str, ...] = ("Succeeded",),
    failure_statuses: tuple[str, ...] = ("Failed", "Stopped"),
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> DeploymentResult:
    """Poll until a deployment reaches a target or failure status.

    Args:
        deployment_id: The deployment ID to monitor.
        target_statuses: Statuses considered successful.
        failure_statuses: Statuses considered failed (raises
            immediately).
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between polls (default ``15``).
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentResult` in one of the *target_statuses*.

    Raises:
        AwsTimeoutError: If the deployment does not reach a target
            status within *timeout*.
        RuntimeError: If the deployment enters a *failure_statuses*
            status or the describe call fails.
    """
    deadline = _time.monotonic() + timeout
    while True:
        deployment = get_deployment(deployment_id, region_name=region_name)
        if deployment.status in target_statuses:
            return deployment
        if deployment.status in failure_statuses:
            raise RuntimeError(
                f"Deployment {deployment_id!r} entered failure status: {deployment.status}"
            )
        if _time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Deployment {deployment_id!r} did not reach"
                f" {target_statuses} within {timeout}s"
                f" (last status: {deployment.status})"
            )
        _time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Composite utilities
# ---------------------------------------------------------------------------


def deploy_and_wait(
    application_name: str,
    *,
    deployment_group_name: str,
    revision: dict[str, Any],
    description: str | None = None,
    deployment_config_name: str | None = None,
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> DeploymentResult:
    """Create a deployment and wait for it to complete.

    Combines :func:`create_deployment` and :func:`wait_for_deployment`.

    Args:
        application_name: Application name.
        deployment_group_name: Deployment group name.
        revision: Revision location dict.
        description: Optional deployment description.
        deployment_config_name: Optional deployment configuration name.
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between polls (default ``15``).
        region_name: AWS region override.

    Returns:
        A :class:`DeploymentResult` for the completed deployment.

    Raises:
        AwsTimeoutError: If the deployment does not complete within
            *timeout*.
        RuntimeError: If the create or describe call fails, or the
            deployment enters a failure status.
    """
    deployment_id = create_deployment(
        application_name,
        deployment_group_name=deployment_group_name,
        revision=revision,
        description=description,
        deployment_config_name=deployment_config_name,
        region_name=region_name,
    )
    return wait_for_deployment(
        deployment_id,
        timeout=timeout,
        poll_interval=poll_interval,
        region_name=region_name,
    )


class BatchGetApplicationRevisionsResult(BaseModel):
    """Result of batch_get_application_revisions."""

    model_config = ConfigDict(frozen=True)

    application_name: str | None = None
    error_message: str | None = None
    revisions: list[dict[str, Any]] | None = None


class BatchGetApplicationsResult(BaseModel):
    """Result of batch_get_applications."""

    model_config = ConfigDict(frozen=True)

    applications_info: list[dict[str, Any]] | None = None


class BatchGetDeploymentGroupsResult(BaseModel):
    """Result of batch_get_deployment_groups."""

    model_config = ConfigDict(frozen=True)

    deployment_groups_info: list[dict[str, Any]] | None = None
    error_message: str | None = None


class BatchGetDeploymentInstancesResult(BaseModel):
    """Result of batch_get_deployment_instances."""

    model_config = ConfigDict(frozen=True)

    instances_summary: list[dict[str, Any]] | None = None
    error_message: str | None = None


class BatchGetDeploymentTargetsResult(BaseModel):
    """Result of batch_get_deployment_targets."""

    model_config = ConfigDict(frozen=True)

    deployment_targets: list[dict[str, Any]] | None = None


class BatchGetDeploymentsResult(BaseModel):
    """Result of batch_get_deployments."""

    model_config = ConfigDict(frozen=True)

    deployments_info: list[dict[str, Any]] | None = None


class BatchGetOnPremisesInstancesResult(BaseModel):
    """Result of batch_get_on_premises_instances."""

    model_config = ConfigDict(frozen=True)

    instance_infos: list[dict[str, Any]] | None = None


class DeleteGitHubAccountTokenResult(BaseModel):
    """Result of delete_git_hub_account_token."""

    model_config = ConfigDict(frozen=True)

    token_name: str | None = None


class GetDeploymentInstanceResult(BaseModel):
    """Result of get_deployment_instance."""

    model_config = ConfigDict(frozen=True)

    instance_summary: dict[str, Any] | None = None


class GetDeploymentTargetResult(BaseModel):
    """Result of get_deployment_target."""

    model_config = ConfigDict(frozen=True)

    deployment_target: dict[str, Any] | None = None


class GetOnPremisesInstanceResult(BaseModel):
    """Result of get_on_premises_instance."""

    model_config = ConfigDict(frozen=True)

    instance_info: dict[str, Any] | None = None


class ListDeploymentConfigsResult(BaseModel):
    """Result of list_deployment_configs."""

    model_config = ConfigDict(frozen=True)

    deployment_configs_list: list[str] | None = None
    next_token: str | None = None


class ListDeploymentInstancesResult(BaseModel):
    """Result of list_deployment_instances."""

    model_config = ConfigDict(frozen=True)

    instances_list: list[str] | None = None
    next_token: str | None = None


class ListDeploymentTargetsResult(BaseModel):
    """Result of list_deployment_targets."""

    model_config = ConfigDict(frozen=True)

    target_ids: list[str] | None = None
    next_token: str | None = None


class ListGitHubAccountTokenNamesResult(BaseModel):
    """Result of list_git_hub_account_token_names."""

    model_config = ConfigDict(frozen=True)

    token_name_list: list[str] | None = None
    next_token: str | None = None


class ListOnPremisesInstancesResult(BaseModel):
    """Result of list_on_premises_instances."""

    model_config = ConfigDict(frozen=True)

    instance_names: list[str] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutLifecycleEventHookExecutionStatusResult(BaseModel):
    """Result of put_lifecycle_event_hook_execution_status."""

    model_config = ConfigDict(frozen=True)

    lifecycle_event_hook_execution_id: str | None = None


class UpdateDeploymentGroupResult(BaseModel):
    """Result of update_deployment_group."""

    model_config = ConfigDict(frozen=True)

    hooks_not_cleaned_up: list[dict[str, Any]] | None = None


def add_tags_to_on_premises_instances(
    tags: list[dict[str, Any]],
    instance_names: list[str],
    region_name: str | None = None,
) -> None:
    """Add tags to on premises instances.

    Args:
        tags: Tags.
        instance_names: Instance names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["tags"] = tags
    kwargs["instanceNames"] = instance_names
    try:
        client.add_tags_to_on_premises_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add tags to on premises instances") from exc
    return None


def batch_get_application_revisions(
    application_name: str,
    revisions: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetApplicationRevisionsResult:
    """Batch get application revisions.

    Args:
        application_name: Application name.
        revisions: Revisions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationName"] = application_name
    kwargs["revisions"] = revisions
    try:
        resp = client.batch_get_application_revisions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get application revisions") from exc
    return BatchGetApplicationRevisionsResult(
        application_name=resp.get("applicationName"),
        error_message=resp.get("errorMessage"),
        revisions=resp.get("revisions"),
    )


def batch_get_applications(
    application_names: list[str],
    region_name: str | None = None,
) -> BatchGetApplicationsResult:
    """Batch get applications.

    Args:
        application_names: Application names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationNames"] = application_names
    try:
        resp = client.batch_get_applications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get applications") from exc
    return BatchGetApplicationsResult(
        applications_info=resp.get("applicationsInfo"),
    )


def batch_get_deployment_groups(
    application_name: str,
    deployment_group_names: list[str],
    region_name: str | None = None,
) -> BatchGetDeploymentGroupsResult:
    """Batch get deployment groups.

    Args:
        application_name: Application name.
        deployment_group_names: Deployment group names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationName"] = application_name
    kwargs["deploymentGroupNames"] = deployment_group_names
    try:
        resp = client.batch_get_deployment_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get deployment groups") from exc
    return BatchGetDeploymentGroupsResult(
        deployment_groups_info=resp.get("deploymentGroupsInfo"),
        error_message=resp.get("errorMessage"),
    )


def batch_get_deployment_instances(
    deployment_id: str,
    instance_ids: list[str],
    region_name: str | None = None,
) -> BatchGetDeploymentInstancesResult:
    """Batch get deployment instances.

    Args:
        deployment_id: Deployment id.
        instance_ids: Instance ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    kwargs["instanceIds"] = instance_ids
    try:
        resp = client.batch_get_deployment_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get deployment instances") from exc
    return BatchGetDeploymentInstancesResult(
        instances_summary=resp.get("instancesSummary"),
        error_message=resp.get("errorMessage"),
    )


def batch_get_deployment_targets(
    deployment_id: str,
    target_ids: list[str],
    region_name: str | None = None,
) -> BatchGetDeploymentTargetsResult:
    """Batch get deployment targets.

    Args:
        deployment_id: Deployment id.
        target_ids: Target ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    kwargs["targetIds"] = target_ids
    try:
        resp = client.batch_get_deployment_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get deployment targets") from exc
    return BatchGetDeploymentTargetsResult(
        deployment_targets=resp.get("deploymentTargets"),
    )


def batch_get_deployments(
    deployment_ids: list[str],
    region_name: str | None = None,
) -> BatchGetDeploymentsResult:
    """Batch get deployments.

    Args:
        deployment_ids: Deployment ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentIds"] = deployment_ids
    try:
        resp = client.batch_get_deployments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get deployments") from exc
    return BatchGetDeploymentsResult(
        deployments_info=resp.get("deploymentsInfo"),
    )


def batch_get_on_premises_instances(
    instance_names: list[str],
    region_name: str | None = None,
) -> BatchGetOnPremisesInstancesResult:
    """Batch get on premises instances.

    Args:
        instance_names: Instance names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceNames"] = instance_names
    try:
        resp = client.batch_get_on_premises_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get on premises instances") from exc
    return BatchGetOnPremisesInstancesResult(
        instance_infos=resp.get("instanceInfos"),
    )


def delete_deployment_config(
    deployment_config_name: str,
    region_name: str | None = None,
) -> None:
    """Delete deployment config.

    Args:
        deployment_config_name: Deployment config name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentConfigName"] = deployment_config_name
    try:
        client.delete_deployment_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete deployment config") from exc
    return None


def delete_git_hub_account_token(
    *,
    token_name: str | None = None,
    region_name: str | None = None,
) -> DeleteGitHubAccountTokenResult:
    """Delete git hub account token.

    Args:
        token_name: Token name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if token_name is not None:
        kwargs["tokenName"] = token_name
    try:
        resp = client.delete_git_hub_account_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete git hub account token") from exc
    return DeleteGitHubAccountTokenResult(
        token_name=resp.get("tokenName"),
    )


def delete_resources_by_external_id(
    *,
    external_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete resources by external id.

    Args:
        external_id: External id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if external_id is not None:
        kwargs["externalId"] = external_id
    try:
        client.delete_resources_by_external_id(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resources by external id") from exc
    return None


def deregister_on_premises_instance(
    instance_name: str,
    region_name: str | None = None,
) -> None:
    """Deregister on premises instance.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    try:
        client.deregister_on_premises_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister on premises instance") from exc
    return None


def get_deployment_instance(
    deployment_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> GetDeploymentInstanceResult:
    """Get deployment instance.

    Args:
        deployment_id: Deployment id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    kwargs["instanceId"] = instance_id
    try:
        resp = client.get_deployment_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get deployment instance") from exc
    return GetDeploymentInstanceResult(
        instance_summary=resp.get("instanceSummary"),
    )


def get_deployment_target(
    deployment_id: str,
    target_id: str,
    region_name: str | None = None,
) -> GetDeploymentTargetResult:
    """Get deployment target.

    Args:
        deployment_id: Deployment id.
        target_id: Target id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    kwargs["targetId"] = target_id
    try:
        resp = client.get_deployment_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get deployment target") from exc
    return GetDeploymentTargetResult(
        deployment_target=resp.get("deploymentTarget"),
    )


def get_on_premises_instance(
    instance_name: str,
    region_name: str | None = None,
) -> GetOnPremisesInstanceResult:
    """Get on premises instance.

    Args:
        instance_name: Instance name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    try:
        resp = client.get_on_premises_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get on premises instance") from exc
    return GetOnPremisesInstanceResult(
        instance_info=resp.get("instanceInfo"),
    )


def list_deployment_configs(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDeploymentConfigsResult:
    """List deployment configs.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_deployment_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list deployment configs") from exc
    return ListDeploymentConfigsResult(
        deployment_configs_list=resp.get("deploymentConfigsList"),
        next_token=resp.get("nextToken"),
    )


def list_deployment_instances(
    deployment_id: str,
    *,
    next_token: str | None = None,
    instance_status_filter: list[str] | None = None,
    instance_type_filter: list[str] | None = None,
    region_name: str | None = None,
) -> ListDeploymentInstancesResult:
    """List deployment instances.

    Args:
        deployment_id: Deployment id.
        next_token: Next token.
        instance_status_filter: Instance status filter.
        instance_type_filter: Instance type filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if instance_status_filter is not None:
        kwargs["instanceStatusFilter"] = instance_status_filter
    if instance_type_filter is not None:
        kwargs["instanceTypeFilter"] = instance_type_filter
    try:
        resp = client.list_deployment_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list deployment instances") from exc
    return ListDeploymentInstancesResult(
        instances_list=resp.get("instancesList"),
        next_token=resp.get("nextToken"),
    )


def list_deployment_targets(
    deployment_id: str,
    *,
    next_token: str | None = None,
    target_filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListDeploymentTargetsResult:
    """List deployment targets.

    Args:
        deployment_id: Deployment id.
        next_token: Next token.
        target_filters: Target filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["deploymentId"] = deployment_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if target_filters is not None:
        kwargs["targetFilters"] = target_filters
    try:
        resp = client.list_deployment_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list deployment targets") from exc
    return ListDeploymentTargetsResult(
        target_ids=resp.get("targetIds"),
        next_token=resp.get("nextToken"),
    )


def list_git_hub_account_token_names(
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListGitHubAccountTokenNamesResult:
    """List git hub account token names.

    Args:
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_git_hub_account_token_names(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list git hub account token names") from exc
    return ListGitHubAccountTokenNamesResult(
        token_name_list=resp.get("tokenNameList"),
        next_token=resp.get("nextToken"),
    )


def list_on_premises_instances(
    *,
    registration_status: str | None = None,
    tag_filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListOnPremisesInstancesResult:
    """List on premises instances.

    Args:
        registration_status: Registration status.
        tag_filters: Tag filters.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if registration_status is not None:
        kwargs["registrationStatus"] = registration_status
    if tag_filters is not None:
        kwargs["tagFilters"] = tag_filters
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_on_premises_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list on premises instances") from exc
    return ListOnPremisesInstancesResult(
        instance_names=resp.get("instanceNames"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def put_lifecycle_event_hook_execution_status(
    *,
    deployment_id: str | None = None,
    lifecycle_event_hook_execution_id: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> PutLifecycleEventHookExecutionStatusResult:
    """Put lifecycle event hook execution status.

    Args:
        deployment_id: Deployment id.
        lifecycle_event_hook_execution_id: Lifecycle event hook execution id.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if deployment_id is not None:
        kwargs["deploymentId"] = deployment_id
    if lifecycle_event_hook_execution_id is not None:
        kwargs["lifecycleEventHookExecutionId"] = lifecycle_event_hook_execution_id
    if status is not None:
        kwargs["status"] = status
    try:
        resp = client.put_lifecycle_event_hook_execution_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put lifecycle event hook execution status") from exc
    return PutLifecycleEventHookExecutionStatusResult(
        lifecycle_event_hook_execution_id=resp.get("lifecycleEventHookExecutionId"),
    )


def register_on_premises_instance(
    instance_name: str,
    *,
    iam_session_arn: str | None = None,
    iam_user_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Register on premises instance.

    Args:
        instance_name: Instance name.
        iam_session_arn: Iam session arn.
        iam_user_arn: Iam user arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["instanceName"] = instance_name
    if iam_session_arn is not None:
        kwargs["iamSessionArn"] = iam_session_arn
    if iam_user_arn is not None:
        kwargs["iamUserArn"] = iam_user_arn
    try:
        client.register_on_premises_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register on premises instance") from exc
    return None


def remove_tags_from_on_premises_instances(
    tags: list[dict[str, Any]],
    instance_names: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags from on premises instances.

    Args:
        tags: Tags.
        instance_names: Instance names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["tags"] = tags
    kwargs["instanceNames"] = instance_names
    try:
        client.remove_tags_from_on_premises_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from on premises instances") from exc
    return None


def skip_wait_time_for_instance_termination(
    *,
    deployment_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Skip wait time for instance termination.

    Args:
        deployment_id: Deployment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if deployment_id is not None:
        kwargs["deploymentId"] = deployment_id
    try:
        client.skip_wait_time_for_instance_termination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to skip wait time for instance termination") from exc
    return None


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
    client = get_client("codedeploy", region_name)
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
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_application(
    *,
    application_name: str | None = None,
    new_application_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update application.

    Args:
        application_name: Application name.
        new_application_name: New application name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["applicationName"] = application_name
    if new_application_name is not None:
        kwargs["newApplicationName"] = new_application_name
    try:
        client.update_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application") from exc
    return None


def update_deployment_group(
    application_name: str,
    current_deployment_group_name: str,
    *,
    new_deployment_group_name: str | None = None,
    deployment_config_name: str | None = None,
    ec2_tag_filters: list[dict[str, Any]] | None = None,
    on_premises_instance_tag_filters: list[dict[str, Any]] | None = None,
    auto_scaling_groups: list[str] | None = None,
    service_role_arn: str | None = None,
    trigger_configurations: list[dict[str, Any]] | None = None,
    alarm_configuration: dict[str, Any] | None = None,
    auto_rollback_configuration: dict[str, Any] | None = None,
    outdated_instances_strategy: str | None = None,
    deployment_style: dict[str, Any] | None = None,
    blue_green_deployment_configuration: dict[str, Any] | None = None,
    load_balancer_info: dict[str, Any] | None = None,
    ec2_tag_set: dict[str, Any] | None = None,
    ecs_services: list[dict[str, Any]] | None = None,
    on_premises_tag_set: dict[str, Any] | None = None,
    termination_hook_enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateDeploymentGroupResult:
    """Update deployment group.

    Args:
        application_name: Application name.
        current_deployment_group_name: Current deployment group name.
        new_deployment_group_name: New deployment group name.
        deployment_config_name: Deployment config name.
        ec2_tag_filters: Ec2 tag filters.
        on_premises_instance_tag_filters: On premises instance tag filters.
        auto_scaling_groups: Auto scaling groups.
        service_role_arn: Service role arn.
        trigger_configurations: Trigger configurations.
        alarm_configuration: Alarm configuration.
        auto_rollback_configuration: Auto rollback configuration.
        outdated_instances_strategy: Outdated instances strategy.
        deployment_style: Deployment style.
        blue_green_deployment_configuration: Blue green deployment configuration.
        load_balancer_info: Load balancer info.
        ec2_tag_set: Ec2 tag set.
        ecs_services: Ecs services.
        on_premises_tag_set: On premises tag set.
        termination_hook_enabled: Termination hook enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codedeploy", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationName"] = application_name
    kwargs["currentDeploymentGroupName"] = current_deployment_group_name
    if new_deployment_group_name is not None:
        kwargs["newDeploymentGroupName"] = new_deployment_group_name
    if deployment_config_name is not None:
        kwargs["deploymentConfigName"] = deployment_config_name
    if ec2_tag_filters is not None:
        kwargs["ec2TagFilters"] = ec2_tag_filters
    if on_premises_instance_tag_filters is not None:
        kwargs["onPremisesInstanceTagFilters"] = on_premises_instance_tag_filters
    if auto_scaling_groups is not None:
        kwargs["autoScalingGroups"] = auto_scaling_groups
    if service_role_arn is not None:
        kwargs["serviceRoleArn"] = service_role_arn
    if trigger_configurations is not None:
        kwargs["triggerConfigurations"] = trigger_configurations
    if alarm_configuration is not None:
        kwargs["alarmConfiguration"] = alarm_configuration
    if auto_rollback_configuration is not None:
        kwargs["autoRollbackConfiguration"] = auto_rollback_configuration
    if outdated_instances_strategy is not None:
        kwargs["outdatedInstancesStrategy"] = outdated_instances_strategy
    if deployment_style is not None:
        kwargs["deploymentStyle"] = deployment_style
    if blue_green_deployment_configuration is not None:
        kwargs["blueGreenDeploymentConfiguration"] = blue_green_deployment_configuration
    if load_balancer_info is not None:
        kwargs["loadBalancerInfo"] = load_balancer_info
    if ec2_tag_set is not None:
        kwargs["ec2TagSet"] = ec2_tag_set
    if ecs_services is not None:
        kwargs["ecsServices"] = ecs_services
    if on_premises_tag_set is not None:
        kwargs["onPremisesTagSet"] = on_premises_tag_set
    if termination_hook_enabled is not None:
        kwargs["terminationHookEnabled"] = termination_hook_enabled
    try:
        resp = client.update_deployment_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update deployment group") from exc
    return UpdateDeploymentGroupResult(
        hooks_not_cleaned_up=resp.get("hooksNotCleanedUp"),
    )
