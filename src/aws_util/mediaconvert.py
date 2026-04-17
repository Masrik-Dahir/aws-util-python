"""aws_util.mediaconvert --- AWS Elemental MediaConvert utilities.

Provides helpers for managing MediaConvert jobs, job templates, queues,
and endpoints.  Each function wraps a single boto3 MediaConvert API call
with structured Pydantic result models and consistent error handling.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "CreatePresetResult",
    "EndpointResult",
    "GetJobsQueryResultsResult",
    "GetPolicyResult",
    "GetPresetResult",
    "JobResult",
    "JobTemplateResult",
    "ListPresetsResult",
    "ListTagsForResourceResult",
    "ListVersionsResult",
    "ProbeResult",
    "PutPolicyResult",
    "QueueResult",
    "SearchJobsResult",
    "StartJobsQueryResult",
    "UpdateJobTemplateResult",
    "UpdatePresetResult",
    "UpdateQueueResult",
    "associate_certificate",
    "cancel_job",
    "create_job",
    "create_job_template",
    "create_preset",
    "create_queue",
    "create_resource_share",
    "delete_job_template",
    "delete_policy",
    "delete_preset",
    "delete_queue",
    "describe_endpoints",
    "disassociate_certificate",
    "get_job",
    "get_job_template",
    "get_jobs_query_results",
    "get_policy",
    "get_preset",
    "get_queue",
    "list_job_templates",
    "list_jobs",
    "list_presets",
    "list_queues",
    "list_tags_for_resource",
    "list_versions",
    "probe",
    "put_policy",
    "search_jobs",
    "start_jobs_query",
    "tag_resource",
    "untag_resource",
    "update_job_template",
    "update_preset",
    "update_queue",
    "wait_for_job",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class JobResult(BaseModel):
    """Metadata for a MediaConvert job."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str | None = None
    status: str | None = None
    queue: str | None = None
    role: str | None = None
    settings: dict[str, Any] = {}
    created_at: Any = None
    error_code: int | None = None
    error_message: str | None = None
    extra: dict[str, Any] = {}


class JobTemplateResult(BaseModel):
    """Metadata for a MediaConvert job template."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str | None = None
    description: str | None = None
    category: str | None = None
    queue: str | None = None
    settings: dict[str, Any] = {}
    extra: dict[str, Any] = {}


class QueueResult(BaseModel):
    """Metadata for a MediaConvert queue."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str | None = None
    status: str | None = None
    description: str | None = None
    pricing_plan: str | None = None
    extra: dict[str, Any] = {}


class EndpointResult(BaseModel):
    """A MediaConvert account endpoint."""

    model_config = ConfigDict(frozen=True)

    url: str
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_job(data: dict[str, Any]) -> JobResult:
    """Convert a raw API job dict to a :class:`JobResult`."""
    return JobResult(
        id=data.get("Id", ""),
        arn=data.get("Arn"),
        status=data.get("Status"),
        queue=data.get("Queue"),
        role=data.get("Role"),
        settings=data.get("Settings", {}),
        created_at=data.get("CreatedAt"),
        error_code=data.get("ErrorCode"),
        error_message=data.get("ErrorMessage"),
    )


def _parse_job_template(data: dict[str, Any]) -> JobTemplateResult:
    """Convert a raw API job template dict to a :class:`JobTemplateResult`."""
    return JobTemplateResult(
        name=data.get("Name", ""),
        arn=data.get("Arn"),
        description=data.get("Description"),
        category=data.get("Category"),
        queue=data.get("Queue"),
        settings=data.get("Settings", {}),
    )


def _parse_queue(data: dict[str, Any]) -> QueueResult:
    """Convert a raw API queue dict to a :class:`QueueResult`."""
    return QueueResult(
        name=data.get("Name", ""),
        arn=data.get("Arn"),
        status=data.get("Status"),
        description=data.get("Description"),
        pricing_plan=data.get("PricingPlan"),
    )


# ---------------------------------------------------------------------------
# Job functions
# ---------------------------------------------------------------------------


