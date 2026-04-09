"""aws_util.emr — Amazon EMR (Elastic MapReduce) utilities.

Provides convenience wrappers around EMR cluster management, step execution,
instance group configuration, security, and auto-scaling operations with
Pydantic-modelled results.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "AddInstanceFleetResult",
    "BootstrapActionResult",
    "CancelStepsResult",
    "ClusterResult",
    "CreatePersistentAppUiResult",
    "CreateStudioResult",
    "DescribeJobFlowsResult",
    "DescribeNotebookExecutionResult",
    "DescribePersistentAppUiResult",
    "DescribeReleaseLabelResult",
    "DescribeSecurityConfigurationResult",
    "DescribeStudioResult",
    "GetAutoTerminationPolicyResult",
    "GetBlockPublicAccessConfigurationResult",
    "GetClusterSessionCredentialsResult",
    "GetManagedScalingPolicyResult",
    "GetOnClusterAppUiPresignedUrlResult",
    "GetPersistentAppUiPresignedUrlResult",
    "GetStudioSessionMappingResult",
    "InstanceGroupResult",
    "ListInstanceFleetsResult",
    "ListInstancesResult",
    "ListNotebookExecutionsResult",
    "ListReleaseLabelsResult",
    "ListStudioSessionMappingsResult",
    "ListStudiosResult",
    "ListSupportedInstanceTypesResult",
    "ModifyClusterResult",
    "SecurityConfigurationResult",
    "StartNotebookExecutionResult",
    "StepResult",
    "add_instance_fleet",
    "add_instance_groups",
    "add_job_flow_steps",
    "add_tags",
    "cancel_steps",
    "create_persistent_app_ui",
    "create_security_configuration",
    "create_studio",
    "create_studio_session_mapping",
    "delete_security_configuration",
    "delete_studio",
    "delete_studio_session_mapping",
    "describe_cluster",
    "describe_job_flows",
    "describe_notebook_execution",
    "describe_persistent_app_ui",
    "describe_release_label",
    "describe_security_configuration",
    "describe_step",
    "describe_studio",
    "get_auto_termination_policy",
    "get_block_public_access_configuration",
    "get_cluster_session_credentials",
    "get_managed_scaling_policy",
    "get_on_cluster_app_ui_presigned_url",
    "get_persistent_app_ui_presigned_url",
    "get_studio_session_mapping",
    "list_bootstrap_actions",
    "list_clusters",
    "list_instance_fleets",
    "list_instance_groups",
    "list_instances",
    "list_notebook_executions",
    "list_release_labels",
    "list_security_configurations",
    "list_steps",
    "list_studio_session_mappings",
    "list_studios",
    "list_supported_instance_types",
    "modify_cluster",
    "modify_instance_fleet",
    "modify_instance_groups",
    "put_auto_scaling_policy",
    "put_auto_termination_policy",
    "put_block_public_access_configuration",
    "put_managed_scaling_policy",
    "remove_auto_scaling_policy",
    "remove_auto_termination_policy",
    "remove_managed_scaling_policy",
    "remove_tags",
    "run_and_wait",
    "run_job_flow",
    "set_keep_job_flow_alive_when_no_steps",
    "set_termination_protection",
    "set_unhealthy_node_replacement",
    "set_visible_to_all_users",
    "start_notebook_execution",
    "stop_notebook_execution",
    "terminate_job_flows",
    "update_studio",
    "update_studio_session_mapping",
    "wait_for_cluster",
]

# ---------------------------------------------------------------------------
# Terminal states — clusters that will never transition further
# ---------------------------------------------------------------------------

_TERMINAL_STATES: frozenset[str] = frozenset(
    {
        "TERMINATED",
        "TERMINATED_WITH_ERRORS",
    }
)

_READY_STATES: frozenset[str] = frozenset(
    {
        "WAITING",
        "RUNNING",
    }
)

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ClusterResult(BaseModel):
    """Metadata for an EMR cluster."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    cluster_id: str
    name: str
    status: str
    state_change_reason: dict[str, Any] = {}
    normalized_instance_hours: int = 0
    log_uri: str | None = None
    release_label: str | None = None
    auto_terminate: bool = False
    termination_protected: bool = False
    tags: list[dict[str, str]] = []
    extra: dict[str, Any] = {}


class StepResult(BaseModel):
    """Metadata for an EMR step."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    step_id: str
    name: str
    status: str
    action_on_failure: str | None = None
    extra: dict[str, Any] = {}


class InstanceGroupResult(BaseModel):
    """Metadata for an EMR instance group."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    instance_group_id: str
    name: str
    market: str
    instance_role: str
    instance_type: str
    requested_instance_count: int = 0
    running_instance_count: int = 0
    status: str
    extra: dict[str, Any] = {}


