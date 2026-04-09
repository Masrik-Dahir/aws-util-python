"""Native async Glue utilities using the async engine."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.glue import (
    BatchCreatePartitionResult,
    BatchDeleteConnectionResult,
    BatchDeletePartitionResult,
    BatchDeleteTableResult,
    BatchDeleteTableVersionResult,
    BatchGetBlueprintsResult,
    BatchGetCrawlersResult,
    BatchGetCustomEntityTypesResult,
    BatchGetDataQualityResultResult,
    BatchGetDevEndpointsResult,
    BatchGetJobsResult,
    BatchGetPartitionResult,
    BatchGetTableOptimizerResult,
    BatchGetTriggersResult,
    BatchGetWorkflowsResult,
    BatchPutDataQualityStatisticAnnotationResult,
    BatchStopJobRunResult,
    BatchUpdatePartitionResult,
    CancelMlTaskRunResult,
    CheckSchemaVersionValidityResult,
    CreateBlueprintResult,
    CreateConnectionResult,
    CreateCustomEntityTypeResult,
    CreateDataQualityRulesetResult,
    CreateDevEndpointResult,
    CreateGlueIdentityCenterConfigurationResult,
    CreateIntegrationResourcePropertyResult,
    CreateIntegrationResult,
    CreateJobResult,
    CreateMlTransformResult,
    CreateRegistryResult,
    CreateSchemaResult,
    CreateScriptResult,
    CreateSecurityConfigurationResult,
    CreateSessionResult,
    CreateTriggerResult,
    CreateUsageProfileResult,
    CreateWorkflowResult,
    DeleteBlueprintResult,
    DeleteCustomEntityTypeResult,
    DeleteIntegrationResult,
    DeleteJobResult,
    DeleteMlTransformResult,
    DeleteRegistryResult,
    DeleteSchemaResult,
    DeleteSchemaVersionsResult,
    DeleteSessionResult,
    DeleteTriggerResult,
    DeleteWorkflowResult,
    DescribeConnectionTypeResult,
    DescribeEntityResult,
    DescribeInboundIntegrationsResult,
    DescribeIntegrationsResult,
    GetBlueprintResult,
    GetBlueprintRunResult,
    GetBlueprintRunsResult,
    GetCatalogImportStatusResult,
    GetCatalogResult,
    GetCatalogsResult,
    GetClassifierResult,
    GetClassifiersResult,
    GetColumnStatisticsForPartitionResult,
    GetColumnStatisticsForTableResult,
    GetColumnStatisticsTaskRunResult,
    GetColumnStatisticsTaskRunsResult,
    GetColumnStatisticsTaskSettingsResult,
    GetConnectionResult,
    GetConnectionsResult,
    GetCrawlerMetricsResult,
    GetCrawlerResult,
    GetCrawlersResult,
    GetCustomEntityTypeResult,
    GetDatabaseResult,
    GetDatabasesResult,
    GetDataCatalogEncryptionSettingsResult,
    GetDataflowGraphResult,
    GetDataQualityModelResult,
    GetDataQualityModelResultResult,
    GetDataQualityResultResult,
    GetDataQualityRuleRecommendationRunResult,
    GetDataQualityRulesetEvaluationRunResult,
    GetDataQualityRulesetResult,
    GetDevEndpointResult,
    GetDevEndpointsResult,
    GetEntityRecordsResult,
    GetGlueIdentityCenterConfigurationResult,
    GetIntegrationResourcePropertyResult,
    GetIntegrationTablePropertiesResult,
    GetJobBookmarkResult,
    GetJobRunsResult,
    GetJobsResult,
    GetMappingResult,
    GetMlTaskRunResult,
    GetMlTaskRunsResult,
    GetMlTransformResult,
    GetMlTransformsResult,
    GetPartitionIndexesResult,
    GetPartitionResult,
    GetPartitionsResult,
    GetPlanResult,
    GetRegistryResult,
    GetResourcePoliciesResult,
    GetResourcePolicyResult,
    GetSchemaByDefinitionResult,
    GetSchemaResult,
    GetSchemaVersionResult,
    GetSchemaVersionsDiffResult,
    GetSecurityConfigurationResult,
    GetSecurityConfigurationsResult,
    GetSessionResult,
    GetStatementResult,
    GetTableOptimizerResult,
    GetTableResult,
    GetTablesResult,
    GetTableVersionResult,
    GetTableVersionsResult,
    GetTagsResult,
    GetTriggerResult,
    GetTriggersResult,
    GetUnfilteredPartitionMetadataResult,
    GetUnfilteredPartitionsMetadataResult,
    GetUnfilteredTableMetadataResult,
    GetUsageProfileResult,
    GetUserDefinedFunctionResult,
    GetUserDefinedFunctionsResult,
    GetWorkflowResult,
    GetWorkflowRunPropertiesResult,
    GetWorkflowRunResult,
    GetWorkflowRunsResult,
    GlueJob,
    GlueJobRun,
    ListBlueprintsResult,
    ListColumnStatisticsTaskRunsResult,
    ListConnectionTypesResult,
    ListCrawlersResult,
    ListCrawlsResult,
    ListCustomEntityTypesResult,
    ListDataQualityResultsResult,
    ListDataQualityRuleRecommendationRunsResult,
    ListDataQualityRulesetEvaluationRunsResult,
    ListDataQualityRulesetsResult,
    ListDataQualityStatisticAnnotationsResult,
    ListDataQualityStatisticsResult,
    ListDevEndpointsResult,
    ListEntitiesResult,
    ListMlTransformsResult,
    ListRegistriesResult,
    ListSchemasResult,
    ListSchemaVersionsResult,
    ListSessionsResult,
    ListStatementsResult,
    ListTableOptimizerRunsResult,
    ListTriggersResult,
    ListUsageProfilesResult,
    ListWorkflowsResult,
    ModifyIntegrationResult,
    PutResourcePolicyResult,
    PutSchemaVersionMetadataResult,
    QuerySchemaVersionMetadataResult,
    RegisterSchemaVersionResult,
    RemoveSchemaVersionMetadataResult,
    ResetJobBookmarkResult,
    ResumeWorkflowRunResult,
    RunStatementResult,
    SearchTablesResult,
    StartBlueprintRunResult,
    StartColumnStatisticsTaskRunResult,
    StartDataQualityRuleRecommendationRunResult,
    StartDataQualityRulesetEvaluationRunResult,
    StartExportLabelsTaskRunResult,
    StartImportLabelsTaskRunResult,
    StartMlEvaluationTaskRunResult,
    StartMlLabelingSetGenerationTaskRunResult,
    StartTriggerResult,
    StartWorkflowRunResult,
    StopSessionResult,
    StopTriggerResult,
    UpdateBlueprintResult,
    UpdateColumnStatisticsForPartitionResult,
    UpdateColumnStatisticsForTableResult,
    UpdateDataQualityRulesetResult,
    UpdateIntegrationResourcePropertyResult,
    UpdateJobFromSourceControlResult,
    UpdateJobResult,
    UpdateMlTransformResult,
    UpdateRegistryResult,
    UpdateSchemaResult,
    UpdateSourceControlFromJobResult,
    UpdateTriggerResult,
    UpdateUsageProfileResult,
    UpdateWorkflowResult,
)

_TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "TIMEOUT", "STOPPED", "ERROR"}

__all__ = [
    "BatchCreatePartitionResult",
    "BatchDeleteConnectionResult",
    "BatchDeletePartitionResult",
    "BatchDeleteTableResult",
    "BatchDeleteTableVersionResult",
    "BatchGetBlueprintsResult",
    "BatchGetCrawlersResult",
    "BatchGetCustomEntityTypesResult",
    "BatchGetDataQualityResultResult",
    "BatchGetDevEndpointsResult",
    "BatchGetJobsResult",
    "BatchGetPartitionResult",
    "BatchGetTableOptimizerResult",
    "BatchGetTriggersResult",
    "BatchGetWorkflowsResult",
    "BatchPutDataQualityStatisticAnnotationResult",
    "BatchStopJobRunResult",
    "BatchUpdatePartitionResult",
    "CancelMlTaskRunResult",
    "CheckSchemaVersionValidityResult",
    "CreateBlueprintResult",
    "CreateConnectionResult",
    "CreateCustomEntityTypeResult",
    "CreateDataQualityRulesetResult",
    "CreateDevEndpointResult",
    "CreateGlueIdentityCenterConfigurationResult",
    "CreateIntegrationResourcePropertyResult",
    "CreateIntegrationResult",
    "CreateJobResult",
    "CreateMlTransformResult",
    "CreateRegistryResult",
    "CreateSchemaResult",
    "CreateScriptResult",
    "CreateSecurityConfigurationResult",
    "CreateSessionResult",
    "CreateTriggerResult",
    "CreateUsageProfileResult",
    "CreateWorkflowResult",
    "DeleteBlueprintResult",
    "DeleteCustomEntityTypeResult",
    "DeleteIntegrationResult",
    "DeleteJobResult",
    "DeleteMlTransformResult",
    "DeleteRegistryResult",
    "DeleteSchemaResult",
    "DeleteSchemaVersionsResult",
    "DeleteSessionResult",
    "DeleteTriggerResult",
    "DeleteWorkflowResult",
    "DescribeConnectionTypeResult",
    "DescribeEntityResult",
    "DescribeInboundIntegrationsResult",
    "DescribeIntegrationsResult",
    "GetBlueprintResult",
    "GetBlueprintRunResult",
    "GetBlueprintRunsResult",
    "GetCatalogImportStatusResult",
    "GetCatalogResult",
    "GetCatalogsResult",
    "GetClassifierResult",
    "GetClassifiersResult",
    "GetColumnStatisticsForPartitionResult",
    "GetColumnStatisticsForTableResult",
    "GetColumnStatisticsTaskRunResult",
    "GetColumnStatisticsTaskRunsResult",
    "GetColumnStatisticsTaskSettingsResult",
    "GetConnectionResult",
    "GetConnectionsResult",
    "GetCrawlerMetricsResult",
    "GetCrawlerResult",
    "GetCrawlersResult",
    "GetCustomEntityTypeResult",
    "GetDataCatalogEncryptionSettingsResult",
    "GetDataQualityModelResult",
    "GetDataQualityModelResultResult",
    "GetDataQualityResultResult",
    "GetDataQualityRuleRecommendationRunResult",
    "GetDataQualityRulesetEvaluationRunResult",
    "GetDataQualityRulesetResult",
    "GetDatabaseResult",
    "GetDatabasesResult",
    "GetDataflowGraphResult",
    "GetDevEndpointResult",
    "GetDevEndpointsResult",
    "GetEntityRecordsResult",
    "GetGlueIdentityCenterConfigurationResult",
    "GetIntegrationResourcePropertyResult",
    "GetIntegrationTablePropertiesResult",
    "GetJobBookmarkResult",
    "GetJobRunsResult",
    "GetJobsResult",
    "GetMappingResult",
    "GetMlTaskRunResult",
    "GetMlTaskRunsResult",
    "GetMlTransformResult",
    "GetMlTransformsResult",
    "GetPartitionIndexesResult",
    "GetPartitionResult",
    "GetPartitionsResult",
    "GetPlanResult",
    "GetRegistryResult",
    "GetResourcePoliciesResult",
    "GetResourcePolicyResult",
    "GetSchemaByDefinitionResult",
    "GetSchemaResult",
    "GetSchemaVersionResult",
    "GetSchemaVersionsDiffResult",
    "GetSecurityConfigurationResult",
    "GetSecurityConfigurationsResult",
    "GetSessionResult",
    "GetStatementResult",
    "GetTableOptimizerResult",
    "GetTableResult",
    "GetTableVersionResult",
    "GetTableVersionsResult",
    "GetTablesResult",
    "GetTagsResult",
    "GetTriggerResult",
    "GetTriggersResult",
    "GetUnfilteredPartitionMetadataResult",
    "GetUnfilteredPartitionsMetadataResult",
    "GetUnfilteredTableMetadataResult",
    "GetUsageProfileResult",
    "GetUserDefinedFunctionResult",
    "GetUserDefinedFunctionsResult",
    "GetWorkflowResult",
    "GetWorkflowRunPropertiesResult",
    "GetWorkflowRunResult",
    "GetWorkflowRunsResult",
    "GlueJob",
    "GlueJobRun",
    "ListBlueprintsResult",
    "ListColumnStatisticsTaskRunsResult",
    "ListConnectionTypesResult",
    "ListCrawlersResult",
    "ListCrawlsResult",
    "ListCustomEntityTypesResult",
    "ListDataQualityResultsResult",
    "ListDataQualityRuleRecommendationRunsResult",
    "ListDataQualityRulesetEvaluationRunsResult",
    "ListDataQualityRulesetsResult",
    "ListDataQualityStatisticAnnotationsResult",
    "ListDataQualityStatisticsResult",
    "ListDevEndpointsResult",
    "ListEntitiesResult",
    "ListMlTransformsResult",
    "ListRegistriesResult",
    "ListSchemaVersionsResult",
    "ListSchemasResult",
    "ListSessionsResult",
    "ListStatementsResult",
    "ListTableOptimizerRunsResult",
    "ListTriggersResult",
    "ListUsageProfilesResult",
    "ListWorkflowsResult",
    "ModifyIntegrationResult",
    "PutResourcePolicyResult",
    "PutSchemaVersionMetadataResult",
    "QuerySchemaVersionMetadataResult",
    "RegisterSchemaVersionResult",
    "RemoveSchemaVersionMetadataResult",
    "ResetJobBookmarkResult",
    "ResumeWorkflowRunResult",
    "RunStatementResult",
    "SearchTablesResult",
    "StartBlueprintRunResult",
    "StartColumnStatisticsTaskRunResult",
    "StartDataQualityRuleRecommendationRunResult",
    "StartDataQualityRulesetEvaluationRunResult",
    "StartExportLabelsTaskRunResult",
    "StartImportLabelsTaskRunResult",
    "StartMlEvaluationTaskRunResult",
    "StartMlLabelingSetGenerationTaskRunResult",
    "StartTriggerResult",
    "StartWorkflowRunResult",
    "StopSessionResult",
    "StopTriggerResult",
    "UpdateBlueprintResult",
    "UpdateColumnStatisticsForPartitionResult",
    "UpdateColumnStatisticsForTableResult",
    "UpdateDataQualityRulesetResult",
    "UpdateIntegrationResourcePropertyResult",
    "UpdateJobFromSourceControlResult",
    "UpdateJobResult",
    "UpdateMlTransformResult",
    "UpdateRegistryResult",
    "UpdateSchemaResult",
    "UpdateSourceControlFromJobResult",
    "UpdateTriggerResult",
    "UpdateUsageProfileResult",
    "UpdateWorkflowResult",
    "batch_create_partition",
    "batch_delete_connection",
    "batch_delete_partition",
    "batch_delete_table",
    "batch_delete_table_version",
    "batch_get_blueprints",
    "batch_get_crawlers",
    "batch_get_custom_entity_types",
    "batch_get_data_quality_result",
    "batch_get_dev_endpoints",
    "batch_get_jobs",
    "batch_get_partition",
    "batch_get_table_optimizer",
    "batch_get_triggers",
    "batch_get_workflows",
    "batch_put_data_quality_statistic_annotation",
    "batch_stop_job_run",
    "batch_update_partition",
    "cancel_data_quality_rule_recommendation_run",
    "cancel_data_quality_ruleset_evaluation_run",
    "cancel_ml_task_run",
    "cancel_statement",
    "check_schema_version_validity",
    "create_blueprint",
    "create_catalog",
    "create_classifier",
    "create_column_statistics_task_settings",
    "create_connection",
    "create_crawler",
    "create_custom_entity_type",
    "create_data_quality_ruleset",
    "create_database",
    "create_dev_endpoint",
    "create_glue_identity_center_configuration",
    "create_integration",
    "create_integration_resource_property",
    "create_integration_table_properties",
    "create_job",
    "create_ml_transform",
    "create_partition",
    "create_partition_index",
    "create_registry",
    "create_schema",
    "create_script",
    "create_security_configuration",
    "create_session",
    "create_table",
    "create_table_optimizer",
    "create_trigger",
    "create_usage_profile",
    "create_user_defined_function",
    "create_workflow",
    "delete_blueprint",
    "delete_catalog",
    "delete_classifier",
    "delete_column_statistics_for_partition",
    "delete_column_statistics_for_table",
    "delete_column_statistics_task_settings",
    "delete_connection",
    "delete_crawler",
    "delete_custom_entity_type",
    "delete_data_quality_ruleset",
    "delete_database",
    "delete_dev_endpoint",
    "delete_glue_identity_center_configuration",
    "delete_integration",
    "delete_integration_table_properties",
    "delete_job",
    "delete_ml_transform",
    "delete_partition",
    "delete_partition_index",
    "delete_registry",
    "delete_resource_policy",
    "delete_schema",
    "delete_schema_versions",
    "delete_security_configuration",
    "delete_session",
    "delete_table",
    "delete_table_optimizer",
    "delete_table_version",
    "delete_trigger",
    "delete_usage_profile",
    "delete_user_defined_function",
    "delete_workflow",
    "describe_connection_type",
    "describe_entity",
    "describe_inbound_integrations",
    "describe_integrations",
    "get_blueprint",
    "get_blueprint_run",
    "get_blueprint_runs",
    "get_catalog",
    "get_catalog_import_status",
    "get_catalogs",
    "get_classifier",
    "get_classifiers",
    "get_column_statistics_for_partition",
    "get_column_statistics_for_table",
    "get_column_statistics_task_run",
    "get_column_statistics_task_runs",
    "get_column_statistics_task_settings",
    "get_connection",
    "get_connections",
    "get_crawler",
    "get_crawler_metrics",
    "get_crawlers",
    "get_custom_entity_type",
    "get_data_catalog_encryption_settings",
    "get_data_quality_model",
    "get_data_quality_model_result",
    "get_data_quality_result",
    "get_data_quality_rule_recommendation_run",
    "get_data_quality_ruleset",
    "get_data_quality_ruleset_evaluation_run",
    "get_database",
    "get_databases",
    "get_dataflow_graph",
    "get_dev_endpoint",
    "get_dev_endpoints",
    "get_entity_records",
    "get_glue_identity_center_configuration",
    "get_integration_resource_property",
    "get_integration_table_properties",
    "get_job",
    "get_job_bookmark",
    "get_job_run",
    "get_job_runs",
    "get_jobs",
    "get_mapping",
    "get_ml_task_run",
    "get_ml_task_runs",
    "get_ml_transform",
    "get_ml_transforms",
    "get_partition",
    "get_partition_indexes",
    "get_partitions",
    "get_plan",
    "get_registry",
    "get_resource_policies",
    "get_resource_policy",
    "get_schema",
    "get_schema_by_definition",
    "get_schema_version",
    "get_schema_versions_diff",
    "get_security_configuration",
    "get_security_configurations",
    "get_session",
    "get_statement",
    "get_table",
    "get_table_optimizer",
    "get_table_version",
    "get_table_versions",
    "get_tables",
    "get_tags",
    "get_trigger",
    "get_triggers",
    "get_unfiltered_partition_metadata",
    "get_unfiltered_partitions_metadata",
    "get_unfiltered_table_metadata",
    "get_usage_profile",
    "get_user_defined_function",
    "get_user_defined_functions",
    "get_workflow",
    "get_workflow_run",
    "get_workflow_run_properties",
    "get_workflow_runs",
    "import_catalog_to_glue",
    "list_blueprints",
    "list_column_statistics_task_runs",
    "list_connection_types",
    "list_crawlers",
    "list_crawls",
    "list_custom_entity_types",
    "list_data_quality_results",
    "list_data_quality_rule_recommendation_runs",
    "list_data_quality_ruleset_evaluation_runs",
    "list_data_quality_rulesets",
    "list_data_quality_statistic_annotations",
    "list_data_quality_statistics",
    "list_dev_endpoints",
    "list_entities",
    "list_job_runs",
    "list_jobs",
    "list_ml_transforms",
    "list_registries",
    "list_schema_versions",
    "list_schemas",
    "list_sessions",
    "list_statements",
    "list_table_optimizer_runs",
    "list_triggers",
    "list_usage_profiles",
    "list_workflows",
    "modify_integration",
    "put_data_catalog_encryption_settings",
    "put_data_quality_profile_annotation",
    "put_resource_policy",
    "put_schema_version_metadata",
    "put_workflow_run_properties",
    "query_schema_version_metadata",
    "register_schema_version",
    "remove_schema_version_metadata",
    "reset_job_bookmark",
    "resume_workflow_run",
    "run_connection",
    "run_job_and_wait",
    "run_statement",
    "search_tables",
    "start_blueprint_run",
    "start_column_statistics_task_run",
    "start_column_statistics_task_run_schedule",
    "start_crawler",
    "start_crawler_schedule",
    "start_data_quality_rule_recommendation_run",
    "start_data_quality_ruleset_evaluation_run",
    "start_export_labels_task_run",
    "start_import_labels_task_run",
    "start_job_run",
    "start_ml_evaluation_task_run",
    "start_ml_labeling_set_generation_task_run",
    "start_trigger",
    "start_workflow_run",
    "stop_column_statistics_task_run",
    "stop_column_statistics_task_run_schedule",
    "stop_crawler",
    "stop_crawler_schedule",
    "stop_job_run",
    "stop_session",
    "stop_trigger",
    "stop_workflow_run",
    "tag_resource",
    "untag_resource",
    "update_blueprint",
    "update_catalog",
    "update_classifier",
    "update_column_statistics_for_partition",
    "update_column_statistics_for_table",
    "update_column_statistics_task_settings",
    "update_connection",
    "update_crawler",
    "update_crawler_schedule",
    "update_data_quality_ruleset",
    "update_database",
    "update_dev_endpoint",
    "update_glue_identity_center_configuration",
    "update_integration_resource_property",
    "update_integration_table_properties",
    "update_job",
    "update_job_from_source_control",
    "update_ml_transform",
    "update_partition",
    "update_registry",
    "update_schema",
    "update_source_control_from_job",
    "update_table",
    "update_table_optimizer",
    "update_trigger",
    "update_usage_profile",
    "update_user_defined_function",
    "update_workflow",
    "wait_for_job_run",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_run(run: dict) -> GlueJobRun:
    """Convert a raw API run dict to a :class:`GlueJobRun`."""
    return GlueJobRun(
        job_run_id=run["Id"],
        job_name=run["JobName"],
        job_run_state=run["JobRunState"],
        started_on=run.get("StartedOn"),
        completed_on=run.get("CompletedOn"),
        execution_time=run.get("ExecutionTime"),
        error_message=run.get("ErrorMessage"),
        arguments=run.get("Arguments", {}),
    )


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def start_job_run(
    job_name: str,
    arguments: dict[str, str] | None = None,
    worker_type: str | None = None,
    number_of_workers: int | None = None,
    region_name: str | None = None,
) -> str:
    """Start a Glue ETL job run.

    Args:
        job_name: Name of the Glue job.
        arguments: Job-specific arguments as ``{"--key": "value"}``.  Keys
            must start with ``"--"``.
        worker_type: Override the job's worker type (``"G.1X"``, ``"G.2X"``,
            ``"Standard"``, etc.).
        number_of_workers: Override the number of workers.
        region_name: AWS region override.

    Returns:
        The job run ID.

    Raises:
        RuntimeError: If the start request fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {"JobName": job_name}
    if arguments:
        kwargs["Arguments"] = arguments
    if worker_type:
        kwargs["WorkerType"] = worker_type
    if number_of_workers:
        kwargs["NumberOfWorkers"] = number_of_workers
    try:
        resp = await client.call("StartJobRun", **kwargs)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to start Glue job {job_name!r}") from exc
    return resp["JobRunId"]


