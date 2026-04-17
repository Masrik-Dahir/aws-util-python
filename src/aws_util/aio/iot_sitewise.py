"""Native async IoT SiteWise utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error
from aws_util.iot_sitewise import (
    AssetModelResult,
    AssetResult,
    BatchAssociateProjectAssetsResult,
    BatchDisassociateProjectAssetsResult,
    BatchGetAssetPropertyAggregatesResult,
    BatchGetAssetPropertyValueHistoryResult,
    BatchGetAssetPropertyValueResult,
    BatchPutAssetPropertyValueResult,
    CreateAccessPolicyResult,
    CreateAssetModelCompositeModelResult,
    CreateBulkImportJobResult,
    CreateComputationModelResult,
    CreateDatasetResult,
    CreateGatewayResult,
    CreateProjectResult,
    DashboardResult,
    DeleteAssetModelCompositeModelResult,
    DeleteAssetModelInterfaceRelationshipResult,
    DeleteComputationModelResult,
    DeleteDatasetResult,
    DescribeAccessPolicyResult,
    DescribeActionResult,
    DescribeAssetCompositeModelResult,
    DescribeAssetModelCompositeModelResult,
    DescribeAssetModelInterfaceRelationshipResult,
    DescribeAssetPropertyResult,
    DescribeBulkImportJobResult,
    DescribeComputationModelExecutionSummaryResult,
    DescribeComputationModelResult,
    DescribeDashboardResult,
    DescribeDatasetResult,
    DescribeDefaultEncryptionConfigurationResult,
    DescribeExecutionResult,
    DescribeGatewayCapabilityConfigurationResult,
    DescribeGatewayResult,
    DescribeLoggingOptionsResult,
    DescribeProjectResult,
    DescribeStorageConfigurationResult,
    DescribeTimeSeriesResult,
    ExecuteActionResult,
    ExecuteQueryResult,
    GetInterpolatedAssetPropertyValuesResult,
    InvokeAssistantResult,
    ListAccessPoliciesResult,
    ListActionsResult,
    ListAssetModelCompositeModelsResult,
    ListAssetModelPropertiesResult,
    ListAssetPropertiesResult,
    ListAssetRelationshipsResult,
    ListAssociatedAssetsResult,
    ListBulkImportJobsResult,
    ListCompositionRelationshipsResult,
    ListComputationModelDataBindingUsagesResult,
    ListComputationModelResolveToResourcesResult,
    ListComputationModelsResult,
    ListDatasetsResult,
    ListExecutionsResult,
    ListGatewaysResult,
    ListInterfaceRelationshipsResult,
    ListProjectAssetsResult,
    ListProjectsResult,
    ListTagsForResourceResult,
    ListTimeSeriesResult,
    PortalResult,
    PropertyValueResult,
    PutAssetModelInterfaceRelationshipResult,
    PutDefaultEncryptionConfigurationResult,
    PutStorageConfigurationResult,
    UpdateAssetModelCompositeModelResult,
    UpdateAssetModelResult,
    UpdateAssetResult,
    UpdateComputationModelResult,
    UpdateDatasetResult,
    UpdateGatewayCapabilityConfigurationResult,
    UpdatePortalResult,
    _parse_asset,
    _parse_asset_model,
    _parse_dashboard,
    _parse_portal,
    _parse_property_value,
)

__all__ = [
    "AssetModelResult",
    "AssetResult",
    "BatchAssociateProjectAssetsResult",
    "BatchDisassociateProjectAssetsResult",
    "BatchGetAssetPropertyAggregatesResult",
    "BatchGetAssetPropertyValueHistoryResult",
    "BatchGetAssetPropertyValueResult",
    "BatchPutAssetPropertyValueResult",
    "CreateAccessPolicyResult",
    "CreateAssetModelCompositeModelResult",
    "CreateBulkImportJobResult",
    "CreateComputationModelResult",
    "CreateDatasetResult",
    "CreateGatewayResult",
    "CreateProjectResult",
    "DashboardResult",
    "DeleteAssetModelCompositeModelResult",
    "DeleteAssetModelInterfaceRelationshipResult",
    "DeleteComputationModelResult",
    "DeleteDatasetResult",
    "DescribeAccessPolicyResult",
    "DescribeActionResult",
    "DescribeAssetCompositeModelResult",
    "DescribeAssetModelCompositeModelResult",
    "DescribeAssetModelInterfaceRelationshipResult",
    "DescribeAssetPropertyResult",
    "DescribeBulkImportJobResult",
    "DescribeComputationModelExecutionSummaryResult",
    "DescribeComputationModelResult",
    "DescribeDashboardResult",
    "DescribeDatasetResult",
    "DescribeDefaultEncryptionConfigurationResult",
    "DescribeExecutionResult",
    "DescribeGatewayCapabilityConfigurationResult",
    "DescribeGatewayResult",
    "DescribeLoggingOptionsResult",
    "DescribeProjectResult",
    "DescribeStorageConfigurationResult",
    "DescribeTimeSeriesResult",
    "ExecuteActionResult",
    "ExecuteQueryResult",
    "GetInterpolatedAssetPropertyValuesResult",
    "InvokeAssistantResult",
    "ListAccessPoliciesResult",
    "ListActionsResult",
    "ListAssetModelCompositeModelsResult",
    "ListAssetModelPropertiesResult",
    "ListAssetPropertiesResult",
    "ListAssetRelationshipsResult",
    "ListAssociatedAssetsResult",
    "ListBulkImportJobsResult",
    "ListCompositionRelationshipsResult",
    "ListComputationModelDataBindingUsagesResult",
    "ListComputationModelResolveToResourcesResult",
    "ListComputationModelsResult",
    "ListDatasetsResult",
    "ListExecutionsResult",
    "ListGatewaysResult",
    "ListInterfaceRelationshipsResult",
    "ListProjectAssetsResult",
    "ListProjectsResult",
    "ListTagsForResourceResult",
    "ListTimeSeriesResult",
    "PortalResult",
    "PropertyValueResult",
    "PutAssetModelInterfaceRelationshipResult",
    "PutDefaultEncryptionConfigurationResult",
    "PutStorageConfigurationResult",
    "UpdateAssetModelCompositeModelResult",
    "UpdateAssetModelResult",
    "UpdateAssetResult",
    "UpdateComputationModelResult",
    "UpdateDatasetResult",
    "UpdateGatewayCapabilityConfigurationResult",
    "UpdatePortalResult",
    "associate_assets",
    "associate_time_series_to_asset_property",
    "batch_associate_project_assets",
    "batch_disassociate_project_assets",
    "batch_get_asset_property_aggregates",
    "batch_get_asset_property_value",
    "batch_get_asset_property_value_history",
    "batch_put_asset_property_value",
    "create_access_policy",
    "create_asset",
    "create_asset_model",
    "create_asset_model_composite_model",
    "create_bulk_import_job",
    "create_computation_model",
    "create_dashboard",
    "create_dataset",
    "create_gateway",
    "create_portal",
    "create_project",
    "delete_access_policy",
    "delete_asset",
    "delete_asset_model",
    "delete_asset_model_composite_model",
    "delete_asset_model_interface_relationship",
    "delete_computation_model",
    "delete_dashboard",
    "delete_dataset",
    "delete_gateway",
    "delete_portal",
    "delete_project",
    "delete_time_series",
    "describe_access_policy",
    "describe_action",
    "describe_asset",
    "describe_asset_composite_model",
    "describe_asset_model",
    "describe_asset_model_composite_model",
    "describe_asset_model_interface_relationship",
    "describe_asset_property",
    "describe_bulk_import_job",
    "describe_computation_model",
    "describe_computation_model_execution_summary",
    "describe_dashboard",
    "describe_dataset",
    "describe_default_encryption_configuration",
    "describe_execution",
    "describe_gateway",
    "describe_gateway_capability_configuration",
    "describe_logging_options",
    "describe_portal",
    "describe_project",
    "describe_storage_configuration",
    "describe_time_series",
    "disassociate_assets",
    "disassociate_time_series_from_asset_property",
    "execute_action",
    "execute_query",
    "get_asset_property_aggregates",
    "get_asset_property_value",
    "get_asset_property_value_history",
    "get_interpolated_asset_property_values",
    "invoke_assistant",
    "list_access_policies",
    "list_actions",
    "list_asset_model_composite_models",
    "list_asset_model_properties",
    "list_asset_models",
    "list_asset_properties",
    "list_asset_relationships",
    "list_assets",
    "list_associated_assets",
    "list_bulk_import_jobs",
    "list_composition_relationships",
    "list_computation_model_data_binding_usages",
    "list_computation_model_resolve_to_resources",
    "list_computation_models",
    "list_dashboards",
    "list_datasets",
    "list_executions",
    "list_gateways",
    "list_interface_relationships",
    "list_portals",
    "list_project_assets",
    "list_projects",
    "list_tags_for_resource",
    "list_time_series",
    "put_asset_model_interface_relationship",
    "put_asset_property_values",
    "put_default_encryption_configuration",
    "put_logging_options",
    "put_storage_configuration",
    "tag_resource",
    "untag_resource",
    "update_access_policy",
    "update_asset",
    "update_asset_model",
    "update_asset_model_composite_model",
    "update_asset_property",
    "update_computation_model",
    "update_dashboard",
    "update_dataset",
    "update_gateway",
    "update_gateway_capability_configuration",
    "update_portal",
    "update_project",
    "wait_for_asset",
    "wait_for_asset_model",
]


# ---------------------------------------------------------------------------
# Asset-model operations
# ---------------------------------------------------------------------------


async def create_asset_model(
    asset_model_name: str,
    *,
    asset_model_properties: list[dict[str, Any]] | None = None,
    asset_model_hierarchies: list[dict[str, Any]] | None = None,
    asset_model_description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AssetModelResult:
    """Create an IoT SiteWise asset model.

    Args:
        asset_model_name: Human-readable name for the model.
        asset_model_properties: Property definitions.
        asset_model_hierarchies: Hierarchy definitions.
        asset_model_description: Optional description.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        An :class:`AssetModelResult` for the new asset model.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {"assetModelName": asset_model_name}
    if asset_model_properties is not None:
        kwargs["assetModelProperties"] = asset_model_properties
    if asset_model_hierarchies is not None:
        kwargs["assetModelHierarchies"] = asset_model_hierarchies
    if asset_model_description is not None:
        kwargs["assetModelDescription"] = asset_model_description
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateAssetModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_asset_model failed") from exc
    return _parse_asset_model(resp)


