"""aws_util.codebuild -- AWS CodeBuild utilities.

Provides helpers for managing CodeBuild projects and builds, including
project CRUD, build start/stop/retry, and composite wait operations.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "BatchDeleteBuildsResult",
    "BatchGetBuildBatchesResult",
    "BatchGetCommandExecutionsResult",
    "BatchGetFleetsResult",
    "BatchGetReportGroupsResult",
    "BatchGetReportsResult",
    "BatchGetSandboxesResult",
    "BuildResult",
    "CreateFleetResult",
    "CreateReportGroupResult",
    "CreateWebhookResult",
    "DeleteBuildBatchResult",
    "DeleteSourceCredentialsResult",
    "DescribeCodeCoveragesResult",
    "DescribeTestCasesResult",
    "GetReportGroupTrendResult",
    "GetResourcePolicyResult",
    "ImportSourceCredentialsResult",
    "ListBuildBatchesForProjectResult",
    "ListBuildBatchesResult",
    "ListCommandExecutionsForSandboxResult",
    "ListCuratedEnvironmentImagesResult",
    "ListFleetsResult",
    "ListReportGroupsResult",
    "ListReportsForReportGroupResult",
    "ListReportsResult",
    "ListSandboxesForProjectResult",
    "ListSandboxesResult",
    "ListSharedProjectsResult",
    "ListSharedReportGroupsResult",
    "ListSourceCredentialsResult",
    "ProjectResult",
    "PutResourcePolicyResult",
    "RetryBuildBatchResult",
    "StartBuildBatchResult",
    "StartCommandExecutionResult",
    "StartSandboxConnectionResult",
    "StartSandboxResult",
    "StopBuildBatchResult",
    "StopSandboxResult",
    "UpdateFleetResult",
    "UpdateProjectVisibilityResult",
    "UpdateReportGroupResult",
    "UpdateWebhookResult",
    "batch_delete_builds",
    "batch_get_build_batches",
    "batch_get_builds",
    "batch_get_command_executions",
    "batch_get_fleets",
    "batch_get_projects",
    "batch_get_report_groups",
    "batch_get_reports",
    "batch_get_sandboxes",
    "create_fleet",
    "create_project",
    "create_report_group",
    "create_webhook",
    "delete_build_batch",
    "delete_fleet",
    "delete_project",
    "delete_report",
    "delete_report_group",
    "delete_resource_policy",
    "delete_source_credentials",
    "delete_webhook",
    "describe_code_coverages",
    "describe_test_cases",
    "get_report_group_trend",
    "get_resource_policy",
    "import_source_credentials",
    "invalidate_project_cache",
    "list_build_batches",
    "list_build_batches_for_project",
    "list_builds",
    "list_builds_for_project",
    "list_command_executions_for_sandbox",
    "list_curated_environment_images",
    "list_fleets",
    "list_projects",
    "list_report_groups",
    "list_reports",
    "list_reports_for_report_group",
    "list_sandboxes",
    "list_sandboxes_for_project",
    "list_shared_projects",
    "list_shared_report_groups",
    "list_source_credentials",
    "put_resource_policy",
    "retry_build",
    "retry_build_batch",
    "start_build",
    "start_build_and_wait",
    "start_build_batch",
    "start_command_execution",
    "start_sandbox",
    "start_sandbox_connection",
    "stop_build",
    "stop_build_batch",
    "stop_sandbox",
    "update_fleet",
    "update_project",
    "update_project_visibility",
    "update_report_group",
    "update_webhook",
    "wait_for_build",
]

_TERMINAL_BUILD_STATUSES = {"SUCCEEDED", "FAILED", "FAULT", "TIMED_OUT", "STOPPED"}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ProjectResult(BaseModel):
    """A CodeBuild project."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    description: str | None = None
    source: dict[str, Any]
    artifacts: dict[str, Any] | None = None
    environment: dict[str, Any]
    service_role: str | None = None
    created: str | None = None
    last_modified: str | None = None
    extra: dict[str, Any] = {}


class BuildResult(BaseModel):
    """A CodeBuild build."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    project_name: str
    build_status: str
    current_phase: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    source_version: str | None = None
    logs: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_project(data: dict[str, Any]) -> ProjectResult:
    """Convert a raw CodeBuild project dict into a ``ProjectResult``."""
    return ProjectResult(
        name=data["name"],
        arn=data["arn"],
        description=data.get("description"),
        source=data.get("source", {}),
        artifacts=data.get("artifacts"),
        environment=data.get("environment", {}),
        service_role=data.get("serviceRole"),
        created=str(data["created"]) if data.get("created") else None,
        last_modified=(str(data["lastModified"]) if data.get("lastModified") else None),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "name",
                "arn",
                "description",
                "source",
                "artifacts",
                "environment",
                "serviceRole",
                "created",
                "lastModified",
            }
        },
    )


def _parse_build(data: dict[str, Any]) -> BuildResult:
    """Convert a raw CodeBuild build dict into a ``BuildResult``."""
    return BuildResult(
        id=data["id"],
        arn=data["arn"],
        project_name=data.get("projectName", ""),
        build_status=data.get("buildStatus", "UNKNOWN"),
        current_phase=data.get("currentPhase"),
        start_time=str(data["startTime"]) if data.get("startTime") else None,
        end_time=str(data["endTime"]) if data.get("endTime") else None,
        source_version=data.get("sourceVersion"),
        logs=data.get("logs"),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "id",
                "arn",
                "projectName",
                "buildStatus",
                "currentPhase",
                "startTime",
                "endTime",
                "sourceVersion",
                "logs",
            }
        },
    )


# ---------------------------------------------------------------------------
# Project operations
# ---------------------------------------------------------------------------


def create_project(
    name: str,
    *,
    source: dict[str, Any],
    artifacts: dict[str, Any],
    environment: dict[str, Any],
    service_role: str,
    description: str | None = None,
    region_name: str | None = None,
) -> ProjectResult:
    """Create a new CodeBuild project.

    Args:
        name: Unique project name.
        source: Source configuration dict (type, location, etc.).
        artifacts: Artifacts configuration dict (type, location, etc.).
        environment: Environment configuration dict (type, computeType, image).
        service_role: IAM service role ARN for CodeBuild.
        description: Optional project description.
        region_name: AWS region override.

    Returns:
        A :class:`ProjectResult` for the created project.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "source": source,
        "artifacts": artifacts,
        "environment": environment,
        "serviceRole": service_role,
    }
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.create_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_project failed for {name!r}") from exc
    return _parse_project(resp["project"])


