"""Native async EMR Serverless utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.emr_serverless import (
    ApplicationResult,
    GetDashboardForJobRunResult,
    JobRunResult,
    ListJobRunAttemptsResult,
    ListTagsForResourceResult,
    _parse_application,
    _parse_job_run,
)
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
# Application operations
# ---------------------------------------------------------------------------


async def create_application(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "releaseLabel": release_label,
        "type": application_type,
    }
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_application failed for {name!r}") from exc
    return ApplicationResult(
        application_id=resp.get("applicationId", ""),
        name=resp.get("name", name),
        arn=resp.get("arn", ""),
    )


async def get_application(
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
    client = async_client("emr-serverless", region_name)
    try:
        resp = await client.call("GetApplication", applicationId=application_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_application failed for {application_id!r}") from exc
    return _parse_application(resp.get("application", {}))


async def list_applications(
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
    client = async_client("emr-serverless", region_name)
    apps: list[ApplicationResult] = []
    try:
        kwargs: dict[str, Any] = {}
        while True:
            resp = await client.call("ListApplications", **kwargs)
            for item in resp.get("applications", []):
                apps.append(_parse_application(item))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_applications failed") from exc
    return apps


async def delete_application(
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
    client = async_client("emr-serverless", region_name)
    try:
        await client.call("DeleteApplication", applicationId=application_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_application failed for {application_id!r}") from exc
    return {"application_id": application_id}


async def update_application(
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
    client = async_client("emr-serverless", region_name)
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
        resp = await client.call("UpdateApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_application failed for {application_id!r}") from exc
    return _parse_application(resp.get("application", {}))


# ---------------------------------------------------------------------------
# Job run operations
# ---------------------------------------------------------------------------


async def start_job_run(
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
    client = async_client("emr-serverless", region_name)
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
        resp = await client.call("StartJobRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"start_job_run failed for application {application_id!r}",
        ) from exc
    return JobRunResult(
        application_id=resp.get("applicationId", application_id),
        job_run_id=resp.get("jobRunId", ""),
        arn=resp.get("arn", ""),
    )


async def get_job_run(
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
    client = async_client("emr-serverless", region_name)
    try:
        resp = await client.call(
            "GetJobRun",
            applicationId=application_id,
            jobRunId=job_run_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_job_run failed for {job_run_id!r}") from exc
    return _parse_job_run(resp.get("jobRun", {}))


async def list_job_runs(
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
    client = async_client("emr-serverless", region_name)
    runs: list[JobRunResult] = []
    try:
        kwargs: dict[str, Any] = {
            "applicationId": application_id,
        }
        while True:
            resp = await client.call("ListJobRuns", **kwargs)
            for item in resp.get("jobRuns", []):
                runs.append(_parse_job_run(item))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_job_runs failed") from exc
    return runs


async def cancel_job_run(
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
    client = async_client("emr-serverless", region_name)
    try:
        await client.call(
            "CancelJobRun",
            applicationId=application_id,
            jobRunId=job_run_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"cancel_job_run failed for {job_run_id!r}") from exc
    return {"application_id": application_id, "job_run_id": job_run_id}


async def get_dashboard_for_job_run(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    kwargs["jobRunId"] = job_run_id
    if attempt is not None:
        kwargs["attempt"] = attempt
    if access_system_profile_logs is not None:
        kwargs["accessSystemProfileLogs"] = access_system_profile_logs
    try:
        resp = await client.call("GetDashboardForJobRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dashboard for job run") from exc
    return GetDashboardForJobRunResult(
        url=resp.get("url"),
    )


async def list_job_run_attempts(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    kwargs["jobRunId"] = job_run_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListJobRunAttempts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list job run attempts") from exc
    return ListJobRunAttemptsResult(
        job_run_attempts=resp.get("jobRunAttempts"),
        next_token=resp.get("nextToken"),
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def start_application(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    try:
        await client.call("StartApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start application") from exc
    return None


async def stop_application(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["applicationId"] = application_id
    try:
        await client.call("StopApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop application") from exc
    return None


async def tag_resource(
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
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
    client = async_client("emr-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
