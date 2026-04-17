"""aws_util.emr_serverless — Amazon EMR Serverless utilities.

Provides convenience wrappers around EMR Serverless application and job run
management operations with Pydantic-modelled results.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ApplicationResult",
    "GetDashboardForJobRunResult",
    "JobRunResult",
    "ListJobRunAttemptsResult",
    "ListTagsForResourceResult",
    "cancel_job_run",
    "create_application",
    "delete_application",
    "get_application",
    "get_dashboard_for_job_run",
    "get_job_run",
    "list_applications",
    "list_job_run_attempts",
    "list_job_runs",
    "list_tags_for_resource",
    "start_application",
    "start_job_run",
    "stop_application",
    "tag_resource",
    "untag_resource",
    "update_application",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ApplicationResult(BaseModel):
    """Metadata for an EMR Serverless application."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_id: str
    name: str
    arn: str = ""
    state: str = ""
    release_label: str | None = None
    type: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class JobRunResult(BaseModel):
    """Metadata for an EMR Serverless job run."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    application_id: str
    job_run_id: str
    name: str = ""
    arn: str = ""
    state: str = ""
    state_details: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    execution_role: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_APP_FIELDS = {
    "applicationId",
    "name",
    "arn",
    "state",
    "releaseLabel",
    "type",
    "createdAt",
    "updatedAt",
    "tags",
}

_JOB_FIELDS = {
    "applicationId",
    "jobRunId",
    "name",
    "arn",
    "state",
    "stateDetails",
    "createdAt",
    "updatedAt",
    "executionRoleArn",
}


def _parse_application(data: dict[str, Any]) -> ApplicationResult:
    """Parse a raw EMR Serverless application dict."""
    created = data.get("createdAt")
    updated = data.get("updatedAt")
    return ApplicationResult(
        application_id=data.get("applicationId", ""),
        name=data.get("name", ""),
        arn=data.get("arn", ""),
        state=data.get("state", ""),
        release_label=data.get("releaseLabel"),
        type=data.get("type"),
        created_at=str(created) if created is not None else None,
        updated_at=str(updated) if updated is not None else None,
        tags=data.get("tags", {}),
        extra={k: v for k, v in data.items() if k not in _APP_FIELDS},
    )


def _parse_job_run(data: dict[str, Any]) -> JobRunResult:
    """Parse a raw EMR Serverless job run dict."""
    created = data.get("createdAt")
    updated = data.get("updatedAt")
    return JobRunResult(
        application_id=data.get("applicationId", ""),
        job_run_id=data.get("jobRunId", ""),
        name=data.get("name", ""),
        arn=data.get("arn", ""),
        state=data.get("state", ""),
        state_details=data.get("stateDetails"),
        created_at=str(created) if created is not None else None,
        updated_at=str(updated) if updated is not None else None,
        execution_role=data.get("executionRoleArn"),
        extra={k: v for k, v in data.items() if k not in _JOB_FIELDS},
    )


# ---------------------------------------------------------------------------
# Application operations
# ---------------------------------------------------------------------------


def create_application(
    name: str,
    *,
    release_label: str,
    application_type: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ApplicationResult:
    """Create an EMR Serverless application.

    Args:
        name: Name for the new application.
        release_label: EMR release label (e.g. ``"emr-6.9.0"``).
        application_type: Application type (``"SPARK"`` or ``"HIVE"``).
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult` for the new application.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "releaseLabel": release_label,
        "type": application_type,
    }
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_application failed for {name!r}") from exc
    return ApplicationResult(
        application_id=resp.get("applicationId", ""),
        name=resp.get("name", name),
        arn=resp.get("arn", ""),
    )


def get_application(
    application_id: str,
    *,
    region_name: str | None = None,
) -> ApplicationResult:
    """Get details of an EMR Serverless application.

    Args:
        application_id: ID of the application.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    try:
        resp = client.get_application(applicationId=application_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_application failed for {application_id!r}") from exc
    return _parse_application(resp.get("application", {}))


def list_applications(
    *,
    region_name: str | None = None,
) -> list[ApplicationResult]:
    """List all EMR Serverless applications.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ApplicationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    apps: list[ApplicationResult] = []
    try:
        paginator = client.get_paginator("list_applications")
        for page in paginator.paginate():
            for item in page.get("applications", []):
                apps.append(_parse_application(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_applications failed") from exc
    return apps


def delete_application(
    application_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Delete an EMR Serverless application.

    Args:
        application_id: ID of the application to delete.
        region_name: AWS region override.

    Returns:
        A dict with the application_id.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    try:
        client.delete_application(applicationId=application_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_application failed for {application_id!r}") from exc
    return {"application_id": application_id}


def update_application(
    application_id: str,
    *,
    initial_capacity: dict[str, Any] | None = None,
    maximum_capacity: dict[str, Any] | None = None,
    auto_start_configuration: dict[str, Any] | None = None,
    auto_stop_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ApplicationResult:
    """Update an EMR Serverless application.

    Args:
        application_id: ID of the application.
        initial_capacity: Optional initial capacity configuration.
        maximum_capacity: Optional maximum capacity configuration.
        auto_start_configuration: Optional auto-start configuration.
        auto_stop_configuration: Optional auto-stop configuration.
        region_name: AWS region override.

    Returns:
        An :class:`ApplicationResult` with updated details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {"applicationId": application_id}
    if initial_capacity is not None:
        kwargs["initialCapacity"] = initial_capacity
    if maximum_capacity is not None:
        kwargs["maximumCapacity"] = maximum_capacity
    if auto_start_configuration is not None:
        kwargs["autoStartConfiguration"] = auto_start_configuration
    if auto_stop_configuration is not None:
        kwargs["autoStopConfiguration"] = auto_stop_configuration
    try:
        resp = client.update_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_application failed for {application_id!r}") from exc
    return _parse_application(resp.get("application", {}))


# ---------------------------------------------------------------------------
# Job run operations
# ---------------------------------------------------------------------------


def start_job_run(
    application_id: str,
    *,
    execution_role_arn: str,
    job_driver: dict[str, Any],
    name: str | None = None,
    configuration_overrides: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> JobRunResult:
    """Start a job run on an EMR Serverless application.

    Args:
        application_id: ID of the application.
        execution_role_arn: IAM role ARN for execution.
        job_driver: Job driver configuration.
        name: Optional name for the job run.
        configuration_overrides: Optional configuration overrides.
        region_name: AWS region override.

    Returns:
        A :class:`JobRunResult` for the new job run.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {
        "applicationId": application_id,
        "executionRoleArn": execution_role_arn,
        "jobDriver": job_driver,
    }
    if name is not None:
        kwargs["name"] = name
    if configuration_overrides is not None:
        kwargs["configurationOverrides"] = configuration_overrides
    try:
        resp = client.start_job_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"start_job_run failed for application {application_id!r}"
        ) from exc
    return JobRunResult(
        application_id=resp.get("applicationId", application_id),
        job_run_id=resp.get("jobRunId", ""),
        arn=resp.get("arn", ""),
    )


def get_job_run(
    application_id: str,
    job_run_id: str,
    *,
    region_name: str | None = None,
) -> JobRunResult:
    """Get details of an EMR Serverless job run.

    Args:
        application_id: ID of the application.
        job_run_id: ID of the job run.
        region_name: AWS region override.

    Returns:
        A :class:`JobRunResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    try:
        resp = client.get_job_run(applicationId=application_id, jobRunId=job_run_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_job_run failed for {job_run_id!r}") from exc
    return _parse_job_run(resp.get("jobRun", {}))


def list_job_runs(
    application_id: str,
    *,
    region_name: str | None = None,
) -> list[JobRunResult]:
    """List job runs for an EMR Serverless application.

    Args:
        application_id: ID of the application.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobRunResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    runs: list[JobRunResult] = []
    try:
        paginator = client.get_paginator("list_job_runs")
        for page in paginator.paginate(applicationId=application_id):
            for item in page.get("jobRuns", []):
                runs.append(_parse_job_run(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_job_runs failed") from exc
    return runs


def cancel_job_run(
    application_id: str,
    job_run_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """Cancel an EMR Serverless job run.

    Args:
        application_id: ID of the application.
        job_run_id: ID of the job run to cancel.
        region_name: AWS region override.

    Returns:
        A dict with application_id and job_run_id.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    try:
        client.cancel_job_run(applicationId=application_id, jobRunId=job_run_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"cancel_job_run failed for {job_run_id!r}") from exc
    return {"application_id": application_id, "job_run_id": job_run_id}


class GetDashboardForJobRunResult(BaseModel):
    """Result of get_dashboard_for_job_run."""

    model_config = ConfigDict(frozen=True)

    url: str | None = None


class ListJobRunAttemptsResult(BaseModel):
    """Result of list_job_run_attempts."""

    model_config = ConfigDict(frozen=True)

    job_run_attempts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


def get_dashboard_for_job_run(
    application_id: str,
    job_run_id: str,
    *,
    attempt: int | None = None,
    access_system_profile_logs: bool | None = None,
    region_name: str | None = None,
) -> GetDashboardForJobRunResult:
    """Get dashboard for job run.

    Args:
        application_id: Application id.
        job_run_id: Job run id.
        attempt: Attempt.
        access_system_profile_logs: Access system profile logs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    kwargs["jobRunId"] = job_run_id
    if attempt is not None:
        kwargs["attempt"] = attempt
    if access_system_profile_logs is not None:
        kwargs["accessSystemProfileLogs"] = access_system_profile_logs
    try:
        resp = client.get_dashboard_for_job_run(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get dashboard for job run") from exc
    return GetDashboardForJobRunResult(
        url=resp.get("url"),
    )


def list_job_run_attempts(
    application_id: str,
    job_run_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListJobRunAttemptsResult:
    """List job run attempts.

    Args:
        application_id: Application id.
        job_run_id: Job run id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    kwargs["jobRunId"] = job_run_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_job_run_attempts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list job run attempts") from exc
    return ListJobRunAttemptsResult(
        job_run_attempts=resp.get("jobRunAttempts"),
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
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def start_application(
    application_id: str,
    region_name: str | None = None,
) -> None:
    """Start application.

    Args:
        application_id: Application id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    try:
        client.start_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start application") from exc
    return None


def stop_application(
    application_id: str,
    region_name: str | None = None,
) -> None:
    """Stop application.

    Args:
        application_id: Application id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    try:
        client.stop_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop application") from exc
    return None


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
    client = get_client("emr-serverless", region_name)
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
    client = get_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