def create_job(
    role: str,
    settings: dict[str, Any],
    *,
    queue: str | None = None,
    job_template: str | None = None,
    region_name: str | None = None,
) -> JobResult:
    """Create a MediaConvert transcoding job.

    Args:
        role: IAM role ARN for the job.
        settings: Job settings dict containing input/output configurations.
        queue: Queue ARN or name to submit the job to.
        job_template: Job template name or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`JobResult` describing the new job.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {
        "Role": role,
        "Settings": settings,
    }
    if queue is not None:
        kwargs["Queue"] = queue
    if job_template is not None:
        kwargs["JobTemplate"] = job_template
    try:
        resp = client.create_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_job failed") from exc
    return _parse_job(resp.get("Job", {}))


def get_job(
    job_id: str,
    *,
    region_name: str | None = None,
) -> JobResult:
    """Fetch a MediaConvert job by ID.

    Args:
        job_id: The job identifier.
        region_name: AWS region override.

    Returns:
        A :class:`JobResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        resp = client.get_job(Id=job_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_job failed for {job_id!r}") from exc
    return _parse_job(resp.get("Job", {}))


def list_jobs(
    *,
    queue: str | None = None,
    status: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[JobResult]:
    """List MediaConvert jobs, optionally filtered by queue or status.

    Args:
        queue: Queue ARN to filter by.
        status: Job status filter (e.g. ``"SUBMITTED"``, ``"COMPLETE"``).
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if queue is not None:
        kwargs["Queue"] = queue
    if status is not None:
        kwargs["Status"] = status
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    jobs: list[JobResult] = []
    try:
        while True:
            resp = client.list_jobs(**kwargs)
            for j in resp.get("Jobs", []):
                jobs.append(_parse_job(j))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return jobs


def cancel_job(
    job_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Cancel a MediaConvert job.

    Args:
        job_id: The job identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        client.cancel_job(Id=job_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"cancel_job failed for {job_id!r}") from exc


# ---------------------------------------------------------------------------
# Job template functions
# ---------------------------------------------------------------------------


def create_job_template(
    name: str,
    settings: dict[str, Any],
    *,
    description: str | None = None,
    category: str | None = None,
    queue: str | None = None,
    region_name: str | None = None,
) -> JobTemplateResult:
    """Create a MediaConvert job template.

    Args:
        name: Template name.
        settings: Template settings dict.
        description: Human-readable description.
        category: Template category.
        queue: Default queue ARN.
        region_name: AWS region override.

    Returns:
        A :class:`JobTemplateResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "Settings": settings,
    }
    if description is not None:
        kwargs["Description"] = description
    if category is not None:
        kwargs["Category"] = category
    if queue is not None:
        kwargs["Queue"] = queue
    try:
        resp = client.create_job_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_job_template failed") from exc
    return _parse_job_template(resp.get("JobTemplate", {}))


def get_job_template(
    name: str,
    *,
    region_name: str | None = None,
) -> JobTemplateResult:
    """Fetch a MediaConvert job template by name.

    Args:
        name: The template name.
        region_name: AWS region override.

    Returns:
        A :class:`JobTemplateResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        resp = client.get_job_template(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_job_template failed for {name!r}") from exc
    return _parse_job_template(resp.get("JobTemplate", {}))


def list_job_templates(
    *,
    category: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[JobTemplateResult]:
    """List MediaConvert job templates.

    Args:
        category: Filter by category.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`JobTemplateResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if category is not None:
        kwargs["Category"] = category
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    templates: list[JobTemplateResult] = []
    try:
        while True:
            resp = client.list_job_templates(**kwargs)
            for t in resp.get("JobTemplates", []):
                templates.append(_parse_job_template(t))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_job_templates failed") from exc
    return templates


def delete_job_template(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a MediaConvert job template.

    Args:
        name: The template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        client.delete_job_template(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_job_template failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Queue functions
# ---------------------------------------------------------------------------


def create_queue(
    name: str,
    *,
    description: str | None = None,
    pricing_plan: str | None = None,
    region_name: str | None = None,
) -> QueueResult:
    """Create a MediaConvert queue.

    Args:
        name: Queue name.
        description: Human-readable description.
        pricing_plan: ``"ON_DEMAND"`` or ``"RESERVED"``.
        region_name: AWS region override.

    Returns:
        A :class:`QueueResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {"Name": name}
    if description is not None:
        kwargs["Description"] = description
    if pricing_plan is not None:
        kwargs["PricingPlan"] = pricing_plan
    try:
        resp = client.create_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_queue failed") from exc
    return _parse_queue(resp.get("Queue", {}))


