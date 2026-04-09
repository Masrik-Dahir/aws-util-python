"""Native async Amazon Personalize utilities using the async engine."""

from __future__ import annotations

import asyncio
import time as _time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error
from aws_util.personalize import (
    CampaignInfo,
    CreateBatchInferenceJobResult,
    CreateBatchSegmentJobResult,
    CreateDataDeletionJobResult,
    CreateDatasetExportJobResult,
    CreateDatasetImportJobResult,
    CreateEventTrackerResult,
    CreateFilterResult,
    CreateMetricAttributionResult,
    CreateRecommenderResult,
    DatasetGroupInfo,
    DatasetInfo,
    DescribeAlgorithmResult,
    DescribeBatchInferenceJobResult,
    DescribeBatchSegmentJobResult,
    DescribeDataDeletionJobResult,
    DescribeDatasetExportJobResult,
    DescribeDatasetImportJobResult,
    DescribeDatasetResult,
    DescribeEventTrackerResult,
    DescribeFeatureTransformationResult,
    DescribeFilterResult,
    DescribeMetricAttributionResult,
    DescribeRecipeResult,
    DescribeRecommenderResult,
    DescribeSchemaResult,
    GetSolutionMetricsResult,
    ListBatchInferenceJobsResult,
    ListBatchSegmentJobsResult,
    ListCampaignsResult,
    ListDataDeletionJobsResult,
    ListDatasetExportJobsResult,
    ListDatasetImportJobsResult,
    ListDatasetsResult,
    ListEventTrackersResult,
    ListFiltersResult,
    ListMetricAttributionMetricsResult,
    ListMetricAttributionsResult,
    ListRecipesResult,
    ListRecommendersResult,
    ListSchemasResult,
    ListSolutionsResult,
    ListSolutionVersionsResult,
    ListTagsForResourceResult,
    SchemaInfo,
    SolutionInfo,
    SolutionVersionInfo,
    StartRecommenderResult,
    StopRecommenderResult,
    UpdateDatasetResult,
    UpdateMetricAttributionResult,
    UpdateRecommenderResult,
    UpdateSolutionResult,
)

__all__ = [
    "CampaignInfo",
    "CreateBatchInferenceJobResult",
    "CreateBatchSegmentJobResult",
    "CreateDataDeletionJobResult",
    "CreateDatasetExportJobResult",
    "CreateDatasetImportJobResult",
    "CreateEventTrackerResult",
    "CreateFilterResult",
    "CreateMetricAttributionResult",
    "CreateRecommenderResult",
    "DatasetGroupInfo",
    "DatasetInfo",
    "DescribeAlgorithmResult",
    "DescribeBatchInferenceJobResult",
    "DescribeBatchSegmentJobResult",
    "DescribeDataDeletionJobResult",
    "DescribeDatasetExportJobResult",
    "DescribeDatasetImportJobResult",
    "DescribeDatasetResult",
    "DescribeEventTrackerResult",
    "DescribeFeatureTransformationResult",
    "DescribeFilterResult",
    "DescribeMetricAttributionResult",
    "DescribeRecipeResult",
    "DescribeRecommenderResult",
    "DescribeSchemaResult",
    "GetSolutionMetricsResult",
    "ListBatchInferenceJobsResult",
    "ListBatchSegmentJobsResult",
    "ListCampaignsResult",
    "ListDataDeletionJobsResult",
    "ListDatasetExportJobsResult",
    "ListDatasetImportJobsResult",
    "ListDatasetsResult",
    "ListEventTrackersResult",
    "ListFiltersResult",
    "ListMetricAttributionMetricsResult",
    "ListMetricAttributionsResult",
    "ListRecipesResult",
    "ListRecommendersResult",
    "ListSchemasResult",
    "ListSolutionVersionsResult",
    "ListSolutionsResult",
    "ListTagsForResourceResult",
    "SchemaInfo",
    "SolutionInfo",
    "SolutionVersionInfo",
    "StartRecommenderResult",
    "StopRecommenderResult",
    "UpdateDatasetResult",
    "UpdateMetricAttributionResult",
    "UpdateRecommenderResult",
    "UpdateSolutionResult",
    "create_batch_inference_job",
    "create_batch_segment_job",
    "create_campaign",
    "create_data_deletion_job",
    "create_dataset",
    "create_dataset_export_job",
    "create_dataset_group",
    "create_dataset_import_job",
    "create_event_tracker",
    "create_filter",
    "create_metric_attribution",
    "create_recommender",
    "create_schema",
    "create_solution",
    "create_solution_version",
    "delete_campaign",
    "delete_dataset",
    "delete_dataset_group",
    "delete_event_tracker",
    "delete_filter",
    "delete_metric_attribution",
    "delete_recommender",
    "delete_schema",
    "delete_solution",
    "describe_algorithm",
    "describe_batch_inference_job",
    "describe_batch_segment_job",
    "describe_campaign",
    "describe_data_deletion_job",
    "describe_dataset",
    "describe_dataset_export_job",
    "describe_dataset_group",
    "describe_dataset_import_job",
    "describe_event_tracker",
    "describe_feature_transformation",
    "describe_filter",
    "describe_metric_attribution",
    "describe_recipe",
    "describe_recommender",
    "describe_schema",
    "describe_solution",
    "describe_solution_version",
    "get_solution_metrics",
    "list_batch_inference_jobs",
    "list_batch_segment_jobs",
    "list_campaigns",
    "list_data_deletion_jobs",
    "list_dataset_export_jobs",
    "list_dataset_groups",
    "list_dataset_import_jobs",
    "list_datasets",
    "list_event_trackers",
    "list_filters",
    "list_metric_attribution_metrics",
    "list_metric_attributions",
    "list_recipes",
    "list_recommenders",
    "list_schemas",
    "list_solution_versions",
    "list_solutions",
    "list_tags_for_resource",
    "start_recommender",
    "stop_recommender",
    "stop_solution_version_creation",
    "tag_resource",
    "untag_resource",
    "update_campaign",
    "update_dataset",
    "update_metric_attribution",
    "update_recommender",
    "update_solution",
    "wait_for_campaign",
    "wait_for_solution_version",
]


