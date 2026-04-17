"""aws_util.batch — AWS Batch utilities.

Provides helpers for managing AWS Batch compute environments, job queues,
job definitions, and jobs.  Each function wraps a single boto3 Batch API
call with structured Pydantic result models and consistent error handling.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "ComputeEnvironmentResult",
    "CreateConsumableResourceResult",
    "CreateSchedulingPolicyResult",
    "CreateServiceEnvironmentResult",
    "DescribeConsumableResourceResult",
    "DescribeSchedulingPoliciesResult",
    "DescribeServiceEnvironmentsResult",
    "DescribeServiceJobResult",
    "GetJobQueueSnapshotResult",
    "JobDefinitionResult",
    "JobQueueResult",
    "JobResult",
    "ListConsumableResourcesResult",
    "ListJobsByConsumableResourceResult",
    "ListSchedulingPoliciesResult",
    "ListServiceJobsResult",
    "ListTagsForResourceResult",
    "SubmitServiceJobResult",
    "UpdateConsumableResourceResult",
    "UpdateServiceEnvironmentResult",
    "cancel_job",
    "create_compute_environment",
    "create_consumable_resource",
    "create_job_queue",
    "create_scheduling_policy",
    "create_service_environment",
    "delete_compute_environment",
    "delete_consumable_resource",
    "delete_job_queue",
    "delete_scheduling_policy",
    "delete_service_environment",
    "deregister_job_definition",
    "describe_compute_environments",
    "describe_consumable_resource",
    "describe_job_definitions",
    "describe_job_queues",
    "describe_jobs",
    "describe_scheduling_policies",
    "describe_service_environments",
    "describe_service_job",
    "get_job_queue_snapshot",
    "list_consumable_resources",
    "list_jobs",
    "list_jobs_by_consumable_resource",
    "list_scheduling_policies",
    "list_service_jobs",
    "list_tags_for_resource",
    "register_job_definition",
    "submit_and_wait",
    "submit_job",
    "submit_service_job",
    "tag_resource",
    "terminate_job",
    "terminate_service_job",
    "untag_resource",
    "update_compute_environment",
    "update_consumable_resource",
    "update_job_queue",
    "update_scheduling_policy",
    "update_service_environment",
    "wait_for_job",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ComputeEnvironmentResult(BaseModel):
    """Metadata for an AWS Batch compute environment."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    type: str
    state: str
    status: str
    compute_resources: dict[str, Any] | None = None
    service_role: str | None = None
    extra: dict[str, Any] = {}


class JobQueueResult(BaseModel):
    """Metadata for an AWS Batch job queue."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    state: str
    status: str
    priority: int
    compute_environments: list[dict[str, Any]]
    extra: dict[str, Any] = {}


class JobDefinitionResult(BaseModel):
    """Metadata for an AWS Batch job definition."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    revision: int
    type: str
    status: str
    container_properties: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