async def get_job_run(
    job_name: str,
    run_id: str,
    region_name: str | None = None,
) -> GlueJobRun:
    """Fetch the current status of a Glue job run.

    Args:
        job_name: Name of the Glue job.
        run_id: Job run ID returned by :func:`start_job_run`.
        region_name: AWS region override.

    Returns:
        A :class:`GlueJobRun` with current state and metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    try:
        resp = await client.call("GetJobRun", JobName=job_name, RunId=run_id)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_job_run failed for {job_name!r}/{run_id!r}") from exc
    return _parse_run(resp["JobRun"])


async def get_job(
    job_name: str,
    region_name: str | None = None,
) -> GlueJob:
    """Fetch metadata for a Glue job definition.

    Args:
        job_name: Name of the Glue job.
        region_name: AWS region override.

    Returns:
        A :class:`GlueJob` with job configuration metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    try:
        resp = await client.call("GetJob", JobName=job_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_job failed for {job_name!r}") from exc
    job = resp["Job"]
    return GlueJob(
        job_name=job["Name"],
        description=job.get("Description"),
        role=job.get("Role"),
        glue_version=job.get("GlueVersion"),
        worker_type=job.get("WorkerType"),
        number_of_workers=job.get("NumberOfWorkers"),
        max_retries=job.get("MaxRetries", 0),
        timeout=job.get("Timeout"),
    )


async def list_jobs(
    region_name: str | None = None,
) -> list[str]:
    """List the names of all Glue jobs in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of job names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    try:
        items = await client.paginate("GetJobs", "Jobs")
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return [job["Name"] for job in items]


async def list_job_runs(
    job_name: str,
    region_name: str | None = None,
) -> list[GlueJobRun]:
    """List recent runs for a Glue job.

    Args:
        job_name: Name of the Glue job.
        region_name: AWS region override.

    Returns:
        A list of :class:`GlueJobRun` objects ordered newest first.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    try:
        items = await client.paginate("GetJobRuns", "JobRuns", JobName=job_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"list_job_runs failed for {job_name!r}") from exc
    return [_parse_run(r) for r in items]


async def wait_for_job_run(
    job_name: str,
    run_id: str,
    poll_interval: float = 15.0,
    timeout: float = 3600.0,
    region_name: str | None = None,
) -> GlueJobRun:
    """Poll until a Glue job run reaches a terminal state.

    Args:
        job_name: Name of the Glue job.
        run_id: Job run ID.
        poll_interval: Seconds between status checks (default ``15``).
        timeout: Maximum seconds to wait (default ``3600`` / 1 hour).
        region_name: AWS region override.

    Returns:
        The final :class:`GlueJobRun`.

    Raises:
        TimeoutError: If the run does not finish within *timeout*.
    """
    deadline = time.monotonic() + timeout
    while True:
        run = await get_job_run(job_name, run_id, region_name=region_name)
        if run.finished:
            return run
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Glue job run {run_id!r} did not finish within {timeout}s")
        await asyncio.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def run_job_and_wait(
    job_name: str,
    arguments: dict[str, str] | None = None,
    worker_type: str | None = None,
    number_of_workers: int | None = None,
    poll_interval: float = 15.0,
    timeout: float = 3600.0,
    region_name: str | None = None,
) -> GlueJobRun:
    """Start a Glue job run and wait until it reaches a terminal state.

    Combines :func:`start_job_run` and :func:`wait_for_job_run`.

    Args:
        job_name: Name of the Glue job.
        arguments: Job arguments as ``{"--key": "value"}``.
        worker_type: Override the worker type.
        number_of_workers: Override the number of workers.
        poll_interval: Seconds between status checks (default ``15``).
        timeout: Maximum seconds to wait (default ``3600``).
        region_name: AWS region override.

    Returns:
        The final :class:`GlueJobRun`.

    Raises:
        RuntimeError: If the start request fails.
        TimeoutError: If the run does not finish within *timeout*.
    """
    run_id = await start_job_run(
        job_name,
        arguments=arguments,
        worker_type=worker_type,
        number_of_workers=number_of_workers,
        region_name=region_name,
    )
    return await wait_for_job_run(
        job_name,
        run_id,
        poll_interval=poll_interval,
        timeout=timeout,
        region_name=region_name,
    )


async def stop_job_run(
    job_name: str,
    run_id: str,
    region_name: str | None = None,
) -> None:
    """Stop a running Glue job run.

    Args:
        job_name: Name of the Glue job.
        run_id: Job run ID to stop.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the stop request fails.
    """
    client = async_client("glue", region_name)
    try:
        await client.call(
            "BatchStopJobRun",
            JobName=job_name,
            JobRunIds=[run_id],
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"stop_job_run failed for {job_name!r}/{run_id!r}") from exc


async def batch_create_partition(
    database_name: str,
    table_name: str,
    partition_input_list: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchCreatePartitionResult:
    """Batch create partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_input_list: Partition input list.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionInputList"] = partition_input_list
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchCreatePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch create partition") from exc
    return BatchCreatePartitionResult(
        errors=resp.get("Errors"),
    )


async def batch_delete_connection(
    connection_name_list: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchDeleteConnectionResult:
    """Batch delete connection.

    Args:
        connection_name_list: Connection name list.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionNameList"] = connection_name_list
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchDeleteConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete connection") from exc
    return BatchDeleteConnectionResult(
        succeeded=resp.get("Succeeded"),
        errors=resp.get("Errors"),
    )


async def batch_delete_partition(
    database_name: str,
    table_name: str,
    partitions_to_delete: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchDeletePartitionResult:
    """Batch delete partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partitions_to_delete: Partitions to delete.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionsToDelete"] = partitions_to_delete
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchDeletePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete partition") from exc
    return BatchDeletePartitionResult(
        errors=resp.get("Errors"),
    )


async def batch_delete_table(
    database_name: str,
    tables_to_delete: list[str],
    *,
    catalog_id: str | None = None,
    transaction_id: str | None = None,
    region_name: str | None = None,
) -> BatchDeleteTableResult:
    """Batch delete table.

    Args:
        database_name: Database name.
        tables_to_delete: Tables to delete.
        catalog_id: Catalog id.
        transaction_id: Transaction id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TablesToDelete"] = tables_to_delete
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    try:
        resp = await client.call("BatchDeleteTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete table") from exc
    return BatchDeleteTableResult(
        errors=resp.get("Errors"),
    )


async def batch_delete_table_version(
    database_name: str,
    table_name: str,
    version_ids: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchDeleteTableVersionResult:
    """Batch delete table version.

    Args:
        database_name: Database name.
        table_name: Table name.
        version_ids: Version ids.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["VersionIds"] = version_ids
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchDeleteTableVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete table version") from exc
    return BatchDeleteTableVersionResult(
        errors=resp.get("Errors"),
    )


async def batch_get_blueprints(
    names: list[str],
    *,
    include_blueprint: bool | None = None,
    include_parameter_spec: bool | None = None,
    region_name: str | None = None,
) -> BatchGetBlueprintsResult:
    """Batch get blueprints.

    Args:
        names: Names.
        include_blueprint: Include blueprint.
        include_parameter_spec: Include parameter spec.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    if include_blueprint is not None:
        kwargs["IncludeBlueprint"] = include_blueprint
    if include_parameter_spec is not None:
        kwargs["IncludeParameterSpec"] = include_parameter_spec
    try:
        resp = await client.call("BatchGetBlueprints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get blueprints") from exc
    return BatchGetBlueprintsResult(
        blueprints=resp.get("Blueprints"),
        missing_blueprints=resp.get("MissingBlueprints"),
    )


async def batch_get_crawlers(
    crawler_names: list[str],
    region_name: str | None = None,
) -> BatchGetCrawlersResult:
    """Batch get crawlers.

    Args:
        crawler_names: Crawler names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CrawlerNames"] = crawler_names
    try:
        resp = await client.call("BatchGetCrawlers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get crawlers") from exc
    return BatchGetCrawlersResult(
        crawlers=resp.get("Crawlers"),
        crawlers_not_found=resp.get("CrawlersNotFound"),
    )


async def batch_get_custom_entity_types(
    names: list[str],
    region_name: str | None = None,
) -> BatchGetCustomEntityTypesResult:
    """Batch get custom entity types.

    Args:
        names: Names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    try:
        resp = await client.call("BatchGetCustomEntityTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get custom entity types") from exc
    return BatchGetCustomEntityTypesResult(
        custom_entity_types=resp.get("CustomEntityTypes"),
        custom_entity_types_not_found=resp.get("CustomEntityTypesNotFound"),
    )


async def batch_get_data_quality_result(
    result_ids: list[str],
    region_name: str | None = None,
) -> BatchGetDataQualityResultResult:
    """Batch get data quality result.

    Args:
        result_ids: Result ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResultIds"] = result_ids
    try:
        resp = await client.call("BatchGetDataQualityResult", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get data quality result") from exc
    return BatchGetDataQualityResultResult(
        results=resp.get("Results"),
        results_not_found=resp.get("ResultsNotFound"),
    )


async def batch_get_dev_endpoints(
    dev_endpoint_names: list[str],
    region_name: str | None = None,
) -> BatchGetDevEndpointsResult:
    """Batch get dev endpoints.

    Args:
        dev_endpoint_names: Dev endpoint names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DevEndpointNames"] = dev_endpoint_names
    try:
        resp = await client.call("BatchGetDevEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get dev endpoints") from exc
    return BatchGetDevEndpointsResult(
        dev_endpoints=resp.get("DevEndpoints"),
        dev_endpoints_not_found=resp.get("DevEndpointsNotFound"),
    )


async def batch_get_jobs(
    job_names: list[str],
    region_name: str | None = None,
) -> BatchGetJobsResult:
    """Batch get jobs.

    Args:
        job_names: Job names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobNames"] = job_names
    try:
        resp = await client.call("BatchGetJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get jobs") from exc
    return BatchGetJobsResult(
        jobs=resp.get("Jobs"),
        jobs_not_found=resp.get("JobsNotFound"),
    )


async def batch_get_partition(
    database_name: str,
    table_name: str,
    partitions_to_get: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchGetPartitionResult:
    """Batch get partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partitions_to_get: Partitions to get.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionsToGet"] = partitions_to_get
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchGetPartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get partition") from exc
    return BatchGetPartitionResult(
        partitions=resp.get("Partitions"),
        unprocessed_keys=resp.get("UnprocessedKeys"),
    )


async def batch_get_table_optimizer(
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetTableOptimizerResult:
    """Batch get table optimizer.

    Args:
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Entries"] = entries
    try:
        resp = await client.call("BatchGetTableOptimizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get table optimizer") from exc
    return BatchGetTableOptimizerResult(
        table_optimizers=resp.get("TableOptimizers"),
        failures=resp.get("Failures"),
    )


async def batch_get_triggers(
    trigger_names: list[str],
    region_name: str | None = None,
) -> BatchGetTriggersResult:
    """Batch get triggers.

    Args:
        trigger_names: Trigger names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TriggerNames"] = trigger_names
    try:
        resp = await client.call("BatchGetTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get triggers") from exc
    return BatchGetTriggersResult(
        triggers=resp.get("Triggers"),
        triggers_not_found=resp.get("TriggersNotFound"),
    )


async def batch_get_workflows(
    names: list[str],
    *,
    include_graph: bool | None = None,
    region_name: str | None = None,
) -> BatchGetWorkflowsResult:
    """Batch get workflows.

    Args:
        names: Names.
        include_graph: Include graph.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    if include_graph is not None:
        kwargs["IncludeGraph"] = include_graph
    try:
        resp = await client.call("BatchGetWorkflows", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get workflows") from exc
    return BatchGetWorkflowsResult(
        workflows=resp.get("Workflows"),
        missing_workflows=resp.get("MissingWorkflows"),
    )


async def batch_put_data_quality_statistic_annotation(
    inclusion_annotations: list[dict[str, Any]],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> BatchPutDataQualityStatisticAnnotationResult:
    """Batch put data quality statistic annotation.

    Args:
        inclusion_annotations: Inclusion annotations.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InclusionAnnotations"] = inclusion_annotations
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("BatchPutDataQualityStatisticAnnotation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch put data quality statistic annotation") from exc
    return BatchPutDataQualityStatisticAnnotationResult(
        failed_inclusion_annotations=resp.get("FailedInclusionAnnotations"),
    )


async def batch_stop_job_run(
    job_name: str,
    job_run_ids: list[str],
    region_name: str | None = None,
) -> BatchStopJobRunResult:
    """Batch stop job run.

    Args:
        job_name: Job name.
        job_run_ids: Job run ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    kwargs["JobRunIds"] = job_run_ids
    try:
        resp = await client.call("BatchStopJobRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch stop job run") from exc
    return BatchStopJobRunResult(
        successful_submissions=resp.get("SuccessfulSubmissions"),
        errors=resp.get("Errors"),
    )


async def batch_update_partition(
    database_name: str,
    table_name: str,
    entries: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> BatchUpdatePartitionResult:
    """Batch update partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        entries: Entries.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Entries"] = entries
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("BatchUpdatePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update partition") from exc
    return BatchUpdatePartitionResult(
        errors=resp.get("Errors"),
    )


async def cancel_data_quality_rule_recommendation_run(
    run_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel data quality rule recommendation run.

    Args:
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RunId"] = run_id
    try:
        await client.call("CancelDataQualityRuleRecommendationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel data quality rule recommendation run") from exc
    return None


async def cancel_data_quality_ruleset_evaluation_run(
    run_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel data quality ruleset evaluation run.

    Args:
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RunId"] = run_id
    try:
        await client.call("CancelDataQualityRulesetEvaluationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel data quality ruleset evaluation run") from exc
    return None


async def cancel_ml_task_run(
    transform_id: str,
    task_run_id: str,
    region_name: str | None = None,
) -> CancelMlTaskRunResult:
    """Cancel ml task run.

    Args:
        transform_id: Transform id.
        task_run_id: Task run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    kwargs["TaskRunId"] = task_run_id
    try:
        resp = await client.call("CancelMLTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel ml task run") from exc
    return CancelMlTaskRunResult(
        transform_id=resp.get("TransformId"),
        task_run_id=resp.get("TaskRunId"),
        status=resp.get("Status"),
    )


async def cancel_statement(
    session_id: str,
    id: int,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> None:
    """Cancel statement.

    Args:
        session_id: Session id.
        id: Id.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    kwargs["Id"] = id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        await client.call("CancelStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel statement") from exc
    return None


async def check_schema_version_validity(
    data_format: str,
    schema_definition: str,
    region_name: str | None = None,
) -> CheckSchemaVersionValidityResult:
    """Check schema version validity.

    Args:
        data_format: Data format.
        schema_definition: Schema definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataFormat"] = data_format
    kwargs["SchemaDefinition"] = schema_definition
    try:
        resp = await client.call("CheckSchemaVersionValidity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to check schema version validity") from exc
    return CheckSchemaVersionValidityResult(
        valid=resp.get("Valid"),
        error=resp.get("Error"),
    )


async def create_blueprint(
    name: str,
    blueprint_location: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateBlueprintResult:
    """Create blueprint.

    Args:
        name: Name.
        blueprint_location: Blueprint location.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["BlueprintLocation"] = blueprint_location
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateBlueprint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create blueprint") from exc
    return CreateBlueprintResult(
        name=resp.get("Name"),
    )


async def create_catalog(
    name: str,
    catalog_input: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create catalog.

    Args:
        name: Name.
        catalog_input: Catalog input.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["CatalogInput"] = catalog_input
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create catalog") from exc
    return None


async def create_classifier(
    *,
    grok_classifier: dict[str, Any] | None = None,
    xml_classifier: dict[str, Any] | None = None,
    json_classifier: dict[str, Any] | None = None,
    csv_classifier: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create classifier.

    Args:
        grok_classifier: Grok classifier.
        xml_classifier: Xml classifier.
        json_classifier: Json classifier.
        csv_classifier: Csv classifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if grok_classifier is not None:
        kwargs["GrokClassifier"] = grok_classifier
    if xml_classifier is not None:
        kwargs["XMLClassifier"] = xml_classifier
    if json_classifier is not None:
        kwargs["JsonClassifier"] = json_classifier
    if csv_classifier is not None:
        kwargs["CsvClassifier"] = csv_classifier
    try:
        await client.call("CreateClassifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create classifier") from exc
    return None


async def create_column_statistics_task_settings(
    database_name: str,
    table_name: str,
    role: str,
    *,
    schedule: str | None = None,
    column_name_list: list[str] | None = None,
    sample_size: float | None = None,
    catalog_id: str | None = None,
    security_configuration: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create column statistics task settings.

    Args:
        database_name: Database name.
        table_name: Table name.
        role: Role.
        schedule: Schedule.
        column_name_list: Column name list.
        sample_size: Sample size.
        catalog_id: Catalog id.
        security_configuration: Security configuration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Role"] = role
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if column_name_list is not None:
        kwargs["ColumnNameList"] = column_name_list
    if sample_size is not None:
        kwargs["SampleSize"] = sample_size
    if catalog_id is not None:
        kwargs["CatalogID"] = catalog_id
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateColumnStatisticsTaskSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create column statistics task settings") from exc
    return None


async def create_connection(
    connection_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateConnectionResult:
    """Create connection.

    Args:
        connection_input: Connection input.
        catalog_id: Catalog id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionInput"] = connection_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create connection") from exc
    return CreateConnectionResult(
        create_connection_status=resp.get("CreateConnectionStatus"),
    )


async def create_crawler(
    name: str,
    role: str,
    targets: dict[str, Any],
    *,
    database_name: str | None = None,
    description: str | None = None,
    schedule: str | None = None,
    classifiers: list[str] | None = None,
    table_prefix: str | None = None,
    schema_change_policy: dict[str, Any] | None = None,
    recrawl_policy: dict[str, Any] | None = None,
    lineage_configuration: dict[str, Any] | None = None,
    lake_formation_configuration: dict[str, Any] | None = None,
    configuration: str | None = None,
    crawler_security_configuration: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create crawler.

    Args:
        name: Name.
        role: Role.
        targets: Targets.
        database_name: Database name.
        description: Description.
        schedule: Schedule.
        classifiers: Classifiers.
        table_prefix: Table prefix.
        schema_change_policy: Schema change policy.
        recrawl_policy: Recrawl policy.
        lineage_configuration: Lineage configuration.
        lake_formation_configuration: Lake formation configuration.
        configuration: Configuration.
        crawler_security_configuration: Crawler security configuration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Role"] = role
    kwargs["Targets"] = targets
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if description is not None:
        kwargs["Description"] = description
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if classifiers is not None:
        kwargs["Classifiers"] = classifiers
    if table_prefix is not None:
        kwargs["TablePrefix"] = table_prefix
    if schema_change_policy is not None:
        kwargs["SchemaChangePolicy"] = schema_change_policy
    if recrawl_policy is not None:
        kwargs["RecrawlPolicy"] = recrawl_policy
    if lineage_configuration is not None:
        kwargs["LineageConfiguration"] = lineage_configuration
    if lake_formation_configuration is not None:
        kwargs["LakeFormationConfiguration"] = lake_formation_configuration
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if crawler_security_configuration is not None:
        kwargs["CrawlerSecurityConfiguration"] = crawler_security_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create crawler") from exc
    return None


async def create_custom_entity_type(
    name: str,
    regex_string: str,
    *,
    context_words: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateCustomEntityTypeResult:
    """Create custom entity type.

    Args:
        name: Name.
        regex_string: Regex string.
        context_words: Context words.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RegexString"] = regex_string
    if context_words is not None:
        kwargs["ContextWords"] = context_words
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateCustomEntityType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom entity type") from exc
    return CreateCustomEntityTypeResult(
        name=resp.get("Name"),
    )


async def create_data_quality_ruleset(
    name: str,
    ruleset: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    target_table: dict[str, Any] | None = None,
    data_quality_security_configuration: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateDataQualityRulesetResult:
    """Create data quality ruleset.

    Args:
        name: Name.
        ruleset: Ruleset.
        description: Description.
        tags: Tags.
        target_table: Target table.
        data_quality_security_configuration: Data quality security configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Ruleset"] = ruleset
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    if target_table is not None:
        kwargs["TargetTable"] = target_table
    if data_quality_security_configuration is not None:
        kwargs["DataQualitySecurityConfiguration"] = data_quality_security_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("CreateDataQualityRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data quality ruleset") from exc
    return CreateDataQualityRulesetResult(
        name=resp.get("Name"),
    )


async def create_database(
    database_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create database.

    Args:
        database_input: Database input.
        catalog_id: Catalog id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseInput"] = database_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create database") from exc
    return None


async def create_dev_endpoint(
    endpoint_name: str,
    role_arn: str,
    *,
    security_group_ids: list[str] | None = None,
    subnet_id: str | None = None,
    public_key: str | None = None,
    public_keys: list[str] | None = None,
    number_of_nodes: int | None = None,
    worker_type: str | None = None,
    glue_version: str | None = None,
    number_of_workers: int | None = None,
    extra_python_libs_s3_path: str | None = None,
    extra_jars_s3_path: str | None = None,
    security_configuration: str | None = None,
    tags: dict[str, Any] | None = None,
    arguments: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDevEndpointResult:
    """Create dev endpoint.

    Args:
        endpoint_name: Endpoint name.
        role_arn: Role arn.
        security_group_ids: Security group ids.
        subnet_id: Subnet id.
        public_key: Public key.
        public_keys: Public keys.
        number_of_nodes: Number of nodes.
        worker_type: Worker type.
        glue_version: Glue version.
        number_of_workers: Number of workers.
        extra_python_libs_s3_path: Extra python libs s3 path.
        extra_jars_s3_path: Extra jars s3 path.
        security_configuration: Security configuration.
        tags: Tags.
        arguments: Arguments.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    kwargs["RoleArn"] = role_arn
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if subnet_id is not None:
        kwargs["SubnetId"] = subnet_id
    if public_key is not None:
        kwargs["PublicKey"] = public_key
    if public_keys is not None:
        kwargs["PublicKeys"] = public_keys
    if number_of_nodes is not None:
        kwargs["NumberOfNodes"] = number_of_nodes
    if worker_type is not None:
        kwargs["WorkerType"] = worker_type
    if glue_version is not None:
        kwargs["GlueVersion"] = glue_version
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if extra_python_libs_s3_path is not None:
        kwargs["ExtraPythonLibsS3Path"] = extra_python_libs_s3_path
    if extra_jars_s3_path is not None:
        kwargs["ExtraJarsS3Path"] = extra_jars_s3_path
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    if arguments is not None:
        kwargs["Arguments"] = arguments
    try:
        resp = await client.call("CreateDevEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dev endpoint") from exc
    return CreateDevEndpointResult(
        endpoint_name=resp.get("EndpointName"),
        status=resp.get("Status"),
        security_group_ids=resp.get("SecurityGroupIds"),
        subnet_id=resp.get("SubnetId"),
        role_arn=resp.get("RoleArn"),
        yarn_endpoint_address=resp.get("YarnEndpointAddress"),
        zeppelin_remote_spark_interpreter_port=resp.get("ZeppelinRemoteSparkInterpreterPort"),
        number_of_nodes=resp.get("NumberOfNodes"),
        worker_type=resp.get("WorkerType"),
        glue_version=resp.get("GlueVersion"),
        number_of_workers=resp.get("NumberOfWorkers"),
        availability_zone=resp.get("AvailabilityZone"),
        vpc_id=resp.get("VpcId"),
        extra_python_libs_s3_path=resp.get("ExtraPythonLibsS3Path"),
        extra_jars_s3_path=resp.get("ExtraJarsS3Path"),
        failure_reason=resp.get("FailureReason"),
        security_configuration=resp.get("SecurityConfiguration"),
        created_timestamp=resp.get("CreatedTimestamp"),
        arguments=resp.get("Arguments"),
    )


async def create_glue_identity_center_configuration(
    instance_arn: str,
    *,
    scopes: list[str] | None = None,
    user_background_sessions_enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateGlueIdentityCenterConfigurationResult:
    """Create glue identity center configuration.

    Args:
        instance_arn: Instance arn.
        scopes: Scopes.
        user_background_sessions_enabled: User background sessions enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if scopes is not None:
        kwargs["Scopes"] = scopes
    if user_background_sessions_enabled is not None:
        kwargs["UserBackgroundSessionsEnabled"] = user_background_sessions_enabled
    try:
        resp = await client.call("CreateGlueIdentityCenterConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create glue identity center configuration") from exc
    return CreateGlueIdentityCenterConfigurationResult(
        application_arn=resp.get("ApplicationArn"),
    )


async def create_integration(
    integration_name: str,
    source_arn: str,
    target_arn: str,
    *,
    description: str | None = None,
    data_filter: str | None = None,
    kms_key_id: str | None = None,
    additional_encryption_context: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    integration_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateIntegrationResult:
    """Create integration.

    Args:
        integration_name: Integration name.
        source_arn: Source arn.
        target_arn: Target arn.
        description: Description.
        data_filter: Data filter.
        kms_key_id: Kms key id.
        additional_encryption_context: Additional encryption context.
        tags: Tags.
        integration_config: Integration config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationName"] = integration_name
    kwargs["SourceArn"] = source_arn
    kwargs["TargetArn"] = target_arn
    if description is not None:
        kwargs["Description"] = description
    if data_filter is not None:
        kwargs["DataFilter"] = data_filter
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if additional_encryption_context is not None:
        kwargs["AdditionalEncryptionContext"] = additional_encryption_context
    if tags is not None:
        kwargs["Tags"] = tags
    if integration_config is not None:
        kwargs["IntegrationConfig"] = integration_config
    try:
        resp = await client.call("CreateIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create integration") from exc
    return CreateIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        description=resp.get("Description"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KmsKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
        status=resp.get("Status"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
        data_filter=resp.get("DataFilter"),
        integration_config=resp.get("IntegrationConfig"),
    )


async def create_integration_resource_property(
    resource_arn: str,
    *,
    source_processing_properties: dict[str, Any] | None = None,
    target_processing_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateIntegrationResourcePropertyResult:
    """Create integration resource property.

    Args:
        resource_arn: Resource arn.
        source_processing_properties: Source processing properties.
        target_processing_properties: Target processing properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if source_processing_properties is not None:
        kwargs["SourceProcessingProperties"] = source_processing_properties
    if target_processing_properties is not None:
        kwargs["TargetProcessingProperties"] = target_processing_properties
    try:
        resp = await client.call("CreateIntegrationResourceProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create integration resource property") from exc
    return CreateIntegrationResourcePropertyResult(
        resource_arn=resp.get("ResourceArn"),
        source_processing_properties=resp.get("SourceProcessingProperties"),
        target_processing_properties=resp.get("TargetProcessingProperties"),
    )


async def create_integration_table_properties(
    resource_arn: str,
    table_name: str,
    *,
    source_table_config: dict[str, Any] | None = None,
    target_table_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create integration table properties.

    Args:
        resource_arn: Resource arn.
        table_name: Table name.
        source_table_config: Source table config.
        target_table_config: Target table config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TableName"] = table_name
    if source_table_config is not None:
        kwargs["SourceTableConfig"] = source_table_config
    if target_table_config is not None:
        kwargs["TargetTableConfig"] = target_table_config
    try:
        await client.call("CreateIntegrationTableProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create integration table properties") from exc
    return None


async def create_job(
    name: str,
    role: str,
    command: dict[str, Any],
    *,
    job_mode: str | None = None,
    job_run_queuing_enabled: bool | None = None,
    description: str | None = None,
    log_uri: str | None = None,
    execution_property: dict[str, Any] | None = None,
    default_arguments: dict[str, Any] | None = None,
    non_overridable_arguments: dict[str, Any] | None = None,
    connections: dict[str, Any] | None = None,
    max_retries: int | None = None,
    allocated_capacity: int | None = None,
    timeout: int | None = None,
    max_capacity: float | None = None,
    security_configuration: str | None = None,
    tags: dict[str, Any] | None = None,
    notification_property: dict[str, Any] | None = None,
    glue_version: str | None = None,
    number_of_workers: int | None = None,
    worker_type: str | None = None,
    code_gen_configuration_nodes: dict[str, Any] | None = None,
    execution_class: str | None = None,
    source_control_details: dict[str, Any] | None = None,
    maintenance_window: str | None = None,
    region_name: str | None = None,
) -> CreateJobResult:
    """Create job.

    Args:
        name: Name.
        role: Role.
        command: Command.
        job_mode: Job mode.
        job_run_queuing_enabled: Job run queuing enabled.
        description: Description.
        log_uri: Log uri.
        execution_property: Execution property.
        default_arguments: Default arguments.
        non_overridable_arguments: Non overridable arguments.
        connections: Connections.
        max_retries: Max retries.
        allocated_capacity: Allocated capacity.
        timeout: Timeout.
        max_capacity: Max capacity.
        security_configuration: Security configuration.
        tags: Tags.
        notification_property: Notification property.
        glue_version: Glue version.
        number_of_workers: Number of workers.
        worker_type: Worker type.
        code_gen_configuration_nodes: Code gen configuration nodes.
        execution_class: Execution class.
        source_control_details: Source control details.
        maintenance_window: Maintenance window.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Role"] = role
    kwargs["Command"] = command
    if job_mode is not None:
        kwargs["JobMode"] = job_mode
    if job_run_queuing_enabled is not None:
        kwargs["JobRunQueuingEnabled"] = job_run_queuing_enabled
    if description is not None:
        kwargs["Description"] = description
    if log_uri is not None:
        kwargs["LogUri"] = log_uri
    if execution_property is not None:
        kwargs["ExecutionProperty"] = execution_property
    if default_arguments is not None:
        kwargs["DefaultArguments"] = default_arguments
    if non_overridable_arguments is not None:
        kwargs["NonOverridableArguments"] = non_overridable_arguments
    if connections is not None:
        kwargs["Connections"] = connections
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    if allocated_capacity is not None:
        kwargs["AllocatedCapacity"] = allocated_capacity
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    if notification_property is not None:
        kwargs["NotificationProperty"] = notification_property
    if glue_version is not None:
        kwargs["GlueVersion"] = glue_version
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if worker_type is not None:
        kwargs["WorkerType"] = worker_type
    if code_gen_configuration_nodes is not None:
        kwargs["CodeGenConfigurationNodes"] = code_gen_configuration_nodes
    if execution_class is not None:
        kwargs["ExecutionClass"] = execution_class
    if source_control_details is not None:
        kwargs["SourceControlDetails"] = source_control_details
    if maintenance_window is not None:
        kwargs["MaintenanceWindow"] = maintenance_window
    try:
        resp = await client.call("CreateJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create job") from exc
    return CreateJobResult(
        name=resp.get("Name"),
    )


async def create_ml_transform(
    name: str,
    input_record_tables: list[dict[str, Any]],
    parameters: dict[str, Any],
    role: str,
    *,
    description: str | None = None,
    glue_version: str | None = None,
    max_capacity: float | None = None,
    worker_type: str | None = None,
    number_of_workers: int | None = None,
    timeout: int | None = None,
    max_retries: int | None = None,
    tags: dict[str, Any] | None = None,
    transform_encryption: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateMlTransformResult:
    """Create ml transform.

    Args:
        name: Name.
        input_record_tables: Input record tables.
        parameters: Parameters.
        role: Role.
        description: Description.
        glue_version: Glue version.
        max_capacity: Max capacity.
        worker_type: Worker type.
        number_of_workers: Number of workers.
        timeout: Timeout.
        max_retries: Max retries.
        tags: Tags.
        transform_encryption: Transform encryption.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["InputRecordTables"] = input_record_tables
    kwargs["Parameters"] = parameters
    kwargs["Role"] = role
    if description is not None:
        kwargs["Description"] = description
    if glue_version is not None:
        kwargs["GlueVersion"] = glue_version
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if worker_type is not None:
        kwargs["WorkerType"] = worker_type
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    if tags is not None:
        kwargs["Tags"] = tags
    if transform_encryption is not None:
        kwargs["TransformEncryption"] = transform_encryption
    try:
        resp = await client.call("CreateMLTransform", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ml transform") from exc
    return CreateMlTransformResult(
        transform_id=resp.get("TransformId"),
    )


async def create_partition(
    database_name: str,
    table_name: str,
    partition_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_input: Partition input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionInput"] = partition_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("CreatePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create partition") from exc
    return None


async def create_partition_index(
    database_name: str,
    table_name: str,
    partition_index: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create partition index.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_index: Partition index.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionIndex"] = partition_index
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("CreatePartitionIndex", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create partition index") from exc
    return None


async def create_registry(
    registry_name: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateRegistryResult:
    """Create registry.

    Args:
        registry_name: Registry name.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegistryName"] = registry_name
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateRegistry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create registry") from exc
    return CreateRegistryResult(
        registry_arn=resp.get("RegistryArn"),
        registry_name=resp.get("RegistryName"),
        description=resp.get("Description"),
        tags=resp.get("Tags"),
    )


async def create_schema(
    schema_name: str,
    data_format: str,
    *,
    registry_id: dict[str, Any] | None = None,
    compatibility: str | None = None,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    schema_definition: str | None = None,
    region_name: str | None = None,
) -> CreateSchemaResult:
    """Create schema.

    Args:
        schema_name: Schema name.
        data_format: Data format.
        registry_id: Registry id.
        compatibility: Compatibility.
        description: Description.
        tags: Tags.
        schema_definition: Schema definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaName"] = schema_name
    kwargs["DataFormat"] = data_format
    if registry_id is not None:
        kwargs["RegistryId"] = registry_id
    if compatibility is not None:
        kwargs["Compatibility"] = compatibility
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    if schema_definition is not None:
        kwargs["SchemaDefinition"] = schema_definition
    try:
        resp = await client.call("CreateSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create schema") from exc
    return CreateSchemaResult(
        registry_name=resp.get("RegistryName"),
        registry_arn=resp.get("RegistryArn"),
        schema_name=resp.get("SchemaName"),
        schema_arn=resp.get("SchemaArn"),
        description=resp.get("Description"),
        data_format=resp.get("DataFormat"),
        compatibility=resp.get("Compatibility"),
        schema_checkpoint=resp.get("SchemaCheckpoint"),
        latest_schema_version=resp.get("LatestSchemaVersion"),
        next_schema_version=resp.get("NextSchemaVersion"),
        schema_status=resp.get("SchemaStatus"),
        tags=resp.get("Tags"),
        schema_version_id=resp.get("SchemaVersionId"),
        schema_version_status=resp.get("SchemaVersionStatus"),
    )


async def create_script(
    *,
    dag_nodes: list[dict[str, Any]] | None = None,
    dag_edges: list[dict[str, Any]] | None = None,
    language: str | None = None,
    region_name: str | None = None,
) -> CreateScriptResult:
    """Create script.

    Args:
        dag_nodes: Dag nodes.
        dag_edges: Dag edges.
        language: Language.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if dag_nodes is not None:
        kwargs["DagNodes"] = dag_nodes
    if dag_edges is not None:
        kwargs["DagEdges"] = dag_edges
    if language is not None:
        kwargs["Language"] = language
    try:
        resp = await client.call("CreateScript", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create script") from exc
    return CreateScriptResult(
        python_script=resp.get("PythonScript"),
        scala_code=resp.get("ScalaCode"),
    )


async def create_security_configuration(
    name: str,
    encryption_configuration: dict[str, Any],
    region_name: str | None = None,
) -> CreateSecurityConfigurationResult:
    """Create security configuration.

    Args:
        name: Name.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["EncryptionConfiguration"] = encryption_configuration
    try:
        resp = await client.call("CreateSecurityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create security configuration") from exc
    return CreateSecurityConfigurationResult(
        name=resp.get("Name"),
        created_timestamp=resp.get("CreatedTimestamp"),
    )


async def create_session(
    id: str,
    role: str,
    command: dict[str, Any],
    *,
    description: str | None = None,
    timeout: int | None = None,
    idle_timeout: int | None = None,
    default_arguments: dict[str, Any] | None = None,
    connections: dict[str, Any] | None = None,
    max_capacity: float | None = None,
    number_of_workers: int | None = None,
    worker_type: str | None = None,
    security_configuration: str | None = None,
    glue_version: str | None = None,
    tags: dict[str, Any] | None = None,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> CreateSessionResult:
    """Create session.

    Args:
        id: Id.
        role: Role.
        command: Command.
        description: Description.
        timeout: Timeout.
        idle_timeout: Idle timeout.
        default_arguments: Default arguments.
        connections: Connections.
        max_capacity: Max capacity.
        number_of_workers: Number of workers.
        worker_type: Worker type.
        security_configuration: Security configuration.
        glue_version: Glue version.
        tags: Tags.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    kwargs["Role"] = role
    kwargs["Command"] = command
    if description is not None:
        kwargs["Description"] = description
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if idle_timeout is not None:
        kwargs["IdleTimeout"] = idle_timeout
    if default_arguments is not None:
        kwargs["DefaultArguments"] = default_arguments
    if connections is not None:
        kwargs["Connections"] = connections
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if worker_type is not None:
        kwargs["WorkerType"] = worker_type
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    if glue_version is not None:
        kwargs["GlueVersion"] = glue_version
    if tags is not None:
        kwargs["Tags"] = tags
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("CreateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create session") from exc
    return CreateSessionResult(
        session=resp.get("Session"),
    )


async def create_table(
    database_name: str,
    *,
    catalog_id: str | None = None,
    name: str | None = None,
    table_input: dict[str, Any] | None = None,
    partition_indexes: list[dict[str, Any]] | None = None,
    transaction_id: str | None = None,
    open_table_format_input: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create table.

    Args:
        database_name: Database name.
        catalog_id: Catalog id.
        name: Name.
        table_input: Table input.
        partition_indexes: Partition indexes.
        transaction_id: Transaction id.
        open_table_format_input: Open table format input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if name is not None:
        kwargs["Name"] = name
    if table_input is not None:
        kwargs["TableInput"] = table_input
    if partition_indexes is not None:
        kwargs["PartitionIndexes"] = partition_indexes
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    if open_table_format_input is not None:
        kwargs["OpenTableFormatInput"] = open_table_format_input
    try:
        await client.call("CreateTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create table") from exc
    return None


async def create_table_optimizer(
    catalog_id: str,
    database_name: str,
    table_name: str,
    type_value: str,
    table_optimizer_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create table optimizer.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        type_value: Type value.
        table_optimizer_configuration: Table optimizer configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Type"] = type_value
    kwargs["TableOptimizerConfiguration"] = table_optimizer_configuration
    try:
        await client.call("CreateTableOptimizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create table optimizer") from exc
    return None


async def create_trigger(
    name: str,
    type_value: str,
    actions: list[dict[str, Any]],
    *,
    workflow_name: str | None = None,
    schedule: str | None = None,
    predicate: dict[str, Any] | None = None,
    description: str | None = None,
    start_on_creation: bool | None = None,
    tags: dict[str, Any] | None = None,
    event_batching_condition: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTriggerResult:
    """Create trigger.

    Args:
        name: Name.
        type_value: Type value.
        actions: Actions.
        workflow_name: Workflow name.
        schedule: Schedule.
        predicate: Predicate.
        description: Description.
        start_on_creation: Start on creation.
        tags: Tags.
        event_batching_condition: Event batching condition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    kwargs["Actions"] = actions
    if workflow_name is not None:
        kwargs["WorkflowName"] = workflow_name
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if predicate is not None:
        kwargs["Predicate"] = predicate
    if description is not None:
        kwargs["Description"] = description
    if start_on_creation is not None:
        kwargs["StartOnCreation"] = start_on_creation
    if tags is not None:
        kwargs["Tags"] = tags
    if event_batching_condition is not None:
        kwargs["EventBatchingCondition"] = event_batching_condition
    try:
        resp = await client.call("CreateTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create trigger") from exc
    return CreateTriggerResult(
        name=resp.get("Name"),
    )


async def create_usage_profile(
    name: str,
    configuration: dict[str, Any],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUsageProfileResult:
    """Create usage profile.

    Args:
        name: Name.
        configuration: Configuration.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Configuration"] = configuration
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateUsageProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create usage profile") from exc
    return CreateUsageProfileResult(
        name=resp.get("Name"),
    )


async def create_user_defined_function(
    database_name: str,
    function_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create user defined function.

    Args:
        database_name: Database name.
        function_input: Function input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["FunctionInput"] = function_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("CreateUserDefinedFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create user defined function") from exc
    return None


async def create_workflow(
    name: str,
    *,
    description: str | None = None,
    default_run_properties: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    max_concurrent_runs: int | None = None,
    region_name: str | None = None,
) -> CreateWorkflowResult:
    """Create workflow.

    Args:
        name: Name.
        description: Description.
        default_run_properties: Default run properties.
        tags: Tags.
        max_concurrent_runs: Max concurrent runs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if default_run_properties is not None:
        kwargs["DefaultRunProperties"] = default_run_properties
    if tags is not None:
        kwargs["Tags"] = tags
    if max_concurrent_runs is not None:
        kwargs["MaxConcurrentRuns"] = max_concurrent_runs
    try:
        resp = await client.call("CreateWorkflow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create workflow") from exc
    return CreateWorkflowResult(
        name=resp.get("Name"),
    )


async def delete_blueprint(
    name: str,
    region_name: str | None = None,
) -> DeleteBlueprintResult:
    """Delete blueprint.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteBlueprint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete blueprint") from exc
    return DeleteBlueprintResult(
        name=resp.get("Name"),
    )


async def delete_catalog(
    catalog_id: str,
    region_name: str | None = None,
) -> None:
    """Delete catalog.

    Args:
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete catalog") from exc
    return None


async def delete_classifier(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete classifier.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteClassifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete classifier") from exc
    return None


async def delete_column_statistics_for_partition(
    database_name: str,
    table_name: str,
    partition_values: list[str],
    column_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete column statistics for partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        column_name: Column name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    kwargs["ColumnName"] = column_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteColumnStatisticsForPartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete column statistics for partition") from exc
    return None


async def delete_column_statistics_for_table(
    database_name: str,
    table_name: str,
    column_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete column statistics for table.

    Args:
        database_name: Database name.
        table_name: Table name.
        column_name: Column name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["ColumnName"] = column_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteColumnStatisticsForTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete column statistics for table") from exc
    return None


async def delete_column_statistics_task_settings(
    database_name: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Delete column statistics task settings.

    Args:
        database_name: Database name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    try:
        await client.call("DeleteColumnStatisticsTaskSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete column statistics task settings") from exc
    return None


async def delete_connection(
    connection_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete connection.

    Args:
        connection_name: Connection name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionName"] = connection_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return None


async def delete_crawler(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete crawler.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete crawler") from exc
    return None


async def delete_custom_entity_type(
    name: str,
    region_name: str | None = None,
) -> DeleteCustomEntityTypeResult:
    """Delete custom entity type.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteCustomEntityType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom entity type") from exc
    return DeleteCustomEntityTypeResult(
        name=resp.get("Name"),
    )


async def delete_data_quality_ruleset(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete data quality ruleset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteDataQualityRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data quality ruleset") from exc
    return None


async def delete_database(
    name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete database.

    Args:
        name: Name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete database") from exc
    return None


async def delete_dev_endpoint(
    endpoint_name: str,
    region_name: str | None = None,
) -> None:
    """Delete dev endpoint.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    try:
        await client.call("DeleteDevEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dev endpoint") from exc
    return None


async def delete_glue_identity_center_configuration(
    region_name: str | None = None,
) -> None:
    """Delete glue identity center configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DeleteGlueIdentityCenterConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete glue identity center configuration") from exc
    return None


async def delete_integration(
    integration_identifier: str,
    region_name: str | None = None,
) -> DeleteIntegrationResult:
    """Delete integration.

    Args:
        integration_identifier: Integration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationIdentifier"] = integration_identifier
    try:
        resp = await client.call("DeleteIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete integration") from exc
    return DeleteIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        description=resp.get("Description"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KmsKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
        status=resp.get("Status"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
        data_filter=resp.get("DataFilter"),
    )


async def delete_integration_table_properties(
    resource_arn: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Delete integration table properties.

    Args:
        resource_arn: Resource arn.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TableName"] = table_name
    try:
        await client.call("DeleteIntegrationTableProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete integration table properties") from exc
    return None


async def delete_job(
    job_name: str,
    region_name: str | None = None,
) -> DeleteJobResult:
    """Delete job.

    Args:
        job_name: Job name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    try:
        resp = await client.call("DeleteJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete job") from exc
    return DeleteJobResult(
        job_name=resp.get("JobName"),
    )


async def delete_ml_transform(
    transform_id: str,
    region_name: str | None = None,
) -> DeleteMlTransformResult:
    """Delete ml transform.

    Args:
        transform_id: Transform id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    try:
        resp = await client.call("DeleteMLTransform", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ml transform") from exc
    return DeleteMlTransformResult(
        transform_id=resp.get("TransformId"),
    )


async def delete_partition(
    database_name: str,
    table_name: str,
    partition_values: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeletePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete partition") from exc
    return None


async def delete_partition_index(
    database_name: str,
    table_name: str,
    index_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete partition index.

    Args:
        database_name: Database name.
        table_name: Table name.
        index_name: Index name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["IndexName"] = index_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeletePartitionIndex", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete partition index") from exc
    return None


async def delete_registry(
    registry_id: dict[str, Any],
    region_name: str | None = None,
) -> DeleteRegistryResult:
    """Delete registry.

    Args:
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegistryId"] = registry_id
    try:
        resp = await client.call("DeleteRegistry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete registry") from exc
    return DeleteRegistryResult(
        registry_name=resp.get("RegistryName"),
        registry_arn=resp.get("RegistryArn"),
        status=resp.get("Status"),
    )


async def delete_resource_policy(
    *,
    policy_hash_condition: str | None = None,
    resource_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        policy_hash_condition: Policy hash condition.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if policy_hash_condition is not None:
        kwargs["PolicyHashCondition"] = policy_hash_condition
    if resource_arn is not None:
        kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def delete_schema(
    schema_id: dict[str, Any],
    region_name: str | None = None,
) -> DeleteSchemaResult:
    """Delete schema.

    Args:
        schema_id: Schema id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    try:
        resp = await client.call("DeleteSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete schema") from exc
    return DeleteSchemaResult(
        schema_arn=resp.get("SchemaArn"),
        schema_name=resp.get("SchemaName"),
        status=resp.get("Status"),
    )


async def delete_schema_versions(
    schema_id: dict[str, Any],
    versions: str,
    region_name: str | None = None,
) -> DeleteSchemaVersionsResult:
    """Delete schema versions.

    Args:
        schema_id: Schema id.
        versions: Versions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    kwargs["Versions"] = versions
    try:
        resp = await client.call("DeleteSchemaVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete schema versions") from exc
    return DeleteSchemaVersionsResult(
        schema_version_errors=resp.get("SchemaVersionErrors"),
    )


async def delete_security_configuration(
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
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteSecurityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete security configuration") from exc
    return None


async def delete_session(
    id: str,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> DeleteSessionResult:
    """Delete session.

    Args:
        id: Id.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("DeleteSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete session") from exc
    return DeleteSessionResult(
        id=resp.get("Id"),
    )


async def delete_table(
    database_name: str,
    name: str,
    *,
    catalog_id: str | None = None,
    transaction_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete table.

    Args:
        database_name: Database name.
        name: Name.
        catalog_id: Catalog id.
        transaction_id: Transaction id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["Name"] = name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    try:
        await client.call("DeleteTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete table") from exc
    return None


async def delete_table_optimizer(
    catalog_id: str,
    database_name: str,
    table_name: str,
    type_value: str,
    region_name: str | None = None,
) -> None:
    """Delete table optimizer.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Type"] = type_value
    try:
        await client.call("DeleteTableOptimizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete table optimizer") from exc
    return None


async def delete_table_version(
    database_name: str,
    table_name: str,
    version_id: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete table version.

    Args:
        database_name: Database name.
        table_name: Table name.
        version_id: Version id.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["VersionId"] = version_id
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteTableVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete table version") from exc
    return None


async def delete_trigger(
    name: str,
    region_name: str | None = None,
) -> DeleteTriggerResult:
    """Delete trigger.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete trigger") from exc
    return DeleteTriggerResult(
        name=resp.get("Name"),
    )


async def delete_usage_profile(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete usage profile.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteUsageProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete usage profile") from exc
    return None


async def delete_user_defined_function(
    database_name: str,
    function_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete user defined function.

    Args:
        database_name: Database name.
        function_name: Function name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["FunctionName"] = function_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("DeleteUserDefinedFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user defined function") from exc
    return None


async def delete_workflow(
    name: str,
    region_name: str | None = None,
) -> DeleteWorkflowResult:
    """Delete workflow.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("DeleteWorkflow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete workflow") from exc
    return DeleteWorkflowResult(
        name=resp.get("Name"),
    )


async def describe_connection_type(
    connection_type: str,
    region_name: str | None = None,
) -> DescribeConnectionTypeResult:
    """Describe connection type.

    Args:
        connection_type: Connection type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionType"] = connection_type
    try:
        resp = await client.call("DescribeConnectionType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe connection type") from exc
    return DescribeConnectionTypeResult(
        connection_type=resp.get("ConnectionType"),
        description=resp.get("Description"),
        capabilities=resp.get("Capabilities"),
        connection_properties=resp.get("ConnectionProperties"),
        connection_options=resp.get("ConnectionOptions"),
        authentication_configuration=resp.get("AuthenticationConfiguration"),
        compute_environment_configurations=resp.get("ComputeEnvironmentConfigurations"),
        physical_connection_requirements=resp.get("PhysicalConnectionRequirements"),
        athena_connection_properties=resp.get("AthenaConnectionProperties"),
        python_connection_properties=resp.get("PythonConnectionProperties"),
        spark_connection_properties=resp.get("SparkConnectionProperties"),
    )


async def describe_entity(
    connection_name: str,
    entity_name: str,
    *,
    catalog_id: str | None = None,
    next_token: str | None = None,
    data_store_api_version: str | None = None,
    region_name: str | None = None,
) -> DescribeEntityResult:
    """Describe entity.

    Args:
        connection_name: Connection name.
        entity_name: Entity name.
        catalog_id: Catalog id.
        next_token: Next token.
        data_store_api_version: Data store api version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectionName"] = connection_name
    kwargs["EntityName"] = entity_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if data_store_api_version is not None:
        kwargs["DataStoreApiVersion"] = data_store_api_version
    try:
        resp = await client.call("DescribeEntity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe entity") from exc
    return DescribeEntityResult(
        fields=resp.get("Fields"),
        next_token=resp.get("NextToken"),
    )


async def describe_inbound_integrations(
    *,
    integration_arn: str | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    target_arn: str | None = None,
    region_name: str | None = None,
) -> DescribeInboundIntegrationsResult:
    """Describe inbound integrations.

    Args:
        integration_arn: Integration arn.
        marker: Marker.
        max_records: Max records.
        target_arn: Target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if integration_arn is not None:
        kwargs["IntegrationArn"] = integration_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    try:
        resp = await client.call("DescribeInboundIntegrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe inbound integrations") from exc
    return DescribeInboundIntegrationsResult(
        inbound_integrations=resp.get("InboundIntegrations"),
        marker=resp.get("Marker"),
    )


async def describe_integrations(
    *,
    integration_identifier: str | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeIntegrationsResult:
    """Describe integrations.

    Args:
        integration_identifier: Integration identifier.
        marker: Marker.
        max_records: Max records.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if integration_identifier is not None:
        kwargs["IntegrationIdentifier"] = integration_identifier
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeIntegrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe integrations") from exc
    return DescribeIntegrationsResult(
        integrations=resp.get("Integrations"),
        marker=resp.get("Marker"),
    )


async def get_blueprint(
    name: str,
    *,
    include_blueprint: bool | None = None,
    include_parameter_spec: bool | None = None,
    region_name: str | None = None,
) -> GetBlueprintResult:
    """Get blueprint.

    Args:
        name: Name.
        include_blueprint: Include blueprint.
        include_parameter_spec: Include parameter spec.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if include_blueprint is not None:
        kwargs["IncludeBlueprint"] = include_blueprint
    if include_parameter_spec is not None:
        kwargs["IncludeParameterSpec"] = include_parameter_spec
    try:
        resp = await client.call("GetBlueprint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get blueprint") from exc
    return GetBlueprintResult(
        blueprint=resp.get("Blueprint"),
    )


async def get_blueprint_run(
    blueprint_name: str,
    run_id: str,
    region_name: str | None = None,
) -> GetBlueprintRunResult:
    """Get blueprint run.

    Args:
        blueprint_name: Blueprint name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueprintName"] = blueprint_name
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("GetBlueprintRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get blueprint run") from exc
    return GetBlueprintRunResult(
        blueprint_run=resp.get("BlueprintRun"),
    )


async def get_blueprint_runs(
    blueprint_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetBlueprintRunsResult:
    """Get blueprint runs.

    Args:
        blueprint_name: Blueprint name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueprintName"] = blueprint_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetBlueprintRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get blueprint runs") from exc
    return GetBlueprintRunsResult(
        blueprint_runs=resp.get("BlueprintRuns"),
        next_token=resp.get("NextToken"),
    )


async def get_catalog(
    catalog_id: str,
    region_name: str | None = None,
) -> GetCatalogResult:
    """Get catalog.

    Args:
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get catalog") from exc
    return GetCatalogResult(
        catalog=resp.get("Catalog"),
    )


async def get_catalog_import_status(
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetCatalogImportStatusResult:
    """Get catalog import status.

    Args:
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetCatalogImportStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get catalog import status") from exc
    return GetCatalogImportStatusResult(
        import_status=resp.get("ImportStatus"),
    )


async def get_catalogs(
    *,
    parent_catalog_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    recursive: bool | None = None,
    include_root: bool | None = None,
    region_name: str | None = None,
) -> GetCatalogsResult:
    """Get catalogs.

    Args:
        parent_catalog_id: Parent catalog id.
        next_token: Next token.
        max_results: Max results.
        recursive: Recursive.
        include_root: Include root.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if parent_catalog_id is not None:
        kwargs["ParentCatalogId"] = parent_catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if recursive is not None:
        kwargs["Recursive"] = recursive
    if include_root is not None:
        kwargs["IncludeRoot"] = include_root
    try:
        resp = await client.call("GetCatalogs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get catalogs") from exc
    return GetCatalogsResult(
        catalog_list=resp.get("CatalogList"),
        next_token=resp.get("NextToken"),
    )


async def get_classifier(
    name: str,
    region_name: str | None = None,
) -> GetClassifierResult:
    """Get classifier.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetClassifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get classifier") from exc
    return GetClassifierResult(
        classifier=resp.get("Classifier"),
    )


async def get_classifiers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetClassifiersResult:
    """Get classifiers.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetClassifiers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get classifiers") from exc
    return GetClassifiersResult(
        classifiers=resp.get("Classifiers"),
        next_token=resp.get("NextToken"),
    )


async def get_column_statistics_for_partition(
    database_name: str,
    table_name: str,
    partition_values: list[str],
    column_names: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetColumnStatisticsForPartitionResult:
    """Get column statistics for partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        column_names: Column names.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    kwargs["ColumnNames"] = column_names
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetColumnStatisticsForPartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get column statistics for partition") from exc
    return GetColumnStatisticsForPartitionResult(
        column_statistics_list=resp.get("ColumnStatisticsList"),
        errors=resp.get("Errors"),
    )


async def get_column_statistics_for_table(
    database_name: str,
    table_name: str,
    column_names: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetColumnStatisticsForTableResult:
    """Get column statistics for table.

    Args:
        database_name: Database name.
        table_name: Table name.
        column_names: Column names.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["ColumnNames"] = column_names
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetColumnStatisticsForTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get column statistics for table") from exc
    return GetColumnStatisticsForTableResult(
        column_statistics_list=resp.get("ColumnStatisticsList"),
        errors=resp.get("Errors"),
    )


async def get_column_statistics_task_run(
    column_statistics_task_run_id: str,
    region_name: str | None = None,
) -> GetColumnStatisticsTaskRunResult:
    """Get column statistics task run.

    Args:
        column_statistics_task_run_id: Column statistics task run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ColumnStatisticsTaskRunId"] = column_statistics_task_run_id
    try:
        resp = await client.call("GetColumnStatisticsTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get column statistics task run") from exc
    return GetColumnStatisticsTaskRunResult(
        column_statistics_task_run=resp.get("ColumnStatisticsTaskRun"),
    )


async def get_column_statistics_task_runs(
    database_name: str,
    table_name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetColumnStatisticsTaskRunsResult:
    """Get column statistics task runs.

    Args:
        database_name: Database name.
        table_name: Table name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetColumnStatisticsTaskRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get column statistics task runs") from exc
    return GetColumnStatisticsTaskRunsResult(
        column_statistics_task_runs=resp.get("ColumnStatisticsTaskRuns"),
        next_token=resp.get("NextToken"),
    )


async def get_column_statistics_task_settings(
    database_name: str,
    table_name: str,
    region_name: str | None = None,
) -> GetColumnStatisticsTaskSettingsResult:
    """Get column statistics task settings.

    Args:
        database_name: Database name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    try:
        resp = await client.call("GetColumnStatisticsTaskSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get column statistics task settings") from exc
    return GetColumnStatisticsTaskSettingsResult(
        column_statistics_task_settings=resp.get("ColumnStatisticsTaskSettings"),
    )


async def get_connection(
    name: str,
    *,
    catalog_id: str | None = None,
    hide_password: bool | None = None,
    apply_override_for_compute_environment: str | None = None,
    region_name: str | None = None,
) -> GetConnectionResult:
    """Get connection.

    Args:
        name: Name.
        catalog_id: Catalog id.
        hide_password: Hide password.
        apply_override_for_compute_environment: Apply override for compute environment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if hide_password is not None:
        kwargs["HidePassword"] = hide_password
    if apply_override_for_compute_environment is not None:
        kwargs["ApplyOverrideForComputeEnvironment"] = apply_override_for_compute_environment
    try:
        resp = await client.call("GetConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connection") from exc
    return GetConnectionResult(
        connection=resp.get("Connection"),
    )


async def get_connections(
    *,
    catalog_id: str | None = None,
    filter: dict[str, Any] | None = None,
    hide_password: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetConnectionsResult:
    """Get connections.

    Args:
        catalog_id: Catalog id.
        filter: Filter.
        hide_password: Hide password.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if filter is not None:
        kwargs["Filter"] = filter
    if hide_password is not None:
        kwargs["HidePassword"] = hide_password
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetConnections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connections") from exc
    return GetConnectionsResult(
        connection_list=resp.get("ConnectionList"),
        next_token=resp.get("NextToken"),
    )


async def get_crawler(
    name: str,
    region_name: str | None = None,
) -> GetCrawlerResult:
    """Get crawler.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get crawler") from exc
    return GetCrawlerResult(
        crawler=resp.get("Crawler"),
    )


async def get_crawler_metrics(
    *,
    crawler_name_list: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetCrawlerMetricsResult:
    """Get crawler metrics.

    Args:
        crawler_name_list: Crawler name list.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if crawler_name_list is not None:
        kwargs["CrawlerNameList"] = crawler_name_list
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetCrawlerMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get crawler metrics") from exc
    return GetCrawlerMetricsResult(
        crawler_metrics_list=resp.get("CrawlerMetricsList"),
        next_token=resp.get("NextToken"),
    )


async def get_crawlers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetCrawlersResult:
    """Get crawlers.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetCrawlers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get crawlers") from exc
    return GetCrawlersResult(
        crawlers=resp.get("Crawlers"),
        next_token=resp.get("NextToken"),
    )


async def get_custom_entity_type(
    name: str,
    region_name: str | None = None,
) -> GetCustomEntityTypeResult:
    """Get custom entity type.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetCustomEntityType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get custom entity type") from exc
    return GetCustomEntityTypeResult(
        name=resp.get("Name"),
        regex_string=resp.get("RegexString"),
        context_words=resp.get("ContextWords"),
    )


async def get_data_catalog_encryption_settings(
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetDataCatalogEncryptionSettingsResult:
    """Get data catalog encryption settings.

    Args:
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetDataCatalogEncryptionSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data catalog encryption settings") from exc
    return GetDataCatalogEncryptionSettingsResult(
        data_catalog_encryption_settings=resp.get("DataCatalogEncryptionSettings"),
    )


async def get_data_quality_model(
    profile_id: str,
    *,
    statistic_id: str | None = None,
    region_name: str | None = None,
) -> GetDataQualityModelResult:
    """Get data quality model.

    Args:
        profile_id: Profile id.
        statistic_id: Statistic id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProfileId"] = profile_id
    if statistic_id is not None:
        kwargs["StatisticId"] = statistic_id
    try:
        resp = await client.call("GetDataQualityModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality model") from exc
    return GetDataQualityModelResult(
        status=resp.get("Status"),
        started_on=resp.get("StartedOn"),
        completed_on=resp.get("CompletedOn"),
        failure_reason=resp.get("FailureReason"),
    )


async def get_data_quality_model_result(
    statistic_id: str,
    profile_id: str,
    region_name: str | None = None,
) -> GetDataQualityModelResultResult:
    """Get data quality model result.

    Args:
        statistic_id: Statistic id.
        profile_id: Profile id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StatisticId"] = statistic_id
    kwargs["ProfileId"] = profile_id
    try:
        resp = await client.call("GetDataQualityModelResult", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality model result") from exc
    return GetDataQualityModelResultResult(
        completed_on=resp.get("CompletedOn"),
        model=resp.get("Model"),
    )


async def get_data_quality_result(
    result_id: str,
    region_name: str | None = None,
) -> GetDataQualityResultResult:
    """Get data quality result.

    Args:
        result_id: Result id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResultId"] = result_id
    try:
        resp = await client.call("GetDataQualityResult", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality result") from exc
    return GetDataQualityResultResult(
        result_id=resp.get("ResultId"),
        profile_id=resp.get("ProfileId"),
        score=resp.get("Score"),
        data_source=resp.get("DataSource"),
        ruleset_name=resp.get("RulesetName"),
        evaluation_context=resp.get("EvaluationContext"),
        started_on=resp.get("StartedOn"),
        completed_on=resp.get("CompletedOn"),
        job_name=resp.get("JobName"),
        job_run_id=resp.get("JobRunId"),
        ruleset_evaluation_run_id=resp.get("RulesetEvaluationRunId"),
        rule_results=resp.get("RuleResults"),
        analyzer_results=resp.get("AnalyzerResults"),
        observations=resp.get("Observations"),
        aggregated_metrics=resp.get("AggregatedMetrics"),
    )


async def get_data_quality_rule_recommendation_run(
    run_id: str,
    region_name: str | None = None,
) -> GetDataQualityRuleRecommendationRunResult:
    """Get data quality rule recommendation run.

    Args:
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("GetDataQualityRuleRecommendationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality rule recommendation run") from exc
    return GetDataQualityRuleRecommendationRunResult(
        run_id=resp.get("RunId"),
        data_source=resp.get("DataSource"),
        role=resp.get("Role"),
        number_of_workers=resp.get("NumberOfWorkers"),
        timeout=resp.get("Timeout"),
        status=resp.get("Status"),
        error_string=resp.get("ErrorString"),
        started_on=resp.get("StartedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
        completed_on=resp.get("CompletedOn"),
        execution_time=resp.get("ExecutionTime"),
        recommended_ruleset=resp.get("RecommendedRuleset"),
        created_ruleset_name=resp.get("CreatedRulesetName"),
        data_quality_security_configuration=resp.get("DataQualitySecurityConfiguration"),
    )


async def get_data_quality_ruleset(
    name: str,
    region_name: str | None = None,
) -> GetDataQualityRulesetResult:
    """Get data quality ruleset.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetDataQualityRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality ruleset") from exc
    return GetDataQualityRulesetResult(
        name=resp.get("Name"),
        description=resp.get("Description"),
        ruleset=resp.get("Ruleset"),
        target_table=resp.get("TargetTable"),
        created_on=resp.get("CreatedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
        recommendation_run_id=resp.get("RecommendationRunId"),
        data_quality_security_configuration=resp.get("DataQualitySecurityConfiguration"),
    )


async def get_data_quality_ruleset_evaluation_run(
    run_id: str,
    region_name: str | None = None,
) -> GetDataQualityRulesetEvaluationRunResult:
    """Get data quality ruleset evaluation run.

    Args:
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("GetDataQualityRulesetEvaluationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data quality ruleset evaluation run") from exc
    return GetDataQualityRulesetEvaluationRunResult(
        run_id=resp.get("RunId"),
        data_source=resp.get("DataSource"),
        role=resp.get("Role"),
        number_of_workers=resp.get("NumberOfWorkers"),
        timeout=resp.get("Timeout"),
        additional_run_options=resp.get("AdditionalRunOptions"),
        status=resp.get("Status"),
        error_string=resp.get("ErrorString"),
        started_on=resp.get("StartedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
        completed_on=resp.get("CompletedOn"),
        execution_time=resp.get("ExecutionTime"),
        ruleset_names=resp.get("RulesetNames"),
        result_ids=resp.get("ResultIds"),
        additional_data_sources=resp.get("AdditionalDataSources"),
    )


async def get_database(
    name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetDatabaseResult:
    """Get database.

    Args:
        name: Name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get database") from exc
    return GetDatabaseResult(
        database=resp.get("Database"),
    )


async def get_databases(
    *,
    catalog_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    resource_share_type: str | None = None,
    attributes_to_get: list[str] | None = None,
    region_name: str | None = None,
) -> GetDatabasesResult:
    """Get databases.

    Args:
        catalog_id: Catalog id.
        next_token: Next token.
        max_results: Max results.
        resource_share_type: Resource share type.
        attributes_to_get: Attributes to get.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if resource_share_type is not None:
        kwargs["ResourceShareType"] = resource_share_type
    if attributes_to_get is not None:
        kwargs["AttributesToGet"] = attributes_to_get
    try:
        resp = await client.call("GetDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get databases") from exc
    return GetDatabasesResult(
        database_list=resp.get("DatabaseList"),
        next_token=resp.get("NextToken"),
    )


async def get_dataflow_graph(
    *,
    python_script: str | None = None,
    region_name: str | None = None,
) -> GetDataflowGraphResult:
    """Get dataflow graph.

    Args:
        python_script: Python script.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if python_script is not None:
        kwargs["PythonScript"] = python_script
    try:
        resp = await client.call("GetDataflowGraph", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dataflow graph") from exc
    return GetDataflowGraphResult(
        dag_nodes=resp.get("DagNodes"),
        dag_edges=resp.get("DagEdges"),
    )


async def get_dev_endpoint(
    endpoint_name: str,
    region_name: str | None = None,
) -> GetDevEndpointResult:
    """Get dev endpoint.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    try:
        resp = await client.call("GetDevEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dev endpoint") from exc
    return GetDevEndpointResult(
        dev_endpoint=resp.get("DevEndpoint"),
    )


async def get_dev_endpoints(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetDevEndpointsResult:
    """Get dev endpoints.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetDevEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get dev endpoints") from exc
    return GetDevEndpointsResult(
        dev_endpoints=resp.get("DevEndpoints"),
        next_token=resp.get("NextToken"),
    )


async def get_entity_records(
    entity_name: str,
    limit: int,
    *,
    connection_name: str | None = None,
    catalog_id: str | None = None,
    next_token: str | None = None,
    data_store_api_version: str | None = None,
    connection_options: dict[str, Any] | None = None,
    filter_predicate: str | None = None,
    order_by: str | None = None,
    selected_fields: list[str] | None = None,
    region_name: str | None = None,
) -> GetEntityRecordsResult:
    """Get entity records.

    Args:
        entity_name: Entity name.
        limit: Limit.
        connection_name: Connection name.
        catalog_id: Catalog id.
        next_token: Next token.
        data_store_api_version: Data store api version.
        connection_options: Connection options.
        filter_predicate: Filter predicate.
        order_by: Order by.
        selected_fields: Selected fields.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EntityName"] = entity_name
    kwargs["Limit"] = limit
    if connection_name is not None:
        kwargs["ConnectionName"] = connection_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if data_store_api_version is not None:
        kwargs["DataStoreApiVersion"] = data_store_api_version
    if connection_options is not None:
        kwargs["ConnectionOptions"] = connection_options
    if filter_predicate is not None:
        kwargs["FilterPredicate"] = filter_predicate
    if order_by is not None:
        kwargs["OrderBy"] = order_by
    if selected_fields is not None:
        kwargs["SelectedFields"] = selected_fields
    try:
        resp = await client.call("GetEntityRecords", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get entity records") from exc
    return GetEntityRecordsResult(
        records=resp.get("Records"),
        next_token=resp.get("NextToken"),
    )


async def get_glue_identity_center_configuration(
    region_name: str | None = None,
) -> GetGlueIdentityCenterConfigurationResult:
    """Get glue identity center configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetGlueIdentityCenterConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get glue identity center configuration") from exc
    return GetGlueIdentityCenterConfigurationResult(
        application_arn=resp.get("ApplicationArn"),
        instance_arn=resp.get("InstanceArn"),
        scopes=resp.get("Scopes"),
        user_background_sessions_enabled=resp.get("UserBackgroundSessionsEnabled"),
    )


async def get_integration_resource_property(
    resource_arn: str,
    region_name: str | None = None,
) -> GetIntegrationResourcePropertyResult:
    """Get integration resource property.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetIntegrationResourceProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get integration resource property") from exc
    return GetIntegrationResourcePropertyResult(
        resource_arn=resp.get("ResourceArn"),
        source_processing_properties=resp.get("SourceProcessingProperties"),
        target_processing_properties=resp.get("TargetProcessingProperties"),
    )


async def get_integration_table_properties(
    resource_arn: str,
    table_name: str,
    region_name: str | None = None,
) -> GetIntegrationTablePropertiesResult:
    """Get integration table properties.

    Args:
        resource_arn: Resource arn.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TableName"] = table_name
    try:
        resp = await client.call("GetIntegrationTableProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get integration table properties") from exc
    return GetIntegrationTablePropertiesResult(
        resource_arn=resp.get("ResourceArn"),
        table_name=resp.get("TableName"),
        source_table_config=resp.get("SourceTableConfig"),
        target_table_config=resp.get("TargetTableConfig"),
    )


async def get_job_bookmark(
    job_name: str,
    *,
    run_id: str | None = None,
    region_name: str | None = None,
) -> GetJobBookmarkResult:
    """Get job bookmark.

    Args:
        job_name: Job name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    if run_id is not None:
        kwargs["RunId"] = run_id
    try:
        resp = await client.call("GetJobBookmark", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get job bookmark") from exc
    return GetJobBookmarkResult(
        job_bookmark_entry=resp.get("JobBookmarkEntry"),
    )


async def get_job_runs(
    job_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetJobRunsResult:
    """Get job runs.

    Args:
        job_name: Job name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetJobRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get job runs") from exc
    return GetJobRunsResult(
        job_runs=resp.get("JobRuns"),
        next_token=resp.get("NextToken"),
    )


async def get_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetJobsResult:
    """Get jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get jobs") from exc
    return GetJobsResult(
        jobs=resp.get("Jobs"),
        next_token=resp.get("NextToken"),
    )


async def get_mapping(
    source: dict[str, Any],
    *,
    sinks: list[dict[str, Any]] | None = None,
    location: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetMappingResult:
    """Get mapping.

    Args:
        source: Source.
        sinks: Sinks.
        location: Location.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Source"] = source
    if sinks is not None:
        kwargs["Sinks"] = sinks
    if location is not None:
        kwargs["Location"] = location
    try:
        resp = await client.call("GetMapping", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get mapping") from exc
    return GetMappingResult(
        mapping=resp.get("Mapping"),
    )


async def get_ml_task_run(
    transform_id: str,
    task_run_id: str,
    region_name: str | None = None,
) -> GetMlTaskRunResult:
    """Get ml task run.

    Args:
        transform_id: Transform id.
        task_run_id: Task run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    kwargs["TaskRunId"] = task_run_id
    try:
        resp = await client.call("GetMLTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ml task run") from exc
    return GetMlTaskRunResult(
        transform_id=resp.get("TransformId"),
        task_run_id=resp.get("TaskRunId"),
        status=resp.get("Status"),
        log_group_name=resp.get("LogGroupName"),
        properties=resp.get("Properties"),
        error_string=resp.get("ErrorString"),
        started_on=resp.get("StartedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
        completed_on=resp.get("CompletedOn"),
        execution_time=resp.get("ExecutionTime"),
    )


async def get_ml_task_runs(
    transform_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    sort: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetMlTaskRunsResult:
    """Get ml task runs.

    Args:
        transform_id: Transform id.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        sort: Sort.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filter is not None:
        kwargs["Filter"] = filter
    if sort is not None:
        kwargs["Sort"] = sort
    try:
        resp = await client.call("GetMLTaskRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ml task runs") from exc
    return GetMlTaskRunsResult(
        task_runs=resp.get("TaskRuns"),
        next_token=resp.get("NextToken"),
    )


async def get_ml_transform(
    transform_id: str,
    region_name: str | None = None,
) -> GetMlTransformResult:
    """Get ml transform.

    Args:
        transform_id: Transform id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    try:
        resp = await client.call("GetMLTransform", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ml transform") from exc
    return GetMlTransformResult(
        transform_id=resp.get("TransformId"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        status=resp.get("Status"),
        created_on=resp.get("CreatedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
        input_record_tables=resp.get("InputRecordTables"),
        parameters=resp.get("Parameters"),
        evaluation_metrics=resp.get("EvaluationMetrics"),
        label_count=resp.get("LabelCount"),
        model_schema=resp.get("Schema"),
        role=resp.get("Role"),
        glue_version=resp.get("GlueVersion"),
        max_capacity=resp.get("MaxCapacity"),
        worker_type=resp.get("WorkerType"),
        number_of_workers=resp.get("NumberOfWorkers"),
        timeout=resp.get("Timeout"),
        max_retries=resp.get("MaxRetries"),
        transform_encryption=resp.get("TransformEncryption"),
    )


async def get_ml_transforms(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    sort: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetMlTransformsResult:
    """Get ml transforms.

    Args:
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        sort: Sort.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filter is not None:
        kwargs["Filter"] = filter
    if sort is not None:
        kwargs["Sort"] = sort
    try:
        resp = await client.call("GetMLTransforms", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ml transforms") from exc
    return GetMlTransformsResult(
        transforms=resp.get("Transforms"),
        next_token=resp.get("NextToken"),
    )


async def get_partition(
    database_name: str,
    table_name: str,
    partition_values: list[str],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetPartitionResult:
    """Get partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetPartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get partition") from exc
    return GetPartitionResult(
        partition=resp.get("Partition"),
    )


async def get_partition_indexes(
    database_name: str,
    table_name: str,
    *,
    catalog_id: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetPartitionIndexesResult:
    """Get partition indexes.

    Args:
        database_name: Database name.
        table_name: Table name.
        catalog_id: Catalog id.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetPartitionIndexes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get partition indexes") from exc
    return GetPartitionIndexesResult(
        partition_index_descriptor_list=resp.get("PartitionIndexDescriptorList"),
        next_token=resp.get("NextToken"),
    )


async def get_partitions(
    database_name: str,
    table_name: str,
    *,
    catalog_id: str | None = None,
    expression: str | None = None,
    next_token: str | None = None,
    segment: dict[str, Any] | None = None,
    max_results: int | None = None,
    exclude_column_schema: bool | None = None,
    transaction_id: str | None = None,
    query_as_of_time: str | None = None,
    region_name: str | None = None,
) -> GetPartitionsResult:
    """Get partitions.

    Args:
        database_name: Database name.
        table_name: Table name.
        catalog_id: Catalog id.
        expression: Expression.
        next_token: Next token.
        segment: Segment.
        max_results: Max results.
        exclude_column_schema: Exclude column schema.
        transaction_id: Transaction id.
        query_as_of_time: Query as of time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if expression is not None:
        kwargs["Expression"] = expression
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if segment is not None:
        kwargs["Segment"] = segment
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if exclude_column_schema is not None:
        kwargs["ExcludeColumnSchema"] = exclude_column_schema
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    if query_as_of_time is not None:
        kwargs["QueryAsOfTime"] = query_as_of_time
    try:
        resp = await client.call("GetPartitions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get partitions") from exc
    return GetPartitionsResult(
        partitions=resp.get("Partitions"),
        next_token=resp.get("NextToken"),
    )


async def get_plan(
    mapping: list[dict[str, Any]],
    source: dict[str, Any],
    *,
    sinks: list[dict[str, Any]] | None = None,
    location: dict[str, Any] | None = None,
    language: str | None = None,
    additional_plan_options_map: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetPlanResult:
    """Get plan.

    Args:
        mapping: Mapping.
        source: Source.
        sinks: Sinks.
        location: Location.
        language: Language.
        additional_plan_options_map: Additional plan options map.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Mapping"] = mapping
    kwargs["Source"] = source
    if sinks is not None:
        kwargs["Sinks"] = sinks
    if location is not None:
        kwargs["Location"] = location
    if language is not None:
        kwargs["Language"] = language
    if additional_plan_options_map is not None:
        kwargs["AdditionalPlanOptionsMap"] = additional_plan_options_map
    try:
        resp = await client.call("GetPlan", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get plan") from exc
    return GetPlanResult(
        python_script=resp.get("PythonScript"),
        scala_code=resp.get("ScalaCode"),
    )


async def get_registry(
    registry_id: dict[str, Any],
    region_name: str | None = None,
) -> GetRegistryResult:
    """Get registry.

    Args:
        registry_id: Registry id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegistryId"] = registry_id
    try:
        resp = await client.call("GetRegistry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get registry") from exc
    return GetRegistryResult(
        registry_name=resp.get("RegistryName"),
        registry_arn=resp.get("RegistryArn"),
        description=resp.get("Description"),
        status=resp.get("Status"),
        created_time=resp.get("CreatedTime"),
        updated_time=resp.get("UpdatedTime"),
    )


async def get_resource_policies(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetResourcePoliciesResult:
    """Get resource policies.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetResourcePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policies") from exc
    return GetResourcePoliciesResult(
        get_resource_policies_response_list=resp.get("GetResourcePoliciesResponseList"),
        next_token=resp.get("NextToken"),
    )


async def get_resource_policy(
    *,
    resource_arn: str | None = None,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if resource_arn is not None:
        kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy_in_json=resp.get("PolicyInJson"),
        policy_hash=resp.get("PolicyHash"),
        create_time=resp.get("CreateTime"),
        update_time=resp.get("UpdateTime"),
    )


async def get_schema(
    schema_id: dict[str, Any],
    region_name: str | None = None,
) -> GetSchemaResult:
    """Get schema.

    Args:
        schema_id: Schema id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    try:
        resp = await client.call("GetSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get schema") from exc
    return GetSchemaResult(
        registry_name=resp.get("RegistryName"),
        registry_arn=resp.get("RegistryArn"),
        schema_name=resp.get("SchemaName"),
        schema_arn=resp.get("SchemaArn"),
        description=resp.get("Description"),
        data_format=resp.get("DataFormat"),
        compatibility=resp.get("Compatibility"),
        schema_checkpoint=resp.get("SchemaCheckpoint"),
        latest_schema_version=resp.get("LatestSchemaVersion"),
        next_schema_version=resp.get("NextSchemaVersion"),
        schema_status=resp.get("SchemaStatus"),
        created_time=resp.get("CreatedTime"),
        updated_time=resp.get("UpdatedTime"),
    )


async def get_schema_by_definition(
    schema_id: dict[str, Any],
    schema_definition: str,
    region_name: str | None = None,
) -> GetSchemaByDefinitionResult:
    """Get schema by definition.

    Args:
        schema_id: Schema id.
        schema_definition: Schema definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    kwargs["SchemaDefinition"] = schema_definition
    try:
        resp = await client.call("GetSchemaByDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get schema by definition") from exc
    return GetSchemaByDefinitionResult(
        schema_version_id=resp.get("SchemaVersionId"),
        schema_arn=resp.get("SchemaArn"),
        data_format=resp.get("DataFormat"),
        status=resp.get("Status"),
        created_time=resp.get("CreatedTime"),
    )


async def get_schema_version(
    *,
    schema_id: dict[str, Any] | None = None,
    schema_version_id: str | None = None,
    schema_version_number: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetSchemaVersionResult:
    """Get schema version.

    Args:
        schema_id: Schema id.
        schema_version_id: Schema version id.
        schema_version_number: Schema version number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if schema_id is not None:
        kwargs["SchemaId"] = schema_id
    if schema_version_id is not None:
        kwargs["SchemaVersionId"] = schema_version_id
    if schema_version_number is not None:
        kwargs["SchemaVersionNumber"] = schema_version_number
    try:
        resp = await client.call("GetSchemaVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get schema version") from exc
    return GetSchemaVersionResult(
        schema_version_id=resp.get("SchemaVersionId"),
        schema_definition=resp.get("SchemaDefinition"),
        data_format=resp.get("DataFormat"),
        schema_arn=resp.get("SchemaArn"),
        version_number=resp.get("VersionNumber"),
        status=resp.get("Status"),
        created_time=resp.get("CreatedTime"),
    )


async def get_schema_versions_diff(
    schema_id: dict[str, Any],
    first_schema_version_number: dict[str, Any],
    second_schema_version_number: dict[str, Any],
    schema_diff_type: str,
    region_name: str | None = None,
) -> GetSchemaVersionsDiffResult:
    """Get schema versions diff.

    Args:
        schema_id: Schema id.
        first_schema_version_number: First schema version number.
        second_schema_version_number: Second schema version number.
        schema_diff_type: Schema diff type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    kwargs["FirstSchemaVersionNumber"] = first_schema_version_number
    kwargs["SecondSchemaVersionNumber"] = second_schema_version_number
    kwargs["SchemaDiffType"] = schema_diff_type
    try:
        resp = await client.call("GetSchemaVersionsDiff", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get schema versions diff") from exc
    return GetSchemaVersionsDiffResult(
        diff=resp.get("Diff"),
    )


async def get_security_configuration(
    name: str,
    region_name: str | None = None,
) -> GetSecurityConfigurationResult:
    """Get security configuration.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetSecurityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get security configuration") from exc
    return GetSecurityConfigurationResult(
        security_configuration=resp.get("SecurityConfiguration"),
    )


async def get_security_configurations(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetSecurityConfigurationsResult:
    """Get security configurations.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetSecurityConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get security configurations") from exc
    return GetSecurityConfigurationsResult(
        security_configurations=resp.get("SecurityConfigurations"),
        next_token=resp.get("NextToken"),
    )


async def get_session(
    id: str,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> GetSessionResult:
    """Get session.

    Args:
        id: Id.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("GetSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get session") from exc
    return GetSessionResult(
        session=resp.get("Session"),
    )


async def get_statement(
    session_id: str,
    id: int,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> GetStatementResult:
    """Get statement.

    Args:
        session_id: Session id.
        id: Id.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    kwargs["Id"] = id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("GetStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get statement") from exc
    return GetStatementResult(
        statement=resp.get("Statement"),
    )


async def get_table(
    database_name: str,
    name: str,
    *,
    catalog_id: str | None = None,
    transaction_id: str | None = None,
    query_as_of_time: str | None = None,
    audit_context: dict[str, Any] | None = None,
    include_status_details: bool | None = None,
    region_name: str | None = None,
) -> GetTableResult:
    """Get table.

    Args:
        database_name: Database name.
        name: Name.
        catalog_id: Catalog id.
        transaction_id: Transaction id.
        query_as_of_time: Query as of time.
        audit_context: Audit context.
        include_status_details: Include status details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["Name"] = name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    if query_as_of_time is not None:
        kwargs["QueryAsOfTime"] = query_as_of_time
    if audit_context is not None:
        kwargs["AuditContext"] = audit_context
    if include_status_details is not None:
        kwargs["IncludeStatusDetails"] = include_status_details
    try:
        resp = await client.call("GetTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table") from exc
    return GetTableResult(
        table=resp.get("Table"),
    )


async def get_table_optimizer(
    catalog_id: str,
    database_name: str,
    table_name: str,
    type_value: str,
    region_name: str | None = None,
) -> GetTableOptimizerResult:
    """Get table optimizer.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Type"] = type_value
    try:
        resp = await client.call("GetTableOptimizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table optimizer") from exc
    return GetTableOptimizerResult(
        catalog_id=resp.get("CatalogId"),
        database_name=resp.get("DatabaseName"),
        table_name=resp.get("TableName"),
        table_optimizer=resp.get("TableOptimizer"),
    )


async def get_table_version(
    database_name: str,
    table_name: str,
    *,
    catalog_id: str | None = None,
    version_id: str | None = None,
    region_name: str | None = None,
) -> GetTableVersionResult:
    """Get table version.

    Args:
        database_name: Database name.
        table_name: Table name.
        catalog_id: Catalog id.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if version_id is not None:
        kwargs["VersionId"] = version_id
    try:
        resp = await client.call("GetTableVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table version") from exc
    return GetTableVersionResult(
        table_version=resp.get("TableVersion"),
    )


async def get_table_versions(
    database_name: str,
    table_name: str,
    *,
    catalog_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetTableVersionsResult:
    """Get table versions.

    Args:
        database_name: Database name.
        table_name: Table name.
        catalog_id: Catalog id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetTableVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table versions") from exc
    return GetTableVersionsResult(
        table_versions=resp.get("TableVersions"),
        next_token=resp.get("NextToken"),
    )


async def get_tables(
    database_name: str,
    *,
    catalog_id: str | None = None,
    expression: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    transaction_id: str | None = None,
    query_as_of_time: str | None = None,
    audit_context: dict[str, Any] | None = None,
    include_status_details: bool | None = None,
    attributes_to_get: list[str] | None = None,
    region_name: str | None = None,
) -> GetTablesResult:
    """Get tables.

    Args:
        database_name: Database name.
        catalog_id: Catalog id.
        expression: Expression.
        next_token: Next token.
        max_results: Max results.
        transaction_id: Transaction id.
        query_as_of_time: Query as of time.
        audit_context: Audit context.
        include_status_details: Include status details.
        attributes_to_get: Attributes to get.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if expression is not None:
        kwargs["Expression"] = expression
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    if query_as_of_time is not None:
        kwargs["QueryAsOfTime"] = query_as_of_time
    if audit_context is not None:
        kwargs["AuditContext"] = audit_context
    if include_status_details is not None:
        kwargs["IncludeStatusDetails"] = include_status_details
    if attributes_to_get is not None:
        kwargs["AttributesToGet"] = attributes_to_get
    try:
        resp = await client.call("GetTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get tables") from exc
    return GetTablesResult(
        table_list=resp.get("TableList"),
        next_token=resp.get("NextToken"),
    )


async def get_tags(
    resource_arn: str,
    region_name: str | None = None,
) -> GetTagsResult:
    """Get tags.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get tags") from exc
    return GetTagsResult(
        tags=resp.get("Tags"),
    )


async def get_trigger(
    name: str,
    region_name: str | None = None,
) -> GetTriggerResult:
    """Get trigger.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get trigger") from exc
    return GetTriggerResult(
        trigger=resp.get("Trigger"),
    )


async def get_triggers(
    *,
    next_token: str | None = None,
    dependent_job_name: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetTriggersResult:
    """Get triggers.

    Args:
        next_token: Next token.
        dependent_job_name: Dependent job name.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if dependent_job_name is not None:
        kwargs["DependentJobName"] = dependent_job_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get triggers") from exc
    return GetTriggersResult(
        triggers=resp.get("Triggers"),
        next_token=resp.get("NextToken"),
    )


async def get_unfiltered_partition_metadata(
    catalog_id: str,
    database_name: str,
    table_name: str,
    partition_values: list[str],
    supported_permission_types: list[str],
    *,
    region: str | None = None,
    audit_context: dict[str, Any] | None = None,
    query_session_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetUnfilteredPartitionMetadataResult:
    """Get unfiltered partition metadata.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        supported_permission_types: Supported permission types.
        region: Region.
        audit_context: Audit context.
        query_session_context: Query session context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    kwargs["SupportedPermissionTypes"] = supported_permission_types
    if region is not None:
        kwargs["Region"] = region
    if audit_context is not None:
        kwargs["AuditContext"] = audit_context
    if query_session_context is not None:
        kwargs["QuerySessionContext"] = query_session_context
    try:
        resp = await client.call("GetUnfilteredPartitionMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get unfiltered partition metadata") from exc
    return GetUnfilteredPartitionMetadataResult(
        partition=resp.get("Partition"),
        authorized_columns=resp.get("AuthorizedColumns"),
        is_registered_with_lake_formation=resp.get("IsRegisteredWithLakeFormation"),
    )


async def get_unfiltered_partitions_metadata(
    catalog_id: str,
    database_name: str,
    table_name: str,
    supported_permission_types: list[str],
    *,
    region: str | None = None,
    expression: str | None = None,
    audit_context: dict[str, Any] | None = None,
    next_token: str | None = None,
    segment: dict[str, Any] | None = None,
    max_results: int | None = None,
    query_session_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetUnfilteredPartitionsMetadataResult:
    """Get unfiltered partitions metadata.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        supported_permission_types: Supported permission types.
        region: Region.
        expression: Expression.
        audit_context: Audit context.
        next_token: Next token.
        segment: Segment.
        max_results: Max results.
        query_session_context: Query session context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["SupportedPermissionTypes"] = supported_permission_types
    if region is not None:
        kwargs["Region"] = region
    if expression is not None:
        kwargs["Expression"] = expression
    if audit_context is not None:
        kwargs["AuditContext"] = audit_context
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if segment is not None:
        kwargs["Segment"] = segment
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if query_session_context is not None:
        kwargs["QuerySessionContext"] = query_session_context
    try:
        resp = await client.call("GetUnfilteredPartitionsMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get unfiltered partitions metadata") from exc
    return GetUnfilteredPartitionsMetadataResult(
        unfiltered_partitions=resp.get("UnfilteredPartitions"),
        next_token=resp.get("NextToken"),
    )


async def get_unfiltered_table_metadata(
    catalog_id: str,
    database_name: str,
    name: str,
    supported_permission_types: list[str],
    *,
    region: str | None = None,
    audit_context: dict[str, Any] | None = None,
    parent_resource_arn: str | None = None,
    root_resource_arn: str | None = None,
    supported_dialect: dict[str, Any] | None = None,
    permissions: list[str] | None = None,
    query_session_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetUnfilteredTableMetadataResult:
    """Get unfiltered table metadata.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        name: Name.
        supported_permission_types: Supported permission types.
        region: Region.
        audit_context: Audit context.
        parent_resource_arn: Parent resource arn.
        root_resource_arn: Root resource arn.
        supported_dialect: Supported dialect.
        permissions: Permissions.
        query_session_context: Query session context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["Name"] = name
    kwargs["SupportedPermissionTypes"] = supported_permission_types
    if region is not None:
        kwargs["Region"] = region
    if audit_context is not None:
        kwargs["AuditContext"] = audit_context
    if parent_resource_arn is not None:
        kwargs["ParentResourceArn"] = parent_resource_arn
    if root_resource_arn is not None:
        kwargs["RootResourceArn"] = root_resource_arn
    if supported_dialect is not None:
        kwargs["SupportedDialect"] = supported_dialect
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if query_session_context is not None:
        kwargs["QuerySessionContext"] = query_session_context
    try:
        resp = await client.call("GetUnfilteredTableMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get unfiltered table metadata") from exc
    return GetUnfilteredTableMetadataResult(
        table=resp.get("Table"),
        authorized_columns=resp.get("AuthorizedColumns"),
        is_registered_with_lake_formation=resp.get("IsRegisteredWithLakeFormation"),
        cell_filters=resp.get("CellFilters"),
        query_authorization_id=resp.get("QueryAuthorizationId"),
        is_multi_dialect_view=resp.get("IsMultiDialectView"),
        resource_arn=resp.get("ResourceArn"),
        is_protected=resp.get("IsProtected"),
        permissions=resp.get("Permissions"),
        row_filter=resp.get("RowFilter"),
    )


async def get_usage_profile(
    name: str,
    region_name: str | None = None,
) -> GetUsageProfileResult:
    """Get usage profile.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetUsageProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get usage profile") from exc
    return GetUsageProfileResult(
        name=resp.get("Name"),
        description=resp.get("Description"),
        configuration=resp.get("Configuration"),
        created_on=resp.get("CreatedOn"),
        last_modified_on=resp.get("LastModifiedOn"),
    )


async def get_user_defined_function(
    database_name: str,
    function_name: str,
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> GetUserDefinedFunctionResult:
    """Get user defined function.

    Args:
        database_name: Database name.
        function_name: Function name.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["FunctionName"] = function_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("GetUserDefinedFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get user defined function") from exc
    return GetUserDefinedFunctionResult(
        user_defined_function=resp.get("UserDefinedFunction"),
    )


async def get_user_defined_functions(
    pattern: str,
    *,
    catalog_id: str | None = None,
    database_name: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetUserDefinedFunctionsResult:
    """Get user defined functions.

    Args:
        pattern: Pattern.
        catalog_id: Catalog id.
        database_name: Database name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Pattern"] = pattern
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetUserDefinedFunctions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get user defined functions") from exc
    return GetUserDefinedFunctionsResult(
        user_defined_functions=resp.get("UserDefinedFunctions"),
        next_token=resp.get("NextToken"),
    )


async def get_workflow(
    name: str,
    *,
    include_graph: bool | None = None,
    region_name: str | None = None,
) -> GetWorkflowResult:
    """Get workflow.

    Args:
        name: Name.
        include_graph: Include graph.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if include_graph is not None:
        kwargs["IncludeGraph"] = include_graph
    try:
        resp = await client.call("GetWorkflow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get workflow") from exc
    return GetWorkflowResult(
        workflow=resp.get("Workflow"),
    )


async def get_workflow_run(
    name: str,
    run_id: str,
    *,
    include_graph: bool | None = None,
    region_name: str | None = None,
) -> GetWorkflowRunResult:
    """Get workflow run.

    Args:
        name: Name.
        run_id: Run id.
        include_graph: Include graph.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    if include_graph is not None:
        kwargs["IncludeGraph"] = include_graph
    try:
        resp = await client.call("GetWorkflowRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get workflow run") from exc
    return GetWorkflowRunResult(
        run=resp.get("Run"),
    )


async def get_workflow_run_properties(
    name: str,
    run_id: str,
    region_name: str | None = None,
) -> GetWorkflowRunPropertiesResult:
    """Get workflow run properties.

    Args:
        name: Name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        resp = await client.call("GetWorkflowRunProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get workflow run properties") from exc
    return GetWorkflowRunPropertiesResult(
        run_properties=resp.get("RunProperties"),
    )


async def get_workflow_runs(
    name: str,
    *,
    include_graph: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetWorkflowRunsResult:
    """Get workflow runs.

    Args:
        name: Name.
        include_graph: Include graph.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if include_graph is not None:
        kwargs["IncludeGraph"] = include_graph
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetWorkflowRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get workflow runs") from exc
    return GetWorkflowRunsResult(
        runs=resp.get("Runs"),
        next_token=resp.get("NextToken"),
    )


async def import_catalog_to_glue(
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Import catalog to glue.

    Args:
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("ImportCatalogToGlue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import catalog to glue") from exc
    return None


async def list_blueprints(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListBlueprintsResult:
    """List blueprints.

    Args:
        next_token: Next token.
        max_results: Max results.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListBlueprints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list blueprints") from exc
    return ListBlueprintsResult(
        blueprints=resp.get("Blueprints"),
        next_token=resp.get("NextToken"),
    )


async def list_column_statistics_task_runs(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListColumnStatisticsTaskRunsResult:
    """List column statistics task runs.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListColumnStatisticsTaskRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list column statistics task runs") from exc
    return ListColumnStatisticsTaskRunsResult(
        column_statistics_task_run_ids=resp.get("ColumnStatisticsTaskRunIds"),
        next_token=resp.get("NextToken"),
    )


async def list_connection_types(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConnectionTypesResult:
    """List connection types.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListConnectionTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list connection types") from exc
    return ListConnectionTypesResult(
        connection_types=resp.get("ConnectionTypes"),
        next_token=resp.get("NextToken"),
    )


async def list_crawlers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListCrawlersResult:
    """List crawlers.

    Args:
        max_results: Max results.
        next_token: Next token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListCrawlers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list crawlers") from exc
    return ListCrawlersResult(
        crawler_names=resp.get("CrawlerNames"),
        next_token=resp.get("NextToken"),
    )


async def list_crawls(
    crawler_name: str,
    *,
    max_results: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCrawlsResult:
    """List crawls.

    Args:
        crawler_name: Crawler name.
        max_results: Max results.
        filters: Filters.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CrawlerName"] = crawler_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListCrawls", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list crawls") from exc
    return ListCrawlsResult(
        crawls=resp.get("Crawls"),
        next_token=resp.get("NextToken"),
    )


async def list_custom_entity_types(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListCustomEntityTypesResult:
    """List custom entity types.

    Args:
        next_token: Next token.
        max_results: Max results.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListCustomEntityTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom entity types") from exc
    return ListCustomEntityTypesResult(
        custom_entity_types=resp.get("CustomEntityTypes"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_results(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDataQualityResultsResult:
    """List data quality results.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDataQualityResults", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality results") from exc
    return ListDataQualityResultsResult(
        results=resp.get("Results"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_rule_recommendation_runs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDataQualityRuleRecommendationRunsResult:
    """List data quality rule recommendation runs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDataQualityRuleRecommendationRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality rule recommendation runs") from exc
    return ListDataQualityRuleRecommendationRunsResult(
        runs=resp.get("Runs"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_ruleset_evaluation_runs(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDataQualityRulesetEvaluationRunsResult:
    """List data quality ruleset evaluation runs.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDataQualityRulesetEvaluationRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality ruleset evaluation runs") from exc
    return ListDataQualityRulesetEvaluationRunsResult(
        runs=resp.get("Runs"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_rulesets(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListDataQualityRulesetsResult:
    """List data quality rulesets.

    Args:
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filter is not None:
        kwargs["Filter"] = filter
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListDataQualityRulesets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality rulesets") from exc
    return ListDataQualityRulesetsResult(
        rulesets=resp.get("Rulesets"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_statistic_annotations(
    *,
    statistic_id: str | None = None,
    profile_id: str | None = None,
    timestamp_filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDataQualityStatisticAnnotationsResult:
    """List data quality statistic annotations.

    Args:
        statistic_id: Statistic id.
        profile_id: Profile id.
        timestamp_filter: Timestamp filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if statistic_id is not None:
        kwargs["StatisticId"] = statistic_id
    if profile_id is not None:
        kwargs["ProfileId"] = profile_id
    if timestamp_filter is not None:
        kwargs["TimestampFilter"] = timestamp_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListDataQualityStatisticAnnotations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality statistic annotations") from exc
    return ListDataQualityStatisticAnnotationsResult(
        annotations=resp.get("Annotations"),
        next_token=resp.get("NextToken"),
    )


async def list_data_quality_statistics(
    *,
    statistic_id: str | None = None,
    profile_id: str | None = None,
    timestamp_filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDataQualityStatisticsResult:
    """List data quality statistics.

    Args:
        statistic_id: Statistic id.
        profile_id: Profile id.
        timestamp_filter: Timestamp filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if statistic_id is not None:
        kwargs["StatisticId"] = statistic_id
    if profile_id is not None:
        kwargs["ProfileId"] = profile_id
    if timestamp_filter is not None:
        kwargs["TimestampFilter"] = timestamp_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListDataQualityStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data quality statistics") from exc
    return ListDataQualityStatisticsResult(
        statistics=resp.get("Statistics"),
        next_token=resp.get("NextToken"),
    )


async def list_dev_endpoints(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListDevEndpointsResult:
    """List dev endpoints.

    Args:
        next_token: Next token.
        max_results: Max results.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListDevEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dev endpoints") from exc
    return ListDevEndpointsResult(
        dev_endpoint_names=resp.get("DevEndpointNames"),
        next_token=resp.get("NextToken"),
    )


async def list_entities(
    *,
    connection_name: str | None = None,
    catalog_id: str | None = None,
    parent_entity_name: str | None = None,
    next_token: str | None = None,
    data_store_api_version: str | None = None,
    region_name: str | None = None,
) -> ListEntitiesResult:
    """List entities.

    Args:
        connection_name: Connection name.
        catalog_id: Catalog id.
        parent_entity_name: Parent entity name.
        next_token: Next token.
        data_store_api_version: Data store api version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if connection_name is not None:
        kwargs["ConnectionName"] = connection_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if parent_entity_name is not None:
        kwargs["ParentEntityName"] = parent_entity_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if data_store_api_version is not None:
        kwargs["DataStoreApiVersion"] = data_store_api_version
    try:
        resp = await client.call("ListEntities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list entities") from exc
    return ListEntitiesResult(
        entities=resp.get("Entities"),
        next_token=resp.get("NextToken"),
    )


async def list_ml_transforms(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: dict[str, Any] | None = None,
    sort: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListMlTransformsResult:
    """List ml transforms.

    Args:
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        sort: Sort.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filter is not None:
        kwargs["Filter"] = filter
    if sort is not None:
        kwargs["Sort"] = sort
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListMLTransforms", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ml transforms") from exc
    return ListMlTransformsResult(
        transform_ids=resp.get("TransformIds"),
        next_token=resp.get("NextToken"),
    )


async def list_registries(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRegistriesResult:
    """List registries.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListRegistries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list registries") from exc
    return ListRegistriesResult(
        registries=resp.get("Registries"),
        next_token=resp.get("NextToken"),
    )


async def list_schema_versions(
    schema_id: dict[str, Any],
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSchemaVersionsResult:
    """List schema versions.

    Args:
        schema_id: Schema id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSchemaVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list schema versions") from exc
    return ListSchemaVersionsResult(
        schemas=resp.get("Schemas"),
        next_token=resp.get("NextToken"),
    )


async def list_schemas(
    *,
    registry_id: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSchemasResult:
    """List schemas.

    Args:
        registry_id: Registry id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if registry_id is not None:
        kwargs["RegistryId"] = registry_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list schemas") from exc
    return ListSchemasResult(
        schemas=resp.get("Schemas"),
        next_token=resp.get("NextToken"),
    )


async def list_sessions(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    tags: dict[str, Any] | None = None,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> ListSessionsResult:
    """List sessions.

    Args:
        next_token: Next token.
        max_results: Max results.
        tags: Tags.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if tags is not None:
        kwargs["Tags"] = tags
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("ListSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sessions") from exc
    return ListSessionsResult(
        ids=resp.get("Ids"),
        sessions=resp.get("Sessions"),
        next_token=resp.get("NextToken"),
    )


async def list_statements(
    session_id: str,
    *,
    request_origin: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListStatementsResult:
    """List statements.

    Args:
        session_id: Session id.
        request_origin: Request origin.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListStatements", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list statements") from exc
    return ListStatementsResult(
        statements=resp.get("Statements"),
        next_token=resp.get("NextToken"),
    )


async def list_table_optimizer_runs(
    catalog_id: str,
    database_name: str,
    table_name: str,
    type_value: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTableOptimizerRunsResult:
    """List table optimizer runs.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        type_value: Type value.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Type"] = type_value
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTableOptimizerRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list table optimizer runs") from exc
    return ListTableOptimizerRunsResult(
        catalog_id=resp.get("CatalogId"),
        database_name=resp.get("DatabaseName"),
        table_name=resp.get("TableName"),
        next_token=resp.get("NextToken"),
        table_optimizer_runs=resp.get("TableOptimizerRuns"),
    )


async def list_triggers(
    *,
    next_token: str | None = None,
    dependent_job_name: str | None = None,
    max_results: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListTriggersResult:
    """List triggers.

    Args:
        next_token: Next token.
        dependent_job_name: Dependent job name.
        max_results: Max results.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if dependent_job_name is not None:
        kwargs["DependentJobName"] = dependent_job_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ListTriggers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list triggers") from exc
    return ListTriggersResult(
        trigger_names=resp.get("TriggerNames"),
        next_token=resp.get("NextToken"),
    )


async def list_usage_profiles(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUsageProfilesResult:
    """List usage profiles.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListUsageProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list usage profiles") from exc
    return ListUsageProfilesResult(
        profiles=resp.get("Profiles"),
        next_token=resp.get("NextToken"),
    )


async def list_workflows(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListWorkflowsResult:
    """List workflows.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListWorkflows", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list workflows") from exc
    return ListWorkflowsResult(
        workflows=resp.get("Workflows"),
        next_token=resp.get("NextToken"),
    )


async def modify_integration(
    integration_identifier: str,
    *,
    description: str | None = None,
    data_filter: str | None = None,
    integration_config: dict[str, Any] | None = None,
    integration_name: str | None = None,
    region_name: str | None = None,
) -> ModifyIntegrationResult:
    """Modify integration.

    Args:
        integration_identifier: Integration identifier.
        description: Description.
        data_filter: Data filter.
        integration_config: Integration config.
        integration_name: Integration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationIdentifier"] = integration_identifier
    if description is not None:
        kwargs["Description"] = description
    if data_filter is not None:
        kwargs["DataFilter"] = data_filter
    if integration_config is not None:
        kwargs["IntegrationConfig"] = integration_config
    if integration_name is not None:
        kwargs["IntegrationName"] = integration_name
    try:
        resp = await client.call("ModifyIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify integration") from exc
    return ModifyIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        description=resp.get("Description"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KmsKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
        status=resp.get("Status"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
        data_filter=resp.get("DataFilter"),
        integration_config=resp.get("IntegrationConfig"),
    )


async def put_data_catalog_encryption_settings(
    data_catalog_encryption_settings: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put data catalog encryption settings.

    Args:
        data_catalog_encryption_settings: Data catalog encryption settings.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataCatalogEncryptionSettings"] = data_catalog_encryption_settings
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("PutDataCatalogEncryptionSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put data catalog encryption settings") from exc
    return None


async def put_data_quality_profile_annotation(
    profile_id: str,
    inclusion_annotation: str,
    region_name: str | None = None,
) -> None:
    """Put data quality profile annotation.

    Args:
        profile_id: Profile id.
        inclusion_annotation: Inclusion annotation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProfileId"] = profile_id
    kwargs["InclusionAnnotation"] = inclusion_annotation
    try:
        await client.call("PutDataQualityProfileAnnotation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put data quality profile annotation") from exc
    return None


async def put_resource_policy(
    policy_in_json: str,
    *,
    resource_arn: str | None = None,
    policy_hash_condition: str | None = None,
    policy_exists_condition: str | None = None,
    enable_hybrid: str | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        policy_in_json: Policy in json.
        resource_arn: Resource arn.
        policy_hash_condition: Policy hash condition.
        policy_exists_condition: Policy exists condition.
        enable_hybrid: Enable hybrid.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyInJson"] = policy_in_json
    if resource_arn is not None:
        kwargs["ResourceArn"] = resource_arn
    if policy_hash_condition is not None:
        kwargs["PolicyHashCondition"] = policy_hash_condition
    if policy_exists_condition is not None:
        kwargs["PolicyExistsCondition"] = policy_exists_condition
    if enable_hybrid is not None:
        kwargs["EnableHybrid"] = enable_hybrid
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        policy_hash=resp.get("PolicyHash"),
    )


async def put_schema_version_metadata(
    metadata_key_value: dict[str, Any],
    *,
    schema_id: dict[str, Any] | None = None,
    schema_version_number: dict[str, Any] | None = None,
    schema_version_id: str | None = None,
    region_name: str | None = None,
) -> PutSchemaVersionMetadataResult:
    """Put schema version metadata.

    Args:
        metadata_key_value: Metadata key value.
        schema_id: Schema id.
        schema_version_number: Schema version number.
        schema_version_id: Schema version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MetadataKeyValue"] = metadata_key_value
    if schema_id is not None:
        kwargs["SchemaId"] = schema_id
    if schema_version_number is not None:
        kwargs["SchemaVersionNumber"] = schema_version_number
    if schema_version_id is not None:
        kwargs["SchemaVersionId"] = schema_version_id
    try:
        resp = await client.call("PutSchemaVersionMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put schema version metadata") from exc
    return PutSchemaVersionMetadataResult(
        schema_arn=resp.get("SchemaArn"),
        schema_name=resp.get("SchemaName"),
        registry_name=resp.get("RegistryName"),
        latest_version=resp.get("LatestVersion"),
        version_number=resp.get("VersionNumber"),
        schema_version_id=resp.get("SchemaVersionId"),
        metadata_key=resp.get("MetadataKey"),
        metadata_value=resp.get("MetadataValue"),
    )


async def put_workflow_run_properties(
    name: str,
    run_id: str,
    run_properties: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put workflow run properties.

    Args:
        name: Name.
        run_id: Run id.
        run_properties: Run properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    kwargs["RunProperties"] = run_properties
    try:
        await client.call("PutWorkflowRunProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put workflow run properties") from exc
    return None


async def query_schema_version_metadata(
    *,
    schema_id: dict[str, Any] | None = None,
    schema_version_number: dict[str, Any] | None = None,
    schema_version_id: str | None = None,
    metadata_list: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> QuerySchemaVersionMetadataResult:
    """Query schema version metadata.

    Args:
        schema_id: Schema id.
        schema_version_number: Schema version number.
        schema_version_id: Schema version id.
        metadata_list: Metadata list.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if schema_id is not None:
        kwargs["SchemaId"] = schema_id
    if schema_version_number is not None:
        kwargs["SchemaVersionNumber"] = schema_version_number
    if schema_version_id is not None:
        kwargs["SchemaVersionId"] = schema_version_id
    if metadata_list is not None:
        kwargs["MetadataList"] = metadata_list
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("QuerySchemaVersionMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to query schema version metadata") from exc
    return QuerySchemaVersionMetadataResult(
        metadata_info_map=resp.get("MetadataInfoMap"),
        schema_version_id=resp.get("SchemaVersionId"),
        next_token=resp.get("NextToken"),
    )


async def register_schema_version(
    schema_id: dict[str, Any],
    schema_definition: str,
    region_name: str | None = None,
) -> RegisterSchemaVersionResult:
    """Register schema version.

    Args:
        schema_id: Schema id.
        schema_definition: Schema definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    kwargs["SchemaDefinition"] = schema_definition
    try:
        resp = await client.call("RegisterSchemaVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register schema version") from exc
    return RegisterSchemaVersionResult(
        schema_version_id=resp.get("SchemaVersionId"),
        version_number=resp.get("VersionNumber"),
        status=resp.get("Status"),
    )


async def remove_schema_version_metadata(
    metadata_key_value: dict[str, Any],
    *,
    schema_id: dict[str, Any] | None = None,
    schema_version_number: dict[str, Any] | None = None,
    schema_version_id: str | None = None,
    region_name: str | None = None,
) -> RemoveSchemaVersionMetadataResult:
    """Remove schema version metadata.

    Args:
        metadata_key_value: Metadata key value.
        schema_id: Schema id.
        schema_version_number: Schema version number.
        schema_version_id: Schema version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MetadataKeyValue"] = metadata_key_value
    if schema_id is not None:
        kwargs["SchemaId"] = schema_id
    if schema_version_number is not None:
        kwargs["SchemaVersionNumber"] = schema_version_number
    if schema_version_id is not None:
        kwargs["SchemaVersionId"] = schema_version_id
    try:
        resp = await client.call("RemoveSchemaVersionMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove schema version metadata") from exc
    return RemoveSchemaVersionMetadataResult(
        schema_arn=resp.get("SchemaArn"),
        schema_name=resp.get("SchemaName"),
        registry_name=resp.get("RegistryName"),
        latest_version=resp.get("LatestVersion"),
        version_number=resp.get("VersionNumber"),
        schema_version_id=resp.get("SchemaVersionId"),
        metadata_key=resp.get("MetadataKey"),
        metadata_value=resp.get("MetadataValue"),
    )


async def reset_job_bookmark(
    job_name: str,
    *,
    run_id: str | None = None,
    region_name: str | None = None,
) -> ResetJobBookmarkResult:
    """Reset job bookmark.

    Args:
        job_name: Job name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    if run_id is not None:
        kwargs["RunId"] = run_id
    try:
        resp = await client.call("ResetJobBookmark", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset job bookmark") from exc
    return ResetJobBookmarkResult(
        job_bookmark_entry=resp.get("JobBookmarkEntry"),
    )


async def resume_workflow_run(
    name: str,
    run_id: str,
    node_ids: list[str],
    region_name: str | None = None,
) -> ResumeWorkflowRunResult:
    """Resume workflow run.

    Args:
        name: Name.
        run_id: Run id.
        node_ids: Node ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    kwargs["NodeIds"] = node_ids
    try:
        resp = await client.call("ResumeWorkflowRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resume workflow run") from exc
    return ResumeWorkflowRunResult(
        run_id=resp.get("RunId"),
        node_ids=resp.get("NodeIds"),
    )


async def run_connection(
    *,
    connection_name: str | None = None,
    catalog_id: str | None = None,
    run_connection_input: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Run connection.

    Args:
        connection_name: Connection name.
        catalog_id: Catalog id.
        run_connection_input: Run connection input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if connection_name is not None:
        kwargs["ConnectionName"] = connection_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if run_connection_input is not None:
        kwargs["TestConnectionInput"] = run_connection_input
    try:
        await client.call("TestConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run connection") from exc
    return None


async def run_statement(
    session_id: str,
    code: str,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> RunStatementResult:
    """Run statement.

    Args:
        session_id: Session id.
        code: Code.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    kwargs["Code"] = code
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("RunStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run statement") from exc
    return RunStatementResult(
        id=resp.get("Id"),
    )


async def search_tables(
    *,
    catalog_id: str | None = None,
    next_token: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    search_text: str | None = None,
    sort_criteria: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    resource_share_type: str | None = None,
    include_status_details: bool | None = None,
    region_name: str | None = None,
) -> SearchTablesResult:
    """Search tables.

    Args:
        catalog_id: Catalog id.
        next_token: Next token.
        filters: Filters.
        search_text: Search text.
        sort_criteria: Sort criteria.
        max_results: Max results.
        resource_share_type: Resource share type.
        include_status_details: Include status details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filters is not None:
        kwargs["Filters"] = filters
    if search_text is not None:
        kwargs["SearchText"] = search_text
    if sort_criteria is not None:
        kwargs["SortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if resource_share_type is not None:
        kwargs["ResourceShareType"] = resource_share_type
    if include_status_details is not None:
        kwargs["IncludeStatusDetails"] = include_status_details
    try:
        resp = await client.call("SearchTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search tables") from exc
    return SearchTablesResult(
        next_token=resp.get("NextToken"),
        table_list=resp.get("TableList"),
    )


async def start_blueprint_run(
    blueprint_name: str,
    role_arn: str,
    *,
    parameters: str | None = None,
    region_name: str | None = None,
) -> StartBlueprintRunResult:
    """Start blueprint run.

    Args:
        blueprint_name: Blueprint name.
        role_arn: Role arn.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueprintName"] = blueprint_name
    kwargs["RoleArn"] = role_arn
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = await client.call("StartBlueprintRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start blueprint run") from exc
    return StartBlueprintRunResult(
        run_id=resp.get("RunId"),
    )


async def start_column_statistics_task_run(
    database_name: str,
    table_name: str,
    role: str,
    *,
    column_name_list: list[str] | None = None,
    sample_size: float | None = None,
    catalog_id: str | None = None,
    security_configuration: str | None = None,
    region_name: str | None = None,
) -> StartColumnStatisticsTaskRunResult:
    """Start column statistics task run.

    Args:
        database_name: Database name.
        table_name: Table name.
        role: Role.
        column_name_list: Column name list.
        sample_size: Sample size.
        catalog_id: Catalog id.
        security_configuration: Security configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Role"] = role
    if column_name_list is not None:
        kwargs["ColumnNameList"] = column_name_list
    if sample_size is not None:
        kwargs["SampleSize"] = sample_size
    if catalog_id is not None:
        kwargs["CatalogID"] = catalog_id
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    try:
        resp = await client.call("StartColumnStatisticsTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start column statistics task run") from exc
    return StartColumnStatisticsTaskRunResult(
        column_statistics_task_run_id=resp.get("ColumnStatisticsTaskRunId"),
    )


async def start_column_statistics_task_run_schedule(
    database_name: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Start column statistics task run schedule.

    Args:
        database_name: Database name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    try:
        await client.call("StartColumnStatisticsTaskRunSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start column statistics task run schedule") from exc
    return None


async def start_crawler(
    name: str,
    region_name: str | None = None,
) -> None:
    """Start crawler.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("StartCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start crawler") from exc
    return None


async def start_crawler_schedule(
    crawler_name: str,
    region_name: str | None = None,
) -> None:
    """Start crawler schedule.

    Args:
        crawler_name: Crawler name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CrawlerName"] = crawler_name
    try:
        await client.call("StartCrawlerSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start crawler schedule") from exc
    return None


async def start_data_quality_rule_recommendation_run(
    data_source: dict[str, Any],
    role: str,
    *,
    number_of_workers: int | None = None,
    timeout: int | None = None,
    created_ruleset_name: str | None = None,
    data_quality_security_configuration: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartDataQualityRuleRecommendationRunResult:
    """Start data quality rule recommendation run.

    Args:
        data_source: Data source.
        role: Role.
        number_of_workers: Number of workers.
        timeout: Timeout.
        created_ruleset_name: Created ruleset name.
        data_quality_security_configuration: Data quality security configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSource"] = data_source
    kwargs["Role"] = role
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if created_ruleset_name is not None:
        kwargs["CreatedRulesetName"] = created_ruleset_name
    if data_quality_security_configuration is not None:
        kwargs["DataQualitySecurityConfiguration"] = data_quality_security_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("StartDataQualityRuleRecommendationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start data quality rule recommendation run") from exc
    return StartDataQualityRuleRecommendationRunResult(
        run_id=resp.get("RunId"),
    )


async def start_data_quality_ruleset_evaluation_run(
    data_source: dict[str, Any],
    role: str,
    ruleset_names: list[str],
    *,
    number_of_workers: int | None = None,
    timeout: int | None = None,
    client_token: str | None = None,
    additional_run_options: dict[str, Any] | None = None,
    additional_data_sources: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartDataQualityRulesetEvaluationRunResult:
    """Start data quality ruleset evaluation run.

    Args:
        data_source: Data source.
        role: Role.
        ruleset_names: Ruleset names.
        number_of_workers: Number of workers.
        timeout: Timeout.
        client_token: Client token.
        additional_run_options: Additional run options.
        additional_data_sources: Additional data sources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSource"] = data_source
    kwargs["Role"] = role
    kwargs["RulesetNames"] = ruleset_names
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if additional_run_options is not None:
        kwargs["AdditionalRunOptions"] = additional_run_options
    if additional_data_sources is not None:
        kwargs["AdditionalDataSources"] = additional_data_sources
    try:
        resp = await client.call("StartDataQualityRulesetEvaluationRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start data quality ruleset evaluation run") from exc
    return StartDataQualityRulesetEvaluationRunResult(
        run_id=resp.get("RunId"),
    )


async def start_export_labels_task_run(
    transform_id: str,
    output_s3_path: str,
    region_name: str | None = None,
) -> StartExportLabelsTaskRunResult:
    """Start export labels task run.

    Args:
        transform_id: Transform id.
        output_s3_path: Output s3 path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    kwargs["OutputS3Path"] = output_s3_path
    try:
        resp = await client.call("StartExportLabelsTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start export labels task run") from exc
    return StartExportLabelsTaskRunResult(
        task_run_id=resp.get("TaskRunId"),
    )


async def start_import_labels_task_run(
    transform_id: str,
    input_s3_path: str,
    *,
    replace_all_labels: bool | None = None,
    region_name: str | None = None,
) -> StartImportLabelsTaskRunResult:
    """Start import labels task run.

    Args:
        transform_id: Transform id.
        input_s3_path: Input s3 path.
        replace_all_labels: Replace all labels.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    kwargs["InputS3Path"] = input_s3_path
    if replace_all_labels is not None:
        kwargs["ReplaceAllLabels"] = replace_all_labels
    try:
        resp = await client.call("StartImportLabelsTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start import labels task run") from exc
    return StartImportLabelsTaskRunResult(
        task_run_id=resp.get("TaskRunId"),
    )


async def start_ml_evaluation_task_run(
    transform_id: str,
    region_name: str | None = None,
) -> StartMlEvaluationTaskRunResult:
    """Start ml evaluation task run.

    Args:
        transform_id: Transform id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    try:
        resp = await client.call("StartMLEvaluationTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start ml evaluation task run") from exc
    return StartMlEvaluationTaskRunResult(
        task_run_id=resp.get("TaskRunId"),
    )


async def start_ml_labeling_set_generation_task_run(
    transform_id: str,
    output_s3_path: str,
    region_name: str | None = None,
) -> StartMlLabelingSetGenerationTaskRunResult:
    """Start ml labeling set generation task run.

    Args:
        transform_id: Transform id.
        output_s3_path: Output s3 path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    kwargs["OutputS3Path"] = output_s3_path
    try:
        resp = await client.call("StartMLLabelingSetGenerationTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start ml labeling set generation task run") from exc
    return StartMlLabelingSetGenerationTaskRunResult(
        task_run_id=resp.get("TaskRunId"),
    )


async def start_trigger(
    name: str,
    region_name: str | None = None,
) -> StartTriggerResult:
    """Start trigger.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("StartTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start trigger") from exc
    return StartTriggerResult(
        name=resp.get("Name"),
    )


async def start_workflow_run(
    name: str,
    *,
    run_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartWorkflowRunResult:
    """Start workflow run.

    Args:
        name: Name.
        run_properties: Run properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if run_properties is not None:
        kwargs["RunProperties"] = run_properties
    try:
        resp = await client.call("StartWorkflowRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start workflow run") from exc
    return StartWorkflowRunResult(
        run_id=resp.get("RunId"),
    )


async def stop_column_statistics_task_run(
    database_name: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Stop column statistics task run.

    Args:
        database_name: Database name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    try:
        await client.call("StopColumnStatisticsTaskRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop column statistics task run") from exc
    return None


async def stop_column_statistics_task_run_schedule(
    database_name: str,
    table_name: str,
    region_name: str | None = None,
) -> None:
    """Stop column statistics task run schedule.

    Args:
        database_name: Database name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    try:
        await client.call("StopColumnStatisticsTaskRunSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop column statistics task run schedule") from exc
    return None


async def stop_crawler(
    name: str,
    region_name: str | None = None,
) -> None:
    """Stop crawler.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("StopCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop crawler") from exc
    return None


async def stop_crawler_schedule(
    crawler_name: str,
    region_name: str | None = None,
) -> None:
    """Stop crawler schedule.

    Args:
        crawler_name: Crawler name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CrawlerName"] = crawler_name
    try:
        await client.call("StopCrawlerSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop crawler schedule") from exc
    return None


async def stop_session(
    id: str,
    *,
    request_origin: str | None = None,
    region_name: str | None = None,
) -> StopSessionResult:
    """Stop session.

    Args:
        id: Id.
        request_origin: Request origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if request_origin is not None:
        kwargs["RequestOrigin"] = request_origin
    try:
        resp = await client.call("StopSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop session") from exc
    return StopSessionResult(
        id=resp.get("Id"),
    )


async def stop_trigger(
    name: str,
    region_name: str | None = None,
) -> StopTriggerResult:
    """Stop trigger.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("StopTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop trigger") from exc
    return StopTriggerResult(
        name=resp.get("Name"),
    )


async def stop_workflow_run(
    name: str,
    run_id: str,
    region_name: str | None = None,
) -> None:
    """Stop workflow run.

    Args:
        name: Name.
        run_id: Run id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RunId"] = run_id
    try:
        await client.call("StopWorkflowRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop workflow run") from exc
    return None


async def tag_resource(
    resource_arn: str,
    tags_to_add: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags_to_add: Tags to add.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagsToAdd"] = tags_to_add
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tags_to_remove: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tags_to_remove: Tags to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagsToRemove"] = tags_to_remove
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_blueprint(
    name: str,
    blueprint_location: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateBlueprintResult:
    """Update blueprint.

    Args:
        name: Name.
        blueprint_location: Blueprint location.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["BlueprintLocation"] = blueprint_location
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateBlueprint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update blueprint") from exc
    return UpdateBlueprintResult(
        name=resp.get("Name"),
    )


async def update_catalog(
    catalog_id: str,
    catalog_input: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update catalog.

    Args:
        catalog_id: Catalog id.
        catalog_input: Catalog input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["CatalogInput"] = catalog_input
    try:
        await client.call("UpdateCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update catalog") from exc
    return None


async def update_classifier(
    *,
    grok_classifier: dict[str, Any] | None = None,
    xml_classifier: dict[str, Any] | None = None,
    json_classifier: dict[str, Any] | None = None,
    csv_classifier: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update classifier.

    Args:
        grok_classifier: Grok classifier.
        xml_classifier: Xml classifier.
        json_classifier: Json classifier.
        csv_classifier: Csv classifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if grok_classifier is not None:
        kwargs["GrokClassifier"] = grok_classifier
    if xml_classifier is not None:
        kwargs["XMLClassifier"] = xml_classifier
    if json_classifier is not None:
        kwargs["JsonClassifier"] = json_classifier
    if csv_classifier is not None:
        kwargs["CsvClassifier"] = csv_classifier
    try:
        await client.call("UpdateClassifier", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update classifier") from exc
    return None


async def update_column_statistics_for_partition(
    database_name: str,
    table_name: str,
    partition_values: list[str],
    column_statistics_list: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> UpdateColumnStatisticsForPartitionResult:
    """Update column statistics for partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_values: Partition values.
        column_statistics_list: Column statistics list.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValues"] = partition_values
    kwargs["ColumnStatisticsList"] = column_statistics_list
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("UpdateColumnStatisticsForPartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update column statistics for partition") from exc
    return UpdateColumnStatisticsForPartitionResult(
        errors=resp.get("Errors"),
    )


async def update_column_statistics_for_table(
    database_name: str,
    table_name: str,
    column_statistics_list: list[dict[str, Any]],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> UpdateColumnStatisticsForTableResult:
    """Update column statistics for table.

    Args:
        database_name: Database name.
        table_name: Table name.
        column_statistics_list: Column statistics list.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["ColumnStatisticsList"] = column_statistics_list
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        resp = await client.call("UpdateColumnStatisticsForTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update column statistics for table") from exc
    return UpdateColumnStatisticsForTableResult(
        errors=resp.get("Errors"),
    )


async def update_column_statistics_task_settings(
    database_name: str,
    table_name: str,
    *,
    role: str | None = None,
    schedule: str | None = None,
    column_name_list: list[str] | None = None,
    sample_size: float | None = None,
    catalog_id: str | None = None,
    security_configuration: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update column statistics task settings.

    Args:
        database_name: Database name.
        table_name: Table name.
        role: Role.
        schedule: Schedule.
        column_name_list: Column name list.
        sample_size: Sample size.
        catalog_id: Catalog id.
        security_configuration: Security configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if role is not None:
        kwargs["Role"] = role
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if column_name_list is not None:
        kwargs["ColumnNameList"] = column_name_list
    if sample_size is not None:
        kwargs["SampleSize"] = sample_size
    if catalog_id is not None:
        kwargs["CatalogID"] = catalog_id
    if security_configuration is not None:
        kwargs["SecurityConfiguration"] = security_configuration
    try:
        await client.call("UpdateColumnStatisticsTaskSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update column statistics task settings") from exc
    return None


async def update_connection(
    name: str,
    connection_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update connection.

    Args:
        name: Name.
        connection_input: Connection input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ConnectionInput"] = connection_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("UpdateConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update connection") from exc
    return None


async def update_crawler(
    name: str,
    *,
    role: str | None = None,
    database_name: str | None = None,
    description: str | None = None,
    targets: dict[str, Any] | None = None,
    schedule: str | None = None,
    classifiers: list[str] | None = None,
    table_prefix: str | None = None,
    schema_change_policy: dict[str, Any] | None = None,
    recrawl_policy: dict[str, Any] | None = None,
    lineage_configuration: dict[str, Any] | None = None,
    lake_formation_configuration: dict[str, Any] | None = None,
    configuration: str | None = None,
    crawler_security_configuration: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update crawler.

    Args:
        name: Name.
        role: Role.
        database_name: Database name.
        description: Description.
        targets: Targets.
        schedule: Schedule.
        classifiers: Classifiers.
        table_prefix: Table prefix.
        schema_change_policy: Schema change policy.
        recrawl_policy: Recrawl policy.
        lineage_configuration: Lineage configuration.
        lake_formation_configuration: Lake formation configuration.
        configuration: Configuration.
        crawler_security_configuration: Crawler security configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if role is not None:
        kwargs["Role"] = role
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if description is not None:
        kwargs["Description"] = description
    if targets is not None:
        kwargs["Targets"] = targets
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if classifiers is not None:
        kwargs["Classifiers"] = classifiers
    if table_prefix is not None:
        kwargs["TablePrefix"] = table_prefix
    if schema_change_policy is not None:
        kwargs["SchemaChangePolicy"] = schema_change_policy
    if recrawl_policy is not None:
        kwargs["RecrawlPolicy"] = recrawl_policy
    if lineage_configuration is not None:
        kwargs["LineageConfiguration"] = lineage_configuration
    if lake_formation_configuration is not None:
        kwargs["LakeFormationConfiguration"] = lake_formation_configuration
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if crawler_security_configuration is not None:
        kwargs["CrawlerSecurityConfiguration"] = crawler_security_configuration
    try:
        await client.call("UpdateCrawler", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update crawler") from exc
    return None


async def update_crawler_schedule(
    crawler_name: str,
    *,
    schedule: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update crawler schedule.

    Args:
        crawler_name: Crawler name.
        schedule: Schedule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CrawlerName"] = crawler_name
    if schedule is not None:
        kwargs["Schedule"] = schedule
    try:
        await client.call("UpdateCrawlerSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update crawler schedule") from exc
    return None


async def update_data_quality_ruleset(
    name: str,
    *,
    description: str | None = None,
    ruleset: str | None = None,
    region_name: str | None = None,
) -> UpdateDataQualityRulesetResult:
    """Update data quality ruleset.

    Args:
        name: Name.
        description: Description.
        ruleset: Ruleset.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if ruleset is not None:
        kwargs["Ruleset"] = ruleset
    try:
        resp = await client.call("UpdateDataQualityRuleset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data quality ruleset") from exc
    return UpdateDataQualityRulesetResult(
        name=resp.get("Name"),
        description=resp.get("Description"),
        ruleset=resp.get("Ruleset"),
    )


async def update_database(
    name: str,
    database_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update database.

    Args:
        name: Name.
        database_input: Database input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["DatabaseInput"] = database_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("UpdateDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update database") from exc
    return None


async def update_dev_endpoint(
    endpoint_name: str,
    *,
    public_key: str | None = None,
    add_public_keys: list[str] | None = None,
    delete_public_keys: list[str] | None = None,
    custom_libraries: dict[str, Any] | None = None,
    update_etl_libraries: bool | None = None,
    delete_arguments: list[str] | None = None,
    add_arguments: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update dev endpoint.

    Args:
        endpoint_name: Endpoint name.
        public_key: Public key.
        add_public_keys: Add public keys.
        delete_public_keys: Delete public keys.
        custom_libraries: Custom libraries.
        update_etl_libraries: Update etl libraries.
        delete_arguments: Delete arguments.
        add_arguments: Add arguments.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    if public_key is not None:
        kwargs["PublicKey"] = public_key
    if add_public_keys is not None:
        kwargs["AddPublicKeys"] = add_public_keys
    if delete_public_keys is not None:
        kwargs["DeletePublicKeys"] = delete_public_keys
    if custom_libraries is not None:
        kwargs["CustomLibraries"] = custom_libraries
    if update_etl_libraries is not None:
        kwargs["UpdateEtlLibraries"] = update_etl_libraries
    if delete_arguments is not None:
        kwargs["DeleteArguments"] = delete_arguments
    if add_arguments is not None:
        kwargs["AddArguments"] = add_arguments
    try:
        await client.call("UpdateDevEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dev endpoint") from exc
    return None


async def update_glue_identity_center_configuration(
    *,
    scopes: list[str] | None = None,
    user_background_sessions_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update glue identity center configuration.

    Args:
        scopes: Scopes.
        user_background_sessions_enabled: User background sessions enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if scopes is not None:
        kwargs["Scopes"] = scopes
    if user_background_sessions_enabled is not None:
        kwargs["UserBackgroundSessionsEnabled"] = user_background_sessions_enabled
    try:
        await client.call("UpdateGlueIdentityCenterConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update glue identity center configuration") from exc
    return None


async def update_integration_resource_property(
    resource_arn: str,
    *,
    source_processing_properties: dict[str, Any] | None = None,
    target_processing_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateIntegrationResourcePropertyResult:
    """Update integration resource property.

    Args:
        resource_arn: Resource arn.
        source_processing_properties: Source processing properties.
        target_processing_properties: Target processing properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if source_processing_properties is not None:
        kwargs["SourceProcessingProperties"] = source_processing_properties
    if target_processing_properties is not None:
        kwargs["TargetProcessingProperties"] = target_processing_properties
    try:
        resp = await client.call("UpdateIntegrationResourceProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update integration resource property") from exc
    return UpdateIntegrationResourcePropertyResult(
        resource_arn=resp.get("ResourceArn"),
        source_processing_properties=resp.get("SourceProcessingProperties"),
        target_processing_properties=resp.get("TargetProcessingProperties"),
    )


async def update_integration_table_properties(
    resource_arn: str,
    table_name: str,
    *,
    source_table_config: dict[str, Any] | None = None,
    target_table_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update integration table properties.

    Args:
        resource_arn: Resource arn.
        table_name: Table name.
        source_table_config: Source table config.
        target_table_config: Target table config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TableName"] = table_name
    if source_table_config is not None:
        kwargs["SourceTableConfig"] = source_table_config
    if target_table_config is not None:
        kwargs["TargetTableConfig"] = target_table_config
    try:
        await client.call("UpdateIntegrationTableProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update integration table properties") from exc
    return None


async def update_job(
    job_name: str,
    job_update: dict[str, Any],
    region_name: str | None = None,
) -> UpdateJobResult:
    """Update job.

    Args:
        job_name: Job name.
        job_update: Job update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    kwargs["JobUpdate"] = job_update
    try:
        resp = await client.call("UpdateJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update job") from exc
    return UpdateJobResult(
        job_name=resp.get("JobName"),
    )


async def update_job_from_source_control(
    *,
    job_name: str | None = None,
    provider: str | None = None,
    repository_name: str | None = None,
    repository_owner: str | None = None,
    branch_name: str | None = None,
    folder: str | None = None,
    commit_id: str | None = None,
    auth_strategy: str | None = None,
    auth_token: str | None = None,
    region_name: str | None = None,
) -> UpdateJobFromSourceControlResult:
    """Update job from source control.

    Args:
        job_name: Job name.
        provider: Provider.
        repository_name: Repository name.
        repository_owner: Repository owner.
        branch_name: Branch name.
        folder: Folder.
        commit_id: Commit id.
        auth_strategy: Auth strategy.
        auth_token: Auth token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if job_name is not None:
        kwargs["JobName"] = job_name
    if provider is not None:
        kwargs["Provider"] = provider
    if repository_name is not None:
        kwargs["RepositoryName"] = repository_name
    if repository_owner is not None:
        kwargs["RepositoryOwner"] = repository_owner
    if branch_name is not None:
        kwargs["BranchName"] = branch_name
    if folder is not None:
        kwargs["Folder"] = folder
    if commit_id is not None:
        kwargs["CommitId"] = commit_id
    if auth_strategy is not None:
        kwargs["AuthStrategy"] = auth_strategy
    if auth_token is not None:
        kwargs["AuthToken"] = auth_token
    try:
        resp = await client.call("UpdateJobFromSourceControl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update job from source control") from exc
    return UpdateJobFromSourceControlResult(
        job_name=resp.get("JobName"),
    )


async def update_ml_transform(
    transform_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    parameters: dict[str, Any] | None = None,
    role: str | None = None,
    glue_version: str | None = None,
    max_capacity: float | None = None,
    worker_type: str | None = None,
    number_of_workers: int | None = None,
    timeout: int | None = None,
    max_retries: int | None = None,
    region_name: str | None = None,
) -> UpdateMlTransformResult:
    """Update ml transform.

    Args:
        transform_id: Transform id.
        name: Name.
        description: Description.
        parameters: Parameters.
        role: Role.
        glue_version: Glue version.
        max_capacity: Max capacity.
        worker_type: Worker type.
        number_of_workers: Number of workers.
        timeout: Timeout.
        max_retries: Max retries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransformId"] = transform_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if role is not None:
        kwargs["Role"] = role
    if glue_version is not None:
        kwargs["GlueVersion"] = glue_version
    if max_capacity is not None:
        kwargs["MaxCapacity"] = max_capacity
    if worker_type is not None:
        kwargs["WorkerType"] = worker_type
    if number_of_workers is not None:
        kwargs["NumberOfWorkers"] = number_of_workers
    if timeout is not None:
        kwargs["Timeout"] = timeout
    if max_retries is not None:
        kwargs["MaxRetries"] = max_retries
    try:
        resp = await client.call("UpdateMLTransform", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ml transform") from exc
    return UpdateMlTransformResult(
        transform_id=resp.get("TransformId"),
    )


async def update_partition(
    database_name: str,
    table_name: str,
    partition_value_list: list[str],
    partition_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update partition.

    Args:
        database_name: Database name.
        table_name: Table name.
        partition_value_list: Partition value list.
        partition_input: Partition input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["PartitionValueList"] = partition_value_list
    kwargs["PartitionInput"] = partition_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("UpdatePartition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update partition") from exc
    return None


async def update_registry(
    registry_id: dict[str, Any],
    description: str,
    region_name: str | None = None,
) -> UpdateRegistryResult:
    """Update registry.

    Args:
        registry_id: Registry id.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegistryId"] = registry_id
    kwargs["Description"] = description
    try:
        resp = await client.call("UpdateRegistry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update registry") from exc
    return UpdateRegistryResult(
        registry_name=resp.get("RegistryName"),
        registry_arn=resp.get("RegistryArn"),
    )


async def update_schema(
    schema_id: dict[str, Any],
    *,
    schema_version_number: dict[str, Any] | None = None,
    compatibility: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateSchemaResult:
    """Update schema.

    Args:
        schema_id: Schema id.
        schema_version_number: Schema version number.
        compatibility: Compatibility.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SchemaId"] = schema_id
    if schema_version_number is not None:
        kwargs["SchemaVersionNumber"] = schema_version_number
    if compatibility is not None:
        kwargs["Compatibility"] = compatibility
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateSchema", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update schema") from exc
    return UpdateSchemaResult(
        schema_arn=resp.get("SchemaArn"),
        schema_name=resp.get("SchemaName"),
        registry_name=resp.get("RegistryName"),
    )


async def update_source_control_from_job(
    *,
    job_name: str | None = None,
    provider: str | None = None,
    repository_name: str | None = None,
    repository_owner: str | None = None,
    branch_name: str | None = None,
    folder: str | None = None,
    commit_id: str | None = None,
    auth_strategy: str | None = None,
    auth_token: str | None = None,
    region_name: str | None = None,
) -> UpdateSourceControlFromJobResult:
    """Update source control from job.

    Args:
        job_name: Job name.
        provider: Provider.
        repository_name: Repository name.
        repository_owner: Repository owner.
        branch_name: Branch name.
        folder: Folder.
        commit_id: Commit id.
        auth_strategy: Auth strategy.
        auth_token: Auth token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    if job_name is not None:
        kwargs["JobName"] = job_name
    if provider is not None:
        kwargs["Provider"] = provider
    if repository_name is not None:
        kwargs["RepositoryName"] = repository_name
    if repository_owner is not None:
        kwargs["RepositoryOwner"] = repository_owner
    if branch_name is not None:
        kwargs["BranchName"] = branch_name
    if folder is not None:
        kwargs["Folder"] = folder
    if commit_id is not None:
        kwargs["CommitId"] = commit_id
    if auth_strategy is not None:
        kwargs["AuthStrategy"] = auth_strategy
    if auth_token is not None:
        kwargs["AuthToken"] = auth_token
    try:
        resp = await client.call("UpdateSourceControlFromJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update source control from job") from exc
    return UpdateSourceControlFromJobResult(
        job_name=resp.get("JobName"),
    )


async def update_table(
    database_name: str,
    *,
    catalog_id: str | None = None,
    name: str | None = None,
    table_input: dict[str, Any] | None = None,
    skip_archive: bool | None = None,
    transaction_id: str | None = None,
    version_id: str | None = None,
    view_update_action: str | None = None,
    force: bool | None = None,
    update_open_table_format_input: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update table.

    Args:
        database_name: Database name.
        catalog_id: Catalog id.
        name: Name.
        table_input: Table input.
        skip_archive: Skip archive.
        transaction_id: Transaction id.
        version_id: Version id.
        view_update_action: View update action.
        force: Force.
        update_open_table_format_input: Update open table format input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    if name is not None:
        kwargs["Name"] = name
    if table_input is not None:
        kwargs["TableInput"] = table_input
    if skip_archive is not None:
        kwargs["SkipArchive"] = skip_archive
    if transaction_id is not None:
        kwargs["TransactionId"] = transaction_id
    if version_id is not None:
        kwargs["VersionId"] = version_id
    if view_update_action is not None:
        kwargs["ViewUpdateAction"] = view_update_action
    if force is not None:
        kwargs["Force"] = force
    if update_open_table_format_input is not None:
        kwargs["UpdateOpenTableFormatInput"] = update_open_table_format_input
    try:
        await client.call("UpdateTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update table") from exc
    return None


async def update_table_optimizer(
    catalog_id: str,
    database_name: str,
    table_name: str,
    type_value: str,
    table_optimizer_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update table optimizer.

    Args:
        catalog_id: Catalog id.
        database_name: Database name.
        table_name: Table name.
        type_value: Type value.
        table_optimizer_configuration: Table optimizer configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogId"] = catalog_id
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    kwargs["Type"] = type_value
    kwargs["TableOptimizerConfiguration"] = table_optimizer_configuration
    try:
        await client.call("UpdateTableOptimizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update table optimizer") from exc
    return None


async def update_trigger(
    name: str,
    trigger_update: dict[str, Any],
    region_name: str | None = None,
) -> UpdateTriggerResult:
    """Update trigger.

    Args:
        name: Name.
        trigger_update: Trigger update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["TriggerUpdate"] = trigger_update
    try:
        resp = await client.call("UpdateTrigger", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update trigger") from exc
    return UpdateTriggerResult(
        trigger=resp.get("Trigger"),
    )


async def update_usage_profile(
    name: str,
    configuration: dict[str, Any],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateUsageProfileResult:
    """Update usage profile.

    Args:
        name: Name.
        configuration: Configuration.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Configuration"] = configuration
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateUsageProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update usage profile") from exc
    return UpdateUsageProfileResult(
        name=resp.get("Name"),
    )


async def update_user_defined_function(
    database_name: str,
    function_name: str,
    function_input: dict[str, Any],
    *,
    catalog_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update user defined function.

    Args:
        database_name: Database name.
        function_name: Function name.
        function_input: Function input.
        catalog_id: Catalog id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseName"] = database_name
    kwargs["FunctionName"] = function_name
    kwargs["FunctionInput"] = function_input
    if catalog_id is not None:
        kwargs["CatalogId"] = catalog_id
    try:
        await client.call("UpdateUserDefinedFunction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update user defined function") from exc
    return None


async def update_workflow(
    name: str,
    *,
    description: str | None = None,
    default_run_properties: dict[str, Any] | None = None,
    max_concurrent_runs: int | None = None,
    region_name: str | None = None,
) -> UpdateWorkflowResult:
    """Update workflow.

    Args:
        name: Name.
        description: Description.
        default_run_properties: Default run properties.
        max_concurrent_runs: Max concurrent runs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("glue", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if default_run_properties is not None:
        kwargs["DefaultRunProperties"] = default_run_properties
    if max_concurrent_runs is not None:
        kwargs["MaxConcurrentRuns"] = max_concurrent_runs
    try:
        resp = await client.call("UpdateWorkflow", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update workflow") from exc
    return UpdateWorkflowResult(
        name=resp.get("Name"),
    )