def get_queue(
    name: str,
    *,
    region_name: str | None = None,
) -> QueueResult:
    """Fetch a MediaConvert queue by name.

    Args:
        name: The queue name.
        region_name: AWS region override.

    Returns:
        A :class:`QueueResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        resp = client.get_queue(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_queue failed for {name!r}") from exc
    return _parse_queue(resp.get("Queue", {}))


def list_queues(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[QueueResult]:
    """List MediaConvert queues.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`QueueResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    queues: list[QueueResult] = []
    try:
        while True:
            resp = client.list_queues(**kwargs)
            for q in resp.get("Queues", []):
                queues.append(_parse_queue(q))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_queues failed") from exc
    return queues


def delete_queue(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a MediaConvert queue.

    Args:
        name: The queue name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    try:
        client.delete_queue(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_queue failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Endpoint functions
# ---------------------------------------------------------------------------


def describe_endpoints(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[EndpointResult]:
    """Describe MediaConvert account-specific endpoints.

    Args:
        max_results: Maximum number of results.
        region_name: AWS region override.

    Returns:
        A list of :class:`EndpointResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    endpoints: list[EndpointResult] = []
    try:
        while True:
            resp = client.describe_endpoints(**kwargs)
            for ep in resp.get("Endpoints", []):
                endpoints.append(EndpointResult(url=ep.get("Url", "")))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_endpoints failed") from exc
    return endpoints


# ---------------------------------------------------------------------------
# Polling / wait utilities
# ---------------------------------------------------------------------------


def wait_for_job(
    job_id: str,
    *,
    target_statuses: list[str] | None = None,
    timeout: float = 600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> JobResult:
    """Poll until a MediaConvert job reaches a terminal status.

    Args:
        job_id: The job identifier.
        target_statuses: Statuses considered complete.  Defaults to
            ``["COMPLETE", "ERROR", "CANCELED"]``.
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`JobResult` once a target status is reached.

    Raises:
        AwsTimeoutError: If *timeout* is exceeded.
        RuntimeError: If an API call fails.
    """
    if target_statuses is None:
        target_statuses = ["COMPLETE", "ERROR", "CANCELED"]
    deadline = time.monotonic() + timeout
    while True:
        result = get_job(job_id, region_name=region_name)
        if result.status in target_statuses:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Job {job_id!r} did not reach "
                f"{target_statuses!r} within {timeout}s "
                f"(current: {result.status!r})"
            )
        time.sleep(poll_interval)


class CreatePresetResult(BaseModel):
    """Result of create_preset."""

    model_config = ConfigDict(frozen=True)

    preset: dict[str, Any] | None = None


class GetJobsQueryResultsResult(BaseModel):
    """Result of get_jobs_query_results."""

    model_config = ConfigDict(frozen=True)

    jobs: list[dict[str, Any]] | None = None
    next_token: str | None = None
    status: str | None = None


class GetPolicyResult(BaseModel):
    """Result of get_policy."""

    model_config = ConfigDict(frozen=True)

    policy: dict[str, Any] | None = None


class GetPresetResult(BaseModel):
    """Result of get_preset."""

    model_config = ConfigDict(frozen=True)

    preset: dict[str, Any] | None = None


class ListPresetsResult(BaseModel):
    """Result of list_presets."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    presets: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_tags: dict[str, Any] | None = None


class ListVersionsResult(BaseModel):
    """Result of list_versions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    versions: list[dict[str, Any]] | None = None


class ProbeResult(BaseModel):
    """Result of probe."""

    model_config = ConfigDict(frozen=True)

    probe_results: list[dict[str, Any]] | None = None