async def describe_asset_model(
    asset_model_id: str,
    *,
    region_name: str | None = None,
) -> AssetModelResult:
    """Describe an IoT SiteWise asset model.

    Args:
        asset_model_id: The asset model ID.
        region_name: AWS region override.

    Returns:
        An :class:`AssetModelResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        resp = await client.call("DescribeAssetModel", assetModelId=asset_model_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_asset_model failed") from exc
    return _parse_asset_model(resp)


async def list_asset_models(
    *,
    region_name: str | None = None,
) -> list[AssetModelResult]:
    """List all IoT SiteWise asset models.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`AssetModelResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    results: list[AssetModelResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListAssetModels", **kwargs)
            for model in resp.get("assetModelSummaries", []):
                results.append(_parse_asset_model(model))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_asset_models failed") from exc
    return results


async def delete_asset_model(
    asset_model_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IoT SiteWise asset model.

    Args:
        asset_model_id: The asset model ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        await client.call("DeleteAssetModel", assetModelId=asset_model_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_asset_model failed") from exc


# ---------------------------------------------------------------------------
# Asset operations
# ---------------------------------------------------------------------------


async def create_asset(
    asset_name: str,
    *,
    asset_model_id: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AssetResult:
    """Create an IoT SiteWise asset.

    Args:
        asset_name: Human-readable name for the asset.
        asset_model_id: The asset model to use.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        An :class:`AssetResult` for the new asset.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {
        "assetName": asset_name,
        "assetModelId": asset_model_id,
    }
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateAsset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_asset failed") from exc
    return _parse_asset(resp)


async def describe_asset(
    asset_id: str,
    *,
    region_name: str | None = None,
) -> AssetResult:
    """Describe an IoT SiteWise asset.

    Args:
        asset_id: The asset ID.
        region_name: AWS region override.

    Returns:
        An :class:`AssetResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        resp = await client.call("DescribeAsset", assetId=asset_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_asset failed") from exc
    return _parse_asset(resp)


async def list_assets(
    *,
    asset_model_id: str | None = None,
    region_name: str | None = None,
) -> list[AssetResult]:
    """List IoT SiteWise assets, optionally filtered by model.

    Args:
        asset_model_id: Filter by asset model ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`AssetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    results: list[AssetResult] = []
    kwargs: dict[str, Any] = {}
    if asset_model_id:
        kwargs["assetModelId"] = asset_model_id
    try:
        while True:
            resp = await client.call("ListAssets", **kwargs)
            for asset in resp.get("assetSummaries", []):
                results.append(_parse_asset(asset))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_assets failed") from exc
    return results


async def delete_asset(
    asset_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IoT SiteWise asset.

    Args:
        asset_id: The asset ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        await client.call("DeleteAsset", assetId=asset_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_asset failed") from exc


# ---------------------------------------------------------------------------
# Asset association
# ---------------------------------------------------------------------------


async def associate_assets(
    asset_id: str,
    *,
    hierarchy_id: str,
    child_asset_id: str,
    region_name: str | None = None,
) -> None:
    """Associate a child asset with a parent asset.

    Args:
        asset_id: The parent asset ID.
        hierarchy_id: The hierarchy ID on the parent model.
        child_asset_id: The child asset ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        await client.call(
            "AssociateAssets",
            assetId=asset_id,
            hierarchyId=hierarchy_id,
            childAssetId=child_asset_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "associate_assets failed") from exc


async def disassociate_assets(
    asset_id: str,
    *,
    hierarchy_id: str,
    child_asset_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate a child asset from a parent asset.

    Args:
        asset_id: The parent asset ID.
        hierarchy_id: The hierarchy ID on the parent model.
        child_asset_id: The child asset ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        await client.call(
            "DisassociateAssets",
            assetId=asset_id,
            hierarchyId=hierarchy_id,
            childAssetId=child_asset_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "disassociate_assets failed") from exc


# ---------------------------------------------------------------------------
# Property value operations
# ---------------------------------------------------------------------------


async def put_asset_property_values(
    entries: list[dict[str, Any]],
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Ingest asset property values in batch.

    Args:
        entries: A list of ``BatchPutAssetPropertyValue`` entry dicts.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        resp = await client.call("BatchPutAssetPropertyValue", entries=entries)
    except Exception as exc:
        raise wrap_aws_error(exc, "put_asset_property_values failed") from exc
    return resp


async def get_asset_property_value(
    *,
    asset_id: str | None = None,
    property_id: str | None = None,
    property_alias: str | None = None,
    region_name: str | None = None,
) -> PropertyValueResult:
    """Get the latest value of an asset property.

    Args:
        asset_id: The asset ID.
        property_id: The property ID.
        property_alias: A property alias.
        region_name: AWS region override.

    Returns:
        A :class:`PropertyValueResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if asset_id:
        kwargs["assetId"] = asset_id
    if property_id:
        kwargs["propertyId"] = property_id
    if property_alias:
        kwargs["propertyAlias"] = property_alias
    try:
        resp = await client.call("GetAssetPropertyValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_asset_property_value failed") from exc
    return _parse_property_value(resp.get("propertyValue", {}))


async def get_asset_property_aggregates(
    *,
    aggregate_types: list[str],
    resolution: str,
    start_date: str,
    end_date: str,
    asset_id: str | None = None,
    property_id: str | None = None,
    property_alias: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Get aggregated values for an asset property.

    Args:
        aggregate_types: Aggregation types (e.g. ``["AVERAGE", "MAX"]``).
        resolution: Time resolution (e.g. ``"1m"``, ``"1h"``).
        start_date: ISO-8601 start datetime.
        end_date: ISO-8601 end datetime.
        asset_id: The asset ID.
        property_id: The property ID.
        property_alias: A property alias.
        region_name: AWS region override.

    Returns:
        A list of aggregated value dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {
        "aggregateTypes": aggregate_types,
        "resolution": resolution,
        "startDate": start_date,
        "endDate": end_date,
    }
    if asset_id:
        kwargs["assetId"] = asset_id
    if property_id:
        kwargs["propertyId"] = property_id
    if property_alias:
        kwargs["propertyAlias"] = property_alias
    results: list[dict[str, Any]] = []
    try:
        while True:
            resp = await client.call("GetAssetPropertyAggregates", **kwargs)
            results.extend(resp.get("aggregatedValues", []))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "get_asset_property_aggregates failed") from exc
    return results


async def get_asset_property_value_history(
    *,
    asset_id: str | None = None,
    property_id: str | None = None,
    property_alias: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    region_name: str | None = None,
) -> list[PropertyValueResult]:
    """Get the value history for an asset property.

    Args:
        asset_id: The asset ID.
        property_id: The property ID.
        property_alias: A property alias.
        start_date: ISO-8601 start datetime.
        end_date: ISO-8601 end datetime.
        region_name: AWS region override.

    Returns:
        A list of :class:`PropertyValueResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if asset_id:
        kwargs["assetId"] = asset_id
    if property_id:
        kwargs["propertyId"] = property_id
    if property_alias:
        kwargs["propertyAlias"] = property_alias
    if start_date:
        kwargs["startDate"] = start_date
    if end_date:
        kwargs["endDate"] = end_date
    results: list[PropertyValueResult] = []
    try:
        while True:
            resp = await client.call("GetAssetPropertyValueHistory", **kwargs)
            for entry in resp.get("assetPropertyValueHistory", []):
                results.append(_parse_property_value(entry))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "get_asset_property_value_history failed") from exc
    return results


# ---------------------------------------------------------------------------
# Portal operations
# ---------------------------------------------------------------------------


async def create_portal(
    portal_name: str,
    *,
    portal_contact_email: str,
    role_arn: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> PortalResult:
    """Create an IoT SiteWise portal.

    Args:
        portal_name: Human-readable name.
        portal_contact_email: Administrator contact e-mail.
        role_arn: Service role ARN for the portal.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`PortalResult` for the new portal.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {
        "portalName": portal_name,
        "portalContactEmail": portal_contact_email,
    }
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreatePortal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_portal failed") from exc
    return _parse_portal(resp)


async def describe_portal(
    portal_id: str,
    *,
    region_name: str | None = None,
) -> PortalResult:
    """Describe an IoT SiteWise portal.

    Args:
        portal_id: The portal ID.
        region_name: AWS region override.

    Returns:
        A :class:`PortalResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        resp = await client.call("DescribePortal", portalId=portal_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_portal failed") from exc
    return _parse_portal(resp)


async def list_portals(
    *,
    region_name: str | None = None,
) -> list[PortalResult]:
    """List all IoT SiteWise portals.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`PortalResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    results: list[PortalResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListPortals", **kwargs)
            for portal in resp.get("portalSummaries", []):
                results.append(_parse_portal(portal))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_portals failed") from exc
    return results


async def delete_portal(
    portal_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IoT SiteWise portal.

    Args:
        portal_id: The portal ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    try:
        await client.call("DeletePortal", portalId=portal_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_portal failed") from exc


# ---------------------------------------------------------------------------
# Dashboard operations
# ---------------------------------------------------------------------------


async def create_dashboard(
    project_id: str,
    *,
    dashboard_name: str,
    dashboard_definition: str,
    dashboard_description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DashboardResult:
    """Create an IoT SiteWise dashboard.

    Args:
        project_id: The project that owns the dashboard.
        dashboard_name: Human-readable name.
        dashboard_definition: JSON dashboard definition.
        dashboard_description: Optional description.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`DashboardResult` for the new dashboard.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {
        "projectId": project_id,
        "dashboardName": dashboard_name,
        "dashboardDefinition": dashboard_definition,
    }
    if dashboard_description is not None:
        kwargs["dashboardDescription"] = dashboard_description
    if tags:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_dashboard failed") from exc
    return _parse_dashboard(resp)


async def list_dashboards(
    project_id: str,
    *,
    region_name: str | None = None,
) -> list[DashboardResult]:
    """List dashboards for a project.

    Args:
        project_id: The project ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`DashboardResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    results: list[DashboardResult] = []
    kwargs: dict[str, Any] = {"projectId": project_id}
    try:
        while True:
            resp = await client.call("ListDashboards", **kwargs)
            for dash in resp.get("dashboardSummaries", []):
                results.append(_parse_dashboard(dash))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_dashboards failed") from exc
    return results


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def wait_for_asset_model(
    asset_model_id: str,
    *,
    target_state: str = "ACTIVE",
    timeout: float = 300.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> AssetModelResult:
    """Poll until an asset model reaches the desired state.

    Args:
        asset_model_id: The asset model ID to monitor.
        target_state: Desired status (default ``"ACTIVE"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`AssetModelResult` once it reaches *target_state*.

    Raises:
        AwsTimeoutError: If the model does not reach the target state
            within *timeout* seconds.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = await describe_asset_model(asset_model_id, region_name=region_name)
        if result.asset_model_status == target_state:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Asset model {asset_model_id!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {result.asset_model_status!r})"
            )
        await asyncio.sleep(poll_interval)


async def wait_for_asset(
    asset_id: str,
    *,
    target_state: str = "ACTIVE",
    timeout: float = 300.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> AssetResult:
    """Poll until an asset reaches the desired state.

    Args:
        asset_id: The asset ID to monitor.
        target_state: Desired status (default ``"ACTIVE"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`AssetResult` once it reaches *target_state*.

    Raises:
        AwsTimeoutError: If the asset does not reach the target state
            within *timeout* seconds.
    """
    deadline = time.monotonic() + timeout
    while True:
        result = await describe_asset(asset_id, region_name=region_name)
        if result.asset_status == target_state:
            return result
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Asset {asset_id!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {result.asset_status!r})"
            )
        await asyncio.sleep(poll_interval)


async def associate_time_series_to_asset_property(
    alias: str,
    asset_id: str,
    property_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate time series to asset property.

    Args:
        alias: Alias.
        asset_id: Asset id.
        property_id: Property id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["alias"] = alias
    kwargs["assetId"] = asset_id
    kwargs["propertyId"] = property_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("AssociateTimeSeriesToAssetProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate time series to asset property") from exc
    return None


async def batch_associate_project_assets(
    project_id: str,
    asset_ids: list[str],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> BatchAssociateProjectAssetsResult:
    """Batch associate project assets.

    Args:
        project_id: Project id.
        asset_ids: Asset ids.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    kwargs["assetIds"] = asset_ids
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("BatchAssociateProjectAssets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch associate project assets") from exc
    return BatchAssociateProjectAssetsResult(
        errors=resp.get("errors"),
    )


async def batch_disassociate_project_assets(
    project_id: str,
    asset_ids: list[str],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> BatchDisassociateProjectAssetsResult:
    """Batch disassociate project assets.

    Args:
        project_id: Project id.
        asset_ids: Asset ids.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    kwargs["assetIds"] = asset_ids
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("BatchDisassociateProjectAssets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch disassociate project assets") from exc
    return BatchDisassociateProjectAssetsResult(
        errors=resp.get("errors"),
    )


async def batch_get_asset_property_aggregates(
    entries: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> BatchGetAssetPropertyAggregatesResult:
    """Batch get asset property aggregates.

    Args:
        entries: Entries.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["entries"] = entries
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("BatchGetAssetPropertyAggregates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get asset property aggregates") from exc
    return BatchGetAssetPropertyAggregatesResult(
        error_entries=resp.get("errorEntries"),
        success_entries=resp.get("successEntries"),
        skipped_entries=resp.get("skippedEntries"),
        next_token=resp.get("nextToken"),
    )


async def batch_get_asset_property_value(
    entries: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> BatchGetAssetPropertyValueResult:
    """Batch get asset property value.

    Args:
        entries: Entries.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["entries"] = entries
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("BatchGetAssetPropertyValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get asset property value") from exc
    return BatchGetAssetPropertyValueResult(
        error_entries=resp.get("errorEntries"),
        success_entries=resp.get("successEntries"),
        skipped_entries=resp.get("skippedEntries"),
        next_token=resp.get("nextToken"),
    )


async def batch_get_asset_property_value_history(
    entries: list[dict[str, Any]],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> BatchGetAssetPropertyValueHistoryResult:
    """Batch get asset property value history.

    Args:
        entries: Entries.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["entries"] = entries
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("BatchGetAssetPropertyValueHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get asset property value history") from exc
    return BatchGetAssetPropertyValueHistoryResult(
        error_entries=resp.get("errorEntries"),
        success_entries=resp.get("successEntries"),
        skipped_entries=resp.get("skippedEntries"),
        next_token=resp.get("nextToken"),
    )


async def batch_put_asset_property_value(
    entries: list[dict[str, Any]],
    *,
    enable_partial_entry_processing: bool | None = None,
    region_name: str | None = None,
) -> BatchPutAssetPropertyValueResult:
    """Batch put asset property value.

    Args:
        entries: Entries.
        enable_partial_entry_processing: Enable partial entry processing.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["entries"] = entries
    if enable_partial_entry_processing is not None:
        kwargs["enablePartialEntryProcessing"] = enable_partial_entry_processing
    try:
        resp = await client.call("BatchPutAssetPropertyValue", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch put asset property value") from exc
    return BatchPutAssetPropertyValueResult(
        error_entries=resp.get("errorEntries"),
    )


async def create_access_policy(
    access_policy_identity: dict[str, Any],
    access_policy_resource: dict[str, Any],
    access_policy_permission: str,
    *,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAccessPolicyResult:
    """Create access policy.

    Args:
        access_policy_identity: Access policy identity.
        access_policy_resource: Access policy resource.
        access_policy_permission: Access policy permission.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPolicyIdentity"] = access_policy_identity
    kwargs["accessPolicyResource"] = access_policy_resource
    kwargs["accessPolicyPermission"] = access_policy_permission
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create access policy") from exc
    return CreateAccessPolicyResult(
        access_policy_id=resp.get("accessPolicyId"),
        access_policy_arn=resp.get("accessPolicyArn"),
    )


async def create_asset_model_composite_model(
    asset_model_id: str,
    asset_model_composite_model_name: str,
    asset_model_composite_model_type: str,
    *,
    asset_model_composite_model_external_id: str | None = None,
    parent_asset_model_composite_model_id: str | None = None,
    asset_model_composite_model_id: str | None = None,
    asset_model_composite_model_description: str | None = None,
    client_token: str | None = None,
    composed_asset_model_id: str | None = None,
    asset_model_composite_model_properties: list[dict[str, Any]] | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    match_for_version_type: str | None = None,
    region_name: str | None = None,
) -> CreateAssetModelCompositeModelResult:
    """Create asset model composite model.

    Args:
        asset_model_id: Asset model id.
        asset_model_composite_model_name: Asset model composite model name.
        asset_model_composite_model_type: Asset model composite model type.
        asset_model_composite_model_external_id: Asset model composite model external id.
        parent_asset_model_composite_model_id: Parent asset model composite model id.
        asset_model_composite_model_id: Asset model composite model id.
        asset_model_composite_model_description: Asset model composite model description.
        client_token: Client token.
        composed_asset_model_id: Composed asset model id.
        asset_model_composite_model_properties: Asset model composite model properties.
        if_match: If match.
        if_none_match: If none match.
        match_for_version_type: Match for version type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["assetModelCompositeModelName"] = asset_model_composite_model_name
    kwargs["assetModelCompositeModelType"] = asset_model_composite_model_type
    if asset_model_composite_model_external_id is not None:
        kwargs["assetModelCompositeModelExternalId"] = asset_model_composite_model_external_id
    if parent_asset_model_composite_model_id is not None:
        kwargs["parentAssetModelCompositeModelId"] = parent_asset_model_composite_model_id
    if asset_model_composite_model_id is not None:
        kwargs["assetModelCompositeModelId"] = asset_model_composite_model_id
    if asset_model_composite_model_description is not None:
        kwargs["assetModelCompositeModelDescription"] = asset_model_composite_model_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if composed_asset_model_id is not None:
        kwargs["composedAssetModelId"] = composed_asset_model_id
    if asset_model_composite_model_properties is not None:
        kwargs["assetModelCompositeModelProperties"] = asset_model_composite_model_properties
    if if_match is not None:
        kwargs["ifMatch"] = if_match
    if if_none_match is not None:
        kwargs["ifNoneMatch"] = if_none_match
    if match_for_version_type is not None:
        kwargs["matchForVersionType"] = match_for_version_type
    try:
        resp = await client.call("CreateAssetModelCompositeModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create asset model composite model") from exc
    return CreateAssetModelCompositeModelResult(
        asset_model_composite_model_id=resp.get("assetModelCompositeModelId"),
        asset_model_composite_model_path=resp.get("assetModelCompositeModelPath"),
        asset_model_status=resp.get("assetModelStatus"),
    )


async def create_bulk_import_job(
    job_name: str,
    job_role_arn: str,
    files: list[dict[str, Any]],
    error_report_location: dict[str, Any],
    job_configuration: dict[str, Any],
    *,
    adaptive_ingestion: bool | None = None,
    delete_files_after_import: bool | None = None,
    region_name: str | None = None,
) -> CreateBulkImportJobResult:
    """Create bulk import job.

    Args:
        job_name: Job name.
        job_role_arn: Job role arn.
        files: Files.
        error_report_location: Error report location.
        job_configuration: Job configuration.
        adaptive_ingestion: Adaptive ingestion.
        delete_files_after_import: Delete files after import.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobName"] = job_name
    kwargs["jobRoleArn"] = job_role_arn
    kwargs["files"] = files
    kwargs["errorReportLocation"] = error_report_location
    kwargs["jobConfiguration"] = job_configuration
    if adaptive_ingestion is not None:
        kwargs["adaptiveIngestion"] = adaptive_ingestion
    if delete_files_after_import is not None:
        kwargs["deleteFilesAfterImport"] = delete_files_after_import
    try:
        resp = await client.call("CreateBulkImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create bulk import job") from exc
    return CreateBulkImportJobResult(
        job_id=resp.get("jobId"),
        job_name=resp.get("jobName"),
        job_status=resp.get("jobStatus"),
    )


async def create_computation_model(
    computation_model_name: str,
    computation_model_configuration: dict[str, Any],
    computation_model_data_binding: dict[str, Any],
    *,
    computation_model_description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateComputationModelResult:
    """Create computation model.

    Args:
        computation_model_name: Computation model name.
        computation_model_configuration: Computation model configuration.
        computation_model_data_binding: Computation model data binding.
        computation_model_description: Computation model description.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelName"] = computation_model_name
    kwargs["computationModelConfiguration"] = computation_model_configuration
    kwargs["computationModelDataBinding"] = computation_model_data_binding
    if computation_model_description is not None:
        kwargs["computationModelDescription"] = computation_model_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateComputationModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create computation model") from exc
    return CreateComputationModelResult(
        computation_model_id=resp.get("computationModelId"),
        computation_model_arn=resp.get("computationModelArn"),
        computation_model_status=resp.get("computationModelStatus"),
    )


async def create_dataset(
    dataset_name: str,
    dataset_source: dict[str, Any],
    *,
    dataset_id: str | None = None,
    dataset_description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDatasetResult:
    """Create dataset.

    Args:
        dataset_name: Dataset name.
        dataset_source: Dataset source.
        dataset_id: Dataset id.
        dataset_description: Dataset description.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetName"] = dataset_name
    kwargs["datasetSource"] = dataset_source
    if dataset_id is not None:
        kwargs["datasetId"] = dataset_id
    if dataset_description is not None:
        kwargs["datasetDescription"] = dataset_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dataset") from exc
    return CreateDatasetResult(
        dataset_id=resp.get("datasetId"),
        dataset_arn=resp.get("datasetArn"),
        dataset_status=resp.get("datasetStatus"),
    )


async def create_gateway(
    gateway_name: str,
    gateway_platform: dict[str, Any],
    *,
    gateway_version: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateGatewayResult:
    """Create gateway.

    Args:
        gateway_name: Gateway name.
        gateway_platform: Gateway platform.
        gateway_version: Gateway version.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayName"] = gateway_name
    kwargs["gatewayPlatform"] = gateway_platform
    if gateway_version is not None:
        kwargs["gatewayVersion"] = gateway_version
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateGateway", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create gateway") from exc
    return CreateGatewayResult(
        gateway_id=resp.get("gatewayId"),
        gateway_arn=resp.get("gatewayArn"),
    )


async def create_project(
    portal_id: str,
    project_name: str,
    *,
    project_description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateProjectResult:
    """Create project.

    Args:
        portal_id: Portal id.
        project_name: Project name.
        project_description: Project description.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portalId"] = portal_id
    kwargs["projectName"] = project_name
    if project_description is not None:
        kwargs["projectDescription"] = project_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create project") from exc
    return CreateProjectResult(
        project_id=resp.get("projectId"),
        project_arn=resp.get("projectArn"),
    )


async def delete_access_policy(
    access_policy_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete access policy.

    Args:
        access_policy_id: Access policy id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPolicyId"] = access_policy_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeleteAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete access policy") from exc
    return None


async def delete_asset_model_composite_model(
    asset_model_id: str,
    asset_model_composite_model_id: str,
    *,
    client_token: str | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    match_for_version_type: str | None = None,
    region_name: str | None = None,
) -> DeleteAssetModelCompositeModelResult:
    """Delete asset model composite model.

    Args:
        asset_model_id: Asset model id.
        asset_model_composite_model_id: Asset model composite model id.
        client_token: Client token.
        if_match: If match.
        if_none_match: If none match.
        match_for_version_type: Match for version type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["assetModelCompositeModelId"] = asset_model_composite_model_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if if_match is not None:
        kwargs["ifMatch"] = if_match
    if if_none_match is not None:
        kwargs["ifNoneMatch"] = if_none_match
    if match_for_version_type is not None:
        kwargs["matchForVersionType"] = match_for_version_type
    try:
        resp = await client.call("DeleteAssetModelCompositeModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete asset model composite model") from exc
    return DeleteAssetModelCompositeModelResult(
        asset_model_status=resp.get("assetModelStatus"),
    )


async def delete_asset_model_interface_relationship(
    asset_model_id: str,
    interface_asset_model_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> DeleteAssetModelInterfaceRelationshipResult:
    """Delete asset model interface relationship.

    Args:
        asset_model_id: Asset model id.
        interface_asset_model_id: Interface asset model id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["interfaceAssetModelId"] = interface_asset_model_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("DeleteAssetModelInterfaceRelationship", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete asset model interface relationship") from exc
    return DeleteAssetModelInterfaceRelationshipResult(
        asset_model_id=resp.get("assetModelId"),
        interface_asset_model_id=resp.get("interfaceAssetModelId"),
        asset_model_arn=resp.get("assetModelArn"),
        asset_model_status=resp.get("assetModelStatus"),
    )


async def delete_computation_model(
    computation_model_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> DeleteComputationModelResult:
    """Delete computation model.

    Args:
        computation_model_id: Computation model id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelId"] = computation_model_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("DeleteComputationModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete computation model") from exc
    return DeleteComputationModelResult(
        computation_model_status=resp.get("computationModelStatus"),
    )


async def delete_dashboard(
    dashboard_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete dashboard.

    Args:
        dashboard_id: Dashboard id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dashboardId"] = dashboard_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeleteDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dashboard") from exc
    return None


async def delete_dataset(
    dataset_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> DeleteDatasetResult:
    """Delete dataset.

    Args:
        dataset_id: Dataset id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetId"] = dataset_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("DeleteDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dataset") from exc
    return DeleteDatasetResult(
        dataset_status=resp.get("datasetStatus"),
    )


async def delete_gateway(
    gateway_id: str,
    region_name: str | None = None,
) -> None:
    """Delete gateway.

    Args:
        gateway_id: Gateway id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayId"] = gateway_id
    try:
        await client.call("DeleteGateway", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete gateway") from exc
    return None


async def delete_project(
    project_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete project.

    Args:
        project_id: Project id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeleteProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete project") from exc
    return None


async def delete_time_series(
    *,
    alias: str | None = None,
    asset_id: str | None = None,
    property_id: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete time series.

    Args:
        alias: Alias.
        asset_id: Asset id.
        property_id: Property id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if alias is not None:
        kwargs["alias"] = alias
    if asset_id is not None:
        kwargs["assetId"] = asset_id
    if property_id is not None:
        kwargs["propertyId"] = property_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeleteTimeSeries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete time series") from exc
    return None


async def describe_access_policy(
    access_policy_id: str,
    region_name: str | None = None,
) -> DescribeAccessPolicyResult:
    """Describe access policy.

    Args:
        access_policy_id: Access policy id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPolicyId"] = access_policy_id
    try:
        resp = await client.call("DescribeAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe access policy") from exc
    return DescribeAccessPolicyResult(
        access_policy_id=resp.get("accessPolicyId"),
        access_policy_arn=resp.get("accessPolicyArn"),
        access_policy_identity=resp.get("accessPolicyIdentity"),
        access_policy_resource=resp.get("accessPolicyResource"),
        access_policy_permission=resp.get("accessPolicyPermission"),
        access_policy_creation_date=resp.get("accessPolicyCreationDate"),
        access_policy_last_update_date=resp.get("accessPolicyLastUpdateDate"),
    )


async def describe_action(
    action_id: str,
    region_name: str | None = None,
) -> DescribeActionResult:
    """Describe action.

    Args:
        action_id: Action id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionId"] = action_id
    try:
        resp = await client.call("DescribeAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe action") from exc
    return DescribeActionResult(
        action_id=resp.get("actionId"),
        target_resource=resp.get("targetResource"),
        action_definition_id=resp.get("actionDefinitionId"),
        action_payload=resp.get("actionPayload"),
        execution_time=resp.get("executionTime"),
        resolve_to=resp.get("resolveTo"),
    )


async def describe_asset_composite_model(
    asset_id: str,
    asset_composite_model_id: str,
    region_name: str | None = None,
) -> DescribeAssetCompositeModelResult:
    """Describe asset composite model.

    Args:
        asset_id: Asset id.
        asset_composite_model_id: Asset composite model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    kwargs["assetCompositeModelId"] = asset_composite_model_id
    try:
        resp = await client.call("DescribeAssetCompositeModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset composite model") from exc
    return DescribeAssetCompositeModelResult(
        asset_id=resp.get("assetId"),
        asset_composite_model_id=resp.get("assetCompositeModelId"),
        asset_composite_model_external_id=resp.get("assetCompositeModelExternalId"),
        asset_composite_model_path=resp.get("assetCompositeModelPath"),
        asset_composite_model_name=resp.get("assetCompositeModelName"),
        asset_composite_model_description=resp.get("assetCompositeModelDescription"),
        asset_composite_model_type=resp.get("assetCompositeModelType"),
        asset_composite_model_properties=resp.get("assetCompositeModelProperties"),
        asset_composite_model_summaries=resp.get("assetCompositeModelSummaries"),
        action_definitions=resp.get("actionDefinitions"),
    )


async def describe_asset_model_composite_model(
    asset_model_id: str,
    asset_model_composite_model_id: str,
    *,
    asset_model_version: str | None = None,
    region_name: str | None = None,
) -> DescribeAssetModelCompositeModelResult:
    """Describe asset model composite model.

    Args:
        asset_model_id: Asset model id.
        asset_model_composite_model_id: Asset model composite model id.
        asset_model_version: Asset model version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["assetModelCompositeModelId"] = asset_model_composite_model_id
    if asset_model_version is not None:
        kwargs["assetModelVersion"] = asset_model_version
    try:
        resp = await client.call("DescribeAssetModelCompositeModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset model composite model") from exc
    return DescribeAssetModelCompositeModelResult(
        asset_model_id=resp.get("assetModelId"),
        asset_model_composite_model_id=resp.get("assetModelCompositeModelId"),
        asset_model_composite_model_external_id=resp.get("assetModelCompositeModelExternalId"),
        asset_model_composite_model_path=resp.get("assetModelCompositeModelPath"),
        asset_model_composite_model_name=resp.get("assetModelCompositeModelName"),
        asset_model_composite_model_description=resp.get("assetModelCompositeModelDescription"),
        asset_model_composite_model_type=resp.get("assetModelCompositeModelType"),
        asset_model_composite_model_properties=resp.get("assetModelCompositeModelProperties"),
        composition_details=resp.get("compositionDetails"),
        asset_model_composite_model_summaries=resp.get("assetModelCompositeModelSummaries"),
        action_definitions=resp.get("actionDefinitions"),
    )


async def describe_asset_model_interface_relationship(
    asset_model_id: str,
    interface_asset_model_id: str,
    region_name: str | None = None,
) -> DescribeAssetModelInterfaceRelationshipResult:
    """Describe asset model interface relationship.

    Args:
        asset_model_id: Asset model id.
        interface_asset_model_id: Interface asset model id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["interfaceAssetModelId"] = interface_asset_model_id
    try:
        resp = await client.call("DescribeAssetModelInterfaceRelationship", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset model interface relationship") from exc
    return DescribeAssetModelInterfaceRelationshipResult(
        asset_model_id=resp.get("assetModelId"),
        interface_asset_model_id=resp.get("interfaceAssetModelId"),
        property_mappings=resp.get("propertyMappings"),
        hierarchy_mappings=resp.get("hierarchyMappings"),
    )


async def describe_asset_property(
    asset_id: str,
    property_id: str,
    region_name: str | None = None,
) -> DescribeAssetPropertyResult:
    """Describe asset property.

    Args:
        asset_id: Asset id.
        property_id: Property id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    kwargs["propertyId"] = property_id
    try:
        resp = await client.call("DescribeAssetProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe asset property") from exc
    return DescribeAssetPropertyResult(
        asset_id=resp.get("assetId"),
        asset_external_id=resp.get("assetExternalId"),
        asset_name=resp.get("assetName"),
        asset_model_id=resp.get("assetModelId"),
        asset_property=resp.get("assetProperty"),
        composite_model=resp.get("compositeModel"),
    )


async def describe_bulk_import_job(
    job_id: str,
    region_name: str | None = None,
) -> DescribeBulkImportJobResult:
    """Describe bulk import job.

    Args:
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    try:
        resp = await client.call("DescribeBulkImportJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe bulk import job") from exc
    return DescribeBulkImportJobResult(
        job_id=resp.get("jobId"),
        job_name=resp.get("jobName"),
        job_status=resp.get("jobStatus"),
        job_role_arn=resp.get("jobRoleArn"),
        files=resp.get("files"),
        error_report_location=resp.get("errorReportLocation"),
        job_configuration=resp.get("jobConfiguration"),
        job_creation_date=resp.get("jobCreationDate"),
        job_last_update_date=resp.get("jobLastUpdateDate"),
        adaptive_ingestion=resp.get("adaptiveIngestion"),
        delete_files_after_import=resp.get("deleteFilesAfterImport"),
    )


async def describe_computation_model(
    computation_model_id: str,
    *,
    computation_model_version: str | None = None,
    region_name: str | None = None,
) -> DescribeComputationModelResult:
    """Describe computation model.

    Args:
        computation_model_id: Computation model id.
        computation_model_version: Computation model version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelId"] = computation_model_id
    if computation_model_version is not None:
        kwargs["computationModelVersion"] = computation_model_version
    try:
        resp = await client.call("DescribeComputationModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe computation model") from exc
    return DescribeComputationModelResult(
        computation_model_id=resp.get("computationModelId"),
        computation_model_arn=resp.get("computationModelArn"),
        computation_model_name=resp.get("computationModelName"),
        computation_model_description=resp.get("computationModelDescription"),
        computation_model_configuration=resp.get("computationModelConfiguration"),
        computation_model_data_binding=resp.get("computationModelDataBinding"),
        computation_model_creation_date=resp.get("computationModelCreationDate"),
        computation_model_last_update_date=resp.get("computationModelLastUpdateDate"),
        computation_model_status=resp.get("computationModelStatus"),
        computation_model_version=resp.get("computationModelVersion"),
        action_definitions=resp.get("actionDefinitions"),
    )


async def describe_computation_model_execution_summary(
    computation_model_id: str,
    *,
    resolve_to_resource_type: str | None = None,
    resolve_to_resource_id: str | None = None,
    region_name: str | None = None,
) -> DescribeComputationModelExecutionSummaryResult:
    """Describe computation model execution summary.

    Args:
        computation_model_id: Computation model id.
        resolve_to_resource_type: Resolve to resource type.
        resolve_to_resource_id: Resolve to resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelId"] = computation_model_id
    if resolve_to_resource_type is not None:
        kwargs["resolveToResourceType"] = resolve_to_resource_type
    if resolve_to_resource_id is not None:
        kwargs["resolveToResourceId"] = resolve_to_resource_id
    try:
        resp = await client.call("DescribeComputationModelExecutionSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe computation model execution summary") from exc
    return DescribeComputationModelExecutionSummaryResult(
        computation_model_id=resp.get("computationModelId"),
        resolve_to=resp.get("resolveTo"),
        computation_model_execution_summary=resp.get("computationModelExecutionSummary"),
    )


async def describe_dashboard(
    dashboard_id: str,
    region_name: str | None = None,
) -> DescribeDashboardResult:
    """Describe dashboard.

    Args:
        dashboard_id: Dashboard id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dashboardId"] = dashboard_id
    try:
        resp = await client.call("DescribeDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dashboard") from exc
    return DescribeDashboardResult(
        dashboard_id=resp.get("dashboardId"),
        dashboard_arn=resp.get("dashboardArn"),
        dashboard_name=resp.get("dashboardName"),
        project_id=resp.get("projectId"),
        dashboard_description=resp.get("dashboardDescription"),
        dashboard_definition=resp.get("dashboardDefinition"),
        dashboard_creation_date=resp.get("dashboardCreationDate"),
        dashboard_last_update_date=resp.get("dashboardLastUpdateDate"),
    )


async def describe_dataset(
    dataset_id: str,
    region_name: str | None = None,
) -> DescribeDatasetResult:
    """Describe dataset.

    Args:
        dataset_id: Dataset id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetId"] = dataset_id
    try:
        resp = await client.call("DescribeDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dataset") from exc
    return DescribeDatasetResult(
        dataset_id=resp.get("datasetId"),
        dataset_arn=resp.get("datasetArn"),
        dataset_name=resp.get("datasetName"),
        dataset_description=resp.get("datasetDescription"),
        dataset_source=resp.get("datasetSource"),
        dataset_status=resp.get("datasetStatus"),
        dataset_creation_date=resp.get("datasetCreationDate"),
        dataset_last_update_date=resp.get("datasetLastUpdateDate"),
        dataset_version=resp.get("datasetVersion"),
    )


async def describe_default_encryption_configuration(
    region_name: str | None = None,
) -> DescribeDefaultEncryptionConfigurationResult:
    """Describe default encryption configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeDefaultEncryptionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe default encryption configuration") from exc
    return DescribeDefaultEncryptionConfigurationResult(
        encryption_type=resp.get("encryptionType"),
        kms_key_arn=resp.get("kmsKeyArn"),
        configuration_status=resp.get("configurationStatus"),
    )


async def describe_execution(
    execution_id: str,
    region_name: str | None = None,
) -> DescribeExecutionResult:
    """Describe execution.

    Args:
        execution_id: Execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionId"] = execution_id
    try:
        resp = await client.call("DescribeExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe execution") from exc
    return DescribeExecutionResult(
        execution_id=resp.get("executionId"),
        action_type=resp.get("actionType"),
        target_resource=resp.get("targetResource"),
        target_resource_version=resp.get("targetResourceVersion"),
        resolve_to=resp.get("resolveTo"),
        execution_start_time=resp.get("executionStartTime"),
        execution_end_time=resp.get("executionEndTime"),
        execution_status=resp.get("executionStatus"),
        execution_result=resp.get("executionResult"),
        execution_details=resp.get("executionDetails"),
        execution_entity_version=resp.get("executionEntityVersion"),
    )


async def describe_gateway(
    gateway_id: str,
    region_name: str | None = None,
) -> DescribeGatewayResult:
    """Describe gateway.

    Args:
        gateway_id: Gateway id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayId"] = gateway_id
    try:
        resp = await client.call("DescribeGateway", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe gateway") from exc
    return DescribeGatewayResult(
        gateway_id=resp.get("gatewayId"),
        gateway_name=resp.get("gatewayName"),
        gateway_arn=resp.get("gatewayArn"),
        gateway_platform=resp.get("gatewayPlatform"),
        gateway_version=resp.get("gatewayVersion"),
        gateway_capability_summaries=resp.get("gatewayCapabilitySummaries"),
        creation_date=resp.get("creationDate"),
        last_update_date=resp.get("lastUpdateDate"),
    )


async def describe_gateway_capability_configuration(
    gateway_id: str,
    capability_namespace: str,
    region_name: str | None = None,
) -> DescribeGatewayCapabilityConfigurationResult:
    """Describe gateway capability configuration.

    Args:
        gateway_id: Gateway id.
        capability_namespace: Capability namespace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayId"] = gateway_id
    kwargs["capabilityNamespace"] = capability_namespace
    try:
        resp = await client.call("DescribeGatewayCapabilityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe gateway capability configuration") from exc
    return DescribeGatewayCapabilityConfigurationResult(
        gateway_id=resp.get("gatewayId"),
        capability_namespace=resp.get("capabilityNamespace"),
        capability_configuration=resp.get("capabilityConfiguration"),
        capability_sync_status=resp.get("capabilitySyncStatus"),
    )


async def describe_logging_options(
    region_name: str | None = None,
) -> DescribeLoggingOptionsResult:
    """Describe logging options.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeLoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe logging options") from exc
    return DescribeLoggingOptionsResult(
        logging_options=resp.get("loggingOptions"),
    )


async def describe_project(
    project_id: str,
    region_name: str | None = None,
) -> DescribeProjectResult:
    """Describe project.

    Args:
        project_id: Project id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    try:
        resp = await client.call("DescribeProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe project") from exc
    return DescribeProjectResult(
        project_id=resp.get("projectId"),
        project_arn=resp.get("projectArn"),
        project_name=resp.get("projectName"),
        portal_id=resp.get("portalId"),
        project_description=resp.get("projectDescription"),
        project_creation_date=resp.get("projectCreationDate"),
        project_last_update_date=resp.get("projectLastUpdateDate"),
    )


async def describe_storage_configuration(
    region_name: str | None = None,
) -> DescribeStorageConfigurationResult:
    """Describe storage configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeStorageConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe storage configuration") from exc
    return DescribeStorageConfigurationResult(
        storage_type=resp.get("storageType"),
        multi_layer_storage=resp.get("multiLayerStorage"),
        disassociated_data_storage=resp.get("disassociatedDataStorage"),
        retention_period=resp.get("retentionPeriod"),
        configuration_status=resp.get("configurationStatus"),
        last_update_date=resp.get("lastUpdateDate"),
        warm_tier=resp.get("warmTier"),
        warm_tier_retention_period=resp.get("warmTierRetentionPeriod"),
        disallow_ingest_null_na_n=resp.get("disallowIngestNullNaN"),
    )


async def describe_time_series(
    *,
    alias: str | None = None,
    asset_id: str | None = None,
    property_id: str | None = None,
    region_name: str | None = None,
) -> DescribeTimeSeriesResult:
    """Describe time series.

    Args:
        alias: Alias.
        asset_id: Asset id.
        property_id: Property id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if alias is not None:
        kwargs["alias"] = alias
    if asset_id is not None:
        kwargs["assetId"] = asset_id
    if property_id is not None:
        kwargs["propertyId"] = property_id
    try:
        resp = await client.call("DescribeTimeSeries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe time series") from exc
    return DescribeTimeSeriesResult(
        asset_id=resp.get("assetId"),
        property_id=resp.get("propertyId"),
        alias=resp.get("alias"),
        time_series_id=resp.get("timeSeriesId"),
        data_type=resp.get("dataType"),
        data_type_spec=resp.get("dataTypeSpec"),
        time_series_creation_date=resp.get("timeSeriesCreationDate"),
        time_series_last_update_date=resp.get("timeSeriesLastUpdateDate"),
        time_series_arn=resp.get("timeSeriesArn"),
    )


async def disassociate_time_series_from_asset_property(
    alias: str,
    asset_id: str,
    property_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate time series from asset property.

    Args:
        alias: Alias.
        asset_id: Asset id.
        property_id: Property id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["alias"] = alias
    kwargs["assetId"] = asset_id
    kwargs["propertyId"] = property_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DisassociateTimeSeriesFromAssetProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate time series from asset property") from exc
    return None


async def execute_action(
    target_resource: dict[str, Any],
    action_definition_id: str,
    action_payload: dict[str, Any],
    *,
    client_token: str | None = None,
    resolve_to: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ExecuteActionResult:
    """Execute action.

    Args:
        target_resource: Target resource.
        action_definition_id: Action definition id.
        action_payload: Action payload.
        client_token: Client token.
        resolve_to: Resolve to.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetResource"] = target_resource
    kwargs["actionDefinitionId"] = action_definition_id
    kwargs["actionPayload"] = action_payload
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if resolve_to is not None:
        kwargs["resolveTo"] = resolve_to
    try:
        resp = await client.call("ExecuteAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to execute action") from exc
    return ExecuteActionResult(
        action_id=resp.get("actionId"),
    )


async def execute_query(
    query_statement: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> ExecuteQueryResult:
    """Execute query.

    Args:
        query_statement: Query statement.
        next_token: Next token.
        max_results: Max results.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryStatement"] = query_statement
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("ExecuteQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to execute query") from exc
    return ExecuteQueryResult(
        columns=resp.get("columns"),
        rows=resp.get("rows"),
        next_token=resp.get("nextToken"),
    )


async def get_interpolated_asset_property_values(
    start_time_in_seconds: int,
    end_time_in_seconds: int,
    quality: str,
    interval_in_seconds: int,
    type_value: str,
    *,
    asset_id: str | None = None,
    property_id: str | None = None,
    property_alias: str | None = None,
    start_time_offset_in_nanos: int | None = None,
    end_time_offset_in_nanos: int | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    interval_window_in_seconds: int | None = None,
    region_name: str | None = None,
) -> GetInterpolatedAssetPropertyValuesResult:
    """Get interpolated asset property values.

    Args:
        start_time_in_seconds: Start time in seconds.
        end_time_in_seconds: End time in seconds.
        quality: Quality.
        interval_in_seconds: Interval in seconds.
        type_value: Type value.
        asset_id: Asset id.
        property_id: Property id.
        property_alias: Property alias.
        start_time_offset_in_nanos: Start time offset in nanos.
        end_time_offset_in_nanos: End time offset in nanos.
        next_token: Next token.
        max_results: Max results.
        interval_window_in_seconds: Interval window in seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["startTimeInSeconds"] = start_time_in_seconds
    kwargs["endTimeInSeconds"] = end_time_in_seconds
    kwargs["quality"] = quality
    kwargs["intervalInSeconds"] = interval_in_seconds
    kwargs["type"] = type_value
    if asset_id is not None:
        kwargs["assetId"] = asset_id
    if property_id is not None:
        kwargs["propertyId"] = property_id
    if property_alias is not None:
        kwargs["propertyAlias"] = property_alias
    if start_time_offset_in_nanos is not None:
        kwargs["startTimeOffsetInNanos"] = start_time_offset_in_nanos
    if end_time_offset_in_nanos is not None:
        kwargs["endTimeOffsetInNanos"] = end_time_offset_in_nanos
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if interval_window_in_seconds is not None:
        kwargs["intervalWindowInSeconds"] = interval_window_in_seconds
    try:
        resp = await client.call("GetInterpolatedAssetPropertyValues", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get interpolated asset property values") from exc
    return GetInterpolatedAssetPropertyValuesResult(
        interpolated_asset_property_values=resp.get("interpolatedAssetPropertyValues"),
        next_token=resp.get("nextToken"),
    )


async def invoke_assistant(
    message: str,
    *,
    conversation_id: str | None = None,
    enable_trace: bool | None = None,
    region_name: str | None = None,
) -> InvokeAssistantResult:
    """Invoke assistant.

    Args:
        message: Message.
        conversation_id: Conversation id.
        enable_trace: Enable trace.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["message"] = message
    if conversation_id is not None:
        kwargs["conversationId"] = conversation_id
    if enable_trace is not None:
        kwargs["enableTrace"] = enable_trace
    try:
        resp = await client.call("InvokeAssistant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to invoke assistant") from exc
    return InvokeAssistantResult(
        body=resp.get("body"),
        conversation_id=resp.get("conversationId"),
    )


async def list_access_policies(
    *,
    identity_type: str | None = None,
    identity_id: str | None = None,
    resource_type: str | None = None,
    resource_id: str | None = None,
    iam_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccessPoliciesResult:
    """List access policies.

    Args:
        identity_type: Identity type.
        identity_id: Identity id.
        resource_type: Resource type.
        resource_id: Resource id.
        iam_arn: Iam arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if identity_type is not None:
        kwargs["identityType"] = identity_type
    if identity_id is not None:
        kwargs["identityId"] = identity_id
    if resource_type is not None:
        kwargs["resourceType"] = resource_type
    if resource_id is not None:
        kwargs["resourceId"] = resource_id
    if iam_arn is not None:
        kwargs["iamArn"] = iam_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAccessPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access policies") from exc
    return ListAccessPoliciesResult(
        access_policy_summaries=resp.get("accessPolicySummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_actions(
    target_resource_type: str,
    target_resource_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    resolve_to_resource_type: str | None = None,
    resolve_to_resource_id: str | None = None,
    region_name: str | None = None,
) -> ListActionsResult:
    """List actions.

    Args:
        target_resource_type: Target resource type.
        target_resource_id: Target resource id.
        next_token: Next token.
        max_results: Max results.
        resolve_to_resource_type: Resolve to resource type.
        resolve_to_resource_id: Resolve to resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetResourceType"] = target_resource_type
    kwargs["targetResourceId"] = target_resource_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if resolve_to_resource_type is not None:
        kwargs["resolveToResourceType"] = resolve_to_resource_type
    if resolve_to_resource_id is not None:
        kwargs["resolveToResourceId"] = resolve_to_resource_id
    try:
        resp = await client.call("ListActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list actions") from exc
    return ListActionsResult(
        action_summaries=resp.get("actionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_asset_model_composite_models(
    asset_model_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    asset_model_version: str | None = None,
    region_name: str | None = None,
) -> ListAssetModelCompositeModelsResult:
    """List asset model composite models.

    Args:
        asset_model_id: Asset model id.
        next_token: Next token.
        max_results: Max results.
        asset_model_version: Asset model version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if asset_model_version is not None:
        kwargs["assetModelVersion"] = asset_model_version
    try:
        resp = await client.call("ListAssetModelCompositeModels", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset model composite models") from exc
    return ListAssetModelCompositeModelsResult(
        asset_model_composite_model_summaries=resp.get("assetModelCompositeModelSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_asset_model_properties(
    asset_model_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: str | None = None,
    asset_model_version: str | None = None,
    region_name: str | None = None,
) -> ListAssetModelPropertiesResult:
    """List asset model properties.

    Args:
        asset_model_id: Asset model id.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        asset_model_version: Asset model version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    if asset_model_version is not None:
        kwargs["assetModelVersion"] = asset_model_version
    try:
        resp = await client.call("ListAssetModelProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset model properties") from exc
    return ListAssetModelPropertiesResult(
        asset_model_property_summaries=resp.get("assetModelPropertySummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_asset_properties(
    asset_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: str | None = None,
    region_name: str | None = None,
) -> ListAssetPropertiesResult:
    """List asset properties.

    Args:
        asset_id: Asset id.
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("ListAssetProperties", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset properties") from exc
    return ListAssetPropertiesResult(
        asset_property_summaries=resp.get("assetPropertySummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_asset_relationships(
    asset_id: str,
    traversal_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAssetRelationshipsResult:
    """List asset relationships.

    Args:
        asset_id: Asset id.
        traversal_type: Traversal type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    kwargs["traversalType"] = traversal_type
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAssetRelationships", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list asset relationships") from exc
    return ListAssetRelationshipsResult(
        asset_relationship_summaries=resp.get("assetRelationshipSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_associated_assets(
    asset_id: str,
    *,
    hierarchy_id: str | None = None,
    traversal_direction: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAssociatedAssetsResult:
    """List associated assets.

    Args:
        asset_id: Asset id.
        hierarchy_id: Hierarchy id.
        traversal_direction: Traversal direction.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    if hierarchy_id is not None:
        kwargs["hierarchyId"] = hierarchy_id
    if traversal_direction is not None:
        kwargs["traversalDirection"] = traversal_direction
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAssociatedAssets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list associated assets") from exc
    return ListAssociatedAssetsResult(
        asset_summaries=resp.get("assetSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_bulk_import_jobs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filter: str | None = None,
    region_name: str | None = None,
) -> ListBulkImportJobsResult:
    """List bulk import jobs.

    Args:
        next_token: Next token.
        max_results: Max results.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("ListBulkImportJobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list bulk import jobs") from exc
    return ListBulkImportJobsResult(
        job_summaries=resp.get("jobSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_composition_relationships(
    asset_model_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCompositionRelationshipsResult:
    """List composition relationships.

    Args:
        asset_model_id: Asset model id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCompositionRelationships", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list composition relationships") from exc
    return ListCompositionRelationshipsResult(
        composition_relationship_summaries=resp.get("compositionRelationshipSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_computation_model_data_binding_usages(
    data_binding_value_filter: dict[str, Any],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListComputationModelDataBindingUsagesResult:
    """List computation model data binding usages.

    Args:
        data_binding_value_filter: Data binding value filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dataBindingValueFilter"] = data_binding_value_filter
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListComputationModelDataBindingUsages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list computation model data binding usages") from exc
    return ListComputationModelDataBindingUsagesResult(
        data_binding_usage_summaries=resp.get("dataBindingUsageSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_computation_model_resolve_to_resources(
    computation_model_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListComputationModelResolveToResourcesResult:
    """List computation model resolve to resources.

    Args:
        computation_model_id: Computation model id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelId"] = computation_model_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListComputationModelResolveToResources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list computation model resolve to resources") from exc
    return ListComputationModelResolveToResourcesResult(
        computation_model_resolve_to_resource_summaries=resp.get(
            "computationModelResolveToResourceSummaries"
        ),
        next_token=resp.get("nextToken"),
    )


async def list_computation_models(
    *,
    computation_model_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListComputationModelsResult:
    """List computation models.

    Args:
        computation_model_type: Computation model type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if computation_model_type is not None:
        kwargs["computationModelType"] = computation_model_type
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListComputationModels", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list computation models") from exc
    return ListComputationModelsResult(
        computation_model_summaries=resp.get("computationModelSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_datasets(
    source_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasetsResult:
    """List datasets.

    Args:
        source_type: Source type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["sourceType"] = source_type
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDatasets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list datasets") from exc
    return ListDatasetsResult(
        dataset_summaries=resp.get("datasetSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_executions(
    target_resource_type: str,
    target_resource_id: str,
    *,
    resolve_to_resource_type: str | None = None,
    resolve_to_resource_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    action_type: str | None = None,
    region_name: str | None = None,
) -> ListExecutionsResult:
    """List executions.

    Args:
        target_resource_type: Target resource type.
        target_resource_id: Target resource id.
        resolve_to_resource_type: Resolve to resource type.
        resolve_to_resource_id: Resolve to resource id.
        next_token: Next token.
        max_results: Max results.
        action_type: Action type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetResourceType"] = target_resource_type
    kwargs["targetResourceId"] = target_resource_id
    if resolve_to_resource_type is not None:
        kwargs["resolveToResourceType"] = resolve_to_resource_type
    if resolve_to_resource_id is not None:
        kwargs["resolveToResourceId"] = resolve_to_resource_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if action_type is not None:
        kwargs["actionType"] = action_type
    try:
        resp = await client.call("ListExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list executions") from exc
    return ListExecutionsResult(
        execution_summaries=resp.get("executionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_gateways(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListGatewaysResult:
    """List gateways.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListGateways", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list gateways") from exc
    return ListGatewaysResult(
        gateway_summaries=resp.get("gatewaySummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_interface_relationships(
    interface_asset_model_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInterfaceRelationshipsResult:
    """List interface relationships.

    Args:
        interface_asset_model_id: Interface asset model id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["interfaceAssetModelId"] = interface_asset_model_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListInterfaceRelationships", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list interface relationships") from exc
    return ListInterfaceRelationshipsResult(
        interface_relationship_summaries=resp.get("interfaceRelationshipSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_project_assets(
    project_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListProjectAssetsResult:
    """List project assets.

    Args:
        project_id: Project id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListProjectAssets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list project assets") from exc
    return ListProjectAssetsResult(
        asset_ids=resp.get("assetIds"),
        next_token=resp.get("nextToken"),
    )


async def list_projects(
    portal_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListProjectsResult:
    """List projects.

    Args:
        portal_id: Portal id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portalId"] = portal_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListProjects", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list projects") from exc
    return ListProjectsResult(
        project_summaries=resp.get("projectSummaries"),
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
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def list_time_series(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    asset_id: str | None = None,
    alias_prefix: str | None = None,
    time_series_type: str | None = None,
    region_name: str | None = None,
) -> ListTimeSeriesResult:
    """List time series.

    Args:
        next_token: Next token.
        max_results: Max results.
        asset_id: Asset id.
        alias_prefix: Alias prefix.
        time_series_type: Time series type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if asset_id is not None:
        kwargs["assetId"] = asset_id
    if alias_prefix is not None:
        kwargs["aliasPrefix"] = alias_prefix
    if time_series_type is not None:
        kwargs["timeSeriesType"] = time_series_type
    try:
        resp = await client.call("ListTimeSeries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list time series") from exc
    return ListTimeSeriesResult(
        time_series_summaries=resp.get("TimeSeriesSummaries"),
        next_token=resp.get("nextToken"),
    )


async def put_asset_model_interface_relationship(
    asset_model_id: str,
    interface_asset_model_id: str,
    property_mapping_configuration: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> PutAssetModelInterfaceRelationshipResult:
    """Put asset model interface relationship.

    Args:
        asset_model_id: Asset model id.
        interface_asset_model_id: Interface asset model id.
        property_mapping_configuration: Property mapping configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["interfaceAssetModelId"] = interface_asset_model_id
    kwargs["propertyMappingConfiguration"] = property_mapping_configuration
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("PutAssetModelInterfaceRelationship", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put asset model interface relationship") from exc
    return PutAssetModelInterfaceRelationshipResult(
        asset_model_id=resp.get("assetModelId"),
        interface_asset_model_id=resp.get("interfaceAssetModelId"),
        asset_model_arn=resp.get("assetModelArn"),
        asset_model_status=resp.get("assetModelStatus"),
    )


async def put_default_encryption_configuration(
    encryption_type: str,
    *,
    kms_key_id: str | None = None,
    region_name: str | None = None,
) -> PutDefaultEncryptionConfigurationResult:
    """Put default encryption configuration.

    Args:
        encryption_type: Encryption type.
        kms_key_id: Kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["encryptionType"] = encryption_type
    if kms_key_id is not None:
        kwargs["kmsKeyId"] = kms_key_id
    try:
        resp = await client.call("PutDefaultEncryptionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put default encryption configuration") from exc
    return PutDefaultEncryptionConfigurationResult(
        encryption_type=resp.get("encryptionType"),
        kms_key_arn=resp.get("kmsKeyArn"),
        configuration_status=resp.get("configurationStatus"),
    )


async def put_logging_options(
    logging_options: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put logging options.

    Args:
        logging_options: Logging options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loggingOptions"] = logging_options
    try:
        await client.call("PutLoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put logging options") from exc
    return None


async def put_storage_configuration(
    storage_type: str,
    *,
    multi_layer_storage: dict[str, Any] | None = None,
    disassociated_data_storage: str | None = None,
    retention_period: dict[str, Any] | None = None,
    warm_tier: str | None = None,
    warm_tier_retention_period: dict[str, Any] | None = None,
    disallow_ingest_null_na_n: bool | None = None,
    region_name: str | None = None,
) -> PutStorageConfigurationResult:
    """Put storage configuration.

    Args:
        storage_type: Storage type.
        multi_layer_storage: Multi layer storage.
        disassociated_data_storage: Disassociated data storage.
        retention_period: Retention period.
        warm_tier: Warm tier.
        warm_tier_retention_period: Warm tier retention period.
        disallow_ingest_null_na_n: Disallow ingest null na n.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["storageType"] = storage_type
    if multi_layer_storage is not None:
        kwargs["multiLayerStorage"] = multi_layer_storage
    if disassociated_data_storage is not None:
        kwargs["disassociatedDataStorage"] = disassociated_data_storage
    if retention_period is not None:
        kwargs["retentionPeriod"] = retention_period
    if warm_tier is not None:
        kwargs["warmTier"] = warm_tier
    if warm_tier_retention_period is not None:
        kwargs["warmTierRetentionPeriod"] = warm_tier_retention_period
    if disallow_ingest_null_na_n is not None:
        kwargs["disallowIngestNullNaN"] = disallow_ingest_null_na_n
    try:
        resp = await client.call("PutStorageConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put storage configuration") from exc
    return PutStorageConfigurationResult(
        storage_type=resp.get("storageType"),
        multi_layer_storage=resp.get("multiLayerStorage"),
        disassociated_data_storage=resp.get("disassociatedDataStorage"),
        retention_period=resp.get("retentionPeriod"),
        configuration_status=resp.get("configurationStatus"),
        warm_tier=resp.get("warmTier"),
        warm_tier_retention_period=resp.get("warmTierRetentionPeriod"),
        disallow_ingest_null_na_n=resp.get("disallowIngestNullNaN"),
    )


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
    client = async_client("iotsitewise", region_name)
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
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_access_policy(
    access_policy_id: str,
    access_policy_identity: dict[str, Any],
    access_policy_resource: dict[str, Any],
    access_policy_permission: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update access policy.

    Args:
        access_policy_id: Access policy id.
        access_policy_identity: Access policy identity.
        access_policy_resource: Access policy resource.
        access_policy_permission: Access policy permission.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["accessPolicyId"] = access_policy_id
    kwargs["accessPolicyIdentity"] = access_policy_identity
    kwargs["accessPolicyResource"] = access_policy_resource
    kwargs["accessPolicyPermission"] = access_policy_permission
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdateAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update access policy") from exc
    return None


async def update_asset(
    asset_id: str,
    asset_name: str,
    *,
    asset_external_id: str | None = None,
    client_token: str | None = None,
    asset_description: str | None = None,
    region_name: str | None = None,
) -> UpdateAssetResult:
    """Update asset.

    Args:
        asset_id: Asset id.
        asset_name: Asset name.
        asset_external_id: Asset external id.
        client_token: Client token.
        asset_description: Asset description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    kwargs["assetName"] = asset_name
    if asset_external_id is not None:
        kwargs["assetExternalId"] = asset_external_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if asset_description is not None:
        kwargs["assetDescription"] = asset_description
    try:
        resp = await client.call("UpdateAsset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update asset") from exc
    return UpdateAssetResult(
        asset_status=resp.get("assetStatus"),
    )


async def update_asset_model(
    asset_model_id: str,
    asset_model_name: str,
    *,
    asset_model_external_id: str | None = None,
    asset_model_description: str | None = None,
    asset_model_properties: list[dict[str, Any]] | None = None,
    asset_model_hierarchies: list[dict[str, Any]] | None = None,
    asset_model_composite_models: list[dict[str, Any]] | None = None,
    client_token: str | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    match_for_version_type: str | None = None,
    region_name: str | None = None,
) -> UpdateAssetModelResult:
    """Update asset model.

    Args:
        asset_model_id: Asset model id.
        asset_model_name: Asset model name.
        asset_model_external_id: Asset model external id.
        asset_model_description: Asset model description.
        asset_model_properties: Asset model properties.
        asset_model_hierarchies: Asset model hierarchies.
        asset_model_composite_models: Asset model composite models.
        client_token: Client token.
        if_match: If match.
        if_none_match: If none match.
        match_for_version_type: Match for version type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["assetModelName"] = asset_model_name
    if asset_model_external_id is not None:
        kwargs["assetModelExternalId"] = asset_model_external_id
    if asset_model_description is not None:
        kwargs["assetModelDescription"] = asset_model_description
    if asset_model_properties is not None:
        kwargs["assetModelProperties"] = asset_model_properties
    if asset_model_hierarchies is not None:
        kwargs["assetModelHierarchies"] = asset_model_hierarchies
    if asset_model_composite_models is not None:
        kwargs["assetModelCompositeModels"] = asset_model_composite_models
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if if_match is not None:
        kwargs["ifMatch"] = if_match
    if if_none_match is not None:
        kwargs["ifNoneMatch"] = if_none_match
    if match_for_version_type is not None:
        kwargs["matchForVersionType"] = match_for_version_type
    try:
        resp = await client.call("UpdateAssetModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update asset model") from exc
    return UpdateAssetModelResult(
        asset_model_status=resp.get("assetModelStatus"),
    )


async def update_asset_model_composite_model(
    asset_model_id: str,
    asset_model_composite_model_id: str,
    asset_model_composite_model_name: str,
    *,
    asset_model_composite_model_external_id: str | None = None,
    asset_model_composite_model_description: str | None = None,
    client_token: str | None = None,
    asset_model_composite_model_properties: list[dict[str, Any]] | None = None,
    if_match: str | None = None,
    if_none_match: str | None = None,
    match_for_version_type: str | None = None,
    region_name: str | None = None,
) -> UpdateAssetModelCompositeModelResult:
    """Update asset model composite model.

    Args:
        asset_model_id: Asset model id.
        asset_model_composite_model_id: Asset model composite model id.
        asset_model_composite_model_name: Asset model composite model name.
        asset_model_composite_model_external_id: Asset model composite model external id.
        asset_model_composite_model_description: Asset model composite model description.
        client_token: Client token.
        asset_model_composite_model_properties: Asset model composite model properties.
        if_match: If match.
        if_none_match: If none match.
        match_for_version_type: Match for version type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetModelId"] = asset_model_id
    kwargs["assetModelCompositeModelId"] = asset_model_composite_model_id
    kwargs["assetModelCompositeModelName"] = asset_model_composite_model_name
    if asset_model_composite_model_external_id is not None:
        kwargs["assetModelCompositeModelExternalId"] = asset_model_composite_model_external_id
    if asset_model_composite_model_description is not None:
        kwargs["assetModelCompositeModelDescription"] = asset_model_composite_model_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if asset_model_composite_model_properties is not None:
        kwargs["assetModelCompositeModelProperties"] = asset_model_composite_model_properties
    if if_match is not None:
        kwargs["ifMatch"] = if_match
    if if_none_match is not None:
        kwargs["ifNoneMatch"] = if_none_match
    if match_for_version_type is not None:
        kwargs["matchForVersionType"] = match_for_version_type
    try:
        resp = await client.call("UpdateAssetModelCompositeModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update asset model composite model") from exc
    return UpdateAssetModelCompositeModelResult(
        asset_model_composite_model_path=resp.get("assetModelCompositeModelPath"),
        asset_model_status=resp.get("assetModelStatus"),
    )


async def update_asset_property(
    asset_id: str,
    property_id: str,
    *,
    property_alias: str | None = None,
    property_notification_state: str | None = None,
    client_token: str | None = None,
    property_unit: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update asset property.

    Args:
        asset_id: Asset id.
        property_id: Property id.
        property_alias: Property alias.
        property_notification_state: Property notification state.
        client_token: Client token.
        property_unit: Property unit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["assetId"] = asset_id
    kwargs["propertyId"] = property_id
    if property_alias is not None:
        kwargs["propertyAlias"] = property_alias
    if property_notification_state is not None:
        kwargs["propertyNotificationState"] = property_notification_state
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if property_unit is not None:
        kwargs["propertyUnit"] = property_unit
    try:
        await client.call("UpdateAssetProperty", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update asset property") from exc
    return None


async def update_computation_model(
    computation_model_id: str,
    computation_model_name: str,
    computation_model_configuration: dict[str, Any],
    computation_model_data_binding: dict[str, Any],
    *,
    computation_model_description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdateComputationModelResult:
    """Update computation model.

    Args:
        computation_model_id: Computation model id.
        computation_model_name: Computation model name.
        computation_model_configuration: Computation model configuration.
        computation_model_data_binding: Computation model data binding.
        computation_model_description: Computation model description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["computationModelId"] = computation_model_id
    kwargs["computationModelName"] = computation_model_name
    kwargs["computationModelConfiguration"] = computation_model_configuration
    kwargs["computationModelDataBinding"] = computation_model_data_binding
    if computation_model_description is not None:
        kwargs["computationModelDescription"] = computation_model_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("UpdateComputationModel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update computation model") from exc
    return UpdateComputationModelResult(
        computation_model_status=resp.get("computationModelStatus"),
    )


async def update_dashboard(
    dashboard_id: str,
    dashboard_name: str,
    dashboard_definition: str,
    *,
    dashboard_description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update dashboard.

    Args:
        dashboard_id: Dashboard id.
        dashboard_name: Dashboard name.
        dashboard_definition: Dashboard definition.
        dashboard_description: Dashboard description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dashboardId"] = dashboard_id
    kwargs["dashboardName"] = dashboard_name
    kwargs["dashboardDefinition"] = dashboard_definition
    if dashboard_description is not None:
        kwargs["dashboardDescription"] = dashboard_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdateDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard") from exc
    return None


async def update_dataset(
    dataset_id: str,
    dataset_name: str,
    dataset_source: dict[str, Any],
    *,
    dataset_description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdateDatasetResult:
    """Update dataset.

    Args:
        dataset_id: Dataset id.
        dataset_name: Dataset name.
        dataset_source: Dataset source.
        dataset_description: Dataset description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["datasetId"] = dataset_id
    kwargs["datasetName"] = dataset_name
    kwargs["datasetSource"] = dataset_source
    if dataset_description is not None:
        kwargs["datasetDescription"] = dataset_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("UpdateDataset", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dataset") from exc
    return UpdateDatasetResult(
        dataset_id=resp.get("datasetId"),
        dataset_arn=resp.get("datasetArn"),
        dataset_status=resp.get("datasetStatus"),
    )


async def update_gateway(
    gateway_id: str,
    gateway_name: str,
    region_name: str | None = None,
) -> None:
    """Update gateway.

    Args:
        gateway_id: Gateway id.
        gateway_name: Gateway name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayId"] = gateway_id
    kwargs["gatewayName"] = gateway_name
    try:
        await client.call("UpdateGateway", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update gateway") from exc
    return None


async def update_gateway_capability_configuration(
    gateway_id: str,
    capability_namespace: str,
    capability_configuration: str,
    region_name: str | None = None,
) -> UpdateGatewayCapabilityConfigurationResult:
    """Update gateway capability configuration.

    Args:
        gateway_id: Gateway id.
        capability_namespace: Capability namespace.
        capability_configuration: Capability configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["gatewayId"] = gateway_id
    kwargs["capabilityNamespace"] = capability_namespace
    kwargs["capabilityConfiguration"] = capability_configuration
    try:
        resp = await client.call("UpdateGatewayCapabilityConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update gateway capability configuration") from exc
    return UpdateGatewayCapabilityConfigurationResult(
        capability_namespace=resp.get("capabilityNamespace"),
        capability_sync_status=resp.get("capabilitySyncStatus"),
    )


async def update_portal(
    portal_id: str,
    portal_name: str,
    portal_contact_email: str,
    role_arn: str,
    *,
    portal_description: str | None = None,
    portal_logo_image: dict[str, Any] | None = None,
    client_token: str | None = None,
    notification_sender_email: str | None = None,
    alarms: dict[str, Any] | None = None,
    portal_type: str | None = None,
    portal_type_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdatePortalResult:
    """Update portal.

    Args:
        portal_id: Portal id.
        portal_name: Portal name.
        portal_contact_email: Portal contact email.
        role_arn: Role arn.
        portal_description: Portal description.
        portal_logo_image: Portal logo image.
        client_token: Client token.
        notification_sender_email: Notification sender email.
        alarms: Alarms.
        portal_type: Portal type.
        portal_type_configuration: Portal type configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["portalId"] = portal_id
    kwargs["portalName"] = portal_name
    kwargs["portalContactEmail"] = portal_contact_email
    kwargs["roleArn"] = role_arn
    if portal_description is not None:
        kwargs["portalDescription"] = portal_description
    if portal_logo_image is not None:
        kwargs["portalLogoImage"] = portal_logo_image
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if notification_sender_email is not None:
        kwargs["notificationSenderEmail"] = notification_sender_email
    if alarms is not None:
        kwargs["alarms"] = alarms
    if portal_type is not None:
        kwargs["portalType"] = portal_type
    if portal_type_configuration is not None:
        kwargs["portalTypeConfiguration"] = portal_type_configuration
    try:
        resp = await client.call("UpdatePortal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update portal") from exc
    return UpdatePortalResult(
        portal_status=resp.get("portalStatus"),
    )


async def update_project(
    project_id: str,
    project_name: str,
    *,
    project_description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update project.

    Args:
        project_id: Project id.
        project_name: Project name.
        project_description: Project description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iotsitewise", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["projectId"] = project_id
    kwargs["projectName"] = project_name
    if project_description is not None:
        kwargs["projectDescription"] = project_description
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdateProject", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update project") from exc
    return None
