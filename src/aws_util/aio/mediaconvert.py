"""Native async MediaConvert utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error
from aws_util.mediaconvert import (
    CreatePresetResult,
    EndpointResult,
    GetJobsQueryResultsResult,
    GetPolicyResult,
    GetPresetResult,
    JobResult,
    JobTemplateResult,
    ListPresetsResult,
    ListTagsForResourceResult,
    ListVersionsResult,
    ProbeResult,
    PutPolicyResult,
    QueueResult,
    SearchJobsResult,
    StartJobsQueryResult,
    UpdateJobTemplateResult,
    UpdatePresetResult,
    UpdateQueueResult,
    _parse_job,
    _parse_job_template,
    _parse_queue,
)

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
# Job functions
# ---------------------------------------------------------------------------


async def create_job(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {
        "Role": role,
        "Settings": settings,
    }
    if queue is not None:
        kwargs["Queue"] = queue
    if job_template is not None:
        kwargs["JobTemplate"] = job_template
    try:
        resp = await client.call("CreateJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_job failed") from exc
    return _parse_job(resp.get("Job", {}))


async def get_job(
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
    client = async_client("mediaconvert", region_name)
    try:
        resp = await client.call("GetJob", Id=job_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_job failed for {job_id!r}") from exc
    return _parse_job(resp.get("Job", {}))


async def list_jobs(
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
    client = async_client("mediaconvert", region_name)
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
            resp = await client.call("ListJobs", **kwargs)
            for j in resp.get("Jobs", []):
                jobs.append(_parse_job(j))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return jobs


async def cancel_job(
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
    client = async_client("mediaconvert", region_name)
    try:
        await client.call("CancelJob", Id=job_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"cancel_job failed for {job_id!r}") from exc


# ---------------------------------------------------------------------------
# Job template functions
# ---------------------------------------------------------------------------


async def create_job_template(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("CreateJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_job_template failed") from exc
    return _parse_job_template(resp.get("JobTemplate", {}))


async def get_job_template(
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
    client = async_client("mediaconvert", region_name)
    try:
        resp = await client.call("GetJobTemplate", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_job_template failed for {name!r}") from exc
    return _parse_job_template(resp.get("JobTemplate", {}))


async def list_job_templates(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if category is not None:
        kwargs["Category"] = category
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    templates: list[JobTemplateResult] = []
    try:
        while True:
            resp = await client.call("ListJobTemplates", **kwargs)
            for t in resp.get("JobTemplates", []):
                templates.append(_parse_job_template(t))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_job_templates failed") from exc
    return templates


async def delete_job_template(
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
    client = async_client("mediaconvert", region_name)
    try:
        await client.call("DeleteJobTemplate", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_job_template failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Queue functions
# ---------------------------------------------------------------------------


async def create_queue(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {"Name": name}
    if description is not None:
        kwargs["Description"] = description
    if pricing_plan is not None:
        kwargs["PricingPlan"] = pricing_plan
    try:
        resp = await client.call("CreateQueue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_queue failed") from exc
    return _parse_queue(resp.get("Queue", {}))


async def get_queue(
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
    client = async_client("mediaconvert", region_name)
    try:
        resp = await client.call("GetQueue", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_queue failed for {name!r}") from exc
    return _parse_queue(resp.get("Queue", {}))


async def list_queues(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    queues: list[QueueResult] = []
    try:
        while True:
            resp = await client.call("ListQueues", **kwargs)
            for q in resp.get("Queues", []):
                queues.append(_parse_queue(q))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_queues failed") from exc
    return queues


async def delete_queue(
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
    client = async_client("mediaconvert", region_name)
    try:
        await client.call("DeleteQueue", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_queue failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Endpoint functions
# ---------------------------------------------------------------------------


async def describe_endpoints(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    endpoints: list[EndpointResult] = []
    try:
        while True:
            resp = await client.call("DescribeEndpoints", **kwargs)
            for ep in resp.get("Endpoints", []):
                endpoints.append(EndpointResult(url=ep.get("Url", "")))
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_endpoints failed") from exc
    return endpoints


# ---------------------------------------------------------------------------
# Polling / wait utilities
# ---------------------------------------------------------------------------


async def wait_for_job(
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
        result = await get_job(job_id, region_name=region_name)
        if result.status in target_statuses:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Job {job_id!r} did not reach "
                f"{target_statuses!r} within {timeout}s "
                f"(current: {result.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def associate_certificate(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        await client.call("AssociateCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate certificate") from exc
    return None


async def create_preset(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("CreatePreset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create preset") from exc
    return CreatePresetResult(
        preset=resp.get("Preset"),
    )


async def create_resource_share(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    kwargs["SupportCaseId"] = support_case_id
    try:
        await client.call("CreateResourceShare", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create resource share") from exc
    return None


async def delete_policy(
    region_name: str | None = None,
) -> None:
    """Delete policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DeletePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete policy") from exc
    return None


async def delete_preset(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeletePreset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete preset") from exc
    return None


async def disassociate_certificate(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        await client.call("DisassociateCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate certificate") from exc
    return None


async def get_jobs_query_results(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = await client.call("GetJobsQueryResults", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get jobs query results") from exc
    return GetJobsQueryResultsResult(
        jobs=resp.get("Jobs"),
        next_token=resp.get("NextToken"),
        status=resp.get("Status"),
    )


async def get_policy(
    region_name: str | None = None,
) -> GetPolicyResult:
    """Get policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get policy") from exc
    return GetPolicyResult(
        policy=resp.get("Policy"),
    )


async def get_preset(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetPreset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get preset") from exc
    return GetPresetResult(
        preset=resp.get("Preset"),
    )


async def list_presets(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("ListPresets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list presets") from exc
    return ListPresetsResult(
        next_token=resp.get("NextToken"),
        presets=resp.get("Presets"),
    )


async def list_tags_for_resource(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_tags=resp.get("ResourceTags"),
    )


async def list_versions(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list versions") from exc
    return ListVersionsResult(
        next_token=resp.get("NextToken"),
        versions=resp.get("Versions"),
    )


async def probe(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    if input_files is not None:
        kwargs["InputFiles"] = input_files
    try:
        resp = await client.call("Probe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to probe") from exc
    return ProbeResult(
        probe_results=resp.get("ProbeResults"),
    )


async def put_policy(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Policy"] = policy
    try:
        resp = await client.call("PutPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put policy") from exc
    return PutPolicyResult(
        policy=resp.get("Policy"),
    )


async def search_jobs(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("SearchJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search jobs") from exc
    return SearchJobsResult(
        jobs=resp.get("Jobs"),
        next_token=resp.get("NextToken"),
    )


async def start_jobs_query(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("StartJobsQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start jobs query") from exc
    return StartJobsQueryResult(
        id=resp.get("Id"),
    )


async def tag_resource(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_job_template(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("UpdateJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update job template") from exc
    return UpdateJobTemplateResult(
        job_template=resp.get("JobTemplate"),
    )


async def update_preset(
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
    client = async_client("mediaconvert", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if category is not None:
        kwargs["Category"] = category
    if description is not None:
        kwargs["Description"] = description
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = await client.call("UpdatePreset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update preset") from exc
    return UpdatePresetResult(
        preset=resp.get("Preset"),
    )


async def update_queue(
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
    client = async_client("mediaconvert", region_name)
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
        resp = await client.call("UpdateQueue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update queue") from exc
    return UpdateQueueResult(
        queue=resp.get("Queue"),
    )