class PutPolicyResult(BaseModel):
    """Result of put_policy."""

    model_config = ConfigDict(frozen=True)

    policy: dict[str, Any] | None = None


class SearchJobsResult(BaseModel):
    """Result of search_jobs."""

    model_config = ConfigDict(frozen=True)

    jobs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class StartJobsQueryResult(BaseModel):
    """Result of start_jobs_query."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None


class UpdateJobTemplateResult(BaseModel):
    """Result of update_job_template."""

    model_config = ConfigDict(frozen=True)

    job_template: dict[str, Any] | None = None


class UpdatePresetResult(BaseModel):
    """Result of update_preset."""

    model_config = ConfigDict(frozen=True)

    preset: dict[str, Any] | None = None


class UpdateQueueResult(BaseModel):
    """Result of update_queue."""

    model_config = ConfigDict(frozen=True)

    queue: dict[str, Any] | None = None


def associate_certificate(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Associate certificate.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        client.associate_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate certificate") from exc
    return None


def create_preset(
    name: str,
    settings: dict[str, Any],
    *,
    category: str | None = None,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePresetResult:
    """Create preset.

    Args:
        name: Name.
        settings: Settings.
        category: Category.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Settings"] = settings
    if category is not None:
        kwargs["Category"] = category
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_preset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create preset") from exc
    return CreatePresetResult(
        preset=resp.get("Preset"),
    )


def create_resource_share(
    job_id: str,
    support_case_id: str,
    region_name: str | None = None,
) -> None:
    """Create resource share.

    Args:
        job_id: Job id.
        support_case_id: Support case id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    kwargs["SupportCaseId"] = support_case_id
    try:
        client.create_resource_share(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create resource share") from exc
    return None


def delete_policy(
    region_name: str | None = None,
) -> None:
    """Delete policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.delete_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete policy") from exc
    return None