def batch_get_projects(
    names: list[str],
    *,
    region_name: str | None = None,
) -> list[ProjectResult]:
    """Retrieve details for one or more CodeBuild projects.

    Args:
        names: List of project names to retrieve.
        region_name: AWS region override.

    Returns:
        A list of :class:`ProjectResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    try:
        resp = client.batch_get_projects(names=names)
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_get_projects failed") from exc
    return [_parse_project(p) for p in resp.get("projects", [])]


def list_projects(
    *,
    sort_by: str = "NAME",
    sort_order: str = "ASCENDING",
    region_name: str | None = None,
) -> list[str]:
    """List CodeBuild project names.

    Args:
        sort_by: Sort field (``"NAME"`` or ``"CREATED_TIME"`` or
            ``"LAST_MODIFIED_TIME"``).
        sort_order: ``"ASCENDING"`` or ``"DESCENDING"``.
        region_name: AWS region override.

    Returns:
        A list of project name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    projects: list[str] = []
    try:
        paginator = client.get_paginator("list_projects")
        for page in paginator.paginate(sortBy=sort_by, sortOrder=sort_order):
            projects.extend(page.get("projects", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_projects failed") from exc
    return projects


def update_project(
    name: str,
    *,
    source: dict[str, Any] | None = None,
    artifacts: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> ProjectResult:
    """Update an existing CodeBuild project.

    Only the provided fields are updated; omitted fields remain unchanged.

    Args:
        name: Project name.
        source: Optional new source configuration.
        artifacts: Optional new artifacts configuration.
        environment: Optional new environment configuration.
        description: Optional new description.
        region_name: AWS region override.

    Returns:
        A :class:`ProjectResult` for the updated project.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {"name": name}
    if source is not None:
        kwargs["source"] = source
    if artifacts is not None:
        kwargs["artifacts"] = artifacts
    if environment is not None:
        kwargs["environment"] = environment
    if description is not None:
        kwargs["description"] = description
    try:
        resp = client.update_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_project failed for {name!r}") from exc
    return _parse_project(resp["project"])


def delete_project(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CodeBuild project.

    Args:
        name: Project name to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    try:
        client.delete_project(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_project failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Build operations
# ---------------------------------------------------------------------------


def start_build(
    project_name: str,
    *,
    source_version: str | None = None,
    environment_variables_override: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> BuildResult:
    """Start a new build for a CodeBuild project.

    Args:
        project_name: Name of the project to build.
        source_version: Optional source version (branch, tag, commit ID).
        environment_variables_override: Optional list of env-var dicts
            with ``name``, ``value``, and optional ``type`` keys.
        region_name: AWS region override.

    Returns:
        A :class:`BuildResult` for the started build.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {"projectName": project_name}
    if source_version is not None:
        kwargs["sourceVersion"] = source_version
    if environment_variables_override is not None:
        kwargs["environmentVariablesOverride"] = environment_variables_override
    try:
        resp = client.start_build(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_build failed for {project_name!r}") from exc
    return _parse_build(resp["build"])


def batch_get_builds(
    build_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[BuildResult]:
    """Retrieve details for one or more builds.

    Args:
        build_ids: List of build IDs (e.g. ``["project:build-id"]``).
        region_name: AWS region override.

    Returns:
        A list of :class:`BuildResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    try:
        resp = client.batch_get_builds(ids=build_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_get_builds failed") from exc
    return [_parse_build(b) for b in resp.get("builds", [])]


def list_builds(
    *,
    sort_order: str = "DESCENDING",
    region_name: str | None = None,
) -> list[str]:
    """List build IDs across all projects.

    Args:
        sort_order: ``"ASCENDING"`` or ``"DESCENDING"``.
        region_name: AWS region override.

    Returns:
        A list of build ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    build_ids: list[str] = []
    try:
        paginator = client.get_paginator("list_builds")
        for page in paginator.paginate(sortOrder=sort_order):
            build_ids.extend(page.get("ids", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_builds failed") from exc
    return build_ids


def list_builds_for_project(
    project_name: str,
    *,
    sort_order: str = "DESCENDING",
    region_name: str | None = None,
) -> list[str]:
    """List build IDs for a specific project.

    Args:
        project_name: Name of the project.
        sort_order: ``"ASCENDING"`` or ``"DESCENDING"``.
        region_name: AWS region override.

    Returns:
        A list of build ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    build_ids: list[str] = []
    try:
        paginator = client.get_paginator("list_builds_for_project")
        for page in paginator.paginate(projectName=project_name, sortOrder=sort_order):
            build_ids.extend(page.get("ids", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_builds_for_project failed for {project_name!r}") from exc
    return build_ids


def stop_build(
    build_id: str,
    *,
    region_name: str | None = None,
) -> BuildResult:
    """Stop a running build.

    Args:
        build_id: ID of the build to stop.
        region_name: AWS region override.

    Returns:
        A :class:`BuildResult` for the stopped build.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    try:
        resp = client.stop_build(id=build_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_build failed for {build_id!r}") from exc
    return _parse_build(resp["build"])


def retry_build(
    build_id: str,
    *,
    region_name: str | None = None,
) -> BuildResult:
    """Retry a previously completed build.

    Args:
        build_id: ID of the build to retry.
        region_name: AWS region override.

    Returns:
        A :class:`BuildResult` for the retried build.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    try:
        resp = client.retry_build(id=build_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"retry_build failed for {build_id!r}") from exc
    return _parse_build(resp["build"])


# ---------------------------------------------------------------------------
# Composite / wait operations
# ---------------------------------------------------------------------------


def wait_for_build(
    build_id: str,
    *,
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> BuildResult:
    """Poll until a build reaches a terminal status.

    Args:
        build_id: ID of the build to wait for.
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between status checks (default ``15``).
        region_name: AWS region override.

    Returns:
        The final :class:`BuildResult`.

    Raises:
        AwsTimeoutError: If the build does not finish within *timeout*.
        RuntimeError: If the build finishes with ``FAILED`` status.
    """
    deadline = time.monotonic() + timeout
    while True:
        builds = batch_get_builds([build_id], region_name=region_name)
        if not builds:
            raise RuntimeError(f"Build {build_id!r} not found")
        build = builds[0]
        if build.build_status in _TERMINAL_BUILD_STATUSES:
            if build.build_status == "FAILED":
                raise RuntimeError(f"Build {build_id!r} failed")
            return build
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(f"Build {build_id!r} did not finish within {timeout}s")
        time.sleep(poll_interval)


def start_build_and_wait(
    project_name: str,
    *,
    source_version: str | None = None,
    environment_variables_override: list[dict[str, str]] | None = None,
    timeout: float = 1800,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> BuildResult:
    """Start a build and wait until it reaches a terminal status.

    Combines :func:`start_build` and :func:`wait_for_build`.

    Args:
        project_name: Name of the project to build.
        source_version: Optional source version (branch, tag, commit ID).
        environment_variables_override: Optional environment variable overrides.
        timeout: Maximum seconds to wait (default ``1800``).
        poll_interval: Seconds between status checks (default ``15``).
        region_name: AWS region override.

    Returns:
        The final :class:`BuildResult`.

    Raises:
        AwsTimeoutError: If the build does not finish within *timeout*.
        RuntimeError: If the build finishes with ``FAILED`` status or
            the start request fails.
    """
    build = start_build(
        project_name,
        source_version=source_version,
        environment_variables_override=environment_variables_override,
        region_name=region_name,
    )
    return wait_for_build(
        build.id,
        timeout=timeout,
        poll_interval=poll_interval,
        region_name=region_name,
    )


class BatchDeleteBuildsResult(BaseModel):
    """Result of batch_delete_builds."""

    model_config = ConfigDict(frozen=True)

    builds_deleted: list[str] | None = None
    builds_not_deleted: list[dict[str, Any]] | None = None


class BatchGetBuildBatchesResult(BaseModel):
    """Result of batch_get_build_batches."""

    model_config = ConfigDict(frozen=True)

    build_batches: list[dict[str, Any]] | None = None
    build_batches_not_found: list[str] | None = None


class BatchGetCommandExecutionsResult(BaseModel):
    """Result of batch_get_command_executions."""

    model_config = ConfigDict(frozen=True)

    command_executions: list[dict[str, Any]] | None = None
    command_executions_not_found: list[str] | None = None


class BatchGetFleetsResult(BaseModel):
    """Result of batch_get_fleets."""

    model_config = ConfigDict(frozen=True)

    fleets: list[dict[str, Any]] | None = None
    fleets_not_found: list[str] | None = None


class BatchGetReportGroupsResult(BaseModel):
    """Result of batch_get_report_groups."""

    model_config = ConfigDict(frozen=True)

    report_groups: list[dict[str, Any]] | None = None
    report_groups_not_found: list[str] | None = None


class BatchGetReportsResult(BaseModel):
    """Result of batch_get_reports."""

    model_config = ConfigDict(frozen=True)

    reports: list[dict[str, Any]] | None = None
    reports_not_found: list[str] | None = None


class BatchGetSandboxesResult(BaseModel):
    """Result of batch_get_sandboxes."""

    model_config = ConfigDict(frozen=True)

    sandboxes: list[dict[str, Any]] | None = None
    sandboxes_not_found: list[str] | None = None


class CreateFleetResult(BaseModel):
    """Result of create_fleet."""

    model_config = ConfigDict(frozen=True)

    fleet: dict[str, Any] | None = None


class CreateReportGroupResult(BaseModel):
    """Result of create_report_group."""

    model_config = ConfigDict(frozen=True)

    report_group: dict[str, Any] | None = None


class CreateWebhookResult(BaseModel):
    """Result of create_webhook."""

    model_config = ConfigDict(frozen=True)

    webhook: dict[str, Any] | None = None


class DeleteBuildBatchResult(BaseModel):
    """Result of delete_build_batch."""

    model_config = ConfigDict(frozen=True)

    status_code: str | None = None
    builds_deleted: list[str] | None = None
    builds_not_deleted: list[dict[str, Any]] | None = None


class DeleteSourceCredentialsResult(BaseModel):
    """Result of delete_source_credentials."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None


class DescribeCodeCoveragesResult(BaseModel):
    """Result of describe_code_coverages."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    code_coverages: list[dict[str, Any]] | None = None


class DescribeTestCasesResult(BaseModel):
    """Result of describe_test_cases."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    run_cases: list[dict[str, Any]] | None = None


class GetReportGroupTrendResult(BaseModel):
    """Result of get_report_group_trend."""

    model_config = ConfigDict(frozen=True)

    stats: dict[str, Any] | None = None
    raw_data: list[dict[str, Any]] | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None


class ImportSourceCredentialsResult(BaseModel):
    """Result of import_source_credentials."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None


class ListBuildBatchesResult(BaseModel):
    """Result of list_build_batches."""

    model_config = ConfigDict(frozen=True)

    ids: list[str] | None = None
    next_token: str | None = None


class ListBuildBatchesForProjectResult(BaseModel):
    """Result of list_build_batches_for_project."""

    model_config = ConfigDict(frozen=True)

    ids: list[str] | None = None
    next_token: str | None = None


class ListCommandExecutionsForSandboxResult(BaseModel):
    """Result of list_command_executions_for_sandbox."""

    model_config = ConfigDict(frozen=True)

    command_executions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListCuratedEnvironmentImagesResult(BaseModel):
    """Result of list_curated_environment_images."""

    model_config = ConfigDict(frozen=True)

    platforms: list[dict[str, Any]] | None = None


class ListFleetsResult(BaseModel):
    """Result of list_fleets."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    fleets: list[str] | None = None


class ListReportGroupsResult(BaseModel):
    """Result of list_report_groups."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    report_groups: list[str] | None = None


class ListReportsResult(BaseModel):
    """Result of list_reports."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reports: list[str] | None = None


class ListReportsForReportGroupResult(BaseModel):
    """Result of list_reports_for_report_group."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reports: list[str] | None = None


class ListSandboxesResult(BaseModel):
    """Result of list_sandboxes."""

    model_config = ConfigDict(frozen=True)

    ids: list[str] | None = None
    next_token: str | None = None


class ListSandboxesForProjectResult(BaseModel):
    """Result of list_sandboxes_for_project."""

    model_config = ConfigDict(frozen=True)

    ids: list[str] | None = None
    next_token: str | None = None


class ListSharedProjectsResult(BaseModel):
    """Result of list_shared_projects."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    projects: list[str] | None = None


class ListSharedReportGroupsResult(BaseModel):
    """Result of list_shared_report_groups."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    report_groups: list[str] | None = None


class ListSourceCredentialsResult(BaseModel):
    """Result of list_source_credentials."""

    model_config = ConfigDict(frozen=True)

    source_credentials_infos: list[dict[str, Any]] | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None


class RetryBuildBatchResult(BaseModel):
    """Result of retry_build_batch."""

    model_config = ConfigDict(frozen=True)

    build_batch: dict[str, Any] | None = None


class StartBuildBatchResult(BaseModel):
    """Result of start_build_batch."""

    model_config = ConfigDict(frozen=True)

    build_batch: dict[str, Any] | None = None


class StartCommandExecutionResult(BaseModel):
    """Result of start_command_execution."""

    model_config = ConfigDict(frozen=True)

    command_execution: dict[str, Any] | None = None


class StartSandboxResult(BaseModel):
    """Result of start_sandbox."""

    model_config = ConfigDict(frozen=True)

    sandbox: dict[str, Any] | None = None


class StartSandboxConnectionResult(BaseModel):
    """Result of start_sandbox_connection."""

    model_config = ConfigDict(frozen=True)

    ssm_session: dict[str, Any] | None = None


class StopBuildBatchResult(BaseModel):
    """Result of stop_build_batch."""

    model_config = ConfigDict(frozen=True)

    build_batch: dict[str, Any] | None = None


class StopSandboxResult(BaseModel):
    """Result of stop_sandbox."""

    model_config = ConfigDict(frozen=True)

    sandbox: dict[str, Any] | None = None


class UpdateFleetResult(BaseModel):
    """Result of update_fleet."""

    model_config = ConfigDict(frozen=True)

    fleet: dict[str, Any] | None = None


class UpdateProjectVisibilityResult(BaseModel):
    """Result of update_project_visibility."""

    model_config = ConfigDict(frozen=True)

    project_arn: str | None = None
    public_project_alias: str | None = None
    project_visibility: str | None = None


class UpdateReportGroupResult(BaseModel):
    """Result of update_report_group."""

    model_config = ConfigDict(frozen=True)

    report_group: dict[str, Any] | None = None


class UpdateWebhookResult(BaseModel):
    """Result of update_webhook."""

    model_config = ConfigDict(frozen=True)

    webhook: dict[str, Any] | None = None


def batch_delete_builds(
    ids: list[str],
    region_name: str | None = None,
) -> BatchDeleteBuildsResult:
    """Batch delete builds.

    Args:
        ids: Ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ids"] = ids
    try:
        resp = client.batch_delete_builds(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete builds") from exc
    return BatchDeleteBuildsResult(
        builds_deleted=resp.get("buildsDeleted"),
        builds_not_deleted=resp.get("buildsNotDeleted"),
    )


def batch_get_build_batches(
    ids: list[str],
    region_name: str | None = None,
) -> BatchGetBuildBatchesResult:
    """Batch get build batches.

    Args:
        ids: Ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ids"] = ids
    try:
        resp = client.batch_get_build_batches(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get build batches") from exc
    return BatchGetBuildBatchesResult(
        build_batches=resp.get("buildBatches"),
        build_batches_not_found=resp.get("buildBatchesNotFound"),
    )


def batch_get_command_executions(
    sandbox_id: str,
    command_execution_ids: list[str],
    region_name: str | None = None,
) -> BatchGetCommandExecutionsResult:
    """Batch get command executions.

    Args:
        sandbox_id: Sandbox id.
        command_execution_ids: Command execution ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sandboxId"] = sandbox_id
    kwargs["commandExecutionIds"] = command_execution_ids
    try:
        resp = client.batch_get_command_executions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get command executions") from exc
    return BatchGetCommandExecutionsResult(
        command_executions=resp.get("commandExecutions"),
        command_executions_not_found=resp.get("commandExecutionsNotFound"),
    )


def batch_get_fleets(
    names: list[str],
    region_name: str | None = None,
) -> BatchGetFleetsResult:
    """Batch get fleets.

    Args:
        names: Names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["names"] = names
    try:
        resp = client.batch_get_fleets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get fleets") from exc
    return BatchGetFleetsResult(
        fleets=resp.get("fleets"),
        fleets_not_found=resp.get("fleetsNotFound"),
    )


def batch_get_report_groups(
    report_group_arns: list[str],
    region_name: str | None = None,
) -> BatchGetReportGroupsResult:
    """Batch get report groups.

    Args:
        report_group_arns: Report group arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportGroupArns"] = report_group_arns
    try:
        resp = client.batch_get_report_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get report groups") from exc
    return BatchGetReportGroupsResult(
        report_groups=resp.get("reportGroups"),
        report_groups_not_found=resp.get("reportGroupsNotFound"),
    )


def batch_get_reports(
    report_arns: list[str],
    region_name: str | None = None,
) -> BatchGetReportsResult:
    """Batch get reports.

    Args:
        report_arns: Report arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportArns"] = report_arns
    try:
        resp = client.batch_get_reports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get reports") from exc
    return BatchGetReportsResult(
        reports=resp.get("reports"),
        reports_not_found=resp.get("reportsNotFound"),
    )


def batch_get_sandboxes(
    ids: list[str],
    region_name: str | None = None,
) -> BatchGetSandboxesResult:
    """Batch get sandboxes.

    Args:
        ids: Ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ids"] = ids
    try:
        resp = client.batch_get_sandboxes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get sandboxes") from exc
    return BatchGetSandboxesResult(
        sandboxes=resp.get("sandboxes"),
        sandboxes_not_found=resp.get("sandboxesNotFound"),
    )


def create_fleet(
    name: str,
    base_capacity: int,
    environment_type: str,
    compute_type: str,
    *,
    compute_configuration: dict[str, Any] | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    overflow_behavior: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    proxy_configuration: dict[str, Any] | None = None,
    image_id: str | None = None,
    fleet_service_role: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateFleetResult:
    """Create fleet.

    Args:
        name: Name.
        base_capacity: Base capacity.
        environment_type: Environment type.
        compute_type: Compute type.
        compute_configuration: Compute configuration.
        scaling_configuration: Scaling configuration.
        overflow_behavior: Overflow behavior.
        vpc_config: Vpc config.
        proxy_configuration: Proxy configuration.
        image_id: Image id.
        fleet_service_role: Fleet service role.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["baseCapacity"] = base_capacity
    kwargs["environmentType"] = environment_type
    kwargs["computeType"] = compute_type
    if compute_configuration is not None:
        kwargs["computeConfiguration"] = compute_configuration
    if scaling_configuration is not None:
        kwargs["scalingConfiguration"] = scaling_configuration
    if overflow_behavior is not None:
        kwargs["overflowBehavior"] = overflow_behavior
    if vpc_config is not None:
        kwargs["vpcConfig"] = vpc_config
    if proxy_configuration is not None:
        kwargs["proxyConfiguration"] = proxy_configuration
    if image_id is not None:
        kwargs["imageId"] = image_id
    if fleet_service_role is not None:
        kwargs["fleetServiceRole"] = fleet_service_role
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_fleet(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create fleet") from exc
    return CreateFleetResult(
        fleet=resp.get("fleet"),
    )


def create_report_group(
    name: str,
    type_value: str,
    export_config: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateReportGroupResult:
    """Create report group.

    Args:
        name: Name.
        type_value: Type value.
        export_config: Export config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["type"] = type_value
    kwargs["exportConfig"] = export_config
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_report_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create report group") from exc
    return CreateReportGroupResult(
        report_group=resp.get("reportGroup"),
    )


def create_webhook(
    project_name: str,
    *,
    branch_filter: str | None = None,
    filter_groups: list[list[dict[str, Any]]] | None = None,
    build_type: str | None = None,
    manual_creation: bool | None = None,
    scope_configuration: dict[str, Any] | None = None,
    pull_request_build_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateWebhookResult:
    """Create webhook.

    Args:
        project_name: Project name.
        branch_filter: Branch filter.
        filter_groups: Filter groups.
        build_type: Build type.
        manual_creation: Manual creation.
        scope_configuration: Scope configuration.
        pull_request_build_policy: Pull request build policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    if branch_filter is not None:
        kwargs["branchFilter"] = branch_filter
    if filter_groups is not None:
        kwargs["filterGroups"] = filter_groups
    if build_type is not None:
        kwargs["buildType"] = build_type
    if manual_creation is not None:
        kwargs["manualCreation"] = manual_creation
    if scope_configuration is not None:
        kwargs["scopeConfiguration"] = scope_configuration
    if pull_request_build_policy is not None:
        kwargs["pullRequestBuildPolicy"] = pull_request_build_policy
    try:
        resp = client.create_webhook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create webhook") from exc
    return CreateWebhookResult(
        webhook=resp.get("webhook"),
    )


def delete_build_batch(
    id: str,
    region_name: str | None = None,
) -> DeleteBuildBatchResult:
    """Delete build batch.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.delete_build_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete build batch") from exc
    return DeleteBuildBatchResult(
        status_code=resp.get("statusCode"),
        builds_deleted=resp.get("buildsDeleted"),
        builds_not_deleted=resp.get("buildsNotDeleted"),
    )


def delete_fleet(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete fleet.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        client.delete_fleet(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete fleet") from exc
    return None


def delete_report(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete report.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        client.delete_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete report") from exc
    return None


def delete_report_group(
    arn: str,
    *,
    delete_reports: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete report group.

    Args:
        arn: Arn.
        delete_reports: Delete reports.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if delete_reports is not None:
        kwargs["deleteReports"] = delete_reports
    try:
        client.delete_report_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete report group") from exc
    return None


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
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def delete_source_credentials(
    arn: str,
    region_name: str | None = None,
) -> DeleteSourceCredentialsResult:
    """Delete source credentials.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = client.delete_source_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete source credentials") from exc
    return DeleteSourceCredentialsResult(
        arn=resp.get("arn"),
    )


def delete_webhook(
    project_name: str,
    region_name: str | None = None,
) -> None:
    """Delete webhook.

    Args:
        project_name: Project name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    try:
        client.delete_webhook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete webhook") from exc
    return None


def describe_code_coverages(
    report_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    sort_order: str | None = None,
    sort_by: str | None = None,
    min_line_coverage_percentage: float | None = None,
    max_line_coverage_percentage: float | None = None,
    region_name: str | None = None,
) -> DescribeCodeCoveragesResult:
    """Describe code coverages.

    Args:
        report_arn: Report arn.
        next_token: Next token.
        max_results: Max results.
        sort_order: Sort order.
        sort_by: Sort by.
        min_line_coverage_percentage: Min line coverage percentage.
        max_line_coverage_percentage: Max line coverage percentage.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportArn"] = report_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if min_line_coverage_percentage is not None:
        kwargs["minLineCoveragePercentage"] = min_line_coverage_percentage
    if max_line_coverage_percentage is not None:
        kwargs["maxLineCoveragePercentage"] = max_line_coverage_percentage
    try:
        resp = client.describe_code_coverages(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe code coverages") from exc
    return DescribeCodeCoveragesResult(
        next_token=resp.get("nextToken"),
        code_coverages=resp.get("codeCoverages"),
    )


def describe_test_cases(
    report_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> DescribeTestCasesResult:
    """Describe test cases.

    Args:
        report_arn: Report arn.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportArn"] = report_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_test_cases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe test cases") from exc
    return DescribeTestCasesResult(
        next_token=resp.get("nextToken"),
        run_cases=resp.get("testCases"),
    )


def get_report_group_trend(
    report_group_arn: str,
    trend_field: str,
    *,
    num_of_reports: int | None = None,
    region_name: str | None = None,
) -> GetReportGroupTrendResult:
    """Get report group trend.

    Args:
        report_group_arn: Report group arn.
        trend_field: Trend field.
        num_of_reports: Num of reports.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportGroupArn"] = report_group_arn
    kwargs["trendField"] = trend_field
    if num_of_reports is not None:
        kwargs["numOfReports"] = num_of_reports
    try:
        resp = client.get_report_group_trend(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get report group trend") from exc
    return GetReportGroupTrendResult(
        stats=resp.get("stats"),
        raw_data=resp.get("rawData"),
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
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy=resp.get("policy"),
    )


def import_source_credentials(
    token: str,
    server_type: str,
    auth_type: str,
    *,
    username: str | None = None,
    should_overwrite: bool | None = None,
    region_name: str | None = None,
) -> ImportSourceCredentialsResult:
    """Import source credentials.

    Args:
        token: Token.
        server_type: Server type.
        auth_type: Auth type.
        username: Username.
        should_overwrite: Should overwrite.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["token"] = token
    kwargs["serverType"] = server_type
    kwargs["authType"] = auth_type
    if username is not None:
        kwargs["username"] = username
    if should_overwrite is not None:
        kwargs["shouldOverwrite"] = should_overwrite
    try:
        resp = client.import_source_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import source credentials") from exc
    return ImportSourceCredentialsResult(
        arn=resp.get("arn"),
    )


def invalidate_project_cache(
    project_name: str,
    region_name: str | None = None,
) -> None:
    """Invalidate project cache.

    Args:
        project_name: Project name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    try:
        client.invalidate_project_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to invalidate project cache") from exc
    return None


def list_build_batches(
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBuildBatchesResult:
    """List build batches.

    Args:
        filter: Filter.
        max_results: Max results.
        sort_order: Sort order.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_build_batches(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list build batches") from exc
    return ListBuildBatchesResult(
        ids=resp.get("ids"),
        next_token=resp.get("nextToken"),
    )


def list_build_batches_for_project(
    *,
    project_name: str | None = None,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListBuildBatchesForProjectResult:
    """List build batches for project.

    Args:
        project_name: Project name.
        filter: Filter.
        max_results: Max results.
        sort_order: Sort order.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if project_name is not None:
        kwargs["projectName"] = project_name
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_build_batches_for_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list build batches for project") from exc
    return ListBuildBatchesForProjectResult(
        ids=resp.get("ids"),
        next_token=resp.get("nextToken"),
    )


def list_command_executions_for_sandbox(
    sandbox_id: str,
    *,
    max_results: int | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCommandExecutionsForSandboxResult:
    """List command executions for sandbox.

    Args:
        sandbox_id: Sandbox id.
        max_results: Max results.
        sort_order: Sort order.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sandboxId"] = sandbox_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_command_executions_for_sandbox(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list command executions for sandbox") from exc
    return ListCommandExecutionsForSandboxResult(
        command_executions=resp.get("commandExecutions"),
        next_token=resp.get("nextToken"),
    )


def list_curated_environment_images(
    region_name: str | None = None,
) -> ListCuratedEnvironmentImagesResult:
    """List curated environment images.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.list_curated_environment_images(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list curated environment images") from exc
    return ListCuratedEnvironmentImagesResult(
        platforms=resp.get("platforms"),
    )


def list_fleets(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    sort_order: str | None = None,
    sort_by: str | None = None,
    region_name: str | None = None,
) -> ListFleetsResult:
    """List fleets.

    Args:
        next_token: Next token.
        max_results: Max results.
        sort_order: Sort order.
        sort_by: Sort by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    try:
        resp = client.list_fleets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list fleets") from exc
    return ListFleetsResult(
        next_token=resp.get("nextToken"),
        fleets=resp.get("fleets"),
    )


def list_report_groups(
    *,
    sort_order: str | None = None,
    sort_by: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListReportGroupsResult:
    """List report groups.

    Args:
        sort_order: Sort order.
        sort_by: Sort by.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_report_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list report groups") from exc
    return ListReportGroupsResult(
        next_token=resp.get("nextToken"),
        report_groups=resp.get("reportGroups"),
    )


def list_reports(
    *,
    sort_order: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListReportsResult:
    """List reports.

    Args:
        sort_order: Sort order.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.list_reports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list reports") from exc
    return ListReportsResult(
        next_token=resp.get("nextToken"),
        reports=resp.get("reports"),
    )


def list_reports_for_report_group(
    report_group_arn: str,
    *,
    next_token: str | None = None,
    sort_order: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListReportsForReportGroupResult:
    """List reports for report group.

    Args:
        report_group_arn: Report group arn.
        next_token: Next token.
        sort_order: Sort order.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reportGroupArn"] = report_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.list_reports_for_report_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list reports for report group") from exc
    return ListReportsForReportGroupResult(
        next_token=resp.get("nextToken"),
        reports=resp.get("reports"),
    )


def list_sandboxes(
    *,
    max_results: int | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSandboxesResult:
    """List sandboxes.

    Args:
        max_results: Max results.
        sort_order: Sort order.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_sandboxes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list sandboxes") from exc
    return ListSandboxesResult(
        ids=resp.get("ids"),
        next_token=resp.get("nextToken"),
    )


def list_sandboxes_for_project(
    project_name: str,
    *,
    max_results: int | None = None,
    sort_order: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSandboxesForProjectResult:
    """List sandboxes for project.

    Args:
        project_name: Project name.
        max_results: Max results.
        sort_order: Sort order.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_sandboxes_for_project(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list sandboxes for project") from exc
    return ListSandboxesForProjectResult(
        ids=resp.get("ids"),
        next_token=resp.get("nextToken"),
    )


def list_shared_projects(
    *,
    sort_by: str | None = None,
    sort_order: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSharedProjectsResult:
    """List shared projects.

    Args:
        sort_by: Sort by.
        sort_order: Sort order.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_shared_projects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list shared projects") from exc
    return ListSharedProjectsResult(
        next_token=resp.get("nextToken"),
        projects=resp.get("projects"),
    )


def list_shared_report_groups(
    *,
    sort_order: str | None = None,
    sort_by: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSharedReportGroupsResult:
    """List shared report groups.

    Args:
        sort_order: Sort order.
        sort_by: Sort by.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if sort_by is not None:
        kwargs["sortBy"] = sort_by
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_shared_report_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list shared report groups") from exc
    return ListSharedReportGroupsResult(
        next_token=resp.get("nextToken"),
        report_groups=resp.get("reportGroups"),
    )


def list_source_credentials(
    region_name: str | None = None,
) -> ListSourceCredentialsResult:
    """List source credentials.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.list_source_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list source credentials") from exc
    return ListSourceCredentialsResult(
        source_credentials_infos=resp.get("sourceCredentialsInfos"),
    )


def put_resource_policy(
    policy: str,
    resource_arn: str,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        policy: Policy.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policy"] = policy
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_arn=resp.get("resourceArn"),
    )


def retry_build_batch(
    *,
    id: str | None = None,
    idempotency_token: str | None = None,
    retry_type: str | None = None,
    region_name: str | None = None,
) -> RetryBuildBatchResult:
    """Retry build batch.

    Args:
        id: Id.
        idempotency_token: Idempotency token.
        retry_type: Retry type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if id is not None:
        kwargs["id"] = id
    if idempotency_token is not None:
        kwargs["idempotencyToken"] = idempotency_token
    if retry_type is not None:
        kwargs["retryType"] = retry_type
    try:
        resp = client.retry_build_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to retry build batch") from exc
    return RetryBuildBatchResult(
        build_batch=resp.get("buildBatch"),
    )


def start_build_batch(
    project_name: str,
    *,
    secondary_sources_override: list[dict[str, Any]] | None = None,
    secondary_sources_version_override: list[dict[str, Any]] | None = None,
    source_version: str | None = None,
    artifacts_override: dict[str, Any] | None = None,
    secondary_artifacts_override: list[dict[str, Any]] | None = None,
    environment_variables_override: list[dict[str, Any]] | None = None,
    source_type_override: str | None = None,
    source_location_override: str | None = None,
    source_auth_override: dict[str, Any] | None = None,
    git_clone_depth_override: int | None = None,
    git_submodules_config_override: dict[str, Any] | None = None,
    buildspec_override: str | None = None,
    insecure_ssl_override: bool | None = None,
    report_build_batch_status_override: bool | None = None,
    environment_type_override: str | None = None,
    image_override: str | None = None,
    compute_type_override: str | None = None,
    certificate_override: str | None = None,
    cache_override: dict[str, Any] | None = None,
    service_role_override: str | None = None,
    privileged_mode_override: bool | None = None,
    build_timeout_in_minutes_override: int | None = None,
    queued_timeout_in_minutes_override: int | None = None,
    encryption_key_override: str | None = None,
    idempotency_token: str | None = None,
    logs_config_override: dict[str, Any] | None = None,
    registry_credential_override: dict[str, Any] | None = None,
    image_pull_credentials_type_override: str | None = None,
    build_batch_config_override: dict[str, Any] | None = None,
    debug_session_enabled: bool | None = None,
    region_name: str | None = None,
) -> StartBuildBatchResult:
    """Start build batch.

    Args:
        project_name: Project name.
        secondary_sources_override: Secondary sources override.
        secondary_sources_version_override: Secondary sources version override.
        source_version: Source version.
        artifacts_override: Artifacts override.
        secondary_artifacts_override: Secondary artifacts override.
        environment_variables_override: Environment variables override.
        source_type_override: Source type override.
        source_location_override: Source location override.
        source_auth_override: Source auth override.
        git_clone_depth_override: Git clone depth override.
        git_submodules_config_override: Git submodules config override.
        buildspec_override: Buildspec override.
        insecure_ssl_override: Insecure ssl override.
        report_build_batch_status_override: Report build batch status override.
        environment_type_override: Environment type override.
        image_override: Image override.
        compute_type_override: Compute type override.
        certificate_override: Certificate override.
        cache_override: Cache override.
        service_role_override: Service role override.
        privileged_mode_override: Privileged mode override.
        build_timeout_in_minutes_override: Build timeout in minutes override.
        queued_timeout_in_minutes_override: Queued timeout in minutes override.
        encryption_key_override: Encryption key override.
        idempotency_token: Idempotency token.
        logs_config_override: Logs config override.
        registry_credential_override: Registry credential override.
        image_pull_credentials_type_override: Image pull credentials type override.
        build_batch_config_override: Build batch config override.
        debug_session_enabled: Debug session enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    if secondary_sources_override is not None:
        kwargs["secondarySourcesOverride"] = secondary_sources_override
    if secondary_sources_version_override is not None:
        kwargs["secondarySourcesVersionOverride"] = secondary_sources_version_override
    if source_version is not None:
        kwargs["sourceVersion"] = source_version
    if artifacts_override is not None:
        kwargs["artifactsOverride"] = artifacts_override
    if secondary_artifacts_override is not None:
        kwargs["secondaryArtifactsOverride"] = secondary_artifacts_override
    if environment_variables_override is not None:
        kwargs["environmentVariablesOverride"] = environment_variables_override
    if source_type_override is not None:
        kwargs["sourceTypeOverride"] = source_type_override
    if source_location_override is not None:
        kwargs["sourceLocationOverride"] = source_location_override
    if source_auth_override is not None:
        kwargs["sourceAuthOverride"] = source_auth_override
    if git_clone_depth_override is not None:
        kwargs["gitCloneDepthOverride"] = git_clone_depth_override
    if git_submodules_config_override is not None:
        kwargs["gitSubmodulesConfigOverride"] = git_submodules_config_override
    if buildspec_override is not None:
        kwargs["buildspecOverride"] = buildspec_override
    if insecure_ssl_override is not None:
        kwargs["insecureSslOverride"] = insecure_ssl_override
    if report_build_batch_status_override is not None:
        kwargs["reportBuildBatchStatusOverride"] = report_build_batch_status_override
    if environment_type_override is not None:
        kwargs["environmentTypeOverride"] = environment_type_override
    if image_override is not None:
        kwargs["imageOverride"] = image_override
    if compute_type_override is not None:
        kwargs["computeTypeOverride"] = compute_type_override
    if certificate_override is not None:
        kwargs["certificateOverride"] = certificate_override
    if cache_override is not None:
        kwargs["cacheOverride"] = cache_override
    if service_role_override is not None:
        kwargs["serviceRoleOverride"] = service_role_override
    if privileged_mode_override is not None:
        kwargs["privilegedModeOverride"] = privileged_mode_override
    if build_timeout_in_minutes_override is not None:
        kwargs["buildTimeoutInMinutesOverride"] = build_timeout_in_minutes_override
    if queued_timeout_in_minutes_override is not None:
        kwargs["queuedTimeoutInMinutesOverride"] = queued_timeout_in_minutes_override
    if encryption_key_override is not None:
        kwargs["encryptionKeyOverride"] = encryption_key_override
    if idempotency_token is not None:
        kwargs["idempotencyToken"] = idempotency_token
    if logs_config_override is not None:
        kwargs["logsConfigOverride"] = logs_config_override
    if registry_credential_override is not None:
        kwargs["registryCredentialOverride"] = registry_credential_override
    if image_pull_credentials_type_override is not None:
        kwargs["imagePullCredentialsTypeOverride"] = image_pull_credentials_type_override
    if build_batch_config_override is not None:
        kwargs["buildBatchConfigOverride"] = build_batch_config_override
    if debug_session_enabled is not None:
        kwargs["debugSessionEnabled"] = debug_session_enabled
    try:
        resp = client.start_build_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start build batch") from exc
    return StartBuildBatchResult(
        build_batch=resp.get("buildBatch"),
    )


def start_command_execution(
    sandbox_id: str,
    command: str,
    *,
    type_value: str | None = None,
    region_name: str | None = None,
) -> StartCommandExecutionResult:
    """Start command execution.

    Args:
        sandbox_id: Sandbox id.
        command: Command.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sandboxId"] = sandbox_id
    kwargs["command"] = command
    if type_value is not None:
        kwargs["type"] = type_value
    try:
        resp = client.start_command_execution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start command execution") from exc
    return StartCommandExecutionResult(
        command_execution=resp.get("commandExecution"),
    )


def start_sandbox(
    *,
    project_name: str | None = None,
    idempotency_token: str | None = None,
    region_name: str | None = None,
) -> StartSandboxResult:
    """Start sandbox.

    Args:
        project_name: Project name.
        idempotency_token: Idempotency token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    if project_name is not None:
        kwargs["projectName"] = project_name
    if idempotency_token is not None:
        kwargs["idempotencyToken"] = idempotency_token
    try:
        resp = client.start_sandbox(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start sandbox") from exc
    return StartSandboxResult(
        sandbox=resp.get("sandbox"),
    )


def start_sandbox_connection(
    sandbox_id: str,
    region_name: str | None = None,
) -> StartSandboxConnectionResult:
    """Start sandbox connection.

    Args:
        sandbox_id: Sandbox id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sandboxId"] = sandbox_id
    try:
        resp = client.start_sandbox_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start sandbox connection") from exc
    return StartSandboxConnectionResult(
        ssm_session=resp.get("ssmSession"),
    )


def stop_build_batch(
    id: str,
    region_name: str | None = None,
) -> StopBuildBatchResult:
    """Stop build batch.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.stop_build_batch(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop build batch") from exc
    return StopBuildBatchResult(
        build_batch=resp.get("buildBatch"),
    )


def stop_sandbox(
    id: str,
    region_name: str | None = None,
) -> StopSandboxResult:
    """Stop sandbox.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.stop_sandbox(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop sandbox") from exc
    return StopSandboxResult(
        sandbox=resp.get("sandbox"),
    )


def update_fleet(
    arn: str,
    *,
    base_capacity: int | None = None,
    environment_type: str | None = None,
    compute_type: str | None = None,
    compute_configuration: dict[str, Any] | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    overflow_behavior: str | None = None,
    vpc_config: dict[str, Any] | None = None,
    proxy_configuration: dict[str, Any] | None = None,
    image_id: str | None = None,
    fleet_service_role: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateFleetResult:
    """Update fleet.

    Args:
        arn: Arn.
        base_capacity: Base capacity.
        environment_type: Environment type.
        compute_type: Compute type.
        compute_configuration: Compute configuration.
        scaling_configuration: Scaling configuration.
        overflow_behavior: Overflow behavior.
        vpc_config: Vpc config.
        proxy_configuration: Proxy configuration.
        image_id: Image id.
        fleet_service_role: Fleet service role.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if base_capacity is not None:
        kwargs["baseCapacity"] = base_capacity
    if environment_type is not None:
        kwargs["environmentType"] = environment_type
    if compute_type is not None:
        kwargs["computeType"] = compute_type
    if compute_configuration is not None:
        kwargs["computeConfiguration"] = compute_configuration
    if scaling_configuration is not None:
        kwargs["scalingConfiguration"] = scaling_configuration
    if overflow_behavior is not None:
        kwargs["overflowBehavior"] = overflow_behavior
    if vpc_config is not None:
        kwargs["vpcConfig"] = vpc_config
    if proxy_configuration is not None:
        kwargs["proxyConfiguration"] = proxy_configuration
    if image_id is not None:
        kwargs["imageId"] = image_id
    if fleet_service_role is not None:
        kwargs["fleetServiceRole"] = fleet_service_role
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.update_fleet(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update fleet") from exc
    return UpdateFleetResult(
        fleet=resp.get("fleet"),
    )


def update_project_visibility(
    project_arn: str,
    project_visibility: str,
    *,
    resource_access_role: str | None = None,
    region_name: str | None = None,
) -> UpdateProjectVisibilityResult:
    """Update project visibility.

    Args:
        project_arn: Project arn.
        project_visibility: Project visibility.
        resource_access_role: Resource access role.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectArn"] = project_arn
    kwargs["projectVisibility"] = project_visibility
    if resource_access_role is not None:
        kwargs["resourceAccessRole"] = resource_access_role
    try:
        resp = client.update_project_visibility(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update project visibility") from exc
    return UpdateProjectVisibilityResult(
        project_arn=resp.get("projectArn"),
        public_project_alias=resp.get("publicProjectAlias"),
        project_visibility=resp.get("projectVisibility"),
    )


def update_report_group(
    arn: str,
    *,
    export_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateReportGroupResult:
    """Update report group.

    Args:
        arn: Arn.
        export_config: Export config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if export_config is not None:
        kwargs["exportConfig"] = export_config
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.update_report_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update report group") from exc
    return UpdateReportGroupResult(
        report_group=resp.get("reportGroup"),
    )


def update_webhook(
    project_name: str,
    *,
    branch_filter: str | None = None,
    rotate_secret: bool | None = None,
    filter_groups: list[list[dict[str, Any]]] | None = None,
    build_type: str | None = None,
    pull_request_build_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateWebhookResult:
    """Update webhook.

    Args:
        project_name: Project name.
        branch_filter: Branch filter.
        rotate_secret: Rotate secret.
        filter_groups: Filter groups.
        build_type: Build type.
        pull_request_build_policy: Pull request build policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("codebuild", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectName"] = project_name
    if branch_filter is not None:
        kwargs["branchFilter"] = branch_filter
    if rotate_secret is not None:
        kwargs["rotateSecret"] = rotate_secret
    if filter_groups is not None:
        kwargs["filterGroups"] = filter_groups
    if build_type is not None:
        kwargs["buildType"] = build_type
    if pull_request_build_policy is not None:
        kwargs["pullRequestBuildPolicy"] = pull_request_build_policy
    try:
        resp = client.update_webhook(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update webhook") from exc
    return UpdateWebhookResult(
        webhook=resp.get("webhook"),
    )