class SecurityConfigurationResult(BaseModel):
    """Metadata for an EMR security configuration."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    name: str
    creation_date_time: str | None = None
    extra: dict[str, Any] = {}


class BootstrapActionResult(BaseModel):
    """Metadata for an EMR bootstrap action."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    name: str
    script_path: str
    args: list[str] = []
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_cluster(data: dict[str, Any]) -> ClusterResult:
    """Parse a raw EMR cluster dict into a :class:`ClusterResult`."""
    status_info = data.get("Status", {})
    state = status_info.get("State", "UNKNOWN")
    state_change = status_info.get("StateChangeReason", {})
    creation = data.get("NormalizedInstanceHours", 0)
    known_keys = {
        "Id",
        "Name",
        "Status",
        "NormalizedInstanceHours",
        "LogUri",
        "ReleaseLabel",
        "AutoTerminate",
        "TerminationProtected",
        "Tags",
    }
    return ClusterResult(
        cluster_id=data.get("Id", data.get("ClusterId", "")),
        name=data.get("Name", ""),
        status=state,
        state_change_reason=state_change,
        normalized_instance_hours=creation,
        log_uri=data.get("LogUri"),
        release_label=data.get("ReleaseLabel"),
        auto_terminate=data.get("AutoTerminate", False),
        termination_protected=data.get("TerminationProtected", False),
        tags=data.get("Tags", []),
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


def _parse_step(data: dict[str, Any]) -> StepResult:
    """Parse a raw EMR step dict into a :class:`StepResult`."""
    status_info = data.get("Status", {})
    state = status_info.get("State", "UNKNOWN")
    known_keys = {"Id", "Name", "Status", "ActionOnFailure"}
    return StepResult(
        step_id=data.get("Id", ""),
        name=data.get("Name", ""),
        status=state,
        action_on_failure=data.get("ActionOnFailure"),
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


def _parse_instance_group(data: dict[str, Any]) -> InstanceGroupResult:
    """Parse a raw EMR instance group dict into an :class:`InstanceGroupResult`."""
    status_info = data.get("Status", {})
    state = status_info.get("State", "UNKNOWN")
    known_keys = {
        "Id",
        "Name",
        "Market",
        "InstanceGroupType",
        "InstanceType",
        "RequestedInstanceCount",
        "RunningInstanceCount",
        "Status",
    }
    return InstanceGroupResult(
        instance_group_id=data.get("Id", ""),
        name=data.get("Name", ""),
        market=data.get("Market", ""),
        instance_role=data.get("InstanceGroupType", ""),
        instance_type=data.get("InstanceType", ""),
        requested_instance_count=data.get("RequestedInstanceCount", 0),
        running_instance_count=data.get("RunningInstanceCount", 0),
        status=state,
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


def _parse_security_configuration(
    data: dict[str, Any],
) -> SecurityConfigurationResult:
    """Parse a raw EMR security configuration dict."""
    created = data.get("CreationDateTime")
    known_keys = {"Name", "CreationDateTime"}
    return SecurityConfigurationResult(
        name=data.get("Name", ""),
        creation_date_time=str(created) if created is not None else None,
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


def _parse_bootstrap_action(data: dict[str, Any]) -> BootstrapActionResult:
    """Parse a raw EMR bootstrap action dict."""
    script_config = data.get("ScriptBootstrapAction", {})
    known_keys = {"Name", "ScriptBootstrapAction"}
    return BootstrapActionResult(
        name=data.get("Name", ""),
        script_path=script_config.get("Path", ""),
        args=script_config.get("Args", []),
        extra={k: v for k, v in data.items() if k not in known_keys},
    )


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


def run_job_flow(
    name: str,
    *,
    log_uri: str | None = None,
    release_label: str | None = None,
    instances: dict[str, Any] | None = None,
    steps: list[dict[str, Any]] | None = None,
    applications: list[dict[str, str]] | None = None,
    configurations: list[dict[str, Any]] | None = None,
    service_role: str | None = None,
    job_flow_role: str | None = None,
    tags: list[dict[str, str]] | None = None,
    visible_to_all_users: bool = True,
    region_name: str | None = None,
) -> str:
    """Launch a new EMR cluster (job flow).

    Args:
        name: Cluster name.
        log_uri: S3 URI for cluster logs.
        release_label: EMR release label (e.g. ``"emr-6.15.0"``).
        instances: Instance configuration dict.
        steps: Optional list of step configurations.
        applications: Applications to install (e.g. ``[{"Name": "Spark"}]``).
        configurations: Optional application configurations.
        service_role: IAM service role for EMR.
        job_flow_role: IAM role for EC2 instances.
        tags: Optional resource tags.
        visible_to_all_users: Whether the cluster is visible to all IAM users.
        region_name: AWS region override.

    Returns:
        The new cluster (job flow) ID string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "VisibleToAllUsers": visible_to_all_users,
    }
    if log_uri is not None:
        kwargs["LogUri"] = log_uri
    if release_label is not None:
        kwargs["ReleaseLabel"] = release_label
    if instances is not None:
        kwargs["Instances"] = instances
    if steps is not None:
        kwargs["Steps"] = steps
    if applications is not None:
        kwargs["Applications"] = applications
    if configurations is not None:
        kwargs["Configurations"] = configurations
    if service_role is not None:
        kwargs["ServiceRole"] = service_role
    if job_flow_role is not None:
        kwargs["JobFlowRole"] = job_flow_role
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = client.run_job_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"run_job_flow failed for {name!r}") from exc
    return resp["JobFlowId"]


def describe_cluster(
    cluster_id: str,
    *,
    region_name: str | None = None,
) -> ClusterResult:
    """Describe an EMR cluster.

    Args:
        cluster_id: The cluster identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.describe_cluster(ClusterId=cluster_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_cluster failed for {cluster_id!r}") from exc
    return _parse_cluster(resp["Cluster"])


def list_clusters(
    *,
    cluster_states: list[str] | None = None,
    region_name: str | None = None,
) -> list[ClusterResult]:
    """List EMR clusters, optionally filtered by state.

    Args:
        cluster_states: Optional list of states to filter by.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    results: list[ClusterResult] = []
    kwargs: dict[str, Any] = {}
    if cluster_states is not None:
        kwargs["ClusterStates"] = cluster_states
    try:
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate(**kwargs):
            for cluster in page.get("Clusters", []):
                results.append(_parse_cluster(cluster))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_clusters failed") from exc
    return results


def terminate_job_flows(
    job_flow_ids: list[str],
    *,
    region_name: str | None = None,
) -> None:
    """Terminate one or more EMR clusters.

    Args:
        job_flow_ids: List of cluster IDs to terminate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        client.terminate_job_flows(JobFlowIds=job_flow_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "terminate_job_flows failed") from exc


# ---------------------------------------------------------------------------
# Step operations
# ---------------------------------------------------------------------------


def add_job_flow_steps(
    job_flow_id: str,
    steps: list[dict[str, Any]],
    *,
    region_name: str | None = None,
) -> list[str]:
    """Add steps to a running EMR cluster.

    Args:
        job_flow_id: The cluster ID.
        steps: List of step configuration dicts.
        region_name: AWS region override.

    Returns:
        A list of step IDs for the newly added steps.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.add_job_flow_steps(JobFlowId=job_flow_id, Steps=steps)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"add_job_flow_steps failed for {job_flow_id!r}") from exc
    return resp["StepIds"]


def list_steps(
    cluster_id: str,
    *,
    step_states: list[str] | None = None,
    region_name: str | None = None,
) -> list[StepResult]:
    """List steps for an EMR cluster.

    Args:
        cluster_id: The cluster ID.
        step_states: Optional list of step states to filter by.
        region_name: AWS region override.

    Returns:
        A list of :class:`StepResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    results: list[StepResult] = []
    kwargs: dict[str, Any] = {"ClusterId": cluster_id}
    if step_states is not None:
        kwargs["StepStates"] = step_states
    try:
        paginator = client.get_paginator("list_steps")
        for page in paginator.paginate(**kwargs):
            for step in page.get("Steps", []):
                results.append(_parse_step(step))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_steps failed for {cluster_id!r}") from exc
    return results


def describe_step(
    cluster_id: str,
    step_id: str,
    *,
    region_name: str | None = None,
) -> StepResult:
    """Describe a specific step on an EMR cluster.

    Args:
        cluster_id: The cluster ID.
        step_id: The step ID.
        region_name: AWS region override.

    Returns:
        A :class:`StepResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.describe_step(ClusterId=cluster_id, StepId=step_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_step failed for {step_id!r}") from exc
    return _parse_step(resp["Step"])


# ---------------------------------------------------------------------------
# Instance group operations
# ---------------------------------------------------------------------------


def add_instance_groups(
    job_flow_id: str,
    instance_groups: list[dict[str, Any]],
    *,
    region_name: str | None = None,
) -> list[str]:
    """Add instance groups to an EMR cluster.

    Args:
        job_flow_id: The cluster ID.
        instance_groups: List of instance group configuration dicts.
        region_name: AWS region override.

    Returns:
        A list of instance group IDs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.add_instance_groups(
            JobFlowId=job_flow_id,
            InstanceGroups=instance_groups,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"add_instance_groups failed for {job_flow_id!r}") from exc
    return resp["InstanceGroupIds"]


def list_instance_groups(
    cluster_id: str,
    *,
    region_name: str | None = None,
) -> list[InstanceGroupResult]:
    """List instance groups for an EMR cluster.

    Args:
        cluster_id: The cluster ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    results: list[InstanceGroupResult] = []
    try:
        paginator = client.get_paginator("list_instance_groups")
        for page in paginator.paginate(ClusterId=cluster_id):
            for ig in page.get("InstanceGroups", []):
                results.append(_parse_instance_group(ig))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_instance_groups failed for {cluster_id!r}") from exc
    return results


def modify_instance_groups(
    instance_groups: list[dict[str, Any]],
    *,
    cluster_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Modify instance groups on an EMR cluster.

    Args:
        instance_groups: List of instance group modifications.
        cluster_id: Optional cluster ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {"InstanceGroups": instance_groups}
    if cluster_id is not None:
        kwargs["ClusterId"] = cluster_id
    try:
        client.modify_instance_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "modify_instance_groups failed") from exc


# ---------------------------------------------------------------------------
# Security configuration
# ---------------------------------------------------------------------------


def create_security_configuration(
    name: str,
    security_configuration: str,
    *,
    region_name: str | None = None,
) -> SecurityConfigurationResult:
    """Create an EMR security configuration.

    Args:
        name: Name for the security configuration.
        security_configuration: JSON string of the security configuration.
        region_name: AWS region override.

    Returns:
        A :class:`SecurityConfigurationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.create_security_configuration(
            Name=name,
            SecurityConfiguration=security_configuration,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_security_configuration failed for {name!r}") from exc
    return _parse_security_configuration(resp)


def list_security_configurations(
    *,
    region_name: str | None = None,
) -> list[SecurityConfigurationResult]:
    """List EMR security configurations.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`SecurityConfigurationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    results: list[SecurityConfigurationResult] = []
    try:
        paginator = client.get_paginator("list_security_configurations")
        for page in paginator.paginate():
            for sc in page.get("SecurityConfigurations", []):
                results.append(_parse_security_configuration(sc))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_security_configurations failed") from exc
    return results


# ---------------------------------------------------------------------------
# Termination protection
# ---------------------------------------------------------------------------


def set_termination_protection(
    job_flow_ids: list[str],
    termination_protected: bool,
    *,
    region_name: str | None = None,
) -> None:
    """Enable or disable termination protection for EMR clusters.

    Args:
        job_flow_ids: List of cluster IDs.
        termination_protected: Whether termination protection is enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        client.set_termination_protection(
            JobFlowIds=job_flow_ids,
            TerminationProtected=termination_protected,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "set_termination_protection failed") from exc


# ---------------------------------------------------------------------------
# Auto-scaling policy
# ---------------------------------------------------------------------------


def put_auto_scaling_policy(
    cluster_id: str,
    instance_group_id: str,
    auto_scaling_policy: dict[str, Any],
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Attach an auto-scaling policy to an EMR instance group.

    Args:
        cluster_id: The cluster ID.
        instance_group_id: The instance group ID.
        auto_scaling_policy: The auto-scaling policy configuration.
        region_name: AWS region override.

    Returns:
        The raw API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    try:
        resp = client.put_auto_scaling_policy(
            ClusterId=cluster_id,
            InstanceGroupId=instance_group_id,
            AutoScalingPolicy=auto_scaling_policy,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"put_auto_scaling_policy failed for {instance_group_id!r}"
        ) from exc
    return resp


# ---------------------------------------------------------------------------
# Bootstrap actions
# ---------------------------------------------------------------------------


def list_bootstrap_actions(
    cluster_id: str,
    *,
    region_name: str | None = None,
) -> list[BootstrapActionResult]:
    """List bootstrap actions for an EMR cluster.

    Args:
        cluster_id: The cluster ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`BootstrapActionResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    results: list[BootstrapActionResult] = []
    try:
        paginator = client.get_paginator("list_bootstrap_actions")
        for page in paginator.paginate(ClusterId=cluster_id):
            for ba in page.get("BootstrapActions", []):
                results.append(_parse_bootstrap_action(ba))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_bootstrap_actions failed for {cluster_id!r}") from exc
    return results


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


def wait_for_cluster(
    cluster_id: str,
    *,
    timeout: float = 900,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until an EMR cluster reaches WAITING/RUNNING or a terminal state.

    Args:
        cluster_id: The cluster ID.
        timeout: Maximum seconds to wait (default ``900``).
        poll_interval: Seconds between checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` in a ready or terminal state.

    Raises:
        AwsTimeoutError: If the cluster does not reach a ready state
            within the timeout.
        AwsServiceError: If the cluster reaches a terminal failure state.
    """
    deadline = time.monotonic() + timeout
    while True:
        cluster = describe_cluster(cluster_id, region_name=region_name)
        if cluster.status in _READY_STATES:
            return cluster
        if cluster.status in _TERMINAL_STATES:
            raise AwsServiceError(
                f"Cluster {cluster_id!r} reached terminal state {cluster.status!r}"
            )
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {cluster_id!r} did not become ready within "
                f"{timeout}s (current: {cluster.status!r})"
            )
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Composite operations
# ---------------------------------------------------------------------------


def run_and_wait(
    name: str,
    *,
    log_uri: str | None = None,
    release_label: str | None = None,
    instances: dict[str, Any] | None = None,
    steps: list[dict[str, Any]] | None = None,
    applications: list[dict[str, str]] | None = None,
    configurations: list[dict[str, Any]] | None = None,
    service_role: str | None = None,
    job_flow_role: str | None = None,
    tags: list[dict[str, str]] | None = None,
    visible_to_all_users: bool = True,
    timeout: float = 900,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> ClusterResult:
    """Launch an EMR cluster and wait until it is ready.

    This is a composite of :func:`run_job_flow` followed by
    :func:`wait_for_cluster`.

    Args:
        name: Cluster name.
        log_uri: S3 URI for cluster logs.
        release_label: EMR release label (e.g. ``"emr-6.15.0"``).
        instances: Instance configuration dict.
        steps: Optional list of step configurations.
        applications: Applications to install.
        configurations: Optional application configurations.
        service_role: IAM service role for EMR.
        job_flow_role: IAM role for EC2 instances.
        tags: Optional resource tags.
        visible_to_all_users: Whether the cluster is visible to all IAM users.
        timeout: Maximum seconds to wait for ready state (default ``900``).
        poll_interval: Seconds between status checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` once the cluster is ready.

    Raises:
        AwsTimeoutError: If the cluster does not reach a ready state.
        AwsServiceError: If the cluster reaches a terminal failure state.
    """
    cluster_id = run_job_flow(
        name,
        log_uri=log_uri,
        release_label=release_label,
        instances=instances,
        steps=steps,
        applications=applications,
        configurations=configurations,
        service_role=service_role,
        job_flow_role=job_flow_role,
        tags=tags,
        visible_to_all_users=visible_to_all_users,
        region_name=region_name,
    )
    return wait_for_cluster(
        cluster_id,
        timeout=timeout,
        poll_interval=poll_interval,
        region_name=region_name,
    )


class AddInstanceFleetResult(BaseModel):
    """Result of add_instance_fleet."""

    model_config = ConfigDict(frozen=True)

    cluster_id: str | None = None
    instance_fleet_id: str | None = None
    cluster_arn: str | None = None


class CancelStepsResult(BaseModel):
    """Result of cancel_steps."""

    model_config = ConfigDict(frozen=True)

    cancel_steps_info_list: list[dict[str, Any]] | None = None


class CreatePersistentAppUiResult(BaseModel):
    """Result of create_persistent_app_ui."""

    model_config = ConfigDict(frozen=True)

    persistent_app_ui_id: str | None = None
    runtime_role_enabled_cluster: bool | None = None


class CreateStudioResult(BaseModel):
    """Result of create_studio."""

    model_config = ConfigDict(frozen=True)

    studio_id: str | None = None
    url: str | None = None


class DescribeJobFlowsResult(BaseModel):
    """Result of describe_job_flows."""

    model_config = ConfigDict(frozen=True)

    job_flows: list[dict[str, Any]] | None = None


class DescribeNotebookExecutionResult(BaseModel):
    """Result of describe_notebook_execution."""

    model_config = ConfigDict(frozen=True)

    notebook_execution: dict[str, Any] | None = None


class DescribePersistentAppUiResult(BaseModel):
    """Result of describe_persistent_app_ui."""

    model_config = ConfigDict(frozen=True)

    persistent_app_ui: dict[str, Any] | None = None


class DescribeReleaseLabelResult(BaseModel):
    """Result of describe_release_label."""

    model_config = ConfigDict(frozen=True)

    release_label: str | None = None
    applications: list[dict[str, Any]] | None = None
    next_token: str | None = None
    available_os_releases: list[dict[str, Any]] | None = None


class DescribeSecurityConfigurationResult(BaseModel):
    """Result of describe_security_configuration."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    security_configuration: str | None = None
    creation_date_time: str | None = None


class DescribeStudioResult(BaseModel):
    """Result of describe_studio."""

    model_config = ConfigDict(frozen=True)

    studio: dict[str, Any] | None = None


class GetAutoTerminationPolicyResult(BaseModel):
    """Result of get_auto_termination_policy."""

    model_config = ConfigDict(frozen=True)

    auto_termination_policy: dict[str, Any] | None = None


class GetBlockPublicAccessConfigurationResult(BaseModel):
    """Result of get_block_public_access_configuration."""

    model_config = ConfigDict(frozen=True)

    block_public_access_configuration: dict[str, Any] | None = None
    block_public_access_configuration_metadata: dict[str, Any] | None = None


class GetClusterSessionCredentialsResult(BaseModel):
    """Result of get_cluster_session_credentials."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    expires_at: str | None = None


class GetManagedScalingPolicyResult(BaseModel):
    """Result of get_managed_scaling_policy."""

    model_config = ConfigDict(frozen=True)

    managed_scaling_policy: dict[str, Any] | None = None


class GetOnClusterAppUiPresignedUrlResult(BaseModel):
    """Result of get_on_cluster_app_ui_presigned_url."""

    model_config = ConfigDict(frozen=True)

    presigned_url_ready: bool | None = None
    presigned_url: str | None = None


class GetPersistentAppUiPresignedUrlResult(BaseModel):
    """Result of get_persistent_app_ui_presigned_url."""

    model_config = ConfigDict(frozen=True)

    presigned_url_ready: bool | None = None
    presigned_url: str | None = None


class GetStudioSessionMappingResult(BaseModel):
    """Result of get_studio_session_mapping."""

    model_config = ConfigDict(frozen=True)

    session_mapping: dict[str, Any] | None = None


class ListInstanceFleetsResult(BaseModel):
    """Result of list_instance_fleets."""

    model_config = ConfigDict(frozen=True)

    instance_fleets: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListInstancesResult(BaseModel):
    """Result of list_instances."""

    model_config = ConfigDict(frozen=True)

    instances: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListNotebookExecutionsResult(BaseModel):
    """Result of list_notebook_executions."""

    model_config = ConfigDict(frozen=True)

    notebook_executions: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListReleaseLabelsResult(BaseModel):
    """Result of list_release_labels."""

    model_config = ConfigDict(frozen=True)

    release_labels: list[str] | None = None
    next_token: str | None = None


class ListStudioSessionMappingsResult(BaseModel):
    """Result of list_studio_session_mappings."""

    model_config = ConfigDict(frozen=True)

    session_mappings: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListStudiosResult(BaseModel):
    """Result of list_studios."""

    model_config = ConfigDict(frozen=True)

    studios: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListSupportedInstanceTypesResult(BaseModel):
    """Result of list_supported_instance_types."""

    model_config = ConfigDict(frozen=True)

    supported_instance_types: list[dict[str, Any]] | None = None
    marker: str | None = None


class ModifyClusterResult(BaseModel):
    """Result of modify_cluster."""

    model_config = ConfigDict(frozen=True)

    step_concurrency_level: int | None = None
    extended_support: bool | None = None


class StartNotebookExecutionResult(BaseModel):
    """Result of start_notebook_execution."""

    model_config = ConfigDict(frozen=True)

    notebook_execution_id: str | None = None


def add_instance_fleet(
    cluster_id: str,
    instance_fleet: dict[str, Any],
    region_name: str | None = None,
) -> AddInstanceFleetResult:
    """Add instance fleet.

    Args:
        cluster_id: Cluster id.
        instance_fleet: Instance fleet.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    kwargs["InstanceFleet"] = instance_fleet
    try:
        resp = client.add_instance_fleet(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add instance fleet") from exc
    return AddInstanceFleetResult(
        cluster_id=resp.get("ClusterId"),
        instance_fleet_id=resp.get("InstanceFleetId"),
        cluster_arn=resp.get("ClusterArn"),
    )


def add_tags(
    resource_id: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags.

    Args:
        resource_id: Resource id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["Tags"] = tags
    try:
        client.add_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add tags") from exc
    return None


def cancel_steps(
    cluster_id: str,
    step_ids: list[str],
    *,
    step_cancellation_option: str | None = None,
    region_name: str | None = None,
) -> CancelStepsResult:
    """Cancel steps.

    Args:
        cluster_id: Cluster id.
        step_ids: Step ids.
        step_cancellation_option: Step cancellation option.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    kwargs["StepIds"] = step_ids
    if step_cancellation_option is not None:
        kwargs["StepCancellationOption"] = step_cancellation_option
    try:
        resp = client.cancel_steps(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel steps") from exc
    return CancelStepsResult(
        cancel_steps_info_list=resp.get("CancelStepsInfoList"),
    )


def create_persistent_app_ui(
    target_resource_arn: str,
    *,
    emr_containers_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    x_referer: str | None = None,
    profiler_type: str | None = None,
    region_name: str | None = None,
) -> CreatePersistentAppUiResult:
    """Create persistent app ui.

    Args:
        target_resource_arn: Target resource arn.
        emr_containers_config: Emr containers config.
        tags: Tags.
        x_referer: X referer.
        profiler_type: Profiler type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetResourceArn"] = target_resource_arn
    if emr_containers_config is not None:
        kwargs["EMRContainersConfig"] = emr_containers_config
    if tags is not None:
        kwargs["Tags"] = tags
    if x_referer is not None:
        kwargs["XReferer"] = x_referer
    if profiler_type is not None:
        kwargs["ProfilerType"] = profiler_type
    try:
        resp = client.create_persistent_app_ui(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create persistent app ui") from exc
    return CreatePersistentAppUiResult(
        persistent_app_ui_id=resp.get("PersistentAppUIId"),
        runtime_role_enabled_cluster=resp.get("RuntimeRoleEnabledCluster"),
    )


def create_studio(
    name: str,
    auth_mode: str,
    vpc_id: str,
    subnet_ids: list[str],
    service_role: str,
    workspace_security_group_id: str,
    engine_security_group_id: str,
    default_s3_location: str,
    *,
    description: str | None = None,
    user_role: str | None = None,
    idp_auth_url: str | None = None,
    idp_relay_state_parameter_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    trusted_identity_propagation_enabled: bool | None = None,
    idc_user_assignment: str | None = None,
    idc_instance_arn: str | None = None,
    encryption_key_arn: str | None = None,
    region_name: str | None = None,
) -> CreateStudioResult:
    """Create studio.

    Args:
        name: Name.
        auth_mode: Auth mode.
        vpc_id: Vpc id.
        subnet_ids: Subnet ids.
        service_role: Service role.
        workspace_security_group_id: Workspace security group id.
        engine_security_group_id: Engine security group id.
        default_s3_location: Default s3 location.
        description: Description.
        user_role: User role.
        idp_auth_url: Idp auth url.
        idp_relay_state_parameter_name: Idp relay state parameter name.
        tags: Tags.
        trusted_identity_propagation_enabled: Trusted identity propagation enabled.
        idc_user_assignment: Idc user assignment.
        idc_instance_arn: Idc instance arn.
        encryption_key_arn: Encryption key arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["AuthMode"] = auth_mode
    kwargs["VpcId"] = vpc_id
    kwargs["SubnetIds"] = subnet_ids
    kwargs["ServiceRole"] = service_role
    kwargs["WorkspaceSecurityGroupId"] = workspace_security_group_id
    kwargs["EngineSecurityGroupId"] = engine_security_group_id
    kwargs["DefaultS3Location"] = default_s3_location
    if description is not None:
        kwargs["Description"] = description
    if user_role is not None:
        kwargs["UserRole"] = user_role
    if idp_auth_url is not None:
        kwargs["IdpAuthUrl"] = idp_auth_url
    if idp_relay_state_parameter_name is not None:
        kwargs["IdpRelayStateParameterName"] = idp_relay_state_parameter_name
    if tags is not None:
        kwargs["Tags"] = tags
    if trusted_identity_propagation_enabled is not None:
        kwargs["TrustedIdentityPropagationEnabled"] = trusted_identity_propagation_enabled
    if idc_user_assignment is not None:
        kwargs["IdcUserAssignment"] = idc_user_assignment
    if idc_instance_arn is not None:
        kwargs["IdcInstanceArn"] = idc_instance_arn
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    try:
        resp = client.create_studio(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create studio") from exc
    return CreateStudioResult(
        studio_id=resp.get("StudioId"),
        url=resp.get("Url"),
    )


def create_studio_session_mapping(
    studio_id: str,
    identity_type: str,
    session_policy_arn: str,
    *,
    identity_id: str | None = None,
    identity_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create studio session mapping.

    Args:
        studio_id: Studio id.
        identity_type: Identity type.
        session_policy_arn: Session policy arn.
        identity_id: Identity id.
        identity_name: Identity name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    kwargs["IdentityType"] = identity_type
    kwargs["SessionPolicyArn"] = session_policy_arn
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if identity_name is not None:
        kwargs["IdentityName"] = identity_name
    try:
        client.create_studio_session_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create studio session mapping") from exc
    return None


def delete_security_configuration(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete security configuration.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_security_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete security configuration") from exc
    return None


def delete_studio(
    studio_id: str,
    region_name: str | None = None,
) -> None:
    """Delete studio.

    Args:
        studio_id: Studio id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    try:
        client.delete_studio(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete studio") from exc
    return None


def delete_studio_session_mapping(
    studio_id: str,
    identity_type: str,
    *,
    identity_id: str | None = None,
    identity_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete studio session mapping.

    Args:
        studio_id: Studio id.
        identity_type: Identity type.
        identity_id: Identity id.
        identity_name: Identity name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    kwargs["IdentityType"] = identity_type
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if identity_name is not None:
        kwargs["IdentityName"] = identity_name
    try:
        client.delete_studio_session_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete studio session mapping") from exc
    return None


def describe_job_flows(
    *,
    created_after: str | None = None,
    created_before: str | None = None,
    job_flow_ids: list[str] | None = None,
    job_flow_states: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeJobFlowsResult:
    """Describe job flows.

    Args:
        created_after: Created after.
        created_before: Created before.
        job_flow_ids: Job flow ids.
        job_flow_states: Job flow states.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if created_after is not None:
        kwargs["CreatedAfter"] = created_after
    if created_before is not None:
        kwargs["CreatedBefore"] = created_before
    if job_flow_ids is not None:
        kwargs["JobFlowIds"] = job_flow_ids
    if job_flow_states is not None:
        kwargs["JobFlowStates"] = job_flow_states
    try:
        resp = client.describe_job_flows(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe job flows") from exc
    return DescribeJobFlowsResult(
        job_flows=resp.get("JobFlows"),
    )


def describe_notebook_execution(
    notebook_execution_id: str,
    region_name: str | None = None,
) -> DescribeNotebookExecutionResult:
    """Describe notebook execution.

    Args:
        notebook_execution_id: Notebook execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookExecutionId"] = notebook_execution_id
    try:
        resp = client.describe_notebook_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe notebook execution") from exc
    return DescribeNotebookExecutionResult(
        notebook_execution=resp.get("NotebookExecution"),
    )


def describe_persistent_app_ui(
    persistent_app_ui_id: str,
    region_name: str | None = None,
) -> DescribePersistentAppUiResult:
    """Describe persistent app ui.

    Args:
        persistent_app_ui_id: Persistent app ui id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PersistentAppUIId"] = persistent_app_ui_id
    try:
        resp = client.describe_persistent_app_ui(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe persistent app ui") from exc
    return DescribePersistentAppUiResult(
        persistent_app_ui=resp.get("PersistentAppUI"),
    )


def describe_release_label(
    *,
    release_label: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeReleaseLabelResult:
    """Describe release label.

    Args:
        release_label: Release label.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if release_label is not None:
        kwargs["ReleaseLabel"] = release_label
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_release_label(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe release label") from exc
    return DescribeReleaseLabelResult(
        release_label=resp.get("ReleaseLabel"),
        applications=resp.get("Applications"),
        next_token=resp.get("NextToken"),
        available_os_releases=resp.get("AvailableOSReleases"),
    )


def describe_security_configuration(
    name: str,
    region_name: str | None = None,
) -> DescribeSecurityConfigurationResult:
    """Describe security configuration.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_security_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe security configuration") from exc
    return DescribeSecurityConfigurationResult(
        name=resp.get("Name"),
        security_configuration=resp.get("SecurityConfiguration"),
        creation_date_time=resp.get("CreationDateTime"),
    )


def describe_studio(
    studio_id: str,
    region_name: str | None = None,
) -> DescribeStudioResult:
    """Describe studio.

    Args:
        studio_id: Studio id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    try:
        resp = client.describe_studio(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe studio") from exc
    return DescribeStudioResult(
        studio=resp.get("Studio"),
    )


def get_auto_termination_policy(
    cluster_id: str,
    region_name: str | None = None,
) -> GetAutoTerminationPolicyResult:
    """Get auto termination policy.

    Args:
        cluster_id: Cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    try:
        resp = client.get_auto_termination_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get auto termination policy") from exc
    return GetAutoTerminationPolicyResult(
        auto_termination_policy=resp.get("AutoTerminationPolicy"),
    )


def get_block_public_access_configuration(
    region_name: str | None = None,
) -> GetBlockPublicAccessConfigurationResult:
    """Get block public access configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_block_public_access_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get block public access configuration") from exc
    return GetBlockPublicAccessConfigurationResult(
        block_public_access_configuration=resp.get("BlockPublicAccessConfiguration"),
        block_public_access_configuration_metadata=resp.get(
            "BlockPublicAccessConfigurationMetadata"
        ),
    )


def get_cluster_session_credentials(
    cluster_id: str,
    *,
    execution_role_arn: str | None = None,
    region_name: str | None = None,
) -> GetClusterSessionCredentialsResult:
    """Get cluster session credentials.

    Args:
        cluster_id: Cluster id.
        execution_role_arn: Execution role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if execution_role_arn is not None:
        kwargs["ExecutionRoleArn"] = execution_role_arn
    try:
        resp = client.get_cluster_session_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get cluster session credentials") from exc
    return GetClusterSessionCredentialsResult(
        credentials=resp.get("Credentials"),
        expires_at=resp.get("ExpiresAt"),
    )


def get_managed_scaling_policy(
    cluster_id: str,
    region_name: str | None = None,
) -> GetManagedScalingPolicyResult:
    """Get managed scaling policy.

    Args:
        cluster_id: Cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    try:
        resp = client.get_managed_scaling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get managed scaling policy") from exc
    return GetManagedScalingPolicyResult(
        managed_scaling_policy=resp.get("ManagedScalingPolicy"),
    )


def get_on_cluster_app_ui_presigned_url(
    cluster_id: str,
    *,
    on_cluster_app_ui_type: str | None = None,
    application_id: str | None = None,
    execution_role_arn: str | None = None,
    region_name: str | None = None,
) -> GetOnClusterAppUiPresignedUrlResult:
    """Get on cluster app ui presigned url.

    Args:
        cluster_id: Cluster id.
        on_cluster_app_ui_type: On cluster app ui type.
        application_id: Application id.
        execution_role_arn: Execution role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if on_cluster_app_ui_type is not None:
        kwargs["OnClusterAppUIType"] = on_cluster_app_ui_type
    if application_id is not None:
        kwargs["ApplicationId"] = application_id
    if execution_role_arn is not None:
        kwargs["ExecutionRoleArn"] = execution_role_arn
    try:
        resp = client.get_on_cluster_app_ui_presigned_url(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get on cluster app ui presigned url") from exc
    return GetOnClusterAppUiPresignedUrlResult(
        presigned_url_ready=resp.get("PresignedURLReady"),
        presigned_url=resp.get("PresignedURL"),
    )


def get_persistent_app_ui_presigned_url(
    persistent_app_ui_id: str,
    *,
    persistent_app_ui_type: str | None = None,
    application_id: str | None = None,
    auth_proxy_call: bool | None = None,
    execution_role_arn: str | None = None,
    region_name: str | None = None,
) -> GetPersistentAppUiPresignedUrlResult:
    """Get persistent app ui presigned url.

    Args:
        persistent_app_ui_id: Persistent app ui id.
        persistent_app_ui_type: Persistent app ui type.
        application_id: Application id.
        auth_proxy_call: Auth proxy call.
        execution_role_arn: Execution role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PersistentAppUIId"] = persistent_app_ui_id
    if persistent_app_ui_type is not None:
        kwargs["PersistentAppUIType"] = persistent_app_ui_type
    if application_id is not None:
        kwargs["ApplicationId"] = application_id
    if auth_proxy_call is not None:
        kwargs["AuthProxyCall"] = auth_proxy_call
    if execution_role_arn is not None:
        kwargs["ExecutionRoleArn"] = execution_role_arn
    try:
        resp = client.get_persistent_app_ui_presigned_url(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get persistent app ui presigned url") from exc
    return GetPersistentAppUiPresignedUrlResult(
        presigned_url_ready=resp.get("PresignedURLReady"),
        presigned_url=resp.get("PresignedURL"),
    )


def get_studio_session_mapping(
    studio_id: str,
    identity_type: str,
    *,
    identity_id: str | None = None,
    identity_name: str | None = None,
    region_name: str | None = None,
) -> GetStudioSessionMappingResult:
    """Get studio session mapping.

    Args:
        studio_id: Studio id.
        identity_type: Identity type.
        identity_id: Identity id.
        identity_name: Identity name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    kwargs["IdentityType"] = identity_type
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if identity_name is not None:
        kwargs["IdentityName"] = identity_name
    try:
        resp = client.get_studio_session_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get studio session mapping") from exc
    return GetStudioSessionMappingResult(
        session_mapping=resp.get("SessionMapping"),
    )


def list_instance_fleets(
    cluster_id: str,
    *,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListInstanceFleetsResult:
    """List instance fleets.

    Args:
        cluster_id: Cluster id.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_instance_fleets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list instance fleets") from exc
    return ListInstanceFleetsResult(
        instance_fleets=resp.get("InstanceFleets"),
        marker=resp.get("Marker"),
    )


def list_instances(
    cluster_id: str,
    *,
    instance_group_id: str | None = None,
    instance_group_types: list[str] | None = None,
    instance_fleet_id: str | None = None,
    instance_fleet_type: str | None = None,
    instance_states: list[str] | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListInstancesResult:
    """List instances.

    Args:
        cluster_id: Cluster id.
        instance_group_id: Instance group id.
        instance_group_types: Instance group types.
        instance_fleet_id: Instance fleet id.
        instance_fleet_type: Instance fleet type.
        instance_states: Instance states.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if instance_group_id is not None:
        kwargs["InstanceGroupId"] = instance_group_id
    if instance_group_types is not None:
        kwargs["InstanceGroupTypes"] = instance_group_types
    if instance_fleet_id is not None:
        kwargs["InstanceFleetId"] = instance_fleet_id
    if instance_fleet_type is not None:
        kwargs["InstanceFleetType"] = instance_fleet_type
    if instance_states is not None:
        kwargs["InstanceStates"] = instance_states
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list instances") from exc
    return ListInstancesResult(
        instances=resp.get("Instances"),
        marker=resp.get("Marker"),
    )


def list_notebook_executions(
    *,
    editor_id: str | None = None,
    status: str | None = None,
    from_value: str | None = None,
    to: str | None = None,
    marker: str | None = None,
    execution_engine_id: str | None = None,
    region_name: str | None = None,
) -> ListNotebookExecutionsResult:
    """List notebook executions.

    Args:
        editor_id: Editor id.
        status: Status.
        from_value: From value.
        to: To.
        marker: Marker.
        execution_engine_id: Execution engine id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if editor_id is not None:
        kwargs["EditorId"] = editor_id
    if status is not None:
        kwargs["Status"] = status
    if from_value is not None:
        kwargs["From"] = from_value
    if to is not None:
        kwargs["To"] = to
    if marker is not None:
        kwargs["Marker"] = marker
    if execution_engine_id is not None:
        kwargs["ExecutionEngineId"] = execution_engine_id
    try:
        resp = client.list_notebook_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list notebook executions") from exc
    return ListNotebookExecutionsResult(
        notebook_executions=resp.get("NotebookExecutions"),
        marker=resp.get("Marker"),
    )


def list_release_labels(
    *,
    filters: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListReleaseLabelsResult:
    """List release labels.

    Args:
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_release_labels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list release labels") from exc
    return ListReleaseLabelsResult(
        release_labels=resp.get("ReleaseLabels"),
        next_token=resp.get("NextToken"),
    )


def list_studio_session_mappings(
    *,
    studio_id: str | None = None,
    identity_type: str | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListStudioSessionMappingsResult:
    """List studio session mappings.

    Args:
        studio_id: Studio id.
        identity_type: Identity type.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if studio_id is not None:
        kwargs["StudioId"] = studio_id
    if identity_type is not None:
        kwargs["IdentityType"] = identity_type
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_studio_session_mappings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list studio session mappings") from exc
    return ListStudioSessionMappingsResult(
        session_mappings=resp.get("SessionMappings"),
        marker=resp.get("Marker"),
    )


def list_studios(
    *,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListStudiosResult:
    """List studios.

    Args:
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_studios(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list studios") from exc
    return ListStudiosResult(
        studios=resp.get("Studios"),
        marker=resp.get("Marker"),
    )


def list_supported_instance_types(
    release_label: str,
    *,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListSupportedInstanceTypesResult:
    """List supported instance types.

    Args:
        release_label: Release label.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReleaseLabel"] = release_label
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_supported_instance_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list supported instance types") from exc
    return ListSupportedInstanceTypesResult(
        supported_instance_types=resp.get("SupportedInstanceTypes"),
        marker=resp.get("Marker"),
    )


def modify_cluster(
    cluster_id: str,
    *,
    step_concurrency_level: int | None = None,
    extended_support: bool | None = None,
    region_name: str | None = None,
) -> ModifyClusterResult:
    """Modify cluster.

    Args:
        cluster_id: Cluster id.
        step_concurrency_level: Step concurrency level.
        extended_support: Extended support.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if step_concurrency_level is not None:
        kwargs["StepConcurrencyLevel"] = step_concurrency_level
    if extended_support is not None:
        kwargs["ExtendedSupport"] = extended_support
    try:
        resp = client.modify_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster") from exc
    return ModifyClusterResult(
        step_concurrency_level=resp.get("StepConcurrencyLevel"),
        extended_support=resp.get("ExtendedSupport"),
    )


def modify_instance_fleet(
    cluster_id: str,
    instance_fleet: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Modify instance fleet.

    Args:
        cluster_id: Cluster id.
        instance_fleet: Instance fleet.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    kwargs["InstanceFleet"] = instance_fleet
    try:
        client.modify_instance_fleet(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify instance fleet") from exc
    return None


def put_auto_termination_policy(
    cluster_id: str,
    *,
    auto_termination_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put auto termination policy.

    Args:
        cluster_id: Cluster id.
        auto_termination_policy: Auto termination policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    if auto_termination_policy is not None:
        kwargs["AutoTerminationPolicy"] = auto_termination_policy
    try:
        client.put_auto_termination_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put auto termination policy") from exc
    return None


def put_block_public_access_configuration(
    block_public_access_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put block public access configuration.

    Args:
        block_public_access_configuration: Block public access configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlockPublicAccessConfiguration"] = block_public_access_configuration
    try:
        client.put_block_public_access_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put block public access configuration") from exc
    return None


def put_managed_scaling_policy(
    cluster_id: str,
    managed_scaling_policy: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put managed scaling policy.

    Args:
        cluster_id: Cluster id.
        managed_scaling_policy: Managed scaling policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    kwargs["ManagedScalingPolicy"] = managed_scaling_policy
    try:
        client.put_managed_scaling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put managed scaling policy") from exc
    return None


def remove_auto_scaling_policy(
    cluster_id: str,
    instance_group_id: str,
    region_name: str | None = None,
) -> None:
    """Remove auto scaling policy.

    Args:
        cluster_id: Cluster id.
        instance_group_id: Instance group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    kwargs["InstanceGroupId"] = instance_group_id
    try:
        client.remove_auto_scaling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove auto scaling policy") from exc
    return None


def remove_auto_termination_policy(
    cluster_id: str,
    region_name: str | None = None,
) -> None:
    """Remove auto termination policy.

    Args:
        cluster_id: Cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    try:
        client.remove_auto_termination_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove auto termination policy") from exc
    return None


def remove_managed_scaling_policy(
    cluster_id: str,
    region_name: str | None = None,
) -> None:
    """Remove managed scaling policy.

    Args:
        cluster_id: Cluster id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterId"] = cluster_id
    try:
        client.remove_managed_scaling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove managed scaling policy") from exc
    return None


def remove_tags(
    resource_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags.

    Args:
        resource_id: Resource id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagKeys"] = tag_keys
    try:
        client.remove_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags") from exc
    return None


def set_keep_job_flow_alive_when_no_steps(
    job_flow_ids: list[str],
    keep_job_flow_alive_when_no_steps: bool,
    region_name: str | None = None,
) -> None:
    """Set keep job flow alive when no steps.

    Args:
        job_flow_ids: Job flow ids.
        keep_job_flow_alive_when_no_steps: Keep job flow alive when no steps.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobFlowIds"] = job_flow_ids
    kwargs["KeepJobFlowAliveWhenNoSteps"] = keep_job_flow_alive_when_no_steps
    try:
        client.set_keep_job_flow_alive_when_no_steps(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set keep job flow alive when no steps") from exc
    return None


def set_unhealthy_node_replacement(
    job_flow_ids: list[str],
    unhealthy_node_replacement: bool,
    region_name: str | None = None,
) -> None:
    """Set unhealthy node replacement.

    Args:
        job_flow_ids: Job flow ids.
        unhealthy_node_replacement: Unhealthy node replacement.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobFlowIds"] = job_flow_ids
    kwargs["UnhealthyNodeReplacement"] = unhealthy_node_replacement
    try:
        client.set_unhealthy_node_replacement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set unhealthy node replacement") from exc
    return None


def set_visible_to_all_users(
    job_flow_ids: list[str],
    visible_to_all_users: bool,
    region_name: str | None = None,
) -> None:
    """Set visible to all users.

    Args:
        job_flow_ids: Job flow ids.
        visible_to_all_users: Visible to all users.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobFlowIds"] = job_flow_ids
    kwargs["VisibleToAllUsers"] = visible_to_all_users
    try:
        client.set_visible_to_all_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set visible to all users") from exc
    return None


def start_notebook_execution(
    execution_engine: dict[str, Any],
    service_role: str,
    *,
    editor_id: str | None = None,
    relative_path: str | None = None,
    notebook_execution_name: str | None = None,
    notebook_params: str | None = None,
    notebook_instance_security_group_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    notebook_s3_location: dict[str, Any] | None = None,
    output_notebook_s3_location: dict[str, Any] | None = None,
    output_notebook_format: str | None = None,
    environment_variables: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartNotebookExecutionResult:
    """Start notebook execution.

    Args:
        execution_engine: Execution engine.
        service_role: Service role.
        editor_id: Editor id.
        relative_path: Relative path.
        notebook_execution_name: Notebook execution name.
        notebook_params: Notebook params.
        notebook_instance_security_group_id: Notebook instance security group id.
        tags: Tags.
        notebook_s3_location: Notebook s3 location.
        output_notebook_s3_location: Output notebook s3 location.
        output_notebook_format: Output notebook format.
        environment_variables: Environment variables.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExecutionEngine"] = execution_engine
    kwargs["ServiceRole"] = service_role
    if editor_id is not None:
        kwargs["EditorId"] = editor_id
    if relative_path is not None:
        kwargs["RelativePath"] = relative_path
    if notebook_execution_name is not None:
        kwargs["NotebookExecutionName"] = notebook_execution_name
    if notebook_params is not None:
        kwargs["NotebookParams"] = notebook_params
    if notebook_instance_security_group_id is not None:
        kwargs["NotebookInstanceSecurityGroupId"] = notebook_instance_security_group_id
    if tags is not None:
        kwargs["Tags"] = tags
    if notebook_s3_location is not None:
        kwargs["NotebookS3Location"] = notebook_s3_location
    if output_notebook_s3_location is not None:
        kwargs["OutputNotebookS3Location"] = output_notebook_s3_location
    if output_notebook_format is not None:
        kwargs["OutputNotebookFormat"] = output_notebook_format
    if environment_variables is not None:
        kwargs["EnvironmentVariables"] = environment_variables
    try:
        resp = client.start_notebook_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start notebook execution") from exc
    return StartNotebookExecutionResult(
        notebook_execution_id=resp.get("NotebookExecutionId"),
    )


def stop_notebook_execution(
    notebook_execution_id: str,
    region_name: str | None = None,
) -> None:
    """Stop notebook execution.

    Args:
        notebook_execution_id: Notebook execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookExecutionId"] = notebook_execution_id
    try:
        client.stop_notebook_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop notebook execution") from exc
    return None


def update_studio(
    studio_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    subnet_ids: list[str] | None = None,
    default_s3_location: str | None = None,
    encryption_key_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update studio.

    Args:
        studio_id: Studio id.
        name: Name.
        description: Description.
        subnet_ids: Subnet ids.
        default_s3_location: Default s3 location.
        encryption_key_arn: Encryption key arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if subnet_ids is not None:
        kwargs["SubnetIds"] = subnet_ids
    if default_s3_location is not None:
        kwargs["DefaultS3Location"] = default_s3_location
    if encryption_key_arn is not None:
        kwargs["EncryptionKeyArn"] = encryption_key_arn
    try:
        client.update_studio(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update studio") from exc
    return None


def update_studio_session_mapping(
    studio_id: str,
    identity_type: str,
    session_policy_arn: str,
    *,
    identity_id: str | None = None,
    identity_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update studio session mapping.

    Args:
        studio_id: Studio id.
        identity_type: Identity type.
        session_policy_arn: Session policy arn.
        identity_id: Identity id.
        identity_name: Identity name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StudioId"] = studio_id
    kwargs["IdentityType"] = identity_type
    kwargs["SessionPolicyArn"] = session_policy_arn
    if identity_id is not None:
        kwargs["IdentityId"] = identity_id
    if identity_name is not None:
        kwargs["IdentityName"] = identity_name
    try:
        client.update_studio_session_mapping(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update studio session mapping") from exc
    return None