class JobResult(BaseModel):
    """Metadata for an AWS Batch job."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    job_name: str
    job_queue: str
    status: str
    status_reason: str | None = None
    created_at: int | None = None
    started_at: int | None = None
    stopped_at: int | None = None
    container: dict[str, Any] | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_compute_env(ce: dict[str, Any]) -> ComputeEnvironmentResult:
    """Parse a raw compute-environment dict into a model."""
    return ComputeEnvironmentResult(
        name=ce["computeEnvironmentName"],
        arn=ce["computeEnvironmentArn"],
        type=ce.get("type", "MANAGED"),
        state=ce.get("state", "ENABLED"),
        status=ce.get("status", "VALID"),
        compute_resources=ce.get("computeResources"),
        service_role=ce.get("serviceRole"),
        extra={
            k: v
            for k, v in ce.items()
            if k
            not in {
                "computeEnvironmentName",
                "computeEnvironmentArn",
                "type",
                "state",
                "status",
                "computeResources",
                "serviceRole",
            }
        },
    )


def _parse_job_queue(jq: dict[str, Any]) -> JobQueueResult:
    """Parse a raw job-queue dict into a model."""
    return JobQueueResult(
        name=jq["jobQueueName"],
        arn=jq["jobQueueArn"],
        state=jq.get("state", "ENABLED"),
        status=jq.get("status", "VALID"),
        priority=jq.get("priority", 1),
        compute_environments=jq.get("computeEnvironmentOrder", []),
        extra={
            k: v
            for k, v in jq.items()
            if k
            not in {
                "jobQueueName",
                "jobQueueArn",
                "state",
                "status",
                "priority",
                "computeEnvironmentOrder",
            }
        },
    )


def _parse_job_definition(jd: dict[str, Any]) -> JobDefinitionResult:
    """Parse a raw job-definition dict into a model."""
    return JobDefinitionResult(
        name=jd["jobDefinitionName"],
        arn=jd["jobDefinitionArn"],
        revision=jd.get("revision", 1),
        type=jd.get("type", "container"),
        status=jd.get("status", "ACTIVE"),
        container_properties=jd.get("containerProperties"),
        extra={
            k: v
            for k, v in jd.items()
            if k
            not in {
                "jobDefinitionName",
                "jobDefinitionArn",
                "revision",
                "type",
                "status",
                "containerProperties",
            }
        },
    )


def _parse_job(job: dict[str, Any]) -> JobResult:
    """Parse a raw job dict into a model."""
    return JobResult(
        job_id=job["jobId"],
        job_name=job["jobName"],
        job_queue=job.get("jobQueue", ""),
        status=job.get("status", "SUBMITTED"),
        status_reason=job.get("statusReason"),
        created_at=job.get("createdAt"),
        started_at=job.get("startedAt"),
        stopped_at=job.get("stoppedAt"),
        container=job.get("container"),
        extra={
            k: v
            for k, v in job.items()
            if k
            not in {
                "jobId",
                "jobName",
                "jobQueue",
                "status",
                "statusReason",
                "createdAt",
                "startedAt",
                "stoppedAt",
                "container",
            }
        },
    )


# ---------------------------------------------------------------------------
# Compute environment operations
# ---------------------------------------------------------------------------


def create_compute_environment(
    name: str,
    *,
    type: str = "MANAGED",
    state: str = "ENABLED",
    compute_resources: dict[str, Any] | None = None,
    service_role: str | None = None,
    region_name: str | None = None,
) -> ComputeEnvironmentResult:
    """Create an AWS Batch compute environment.

    Args:
        name: Compute environment name.
        type: ``"MANAGED"`` (default) or ``"UNMANAGED"``.
        state: ``"ENABLED"`` (default) or ``"DISABLED"``.
        compute_resources: Compute resources configuration dict.
        service_role: IAM role ARN for the Batch service.
        region_name: AWS region override.

    Returns:
        A :class:`ComputeEnvironmentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {
        "computeEnvironmentName": name,
        "type": type,
        "state": state,
    }
    if compute_resources is not None:
        kwargs["computeResources"] = compute_resources
    if service_role is not None:
        kwargs["serviceRole"] = service_role

    try:
        resp = client.create_compute_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_compute_environment failed for {name!r}") from exc

    return ComputeEnvironmentResult(
        name=name,
        arn=resp["computeEnvironmentArn"],
        type=type,
        state=state,
        status="VALID",
        compute_resources=compute_resources,
        service_role=service_role,
    )


def describe_compute_environments(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[ComputeEnvironmentResult]:
    """Describe one or more compute environments.

    Args:
        names: Compute environment names or ARNs.  ``None`` lists all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ComputeEnvironmentResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if names is not None:
        kwargs["computeEnvironments"] = names

    try:
        resp = client.describe_compute_environments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_compute_environments failed") from exc

    return [_parse_compute_env(ce) for ce in resp.get("computeEnvironments", [])]


def update_compute_environment(
    name: str,
    *,
    state: str | None = None,
    compute_resources: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ComputeEnvironmentResult:
    """Update an AWS Batch compute environment.

    Args:
        name: Compute environment name or ARN.
        state: New state (``"ENABLED"`` or ``"DISABLED"``).
        compute_resources: Updated compute resources configuration.
        region_name: AWS region override.

    Returns:
        A :class:`ComputeEnvironmentResult` reflecting the update.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {"computeEnvironment": name}
    if state is not None:
        kwargs["state"] = state
    if compute_resources is not None:
        kwargs["computeResources"] = compute_resources

    try:
        resp = client.update_compute_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_compute_environment failed for {name!r}") from exc

    # Describe to get the full current state
    envs = describe_compute_environments(names=[name], region_name=region_name)
    if envs:
        return envs[0]
    return ComputeEnvironmentResult(
        name=name,
        arn=resp.get("computeEnvironmentArn", ""),
        type="MANAGED",
        state=state or "ENABLED",
        status="VALID",
    )


def delete_compute_environment(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an AWS Batch compute environment.

    Args:
        name: Compute environment name or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        client.delete_compute_environment(computeEnvironment=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_compute_environment failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Job queue operations
# ---------------------------------------------------------------------------


def create_job_queue(
    name: str,
    *,
    state: str = "ENABLED",
    priority: int = 1,
    compute_environments: list[dict[str, Any]],
    region_name: str | None = None,
) -> JobQueueResult:
    """Create an AWS Batch job queue.

    Args:
        name: Job queue name.
        state: ``"ENABLED"`` (default) or ``"DISABLED"``.
        priority: Queue scheduling priority.
        compute_environments: List of dicts with ``computeEnvironment``
            and ``order`` keys.
        region_name: AWS region override.

    Returns:
        A :class:`JobQueueResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        resp = client.create_job_queue(
            jobQueueName=name,
            state=state,
            priority=priority,
            computeEnvironmentOrder=compute_environments,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_job_queue failed for {name!r}") from exc

    return JobQueueResult(
        name=name,
        arn=resp["jobQueueArn"],
        state=state,
        status="VALID",
        priority=priority,
        compute_environments=compute_environments,
    )


def describe_job_queues(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[JobQueueResult]:
    """Describe one or more job queues.

    Args:
        names: Job queue names or ARNs.  ``None`` lists all.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobQueueResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if names is not None:
        kwargs["jobQueues"] = names

    try:
        resp = client.describe_job_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_job_queues failed") from exc

    return [_parse_job_queue(jq) for jq in resp.get("jobQueues", [])]


def update_job_queue(
    name: str,
    *,
    state: str | None = None,
    priority: int | None = None,
    compute_environments: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> JobQueueResult:
    """Update an AWS Batch job queue.

    Args:
        name: Job queue name or ARN.
        state: New state (``"ENABLED"`` or ``"DISABLED"``).
        priority: New scheduling priority.
        compute_environments: Updated compute environment order.
        region_name: AWS region override.

    Returns:
        A :class:`JobQueueResult` reflecting the update.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {"jobQueue": name}
    if state is not None:
        kwargs["state"] = state
    if priority is not None:
        kwargs["priority"] = priority
    if compute_environments is not None:
        kwargs["computeEnvironmentOrder"] = compute_environments

    try:
        resp = client.update_job_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_job_queue failed for {name!r}") from exc

    # Describe to get the full current state
    queues = describe_job_queues(names=[name], region_name=region_name)
    if queues:
        return queues[0]
    return JobQueueResult(
        name=name,
        arn=resp.get("jobQueueArn", ""),
        state=state or "ENABLED",
        status="VALID",
        priority=priority or 1,
        compute_environments=compute_environments or [],
    )


def delete_job_queue(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an AWS Batch job queue.

    Args:
        name: Job queue name or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        client.delete_job_queue(jobQueue=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_job_queue failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Job definition operations
# ---------------------------------------------------------------------------


def register_job_definition(
    name: str,
    *,
    type: str = "container",
    container_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> JobDefinitionResult:
    """Register a new AWS Batch job definition.

    Args:
        name: Job definition name.
        type: ``"container"`` (default) or ``"multinode"``.
        container_properties: Container configuration dict.
        region_name: AWS region override.

    Returns:
        A :class:`JobDefinitionResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {
        "jobDefinitionName": name,
        "type": type,
    }
    if container_properties is not None:
        kwargs["containerProperties"] = container_properties

    try:
        resp = client.register_job_definition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"register_job_definition failed for {name!r}") from exc

    return JobDefinitionResult(
        name=name,
        arn=resp["jobDefinitionArn"],
        revision=resp.get("revision", 1),
        type=type,
        status="ACTIVE",
        container_properties=container_properties,
    )


def describe_job_definitions(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[JobDefinitionResult]:
    """Describe one or more job definitions.

    Args:
        names: Job definition names or ARNs.  ``None`` lists all.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobDefinitionResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if names is not None:
        kwargs["jobDefinitions"] = names

    try:
        resp = client.describe_job_definitions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_job_definitions failed") from exc

    return [_parse_job_definition(jd) for jd in resp.get("jobDefinitions", [])]


def deregister_job_definition(
    job_definition: str,
    *,
    region_name: str | None = None,
) -> None:
    """Deregister an AWS Batch job definition.

    Args:
        job_definition: Job definition name:revision or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        client.deregister_job_definition(jobDefinition=job_definition)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"deregister_job_definition failed for {job_definition!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


def submit_job(
    job_name: str,
    *,
    job_queue: str,
    job_definition: str,
    parameters: dict[str, str] | None = None,
    container_overrides: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> str:
    """Submit a job to an AWS Batch job queue.

    Args:
        job_name: Human-readable job name.
        job_queue: Job queue name or ARN.
        job_definition: Job definition name:revision or ARN.
        parameters: Parameter substitutions for the job.
        container_overrides: Container override dict.
        region_name: AWS region override.

    Returns:
        The job ID string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {
        "jobName": job_name,
        "jobQueue": job_queue,
        "jobDefinition": job_definition,
    }
    if parameters is not None:
        kwargs["parameters"] = parameters
    if container_overrides is not None:
        kwargs["containerOverrides"] = container_overrides

    try:
        resp = client.submit_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"submit_job failed for {job_name!r}") from exc

    return resp["jobId"]


def describe_jobs(
    job_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[JobResult]:
    """Describe one or more AWS Batch jobs.

    Args:
        job_ids: Job ID strings (up to 100).
        region_name: AWS region override.

    Returns:
        A list of :class:`JobResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        resp = client.describe_jobs(jobs=job_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_jobs failed") from exc

    return [_parse_job(j) for j in resp.get("jobs", [])]


def list_jobs(
    job_queue: str,
    *,
    job_status: str | None = None,
    region_name: str | None = None,
) -> list[JobResult]:
    """List jobs in an AWS Batch job queue.

    Args:
        job_queue: Job queue name or ARN.
        job_status: Filter by status (e.g. ``"SUBMITTED"``, ``"RUNNING"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`JobResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {"jobQueue": job_queue}
    if job_status is not None:
        kwargs["jobStatus"] = job_status

    try:
        resp = client.list_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc

    return [_parse_job(j) for j in resp.get("jobSummaryList", [])]


def cancel_job(
    job_id: str,
    *,
    reason: str,
    region_name: str | None = None,
) -> None:
    """Cancel an AWS Batch job.

    Args:
        job_id: The job ID to cancel.
        reason: Human-readable cancellation reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        client.cancel_job(jobId=job_id, reason=reason)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"cancel_job failed for {job_id!r}") from exc


def terminate_job(
    job_id: str,
    *,
    reason: str,
    region_name: str | None = None,
) -> None:
    """Terminate an AWS Batch job.

    Args:
        job_id: The job ID to terminate.
        reason: Human-readable termination reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    try:
        client.terminate_job(jobId=job_id, reason=reason)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"terminate_job failed for {job_id!r}") from exc


# ---------------------------------------------------------------------------
# Polling / composite operations
# ---------------------------------------------------------------------------


def wait_for_job(
    job_id: str,
    *,
    target_statuses: tuple[str, ...] = ("SUCCEEDED",),
    failure_statuses: tuple[str, ...] = ("FAILED",),
    timeout: float = 600,
    poll_interval: float = 10,
    region_name: str | None = None,
) -> JobResult:
    """Poll until a job reaches a target or failure status.

    Args:
        job_id: The job ID to monitor.
        target_statuses: Statuses considered successful.
        failure_statuses: Statuses considered terminal failures.
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`JobResult` in a target status.

    Raises:
        AwsTimeoutError: If the job does not reach a target status in time.
        AwsServiceError: If the job reaches a failure status.
        RuntimeError: If the job is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        jobs = describe_jobs([job_id], region_name=region_name)
        if not jobs:
            raise AwsServiceError(f"Job {job_id!r} not found")
        job = jobs[0]
        if job.status in target_statuses:
            return job
        if job.status in failure_statuses:
            raise AwsServiceError(
                f"Job {job_id!r} reached failure status {job.status!r}: "
                f"{job.status_reason or 'no reason'}"
            )
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Job {job_id!r} did not reach status "
                f"{target_statuses!r} within {timeout}s "
                f"(current: {job.status!r})"
            )
        time.sleep(poll_interval)


def submit_and_wait(
    job_name: str,
    *,
    job_queue: str,
    job_definition: str,
    parameters: dict[str, str] | None = None,
    container_overrides: dict[str, Any] | None = None,
    timeout: float = 600,
    poll_interval: float = 10,
    region_name: str | None = None,
) -> JobResult:
    """Submit a job and wait for it to succeed.

    Combines :func:`submit_job` and :func:`wait_for_job`.

    Args:
        job_name: Human-readable job name.
        job_queue: Job queue name or ARN.
        job_definition: Job definition name:revision or ARN.
        parameters: Parameter substitutions.
        container_overrides: Container override dict.
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The final :class:`JobResult` in ``SUCCEEDED`` status.

    Raises:
        AwsTimeoutError: If the job does not succeed in time.
        AwsServiceError: If the job fails.
        RuntimeError: If submit or describe calls fail.
    """
    job_id = submit_job(
        job_name,
        job_queue=job_queue,
        job_definition=job_definition,
        parameters=parameters,
        container_overrides=container_overrides,
        region_name=region_name,
    )
    return wait_for_job(
        job_id,
        timeout=timeout,
        poll_interval=poll_interval,
        region_name=region_name,
    )


class CreateConsumableResourceResult(BaseModel):
    """Result of create_consumable_resource."""

    model_config = ConfigDict(frozen=True)

    consumable_resource_name: str | None = None
    consumable_resource_arn: str | None = None


class CreateSchedulingPolicyResult(BaseModel):
    """Result of create_scheduling_policy."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    arn: str | None = None


class CreateServiceEnvironmentResult(BaseModel):
    """Result of create_service_environment."""

    model_config = ConfigDict(frozen=True)

    service_environment_name: str | None = None
    service_environment_arn: str | None = None


class DescribeConsumableResourceResult(BaseModel):
    """Result of describe_consumable_resource."""

    model_config = ConfigDict(frozen=True)

    consumable_resource_name: str | None = None
    consumable_resource_arn: str | None = None
    total_quantity: int | None = None
    in_use_quantity: int | None = None
    available_quantity: int | None = None
    resource_type: str | None = None
    created_at: int | None = None
    tags: dict[str, Any] | None = None


class DescribeSchedulingPoliciesResult(BaseModel):
    """Result of describe_scheduling_policies."""

    model_config = ConfigDict(frozen=True)

    scheduling_policies: list[dict[str, Any]] | None = None


class DescribeServiceEnvironmentsResult(BaseModel):
    """Result of describe_service_environments."""

    model_config = ConfigDict(frozen=True)

    service_environments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeServiceJobResult(BaseModel):
    """Result of describe_service_job."""

    model_config = ConfigDict(frozen=True)

    attempts: list[dict[str, Any]] | None = None
    created_at: int | None = None
    is_terminated: bool | None = None
    job_arn: str | None = None
    job_id: str | None = None
    job_name: str | None = None
    job_queue: str | None = None
    latest_attempt: dict[str, Any] | None = None
    retry_strategy: dict[str, Any] | None = None
    scheduling_priority: int | None = None
    service_request_payload: str | None = None
    service_job_type: str | None = None
    share_identifier: str | None = None
    started_at: int | None = None
    status: str | None = None
    status_reason: str | None = None
    stopped_at: int | None = None
    tags: dict[str, Any] | None = None
    timeout_config: dict[str, Any] | None = None


class GetJobQueueSnapshotResult(BaseModel):
    """Result of get_job_queue_snapshot."""

    model_config = ConfigDict(frozen=True)

    front_of_queue: dict[str, Any] | None = None


class ListConsumableResourcesResult(BaseModel):
    """Result of list_consumable_resources."""

    model_config = ConfigDict(frozen=True)

    consumable_resources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListJobsByConsumableResourceResult(BaseModel):
    """Result of list_jobs_by_consumable_resource."""

    model_config = ConfigDict(frozen=True)

    jobs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSchedulingPoliciesResult(BaseModel):
    """Result of list_scheduling_policies."""

    model_config = ConfigDict(frozen=True)

    scheduling_policies: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListServiceJobsResult(BaseModel):
    """Result of list_service_jobs."""

    model_config = ConfigDict(frozen=True)

    job_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class SubmitServiceJobResult(BaseModel):
    """Result of submit_service_job."""

    model_config = ConfigDict(frozen=True)

    job_arn: str | None = None
    job_name: str | None = None
    job_id: str | None = None


class UpdateConsumableResourceResult(BaseModel):
    """Result of update_consumable_resource."""

    model_config = ConfigDict(frozen=True)

    consumable_resource_name: str | None = None
    consumable_resource_arn: str | None = None
    total_quantity: int | None = None


class UpdateServiceEnvironmentResult(BaseModel):
    """Result of update_service_environment."""

    model_config = ConfigDict(frozen=True)

    service_environment_name: str | None = None
    service_environment_arn: str | None = None


def create_consumable_resource(
    consumable_resource_name: str,
    *,
    total_quantity: int | None = None,
    resource_type: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateConsumableResourceResult:
    """Create consumable resource.

    Args:
        consumable_resource_name: Consumable resource name.
        total_quantity: Total quantity.
        resource_type: Resource type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["consumableResourceName"] = consumable_resource_name
    if total_quantity is not None:
        kwargs["totalQuantity"] = total_quantity
    if resource_type is not None:
        kwargs["resourceType"] = resource_type
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_consumable_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create consumable resource") from exc
    return CreateConsumableResourceResult(
        consumable_resource_name=resp.get("consumableResourceName"),
        consumable_resource_arn=resp.get("consumableResourceArn"),
    )


def create_scheduling_policy(
    name: str,
    *,
    fairshare_policy: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateSchedulingPolicyResult:
    """Create scheduling policy.

    Args:
        name: Name.
        fairshare_policy: Fairshare policy.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if fairshare_policy is not None:
        kwargs["fairsharePolicy"] = fairshare_policy
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_scheduling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create scheduling policy") from exc
    return CreateSchedulingPolicyResult(
        name=resp.get("name"),
        arn=resp.get("arn"),
    )


def create_service_environment(
    service_environment_name: str,
    service_environment_type: str,
    capacity_limits: list[dict[str, Any]],
    *,
    state: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateServiceEnvironmentResult:
    """Create service environment.

    Args:
        service_environment_name: Service environment name.
        service_environment_type: Service environment type.
        capacity_limits: Capacity limits.
        state: State.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceEnvironmentName"] = service_environment_name
    kwargs["serviceEnvironmentType"] = service_environment_type
    kwargs["capacityLimits"] = capacity_limits
    if state is not None:
        kwargs["state"] = state
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_service_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create service environment") from exc
    return CreateServiceEnvironmentResult(
        service_environment_name=resp.get("serviceEnvironmentName"),
        service_environment_arn=resp.get("serviceEnvironmentArn"),
    )


def delete_consumable_resource(
    consumable_resource: str,
    region_name: str | None = None,
) -> None:
    """Delete consumable resource.

    Args:
        consumable_resource: Consumable resource.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["consumableResource"] = consumable_resource
    try:
        client.delete_consumable_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete consumable resource") from exc
    return None


def delete_scheduling_policy(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete scheduling policy.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        client.delete_scheduling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduling policy") from exc
    return None


def delete_service_environment(
    service_environment: str,
    region_name: str | None = None,
) -> None:
    """Delete service environment.

    Args:
        service_environment: Service environment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceEnvironment"] = service_environment
    try:
        client.delete_service_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete service environment") from exc
    return None


def describe_consumable_resource(
    consumable_resource: str,
    region_name: str | None = None,
) -> DescribeConsumableResourceResult:
    """Describe consumable resource.

    Args:
        consumable_resource: Consumable resource.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["consumableResource"] = consumable_resource
    try:
        resp = client.describe_consumable_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe consumable resource") from exc
    return DescribeConsumableResourceResult(
        consumable_resource_name=resp.get("consumableResourceName"),
        consumable_resource_arn=resp.get("consumableResourceArn"),
        total_quantity=resp.get("totalQuantity"),
        in_use_quantity=resp.get("inUseQuantity"),
        available_quantity=resp.get("availableQuantity"),
        resource_type=resp.get("resourceType"),
        created_at=resp.get("createdAt"),
        tags=resp.get("tags"),
    )


def describe_scheduling_policies(
    arns: list[str],
    region_name: str | None = None,
) -> DescribeSchedulingPoliciesResult:
    """Describe scheduling policies.

    Args:
        arns: Arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arns"] = arns
    try:
        resp = client.describe_scheduling_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduling policies") from exc
    return DescribeSchedulingPoliciesResult(
        scheduling_policies=resp.get("schedulingPolicies"),
    )


def describe_service_environments(
    *,
    service_environments: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeServiceEnvironmentsResult:
    """Describe service environments.

    Args:
        service_environments: Service environments.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if service_environments is not None:
        kwargs["serviceEnvironments"] = service_environments
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.describe_service_environments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe service environments") from exc
    return DescribeServiceEnvironmentsResult(
        service_environments=resp.get("serviceEnvironments"),
        next_token=resp.get("nextToken"),
    )


def describe_service_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeServiceJobResult:
    """Describe service job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    try:
        resp = client.describe_service_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe service job") from exc
    return DescribeServiceJobResult(
        attempts=resp.get("attempts"),
        created_at=resp.get("createdAt"),
        is_terminated=resp.get("isTerminated"),
        job_arn=resp.get("jobArn"),
        job_id=resp.get("jobId"),
        job_name=resp.get("jobName"),
        job_queue=resp.get("jobQueue"),
        latest_attempt=resp.get("latestAttempt"),
        retry_strategy=resp.get("retryStrategy"),
        scheduling_priority=resp.get("schedulingPriority"),
        service_request_payload=resp.get("serviceRequestPayload"),
        service_job_type=resp.get("serviceJobType"),
        share_identifier=resp.get("shareIdentifier"),
        started_at=resp.get("startedAt"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        stopped_at=resp.get("stoppedAt"),
        tags=resp.get("tags"),
        timeout_config=resp.get("timeoutConfig"),
    )


def get_job_queue_snapshot(
    job_queue: str,
    region_name: str | None = None,
) -> GetJobQueueSnapshotResult:
    """Get job queue snapshot.

    Args:
        job_queue: Job queue.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobQueue"] = job_queue
    try:
        resp = client.get_job_queue_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get job queue snapshot") from exc
    return GetJobQueueSnapshotResult(
        front_of_queue=resp.get("frontOfQueue"),
    )


def list_consumable_resources(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConsumableResourcesResult:
    """List consumable resources.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_consumable_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list consumable resources") from exc
    return ListConsumableResourcesResult(
        consumable_resources=resp.get("consumableResources"),
        next_token=resp.get("nextToken"),
    )


def list_jobs_by_consumable_resource(
    consumable_resource: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListJobsByConsumableResourceResult:
    """List jobs by consumable resource.

    Args:
        consumable_resource: Consumable resource.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["consumableResource"] = consumable_resource
    if filters is not None:
        kwargs["filters"] = filters
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_jobs_by_consumable_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list jobs by consumable resource") from exc
    return ListJobsByConsumableResourceResult(
        jobs=resp.get("jobs"),
        next_token=resp.get("nextToken"),
    )


def list_scheduling_policies(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSchedulingPoliciesResult:
    """List scheduling policies.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_scheduling_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list scheduling policies") from exc
    return ListSchedulingPoliciesResult(
        scheduling_policies=resp.get("schedulingPolicies"),
        next_token=resp.get("nextToken"),
    )


def list_service_jobs(
    *,
    job_queue: str | None = None,
    job_status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListServiceJobsResult:
    """List service jobs.

    Args:
        job_queue: Job queue.
        job_status: Job status.
        max_results: Max results.
        next_token: Next token.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    if job_queue is not None:
        kwargs["jobQueue"] = job_queue
    if job_status is not None:
        kwargs["jobStatus"] = job_status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if filters is not None:
        kwargs["filters"] = filters
    try:
        resp = client.list_service_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list service jobs") from exc
    return ListServiceJobsResult(
        job_summary_list=resp.get("jobSummaryList"),
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
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def submit_service_job(
    job_name: str,
    job_queue: str,
    service_request_payload: str,
    service_job_type: str,
    *,
    retry_strategy: dict[str, Any] | None = None,
    scheduling_priority: int | None = None,
    share_identifier: str | None = None,
    timeout_config: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> SubmitServiceJobResult:
    """Submit service job.

    Args:
        job_name: Job name.
        job_queue: Job queue.
        service_request_payload: Service request payload.
        service_job_type: Service job type.
        retry_strategy: Retry strategy.
        scheduling_priority: Scheduling priority.
        share_identifier: Share identifier.
        timeout_config: Timeout config.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["jobQueue"] = job_queue
    kwargs["serviceRequestPayload"] = service_request_payload
    kwargs["serviceJobType"] = service_job_type
    if retry_strategy is not None:
        kwargs["retryStrategy"] = retry_strategy
    if scheduling_priority is not None:
        kwargs["schedulingPriority"] = scheduling_priority
    if share_identifier is not None:
        kwargs["shareIdentifier"] = share_identifier
    if timeout_config is not None:
        kwargs["timeoutConfig"] = timeout_config
    if tags is not None:
        kwargs["tags"] = tags
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.submit_service_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to submit service job") from exc
    return SubmitServiceJobResult(
        job_arn=resp.get("jobArn"),
        job_name=resp.get("jobName"),
        job_id=resp.get("jobId"),
    )


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
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def terminate_service_job(
    job_id: str,
    reason: str,
    region_name: str | None = None,
) -> None:
    """Terminate service job.

    Args:
        job_id: Job id.
        reason: Reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["reason"] = reason
    try:
        client.terminate_service_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to terminate service job") from exc
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
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_consumable_resource(
    consumable_resource: str,
    *,
    operation: str | None = None,
    quantity: int | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdateConsumableResourceResult:
    """Update consumable resource.

    Args:
        consumable_resource: Consumable resource.
        operation: Operation.
        quantity: Quantity.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["consumableResource"] = consumable_resource
    if operation is not None:
        kwargs["operation"] = operation
    if quantity is not None:
        kwargs["quantity"] = quantity
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.update_consumable_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update consumable resource") from exc
    return UpdateConsumableResourceResult(
        consumable_resource_name=resp.get("consumableResourceName"),
        consumable_resource_arn=resp.get("consumableResourceArn"),
        total_quantity=resp.get("totalQuantity"),
    )


def update_scheduling_policy(
    arn: str,
    *,
    fairshare_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update scheduling policy.

    Args:
        arn: Arn.
        fairshare_policy: Fairshare policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if fairshare_policy is not None:
        kwargs["fairsharePolicy"] = fairshare_policy
    try:
        client.update_scheduling_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update scheduling policy") from exc
    return None


def update_service_environment(
    service_environment: str,
    *,
    state: str | None = None,
    capacity_limits: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateServiceEnvironmentResult:
    """Update service environment.

    Args:
        service_environment: Service environment.
        state: State.
        capacity_limits: Capacity limits.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("batch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceEnvironment"] = service_environment
    if state is not None:
        kwargs["state"] = state
    if capacity_limits is not None:
        kwargs["capacityLimits"] = capacity_limits
    try:
        resp = client.update_service_environment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update service environment") from exc
    return UpdateServiceEnvironmentResult(
        service_environment_name=resp.get("serviceEnvironmentName"),
        service_environment_arn=resp.get("serviceEnvironmentArn"),
    )
