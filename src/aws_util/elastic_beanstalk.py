"""aws_util.elastic_beanstalk — AWS Elastic Beanstalk utilities.

Provides helpers for managing Elastic Beanstalk applications, environments,
application versions, and health monitoring.  Each function wraps a single
boto3 ``elasticbeanstalk`` API call with structured Pydantic result models
and consistent error handling.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "ApplicationResult",
    "ApplicationVersionResult",
    "ApplyEnvironmentManagedActionResult",
    "CheckDnsAvailabilityResult",
    "ComposeEnvironmentsResult",
    "CreateConfigurationTemplateResult",
    "CreatePlatformVersionResult",
    "CreateStorageLocationResult",
    "DeletePlatformVersionResult",
    "DescribeAccountAttributesResult",
    "DescribeConfigurationOptionsResult",
    "DescribeConfigurationSettingsResult",
    "DescribeEnvironmentHealthResult",
    "DescribeEnvironmentManagedActionHistoryResult",
    "DescribeEnvironmentManagedActionsResult",
    "DescribeEnvironmentResourcesResult",
    "DescribePlatformVersionResult",
    "EnvironmentResult",
    "EventResult",
    "InstanceHealthResult",
    "ListAvailableSolutionStacksResult",
    "ListPlatformBranchesResult",
    "ListPlatformVersionsResult",
    "ListTagsForResourceResult",
    "RetrieveEnvironmentInfoResult",
    "UpdateApplicationResourceLifecycleResult",
    "UpdateApplicationResult",
    "UpdateApplicationVersionResult",
    "UpdateConfigurationTemplateResult",
    "ValidateConfigurationSettingsResult",
    "abort_environment_update",
    "apply_environment_managed_action",
    "associate_environment_operations_role",
    "check_dns_availability",
    "compose_environments",
    "create_application",
    "create_application_version",
    "create_configuration_template",
    "create_environment",
    "create_platform_version",
    "create_storage_location",
    "delete_application",
    "delete_application_version",
    "delete_configuration_template",
    "delete_environment_configuration",
    "delete_platform_version",
    "describe_account_attributes",
    "describe_application_versions",
    "describe_applications",
    "describe_configuration_options",
    "describe_configuration_settings",
    "describe_environment_health",
    "describe_environment_managed_action_history",
    "describe_environment_managed_actions",
    "describe_environment_resources",
    "describe_environments",
    "describe_events",
    "describe_instances_health",
    "describe_platform_version",
    "disassociate_environment_operations_role",
    "list_available_solution_stacks",
    "list_platform_branches",
    "list_platform_versions",
    "list_tags_for_resource",
    "rebuild_environment",
    "request_environment_info",
    "restart_app_server",
    "retrieve_environment_info",
    "swap_environment_cnames",
    "terminate_environment",
    "update_application",
    "update_application_resource_lifecycle",
    "update_application_version",
    "update_configuration_template",
    "update_environment",
    "update_tags_for_resource",
    "validate_configuration_settings",
    "wait_for_environment",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ApplicationResult(BaseModel):
    """Metadata for an Elastic Beanstalk application."""

    model_config = ConfigDict(frozen=True)

    application_name: str
    description: str = ""
    date_created: str | None = None
    date_updated: str | None = None
    versions: list[str] = []
    extra: dict[str, Any] = {}


class EnvironmentResult(BaseModel):
    """Metadata for an Elastic Beanstalk environment."""

    model_config = ConfigDict(frozen=True)

    environment_id: str
    environment_name: str
    application_name: str
    status: str
    health: str = ""
    solution_stack_name: str = ""
    cname: str = ""
    endpoint_url: str = ""
    version_label: str = ""
    extra: dict[str, Any] = {}


class ApplicationVersionResult(BaseModel):
    """Metadata for an Elastic Beanstalk application version."""

    model_config = ConfigDict(frozen=True)

    application_name: str
    version_label: str
    description: str = ""
    status: str = ""
    source_bundle: dict[str, Any] = {}
    date_created: str | None = None
    extra: dict[str, Any] = {}


class EventResult(BaseModel):
    """Metadata for an Elastic Beanstalk event."""

    model_config = ConfigDict(frozen=True)

    event_date: str | None = None
    message: str = ""
    application_name: str = ""
    environment_name: str = ""
    severity: str = ""
    extra: dict[str, Any] = {}


class InstanceHealthResult(BaseModel):
    """Health data for an instance in an Elastic Beanstalk environment."""

    model_config = ConfigDict(frozen=True)

    instance_id: str
    health_status: str = ""
    color: str = ""
    causes: list[str] = []
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_application(app: dict[str, Any]) -> ApplicationResult:
    """Parse a raw application dict into a model."""
    return ApplicationResult(
        application_name=app["ApplicationName"],
        description=app.get("Description", ""),
        date_created=str(app["DateCreated"]) if app.get("DateCreated") else None,
        date_updated=str(app["DateUpdated"]) if app.get("DateUpdated") else None,
        versions=app.get("Versions", []),
        extra={
            k: v
            for k, v in app.items()
            if k
            not in {
                "ApplicationName",
                "Description",
                "DateCreated",
                "DateUpdated",
                "Versions",
            }
        },
    )


def _parse_environment(env: dict[str, Any]) -> EnvironmentResult:
    """Parse a raw environment dict into a model."""
    return EnvironmentResult(
        environment_id=env.get("EnvironmentId", ""),
        environment_name=env.get("EnvironmentName", ""),
        application_name=env.get("ApplicationName", ""),
        status=env.get("Status", ""),
        health=env.get("Health", ""),
        solution_stack_name=env.get("SolutionStackName", ""),
        cname=env.get("CNAME", ""),
        endpoint_url=env.get("EndpointURL", ""),
        version_label=env.get("VersionLabel", ""),
        extra={
            k: v
            for k, v in env.items()
            if k
            not in {
                "EnvironmentId",
                "EnvironmentName",
                "ApplicationName",
                "Status",
                "Health",
                "SolutionStackName",
                "CNAME",
                "EndpointURL",
                "VersionLabel",
            }
        },
    )


def _parse_application_version(av: dict[str, Any]) -> ApplicationVersionResult:
    """Parse a raw application-version dict into a model."""
    return ApplicationVersionResult(
        application_name=av.get("ApplicationName", ""),
        version_label=av.get("VersionLabel", ""),
        description=av.get("Description", ""),
        status=av.get("Status", ""),
        source_bundle=av.get("SourceBundle", {}),
        date_created=str(av["DateCreated"]) if av.get("DateCreated") else None,
        extra={
            k: v
            for k, v in av.items()
            if k
            not in {
                "ApplicationName",
                "VersionLabel",
                "Description",
                "Status",
                "SourceBundle",
                "DateCreated",
            }
        },
    )


def _parse_event(ev: dict[str, Any]) -> EventResult:
    """Parse a raw event dict into a model."""
    return EventResult(
        event_date=str(ev["EventDate"]) if ev.get("EventDate") else None,
        message=ev.get("Message", ""),
        application_name=ev.get("ApplicationName", ""),
        environment_name=ev.get("EnvironmentName", ""),
        severity=ev.get("Severity", ""),
        extra={
            k: v
            for k, v in ev.items()
            if k
            not in {
                "EventDate",
                "Message",
                "ApplicationName",
                "EnvironmentName",
                "Severity",
            }
        },
    )


def _parse_instance_health(ih: dict[str, Any]) -> InstanceHealthResult:
    """Parse a raw instance-health dict into a model."""
    return InstanceHealthResult(
        instance_id=ih.get("InstanceId", ""),
        health_status=ih.get("HealthStatus", ""),
        color=ih.get("Color", ""),
        causes=ih.get("Causes", []),
        extra={
            k: v
            for k, v in ih.items()
            if k not in {"InstanceId", "HealthStatus", "Color", "Causes"}
        },
    )


# ---------------------------------------------------------------------------
# Application operations
# ---------------------------------------------------------------------------


def create_application(
    application_name: str,
    *,
    description: str = "",
    region_name: str | None = None,
) -> ApplicationResult:
    """Create an Elastic Beanstalk application.

    Args:
        application_name: Application name.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {"ApplicationName": application_name}
    if description:
        kwargs["Description"] = description
    try:
        resp = client.create_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_application failed for {application_name!r}") from exc
    return _parse_application(resp["Application"])


