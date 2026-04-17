"""aws_util.aio.dms — Async DMS utilities.

All functions are native async using the aiohttp-based AsyncClient engine.
Pydantic models are re-exported from the sync module.
"""

from __future__ import annotations

import asyncio
import time as _time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.dms import (
    ApplyPendingMaintenanceActionResult,
    BatchStartRecommendationsResult,
    CancelMetadataModelConversionResult,
    CancelMetadataModelCreationResult,
    CancelReplicationTaskAssessmentRunResult,
    ConnectionResult,
    CreateDataMigrationResult,
    CreateDataProviderResult,
    CreateEventSubscriptionResult,
    CreateFleetAdvisorCollectorResult,
    CreateInstanceProfileResult,
    CreateMigrationProjectResult,
    CreateReplicationConfigResult,
    DeleteCertificateResult,
    DeleteConnectionResult,
    DeleteDataMigrationResult,
    DeleteDataProviderResult,
    DeleteEventSubscriptionResult,
    DeleteFleetAdvisorDatabasesResult,
    DeleteInstanceProfileResult,
    DeleteMigrationProjectResult,
    DeleteReplicationConfigResult,
    DeleteReplicationTaskAssessmentRunResult,
    DescribeAccountAttributesResult,
    DescribeApplicableIndividualAssessmentsResult,
    DescribeCertificatesResult,
    DescribeConversionConfigurationResult,
    DescribeDataMigrationsResult,
    DescribeDataProvidersResult,
    DescribeEndpointSettingsResult,
    DescribeEndpointTypesResult,
    DescribeEngineVersionsResult,
    DescribeEventCategoriesResult,
    DescribeEventsResult,
    DescribeEventSubscriptionsResult,
    DescribeExtensionPackAssociationsResult,
    DescribeFleetAdvisorCollectorsResult,
    DescribeFleetAdvisorDatabasesResult,
    DescribeFleetAdvisorLsaAnalysisResult,
    DescribeFleetAdvisorSchemaObjectSummaryResult,
    DescribeFleetAdvisorSchemasResult,
    DescribeInstanceProfilesResult,
    DescribeMetadataModelAssessmentsResult,
    DescribeMetadataModelChildrenResult,
    DescribeMetadataModelConversionsResult,
    DescribeMetadataModelCreationsResult,
    DescribeMetadataModelExportsAsScriptResult,
    DescribeMetadataModelExportsToTargetResult,
    DescribeMetadataModelImportsResult,
    DescribeMetadataModelResult,
    DescribeMigrationProjectsResult,
    DescribeOrderableReplicationInstancesResult,
    DescribePendingMaintenanceActionsResult,
    DescribeRecommendationLimitationsResult,
    DescribeRecommendationsResult,
    DescribeRefreshSchemasStatusResult,
    DescribeReplicationConfigsResult,
    DescribeReplicationInstanceTaskLogsResult,
    DescribeReplicationsResult,
    DescribeReplicationSubnetGroupsResult,
    DescribeReplicationTableStatisticsResult,
    DescribeReplicationTaskAssessmentResultsResult,
    DescribeReplicationTaskAssessmentRunsResult,
    DescribeReplicationTaskIndividualAssessmentsResult,
    DescribeSchemasResult,
    EndpointResult,
    ExportMetadataModelAssessmentResult,
    GetTargetSelectionRulesResult,
    ImportCertificateResult,
    ListTagsForResourceResult,
    ModifyConversionConfigurationResult,
    ModifyDataMigrationResult,
    ModifyDataProviderResult,
    ModifyEventSubscriptionResult,
    ModifyInstanceProfileResult,
    ModifyMigrationProjectResult,
    ModifyReplicationConfigResult,
    ModifyReplicationSubnetGroupResult,
    ModifyReplicationTaskResult,
    MoveReplicationTaskResult,
    RebootReplicationInstanceResult,
    RefreshSchemasResult,
    ReloadReplicationTablesResult,
    ReloadTablesResult,
    ReplicationInstanceResult,
    ReplicationSubnetGroupResult,
    ReplicationTaskResult,
    RunConnectionResult,
    RunFleetAdvisorLsaAnalysisResult,
    StartDataMigrationResult,
    StartExtensionPackAssociationResult,
    StartMetadataModelAssessmentResult,
    StartMetadataModelConversionResult,
    StartMetadataModelCreationResult,
    StartMetadataModelExportAsScriptResult,
    StartMetadataModelExportToTargetResult,
    StartMetadataModelImportResult,
    StartReplicationResult,
    StartReplicationTaskAssessmentResult,
    StartReplicationTaskAssessmentRunResult,
    StopDataMigrationResult,
    StopReplicationResult,
    TableStatistic,
    UpdateSubscriptionsToEventBridgeResult,
    _parse_connection,
    _parse_endpoint,
    _parse_replication_instance,
    _parse_replication_task,
)
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "ApplyPendingMaintenanceActionResult",
    "BatchStartRecommendationsResult",
    "CancelMetadataModelConversionResult",
    "CancelMetadataModelCreationResult",
    "CancelReplicationTaskAssessmentRunResult",
    "ConnectionResult",
    "CreateDataMigrationResult",
    "CreateDataProviderResult",
    "CreateEventSubscriptionResult",
    "CreateFleetAdvisorCollectorResult",
    "CreateInstanceProfileResult",
    "CreateMigrationProjectResult",
    "CreateReplicationConfigResult",
    "DeleteCertificateResult",
    "DeleteConnectionResult",
    "DeleteDataMigrationResult",
    "DeleteDataProviderResult",
    "DeleteEventSubscriptionResult",
    "DeleteFleetAdvisorDatabasesResult",
    "DeleteInstanceProfileResult",
    "DeleteMigrationProjectResult",
    "DeleteReplicationConfigResult",
    "DeleteReplicationTaskAssessmentRunResult",
    "DescribeAccountAttributesResult",
    "DescribeApplicableIndividualAssessmentsResult",
    "DescribeCertificatesResult",
    "DescribeConversionConfigurationResult",
    "DescribeDataMigrationsResult",
    "DescribeDataProvidersResult",
    "DescribeEndpointSettingsResult",
    "DescribeEndpointTypesResult",
    "DescribeEngineVersionsResult",
    "DescribeEventCategoriesResult",
    "DescribeEventSubscriptionsResult",
    "DescribeEventsResult",
    "DescribeExtensionPackAssociationsResult",
    "DescribeFleetAdvisorCollectorsResult",
    "DescribeFleetAdvisorDatabasesResult",
    "DescribeFleetAdvisorLsaAnalysisResult",
    "DescribeFleetAdvisorSchemaObjectSummaryResult",
    "DescribeFleetAdvisorSchemasResult",
    "DescribeInstanceProfilesResult",
    "DescribeMetadataModelAssessmentsResult",
    "DescribeMetadataModelChildrenResult",
    "DescribeMetadataModelConversionsResult",
    "DescribeMetadataModelCreationsResult",
    "DescribeMetadataModelExportsAsScriptResult",
    "DescribeMetadataModelExportsToTargetResult",
    "DescribeMetadataModelImportsResult",
    "DescribeMetadataModelResult",
    "DescribeMigrationProjectsResult",
    "DescribeOrderableReplicationInstancesResult",
    "DescribePendingMaintenanceActionsResult",
    "DescribeRecommendationLimitationsResult",
    "DescribeRecommendationsResult",
    "DescribeRefreshSchemasStatusResult",
    "DescribeReplicationConfigsResult",
    "DescribeReplicationInstanceTaskLogsResult",
    "DescribeReplicationSubnetGroupsResult",
    "DescribeReplicationTableStatisticsResult",
    "DescribeReplicationTaskAssessmentResultsResult",
    "DescribeReplicationTaskAssessmentRunsResult",
    "DescribeReplicationTaskIndividualAssessmentsResult",
    "DescribeReplicationsResult",
    "DescribeSchemasResult",
    "EndpointResult",
    "ExportMetadataModelAssessmentResult",
    "GetTargetSelectionRulesResult",
    "ImportCertificateResult",
    "ListTagsForResourceResult",
    "ModifyConversionConfigurationResult",
    "ModifyDataMigrationResult",
    "ModifyDataProviderResult",
    "ModifyEventSubscriptionResult",
    "ModifyInstanceProfileResult",
    "ModifyMigrationProjectResult",
    "ModifyReplicationConfigResult",
    "ModifyReplicationSubnetGroupResult",
    "ModifyReplicationTaskResult",
    "MoveReplicationTaskResult",
    "RebootReplicationInstanceResult",
    "RefreshSchemasResult",
    "ReloadReplicationTablesResult",
    "ReloadTablesResult",
    "ReplicationInstanceResult",
    "ReplicationSubnetGroupResult",
    "ReplicationTaskResult",
    "RunConnectionResult",
    "RunFleetAdvisorLsaAnalysisResult",
    "StartDataMigrationResult",
    "StartExtensionPackAssociationResult",
    "StartMetadataModelAssessmentResult",
    "StartMetadataModelConversionResult",
    "StartMetadataModelCreationResult",
    "StartMetadataModelExportAsScriptResult",
    "StartMetadataModelExportToTargetResult",
    "StartMetadataModelImportResult",
    "StartReplicationResult",
    "StartReplicationTaskAssessmentResult",
    "StartReplicationTaskAssessmentRunResult",
    "StopDataMigrationResult",
    "StopReplicationResult",
    "TableStatistic",
    "UpdateSubscriptionsToEventBridgeResult",
    "add_tags_to_resource",
    "apply_pending_maintenance_action",
    "batch_start_recommendations",
    "cancel_metadata_model_conversion",
    "cancel_metadata_model_creation",
    "cancel_replication_task_assessment_run",
    "create_data_migration",
    "create_data_provider",
    "create_endpoint",
    "create_event_subscription",
    "create_fleet_advisor_collector",
    "create_instance_profile",
    "create_migration_project",
    "create_replication_config",
    "create_replication_instance",
    "create_replication_subnet_group",
    "create_replication_task",
    "delete_certificate",
    "delete_connection",
    "delete_data_migration",
    "delete_data_provider",
    "delete_endpoint",
    "delete_event_subscription",
    "delete_fleet_advisor_collector",
    "delete_fleet_advisor_databases",
    "delete_instance_profile",
    "delete_migration_project",
    "delete_replication_config",
    "delete_replication_instance",
    "delete_replication_subnet_group",
    "delete_replication_task",
    "delete_replication_task_assessment_run",
    "describe_account_attributes",
    "describe_applicable_individual_assessments",
    "describe_certificates",
    "describe_connections",
    "describe_conversion_configuration",
    "describe_data_migrations",
    "describe_data_providers",
    "describe_endpoint_settings",
    "describe_endpoint_types",
    "describe_endpoints",
    "describe_engine_versions",
    "describe_event_categories",
    "describe_event_subscriptions",
    "describe_events",
    "describe_extension_pack_associations",
    "describe_fleet_advisor_collectors",
    "describe_fleet_advisor_databases",
    "describe_fleet_advisor_lsa_analysis",
    "describe_fleet_advisor_schema_object_summary",
    "describe_fleet_advisor_schemas",
    "describe_instance_profiles",
    "describe_metadata_model",
    "describe_metadata_model_assessments",
    "describe_metadata_model_children",
    "describe_metadata_model_conversions",
    "describe_metadata_model_creations",
    "describe_metadata_model_exports_as_script",
    "describe_metadata_model_exports_to_target",
    "describe_metadata_model_imports",
    "describe_migration_projects",
    "describe_orderable_replication_instances",
    "describe_pending_maintenance_actions",
    "describe_recommendation_limitations",
    "describe_recommendations",
    "describe_refresh_schemas_status",
    "describe_replication_configs",
    "describe_replication_instance_task_logs",
    "describe_replication_instances",
    "describe_replication_subnet_groups",
    "describe_replication_table_statistics",
    "describe_replication_task_assessment_results",
    "describe_replication_task_assessment_runs",
    "describe_replication_task_individual_assessments",
    "describe_replication_tasks",
    "describe_replications",
    "describe_schemas",
    "describe_table_statistics",
    "export_metadata_model_assessment",
    "get_target_selection_rules",
    "import_certificate",
    "list_tags_for_resource",
    "modify_conversion_configuration",
    "modify_data_migration",
    "modify_data_provider",
    "modify_endpoint",
    "modify_event_subscription",
    "modify_instance_profile",
    "modify_migration_project",
    "modify_replication_config",
    "modify_replication_instance",
    "modify_replication_subnet_group",
    "modify_replication_task",
    "move_replication_task",
    "reboot_replication_instance",
    "refresh_schemas",
    "reload_replication_tables",
    "reload_tables",
    "remove_tags_from_resource",
    "run_connection",
    "run_fleet_advisor_lsa_analysis",
    "start_data_migration",
    "start_extension_pack_association",
    "start_metadata_model_assessment",
    "start_metadata_model_conversion",
    "start_metadata_model_creation",
    "start_metadata_model_export_as_script",
    "start_metadata_model_export_to_target",
    "start_metadata_model_import",
    "start_recommendations",
    "start_replication",
    "start_replication_task",
    "start_replication_task_assessment",
    "start_replication_task_assessment_run",
    "stop_data_migration",
    "stop_replication",
    "stop_replication_task",
    "test_connection",
    "update_subscriptions_to_event_bridge",
    "wait_for_replication_instance",
    "wait_for_replication_task",
]


