"""Tests for aws_util.aio.iot_sitewise -- 100% line coverage."""
from __future__ import annotations

import time as _time
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.iot_sitewise import (
    AssetModelResult,
    AssetResult,
    DashboardResult,
    PortalResult,
    PropertyValueResult,
    associate_assets,
    create_asset,
    create_asset_model,
    create_dashboard,
    create_portal,
    delete_asset,
    delete_asset_model,
    delete_portal,
    describe_asset,
    describe_asset_model,
    describe_portal,
    disassociate_assets,
    get_asset_property_aggregates,
    get_asset_property_value,
    get_asset_property_value_history,
    list_asset_models,
    list_assets,
    list_dashboards,
    list_portals,
    put_asset_property_values,
    wait_for_asset,
    wait_for_asset_model,
    associate_time_series_to_asset_property,
    batch_associate_project_assets,
    batch_disassociate_project_assets,
    batch_get_asset_property_aggregates,
    batch_get_asset_property_value,
    batch_get_asset_property_value_history,
    batch_put_asset_property_value,
    create_access_policy,
    create_asset_model_composite_model,
    create_bulk_import_job,
    create_computation_model,
    create_dataset,
    create_gateway,
    create_project,
    delete_access_policy,
    delete_asset_model_composite_model,
    delete_asset_model_interface_relationship,
    delete_computation_model,
    delete_dashboard,
    delete_dataset,
    delete_gateway,
    delete_project,
    delete_time_series,
    describe_access_policy,
    describe_action,
    describe_asset_composite_model,
    describe_asset_model_composite_model,
    describe_asset_model_interface_relationship,
    describe_asset_property,
    describe_bulk_import_job,
    describe_computation_model,
    describe_computation_model_execution_summary,
    describe_dashboard,
    describe_dataset,
    describe_default_encryption_configuration,
    describe_execution,
    describe_gateway,
    describe_gateway_capability_configuration,
    describe_logging_options,
    describe_project,
    describe_storage_configuration,
    describe_time_series,
    disassociate_time_series_from_asset_property,
    execute_action,
    execute_query,
    get_interpolated_asset_property_values,
    invoke_assistant,
    list_access_policies,
    list_actions,
    list_asset_model_composite_models,
    list_asset_model_properties,
    list_asset_properties,
    list_asset_relationships,
    list_associated_assets,
    list_bulk_import_jobs,
    list_composition_relationships,
    list_computation_model_data_binding_usages,
    list_computation_model_resolve_to_resources,
    list_computation_models,
    list_datasets,
    list_executions,
    list_gateways,
    list_interface_relationships,
    list_project_assets,
    list_projects,
    list_tags_for_resource,
    list_time_series,
    put_asset_model_interface_relationship,
    put_default_encryption_configuration,
    put_logging_options,
    put_storage_configuration,
    tag_resource,
    untag_resource,
    update_access_policy,
    update_asset,
    update_asset_model,
    update_asset_model_composite_model,
    update_asset_property,
    update_computation_model,
    update_dashboard,
    update_dataset,
    update_gateway,
    update_gateway_capability_configuration,
    update_portal,
    update_project,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError

R = "us-east-1"


def _mf(mc):
    return lambda *a, **kw: mc


# -- Asset model --

async def test_create_asset_model(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetModelId": "am1", "assetModelStatus": {"state": "CREATING"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await create_asset_model("m", region_name=R); assert isinstance(r, AssetModelResult)

async def test_create_asset_model_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetModelId": "am1"}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await create_asset_model("m", asset_model_properties=[{}], asset_model_hierarchies=[{}], asset_model_description="d", tags={"k": "v"}, region_name=R)

async def test_create_asset_model_runtime_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_asset_model("m", region_name=R)

async def test_create_asset_model_generic_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_asset_model("m", region_name=R)

async def test_describe_asset_model(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetModelId": "am1", "assetModelStatus": {"state": "ACTIVE"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await describe_asset_model("am1", region_name=R); assert r.asset_model_status == "ACTIVE"

async def test_describe_asset_model_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await describe_asset_model("am1", region_name=R)

async def test_list_asset_models(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetModelSummaries": [{"assetModelId": "am1"}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_asset_models(region_name=R)) == 1

async def test_list_asset_models_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"assetModelSummaries": [{"assetModelId": "am1"}], "nextToken": "t"},
        {"assetModelSummaries": [{"assetModelId": "am2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_asset_models(region_name=R)) == 2

async def test_list_asset_models_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_asset_models(region_name=R)

async def test_delete_asset_model(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await delete_asset_model("am1", region_name=R)

async def test_delete_asset_model_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_asset_model("am1", region_name=R)

# -- Asset --

async def test_create_asset(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetId": "a1", "assetStatus": {"state": "CREATING"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await create_asset("a", asset_model_id="am1", region_name=R); assert isinstance(r, AssetResult)

async def test_create_asset_tags(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetId": "a1"}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await create_asset("a", asset_model_id="am1", tags={"k": "v"}, region_name=R)

async def test_create_asset_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_asset("a", asset_model_id="am1", region_name=R)

async def test_describe_asset(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetId": "a1", "assetStatus": {"state": "ACTIVE"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await describe_asset("a1", region_name=R); assert r.asset_status == "ACTIVE"

async def test_describe_asset_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await describe_asset("a1", region_name=R)

async def test_list_assets(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetSummaries": [{"assetId": "a1"}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_assets(region_name=R)) == 1

async def test_list_assets_filter(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetSummaries": []}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await list_assets(asset_model_id="am1", region_name=R)

async def test_list_assets_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"assetSummaries": [{"assetId": "a1"}], "nextToken": "t"},
        {"assetSummaries": [{"assetId": "a2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_assets(region_name=R)) == 2

async def test_list_assets_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_assets(region_name=R)

async def test_delete_asset(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await delete_asset("a1", region_name=R)

async def test_delete_asset_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_asset("a1", region_name=R)

# -- Association --

async def test_associate_assets(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await associate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

async def test_associate_assets_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await associate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

async def test_disassociate_assets(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await disassociate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

async def test_disassociate_assets_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await disassociate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

# -- Property values --

async def test_put_asset_property_values(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"errorEntries": []}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await put_asset_property_values([{}], region_name=R); assert "errorEntries" in r

async def test_put_asset_property_values_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await put_asset_property_values([], region_name=R)

async def test_get_asset_property_value(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"propertyValue": {"value": {"doubleValue": 1.0}, "timestamp": {}}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await get_asset_property_value(asset_id="a1", property_id="p1", region_name=R)
    assert isinstance(r, PropertyValueResult)

async def test_get_asset_property_value_alias(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"propertyValue": {}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await get_asset_property_value(property_alias="/a", region_name=R)

async def test_get_asset_property_value_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await get_asset_property_value(asset_id="a1", region_name=R)

async def test_get_asset_property_aggregates(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"aggregatedValues": [{"v": 1}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await get_asset_property_aggregates(aggregate_types=["AVERAGE"], resolution="1m", start_date="s", end_date="e", asset_id="a1", property_id="p1", region_name=R)
    assert len(r) == 1

async def test_get_asset_property_aggregates_alias(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"aggregatedValues": []}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await get_asset_property_aggregates(aggregate_types=["MAX"], resolution="1h", start_date="s", end_date="e", property_alias="/a", region_name=R)

async def test_get_asset_property_aggregates_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"aggregatedValues": [{"v": 1}], "nextToken": "t"},
        {"aggregatedValues": [{"v": 2}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await get_asset_property_aggregates(aggregate_types=["AVERAGE"], resolution="1m", start_date="s", end_date="e", region_name=R)
    assert len(r) == 2

async def test_get_asset_property_aggregates_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await get_asset_property_aggregates(aggregate_types=[], resolution="1m", start_date="s", end_date="e", region_name=R)

async def test_get_asset_property_value_history(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetPropertyValueHistory": [{"value": {}}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await get_asset_property_value_history(asset_id="a1", property_id="p1", start_date="s", end_date="e", region_name=R)
    assert len(r) == 1

async def test_get_asset_property_value_history_alias(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"assetPropertyValueHistory": []}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await get_asset_property_value_history(property_alias="/a", region_name=R)

async def test_get_asset_property_value_history_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"assetPropertyValueHistory": [{"value": {}}], "nextToken": "t"},
        {"assetPropertyValueHistory": [{"value": {}}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await get_asset_property_value_history(asset_id="a1", region_name=R)) == 2

async def test_get_asset_property_value_history_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await get_asset_property_value_history(asset_id="a1", region_name=R)

# -- Portal --

async def test_create_portal(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"portalId": "p1", "portalStatus": {"state": "CREATING"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await create_portal("p", portal_contact_email="a@b.com", region_name=R); assert isinstance(r, PortalResult)

async def test_create_portal_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"portalId": "p1"}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await create_portal("p", portal_contact_email="a@b.com", role_arn="arn", tags={"k": "v"}, region_name=R)

async def test_create_portal_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_portal("p", portal_contact_email="a@b.com", region_name=R)

async def test_describe_portal(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"portalId": "p1", "portalStatus": {"state": "ACTIVE"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await describe_portal("p1", region_name=R); assert r.portal_status == "ACTIVE"

async def test_describe_portal_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await describe_portal("p1", region_name=R)

async def test_list_portals(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"portalSummaries": [{"portalId": "p1"}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_portals(region_name=R)) == 1

async def test_list_portals_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"portalSummaries": [{"portalId": "p1"}], "nextToken": "t"},
        {"portalSummaries": [{"portalId": "p2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_portals(region_name=R)) == 2

async def test_list_portals_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_portals(region_name=R)

async def test_delete_portal(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await delete_portal("p1", region_name=R)

async def test_delete_portal_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_portal("p1", region_name=R)

# -- Dashboard --

async def test_create_dashboard(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"dashboardId": "d1", "dashboardArn": "arn"}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await create_dashboard("proj1", dashboard_name="d", dashboard_definition="{}", region_name=R)
    assert isinstance(r, DashboardResult)

async def test_create_dashboard_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"dashboardId": "d1"}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    await create_dashboard("proj1", dashboard_name="d", dashboard_definition="{}", dashboard_description="desc", tags={"k": "v"}, region_name=R)

async def test_create_dashboard_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_dashboard("proj1", dashboard_name="d", dashboard_definition="{}", region_name=R)

async def test_list_dashboards(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"dashboardSummaries": [{"dashboardId": "d1"}]}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_dashboards("proj1", region_name=R)) == 1

async def test_list_dashboards_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"dashboardSummaries": [{"dashboardId": "d1"}], "nextToken": "t"},
        {"dashboardSummaries": [{"dashboardId": "d2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    assert len(await list_dashboards("proj1", region_name=R)) == 2

async def test_list_dashboards_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_dashboards("proj1", region_name=R)

# -- Waiters --

async def test_wait_for_asset_model_active(monkeypatch):
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", lambda: 0)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock(); mc.call.return_value = {"assetModelId": "am1", "assetModelStatus": {"state": "ACTIVE"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await wait_for_asset_model("am1", region_name=R); assert r.asset_model_status == "ACTIVE"

async def test_wait_for_asset_model_polls_then_succeeds(monkeypatch):
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", lambda: 0)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock()
    mc.call.side_effect = [
        {"assetModelId": "am1", "assetModelStatus": {"state": "CREATING"}},
        {"assetModelId": "am1", "assetModelStatus": {"state": "ACTIVE"}},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await wait_for_asset_model("am1", region_name=R)
    assert r.asset_model_status == "ACTIVE"


async def test_wait_for_asset_model_timeout(monkeypatch):
    counter = {"n": 0}
    def mono():
        counter["n"] += 1
        return 0 if counter["n"] <= 1 else 999
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", mono)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock(); mc.call.return_value = {"assetModelId": "am1", "assetModelStatus": {"state": "CREATING"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsTimeoutError): await wait_for_asset_model("am1", timeout=1.0, region_name=R)

async def test_wait_for_asset_active(monkeypatch):
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", lambda: 0)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock(); mc.call.return_value = {"assetId": "a1", "assetStatus": {"state": "ACTIVE"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await wait_for_asset("a1", region_name=R); assert r.asset_status == "ACTIVE"

async def test_wait_for_asset_timeout(monkeypatch):
    counter = {"n": 0}
    def mono():
        counter["n"] += 1
        return 0 if counter["n"] <= 1 else 999
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", mono)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock(); mc.call.return_value = {"assetId": "a1", "assetStatus": {"state": "CREATING"}}
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    with pytest.raises(AwsTimeoutError): await wait_for_asset("a1", timeout=1.0, region_name=R)


async def test_wait_for_asset_polls_then_succeeds(monkeypatch):
    monkeypatch.setattr("aws_util.aio.iot_sitewise.time.monotonic", lambda: 0)
    monkeypatch.setattr("aws_util.aio.iot_sitewise.asyncio.sleep", AsyncMock())
    mc = AsyncMock()
    mc.call.side_effect = [
        {"assetId": "a1", "assetStatus": {"state": "CREATING"}},
        {"assetId": "a1", "assetStatus": {"state": "ACTIVE"}},
    ]
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", _mf(mc))
    r = await wait_for_asset("a1", region_name=R)
    assert r.asset_status == "ACTIVE"


async def test_associate_time_series_to_asset_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", )
    mock_client.call.assert_called_once()


async def test_associate_time_series_to_asset_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", )


async def test_batch_associate_project_assets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_project_assets("test-project_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_associate_project_assets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_project_assets("test-project_id", [], )


async def test_batch_disassociate_project_assets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_project_assets("test-project_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_project_assets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_project_assets("test-project_id", [], )


async def test_batch_get_asset_property_aggregates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_asset_property_aggregates([], )
    mock_client.call.assert_called_once()


async def test_batch_get_asset_property_aggregates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_asset_property_aggregates([], )


async def test_batch_get_asset_property_value(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_asset_property_value([], )
    mock_client.call.assert_called_once()


async def test_batch_get_asset_property_value_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_asset_property_value([], )


async def test_batch_get_asset_property_value_history(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_asset_property_value_history([], )
    mock_client.call.assert_called_once()


async def test_batch_get_asset_property_value_history_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_asset_property_value_history([], )


async def test_batch_put_asset_property_value(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_put_asset_property_value([], )
    mock_client.call.assert_called_once()


async def test_batch_put_asset_property_value_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_put_asset_property_value([], )


async def test_create_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_access_policy({}, {}, "test-access_policy_permission", )
    mock_client.call.assert_called_once()


async def test_create_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_access_policy({}, {}, "test-access_policy_permission", )


async def test_create_asset_model_composite_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", )
    mock_client.call.assert_called_once()


async def test_create_asset_model_composite_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", )


async def test_create_bulk_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_bulk_import_job("test-job_name", "test-job_role_arn", [], {}, {}, )
    mock_client.call.assert_called_once()


async def test_create_bulk_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_bulk_import_job("test-job_name", "test-job_role_arn", [], {}, {}, )


async def test_create_computation_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_computation_model("test-computation_model_name", {}, {}, )
    mock_client.call.assert_called_once()


async def test_create_computation_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_computation_model("test-computation_model_name", {}, {}, )


async def test_create_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dataset("test-dataset_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dataset("test-dataset_name", {}, )


async def test_create_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_gateway("test-gateway_name", {}, )
    mock_client.call.assert_called_once()


async def test_create_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_gateway("test-gateway_name", {}, )


async def test_create_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_project("test-portal_id", "test-project_name", )
    mock_client.call.assert_called_once()


async def test_create_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_project("test-portal_id", "test-project_name", )


async def test_delete_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_access_policy("test-access_policy_id", )
    mock_client.call.assert_called_once()


async def test_delete_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_access_policy("test-access_policy_id", )


async def test_delete_asset_model_composite_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", )
    mock_client.call.assert_called_once()


async def test_delete_asset_model_composite_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", )


async def test_delete_asset_model_interface_relationship(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", )
    mock_client.call.assert_called_once()


async def test_delete_asset_model_interface_relationship_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", )


async def test_delete_computation_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_computation_model("test-computation_model_id", )
    mock_client.call.assert_called_once()


async def test_delete_computation_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_computation_model("test-computation_model_id", )


async def test_delete_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dashboard("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_delete_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dashboard("test-dashboard_id", )


async def test_delete_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dataset("test-dataset_id", )
    mock_client.call.assert_called_once()


async def test_delete_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dataset("test-dataset_id", )


async def test_delete_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_gateway("test-gateway_id", )
    mock_client.call.assert_called_once()


async def test_delete_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_gateway("test-gateway_id", )


async def test_delete_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_project("test-project_id", )
    mock_client.call.assert_called_once()


async def test_delete_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_project("test-project_id", )


async def test_delete_time_series(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_time_series()
    mock_client.call.assert_called_once()


async def test_delete_time_series_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_time_series()


async def test_describe_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_access_policy("test-access_policy_id", )
    mock_client.call.assert_called_once()


async def test_describe_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_access_policy("test-access_policy_id", )


async def test_describe_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_action("test-action_id", )
    mock_client.call.assert_called_once()


async def test_describe_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_action("test-action_id", )


async def test_describe_asset_composite_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_composite_model("test-asset_id", "test-asset_composite_model_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_composite_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_composite_model("test-asset_id", "test-asset_composite_model_id", )


async def test_describe_asset_model_composite_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_model_composite_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", )


async def test_describe_asset_model_interface_relationship(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_model_interface_relationship_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", )


async def test_describe_asset_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_property("test-asset_id", "test-property_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_property("test-asset_id", "test-property_id", )


async def test_describe_bulk_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bulk_import_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_bulk_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bulk_import_job("test-job_id", )


async def test_describe_computation_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_computation_model("test-computation_model_id", )
    mock_client.call.assert_called_once()


async def test_describe_computation_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_computation_model("test-computation_model_id", )


async def test_describe_computation_model_execution_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_computation_model_execution_summary("test-computation_model_id", )
    mock_client.call.assert_called_once()


async def test_describe_computation_model_execution_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_computation_model_execution_summary("test-computation_model_id", )


async def test_describe_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboard("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboard("test-dashboard_id", )


async def test_describe_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dataset("test-dataset_id", )
    mock_client.call.assert_called_once()


async def test_describe_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dataset("test-dataset_id", )


async def test_describe_default_encryption_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_default_encryption_configuration()
    mock_client.call.assert_called_once()


async def test_describe_default_encryption_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_default_encryption_configuration()


async def test_describe_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_execution("test-execution_id", )
    mock_client.call.assert_called_once()


async def test_describe_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_execution("test-execution_id", )


async def test_describe_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_gateway("test-gateway_id", )
    mock_client.call.assert_called_once()


async def test_describe_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_gateway("test-gateway_id", )


async def test_describe_gateway_capability_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", )
    mock_client.call.assert_called_once()


async def test_describe_gateway_capability_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", )


async def test_describe_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_logging_options()
    mock_client.call.assert_called_once()


async def test_describe_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_logging_options()


async def test_describe_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_project("test-project_id", )
    mock_client.call.assert_called_once()


async def test_describe_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_project("test-project_id", )


async def test_describe_storage_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_storage_configuration()
    mock_client.call.assert_called_once()


async def test_describe_storage_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_storage_configuration()


async def test_describe_time_series(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_time_series()
    mock_client.call.assert_called_once()


async def test_describe_time_series_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_time_series()


async def test_disassociate_time_series_from_asset_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_time_series_from_asset_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", )


async def test_execute_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_action({}, "test-action_definition_id", {}, )
    mock_client.call.assert_called_once()


async def test_execute_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_action({}, "test-action_definition_id", {}, )


async def test_execute_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_query("test-query_statement", )
    mock_client.call.assert_called_once()


async def test_execute_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_query("test-query_statement", )


async def test_get_interpolated_asset_property_values(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_interpolated_asset_property_values(1, 1, "test-quality", 1, "test-type_value", )
    mock_client.call.assert_called_once()


async def test_get_interpolated_asset_property_values_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_interpolated_asset_property_values(1, 1, "test-quality", 1, "test-type_value", )


async def test_invoke_assistant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await invoke_assistant("test-message", )
    mock_client.call.assert_called_once()


async def test_invoke_assistant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await invoke_assistant("test-message", )


async def test_list_access_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_policies()
    mock_client.call.assert_called_once()


async def test_list_access_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_policies()


async def test_list_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_actions("test-target_resource_type", "test-target_resource_id", )
    mock_client.call.assert_called_once()


async def test_list_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_actions("test-target_resource_type", "test-target_resource_id", )


async def test_list_asset_model_composite_models(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_model_composite_models("test-asset_model_id", )
    mock_client.call.assert_called_once()


async def test_list_asset_model_composite_models_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_model_composite_models("test-asset_model_id", )


async def test_list_asset_model_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_model_properties("test-asset_model_id", )
    mock_client.call.assert_called_once()


async def test_list_asset_model_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_model_properties("test-asset_model_id", )


async def test_list_asset_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_properties("test-asset_id", )
    mock_client.call.assert_called_once()


async def test_list_asset_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_properties("test-asset_id", )


async def test_list_asset_relationships(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_relationships("test-asset_id", "test-traversal_type", )
    mock_client.call.assert_called_once()


async def test_list_asset_relationships_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_relationships("test-asset_id", "test-traversal_type", )


async def test_list_associated_assets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associated_assets("test-asset_id", )
    mock_client.call.assert_called_once()


async def test_list_associated_assets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associated_assets("test-asset_id", )


async def test_list_bulk_import_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bulk_import_jobs()
    mock_client.call.assert_called_once()


async def test_list_bulk_import_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bulk_import_jobs()


async def test_list_composition_relationships(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_composition_relationships("test-asset_model_id", )
    mock_client.call.assert_called_once()


async def test_list_composition_relationships_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_composition_relationships("test-asset_model_id", )


async def test_list_computation_model_data_binding_usages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_computation_model_data_binding_usages({}, )
    mock_client.call.assert_called_once()


async def test_list_computation_model_data_binding_usages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_computation_model_data_binding_usages({}, )


async def test_list_computation_model_resolve_to_resources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_computation_model_resolve_to_resources("test-computation_model_id", )
    mock_client.call.assert_called_once()


async def test_list_computation_model_resolve_to_resources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_computation_model_resolve_to_resources("test-computation_model_id", )


async def test_list_computation_models(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_computation_models()
    mock_client.call.assert_called_once()


async def test_list_computation_models_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_computation_models()


async def test_list_datasets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_datasets("test-source_type", )
    mock_client.call.assert_called_once()


async def test_list_datasets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_datasets("test-source_type", )


async def test_list_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_executions("test-target_resource_type", "test-target_resource_id", )
    mock_client.call.assert_called_once()


async def test_list_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_executions("test-target_resource_type", "test-target_resource_id", )


async def test_list_gateways(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_gateways()
    mock_client.call.assert_called_once()


async def test_list_gateways_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_gateways()


async def test_list_interface_relationships(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_interface_relationships("test-interface_asset_model_id", )
    mock_client.call.assert_called_once()


async def test_list_interface_relationships_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_interface_relationships("test-interface_asset_model_id", )


async def test_list_project_assets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_project_assets("test-project_id", )
    mock_client.call.assert_called_once()


async def test_list_project_assets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_project_assets("test-project_id", )


async def test_list_projects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_projects("test-portal_id", )
    mock_client.call.assert_called_once()


async def test_list_projects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_projects("test-portal_id", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_time_series(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_time_series()
    mock_client.call.assert_called_once()


async def test_list_time_series_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_time_series()


async def test_put_asset_model_interface_relationship(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_asset_model_interface_relationship_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, )


async def test_put_default_encryption_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_default_encryption_configuration("test-encryption_type", )
    mock_client.call.assert_called_once()


async def test_put_default_encryption_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_default_encryption_configuration("test-encryption_type", )


async def test_put_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_logging_options({}, )
    mock_client.call.assert_called_once()


async def test_put_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_logging_options({}, )


async def test_put_storage_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_storage_configuration("test-storage_type", )
    mock_client.call.assert_called_once()


async def test_put_storage_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_storage_configuration("test-storage_type", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_access_policy("test-access_policy_id", {}, {}, "test-access_policy_permission", )
    mock_client.call.assert_called_once()


async def test_update_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_access_policy("test-access_policy_id", {}, {}, "test-access_policy_permission", )


async def test_update_asset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_asset("test-asset_id", "test-asset_name", )
    mock_client.call.assert_called_once()


async def test_update_asset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_asset("test-asset_id", "test-asset_name", )


async def test_update_asset_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_asset_model("test-asset_model_id", "test-asset_model_name", )
    mock_client.call.assert_called_once()


async def test_update_asset_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_asset_model("test-asset_model_id", "test-asset_model_name", )


async def test_update_asset_model_composite_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", )
    mock_client.call.assert_called_once()


async def test_update_asset_model_composite_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", )


async def test_update_asset_property(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_asset_property("test-asset_id", "test-property_id", )
    mock_client.call.assert_called_once()


async def test_update_asset_property_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_asset_property("test-asset_id", "test-property_id", )


async def test_update_computation_model(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_computation_model("test-computation_model_id", "test-computation_model_name", {}, {}, )
    mock_client.call.assert_called_once()


async def test_update_computation_model_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_computation_model("test-computation_model_id", "test-computation_model_name", {}, {}, )


async def test_update_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard("test-dashboard_id", "test-dashboard_name", "test-dashboard_definition", )
    mock_client.call.assert_called_once()


async def test_update_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard("test-dashboard_id", "test-dashboard_name", "test-dashboard_definition", )


async def test_update_dataset(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dataset("test-dataset_id", "test-dataset_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_dataset_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dataset("test-dataset_id", "test-dataset_name", {}, )


async def test_update_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_gateway("test-gateway_id", "test-gateway_name", )
    mock_client.call.assert_called_once()


async def test_update_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_gateway("test-gateway_id", "test-gateway_name", )


async def test_update_gateway_capability_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", "test-capability_configuration", )
    mock_client.call.assert_called_once()


async def test_update_gateway_capability_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", "test-capability_configuration", )


async def test_update_portal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_portal("test-portal_id", "test-portal_name", "test-portal_contact_email", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_update_portal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_portal("test-portal_id", "test-portal_name", "test-portal_contact_email", "test-role_arn", )


async def test_update_project(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_project("test-project_id", "test-project_name", )
    mock_client.call.assert_called_once()


async def test_update_project_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_sitewise.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_project("test-project_id", "test-project_name", )


@pytest.mark.asyncio
async def test_associate_time_series_to_asset_property_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import associate_time_series_to_asset_property
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_associate_project_assets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_associate_project_assets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_associate_project_assets("test-project_id", "test-asset_ids", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_disassociate_project_assets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_disassociate_project_assets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_disassociate_project_assets("test-project_id", "test-asset_ids", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_asset_property_aggregates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_get_asset_property_aggregates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_get_asset_property_aggregates("test-entries", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_asset_property_value_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_get_asset_property_value
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_get_asset_property_value("test-entries", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_asset_property_value_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_get_asset_property_value_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_get_asset_property_value_history("test-entries", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_put_asset_property_value_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import batch_put_asset_property_value
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await batch_put_asset_property_value("test-entries", enable_partial_entry_processing=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_access_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_access_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_access_policy("test-access_policy_identity", "test-access_policy_resource", "test-access_policy_permission", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_asset_model_composite_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", asset_model_composite_model_external_id="test-asset_model_composite_model_external_id", parent_asset_model_composite_model_id="test-parent_asset_model_composite_model_id", asset_model_composite_model_id="test-asset_model_composite_model_id", asset_model_composite_model_description="test-asset_model_composite_model_description", client_token="test-client_token", composed_asset_model_id="test-composed_asset_model_id", asset_model_composite_model_properties={}, if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_bulk_import_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_bulk_import_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_bulk_import_job("test-job_name", "test-job_role_arn", "test-files", 1, {}, adaptive_ingestion="test-adaptive_ingestion", delete_files_after_import=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_computation_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_computation_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_computation_model("test-computation_model_name", {}, "test-computation_model_data_binding", computation_model_description="test-computation_model_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_dataset("test-dataset_name", "test-dataset_source", dataset_id="test-dataset_id", dataset_description="test-dataset_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_gateway_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_gateway
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_gateway("test-gateway_name", "test-gateway_platform", gateway_version="test-gateway_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import create_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await create_project(1, "test-project_name", project_description="test-project_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_access_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_access_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_access_policy("test-access_policy_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_asset_model_composite_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", client_token="test-client_token", if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_asset_model_interface_relationship_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_asset_model_interface_relationship
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_computation_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_computation_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_computation_model("test-computation_model_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_dashboard("test-dashboard_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_dataset("test-dataset_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_project("test-project_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_time_series_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import delete_time_series
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await delete_time_series(alias="test-alias", asset_id="test-asset_id", property_id="test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import describe_asset_model_composite_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_computation_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import describe_computation_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await describe_computation_model("test-computation_model_id", computation_model_version="test-computation_model_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_computation_model_execution_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import describe_computation_model_execution_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await describe_computation_model_execution_summary("test-computation_model_id", resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_time_series_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import describe_time_series
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await describe_time_series(alias="test-alias", asset_id="test-asset_id", property_id="test-property_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_time_series_from_asset_property_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import disassociate_time_series_from_asset_property
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import execute_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await execute_action("test-target_resource", {}, "test-action_payload", client_token="test-client_token", resolve_to="test-resolve_to", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import execute_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await execute_query("test-query_statement", next_token="test-next_token", max_results=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_interpolated_asset_property_values_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import get_interpolated_asset_property_values
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await get_interpolated_asset_property_values("test-start_time_in_seconds", "test-end_time_in_seconds", "test-quality", "test-interval_in_seconds", "test-type_value", asset_id="test-asset_id", property_id="test-property_id", property_alias="test-property_alias", start_time_offset_in_nanos="test-start_time_offset_in_nanos", end_time_offset_in_nanos="test-end_time_offset_in_nanos", next_token="test-next_token", max_results=1, interval_window_in_seconds="test-interval_window_in_seconds", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_invoke_assistant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import invoke_assistant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await invoke_assistant("test-message", conversation_id="test-conversation_id", enable_trace=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_access_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_access_policies(identity_type="test-identity_type", identity_id="test-identity_id", resource_type="test-resource_type", resource_id="test-resource_id", iam_arn="test-iam_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_actions("test-target_resource_type", "test-target_resource_id", next_token="test-next_token", max_results=1, resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_model_composite_models_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_asset_model_composite_models
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_asset_model_composite_models("test-asset_model_id", next_token="test-next_token", max_results=1, asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_model_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_asset_model_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_asset_model_properties("test-asset_model_id", next_token="test-next_token", max_results=1, filter="test-filter", asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_properties_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_asset_properties
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_asset_properties("test-asset_id", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_relationships_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_asset_relationships
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_asset_relationships("test-asset_id", "test-traversal_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associated_assets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_associated_assets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_associated_assets("test-asset_id", hierarchy_id="test-hierarchy_id", traversal_direction="test-traversal_direction", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bulk_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_bulk_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_bulk_import_jobs(next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_composition_relationships_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_composition_relationships
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_composition_relationships("test-asset_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_computation_model_data_binding_usages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_computation_model_data_binding_usages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_computation_model_data_binding_usages([{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_computation_model_resolve_to_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_computation_model_resolve_to_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_computation_model_resolve_to_resources("test-computation_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_computation_models_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_computation_models
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_computation_models(computation_model_type="test-computation_model_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_datasets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_datasets("test-source_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_executions("test-target_resource_type", "test-target_resource_id", resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", next_token="test-next_token", max_results=1, action_type="test-action_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_gateways_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_gateways
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_gateways(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_interface_relationships_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_interface_relationships
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_interface_relationships("test-interface_asset_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_project_assets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_project_assets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_project_assets("test-project_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_projects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_projects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_projects(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_time_series_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import list_time_series
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await list_time_series(next_token="test-next_token", max_results=1, asset_id="test-asset_id", alias_prefix="test-alias_prefix", time_series_type="test-time_series_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_asset_model_interface_relationship_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import put_asset_model_interface_relationship
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_default_encryption_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import put_default_encryption_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await put_default_encryption_configuration("test-encryption_type", kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_storage_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import put_storage_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await put_storage_configuration("test-storage_type", multi_layer_storage=True, disassociated_data_storage="test-disassociated_data_storage", retention_period="test-retention_period", warm_tier="test-warm_tier", warm_tier_retention_period="test-warm_tier_retention_period", disallow_ingest_null_na_n="test-disallow_ingest_null_na_n", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_access_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_access_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_access_policy("test-access_policy_id", "test-access_policy_identity", "test-access_policy_resource", "test-access_policy_permission", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_asset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_asset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_asset("test-asset_id", "test-asset_name", asset_external_id="test-asset_external_id", client_token="test-client_token", asset_description="test-asset_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_asset_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_asset_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_asset_model("test-asset_model_id", "test-asset_model_name", asset_model_external_id="test-asset_model_external_id", asset_model_description="test-asset_model_description", asset_model_properties={}, asset_model_hierarchies="test-asset_model_hierarchies", asset_model_composite_models="test-asset_model_composite_models", client_token="test-client_token", if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_asset_model_composite_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", asset_model_composite_model_external_id="test-asset_model_composite_model_external_id", asset_model_composite_model_description="test-asset_model_composite_model_description", client_token="test-client_token", asset_model_composite_model_properties={}, if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_asset_property_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_asset_property
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_asset_property("test-asset_id", "test-property_id", property_alias="test-property_alias", property_notification_state="test-property_notification_state", client_token="test-client_token", property_unit="test-property_unit", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_computation_model_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_computation_model
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_computation_model("test-computation_model_id", "test-computation_model_name", {}, "test-computation_model_data_binding", computation_model_description="test-computation_model_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_dashboard("test-dashboard_id", "test-dashboard_name", {}, dashboard_description="test-dashboard_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_dataset("test-dataset_id", "test-dataset_name", "test-dataset_source", dataset_description="test-dataset_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_portal_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_portal
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_portal(1, 1, 1, "test-role_arn", portal_description=1, portal_logo_image=1, client_token="test-client_token", notification_sender_email="test-notification_sender_email", alarms="test-alarms", portal_type=1, portal_type_configuration=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_project_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_sitewise import update_project
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_sitewise.async_client", lambda *a, **kw: mock_client)
    await update_project("test-project_id", "test-project_name", project_description="test-project_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