def describe_applications(
    *,
    application_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[ApplicationResult]:
    """Describe one or more Elastic Beanstalk applications.

    Args:
        application_names: Application names to describe. ``None`` lists all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ApplicationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if application_names is not None:
        kwargs["ApplicationNames"] = application_names
    try:
        resp = client.describe_applications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_applications failed") from exc
    return [_parse_application(a) for a in resp.get("Applications", [])]


def delete_application(
    application_name: str,
    *,
    terminate_env_by_force: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete an Elastic Beanstalk application.

    Args:
        application_name: Application name.
        terminate_env_by_force: Force-terminate running environments.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    try:
        client.delete_application(
            ApplicationName=application_name,
            TerminateEnvByForce=terminate_env_by_force,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_application failed for {application_name!r}") from exc


# ---------------------------------------------------------------------------
# Environment operations
# ---------------------------------------------------------------------------


def create_environment(
    application_name: str,
    environment_name: str,
    *,
    solution_stack_name: str | None = None,
    version_label: str | None = None,
    option_settings: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> EnvironmentResult:
    """Create an Elastic Beanstalk environment.

    Args:
        application_name: Application to associate.
        environment_name: Environment name.
        solution_stack_name: Platform (e.g. ``"64bit Amazon Linux 2 v5.8.0 running Python 3.8"``).
        version_label: Application version to deploy.
        option_settings: List of option setting dicts.
        region_name: AWS region override.

    Returns:
        An :class:`EnvironmentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {
        "ApplicationName": application_name,
        "EnvironmentName": environment_name,
    }
    if solution_stack_name is not None:
        kwargs["SolutionStackName"] = solution_stack_name
    if version_label is not None:
        kwargs["VersionLabel"] = version_label
    if option_settings is not None:
        kwargs["OptionSettings"] = option_settings
    try:
        resp = client.create_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_environment failed for {environment_name!r}") from exc
    return _parse_environment(resp)


def describe_environments(
    *,
    application_name: str | None = None,
    environment_names: list[str] | None = None,
    environment_ids: list[str] | None = None,
    region_name: str | None = None,
) -> list[EnvironmentResult]:
    """Describe Elastic Beanstalk environments.

    Args:
        application_name: Filter by application.
        environment_names: Filter by environment names.
        environment_ids: Filter by environment IDs.
        region_name: AWS region override.

    Returns:
        A list of :class:`EnvironmentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["ApplicationName"] = application_name
    if environment_names is not None:
        kwargs["EnvironmentNames"] = environment_names
    if environment_ids is not None:
        kwargs["EnvironmentIds"] = environment_ids
    try:
        resp = client.describe_environments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_environments failed") from exc
    return [_parse_environment(e) for e in resp.get("Environments", [])]


def update_environment(
    environment_name: str,
    *,
    version_label: str | None = None,
    option_settings: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> EnvironmentResult:
    """Update an Elastic Beanstalk environment.

    Args:
        environment_name: Environment name.
        version_label: New application version to deploy.
        option_settings: Updated option settings.
        region_name: AWS region override.

    Returns:
        An :class:`EnvironmentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {"EnvironmentName": environment_name}
    if version_label is not None:
        kwargs["VersionLabel"] = version_label
    if option_settings is not None:
        kwargs["OptionSettings"] = option_settings
    try:
        resp = client.update_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_environment failed for {environment_name!r}") from exc
    return _parse_environment(resp)


def terminate_environment(
    environment_name: str,
    *,
    force_terminate: bool = False,
    region_name: str | None = None,
) -> EnvironmentResult:
    """Terminate an Elastic Beanstalk environment.

    Args:
        environment_name: Environment name.
        force_terminate: Force-terminate even if in use.
        region_name: AWS region override.

    Returns:
        An :class:`EnvironmentResult` with terminal status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    try:
        resp = client.terminate_environment(
            EnvironmentName=environment_name,
            ForceTerminate=force_terminate,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"terminate_environment failed for {environment_name!r}") from exc
    return _parse_environment(resp)


# ---------------------------------------------------------------------------
# Application version operations
# ---------------------------------------------------------------------------


def create_application_version(
    application_name: str,
    version_label: str,
    *,
    description: str = "",
    source_bundle: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ApplicationVersionResult:
    """Create an application version.

    Args:
        application_name: Application name.
        version_label: Version label.
        description: Optional description.
        source_bundle: ``{"S3Bucket": ..., "S3Key": ...}`` dict.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationVersionResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {
        "ApplicationName": application_name,
        "VersionLabel": version_label,
    }
    if description:
        kwargs["Description"] = description
    if source_bundle is not None:
        kwargs["SourceBundle"] = source_bundle
    try:
        resp = client.create_application_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"create_application_version failed for {version_label!r}"
        ) from exc
    return _parse_application_version(resp["ApplicationVersion"])


def describe_application_versions(
    application_name: str,
    *,
    version_labels: list[str] | None = None,
    region_name: str | None = None,
) -> list[ApplicationVersionResult]:
    """Describe application versions.

    Args:
        application_name: Application name.
        version_labels: Specific version labels.  ``None`` lists all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ApplicationVersionResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {"ApplicationName": application_name}
    if version_labels is not None:
        kwargs["VersionLabels"] = version_labels
    try:
        resp = client.describe_application_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_application_versions failed") from exc
    return [_parse_application_version(av) for av in resp.get("ApplicationVersions", [])]


def delete_application_version(
    application_name: str,
    version_label: str,
    *,
    delete_source_bundle: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete an application version.

    Args:
        application_name: Application name.
        version_label: Version label to delete.
        delete_source_bundle: Also delete the S3 source bundle.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    try:
        client.delete_application_version(
            ApplicationName=application_name,
            VersionLabel=version_label,
            DeleteSourceBundle=delete_source_bundle,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"delete_application_version failed for {version_label!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Events and health
# ---------------------------------------------------------------------------


def describe_events(
    *,
    application_name: str | None = None,
    environment_name: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> list[EventResult]:
    """Describe Elastic Beanstalk events.

    Args:
        application_name: Filter by application.
        environment_name: Filter by environment.
        max_records: Maximum events to return.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["ApplicationName"] = application_name
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_events failed") from exc
    return [_parse_event(e) for e in resp.get("Events", [])]


def describe_instances_health(
    environment_name: str,
    *,
    attribute_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[InstanceHealthResult]:
    """Describe health of instances in an environment.

    Args:
        environment_name: Environment name.
        attribute_names: Health attribute names to return.
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceHealthResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {"EnvironmentName": environment_name}
    if attribute_names is not None:
        kwargs["AttributeNames"] = attribute_names
    try:
        resp = client.describe_instances_health(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_instances_health failed") from exc
    return [_parse_instance_health(ih) for ih in resp.get("InstanceHealthList", [])]


# ---------------------------------------------------------------------------
# Polling / composite operations
# ---------------------------------------------------------------------------


def wait_for_environment(
    environment_name: str,
    *,
    target_status: str = "Ready",
    timeout: float = 600,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> EnvironmentResult:
    """Poll until an environment reaches the target status.

    Args:
        environment_name: Environment name.
        target_status: Status to wait for (default ``"Ready"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`EnvironmentResult` in the target status.

    Raises:
        AwsTimeoutError: If the environment does not reach the target status.
        AwsServiceError: If the environment reaches ``"Terminated"`` unexpectedly.
    """
    deadline = time.monotonic() + timeout
    while True:
        envs = describe_environments(
            environment_names=[environment_name],
            region_name=region_name,
        )
        if not envs:
            raise AwsServiceError(f"Environment {environment_name!r} not found")
        env = envs[0]
        if env.status == target_status:
            return env
        if env.status == "Terminated" and target_status != "Terminated":
            raise AwsServiceError(f"Environment {environment_name!r} was terminated")
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Environment {environment_name!r} did not reach "
                f"{target_status!r} within {timeout}s "
                f"(current: {env.status!r})"
            )
        time.sleep(poll_interval)


class ApplyEnvironmentManagedActionResult(BaseModel):
    """Result of apply_environment_managed_action."""

    model_config = ConfigDict(frozen=True)

    action_id: str | None = None
    action_description: str | None = None
    action_type: str | None = None
    status: str | None = None


class CheckDnsAvailabilityResult(BaseModel):
    """Result of check_dns_availability."""

    model_config = ConfigDict(frozen=True)

    available: bool | None = None
    fully_qualified_cname: str | None = None


class ComposeEnvironmentsResult(BaseModel):
    """Result of compose_environments."""

    model_config = ConfigDict(frozen=True)

    environments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class CreateConfigurationTemplateResult(BaseModel):
    """Result of create_configuration_template."""

    model_config = ConfigDict(frozen=True)

    solution_stack_name: str | None = None
    platform_arn: str | None = None
    application_name: str | None = None
    template_name: str | None = None
    description: str | None = None
    environment_name: str | None = None
    deployment_status: str | None = None
    date_created: str | None = None
    date_updated: str | None = None
    option_settings: list[dict[str, Any]] | None = None


class CreatePlatformVersionResult(BaseModel):
    """Result of create_platform_version."""

    model_config = ConfigDict(frozen=True)

    platform_summary: dict[str, Any] | None = None
    builder: dict[str, Any] | None = None


class CreateStorageLocationResult(BaseModel):
    """Result of create_storage_location."""

    model_config = ConfigDict(frozen=True)

    s3_bucket: str | None = None


class DeletePlatformVersionResult(BaseModel):
    """Result of delete_platform_version."""

    model_config = ConfigDict(frozen=True)

    platform_summary: dict[str, Any] | None = None


class DescribeAccountAttributesResult(BaseModel):
    """Result of describe_account_attributes."""

    model_config = ConfigDict(frozen=True)

    resource_quotas: dict[str, Any] | None = None


class DescribeConfigurationOptionsResult(BaseModel):
    """Result of describe_configuration_options."""

    model_config = ConfigDict(frozen=True)

    solution_stack_name: str | None = None
    platform_arn: str | None = None
    options: list[dict[str, Any]] | None = None


class DescribeConfigurationSettingsResult(BaseModel):
    """Result of describe_configuration_settings."""

    model_config = ConfigDict(frozen=True)

    configuration_settings: list[dict[str, Any]] | None = None


class DescribeEnvironmentHealthResult(BaseModel):
    """Result of describe_environment_health."""

    model_config = ConfigDict(frozen=True)

    environment_name: str | None = None
    health_status: str | None = None
    status: str | None = None
    color: str | None = None
    causes: list[str] | None = None
    application_metrics: dict[str, Any] | None = None
    instances_health: dict[str, Any] | None = None
    refreshed_at: str | None = None


class DescribeEnvironmentManagedActionHistoryResult(BaseModel):
    """Result of describe_environment_managed_action_history."""

    model_config = ConfigDict(frozen=True)

    managed_action_history_items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeEnvironmentManagedActionsResult(BaseModel):
    """Result of describe_environment_managed_actions."""

    model_config = ConfigDict(frozen=True)

    managed_actions: list[dict[str, Any]] | None = None


class DescribeEnvironmentResourcesResult(BaseModel):
    """Result of describe_environment_resources."""

    model_config = ConfigDict(frozen=True)

    environment_resources: dict[str, Any] | None = None


class DescribePlatformVersionResult(BaseModel):
    """Result of describe_platform_version."""

    model_config = ConfigDict(frozen=True)

    platform_description: dict[str, Any] | None = None


class ListAvailableSolutionStacksResult(BaseModel):
    """Result of list_available_solution_stacks."""

    model_config = ConfigDict(frozen=True)

    solution_stacks: list[str] | None = None
    solution_stack_details: list[dict[str, Any]] | None = None


class ListPlatformBranchesResult(BaseModel):
    """Result of list_platform_branches."""

    model_config = ConfigDict(frozen=True)

    platform_branch_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPlatformVersionsResult(BaseModel):
    """Result of list_platform_versions."""

    model_config = ConfigDict(frozen=True)

    platform_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    resource_tags: list[dict[str, Any]] | None = None


class RetrieveEnvironmentInfoResult(BaseModel):
    """Result of retrieve_environment_info."""

    model_config = ConfigDict(frozen=True)

    environment_info: list[dict[str, Any]] | None = None


class UpdateApplicationResult(BaseModel):
    """Result of update_application."""

    model_config = ConfigDict(frozen=True)

    application: dict[str, Any] | None = None


class UpdateApplicationResourceLifecycleResult(BaseModel):
    """Result of update_application_resource_lifecycle."""

    model_config = ConfigDict(frozen=True)

    application_name: str | None = None
    resource_lifecycle_config: dict[str, Any] | None = None


class UpdateApplicationVersionResult(BaseModel):
    """Result of update_application_version."""

    model_config = ConfigDict(frozen=True)

    application_version: dict[str, Any] | None = None


class UpdateConfigurationTemplateResult(BaseModel):
    """Result of update_configuration_template."""

    model_config = ConfigDict(frozen=True)

    solution_stack_name: str | None = None
    platform_arn: str | None = None
    application_name: str | None = None
    template_name: str | None = None
    description: str | None = None
    environment_name: str | None = None
    deployment_status: str | None = None
    date_created: str | None = None
    date_updated: str | None = None
    option_settings: list[dict[str, Any]] | None = None


class ValidateConfigurationSettingsResult(BaseModel):
    """Result of validate_configuration_settings."""

    model_config = ConfigDict(frozen=True)

    messages: list[dict[str, Any]] | None = None


def abort_environment_update(
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Abort environment update.

    Args:
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        client.abort_environment_update(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to abort environment update") from exc
    return None


def apply_environment_managed_action(
    action_id: str,
    *,
    environment_name: str | None = None,
    environment_id: str | None = None,
    region_name: str | None = None,
) -> ApplyEnvironmentManagedActionResult:
    """Apply environment managed action.

    Args:
        action_id: Action id.
        environment_name: Environment name.
        environment_id: Environment id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionId"] = action_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    try:
        resp = client.apply_environment_managed_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to apply environment managed action") from exc
    return ApplyEnvironmentManagedActionResult(
        action_id=resp.get("ActionId"),
        action_description=resp.get("ActionDescription"),
        action_type=resp.get("ActionType"),
        status=resp.get("Status"),
    )


def associate_environment_operations_role(
    environment_name: str,
    operations_role: str,
    region_name: str | None = None,
) -> None:
    """Associate environment operations role.

    Args:
        environment_name: Environment name.
        operations_role: Operations role.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EnvironmentName"] = environment_name
    kwargs["OperationsRole"] = operations_role
    try:
        client.associate_environment_operations_role(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate environment operations role") from exc
    return None


def check_dns_availability(
    cname_prefix: str,
    region_name: str | None = None,
) -> CheckDnsAvailabilityResult:
    """Check dns availability.

    Args:
        cname_prefix: Cname prefix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CNAMEPrefix"] = cname_prefix
    try:
        resp = client.check_dns_availability(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to check dns availability") from exc
    return CheckDnsAvailabilityResult(
        available=resp.get("Available"),
        fully_qualified_cname=resp.get("FullyQualifiedCNAME"),
    )


def compose_environments(
    *,
    application_name: str | None = None,
    group_name: str | None = None,
    version_labels: list[str] | None = None,
    region_name: str | None = None,
) -> ComposeEnvironmentsResult:
    """Compose environments.

    Args:
        application_name: Application name.
        group_name: Group name.
        version_labels: Version labels.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["ApplicationName"] = application_name
    if group_name is not None:
        kwargs["GroupName"] = group_name
    if version_labels is not None:
        kwargs["VersionLabels"] = version_labels
    try:
        resp = client.compose_environments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to compose environments") from exc
    return ComposeEnvironmentsResult(
        environments=resp.get("Environments"),
        next_token=resp.get("NextToken"),
    )


def create_configuration_template(
    application_name: str,
    template_name: str,
    *,
    solution_stack_name: str | None = None,
    platform_arn: str | None = None,
    source_configuration: dict[str, Any] | None = None,
    environment_id: str | None = None,
    description: str | None = None,
    option_settings: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateConfigurationTemplateResult:
    """Create configuration template.

    Args:
        application_name: Application name.
        template_name: Template name.
        solution_stack_name: Solution stack name.
        platform_arn: Platform arn.
        source_configuration: Source configuration.
        environment_id: Environment id.
        description: Description.
        option_settings: Option settings.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["TemplateName"] = template_name
    if solution_stack_name is not None:
        kwargs["SolutionStackName"] = solution_stack_name
    if platform_arn is not None:
        kwargs["PlatformArn"] = platform_arn
    if source_configuration is not None:
        kwargs["SourceConfiguration"] = source_configuration
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if description is not None:
        kwargs["Description"] = description
    if option_settings is not None:
        kwargs["OptionSettings"] = option_settings
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_configuration_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create configuration template") from exc
    return CreateConfigurationTemplateResult(
        solution_stack_name=resp.get("SolutionStackName"),
        platform_arn=resp.get("PlatformArn"),
        application_name=resp.get("ApplicationName"),
        template_name=resp.get("TemplateName"),
        description=resp.get("Description"),
        environment_name=resp.get("EnvironmentName"),
        deployment_status=resp.get("DeploymentStatus"),
        date_created=resp.get("DateCreated"),
        date_updated=resp.get("DateUpdated"),
        option_settings=resp.get("OptionSettings"),
    )


def create_platform_version(
    platform_name: str,
    platform_version: str,
    platform_definition_bundle: dict[str, Any],
    *,
    environment_name: str | None = None,
    option_settings: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreatePlatformVersionResult:
    """Create platform version.

    Args:
        platform_name: Platform name.
        platform_version: Platform version.
        platform_definition_bundle: Platform definition bundle.
        environment_name: Environment name.
        option_settings: Option settings.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PlatformName"] = platform_name
    kwargs["PlatformVersion"] = platform_version
    kwargs["PlatformDefinitionBundle"] = platform_definition_bundle
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if option_settings is not None:
        kwargs["OptionSettings"] = option_settings
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_platform_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create platform version") from exc
    return CreatePlatformVersionResult(
        platform_summary=resp.get("PlatformSummary"),
        builder=resp.get("Builder"),
    )


def create_storage_location(
    region_name: str | None = None,
) -> CreateStorageLocationResult:
    """Create storage location.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.create_storage_location(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create storage location") from exc
    return CreateStorageLocationResult(
        s3_bucket=resp.get("S3Bucket"),
    )


def delete_configuration_template(
    application_name: str,
    template_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration template.

    Args:
        application_name: Application name.
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["TemplateName"] = template_name
    try:
        client.delete_configuration_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration template") from exc
    return None


def delete_environment_configuration(
    application_name: str,
    environment_name: str,
    region_name: str | None = None,
) -> None:
    """Delete environment configuration.

    Args:
        application_name: Application name.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["EnvironmentName"] = environment_name
    try:
        client.delete_environment_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete environment configuration") from exc
    return None


def delete_platform_version(
    *,
    platform_arn: str | None = None,
    region_name: str | None = None,
) -> DeletePlatformVersionResult:
    """Delete platform version.

    Args:
        platform_arn: Platform arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if platform_arn is not None:
        kwargs["PlatformArn"] = platform_arn
    try:
        resp = client.delete_platform_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete platform version") from exc
    return DeletePlatformVersionResult(
        platform_summary=resp.get("PlatformSummary"),
    )


def describe_account_attributes(
    region_name: str | None = None,
) -> DescribeAccountAttributesResult:
    """Describe account attributes.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_account_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account attributes") from exc
    return DescribeAccountAttributesResult(
        resource_quotas=resp.get("ResourceQuotas"),
    )


def describe_configuration_options(
    *,
    application_name: str | None = None,
    template_name: str | None = None,
    environment_name: str | None = None,
    solution_stack_name: str | None = None,
    platform_arn: str | None = None,
    options: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeConfigurationOptionsResult:
    """Describe configuration options.

    Args:
        application_name: Application name.
        template_name: Template name.
        environment_name: Environment name.
        solution_stack_name: Solution stack name.
        platform_arn: Platform arn.
        options: Options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if application_name is not None:
        kwargs["ApplicationName"] = application_name
    if template_name is not None:
        kwargs["TemplateName"] = template_name
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if solution_stack_name is not None:
        kwargs["SolutionStackName"] = solution_stack_name
    if platform_arn is not None:
        kwargs["PlatformArn"] = platform_arn
    if options is not None:
        kwargs["Options"] = options
    try:
        resp = client.describe_configuration_options(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration options") from exc
    return DescribeConfigurationOptionsResult(
        solution_stack_name=resp.get("SolutionStackName"),
        platform_arn=resp.get("PlatformArn"),
        options=resp.get("Options"),
    )


def describe_configuration_settings(
    application_name: str,
    *,
    template_name: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> DescribeConfigurationSettingsResult:
    """Describe configuration settings.

    Args:
        application_name: Application name.
        template_name: Template name.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    if template_name is not None:
        kwargs["TemplateName"] = template_name
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        resp = client.describe_configuration_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration settings") from exc
    return DescribeConfigurationSettingsResult(
        configuration_settings=resp.get("ConfigurationSettings"),
    )


def describe_environment_health(
    *,
    environment_name: str | None = None,
    environment_id: str | None = None,
    attribute_names: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeEnvironmentHealthResult:
    """Describe environment health.

    Args:
        environment_name: Environment name.
        environment_id: Environment id.
        attribute_names: Attribute names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if attribute_names is not None:
        kwargs["AttributeNames"] = attribute_names
    try:
        resp = client.describe_environment_health(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe environment health") from exc
    return DescribeEnvironmentHealthResult(
        environment_name=resp.get("EnvironmentName"),
        health_status=resp.get("HealthStatus"),
        status=resp.get("Status"),
        color=resp.get("Color"),
        causes=resp.get("Causes"),
        application_metrics=resp.get("ApplicationMetrics"),
        instances_health=resp.get("InstancesHealth"),
        refreshed_at=resp.get("RefreshedAt"),
    )


def describe_environment_managed_action_history(
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    next_token: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> DescribeEnvironmentManagedActionHistoryResult:
    """Describe environment managed action history.

    Args:
        environment_id: Environment id.
        environment_name: Environment name.
        next_token: Next token.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = client.describe_environment_managed_action_history(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe environment managed action history") from exc
    return DescribeEnvironmentManagedActionHistoryResult(
        managed_action_history_items=resp.get("ManagedActionHistoryItems"),
        next_token=resp.get("NextToken"),
    )


def describe_environment_managed_actions(
    *,
    environment_name: str | None = None,
    environment_id: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> DescribeEnvironmentManagedActionsResult:
    """Describe environment managed actions.

    Args:
        environment_name: Environment name.
        environment_id: Environment id.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = client.describe_environment_managed_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe environment managed actions") from exc
    return DescribeEnvironmentManagedActionsResult(
        managed_actions=resp.get("ManagedActions"),
    )


def describe_environment_resources(
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> DescribeEnvironmentResourcesResult:
    """Describe environment resources.

    Args:
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        resp = client.describe_environment_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe environment resources") from exc
    return DescribeEnvironmentResourcesResult(
        environment_resources=resp.get("EnvironmentResources"),
    )


def describe_platform_version(
    *,
    platform_arn: str | None = None,
    region_name: str | None = None,
) -> DescribePlatformVersionResult:
    """Describe platform version.

    Args:
        platform_arn: Platform arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if platform_arn is not None:
        kwargs["PlatformArn"] = platform_arn
    try:
        resp = client.describe_platform_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe platform version") from exc
    return DescribePlatformVersionResult(
        platform_description=resp.get("PlatformDescription"),
    )


def disassociate_environment_operations_role(
    environment_name: str,
    region_name: str | None = None,
) -> None:
    """Disassociate environment operations role.

    Args:
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EnvironmentName"] = environment_name
    try:
        client.disassociate_environment_operations_role(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate environment operations role") from exc
    return None


def list_available_solution_stacks(
    region_name: str | None = None,
) -> ListAvailableSolutionStacksResult:
    """List available solution stacks.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.list_available_solution_stacks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list available solution stacks") from exc
    return ListAvailableSolutionStacksResult(
        solution_stacks=resp.get("SolutionStacks"),
        solution_stack_details=resp.get("SolutionStackDetails"),
    )


def list_platform_branches(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPlatformBranchesResult:
    """List platform branches.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_platform_branches(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list platform branches") from exc
    return ListPlatformBranchesResult(
        platform_branch_summary_list=resp.get("PlatformBranchSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_platform_versions(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPlatformVersionsResult:
    """List platform versions.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_platform_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list platform versions") from exc
    return ListPlatformVersionsResult(
        platform_summary_list=resp.get("PlatformSummaryList"),
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
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_arn=resp.get("ResourceArn"),
        resource_tags=resp.get("ResourceTags"),
    )


def rebuild_environment(
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Rebuild environment.

    Args:
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        client.rebuild_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rebuild environment") from exc
    return None


def request_environment_info(
    info_type: str,
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Request environment info.

    Args:
        info_type: Info type.
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InfoType"] = info_type
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        client.request_environment_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to request environment info") from exc
    return None


def restart_app_server(
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Restart app server.

    Args:
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        client.restart_app_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restart app server") from exc
    return None


def retrieve_environment_info(
    info_type: str,
    *,
    environment_id: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> RetrieveEnvironmentInfoResult:
    """Retrieve environment info.

    Args:
        info_type: Info type.
        environment_id: Environment id.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InfoType"] = info_type
    if environment_id is not None:
        kwargs["EnvironmentId"] = environment_id
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        resp = client.retrieve_environment_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to retrieve environment info") from exc
    return RetrieveEnvironmentInfoResult(
        environment_info=resp.get("EnvironmentInfo"),
    )


def swap_environment_cnames(
    *,
    source_environment_id: str | None = None,
    source_environment_name: str | None = None,
    destination_environment_id: str | None = None,
    destination_environment_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Swap environment cnames.

    Args:
        source_environment_id: Source environment id.
        source_environment_name: Source environment name.
        destination_environment_id: Destination environment id.
        destination_environment_name: Destination environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    if source_environment_id is not None:
        kwargs["SourceEnvironmentId"] = source_environment_id
    if source_environment_name is not None:
        kwargs["SourceEnvironmentName"] = source_environment_name
    if destination_environment_id is not None:
        kwargs["DestinationEnvironmentId"] = destination_environment_id
    if destination_environment_name is not None:
        kwargs["DestinationEnvironmentName"] = destination_environment_name
    try:
        client.swap_environment_cnames(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to swap environment cnames") from exc
    return None


def update_application(
    application_name: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateApplicationResult:
    """Update application.

    Args:
        application_name: Application name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application") from exc
    return UpdateApplicationResult(
        application=resp.get("Application"),
    )


def update_application_resource_lifecycle(
    application_name: str,
    resource_lifecycle_config: dict[str, Any],
    region_name: str | None = None,
) -> UpdateApplicationResourceLifecycleResult:
    """Update application resource lifecycle.

    Args:
        application_name: Application name.
        resource_lifecycle_config: Resource lifecycle config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["ResourceLifecycleConfig"] = resource_lifecycle_config
    try:
        resp = client.update_application_resource_lifecycle(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application resource lifecycle") from exc
    return UpdateApplicationResourceLifecycleResult(
        application_name=resp.get("ApplicationName"),
        resource_lifecycle_config=resp.get("ResourceLifecycleConfig"),
    )


def update_application_version(
    application_name: str,
    version_label: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateApplicationVersionResult:
    """Update application version.

    Args:
        application_name: Application name.
        version_label: Version label.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["VersionLabel"] = version_label
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_application_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application version") from exc
    return UpdateApplicationVersionResult(
        application_version=resp.get("ApplicationVersion"),
    )


def update_configuration_template(
    application_name: str,
    template_name: str,
    *,
    description: str | None = None,
    option_settings: list[dict[str, Any]] | None = None,
    options_to_remove: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateConfigurationTemplateResult:
    """Update configuration template.

    Args:
        application_name: Application name.
        template_name: Template name.
        description: Description.
        option_settings: Option settings.
        options_to_remove: Options to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["TemplateName"] = template_name
    if description is not None:
        kwargs["Description"] = description
    if option_settings is not None:
        kwargs["OptionSettings"] = option_settings
    if options_to_remove is not None:
        kwargs["OptionsToRemove"] = options_to_remove
    try:
        resp = client.update_configuration_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update configuration template") from exc
    return UpdateConfigurationTemplateResult(
        solution_stack_name=resp.get("SolutionStackName"),
        platform_arn=resp.get("PlatformArn"),
        application_name=resp.get("ApplicationName"),
        template_name=resp.get("TemplateName"),
        description=resp.get("Description"),
        environment_name=resp.get("EnvironmentName"),
        deployment_status=resp.get("DeploymentStatus"),
        date_created=resp.get("DateCreated"),
        date_updated=resp.get("DateUpdated"),
        option_settings=resp.get("OptionSettings"),
    )


def update_tags_for_resource(
    resource_arn: str,
    *,
    tags_to_add: list[dict[str, Any]] | None = None,
    tags_to_remove: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Update tags for resource.

    Args:
        resource_arn: Resource arn.
        tags_to_add: Tags to add.
        tags_to_remove: Tags to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if tags_to_add is not None:
        kwargs["TagsToAdd"] = tags_to_add
    if tags_to_remove is not None:
        kwargs["TagsToRemove"] = tags_to_remove
    try:
        client.update_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update tags for resource") from exc
    return None


def validate_configuration_settings(
    application_name: str,
    option_settings: list[dict[str, Any]],
    *,
    template_name: str | None = None,
    environment_name: str | None = None,
    region_name: str | None = None,
) -> ValidateConfigurationSettingsResult:
    """Validate configuration settings.

    Args:
        application_name: Application name.
        option_settings: Option settings.
        template_name: Template name.
        environment_name: Environment name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticbeanstalk", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationName"] = application_name
    kwargs["OptionSettings"] = option_settings
    if template_name is not None:
        kwargs["TemplateName"] = template_name
    if environment_name is not None:
        kwargs["EnvironmentName"] = environment_name
    try:
        resp = client.validate_configuration_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to validate configuration settings") from exc
    return ValidateConfigurationSettingsResult(
        messages=resp.get("Messages"),
    )