# ---------------------------------------------------------------------------
# Dataset groups
# ---------------------------------------------------------------------------


async def create_dataset_group(
    name: str,
    *,
    region_name: str | None = None,
) -> DatasetGroupInfo:
    """Create an Amazon Personalize dataset group.

    Args:
        name: Human-readable name for the dataset group.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetGroupInfo` with the new ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call("CreateDatasetGroup", name=name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_dataset_group failed") from exc
    return DatasetGroupInfo(
        dataset_group_arn=resp.get("datasetGroupArn", ""),
        name=name,
        status="CREATE PENDING",
    )


async def describe_dataset_group(
    dataset_group_arn: str,
    *,
    region_name: str | None = None,
) -> DatasetGroupInfo:
    """Describe an existing dataset group.

    Args:
        dataset_group_arn: ARN of the dataset group.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetGroupInfo` with current status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call(
            "DescribeDatasetGroup",
            datasetGroupArn=dataset_group_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_dataset_group failed") from exc
    dg = resp.get("datasetGroup", {})
    return DatasetGroupInfo(
        dataset_group_arn=dg.get("datasetGroupArn", ""),
        name=dg.get("name", ""),
        status=dg.get("status", ""),
    )


async def list_dataset_groups(
    *,
    max_results: int = 100,
    region_name: str | None = None,
) -> list[DatasetGroupInfo]:
    """List all dataset groups in the account.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`DatasetGroupInfo` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    items: list[DatasetGroupInfo] = []
    kwargs: dict[str, Any] = {"maxResults": max_results}
    try:
        while True:
            resp = await client.call("ListDatasetGroups", **kwargs)
            for dg in resp.get("datasetGroups", []):
                items.append(
                    DatasetGroupInfo(
                        dataset_group_arn=dg.get("datasetGroupArn", ""),
                        name=dg.get("name", ""),
                        status=dg.get("status", ""),
                    )
                )
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_dataset_groups failed") from exc
    return items


# ---------------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------------


async def create_dataset(
    name: str,
    dataset_group_arn: str,
    dataset_type: str,
    schema_arn: str,
    *,
    region_name: str | None = None,
) -> DatasetInfo:
    """Create an Amazon Personalize dataset.

    Args:
        name: Human-readable dataset name.
        dataset_group_arn: ARN of the parent dataset group.
        dataset_type: One of ``"Interactions"``, ``"Items"``, or ``"Users"``.
        schema_arn: ARN of the schema describing the data format.
        region_name: AWS region override.

    Returns:
        A :class:`DatasetInfo` with the new dataset ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call(
            "CreateDataset",
            name=name,
            datasetGroupArn=dataset_group_arn,
            datasetType=dataset_type,
            schemaArn=schema_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_dataset failed") from exc
    return DatasetInfo(
        dataset_arn=resp.get("datasetArn", ""),
        name=name,
        dataset_type=dataset_type,
        status="CREATE PENDING",
    )


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


async def create_schema(
    name: str,
    schema_json: str,
    *,
    region_name: str | None = None,
) -> SchemaInfo:
    """Create an Amazon Personalize schema.

    Args:
        name: Human-readable schema name.
        schema_json: The Avro JSON schema string.
        region_name: AWS region override.

    Returns:
        A :class:`SchemaInfo` with the new schema ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call("CreateSchema", name=name, schema=schema_json)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_schema failed") from exc
    return SchemaInfo(
        schema_arn=resp.get("schemaArn", ""),
        name=name,
    )


# ---------------------------------------------------------------------------
# Solutions
# ---------------------------------------------------------------------------


async def create_solution(
    name: str,
    dataset_group_arn: str,
    recipe_arn: str,
    *,
    region_name: str | None = None,
) -> SolutionInfo:
    """Create an Amazon Personalize solution.

    Args:
        name: Human-readable solution name.
        dataset_group_arn: ARN of the dataset group.
        recipe_arn: ARN of the recipe to use.
        region_name: AWS region override.

    Returns:
        A :class:`SolutionInfo` with the new solution ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call(
            "CreateSolution",
            name=name,
            datasetGroupArn=dataset_group_arn,
            recipeArn=recipe_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_solution failed") from exc
    return SolutionInfo(
        solution_arn=resp.get("solutionArn", ""),
        name=name,
        recipe_arn=recipe_arn,
        status="CREATE PENDING",
    )


async def describe_solution(
    solution_arn: str,
    *,
    region_name: str | None = None,
) -> SolutionInfo:
    """Describe an existing solution.

    Args:
        solution_arn: ARN of the solution.
        region_name: AWS region override.

    Returns:
        A :class:`SolutionInfo` with current metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call("DescribeSolution", solutionArn=solution_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_solution failed") from exc
    sol = resp.get("solution", {})
    return SolutionInfo(
        solution_arn=sol.get("solutionArn", ""),
        name=sol.get("name", ""),
        recipe_arn=sol.get("recipeArn", ""),
        status=sol.get("status", ""),
    )


# ---------------------------------------------------------------------------
# Solution versions
# ---------------------------------------------------------------------------


async def create_solution_version(
    solution_arn: str,
    *,
    region_name: str | None = None,
) -> SolutionVersionInfo:
    """Create a new solution version (model training run).

    Args:
        solution_arn: ARN of the parent solution.
        region_name: AWS region override.

    Returns:
        A :class:`SolutionVersionInfo` with the new version ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call("CreateSolutionVersion", solutionArn=solution_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_solution_version failed") from exc
    return SolutionVersionInfo(
        solution_version_arn=resp.get("solutionVersionArn", ""),
        status="CREATE PENDING",
    )


async def describe_solution_version(
    solution_version_arn: str,
    *,
    region_name: str | None = None,
) -> SolutionVersionInfo:
    """Describe an existing solution version.

    Args:
        solution_version_arn: ARN of the solution version.
        region_name: AWS region override.

    Returns:
        A :class:`SolutionVersionInfo` with current status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call(
            "DescribeSolutionVersion",
            solutionVersionArn=solution_version_arn,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_solution_version failed") from exc
    sv = resp.get("solutionVersion", {})
    return SolutionVersionInfo(
        solution_version_arn=sv.get("solutionVersionArn", ""),
        status=sv.get("status", ""),
        failure_reason=sv.get("failureReason", ""),
    )


async def wait_for_solution_version(
    solution_version_arn: str,
    *,
    timeout: float = 3600.0,
    poll_interval: float = 60.0,
    region_name: str | None = None,
) -> SolutionVersionInfo:
    """Poll until a solution version reaches ACTIVE or a failure state.

    Args:
        solution_version_arn: ARN of the solution version to monitor.
        timeout: Maximum seconds to wait (default ``3600``).
        poll_interval: Seconds between polls (default ``60``).
        region_name: AWS region override.

    Returns:
        The :class:`SolutionVersionInfo` in ``ACTIVE`` status.

    Raises:
        AwsTimeoutError: If the version does not become ACTIVE in time.
        AwsServiceError: If the version enters a failure state.
    """
    deadline = _time.monotonic() + timeout
    while True:
        sv = await describe_solution_version(solution_version_arn, region_name=region_name)
        if sv.status == "ACTIVE":
            return sv
        if sv.status.startswith("CREATE FAILED"):
            raise AwsServiceError(f"Solution version failed: {sv.failure_reason}")
        if _time.monotonic() + poll_interval > deadline:
            raise AwsTimeoutError(
                f"Solution version {solution_version_arn} did not become "
                f"ACTIVE within {timeout}s (last status: {sv.status})"
            )
        await asyncio.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------


async def create_campaign(
    name: str,
    solution_version_arn: str,
    *,
    min_provisioned_tps: int = 1,
    region_name: str | None = None,
) -> CampaignInfo:
    """Create an Amazon Personalize campaign for real-time recommendations.

    Args:
        name: Human-readable campaign name.
        solution_version_arn: ARN of the trained solution version.
        min_provisioned_tps: Minimum provisioned transactions per second.
        region_name: AWS region override.

    Returns:
        A :class:`CampaignInfo` with the new campaign ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call(
            "CreateCampaign",
            name=name,
            solutionVersionArn=solution_version_arn,
            minProvisionedTPS=min_provisioned_tps,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "create_campaign failed") from exc
    return CampaignInfo(
        campaign_arn=resp.get("campaignArn", ""),
        name=name,
        solution_version_arn=solution_version_arn,
        min_provisioned_tps=min_provisioned_tps,
        status="CREATE PENDING",
    )


async def describe_campaign(
    campaign_arn: str,
    *,
    region_name: str | None = None,
) -> CampaignInfo:
    """Describe an existing campaign.

    Args:
        campaign_arn: ARN of the campaign.
        region_name: AWS region override.

    Returns:
        A :class:`CampaignInfo` with current status.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        resp = await client.call("DescribeCampaign", campaignArn=campaign_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "describe_campaign failed") from exc
    camp = resp.get("campaign", {})
    return CampaignInfo(
        campaign_arn=camp.get("campaignArn", ""),
        name=camp.get("name", ""),
        solution_version_arn=camp.get("solutionVersionArn", ""),
        min_provisioned_tps=camp.get("minProvisionedTPS", 1),
        status=camp.get("status", ""),
    )


async def update_campaign(
    campaign_arn: str,
    *,
    solution_version_arn: str | None = None,
    min_provisioned_tps: int | None = None,
    region_name: str | None = None,
) -> CampaignInfo:
    """Update an existing campaign.

    Args:
        campaign_arn: ARN of the campaign to update.
        solution_version_arn: New solution version ARN (optional).
        min_provisioned_tps: New minimum TPS (optional).
        region_name: AWS region override.

    Returns:
        A :class:`CampaignInfo` reflecting the update request.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {"campaignArn": campaign_arn}
    if solution_version_arn is not None:
        kwargs["solutionVersionArn"] = solution_version_arn
    if min_provisioned_tps is not None:
        kwargs["minProvisionedTPS"] = min_provisioned_tps
    try:
        resp = await client.call("UpdateCampaign", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "update_campaign failed") from exc
    return CampaignInfo(
        campaign_arn=resp.get("campaignArn", campaign_arn),
        status="UPDATE PENDING",
    )


async def delete_campaign(
    campaign_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an Amazon Personalize campaign.

    Args:
        campaign_arn: ARN of the campaign to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    try:
        await client.call("DeleteCampaign", campaignArn=campaign_arn)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "delete_campaign failed") from exc


async def wait_for_campaign(
    campaign_arn: str,
    *,
    timeout: float = 1200.0,
    poll_interval: float = 30.0,
    region_name: str | None = None,
) -> CampaignInfo:
    """Poll until a campaign reaches ACTIVE or a failure state.

    Args:
        campaign_arn: ARN of the campaign to monitor.
        timeout: Maximum seconds to wait (default ``1200``).
        poll_interval: Seconds between polls (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`CampaignInfo` in ``ACTIVE`` status.

    Raises:
        AwsTimeoutError: If the campaign does not become ACTIVE in time.
        AwsServiceError: If the campaign enters a failure state.
    """
    deadline = _time.monotonic() + timeout
    while True:
        camp = await describe_campaign(campaign_arn, region_name=region_name)
        if camp.status == "ACTIVE":
            return camp
        if "FAILED" in camp.status:
            raise AwsServiceError(f"Campaign {campaign_arn} failed (status: {camp.status})")
        if _time.monotonic() + poll_interval > deadline:
            raise AwsTimeoutError(
                f"Campaign {campaign_arn} did not become ACTIVE within "
                f"{timeout}s (last status: {camp.status})"
            )
        await asyncio.sleep(poll_interval)


async def create_batch_inference_job(
    job_name: str,
    solution_version_arn: str,
    job_input: dict[str, Any],
    job_output: dict[str, Any],
    role_arn: str,
    *,
    filter_arn: str | None = None,
    num_results: int | None = None,
    batch_inference_job_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    batch_inference_job_mode: str | None = None,
    theme_generation_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateBatchInferenceJobResult:
    """Create batch inference job.

    Args:
        job_name: Job name.
        solution_version_arn: Solution version arn.
        job_input: Job input.
        job_output: Job output.
        role_arn: Role arn.
        filter_arn: Filter arn.
        num_results: Num results.
        batch_inference_job_config: Batch inference job config.
        tags: Tags.
        batch_inference_job_mode: Batch inference job mode.
        theme_generation_config: Theme generation config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["solutionVersionArn"] = solution_version_arn
    kwargs["jobInput"] = job_input
    kwargs["jobOutput"] = job_output
    kwargs["roleArn"] = role_arn
    if filter_arn is not None:
        kwargs["filterArn"] = filter_arn
    if num_results is not None:
        kwargs["numResults"] = num_results
    if batch_inference_job_config is not None:
        kwargs["batchInferenceJobConfig"] = batch_inference_job_config
    if tags is not None:
        kwargs["tags"] = tags
    if batch_inference_job_mode is not None:
        kwargs["batchInferenceJobMode"] = batch_inference_job_mode
    if theme_generation_config is not None:
        kwargs["themeGenerationConfig"] = theme_generation_config
    try:
        resp = await client.call("CreateBatchInferenceJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create batch inference job") from exc
    return CreateBatchInferenceJobResult(
        batch_inference_job_arn=resp.get("batchInferenceJobArn"),
    )


async def create_batch_segment_job(
    job_name: str,
    solution_version_arn: str,
    job_input: dict[str, Any],
    job_output: dict[str, Any],
    role_arn: str,
    *,
    filter_arn: str | None = None,
    num_results: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateBatchSegmentJobResult:
    """Create batch segment job.

    Args:
        job_name: Job name.
        solution_version_arn: Solution version arn.
        job_input: Job input.
        job_output: Job output.
        role_arn: Role arn.
        filter_arn: Filter arn.
        num_results: Num results.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["solutionVersionArn"] = solution_version_arn
    kwargs["jobInput"] = job_input
    kwargs["jobOutput"] = job_output
    kwargs["roleArn"] = role_arn
    if filter_arn is not None:
        kwargs["filterArn"] = filter_arn
    if num_results is not None:
        kwargs["numResults"] = num_results
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateBatchSegmentJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create batch segment job") from exc
    return CreateBatchSegmentJobResult(
        batch_segment_job_arn=resp.get("batchSegmentJobArn"),
    )


async def create_data_deletion_job(
    job_name: str,
    dataset_group_arn: str,
    data_source: dict[str, Any],
    role_arn: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDataDeletionJobResult:
    """Create data deletion job.

    Args:
        job_name: Job name.
        dataset_group_arn: Dataset group arn.
        data_source: Data source.
        role_arn: Role arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["datasetGroupArn"] = dataset_group_arn
    kwargs["dataSource"] = data_source
    kwargs["roleArn"] = role_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDataDeletionJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data deletion job") from exc
    return CreateDataDeletionJobResult(
        data_deletion_job_arn=resp.get("dataDeletionJobArn"),
    )


async def create_dataset_export_job(
    job_name: str,
    dataset_arn: str,
    role_arn: str,
    job_output: dict[str, Any],
    *,
    ingestion_mode: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDatasetExportJobResult:
    """Create dataset export job.

    Args:
        job_name: Job name.
        dataset_arn: Dataset arn.
        role_arn: Role arn.
        job_output: Job output.
        ingestion_mode: Ingestion mode.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["datasetArn"] = dataset_arn
    kwargs["roleArn"] = role_arn
    kwargs["jobOutput"] = job_output
    if ingestion_mode is not None:
        kwargs["ingestionMode"] = ingestion_mode
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDatasetExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dataset export job") from exc
    return CreateDatasetExportJobResult(
        dataset_export_job_arn=resp.get("datasetExportJobArn"),
    )


async def create_dataset_import_job(
    job_name: str,
    dataset_arn: str,
    data_source: dict[str, Any],
    role_arn: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    import_mode: str | None = None,
    publish_attribution_metrics_to_s3: bool | None = None,
    region_name: str | None = None,
) -> CreateDatasetImportJobResult:
    """Create dataset import job.

    Args:
        job_name: Job name.
        dataset_arn: Dataset arn.
        data_source: Data source.
        role_arn: Role arn.
        tags: Tags.
        import_mode: Import mode.
        publish_attribution_metrics_to_s3: Publish attribution metrics to s3.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["datasetArn"] = dataset_arn
    kwargs["dataSource"] = data_source
    kwargs["roleArn"] = role_arn
    if tags is not None:
        kwargs["tags"] = tags
    if import_mode is not None:
        kwargs["importMode"] = import_mode
    if publish_attribution_metrics_to_s3 is not None:
        kwargs["publishAttributionMetricsToS3"] = publish_attribution_metrics_to_s3
    try:
        resp = await client.call("CreateDatasetImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dataset import job") from exc
    return CreateDatasetImportJobResult(
        dataset_import_job_arn=resp.get("datasetImportJobArn"),
    )


async def create_event_tracker(
    name: str,
    dataset_group_arn: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateEventTrackerResult:
    """Create event tracker.

    Args:
        name: Name.
        dataset_group_arn: Dataset group arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["datasetGroupArn"] = dataset_group_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateEventTracker", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create event tracker") from exc
    return CreateEventTrackerResult(
        event_tracker_arn=resp.get("eventTrackerArn"),
        tracking_id=resp.get("trackingId"),
    )


async def create_filter(
    name: str,
    dataset_group_arn: str,
    filter_expression: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateFilterResult:
    """Create filter.

    Args:
        name: Name.
        dataset_group_arn: Dataset group arn.
        filter_expression: Filter expression.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["datasetGroupArn"] = dataset_group_arn
    kwargs["filterExpression"] = filter_expression
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create filter") from exc
    return CreateFilterResult(
        filter_arn=resp.get("filterArn"),
    )


async def create_metric_attribution(
    name: str,
    dataset_group_arn: str,
    metrics: list[dict[str, Any]],
    metrics_output_config: dict[str, Any],
    region_name: str | None = None,
) -> CreateMetricAttributionResult:
    """Create metric attribution.

    Args:
        name: Name.
        dataset_group_arn: Dataset group arn.
        metrics: Metrics.
        metrics_output_config: Metrics output config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["datasetGroupArn"] = dataset_group_arn
    kwargs["metrics"] = metrics
    kwargs["metricsOutputConfig"] = metrics_output_config
    try:
        resp = await client.call("CreateMetricAttribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create metric attribution") from exc
    return CreateMetricAttributionResult(
        metric_attribution_arn=resp.get("metricAttributionArn"),
    )


async def create_recommender(
    name: str,
    dataset_group_arn: str,
    recipe_arn: str,
    *,
    recommender_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRecommenderResult:
    """Create recommender.

    Args:
        name: Name.
        dataset_group_arn: Dataset group arn.
        recipe_arn: Recipe arn.
        recommender_config: Recommender config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["datasetGroupArn"] = dataset_group_arn
    kwargs["recipeArn"] = recipe_arn
    if recommender_config is not None:
        kwargs["recommenderConfig"] = recommender_config
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create recommender") from exc
    return CreateRecommenderResult(
        recommender_arn=resp.get("recommenderArn"),
    )


async def delete_dataset(
    dataset_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset.

    Args:
        dataset_arn: Dataset arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetArn"] = dataset_arn
    try:
        await client.call("DeleteDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset") from exc
    return None


async def delete_dataset_group(
    dataset_group_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete dataset group.

    Args:
        dataset_group_arn: Dataset group arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetGroupArn"] = dataset_group_arn
    try:
        await client.call("DeleteDatasetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset group") from exc
    return None


async def delete_event_tracker(
    event_tracker_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete event tracker.

    Args:
        event_tracker_arn: Event tracker arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["eventTrackerArn"] = event_tracker_arn
    try:
        await client.call("DeleteEventTracker", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete event tracker") from exc
    return None


async def delete_filter(
    filter_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete filter.

    Args:
        filter_arn: Filter arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["filterArn"] = filter_arn
    try:
        await client.call("DeleteFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete filter") from exc
    return None


async def delete_metric_attribution(
    metric_attribution_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete metric attribution.

    Args:
        metric_attribution_arn: Metric attribution arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricAttributionArn"] = metric_attribution_arn
    try:
        await client.call("DeleteMetricAttribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete metric attribution") from exc
    return None


async def delete_recommender(
    recommender_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete recommender.

    Args:
        recommender_arn: Recommender arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recommenderArn"] = recommender_arn
    try:
        await client.call("DeleteRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete recommender") from exc
    return None


async def delete_schema(
    schema_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete schema.

    Args:
        schema_arn: Schema arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["schemaArn"] = schema_arn
    try:
        await client.call("DeleteSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete schema") from exc
    return None


async def delete_solution(
    solution_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete solution.

    Args:
        solution_arn: Solution arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["solutionArn"] = solution_arn
    try:
        await client.call("DeleteSolution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete solution") from exc
    return None


async def describe_algorithm(
    algorithm_arn: str,
    region_name: str | None = None,
) -> DescribeAlgorithmResult:
    """Describe algorithm.

    Args:
        algorithm_arn: Algorithm arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["algorithmArn"] = algorithm_arn
    try:
        resp = await client.call("DescribeAlgorithm", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe algorithm") from exc
    return DescribeAlgorithmResult(
        algorithm=resp.get("algorithm"),
    )


async def describe_batch_inference_job(
    batch_inference_job_arn: str,
    region_name: str | None = None,
) -> DescribeBatchInferenceJobResult:
    """Describe batch inference job.

    Args:
        batch_inference_job_arn: Batch inference job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["batchInferenceJobArn"] = batch_inference_job_arn
    try:
        resp = await client.call("DescribeBatchInferenceJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe batch inference job") from exc
    return DescribeBatchInferenceJobResult(
        batch_inference_job=resp.get("batchInferenceJob"),
    )


async def describe_batch_segment_job(
    batch_segment_job_arn: str,
    region_name: str | None = None,
) -> DescribeBatchSegmentJobResult:
    """Describe batch segment job.

    Args:
        batch_segment_job_arn: Batch segment job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["batchSegmentJobArn"] = batch_segment_job_arn
    try:
        resp = await client.call("DescribeBatchSegmentJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe batch segment job") from exc
    return DescribeBatchSegmentJobResult(
        batch_segment_job=resp.get("batchSegmentJob"),
    )


async def describe_data_deletion_job(
    data_deletion_job_arn: str,
    region_name: str | None = None,
) -> DescribeDataDeletionJobResult:
    """Describe data deletion job.

    Args:
        data_deletion_job_arn: Data deletion job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dataDeletionJobArn"] = data_deletion_job_arn
    try:
        resp = await client.call("DescribeDataDeletionJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data deletion job") from exc
    return DescribeDataDeletionJobResult(
        data_deletion_job=resp.get("dataDeletionJob"),
    )


async def describe_dataset(
    dataset_arn: str,
    region_name: str | None = None,
) -> DescribeDatasetResult:
    """Describe dataset.

    Args:
        dataset_arn: Dataset arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetArn"] = dataset_arn
    try:
        resp = await client.call("DescribeDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset") from exc
    return DescribeDatasetResult(
        dataset=resp.get("dataset"),
    )


async def describe_dataset_export_job(
    dataset_export_job_arn: str,
    region_name: str | None = None,
) -> DescribeDatasetExportJobResult:
    """Describe dataset export job.

    Args:
        dataset_export_job_arn: Dataset export job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetExportJobArn"] = dataset_export_job_arn
    try:
        resp = await client.call("DescribeDatasetExportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset export job") from exc
    return DescribeDatasetExportJobResult(
        dataset_export_job=resp.get("datasetExportJob"),
    )


async def describe_dataset_import_job(
    dataset_import_job_arn: str,
    region_name: str | None = None,
) -> DescribeDatasetImportJobResult:
    """Describe dataset import job.

    Args:
        dataset_import_job_arn: Dataset import job arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetImportJobArn"] = dataset_import_job_arn
    try:
        resp = await client.call("DescribeDatasetImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset import job") from exc
    return DescribeDatasetImportJobResult(
        dataset_import_job=resp.get("datasetImportJob"),
    )


async def describe_event_tracker(
    event_tracker_arn: str,
    region_name: str | None = None,
) -> DescribeEventTrackerResult:
    """Describe event tracker.

    Args:
        event_tracker_arn: Event tracker arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["eventTrackerArn"] = event_tracker_arn
    try:
        resp = await client.call("DescribeEventTracker", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event tracker") from exc
    return DescribeEventTrackerResult(
        event_tracker=resp.get("eventTracker"),
    )


async def describe_feature_transformation(
    feature_transformation_arn: str,
    region_name: str | None = None,
) -> DescribeFeatureTransformationResult:
    """Describe feature transformation.

    Args:
        feature_transformation_arn: Feature transformation arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["featureTransformationArn"] = feature_transformation_arn
    try:
        resp = await client.call("DescribeFeatureTransformation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe feature transformation") from exc
    return DescribeFeatureTransformationResult(
        feature_transformation=resp.get("featureTransformation"),
    )


async def describe_filter(
    filter_arn: str,
    region_name: str | None = None,
) -> DescribeFilterResult:
    """Describe filter.

    Args:
        filter_arn: Filter arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["filterArn"] = filter_arn
    try:
        resp = await client.call("DescribeFilter", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe filter") from exc
    return DescribeFilterResult(
        filter=resp.get("filter"),
    )


async def describe_metric_attribution(
    metric_attribution_arn: str,
    region_name: str | None = None,
) -> DescribeMetricAttributionResult:
    """Describe metric attribution.

    Args:
        metric_attribution_arn: Metric attribution arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricAttributionArn"] = metric_attribution_arn
    try:
        resp = await client.call("DescribeMetricAttribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metric attribution") from exc
    return DescribeMetricAttributionResult(
        metric_attribution=resp.get("metricAttribution"),
    )


async def describe_recipe(
    recipe_arn: str,
    region_name: str | None = None,
) -> DescribeRecipeResult:
    """Describe recipe.

    Args:
        recipe_arn: Recipe arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recipeArn"] = recipe_arn
    try:
        resp = await client.call("DescribeRecipe", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe recipe") from exc
    return DescribeRecipeResult(
        recipe=resp.get("recipe"),
    )


async def describe_recommender(
    recommender_arn: str,
    region_name: str | None = None,
) -> DescribeRecommenderResult:
    """Describe recommender.

    Args:
        recommender_arn: Recommender arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recommenderArn"] = recommender_arn
    try:
        resp = await client.call("DescribeRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe recommender") from exc
    return DescribeRecommenderResult(
        recommender=resp.get("recommender"),
    )


async def describe_schema(
    schema_arn: str,
    region_name: str | None = None,
) -> DescribeSchemaResult:
    """Describe schema.

    Args:
        schema_arn: Schema arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["schemaArn"] = schema_arn
    try:
        resp = await client.call("DescribeSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe schema") from exc
    return DescribeSchemaResult(
        model_schema=resp.get("schema"),
    )


async def get_solution_metrics(
    solution_version_arn: str,
    region_name: str | None = None,
) -> GetSolutionMetricsResult:
    """Get solution metrics.

    Args:
        solution_version_arn: Solution version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["solutionVersionArn"] = solution_version_arn
    try:
        resp = await client.call("GetSolutionMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get solution metrics") from exc
    return GetSolutionMetricsResult(
        solution_version_arn=resp.get("solutionVersionArn"),
        metrics=resp.get("metrics"),
    )


async def list_batch_inference_jobs(
    *,
    solution_version_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListBatchInferenceJobsResult:
    """List batch inference jobs.

    Args:
        solution_version_arn: Solution version arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if solution_version_arn is not None:
        kwargs["solutionVersionArn"] = solution_version_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListBatchInferenceJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list batch inference jobs") from exc
    return ListBatchInferenceJobsResult(
        batch_inference_jobs=resp.get("batchInferenceJobs"),
        next_token=resp.get("nextToken"),
    )


async def list_batch_segment_jobs(
    *,
    solution_version_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListBatchSegmentJobsResult:
    """List batch segment jobs.

    Args:
        solution_version_arn: Solution version arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if solution_version_arn is not None:
        kwargs["solutionVersionArn"] = solution_version_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListBatchSegmentJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list batch segment jobs") from exc
    return ListBatchSegmentJobsResult(
        batch_segment_jobs=resp.get("batchSegmentJobs"),
        next_token=resp.get("nextToken"),
    )


async def list_campaigns(
    *,
    solution_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCampaignsResult:
    """List campaigns.

    Args:
        solution_arn: Solution arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if solution_arn is not None:
        kwargs["solutionArn"] = solution_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCampaigns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list campaigns") from exc
    return ListCampaignsResult(
        campaigns=resp.get("campaigns"),
        next_token=resp.get("nextToken"),
    )


async def list_data_deletion_jobs(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDataDeletionJobsResult:
    """List data deletion jobs.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDataDeletionJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data deletion jobs") from exc
    return ListDataDeletionJobsResult(
        data_deletion_jobs=resp.get("dataDeletionJobs"),
        next_token=resp.get("nextToken"),
    )


async def list_dataset_export_jobs(
    *,
    dataset_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetExportJobsResult:
    """List dataset export jobs.

    Args:
        dataset_arn: Dataset arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_arn is not None:
        kwargs["datasetArn"] = dataset_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDatasetExportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dataset export jobs") from exc
    return ListDatasetExportJobsResult(
        dataset_export_jobs=resp.get("datasetExportJobs"),
        next_token=resp.get("nextToken"),
    )


async def list_dataset_import_jobs(
    *,
    dataset_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetImportJobsResult:
    """List dataset import jobs.

    Args:
        dataset_arn: Dataset arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_arn is not None:
        kwargs["datasetArn"] = dataset_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDatasetImportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dataset import jobs") from exc
    return ListDatasetImportJobsResult(
        dataset_import_jobs=resp.get("datasetImportJobs"),
        next_token=resp.get("nextToken"),
    )


async def list_datasets(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetsResult:
    """List datasets.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDatasets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list datasets") from exc
    return ListDatasetsResult(
        datasets=resp.get("datasets"),
        next_token=resp.get("nextToken"),
    )


async def list_event_trackers(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEventTrackersResult:
    """List event trackers.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListEventTrackers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list event trackers") from exc
    return ListEventTrackersResult(
        event_trackers=resp.get("eventTrackers"),
        next_token=resp.get("nextToken"),
    )


async def list_filters(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFiltersResult:
    """List filters.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListFilters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list filters") from exc
    return ListFiltersResult(
        filters=resp.get("Filters"),
        next_token=resp.get("nextToken"),
    )


async def list_metric_attribution_metrics(
    *,
    metric_attribution_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMetricAttributionMetricsResult:
    """List metric attribution metrics.

    Args:
        metric_attribution_arn: Metric attribution arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if metric_attribution_arn is not None:
        kwargs["metricAttributionArn"] = metric_attribution_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListMetricAttributionMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list metric attribution metrics") from exc
    return ListMetricAttributionMetricsResult(
        metrics=resp.get("metrics"),
        next_token=resp.get("nextToken"),
    )


async def list_metric_attributions(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMetricAttributionsResult:
    """List metric attributions.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListMetricAttributions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list metric attributions") from exc
    return ListMetricAttributionsResult(
        metric_attributions=resp.get("metricAttributions"),
        next_token=resp.get("nextToken"),
    )


async def list_recipes(
    *,
    recipe_provider: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    domain: str | None = None,
    region_name: str | None = None,
) -> ListRecipesResult:
    """List recipes.

    Args:
        recipe_provider: Recipe provider.
        next_token: Next token.
        max_results: Max results.
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if recipe_provider is not None:
        kwargs["recipeProvider"] = recipe_provider
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if domain is not None:
        kwargs["domain"] = domain
    try:
        resp = await client.call("ListRecipes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recipes") from exc
    return ListRecipesResult(
        recipes=resp.get("recipes"),
        next_token=resp.get("nextToken"),
    )


async def list_recommenders(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRecommendersResult:
    """List recommenders.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListRecommenders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recommenders") from exc
    return ListRecommendersResult(
        recommenders=resp.get("recommenders"),
        next_token=resp.get("nextToken"),
    )


async def list_schemas(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSchemasResult:
    """List schemas.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list schemas") from exc
    return ListSchemasResult(
        schemas=resp.get("schemas"),
        next_token=resp.get("nextToken"),
    )


async def list_solution_versions(
    *,
    solution_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSolutionVersionsResult:
    """List solution versions.

    Args:
        solution_arn: Solution arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if solution_arn is not None:
        kwargs["solutionArn"] = solution_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListSolutionVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list solution versions") from exc
    return ListSolutionVersionsResult(
        solution_versions=resp.get("solutionVersions"),
        next_token=resp.get("nextToken"),
    )


async def list_solutions(
    *,
    dataset_group_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSolutionsResult:
    """List solutions.

    Args:
        dataset_group_arn: Dataset group arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if dataset_group_arn is not None:
        kwargs["datasetGroupArn"] = dataset_group_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListSolutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list solutions") from exc
    return ListSolutionsResult(
        solutions=resp.get("solutions"),
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
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def start_recommender(
    recommender_arn: str,
    region_name: str | None = None,
) -> StartRecommenderResult:
    """Start recommender.

    Args:
        recommender_arn: Recommender arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recommenderArn"] = recommender_arn
    try:
        resp = await client.call("StartRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start recommender") from exc
    return StartRecommenderResult(
        recommender_arn=resp.get("recommenderArn"),
    )


async def stop_recommender(
    recommender_arn: str,
    region_name: str | None = None,
) -> StopRecommenderResult:
    """Stop recommender.

    Args:
        recommender_arn: Recommender arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recommenderArn"] = recommender_arn
    try:
        resp = await client.call("StopRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop recommender") from exc
    return StopRecommenderResult(
        recommender_arn=resp.get("recommenderArn"),
    )


async def stop_solution_version_creation(
    solution_version_arn: str,
    region_name: str | None = None,
) -> None:
    """Stop solution version creation.

    Args:
        solution_version_arn: Solution version arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["solutionVersionArn"] = solution_version_arn
    try:
        await client.call("StopSolutionVersionCreation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop solution version creation") from exc
    return None


async def tag_resource(
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
    client = async_client("personalize", region_name)
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
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_dataset(
    dataset_arn: str,
    schema_arn: str,
    region_name: str | None = None,
) -> UpdateDatasetResult:
    """Update dataset.

    Args:
        dataset_arn: Dataset arn.
        schema_arn: Schema arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetArn"] = dataset_arn
    kwargs["schemaArn"] = schema_arn
    try:
        resp = await client.call("UpdateDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dataset") from exc
    return UpdateDatasetResult(
        dataset_arn=resp.get("datasetArn"),
    )


async def update_metric_attribution(
    *,
    add_metrics: list[dict[str, Any]] | None = None,
    remove_metrics: list[str] | None = None,
    metrics_output_config: dict[str, Any] | None = None,
    metric_attribution_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateMetricAttributionResult:
    """Update metric attribution.

    Args:
        add_metrics: Add metrics.
        remove_metrics: Remove metrics.
        metrics_output_config: Metrics output config.
        metric_attribution_arn: Metric attribution arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    if add_metrics is not None:
        kwargs["addMetrics"] = add_metrics
    if remove_metrics is not None:
        kwargs["removeMetrics"] = remove_metrics
    if metrics_output_config is not None:
        kwargs["metricsOutputConfig"] = metrics_output_config
    if metric_attribution_arn is not None:
        kwargs["metricAttributionArn"] = metric_attribution_arn
    try:
        resp = await client.call("UpdateMetricAttribution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update metric attribution") from exc
    return UpdateMetricAttributionResult(
        metric_attribution_arn=resp.get("metricAttributionArn"),
    )


async def update_recommender(
    recommender_arn: str,
    recommender_config: dict[str, Any],
    region_name: str | None = None,
) -> UpdateRecommenderResult:
    """Update recommender.

    Args:
        recommender_arn: Recommender arn.
        recommender_config: Recommender config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recommenderArn"] = recommender_arn
    kwargs["recommenderConfig"] = recommender_config
    try:
        resp = await client.call("UpdateRecommender", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update recommender") from exc
    return UpdateRecommenderResult(
        recommender_arn=resp.get("recommenderArn"),
    )


async def update_solution(
    solution_arn: str,
    *,
    perform_auto_training: bool | None = None,
    solution_update_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateSolutionResult:
    """Update solution.

    Args:
        solution_arn: Solution arn.
        perform_auto_training: Perform auto training.
        solution_update_config: Solution update config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("personalize", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["solutionArn"] = solution_arn
    if perform_auto_training is not None:
        kwargs["performAutoTraining"] = perform_auto_training
    if solution_update_config is not None:
        kwargs["solutionUpdateConfig"] = solution_update_config
    try:
        resp = await client.call("UpdateSolution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update solution") from exc
    return UpdateSolutionResult(
        solution_arn=resp.get("solutionArn"),
    )