# ---------------------------------------------------------------------------
# Replication instances
# ---------------------------------------------------------------------------


async def create_replication_instance(
    replication_instance_identifier: str,
    replication_instance_class: str,
    *,
    allocated_storage: int | None = None,
    availability_zone: str | None = None,
    multi_az: bool = False,
    publicly_accessible: bool = False,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ReplicationInstanceResult:
    """Create a DMS replication instance (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationInstanceIdentifier": (replication_instance_identifier),
        "ReplicationInstanceClass": replication_instance_class,
        "MultiAZ": multi_az,
        "PubliclyAccessible": publicly_accessible,
    }
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if availability_zone:
        kwargs["AvailabilityZone"] = availability_zone
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateReplicationInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_replication_instance") from exc
    return _parse_replication_instance(resp["ReplicationInstance"])


async def describe_replication_instances(
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[ReplicationInstanceResult]:
    """Describe all DMS replication instances (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    results: list[ReplicationInstanceResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeReplicationInstances", **kwargs)
            for ri in resp.get("ReplicationInstances", []):
                results.append(_parse_replication_instance(ri))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_replication_instances") from exc
    return results


async def modify_replication_instance(
    replication_instance_arn: str,
    *,
    replication_instance_class: str | None = None,
    allocated_storage: int | None = None,
    multi_az: bool | None = None,
    apply_immediately: bool = True,
    region_name: str | None = None,
) -> ReplicationInstanceResult:
    """Modify a DMS replication instance (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationInstanceArn": replication_instance_arn,
        "ApplyImmediately": apply_immediately,
    }
    if replication_instance_class:
        kwargs["ReplicationInstanceClass"] = replication_instance_class
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    try:
        resp = await client.call("ModifyReplicationInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_replication_instance") from exc
    return _parse_replication_instance(resp["ReplicationInstance"])


async def delete_replication_instance(
    replication_instance_arn: str,
    *,
    region_name: str | None = None,
) -> ReplicationInstanceResult:
    """Delete a DMS replication instance (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "DeleteReplicationInstance",
            ReplicationInstanceArn=replication_instance_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_replication_instance") from exc
    return _parse_replication_instance(resp["ReplicationInstance"])


async def wait_for_replication_instance(
    replication_instance_arn: str,
    *,
    target_status: str = "available",
    timeout: float = 600,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> ReplicationInstanceResult:
    """Poll until a replication instance reaches target status (async)."""
    deadline = _time.monotonic() + timeout
    while _time.monotonic() < deadline:
        instances = await describe_replication_instances(
            region_name=region_name,
        )
        for inst in instances:
            if inst.replication_instance_arn == (replication_instance_arn):
                if inst.replication_instance_status == (target_status):
                    return inst
                break
        await asyncio.sleep(poll_interval)
    raise AwsTimeoutError(
        f"Replication instance {replication_instance_arn!r} "
        f"did not reach {target_status!r} within {timeout}s"
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


async def create_endpoint(
    endpoint_identifier: str,
    endpoint_type: str,
    engine_name: str,
    *,
    server_name: str | None = None,
    port: int | None = None,
    database_name: str | None = None,
    username: str | None = None,
    password: str | None = None,
    ssl_mode: str | None = None,
    tags: list[dict[str, str]] | None = None,
    extra_connection_attributes: str | None = None,
    region_name: str | None = None,
) -> EndpointResult:
    """Create a DMS endpoint (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {
        "EndpointIdentifier": endpoint_identifier,
        "EndpointType": endpoint_type,
        "EngineName": engine_name,
    }
    if server_name:
        kwargs["ServerName"] = server_name
    if port is not None:
        kwargs["Port"] = port
    if database_name:
        kwargs["DatabaseName"] = database_name
    if username:
        kwargs["Username"] = username
    if password:
        kwargs["Password"] = password
    if ssl_mode:
        kwargs["SslMode"] = ssl_mode
    if tags:
        kwargs["Tags"] = tags
    if extra_connection_attributes:
        kwargs["ExtraConnectionAttributes"] = extra_connection_attributes
    try:
        resp = await client.call("CreateEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_endpoint") from exc
    return _parse_endpoint(resp["Endpoint"])


async def describe_endpoints(
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[EndpointResult]:
    """Describe all DMS endpoints (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    results: list[EndpointResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeEndpoints", **kwargs)
            for ep in resp.get("Endpoints", []):
                results.append(_parse_endpoint(ep))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_endpoints") from exc
    return results


async def modify_endpoint(
    endpoint_arn: str,
    *,
    endpoint_identifier: str | None = None,
    engine_name: str | None = None,
    server_name: str | None = None,
    port: int | None = None,
    database_name: str | None = None,
    username: str | None = None,
    password: str | None = None,
    ssl_mode: str | None = None,
    region_name: str | None = None,
) -> EndpointResult:
    """Modify a DMS endpoint (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {"EndpointArn": endpoint_arn}
    if endpoint_identifier:
        kwargs["EndpointIdentifier"] = endpoint_identifier
    if engine_name:
        kwargs["EngineName"] = engine_name
    if server_name:
        kwargs["ServerName"] = server_name
    if port is not None:
        kwargs["Port"] = port
    if database_name:
        kwargs["DatabaseName"] = database_name
    if username:
        kwargs["Username"] = username
    if password:
        kwargs["Password"] = password
    if ssl_mode:
        kwargs["SslMode"] = ssl_mode
    try:
        resp = await client.call("ModifyEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_endpoint") from exc
    return _parse_endpoint(resp["Endpoint"])


async def delete_endpoint(
    endpoint_arn: str,
    *,
    region_name: str | None = None,
) -> EndpointResult:
    """Delete a DMS endpoint (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "DeleteEndpoint",
            EndpointArn=endpoint_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_endpoint") from exc
    return _parse_endpoint(resp["Endpoint"])


async def test_connection(
    replication_instance_arn: str,
    endpoint_arn: str,
    *,
    region_name: str | None = None,
) -> ConnectionResult:
    """Test connectivity between a replication instance and endpoint (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "TestConnection",
            ReplicationInstanceArn=replication_instance_arn,
            EndpointArn=endpoint_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "test_connection") from exc
    return _parse_connection(resp["Connection"])


async def describe_connections(
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[ConnectionResult]:
    """Describe DMS connections (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    results: list[ConnectionResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeConnections", **kwargs)
            for conn in resp.get("Connections", []):
                results.append(_parse_connection(conn))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_connections") from exc
    return results


# ---------------------------------------------------------------------------
# Replication tasks
# ---------------------------------------------------------------------------


async def create_replication_task(
    replication_task_identifier: str,
    source_endpoint_arn: str,
    target_endpoint_arn: str,
    replication_instance_arn: str,
    migration_type: str,
    table_mappings: str,
    *,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ReplicationTaskResult:
    """Create a DMS replication task (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationTaskIdentifier": (replication_task_identifier),
        "SourceEndpointArn": source_endpoint_arn,
        "TargetEndpointArn": target_endpoint_arn,
        "ReplicationInstanceArn": replication_instance_arn,
        "MigrationType": migration_type,
        "TableMappings": table_mappings,
    }
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateReplicationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_replication_task") from exc
    return _parse_replication_task(resp["ReplicationTask"])


async def describe_replication_tasks(
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[ReplicationTaskResult]:
    """Describe all DMS replication tasks (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    results: list[ReplicationTaskResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeReplicationTasks", **kwargs)
            for task in resp.get("ReplicationTasks", []):
                results.append(_parse_replication_task(task))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_replication_tasks") from exc
    return results


async def start_replication_task(
    replication_task_arn: str,
    start_replication_task_type: str = "start-replication",
    *,
    region_name: str | None = None,
) -> ReplicationTaskResult:
    """Start a DMS replication task (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "StartReplicationTask",
            ReplicationTaskArn=replication_task_arn,
            StartReplicationTaskType=(start_replication_task_type),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "start_replication_task") from exc
    return _parse_replication_task(resp["ReplicationTask"])


async def stop_replication_task(
    replication_task_arn: str,
    *,
    region_name: str | None = None,
) -> ReplicationTaskResult:
    """Stop a DMS replication task (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "StopReplicationTask",
            ReplicationTaskArn=replication_task_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "stop_replication_task") from exc
    return _parse_replication_task(resp["ReplicationTask"])


async def delete_replication_task(
    replication_task_arn: str,
    *,
    region_name: str | None = None,
) -> ReplicationTaskResult:
    """Delete a DMS replication task (async)."""
    client = async_client("dms", region_name)
    try:
        resp = await client.call(
            "DeleteReplicationTask",
            ReplicationTaskArn=replication_task_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_replication_task") from exc
    return _parse_replication_task(resp["ReplicationTask"])


async def wait_for_replication_task(
    replication_task_arn: str,
    *,
    target_status: str = "running",
    timeout: float = 600,
    poll_interval: float = 15,
    region_name: str | None = None,
) -> ReplicationTaskResult:
    """Poll until a replication task reaches target status (async)."""
    deadline = _time.monotonic() + timeout
    while _time.monotonic() < deadline:
        tasks = await describe_replication_tasks(
            region_name=region_name,
        )
        for task in tasks:
            if task.replication_task_arn == (replication_task_arn):
                if task.status == target_status:
                    return task
                break
        await asyncio.sleep(poll_interval)
    raise AwsTimeoutError(
        f"Replication task {replication_task_arn!r} "
        f"did not reach {target_status!r} within {timeout}s"
    )


async def describe_table_statistics(
    replication_task_arn: str,
    *,
    region_name: str | None = None,
) -> list[TableStatistic]:
    """Describe table statistics for a replication task (async)."""
    client = async_client("dms", region_name)
    results: list[TableStatistic] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "ReplicationTaskArn": replication_task_arn,
            }
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeTableStatistics", **kwargs)
            for stat in resp.get("TableStatistics", []):
                results.append(
                    TableStatistic(
                        schema_name=stat.get("SchemaName"),
                        table_name=stat.get("TableName"),
                        inserts=stat.get("Inserts", 0),
                        deletes=stat.get("Deletes", 0),
                        updates=stat.get("Updates", 0),
                        full_load_rows=stat.get("FullLoadRows", 0),
                        table_state=stat.get("TableState"),
                    )
                )
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_table_statistics") from exc
    return results


# ---------------------------------------------------------------------------
# Subnet groups
# ---------------------------------------------------------------------------


async def create_replication_subnet_group(
    replication_subnet_group_identifier: str,
    replication_subnet_group_description: str,
    subnet_ids: list[str],
    *,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ReplicationSubnetGroupResult:
    """Create a DMS replication subnet group (async)."""
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationSubnetGroupIdentifier": (replication_subnet_group_identifier),
        "ReplicationSubnetGroupDescription": (replication_subnet_group_description),
        "SubnetIds": subnet_ids,
    }
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateReplicationSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_replication_subnet_group") from exc
    sg = resp["ReplicationSubnetGroup"]
    return ReplicationSubnetGroupResult(
        replication_subnet_group_identifier=sg.get("ReplicationSubnetGroupIdentifier", ""),
        replication_subnet_group_description=sg.get("ReplicationSubnetGroupDescription"),
        vpc_id=sg.get("VpcId"),
        subnet_group_status=sg.get("SubnetGroupStatus"),
    )


async def add_tags_to_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags to resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("AddTagsToResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags to resource") from exc
    return None


async def apply_pending_maintenance_action(
    replication_instance_arn: str,
    apply_action: str,
    opt_in_type: str,
    region_name: str | None = None,
) -> ApplyPendingMaintenanceActionResult:
    """Apply pending maintenance action.

    Args:
        replication_instance_arn: Replication instance arn.
        apply_action: Apply action.
        opt_in_type: Opt in type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    kwargs["ApplyAction"] = apply_action
    kwargs["OptInType"] = opt_in_type
    try:
        resp = await client.call("ApplyPendingMaintenanceAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to apply pending maintenance action") from exc
    return ApplyPendingMaintenanceActionResult(
        resource_pending_maintenance_actions=resp.get("ResourcePendingMaintenanceActions"),
    )


async def batch_start_recommendations(
    *,
    data: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> BatchStartRecommendationsResult:
    """Batch start recommendations.

    Args:
        data: Data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if data is not None:
        kwargs["Data"] = data
    try:
        resp = await client.call("BatchStartRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch start recommendations") from exc
    return BatchStartRecommendationsResult(
        error_entries=resp.get("ErrorEntries"),
    )


async def cancel_metadata_model_conversion(
    migration_project_identifier: str,
    request_identifier: str,
    region_name: str | None = None,
) -> CancelMetadataModelConversionResult:
    """Cancel metadata model conversion.

    Args:
        migration_project_identifier: Migration project identifier.
        request_identifier: Request identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["RequestIdentifier"] = request_identifier
    try:
        resp = await client.call("CancelMetadataModelConversion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel metadata model conversion") from exc
    return CancelMetadataModelConversionResult(
        request=resp.get("Request"),
    )


async def cancel_metadata_model_creation(
    migration_project_identifier: str,
    request_identifier: str,
    region_name: str | None = None,
) -> CancelMetadataModelCreationResult:
    """Cancel metadata model creation.

    Args:
        migration_project_identifier: Migration project identifier.
        request_identifier: Request identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["RequestIdentifier"] = request_identifier
    try:
        resp = await client.call("CancelMetadataModelCreation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel metadata model creation") from exc
    return CancelMetadataModelCreationResult(
        request=resp.get("Request"),
    )


async def cancel_replication_task_assessment_run(
    replication_task_assessment_run_arn: str,
    region_name: str | None = None,
) -> CancelReplicationTaskAssessmentRunResult:
    """Cancel replication task assessment run.

    Args:
        replication_task_assessment_run_arn: Replication task assessment run arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskAssessmentRunArn"] = replication_task_assessment_run_arn
    try:
        resp = await client.call("CancelReplicationTaskAssessmentRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel replication task assessment run") from exc
    return CancelReplicationTaskAssessmentRunResult(
        replication_task_assessment_run=resp.get("ReplicationTaskAssessmentRun"),
    )


async def create_data_migration(
    migration_project_identifier: str,
    data_migration_type: str,
    service_access_role_arn: str,
    *,
    data_migration_name: str | None = None,
    enable_cloudwatch_logs: bool | None = None,
    source_data_settings: list[dict[str, Any]] | None = None,
    target_data_settings: list[dict[str, Any]] | None = None,
    number_of_jobs: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    selection_rules: str | None = None,
    region_name: str | None = None,
) -> CreateDataMigrationResult:
    """Create data migration.

    Args:
        migration_project_identifier: Migration project identifier.
        data_migration_type: Data migration type.
        service_access_role_arn: Service access role arn.
        data_migration_name: Data migration name.
        enable_cloudwatch_logs: Enable cloudwatch logs.
        source_data_settings: Source data settings.
        target_data_settings: Target data settings.
        number_of_jobs: Number of jobs.
        tags: Tags.
        selection_rules: Selection rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["DataMigrationType"] = data_migration_type
    kwargs["ServiceAccessRoleArn"] = service_access_role_arn
    if data_migration_name is not None:
        kwargs["DataMigrationName"] = data_migration_name
    if enable_cloudwatch_logs is not None:
        kwargs["EnableCloudwatchLogs"] = enable_cloudwatch_logs
    if source_data_settings is not None:
        kwargs["SourceDataSettings"] = source_data_settings
    if target_data_settings is not None:
        kwargs["TargetDataSettings"] = target_data_settings
    if number_of_jobs is not None:
        kwargs["NumberOfJobs"] = number_of_jobs
    if tags is not None:
        kwargs["Tags"] = tags
    if selection_rules is not None:
        kwargs["SelectionRules"] = selection_rules
    try:
        resp = await client.call("CreateDataMigration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data migration") from exc
    return CreateDataMigrationResult(
        data_migration=resp.get("DataMigration"),
    )


async def create_data_provider(
    engine: str,
    settings: dict[str, Any],
    *,
    data_provider_name: str | None = None,
    description: str | None = None,
    virtual: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDataProviderResult:
    """Create data provider.

    Args:
        engine: Engine.
        settings: Settings.
        data_provider_name: Data provider name.
        description: Description.
        virtual: Virtual.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    kwargs["Settings"] = settings
    if data_provider_name is not None:
        kwargs["DataProviderName"] = data_provider_name
    if description is not None:
        kwargs["Description"] = description
    if virtual is not None:
        kwargs["Virtual"] = virtual
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDataProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data provider") from exc
    return CreateDataProviderResult(
        data_provider=resp.get("DataProvider"),
    )


async def create_event_subscription(
    subscription_name: str,
    sns_topic_arn: str,
    *,
    source_type: str | None = None,
    event_categories: list[str] | None = None,
    source_ids: list[str] | None = None,
    enabled: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateEventSubscriptionResult:
    """Create event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        event_categories: Event categories.
        source_ids: Source ids.
        enabled: Enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if source_ids is not None:
        kwargs["SourceIds"] = source_ids
    if enabled is not None:
        kwargs["Enabled"] = enabled
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create event subscription") from exc
    return CreateEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def create_fleet_advisor_collector(
    collector_name: str,
    service_access_role_arn: str,
    s3_bucket_name: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateFleetAdvisorCollectorResult:
    """Create fleet advisor collector.

    Args:
        collector_name: Collector name.
        service_access_role_arn: Service access role arn.
        s3_bucket_name: S3 bucket name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectorName"] = collector_name
    kwargs["ServiceAccessRoleArn"] = service_access_role_arn
    kwargs["S3BucketName"] = s3_bucket_name
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("CreateFleetAdvisorCollector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create fleet advisor collector") from exc
    return CreateFleetAdvisorCollectorResult(
        collector_referenced_id=resp.get("CollectorReferencedId"),
        collector_name=resp.get("CollectorName"),
        description=resp.get("Description"),
        service_access_role_arn=resp.get("ServiceAccessRoleArn"),
        s3_bucket_name=resp.get("S3BucketName"),
    )


async def create_instance_profile(
    *,
    availability_zone: str | None = None,
    kms_key_arn: str | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    network_type: str | None = None,
    instance_profile_name: str | None = None,
    description: str | None = None,
    subnet_group_identifier: str | None = None,
    vpc_security_groups: list[str] | None = None,
    region_name: str | None = None,
) -> CreateInstanceProfileResult:
    """Create instance profile.

    Args:
        availability_zone: Availability zone.
        kms_key_arn: Kms key arn.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        network_type: Network type.
        instance_profile_name: Instance profile name.
        description: Description.
        subnet_group_identifier: Subnet group identifier.
        vpc_security_groups: Vpc security groups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if kms_key_arn is not None:
        kwargs["KmsKeyArn"] = kms_key_arn
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["Tags"] = tags
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if instance_profile_name is not None:
        kwargs["InstanceProfileName"] = instance_profile_name
    if description is not None:
        kwargs["Description"] = description
    if subnet_group_identifier is not None:
        kwargs["SubnetGroupIdentifier"] = subnet_group_identifier
    if vpc_security_groups is not None:
        kwargs["VpcSecurityGroups"] = vpc_security_groups
    try:
        resp = await client.call("CreateInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create instance profile") from exc
    return CreateInstanceProfileResult(
        instance_profile=resp.get("InstanceProfile"),
    )


async def create_migration_project(
    source_data_provider_descriptors: list[dict[str, Any]],
    target_data_provider_descriptors: list[dict[str, Any]],
    instance_profile_identifier: str,
    *,
    migration_project_name: str | None = None,
    transformation_rules: str | None = None,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    schema_conversion_application_attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateMigrationProjectResult:
    """Create migration project.

    Args:
        source_data_provider_descriptors: Source data provider descriptors.
        target_data_provider_descriptors: Target data provider descriptors.
        instance_profile_identifier: Instance profile identifier.
        migration_project_name: Migration project name.
        transformation_rules: Transformation rules.
        description: Description.
        tags: Tags.
        schema_conversion_application_attributes: Schema conversion application attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDataProviderDescriptors"] = source_data_provider_descriptors
    kwargs["TargetDataProviderDescriptors"] = target_data_provider_descriptors
    kwargs["InstanceProfileIdentifier"] = instance_profile_identifier
    if migration_project_name is not None:
        kwargs["MigrationProjectName"] = migration_project_name
    if transformation_rules is not None:
        kwargs["TransformationRules"] = transformation_rules
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    if schema_conversion_application_attributes is not None:
        kwargs["SchemaConversionApplicationAttributes"] = schema_conversion_application_attributes
    try:
        resp = await client.call("CreateMigrationProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create migration project") from exc
    return CreateMigrationProjectResult(
        migration_project=resp.get("MigrationProject"),
    )


async def create_replication_config(
    replication_config_identifier: str,
    source_endpoint_arn: str,
    target_endpoint_arn: str,
    compute_config: dict[str, Any],
    replication_type: str,
    table_mappings: str,
    *,
    replication_settings: str | None = None,
    supplemental_settings: str | None = None,
    resource_identifier: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateReplicationConfigResult:
    """Create replication config.

    Args:
        replication_config_identifier: Replication config identifier.
        source_endpoint_arn: Source endpoint arn.
        target_endpoint_arn: Target endpoint arn.
        compute_config: Compute config.
        replication_type: Replication type.
        table_mappings: Table mappings.
        replication_settings: Replication settings.
        supplemental_settings: Supplemental settings.
        resource_identifier: Resource identifier.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigIdentifier"] = replication_config_identifier
    kwargs["SourceEndpointArn"] = source_endpoint_arn
    kwargs["TargetEndpointArn"] = target_endpoint_arn
    kwargs["ComputeConfig"] = compute_config
    kwargs["ReplicationType"] = replication_type
    kwargs["TableMappings"] = table_mappings
    if replication_settings is not None:
        kwargs["ReplicationSettings"] = replication_settings
    if supplemental_settings is not None:
        kwargs["SupplementalSettings"] = supplemental_settings
    if resource_identifier is not None:
        kwargs["ResourceIdentifier"] = resource_identifier
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateReplicationConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create replication config") from exc
    return CreateReplicationConfigResult(
        replication_config=resp.get("ReplicationConfig"),
    )


async def delete_certificate(
    certificate_arn: str,
    region_name: str | None = None,
) -> DeleteCertificateResult:
    """Delete certificate.

    Args:
        certificate_arn: Certificate arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateArn"] = certificate_arn
    try:
        resp = await client.call("DeleteCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete certificate") from exc
    return DeleteCertificateResult(
        certificate=resp.get("Certificate"),
    )


async def delete_connection(
    endpoint_arn: str,
    replication_instance_arn: str,
    region_name: str | None = None,
) -> DeleteConnectionResult:
    """Delete connection.

    Args:
        endpoint_arn: Endpoint arn.
        replication_instance_arn: Replication instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    try:
        resp = await client.call("DeleteConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return DeleteConnectionResult(
        connection=resp.get("Connection"),
    )


async def delete_data_migration(
    data_migration_identifier: str,
    region_name: str | None = None,
) -> DeleteDataMigrationResult:
    """Delete data migration.

    Args:
        data_migration_identifier: Data migration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataMigrationIdentifier"] = data_migration_identifier
    try:
        resp = await client.call("DeleteDataMigration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data migration") from exc
    return DeleteDataMigrationResult(
        data_migration=resp.get("DataMigration"),
    )


async def delete_data_provider(
    data_provider_identifier: str,
    region_name: str | None = None,
) -> DeleteDataProviderResult:
    """Delete data provider.

    Args:
        data_provider_identifier: Data provider identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataProviderIdentifier"] = data_provider_identifier
    try:
        resp = await client.call("DeleteDataProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data provider") from exc
    return DeleteDataProviderResult(
        data_provider=resp.get("DataProvider"),
    )


async def delete_event_subscription(
    subscription_name: str,
    region_name: str | None = None,
) -> DeleteEventSubscriptionResult:
    """Delete event subscription.

    Args:
        subscription_name: Subscription name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    try:
        resp = await client.call("DeleteEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete event subscription") from exc
    return DeleteEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def delete_fleet_advisor_collector(
    collector_referenced_id: str,
    region_name: str | None = None,
) -> None:
    """Delete fleet advisor collector.

    Args:
        collector_referenced_id: Collector referenced id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CollectorReferencedId"] = collector_referenced_id
    try:
        await client.call("DeleteFleetAdvisorCollector", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete fleet advisor collector") from exc
    return None


async def delete_fleet_advisor_databases(
    database_ids: list[str],
    region_name: str | None = None,
) -> DeleteFleetAdvisorDatabasesResult:
    """Delete fleet advisor databases.

    Args:
        database_ids: Database ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseIds"] = database_ids
    try:
        resp = await client.call("DeleteFleetAdvisorDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete fleet advisor databases") from exc
    return DeleteFleetAdvisorDatabasesResult(
        database_ids=resp.get("DatabaseIds"),
    )


async def delete_instance_profile(
    instance_profile_identifier: str,
    region_name: str | None = None,
) -> DeleteInstanceProfileResult:
    """Delete instance profile.

    Args:
        instance_profile_identifier: Instance profile identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileIdentifier"] = instance_profile_identifier
    try:
        resp = await client.call("DeleteInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete instance profile") from exc
    return DeleteInstanceProfileResult(
        instance_profile=resp.get("InstanceProfile"),
    )


async def delete_migration_project(
    migration_project_identifier: str,
    region_name: str | None = None,
) -> DeleteMigrationProjectResult:
    """Delete migration project.

    Args:
        migration_project_identifier: Migration project identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    try:
        resp = await client.call("DeleteMigrationProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete migration project") from exc
    return DeleteMigrationProjectResult(
        migration_project=resp.get("MigrationProject"),
    )


async def delete_replication_config(
    replication_config_arn: str,
    region_name: str | None = None,
) -> DeleteReplicationConfigResult:
    """Delete replication config.

    Args:
        replication_config_arn: Replication config arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    try:
        resp = await client.call("DeleteReplicationConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete replication config") from exc
    return DeleteReplicationConfigResult(
        replication_config=resp.get("ReplicationConfig"),
    )


async def delete_replication_subnet_group(
    replication_subnet_group_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete replication subnet group.

    Args:
        replication_subnet_group_identifier: Replication subnet group identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationSubnetGroupIdentifier"] = replication_subnet_group_identifier
    try:
        await client.call("DeleteReplicationSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete replication subnet group") from exc
    return None


async def delete_replication_task_assessment_run(
    replication_task_assessment_run_arn: str,
    region_name: str | None = None,
) -> DeleteReplicationTaskAssessmentRunResult:
    """Delete replication task assessment run.

    Args:
        replication_task_assessment_run_arn: Replication task assessment run arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskAssessmentRunArn"] = replication_task_assessment_run_arn
    try:
        resp = await client.call("DeleteReplicationTaskAssessmentRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete replication task assessment run") from exc
    return DeleteReplicationTaskAssessmentRunResult(
        replication_task_assessment_run=resp.get("ReplicationTaskAssessmentRun"),
    )


async def describe_account_attributes(
    region_name: str | None = None,
) -> DescribeAccountAttributesResult:
    """Describe account attributes.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAccountAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account attributes") from exc
    return DescribeAccountAttributesResult(
        account_quotas=resp.get("AccountQuotas"),
        unique_account_identifier=resp.get("UniqueAccountIdentifier"),
    )


async def describe_applicable_individual_assessments(
    *,
    replication_task_arn: str | None = None,
    replication_instance_arn: str | None = None,
    replication_config_arn: str | None = None,
    source_engine_name: str | None = None,
    target_engine_name: str | None = None,
    migration_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeApplicableIndividualAssessmentsResult:
    """Describe applicable individual assessments.

    Args:
        replication_task_arn: Replication task arn.
        replication_instance_arn: Replication instance arn.
        replication_config_arn: Replication config arn.
        source_engine_name: Source engine name.
        target_engine_name: Target engine name.
        migration_type: Migration type.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if replication_task_arn is not None:
        kwargs["ReplicationTaskArn"] = replication_task_arn
    if replication_instance_arn is not None:
        kwargs["ReplicationInstanceArn"] = replication_instance_arn
    if replication_config_arn is not None:
        kwargs["ReplicationConfigArn"] = replication_config_arn
    if source_engine_name is not None:
        kwargs["SourceEngineName"] = source_engine_name
    if target_engine_name is not None:
        kwargs["TargetEngineName"] = target_engine_name
    if migration_type is not None:
        kwargs["MigrationType"] = migration_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeApplicableIndividualAssessments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe applicable individual assessments") from exc
    return DescribeApplicableIndividualAssessmentsResult(
        individual_assessment_names=resp.get("IndividualAssessmentNames"),
        marker=resp.get("Marker"),
    )


async def describe_certificates(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCertificatesResult:
    """Describe certificates.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe certificates") from exc
    return DescribeCertificatesResult(
        marker=resp.get("Marker"),
        certificates=resp.get("Certificates"),
    )


async def describe_conversion_configuration(
    migration_project_identifier: str,
    region_name: str | None = None,
) -> DescribeConversionConfigurationResult:
    """Describe conversion configuration.

    Args:
        migration_project_identifier: Migration project identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    try:
        resp = await client.call("DescribeConversionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe conversion configuration") from exc
    return DescribeConversionConfigurationResult(
        migration_project_identifier=resp.get("MigrationProjectIdentifier"),
        conversion_configuration=resp.get("ConversionConfiguration"),
    )


async def describe_data_migrations(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    without_settings: bool | None = None,
    without_statistics: bool | None = None,
    region_name: str | None = None,
) -> DescribeDataMigrationsResult:
    """Describe data migrations.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        without_settings: Without settings.
        without_statistics: Without statistics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if without_settings is not None:
        kwargs["WithoutSettings"] = without_settings
    if without_statistics is not None:
        kwargs["WithoutStatistics"] = without_statistics
    try:
        resp = await client.call("DescribeDataMigrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data migrations") from exc
    return DescribeDataMigrationsResult(
        data_migrations=resp.get("DataMigrations"),
        marker=resp.get("Marker"),
    )


async def describe_data_providers(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDataProvidersResult:
    """Describe data providers.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDataProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data providers") from exc
    return DescribeDataProvidersResult(
        marker=resp.get("Marker"),
        data_providers=resp.get("DataProviders"),
    )


async def describe_endpoint_settings(
    engine_name: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointSettingsResult:
    """Describe endpoint settings.

    Args:
        engine_name: Engine name.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EngineName"] = engine_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEndpointSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint settings") from exc
    return DescribeEndpointSettingsResult(
        marker=resp.get("Marker"),
        endpoint_settings=resp.get("EndpointSettings"),
    )


async def describe_endpoint_types(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointTypesResult:
    """Describe endpoint types.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEndpointTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint types") from exc
    return DescribeEndpointTypesResult(
        marker=resp.get("Marker"),
        supported_endpoint_types=resp.get("SupportedEndpointTypes"),
    )


async def describe_engine_versions(
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEngineVersionsResult:
    """Describe engine versions.

    Args:
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEngineVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe engine versions") from exc
    return DescribeEngineVersionsResult(
        engine_versions=resp.get("EngineVersions"),
        marker=resp.get("Marker"),
    )


async def describe_event_categories(
    *,
    source_type: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeEventCategoriesResult:
    """Describe event categories.

    Args:
        source_type: Source type.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeEventCategories", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event categories") from exc
    return DescribeEventCategoriesResult(
        event_category_group_list=resp.get("EventCategoryGroupList"),
    )


async def describe_event_subscriptions(
    *,
    subscription_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEventSubscriptionsResult:
    """Describe event subscriptions.

    Args:
        subscription_name: Subscription name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if subscription_name is not None:
        kwargs["SubscriptionName"] = subscription_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEventSubscriptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event subscriptions") from exc
    return DescribeEventSubscriptionsResult(
        marker=resp.get("Marker"),
        event_subscriptions_list=resp.get("EventSubscriptionsList"),
    )


async def describe_events(
    *,
    source_identifier: str | None = None,
    source_type: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    duration: int | None = None,
    event_categories: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEventsResult:
    """Describe events.

    Args:
        source_identifier: Source identifier.
        source_type: Source type.
        start_time: Start time.
        end_time: End time.
        duration: Duration.
        event_categories: Event categories.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if source_identifier is not None:
        kwargs["SourceIdentifier"] = source_identifier
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if duration is not None:
        kwargs["Duration"] = duration
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        marker=resp.get("Marker"),
        events=resp.get("Events"),
    )


async def describe_extension_pack_associations(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeExtensionPackAssociationsResult:
    """Describe extension pack associations.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeExtensionPackAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe extension pack associations") from exc
    return DescribeExtensionPackAssociationsResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_fleet_advisor_collectors(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFleetAdvisorCollectorsResult:
    """Describe fleet advisor collectors.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFleetAdvisorCollectors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet advisor collectors") from exc
    return DescribeFleetAdvisorCollectorsResult(
        collectors=resp.get("Collectors"),
        next_token=resp.get("NextToken"),
    )


async def describe_fleet_advisor_databases(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFleetAdvisorDatabasesResult:
    """Describe fleet advisor databases.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFleetAdvisorDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet advisor databases") from exc
    return DescribeFleetAdvisorDatabasesResult(
        databases=resp.get("Databases"),
        next_token=resp.get("NextToken"),
    )


async def describe_fleet_advisor_lsa_analysis(
    *,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFleetAdvisorLsaAnalysisResult:
    """Describe fleet advisor lsa analysis.

    Args:
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFleetAdvisorLsaAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet advisor lsa analysis") from exc
    return DescribeFleetAdvisorLsaAnalysisResult(
        analysis=resp.get("Analysis"),
        next_token=resp.get("NextToken"),
    )


async def describe_fleet_advisor_schema_object_summary(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFleetAdvisorSchemaObjectSummaryResult:
    """Describe fleet advisor schema object summary.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFleetAdvisorSchemaObjectSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet advisor schema object summary") from exc
    return DescribeFleetAdvisorSchemaObjectSummaryResult(
        fleet_advisor_schema_objects=resp.get("FleetAdvisorSchemaObjects"),
        next_token=resp.get("NextToken"),
    )


async def describe_fleet_advisor_schemas(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFleetAdvisorSchemasResult:
    """Describe fleet advisor schemas.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeFleetAdvisorSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet advisor schemas") from exc
    return DescribeFleetAdvisorSchemasResult(
        fleet_advisor_schemas=resp.get("FleetAdvisorSchemas"),
        next_token=resp.get("NextToken"),
    )


async def describe_instance_profiles(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeInstanceProfilesResult:
    """Describe instance profiles.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeInstanceProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe instance profiles") from exc
    return DescribeInstanceProfilesResult(
        marker=resp.get("Marker"),
        instance_profiles=resp.get("InstanceProfiles"),
    )


async def describe_metadata_model(
    selection_rules: str,
    migration_project_identifier: str,
    origin: str,
    region_name: str | None = None,
) -> DescribeMetadataModelResult:
    """Describe metadata model.

    Args:
        selection_rules: Selection rules.
        migration_project_identifier: Migration project identifier.
        origin: Origin.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SelectionRules"] = selection_rules
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["Origin"] = origin
    try:
        resp = await client.call("DescribeMetadataModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model") from exc
    return DescribeMetadataModelResult(
        metadata_model_name=resp.get("MetadataModelName"),
        metadata_model_type=resp.get("MetadataModelType"),
        target_metadata_models=resp.get("TargetMetadataModels"),
        definition=resp.get("Definition"),
    )


async def describe_metadata_model_assessments(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelAssessmentsResult:
    """Describe metadata model assessments.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelAssessments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model assessments") from exc
    return DescribeMetadataModelAssessmentsResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_metadata_model_children(
    selection_rules: str,
    migration_project_identifier: str,
    origin: str,
    *,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelChildrenResult:
    """Describe metadata model children.

    Args:
        selection_rules: Selection rules.
        migration_project_identifier: Migration project identifier.
        origin: Origin.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SelectionRules"] = selection_rules
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["Origin"] = origin
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelChildren", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model children") from exc
    return DescribeMetadataModelChildrenResult(
        marker=resp.get("Marker"),
        metadata_model_children=resp.get("MetadataModelChildren"),
    )


async def describe_metadata_model_conversions(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelConversionsResult:
    """Describe metadata model conversions.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelConversions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model conversions") from exc
    return DescribeMetadataModelConversionsResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_metadata_model_creations(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelCreationsResult:
    """Describe metadata model creations.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelCreations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model creations") from exc
    return DescribeMetadataModelCreationsResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_metadata_model_exports_as_script(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelExportsAsScriptResult:
    """Describe metadata model exports as script.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelExportsAsScript", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model exports as script") from exc
    return DescribeMetadataModelExportsAsScriptResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_metadata_model_exports_to_target(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelExportsToTargetResult:
    """Describe metadata model exports to target.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelExportsToTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model exports to target") from exc
    return DescribeMetadataModelExportsToTargetResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_metadata_model_imports(
    migration_project_identifier: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeMetadataModelImportsResult:
    """Describe metadata model imports.

    Args:
        migration_project_identifier: Migration project identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeMetadataModelImports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe metadata model imports") from exc
    return DescribeMetadataModelImportsResult(
        marker=resp.get("Marker"),
        requests=resp.get("Requests"),
    )


async def describe_migration_projects(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeMigrationProjectsResult:
    """Describe migration projects.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeMigrationProjects", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe migration projects") from exc
    return DescribeMigrationProjectsResult(
        marker=resp.get("Marker"),
        migration_projects=resp.get("MigrationProjects"),
    )


async def describe_orderable_replication_instances(
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeOrderableReplicationInstancesResult:
    """Describe orderable replication instances.

    Args:
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeOrderableReplicationInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe orderable replication instances") from exc
    return DescribeOrderableReplicationInstancesResult(
        orderable_replication_instances=resp.get("OrderableReplicationInstances"),
        marker=resp.get("Marker"),
    )


async def describe_pending_maintenance_actions(
    *,
    replication_instance_arn: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribePendingMaintenanceActionsResult:
    """Describe pending maintenance actions.

    Args:
        replication_instance_arn: Replication instance arn.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if replication_instance_arn is not None:
        kwargs["ReplicationInstanceArn"] = replication_instance_arn
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribePendingMaintenanceActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe pending maintenance actions") from exc
    return DescribePendingMaintenanceActionsResult(
        pending_maintenance_actions=resp.get("PendingMaintenanceActions"),
        marker=resp.get("Marker"),
    )


async def describe_recommendation_limitations(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeRecommendationLimitationsResult:
    """Describe recommendation limitations.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeRecommendationLimitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe recommendation limitations") from exc
    return DescribeRecommendationLimitationsResult(
        next_token=resp.get("NextToken"),
        limitations=resp.get("Limitations"),
    )


async def describe_recommendations(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeRecommendationsResult:
    """Describe recommendations.

    Args:
        filters: Filters.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("DescribeRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe recommendations") from exc
    return DescribeRecommendationsResult(
        next_token=resp.get("NextToken"),
        recommendations=resp.get("Recommendations"),
    )


async def describe_refresh_schemas_status(
    endpoint_arn: str,
    region_name: str | None = None,
) -> DescribeRefreshSchemasStatusResult:
    """Describe refresh schemas status.

    Args:
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    try:
        resp = await client.call("DescribeRefreshSchemasStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe refresh schemas status") from exc
    return DescribeRefreshSchemasStatusResult(
        refresh_schemas_status=resp.get("RefreshSchemasStatus"),
    )


async def describe_replication_configs(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationConfigsResult:
    """Describe replication configs.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationConfigs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication configs") from exc
    return DescribeReplicationConfigsResult(
        marker=resp.get("Marker"),
        replication_configs=resp.get("ReplicationConfigs"),
    )


async def describe_replication_instance_task_logs(
    replication_instance_arn: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationInstanceTaskLogsResult:
    """Describe replication instance task logs.

    Args:
        replication_instance_arn: Replication instance arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationInstanceTaskLogs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication instance task logs") from exc
    return DescribeReplicationInstanceTaskLogsResult(
        replication_instance_arn=resp.get("ReplicationInstanceArn"),
        replication_instance_task_logs=resp.get("ReplicationInstanceTaskLogs"),
        marker=resp.get("Marker"),
    )


async def describe_replication_subnet_groups(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationSubnetGroupsResult:
    """Describe replication subnet groups.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationSubnetGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication subnet groups") from exc
    return DescribeReplicationSubnetGroupsResult(
        marker=resp.get("Marker"),
        replication_subnet_groups=resp.get("ReplicationSubnetGroups"),
    )


async def describe_replication_table_statistics(
    replication_config_arn: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeReplicationTableStatisticsResult:
    """Describe replication table statistics.

    Args:
        replication_config_arn: Replication config arn.
        max_records: Max records.
        marker: Marker.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeReplicationTableStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication table statistics") from exc
    return DescribeReplicationTableStatisticsResult(
        replication_config_arn=resp.get("ReplicationConfigArn"),
        marker=resp.get("Marker"),
        replication_table_statistics=resp.get("ReplicationTableStatistics"),
    )


async def describe_replication_task_assessment_results(
    *,
    replication_task_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationTaskAssessmentResultsResult:
    """Describe replication task assessment results.

    Args:
        replication_task_arn: Replication task arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if replication_task_arn is not None:
        kwargs["ReplicationTaskArn"] = replication_task_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationTaskAssessmentResults", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication task assessment results") from exc
    return DescribeReplicationTaskAssessmentResultsResult(
        marker=resp.get("Marker"),
        bucket_name=resp.get("BucketName"),
        replication_task_assessment_results=resp.get("ReplicationTaskAssessmentResults"),
    )


async def describe_replication_task_assessment_runs(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationTaskAssessmentRunsResult:
    """Describe replication task assessment runs.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationTaskAssessmentRuns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication task assessment runs") from exc
    return DescribeReplicationTaskAssessmentRunsResult(
        marker=resp.get("Marker"),
        replication_task_assessment_runs=resp.get("ReplicationTaskAssessmentRuns"),
    )


async def describe_replication_task_individual_assessments(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationTaskIndividualAssessmentsResult:
    """Describe replication task individual assessments.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplicationTaskIndividualAssessments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to describe replication task individual assessments"
        ) from exc
    return DescribeReplicationTaskIndividualAssessmentsResult(
        marker=resp.get("Marker"),
        replication_task_individual_assessments=resp.get("ReplicationTaskIndividualAssessments"),
    )


async def describe_replications(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReplicationsResult:
    """Describe replications.

    Args:
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReplications", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replications") from exc
    return DescribeReplicationsResult(
        marker=resp.get("Marker"),
        replications=resp.get("Replications"),
    )


async def describe_schemas(
    endpoint_arn: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeSchemasResult:
    """Describe schemas.

    Args:
        endpoint_arn: Endpoint arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe schemas") from exc
    return DescribeSchemasResult(
        marker=resp.get("Marker"),
        schemas=resp.get("Schemas"),
    )


async def export_metadata_model_assessment(
    migration_project_identifier: str,
    selection_rules: str,
    *,
    file_name: str | None = None,
    assessment_report_types: list[str] | None = None,
    region_name: str | None = None,
) -> ExportMetadataModelAssessmentResult:
    """Export metadata model assessment.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        file_name: File name.
        assessment_report_types: Assessment report types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    if file_name is not None:
        kwargs["FileName"] = file_name
    if assessment_report_types is not None:
        kwargs["AssessmentReportTypes"] = assessment_report_types
    try:
        resp = await client.call("ExportMetadataModelAssessment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to export metadata model assessment") from exc
    return ExportMetadataModelAssessmentResult(
        pdf_report=resp.get("PdfReport"),
        csv_report=resp.get("CsvReport"),
    )


async def get_target_selection_rules(
    migration_project_identifier: str,
    selection_rules: str,
    region_name: str | None = None,
) -> GetTargetSelectionRulesResult:
    """Get target selection rules.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    try:
        resp = await client.call("GetTargetSelectionRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get target selection rules") from exc
    return GetTargetSelectionRulesResult(
        target_selection_rules=resp.get("TargetSelectionRules"),
    )


async def import_certificate(
    certificate_identifier: str,
    *,
    certificate_pem: str | None = None,
    certificate_wallet: bytes | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ImportCertificateResult:
    """Import certificate.

    Args:
        certificate_identifier: Certificate identifier.
        certificate_pem: Certificate pem.
        certificate_wallet: Certificate wallet.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateIdentifier"] = certificate_identifier
    if certificate_pem is not None:
        kwargs["CertificatePem"] = certificate_pem
    if certificate_wallet is not None:
        kwargs["CertificateWallet"] = certificate_wallet
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("ImportCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import certificate") from exc
    return ImportCertificateResult(
        certificate=resp.get("Certificate"),
    )


async def list_tags_for_resource(
    *,
    resource_arn: str | None = None,
    resource_arn_list: list[str] | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        resource_arn_list: Resource arn list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if resource_arn is not None:
        kwargs["ResourceArn"] = resource_arn
    if resource_arn_list is not None:
        kwargs["ResourceArnList"] = resource_arn_list
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tag_list=resp.get("TagList"),
    )


async def modify_conversion_configuration(
    migration_project_identifier: str,
    conversion_configuration: str,
    region_name: str | None = None,
) -> ModifyConversionConfigurationResult:
    """Modify conversion configuration.

    Args:
        migration_project_identifier: Migration project identifier.
        conversion_configuration: Conversion configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["ConversionConfiguration"] = conversion_configuration
    try:
        resp = await client.call("ModifyConversionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify conversion configuration") from exc
    return ModifyConversionConfigurationResult(
        migration_project_identifier=resp.get("MigrationProjectIdentifier"),
    )


async def modify_data_migration(
    data_migration_identifier: str,
    *,
    data_migration_name: str | None = None,
    enable_cloudwatch_logs: bool | None = None,
    service_access_role_arn: str | None = None,
    data_migration_type: str | None = None,
    source_data_settings: list[dict[str, Any]] | None = None,
    target_data_settings: list[dict[str, Any]] | None = None,
    number_of_jobs: int | None = None,
    selection_rules: str | None = None,
    region_name: str | None = None,
) -> ModifyDataMigrationResult:
    """Modify data migration.

    Args:
        data_migration_identifier: Data migration identifier.
        data_migration_name: Data migration name.
        enable_cloudwatch_logs: Enable cloudwatch logs.
        service_access_role_arn: Service access role arn.
        data_migration_type: Data migration type.
        source_data_settings: Source data settings.
        target_data_settings: Target data settings.
        number_of_jobs: Number of jobs.
        selection_rules: Selection rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataMigrationIdentifier"] = data_migration_identifier
    if data_migration_name is not None:
        kwargs["DataMigrationName"] = data_migration_name
    if enable_cloudwatch_logs is not None:
        kwargs["EnableCloudwatchLogs"] = enable_cloudwatch_logs
    if service_access_role_arn is not None:
        kwargs["ServiceAccessRoleArn"] = service_access_role_arn
    if data_migration_type is not None:
        kwargs["DataMigrationType"] = data_migration_type
    if source_data_settings is not None:
        kwargs["SourceDataSettings"] = source_data_settings
    if target_data_settings is not None:
        kwargs["TargetDataSettings"] = target_data_settings
    if number_of_jobs is not None:
        kwargs["NumberOfJobs"] = number_of_jobs
    if selection_rules is not None:
        kwargs["SelectionRules"] = selection_rules
    try:
        resp = await client.call("ModifyDataMigration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify data migration") from exc
    return ModifyDataMigrationResult(
        data_migration=resp.get("DataMigration"),
    )


async def modify_data_provider(
    data_provider_identifier: str,
    *,
    data_provider_name: str | None = None,
    description: str | None = None,
    engine: str | None = None,
    virtual: bool | None = None,
    exact_settings: bool | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ModifyDataProviderResult:
    """Modify data provider.

    Args:
        data_provider_identifier: Data provider identifier.
        data_provider_name: Data provider name.
        description: Description.
        engine: Engine.
        virtual: Virtual.
        exact_settings: Exact settings.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataProviderIdentifier"] = data_provider_identifier
    if data_provider_name is not None:
        kwargs["DataProviderName"] = data_provider_name
    if description is not None:
        kwargs["Description"] = description
    if engine is not None:
        kwargs["Engine"] = engine
    if virtual is not None:
        kwargs["Virtual"] = virtual
    if exact_settings is not None:
        kwargs["ExactSettings"] = exact_settings
    if settings is not None:
        kwargs["Settings"] = settings
    try:
        resp = await client.call("ModifyDataProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify data provider") from exc
    return ModifyDataProviderResult(
        data_provider=resp.get("DataProvider"),
    )


async def modify_event_subscription(
    subscription_name: str,
    *,
    sns_topic_arn: str | None = None,
    source_type: str | None = None,
    event_categories: list[str] | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> ModifyEventSubscriptionResult:
    """Modify event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        event_categories: Event categories.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    if sns_topic_arn is not None:
        kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = await client.call("ModifyEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify event subscription") from exc
    return ModifyEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def modify_instance_profile(
    instance_profile_identifier: str,
    *,
    availability_zone: str | None = None,
    kms_key_arn: str | None = None,
    publicly_accessible: bool | None = None,
    network_type: str | None = None,
    instance_profile_name: str | None = None,
    description: str | None = None,
    subnet_group_identifier: str | None = None,
    vpc_security_groups: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyInstanceProfileResult:
    """Modify instance profile.

    Args:
        instance_profile_identifier: Instance profile identifier.
        availability_zone: Availability zone.
        kms_key_arn: Kms key arn.
        publicly_accessible: Publicly accessible.
        network_type: Network type.
        instance_profile_name: Instance profile name.
        description: Description.
        subnet_group_identifier: Subnet group identifier.
        vpc_security_groups: Vpc security groups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileIdentifier"] = instance_profile_identifier
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if kms_key_arn is not None:
        kwargs["KmsKeyArn"] = kms_key_arn
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if instance_profile_name is not None:
        kwargs["InstanceProfileName"] = instance_profile_name
    if description is not None:
        kwargs["Description"] = description
    if subnet_group_identifier is not None:
        kwargs["SubnetGroupIdentifier"] = subnet_group_identifier
    if vpc_security_groups is not None:
        kwargs["VpcSecurityGroups"] = vpc_security_groups
    try:
        resp = await client.call("ModifyInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify instance profile") from exc
    return ModifyInstanceProfileResult(
        instance_profile=resp.get("InstanceProfile"),
    )


async def modify_migration_project(
    migration_project_identifier: str,
    *,
    migration_project_name: str | None = None,
    source_data_provider_descriptors: list[dict[str, Any]] | None = None,
    target_data_provider_descriptors: list[dict[str, Any]] | None = None,
    instance_profile_identifier: str | None = None,
    transformation_rules: str | None = None,
    description: str | None = None,
    schema_conversion_application_attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ModifyMigrationProjectResult:
    """Modify migration project.

    Args:
        migration_project_identifier: Migration project identifier.
        migration_project_name: Migration project name.
        source_data_provider_descriptors: Source data provider descriptors.
        target_data_provider_descriptors: Target data provider descriptors.
        instance_profile_identifier: Instance profile identifier.
        transformation_rules: Transformation rules.
        description: Description.
        schema_conversion_application_attributes: Schema conversion application attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    if migration_project_name is not None:
        kwargs["MigrationProjectName"] = migration_project_name
    if source_data_provider_descriptors is not None:
        kwargs["SourceDataProviderDescriptors"] = source_data_provider_descriptors
    if target_data_provider_descriptors is not None:
        kwargs["TargetDataProviderDescriptors"] = target_data_provider_descriptors
    if instance_profile_identifier is not None:
        kwargs["InstanceProfileIdentifier"] = instance_profile_identifier
    if transformation_rules is not None:
        kwargs["TransformationRules"] = transformation_rules
    if description is not None:
        kwargs["Description"] = description
    if schema_conversion_application_attributes is not None:
        kwargs["SchemaConversionApplicationAttributes"] = schema_conversion_application_attributes
    try:
        resp = await client.call("ModifyMigrationProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify migration project") from exc
    return ModifyMigrationProjectResult(
        migration_project=resp.get("MigrationProject"),
    )


async def modify_replication_config(
    replication_config_arn: str,
    *,
    replication_config_identifier: str | None = None,
    replication_type: str | None = None,
    table_mappings: str | None = None,
    replication_settings: str | None = None,
    supplemental_settings: str | None = None,
    compute_config: dict[str, Any] | None = None,
    source_endpoint_arn: str | None = None,
    target_endpoint_arn: str | None = None,
    region_name: str | None = None,
) -> ModifyReplicationConfigResult:
    """Modify replication config.

    Args:
        replication_config_arn: Replication config arn.
        replication_config_identifier: Replication config identifier.
        replication_type: Replication type.
        table_mappings: Table mappings.
        replication_settings: Replication settings.
        supplemental_settings: Supplemental settings.
        compute_config: Compute config.
        source_endpoint_arn: Source endpoint arn.
        target_endpoint_arn: Target endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    if replication_config_identifier is not None:
        kwargs["ReplicationConfigIdentifier"] = replication_config_identifier
    if replication_type is not None:
        kwargs["ReplicationType"] = replication_type
    if table_mappings is not None:
        kwargs["TableMappings"] = table_mappings
    if replication_settings is not None:
        kwargs["ReplicationSettings"] = replication_settings
    if supplemental_settings is not None:
        kwargs["SupplementalSettings"] = supplemental_settings
    if compute_config is not None:
        kwargs["ComputeConfig"] = compute_config
    if source_endpoint_arn is not None:
        kwargs["SourceEndpointArn"] = source_endpoint_arn
    if target_endpoint_arn is not None:
        kwargs["TargetEndpointArn"] = target_endpoint_arn
    try:
        resp = await client.call("ModifyReplicationConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify replication config") from exc
    return ModifyReplicationConfigResult(
        replication_config=resp.get("ReplicationConfig"),
    )


async def modify_replication_subnet_group(
    replication_subnet_group_identifier: str,
    subnet_ids: list[str],
    *,
    replication_subnet_group_description: str | None = None,
    region_name: str | None = None,
) -> ModifyReplicationSubnetGroupResult:
    """Modify replication subnet group.

    Args:
        replication_subnet_group_identifier: Replication subnet group identifier.
        subnet_ids: Subnet ids.
        replication_subnet_group_description: Replication subnet group description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationSubnetGroupIdentifier"] = replication_subnet_group_identifier
    kwargs["SubnetIds"] = subnet_ids
    if replication_subnet_group_description is not None:
        kwargs["ReplicationSubnetGroupDescription"] = replication_subnet_group_description
    try:
        resp = await client.call("ModifyReplicationSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify replication subnet group") from exc
    return ModifyReplicationSubnetGroupResult(
        replication_subnet_group=resp.get("ReplicationSubnetGroup"),
    )


async def modify_replication_task(
    replication_task_arn: str,
    *,
    replication_task_identifier: str | None = None,
    migration_type: str | None = None,
    table_mappings: str | None = None,
    replication_task_settings: str | None = None,
    cdc_start_time: str | None = None,
    cdc_start_position: str | None = None,
    cdc_stop_position: str | None = None,
    task_data: str | None = None,
    region_name: str | None = None,
) -> ModifyReplicationTaskResult:
    """Modify replication task.

    Args:
        replication_task_arn: Replication task arn.
        replication_task_identifier: Replication task identifier.
        migration_type: Migration type.
        table_mappings: Table mappings.
        replication_task_settings: Replication task settings.
        cdc_start_time: Cdc start time.
        cdc_start_position: Cdc start position.
        cdc_stop_position: Cdc stop position.
        task_data: Task data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskArn"] = replication_task_arn
    if replication_task_identifier is not None:
        kwargs["ReplicationTaskIdentifier"] = replication_task_identifier
    if migration_type is not None:
        kwargs["MigrationType"] = migration_type
    if table_mappings is not None:
        kwargs["TableMappings"] = table_mappings
    if replication_task_settings is not None:
        kwargs["ReplicationTaskSettings"] = replication_task_settings
    if cdc_start_time is not None:
        kwargs["CdcStartTime"] = cdc_start_time
    if cdc_start_position is not None:
        kwargs["CdcStartPosition"] = cdc_start_position
    if cdc_stop_position is not None:
        kwargs["CdcStopPosition"] = cdc_stop_position
    if task_data is not None:
        kwargs["TaskData"] = task_data
    try:
        resp = await client.call("ModifyReplicationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify replication task") from exc
    return ModifyReplicationTaskResult(
        replication_task=resp.get("ReplicationTask"),
    )


async def move_replication_task(
    replication_task_arn: str,
    target_replication_instance_arn: str,
    region_name: str | None = None,
) -> MoveReplicationTaskResult:
    """Move replication task.

    Args:
        replication_task_arn: Replication task arn.
        target_replication_instance_arn: Target replication instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskArn"] = replication_task_arn
    kwargs["TargetReplicationInstanceArn"] = target_replication_instance_arn
    try:
        resp = await client.call("MoveReplicationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to move replication task") from exc
    return MoveReplicationTaskResult(
        replication_task=resp.get("ReplicationTask"),
    )


async def reboot_replication_instance(
    replication_instance_arn: str,
    *,
    force_failover: bool | None = None,
    force_planned_failover: bool | None = None,
    region_name: str | None = None,
) -> RebootReplicationInstanceResult:
    """Reboot replication instance.

    Args:
        replication_instance_arn: Replication instance arn.
        force_failover: Force failover.
        force_planned_failover: Force planned failover.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    if force_failover is not None:
        kwargs["ForceFailover"] = force_failover
    if force_planned_failover is not None:
        kwargs["ForcePlannedFailover"] = force_planned_failover
    try:
        resp = await client.call("RebootReplicationInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reboot replication instance") from exc
    return RebootReplicationInstanceResult(
        replication_instance=resp.get("ReplicationInstance"),
    )


async def refresh_schemas(
    endpoint_arn: str,
    replication_instance_arn: str,
    region_name: str | None = None,
) -> RefreshSchemasResult:
    """Refresh schemas.

    Args:
        endpoint_arn: Endpoint arn.
        replication_instance_arn: Replication instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointArn"] = endpoint_arn
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    try:
        resp = await client.call("RefreshSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to refresh schemas") from exc
    return RefreshSchemasResult(
        refresh_schemas_status=resp.get("RefreshSchemasStatus"),
    )


async def reload_replication_tables(
    replication_config_arn: str,
    tables_to_reload: list[dict[str, Any]],
    *,
    reload_option: str | None = None,
    region_name: str | None = None,
) -> ReloadReplicationTablesResult:
    """Reload replication tables.

    Args:
        replication_config_arn: Replication config arn.
        tables_to_reload: Tables to reload.
        reload_option: Reload option.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    kwargs["TablesToReload"] = tables_to_reload
    if reload_option is not None:
        kwargs["ReloadOption"] = reload_option
    try:
        resp = await client.call("ReloadReplicationTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reload replication tables") from exc
    return ReloadReplicationTablesResult(
        replication_config_arn=resp.get("ReplicationConfigArn"),
    )


async def reload_tables(
    replication_task_arn: str,
    tables_to_reload: list[dict[str, Any]],
    *,
    reload_option: str | None = None,
    region_name: str | None = None,
) -> ReloadTablesResult:
    """Reload tables.

    Args:
        replication_task_arn: Replication task arn.
        tables_to_reload: Tables to reload.
        reload_option: Reload option.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskArn"] = replication_task_arn
    kwargs["TablesToReload"] = tables_to_reload
    if reload_option is not None:
        kwargs["ReloadOption"] = reload_option
    try:
        resp = await client.call("ReloadTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reload tables") from exc
    return ReloadTablesResult(
        replication_task_arn=resp.get("ReplicationTaskArn"),
    )


async def remove_tags_from_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags from resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("RemoveTagsFromResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return None


async def run_connection(
    replication_instance_arn: str,
    endpoint_arn: str,
    region_name: str | None = None,
) -> RunConnectionResult:
    """Run connection.

    Args:
        replication_instance_arn: Replication instance arn.
        endpoint_arn: Endpoint arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationInstanceArn"] = replication_instance_arn
    kwargs["EndpointArn"] = endpoint_arn
    try:
        resp = await client.call("TestConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run connection") from exc
    return RunConnectionResult(
        connection=resp.get("Connection"),
    )


async def run_fleet_advisor_lsa_analysis(
    region_name: str | None = None,
) -> RunFleetAdvisorLsaAnalysisResult:
    """Run fleet advisor lsa analysis.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("RunFleetAdvisorLsaAnalysis", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run fleet advisor lsa analysis") from exc
    return RunFleetAdvisorLsaAnalysisResult(
        lsa_analysis_id=resp.get("LsaAnalysisId"),
        status=resp.get("Status"),
    )


async def start_data_migration(
    data_migration_identifier: str,
    start_type: str,
    region_name: str | None = None,
) -> StartDataMigrationResult:
    """Start data migration.

    Args:
        data_migration_identifier: Data migration identifier.
        start_type: Start type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataMigrationIdentifier"] = data_migration_identifier
    kwargs["StartType"] = start_type
    try:
        resp = await client.call("StartDataMigration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start data migration") from exc
    return StartDataMigrationResult(
        data_migration=resp.get("DataMigration"),
    )


async def start_extension_pack_association(
    migration_project_identifier: str,
    region_name: str | None = None,
) -> StartExtensionPackAssociationResult:
    """Start extension pack association.

    Args:
        migration_project_identifier: Migration project identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    try:
        resp = await client.call("StartExtensionPackAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start extension pack association") from exc
    return StartExtensionPackAssociationResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_assessment(
    migration_project_identifier: str,
    selection_rules: str,
    region_name: str | None = None,
) -> StartMetadataModelAssessmentResult:
    """Start metadata model assessment.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    try:
        resp = await client.call("StartMetadataModelAssessment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model assessment") from exc
    return StartMetadataModelAssessmentResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_conversion(
    migration_project_identifier: str,
    selection_rules: str,
    region_name: str | None = None,
) -> StartMetadataModelConversionResult:
    """Start metadata model conversion.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    try:
        resp = await client.call("StartMetadataModelConversion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model conversion") from exc
    return StartMetadataModelConversionResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_creation(
    migration_project_identifier: str,
    selection_rules: str,
    metadata_model_name: str,
    properties: dict[str, Any],
    region_name: str | None = None,
) -> StartMetadataModelCreationResult:
    """Start metadata model creation.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        metadata_model_name: Metadata model name.
        properties: Properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    kwargs["MetadataModelName"] = metadata_model_name
    kwargs["Properties"] = properties
    try:
        resp = await client.call("StartMetadataModelCreation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model creation") from exc
    return StartMetadataModelCreationResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_export_as_script(
    migration_project_identifier: str,
    selection_rules: str,
    origin: str,
    *,
    file_name: str | None = None,
    region_name: str | None = None,
) -> StartMetadataModelExportAsScriptResult:
    """Start metadata model export as script.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        origin: Origin.
        file_name: File name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    kwargs["Origin"] = origin
    if file_name is not None:
        kwargs["FileName"] = file_name
    try:
        resp = await client.call("StartMetadataModelExportAsScript", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model export as script") from exc
    return StartMetadataModelExportAsScriptResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_export_to_target(
    migration_project_identifier: str,
    selection_rules: str,
    *,
    overwrite_extension_pack: bool | None = None,
    region_name: str | None = None,
) -> StartMetadataModelExportToTargetResult:
    """Start metadata model export to target.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        overwrite_extension_pack: Overwrite extension pack.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    if overwrite_extension_pack is not None:
        kwargs["OverwriteExtensionPack"] = overwrite_extension_pack
    try:
        resp = await client.call("StartMetadataModelExportToTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model export to target") from exc
    return StartMetadataModelExportToTargetResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_metadata_model_import(
    migration_project_identifier: str,
    selection_rules: str,
    origin: str,
    *,
    refresh: bool | None = None,
    region_name: str | None = None,
) -> StartMetadataModelImportResult:
    """Start metadata model import.

    Args:
        migration_project_identifier: Migration project identifier.
        selection_rules: Selection rules.
        origin: Origin.
        refresh: Refresh.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MigrationProjectIdentifier"] = migration_project_identifier
    kwargs["SelectionRules"] = selection_rules
    kwargs["Origin"] = origin
    if refresh is not None:
        kwargs["Refresh"] = refresh
    try:
        resp = await client.call("StartMetadataModelImport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start metadata model import") from exc
    return StartMetadataModelImportResult(
        request_identifier=resp.get("RequestIdentifier"),
    )


async def start_recommendations(
    database_id: str,
    settings: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Start recommendations.

    Args:
        database_id: Database id.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DatabaseId"] = database_id
    kwargs["Settings"] = settings
    try:
        await client.call("StartRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start recommendations") from exc
    return None


async def start_replication(
    replication_config_arn: str,
    start_replication_type: str,
    *,
    premigration_assessment_settings: str | None = None,
    cdc_start_time: str | None = None,
    cdc_start_position: str | None = None,
    cdc_stop_position: str | None = None,
    region_name: str | None = None,
) -> StartReplicationResult:
    """Start replication.

    Args:
        replication_config_arn: Replication config arn.
        start_replication_type: Start replication type.
        premigration_assessment_settings: Premigration assessment settings.
        cdc_start_time: Cdc start time.
        cdc_start_position: Cdc start position.
        cdc_stop_position: Cdc stop position.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    kwargs["StartReplicationType"] = start_replication_type
    if premigration_assessment_settings is not None:
        kwargs["PremigrationAssessmentSettings"] = premigration_assessment_settings
    if cdc_start_time is not None:
        kwargs["CdcStartTime"] = cdc_start_time
    if cdc_start_position is not None:
        kwargs["CdcStartPosition"] = cdc_start_position
    if cdc_stop_position is not None:
        kwargs["CdcStopPosition"] = cdc_stop_position
    try:
        resp = await client.call("StartReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start replication") from exc
    return StartReplicationResult(
        replication=resp.get("Replication"),
    )


async def start_replication_task_assessment(
    replication_task_arn: str,
    region_name: str | None = None,
) -> StartReplicationTaskAssessmentResult:
    """Start replication task assessment.

    Args:
        replication_task_arn: Replication task arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskArn"] = replication_task_arn
    try:
        resp = await client.call("StartReplicationTaskAssessment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start replication task assessment") from exc
    return StartReplicationTaskAssessmentResult(
        replication_task=resp.get("ReplicationTask"),
    )


async def start_replication_task_assessment_run(
    replication_task_arn: str,
    service_access_role_arn: str,
    result_location_bucket: str,
    assessment_run_name: str,
    *,
    result_location_folder: str | None = None,
    result_encryption_mode: str | None = None,
    result_kms_key_arn: str | None = None,
    include_only: list[str] | None = None,
    exclude: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartReplicationTaskAssessmentRunResult:
    """Start replication task assessment run.

    Args:
        replication_task_arn: Replication task arn.
        service_access_role_arn: Service access role arn.
        result_location_bucket: Result location bucket.
        assessment_run_name: Assessment run name.
        result_location_folder: Result location folder.
        result_encryption_mode: Result encryption mode.
        result_kms_key_arn: Result kms key arn.
        include_only: Include only.
        exclude: Exclude.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationTaskArn"] = replication_task_arn
    kwargs["ServiceAccessRoleArn"] = service_access_role_arn
    kwargs["ResultLocationBucket"] = result_location_bucket
    kwargs["AssessmentRunName"] = assessment_run_name
    if result_location_folder is not None:
        kwargs["ResultLocationFolder"] = result_location_folder
    if result_encryption_mode is not None:
        kwargs["ResultEncryptionMode"] = result_encryption_mode
    if result_kms_key_arn is not None:
        kwargs["ResultKmsKeyArn"] = result_kms_key_arn
    if include_only is not None:
        kwargs["IncludeOnly"] = include_only
    if exclude is not None:
        kwargs["Exclude"] = exclude
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("StartReplicationTaskAssessmentRun", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start replication task assessment run") from exc
    return StartReplicationTaskAssessmentRunResult(
        replication_task_assessment_run=resp.get("ReplicationTaskAssessmentRun"),
    )


async def stop_data_migration(
    data_migration_identifier: str,
    region_name: str | None = None,
) -> StopDataMigrationResult:
    """Stop data migration.

    Args:
        data_migration_identifier: Data migration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataMigrationIdentifier"] = data_migration_identifier
    try:
        resp = await client.call("StopDataMigration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop data migration") from exc
    return StopDataMigrationResult(
        data_migration=resp.get("DataMigration"),
    )


async def stop_replication(
    replication_config_arn: str,
    region_name: str | None = None,
) -> StopReplicationResult:
    """Stop replication.

    Args:
        replication_config_arn: Replication config arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationConfigArn"] = replication_config_arn
    try:
        resp = await client.call("StopReplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop replication") from exc
    return StopReplicationResult(
        replication=resp.get("Replication"),
    )


async def update_subscriptions_to_event_bridge(
    *,
    force_move: bool | None = None,
    region_name: str | None = None,
) -> UpdateSubscriptionsToEventBridgeResult:
    """Update subscriptions to event bridge.

    Args:
        force_move: Force move.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("dms", region_name)
    kwargs: dict[str, Any] = {}
    if force_move is not None:
        kwargs["ForceMove"] = force_move
    try:
        resp = await client.call("UpdateSubscriptionsToEventBridge", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update subscriptions to event bridge") from exc
    return UpdateSubscriptionsToEventBridgeResult(
        result=resp.get("Result"),
    )