def delete_preset(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete preset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_preset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete preset") from exc
    return None


def disassociate_certificate(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Disassociate certificate.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        client.disassociate_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate certificate") from exc
    return None


def get_jobs_query_results(
    id: str,
    region_name: str | None = None,
) -> GetJobsQueryResultsResult:
    """Get jobs query results.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_jobs_query_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get jobs query results") from exc
    return GetJobsQueryResultsResult(
        jobs=resp.get("Jobs"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
    )


def get_policy(
    region_name: str | None = None,
) -> GetPolicyResult:
    """Get policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get policy") from exc
    return GetPolicyResult(
        policy=resp.get("Policy"),
    )


def get_preset(
    name: str,
    region_name: str | None = None,
) -> GetPresetResult:
    """Get preset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.get_preset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get preset") from exc
    return GetPresetResult(
        preset=resp.get("Preset"),
    )


def list_presets(
    *,
    category: str | None = None,
    list_by: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    order: str | None = None,
    region_name: str | None = None,
) -> ListPresetsResult:
    """List presets.

    Args:
        category: Category.
        list_by: List by.
        max_results: Max results.
        next_token: Next token.
        order: Order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if category is not None:
        kwargs["Category"] = category
    if list_by is not None:
        kwargs["ListBy"] = list_by
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if order is not None:
        kwargs["Order"] = order
    try:
        resp = client.list_presets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list presets") from exc
    return ListPresetsResult(
        next_token=resp.get("NextToken"),
        presets=resp.get("Presets"),
    )


def list_tags_for_resource(
    arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_tags=resp.get("ResourceTags"),
    )


def list_versions(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListVersionsResult:
    """List versions.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list versions") from exc
    return ListVersionsResult(
        next_token=resp.get("NextToken"),
        versions=resp.get("Versions"),
    )


def probe(
    *,
    input_files: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ProbeResult:
    """Probe.

    Args:
        input_files: Input files.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if input_files is not None:
        kwargs["InputFiles"] = input_files
    try:
        resp = client.probe(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to probe") from exc
    return ProbeResult(
        probe_results=resp.get("ProbeResults"),
    )


def put_policy(
    policy: dict[str, Any],
    region_name: str | None = None,
) -> PutPolicyResult:
    """Put policy.

    Args:
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Policy"] = policy
    try:
        resp = client.put_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put policy") from exc
    return PutPolicyResult(
        policy=resp.get("Policy"),
    )


def search_jobs(
    *,
    input_file: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    order: str | None = None,
    queue: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> SearchJobsResult:
    """Search jobs.

    Args:
        input_file: Input file.
        max_results: Max results.
        next_token: Next token.
        order: Order.
        queue: Queue.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if input_file is not None:
        kwargs["InputFile"] = input_file
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if order is not None:
        kwargs["Order"] = order
    if queue is not None:
        kwargs["Queue"] = queue
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = client.search_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search jobs") from exc
    return SearchJobsResult(
        jobs=resp.get("Jobs"),
        next_token=resp.get("NextToken"),
    )


def start_jobs_query(
    *,
    filter_list: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    order: str | None = None,
    region_name: str | None = None,
) -> StartJobsQueryResult:
    """Start jobs query.

    Args:
        filter_list: Filter list.
        max_results: Max results.
        next_token: Next token.
        order: Order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if filter_list is not None:
        kwargs["FilterList"] = filter_list
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if order is not None:
        kwargs["Order"] = order
    try:
        resp = client.start_jobs_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start jobs query") from exc
    return StartJobsQueryResult(
        id=resp.get("Id"),
    )


def tag_resource(
    arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        arn: Arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    arn: str,
    *,
    tag_keys: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        arn: Arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_job_template(
    name: str,
    *,
    acceleration_settings: dict[str, Any] | None = None,
    category: str | None = None,
    description: str | None = None,
    hop_destinations: list[dict[str, Any]] | None = None,
    priority: int | None = None,
    queue: str | None = None,
    settings: dict[str, Any] | None = None,
    status_update_interval: str | None = None,
    region_name: str | None = None,
) -> UpdateJobTemplateResult:
    """Update job template.

    Args:
        name: Name.
        acceleration_settings: Acceleration settings.
        category: Category.
        description: Description.
        hop_destinations: Hop destinations.
        priority: Priority.
        queue: Queue.
        settings: Settings.
        status_update_interval: Status update interval.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if acceleration_settings is not None:
        kwargs["AccelerationSettings"] = acceleration_settings
    if category is not None:
        kwargs["Category"] = category
    if description is not None:
        kwargs["Description"] = description
    if hop_destinations is not None:
        kwargs["HopDestinations"] = hop_destinations
    if priority is not None:
        kwargs["Priority"] = priority
    if queue is not None:
        kwargs["Queue"] = queue
    if settings is not None:
        kwargs["Settings"] = settings
    if status_update_interval is not None:
        kwargs["StatusUpdateInterval"] = status_update_interval
    try:
        resp = client.update_job_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update job template") from exc
    return UpdateJobTemplateResult(
        job_template=resp.get("JobTemplate"),
    )


def update_preset(
    name: str,
    *,
    category: str | None = None,
    description: str | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdatePresetResult:
    """Update preset.

    Args:
        name: Name.
        category: Category.
        description: Description.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if category is not None:
        kwargs["Category"] = category
    if description is not None:
        kwargs["Description"] = description
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = client.update_preset(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update preset") from exc
    return UpdatePresetResult(
        preset=resp.get("Preset"),
    )


def update_queue(
    name: str,
    *,
    concurrent_jobs: int | None = None,
    description: str | None = None,
    reservation_plan_settings: dict[str, Any] | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> UpdateQueueResult:
    """Update queue.

    Args:
        name: Name.
        concurrent_jobs: Concurrent jobs.
        description: Description.
        reservation_plan_settings: Reservation plan settings.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if concurrent_jobs is not None:
        kwargs["ConcurrentJobs"] = concurrent_jobs
    if description is not None:
        kwargs["Description"] = description
    if reservation_plan_settings is not None:
        kwargs["ReservationPlanSettings"] = reservation_plan_settings
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = client.update_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue") from exc
    return UpdateQueueResult(
        queue=resp.get("Queue"),
    )
