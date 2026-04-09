"""Tests for aws_util.iot_sitewise -- 100% line coverage."""
from __future__ import annotations

import time as _time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.iot_sitewise import (
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
from aws_util.exceptions import AwsTimeoutError

R = "us-east-1"


def _ce(code="ServiceException", msg="err"):
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# -- Asset model --

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_model(gc):
    c = MagicMock()
    c.create_asset_model.return_value = {"assetModelId": "am1", "assetModelArn": "arn", "assetModelStatus": {"state": "CREATING"}}
    gc.return_value = c
    r = create_asset_model("model1", region_name=R)
    assert isinstance(r, AssetModelResult) and r.asset_model_id == "am1"

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_model_opts(gc):
    c = MagicMock()
    c.create_asset_model.return_value = {"assetModelId": "am1", "assetModelStatus": "CREATING"}
    gc.return_value = c
    create_asset_model("m", asset_model_properties=[{}], asset_model_hierarchies=[{}], asset_model_description="d", tags={"k": "v"}, region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_model_err(gc):
    c = MagicMock(); c.create_asset_model.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): create_asset_model("m", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model(gc):
    c = MagicMock()
    c.describe_asset_model.return_value = {"assetModelId": "am1", "assetModelName": "m", "assetModelStatus": {"state": "ACTIVE"}}
    gc.return_value = c
    r = describe_asset_model("am1", region_name=R); assert r.asset_model_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_status_str(gc):
    c = MagicMock()
    c.describe_asset_model.return_value = {"assetModelId": "am1", "status": "ACTIVE"}
    gc.return_value = c
    r = describe_asset_model("am1", region_name=R); assert r.asset_model_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_err(gc):
    c = MagicMock(); c.describe_asset_model.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): describe_asset_model("am1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_models(gc):
    c = MagicMock()
    c.list_asset_models.return_value = {"assetModelSummaries": [{"assetModelId": "am1", "assetModelStatus": {"state": "ACTIVE"}}]}
    gc.return_value = c
    assert len(list_asset_models(region_name=R)) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_models_pagination(gc):
    c = MagicMock()
    c.list_asset_models.side_effect = [
        {"assetModelSummaries": [{"assetModelId": "am1"}], "nextToken": "t"},
        {"assetModelSummaries": [{"assetModelId": "am2"}]},
    ]
    gc.return_value = c
    assert len(list_asset_models(region_name=R)) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_models_err(gc):
    c = MagicMock(); c.list_asset_models.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): list_asset_models(region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model(gc):
    c = MagicMock(); c.delete_asset_model.return_value = {}; gc.return_value = c
    delete_asset_model("am1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model_err(gc):
    c = MagicMock(); c.delete_asset_model.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): delete_asset_model("am1", region_name=R)

# -- Asset --

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset(gc):
    c = MagicMock()
    c.create_asset.return_value = {"assetId": "a1", "assetArn": "arn", "assetStatus": {"state": "CREATING"}}
    gc.return_value = c
    r = create_asset("asset1", asset_model_id="am1", region_name=R)
    assert isinstance(r, AssetResult)

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_tags(gc):
    c = MagicMock(); c.create_asset.return_value = {"assetId": "a1", "assetStatus": "CREATING"}
    gc.return_value = c
    create_asset("a", asset_model_id="am1", tags={"k": "v"}, region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_err(gc):
    c = MagicMock(); c.create_asset.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): create_asset("a", asset_model_id="am1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset(gc):
    c = MagicMock()
    c.describe_asset.return_value = {"assetId": "a1", "assetStatus": {"state": "ACTIVE"}}
    gc.return_value = c
    r = describe_asset("a1", region_name=R); assert r.asset_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_status_str(gc):
    c = MagicMock()
    c.describe_asset.return_value = {"assetId": "a1", "status": "ACTIVE"}
    gc.return_value = c
    r = describe_asset("a1", region_name=R); assert r.asset_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_err(gc):
    c = MagicMock(); c.describe_asset.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): describe_asset("a1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_list_assets(gc):
    c = MagicMock()
    c.list_assets.return_value = {"assetSummaries": [{"assetId": "a1"}]}
    gc.return_value = c
    assert len(list_assets(region_name=R)) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_list_assets_filter(gc):
    c = MagicMock()
    c.list_assets.return_value = {"assetSummaries": []}
    gc.return_value = c
    list_assets(asset_model_id="am1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_list_assets_pagination(gc):
    c = MagicMock()
    c.list_assets.side_effect = [
        {"assetSummaries": [{"assetId": "a1"}], "nextToken": "t"},
        {"assetSummaries": [{"assetId": "a2"}]},
    ]
    gc.return_value = c
    assert len(list_assets(region_name=R)) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_list_assets_err(gc):
    c = MagicMock(); c.list_assets.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): list_assets(region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset(gc):
    c = MagicMock(); c.delete_asset.return_value = {}; gc.return_value = c
    delete_asset("a1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_err(gc):
    c = MagicMock(); c.delete_asset.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): delete_asset("a1", region_name=R)

# -- Association --

@patch("aws_util.iot_sitewise.get_client")
def test_associate_assets(gc):
    c = MagicMock(); c.associate_assets.return_value = {}; gc.return_value = c
    associate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_associate_assets_err(gc):
    c = MagicMock(); c.associate_assets.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): associate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_disassociate_assets(gc):
    c = MagicMock(); c.disassociate_assets.return_value = {}; gc.return_value = c
    disassociate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_disassociate_assets_err(gc):
    c = MagicMock(); c.disassociate_assets.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): disassociate_assets("a1", hierarchy_id="h1", child_asset_id="a2", region_name=R)

# -- Property values --

@patch("aws_util.iot_sitewise.get_client")
def test_put_asset_property_values(gc):
    c = MagicMock(); c.batch_put_asset_property_value.return_value = {"errorEntries": []}
    gc.return_value = c
    r = put_asset_property_values([{"entryId": "e1"}], region_name=R)
    assert "errorEntries" in r

@patch("aws_util.iot_sitewise.get_client")
def test_put_asset_property_values_err(gc):
    c = MagicMock(); c.batch_put_asset_property_value.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): put_asset_property_values([], region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value(gc):
    c = MagicMock()
    c.get_asset_property_value.return_value = {"propertyValue": {"value": {"doubleValue": 1.0}, "timestamp": {"timeInSeconds": 1}}}
    gc.return_value = c
    r = get_asset_property_value(asset_id="a1", property_id="p1", region_name=R)
    assert isinstance(r, PropertyValueResult)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_alias(gc):
    c = MagicMock()
    c.get_asset_property_value.return_value = {"propertyValue": {}}
    gc.return_value = c
    get_asset_property_value(property_alias="/alias", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_err(gc):
    c = MagicMock(); c.get_asset_property_value.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): get_asset_property_value(asset_id="a1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_aggregates(gc):
    c = MagicMock()
    c.get_asset_property_aggregates.return_value = {"aggregatedValues": [{"value": {}}]}
    gc.return_value = c
    r = get_asset_property_aggregates(aggregate_types=["AVERAGE"], resolution="1m", start_date="2024-01-01", end_date="2024-01-02", asset_id="a1", property_id="p1", region_name=R)
    assert len(r) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_aggregates_alias(gc):
    c = MagicMock()
    c.get_asset_property_aggregates.return_value = {"aggregatedValues": []}
    gc.return_value = c
    get_asset_property_aggregates(aggregate_types=["MAX"], resolution="1h", start_date="s", end_date="e", property_alias="/a", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_aggregates_pagination(gc):
    c = MagicMock()
    c.get_asset_property_aggregates.side_effect = [
        {"aggregatedValues": [{"v": 1}], "nextToken": "t"},
        {"aggregatedValues": [{"v": 2}]},
    ]
    gc.return_value = c
    r = get_asset_property_aggregates(aggregate_types=["AVERAGE"], resolution="1m", start_date="s", end_date="e", region_name=R)
    assert len(r) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_aggregates_err(gc):
    c = MagicMock(); c.get_asset_property_aggregates.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): get_asset_property_aggregates(aggregate_types=[], resolution="1m", start_date="s", end_date="e", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_history(gc):
    c = MagicMock()
    c.get_asset_property_value_history.return_value = {"assetPropertyValueHistory": [{"value": {}, "timestamp": {}}]}
    gc.return_value = c
    r = get_asset_property_value_history(asset_id="a1", property_id="p1", start_date="s", end_date="e", region_name=R)
    assert len(r) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_history_alias(gc):
    c = MagicMock()
    c.get_asset_property_value_history.return_value = {"assetPropertyValueHistory": []}
    gc.return_value = c
    get_asset_property_value_history(property_alias="/a", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_history_pagination(gc):
    c = MagicMock()
    c.get_asset_property_value_history.side_effect = [
        {"assetPropertyValueHistory": [{"value": {}}], "nextToken": "t"},
        {"assetPropertyValueHistory": [{"value": {}}]},
    ]
    gc.return_value = c
    assert len(get_asset_property_value_history(asset_id="a1", region_name=R)) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_get_asset_property_value_history_err(gc):
    c = MagicMock(); c.get_asset_property_value_history.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): get_asset_property_value_history(asset_id="a1", region_name=R)

# -- Portal --

@patch("aws_util.iot_sitewise.get_client")
def test_create_portal(gc):
    c = MagicMock()
    c.create_portal.return_value = {"portalId": "p1", "portalArn": "arn", "portalStatus": {"state": "CREATING"}}
    gc.return_value = c
    r = create_portal("portal1", portal_contact_email="a@b.com", region_name=R)
    assert isinstance(r, PortalResult)

@patch("aws_util.iot_sitewise.get_client")
def test_create_portal_opts(gc):
    c = MagicMock()
    c.create_portal.return_value = {"portalId": "p1", "portalStatus": "CREATING"}
    gc.return_value = c
    create_portal("p", portal_contact_email="a@b.com", role_arn="arn:role", tags={"k": "v"}, region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_create_portal_err(gc):
    c = MagicMock(); c.create_portal.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): create_portal("p", portal_contact_email="a@b.com", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_describe_portal(gc):
    c = MagicMock()
    c.describe_portal.return_value = {"portalId": "p1", "portalStatus": {"state": "ACTIVE"}, "startUrl": "https://x"}
    gc.return_value = c
    r = describe_portal("p1", region_name=R); assert r.portal_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_portal_status_str(gc):
    c = MagicMock()
    c.describe_portal.return_value = {"portalId": "p1", "status": "ACTIVE"}
    gc.return_value = c
    r = describe_portal("p1", region_name=R); assert r.portal_status == "ACTIVE"

@patch("aws_util.iot_sitewise.get_client")
def test_describe_portal_err(gc):
    c = MagicMock(); c.describe_portal.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): describe_portal("p1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_list_portals(gc):
    c = MagicMock()
    c.list_portals.return_value = {"portalSummaries": [{"portalId": "p1"}]}
    gc.return_value = c
    assert len(list_portals(region_name=R)) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_list_portals_pagination(gc):
    c = MagicMock()
    c.list_portals.side_effect = [
        {"portalSummaries": [{"portalId": "p1"}], "nextToken": "t"},
        {"portalSummaries": [{"portalId": "p2"}]},
    ]
    gc.return_value = c
    assert len(list_portals(region_name=R)) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_list_portals_err(gc):
    c = MagicMock(); c.list_portals.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): list_portals(region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_portal(gc):
    c = MagicMock(); c.delete_portal.return_value = {}; gc.return_value = c
    delete_portal("p1", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_delete_portal_err(gc):
    c = MagicMock(); c.delete_portal.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): delete_portal("p1", region_name=R)

# -- Dashboard --

@patch("aws_util.iot_sitewise.get_client")
def test_create_dashboard(gc):
    c = MagicMock()
    c.create_dashboard.return_value = {"dashboardId": "d1", "dashboardArn": "arn"}
    gc.return_value = c
    r = create_dashboard("proj1", dashboard_name="dash1", dashboard_definition="{}", region_name=R)
    assert isinstance(r, DashboardResult)

@patch("aws_util.iot_sitewise.get_client")
def test_create_dashboard_opts(gc):
    c = MagicMock()
    c.create_dashboard.return_value = {"dashboardId": "d1"}
    gc.return_value = c
    create_dashboard("proj1", dashboard_name="d", dashboard_definition="{}", dashboard_description="desc", tags={"k": "v"}, region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_create_dashboard_err(gc):
    c = MagicMock(); c.create_dashboard.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): create_dashboard("proj1", dashboard_name="d", dashboard_definition="{}", region_name=R)

@patch("aws_util.iot_sitewise.get_client")
def test_list_dashboards(gc):
    c = MagicMock()
    c.list_dashboards.return_value = {"dashboardSummaries": [{"dashboardId": "d1"}]}
    gc.return_value = c
    assert len(list_dashboards("proj1", region_name=R)) == 1

@patch("aws_util.iot_sitewise.get_client")
def test_list_dashboards_pagination(gc):
    c = MagicMock()
    c.list_dashboards.side_effect = [
        {"dashboardSummaries": [{"dashboardId": "d1"}], "nextToken": "t"},
        {"dashboardSummaries": [{"dashboardId": "d2"}]},
    ]
    gc.return_value = c
    assert len(list_dashboards("proj1", region_name=R)) == 2

@patch("aws_util.iot_sitewise.get_client")
def test_list_dashboards_err(gc):
    c = MagicMock(); c.list_dashboards.side_effect = _ce(); gc.return_value = c
    with pytest.raises(RuntimeError): list_dashboards("proj1", region_name=R)

# -- Waiters --

@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset_model")
def test_wait_for_asset_model_active(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1]
    mock_time.sleep = MagicMock()
    mock_desc.return_value = AssetModelResult(asset_model_id="am1", asset_model_status="ACTIVE")
    r = wait_for_asset_model("am1", region_name=R)
    assert r.asset_model_status == "ACTIVE"

@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset_model")
def test_wait_for_asset_model_timeout(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1, 999]
    mock_time.sleep = MagicMock()
    mock_desc.return_value = AssetModelResult(asset_model_id="am1", asset_model_status="CREATING")
    with pytest.raises(AwsTimeoutError):
        wait_for_asset_model("am1", timeout=1.0, region_name=R)

@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset")
def test_wait_for_asset_active(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1]
    mock_time.sleep = MagicMock()
    mock_desc.return_value = AssetResult(asset_id="a1", asset_status="ACTIVE")
    r = wait_for_asset("a1", region_name=R)
    assert r.asset_status == "ACTIVE"

@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset")
def test_wait_for_asset_timeout(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1, 999]
    mock_time.sleep = MagicMock()
    mock_desc.return_value = AssetResult(asset_id="a1", asset_status="CREATING")
    with pytest.raises(AwsTimeoutError):
        wait_for_asset("a1", timeout=1.0, region_name=R)


@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset_model")
def test_wait_for_asset_model_poll_then_success(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1, 2]
    mock_time.sleep = MagicMock()
    mock_desc.side_effect = [
        AssetModelResult(asset_model_id="am1", asset_model_status="CREATING"),
        AssetModelResult(asset_model_id="am1", asset_model_status="ACTIVE"),
    ]
    r = wait_for_asset_model("am1", timeout=300.0, poll_interval=5.0, region_name=R)
    assert r.asset_model_status == "ACTIVE"
    mock_time.sleep.assert_called_once_with(5.0)


@patch("aws_util.iot_sitewise.time")
@patch("aws_util.iot_sitewise.describe_asset")
def test_wait_for_asset_poll_then_success(mock_desc, mock_time):
    mock_time.monotonic.side_effect = [0, 1, 2]
    mock_time.sleep = MagicMock()
    mock_desc.side_effect = [
        AssetResult(asset_id="a1", asset_status="CREATING"),
        AssetResult(asset_id="a1", asset_status="ACTIVE"),
    ]
    r = wait_for_asset("a1", timeout=300.0, poll_interval=5.0, region_name=R)
    assert r.asset_status == "ACTIVE"
    mock_time.sleep.assert_called_once_with(5.0)


REGION = "us-east-1"


@patch("aws_util.iot_sitewise.get_client")
def test_associate_time_series_to_asset_property(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_time_series_to_asset_property.return_value = {}
    associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", region_name=REGION)
    mock_client.associate_time_series_to_asset_property.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_associate_time_series_to_asset_property_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_time_series_to_asset_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_time_series_to_asset_property",
    )
    with pytest.raises(RuntimeError, match="Failed to associate time series to asset property"):
        associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_associate_project_assets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_project_assets.return_value = {}
    batch_associate_project_assets("test-project_id", [], region_name=REGION)
    mock_client.batch_associate_project_assets.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_associate_project_assets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_associate_project_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_project_assets",
    )
    with pytest.raises(RuntimeError, match="Failed to batch associate project assets"):
        batch_associate_project_assets("test-project_id", [], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_disassociate_project_assets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_project_assets.return_value = {}
    batch_disassociate_project_assets("test-project_id", [], region_name=REGION)
    mock_client.batch_disassociate_project_assets.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_disassociate_project_assets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_disassociate_project_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_project_assets",
    )
    with pytest.raises(RuntimeError, match="Failed to batch disassociate project assets"):
        batch_disassociate_project_assets("test-project_id", [], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_aggregates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_aggregates.return_value = {}
    batch_get_asset_property_aggregates([], region_name=REGION)
    mock_client.batch_get_asset_property_aggregates.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_aggregates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_aggregates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_asset_property_aggregates",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get asset property aggregates"):
        batch_get_asset_property_aggregates([], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_value(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_value.return_value = {}
    batch_get_asset_property_value([], region_name=REGION)
    mock_client.batch_get_asset_property_value.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_value_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_value.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_asset_property_value",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get asset property value"):
        batch_get_asset_property_value([], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_value_history(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_value_history.return_value = {}
    batch_get_asset_property_value_history([], region_name=REGION)
    mock_client.batch_get_asset_property_value_history.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_get_asset_property_value_history_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_asset_property_value_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_asset_property_value_history",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get asset property value history"):
        batch_get_asset_property_value_history([], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_batch_put_asset_property_value(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_put_asset_property_value.return_value = {}
    batch_put_asset_property_value([], region_name=REGION)
    mock_client.batch_put_asset_property_value.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_batch_put_asset_property_value_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_put_asset_property_value.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_put_asset_property_value",
    )
    with pytest.raises(RuntimeError, match="Failed to batch put asset property value"):
        batch_put_asset_property_value([], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_access_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_access_policy.return_value = {}
    create_access_policy({}, {}, "test-access_policy_permission", region_name=REGION)
    mock_client.create_access_policy.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_access_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_access_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to create access policy"):
        create_access_policy({}, {}, "test-access_policy_permission", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_model_composite_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_asset_model_composite_model.return_value = {}
    create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", region_name=REGION)
    mock_client.create_asset_model_composite_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_asset_model_composite_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_asset_model_composite_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_asset_model_composite_model",
    )
    with pytest.raises(RuntimeError, match="Failed to create asset model composite model"):
        create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_bulk_import_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bulk_import_job.return_value = {}
    create_bulk_import_job("test-job_name", "test-job_role_arn", [], {}, {}, region_name=REGION)
    mock_client.create_bulk_import_job.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_bulk_import_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_bulk_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_bulk_import_job",
    )
    with pytest.raises(RuntimeError, match="Failed to create bulk import job"):
        create_bulk_import_job("test-job_name", "test-job_role_arn", [], {}, {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_computation_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_computation_model.return_value = {}
    create_computation_model("test-computation_model_name", {}, {}, region_name=REGION)
    mock_client.create_computation_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_computation_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_computation_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_computation_model",
    )
    with pytest.raises(RuntimeError, match="Failed to create computation model"):
        create_computation_model("test-computation_model_name", {}, {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_dataset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dataset.return_value = {}
    create_dataset("test-dataset_name", {}, region_name=REGION)
    mock_client.create_dataset.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_dataset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dataset",
    )
    with pytest.raises(RuntimeError, match="Failed to create dataset"):
        create_dataset("test-dataset_name", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_gateway(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_gateway.return_value = {}
    create_gateway("test-gateway_name", {}, region_name=REGION)
    mock_client.create_gateway.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_gateway_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_gateway",
    )
    with pytest.raises(RuntimeError, match="Failed to create gateway"):
        create_gateway("test-gateway_name", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_create_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_project.return_value = {}
    create_project("test-portal_id", "test-project_name", region_name=REGION)
    mock_client.create_project.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_create_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_project",
    )
    with pytest.raises(RuntimeError, match="Failed to create project"):
        create_project("test-portal_id", "test-project_name", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_access_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_access_policy.return_value = {}
    delete_access_policy("test-access_policy_id", region_name=REGION)
    mock_client.delete_access_policy.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_access_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_access_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete access policy"):
        delete_access_policy("test-access_policy_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model_composite_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_asset_model_composite_model.return_value = {}
    delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", region_name=REGION)
    mock_client.delete_asset_model_composite_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model_composite_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_asset_model_composite_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_asset_model_composite_model",
    )
    with pytest.raises(RuntimeError, match="Failed to delete asset model composite model"):
        delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model_interface_relationship(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_asset_model_interface_relationship.return_value = {}
    delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", region_name=REGION)
    mock_client.delete_asset_model_interface_relationship.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_asset_model_interface_relationship_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_asset_model_interface_relationship.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_asset_model_interface_relationship",
    )
    with pytest.raises(RuntimeError, match="Failed to delete asset model interface relationship"):
        delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_computation_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_computation_model.return_value = {}
    delete_computation_model("test-computation_model_id", region_name=REGION)
    mock_client.delete_computation_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_computation_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_computation_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_computation_model",
    )
    with pytest.raises(RuntimeError, match="Failed to delete computation model"):
        delete_computation_model("test-computation_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_dashboard(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dashboard.return_value = {}
    delete_dashboard("test-dashboard_id", region_name=REGION)
    mock_client.delete_dashboard.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_dashboard_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dashboard",
    )
    with pytest.raises(RuntimeError, match="Failed to delete dashboard"):
        delete_dashboard("test-dashboard_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_dataset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dataset.return_value = {}
    delete_dataset("test-dataset_id", region_name=REGION)
    mock_client.delete_dataset.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_dataset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dataset",
    )
    with pytest.raises(RuntimeError, match="Failed to delete dataset"):
        delete_dataset("test-dataset_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_gateway(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_gateway.return_value = {}
    delete_gateway("test-gateway_id", region_name=REGION)
    mock_client.delete_gateway.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_gateway_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_gateway",
    )
    with pytest.raises(RuntimeError, match="Failed to delete gateway"):
        delete_gateway("test-gateway_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_project.return_value = {}
    delete_project("test-project_id", region_name=REGION)
    mock_client.delete_project.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_project",
    )
    with pytest.raises(RuntimeError, match="Failed to delete project"):
        delete_project("test-project_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_delete_time_series(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_time_series.return_value = {}
    delete_time_series(region_name=REGION)
    mock_client.delete_time_series.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_delete_time_series_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_time_series.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_time_series",
    )
    with pytest.raises(RuntimeError, match="Failed to delete time series"):
        delete_time_series(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_access_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_access_policy.return_value = {}
    describe_access_policy("test-access_policy_id", region_name=REGION)
    mock_client.describe_access_policy.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_access_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_access_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to describe access policy"):
        describe_access_policy("test-access_policy_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_action.return_value = {}
    describe_action("test-action_id", region_name=REGION)
    mock_client.describe_action.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_action",
    )
    with pytest.raises(RuntimeError, match="Failed to describe action"):
        describe_action("test-action_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_composite_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_composite_model.return_value = {}
    describe_asset_composite_model("test-asset_id", "test-asset_composite_model_id", region_name=REGION)
    mock_client.describe_asset_composite_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_composite_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_composite_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_composite_model",
    )
    with pytest.raises(RuntimeError, match="Failed to describe asset composite model"):
        describe_asset_composite_model("test-asset_id", "test-asset_composite_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_composite_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_model_composite_model.return_value = {}
    describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", region_name=REGION)
    mock_client.describe_asset_model_composite_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_composite_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_model_composite_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_model_composite_model",
    )
    with pytest.raises(RuntimeError, match="Failed to describe asset model composite model"):
        describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_interface_relationship(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_model_interface_relationship.return_value = {}
    describe_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", region_name=REGION)
    mock_client.describe_asset_model_interface_relationship.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_model_interface_relationship_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_model_interface_relationship.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_model_interface_relationship",
    )
    with pytest.raises(RuntimeError, match="Failed to describe asset model interface relationship"):
        describe_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_property(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_property.return_value = {}
    describe_asset_property("test-asset_id", "test-property_id", region_name=REGION)
    mock_client.describe_asset_property.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_asset_property_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_asset_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_property",
    )
    with pytest.raises(RuntimeError, match="Failed to describe asset property"):
        describe_asset_property("test-asset_id", "test-property_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_bulk_import_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bulk_import_job.return_value = {}
    describe_bulk_import_job("test-job_id", region_name=REGION)
    mock_client.describe_bulk_import_job.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_bulk_import_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_bulk_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bulk_import_job",
    )
    with pytest.raises(RuntimeError, match="Failed to describe bulk import job"):
        describe_bulk_import_job("test-job_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_computation_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_computation_model.return_value = {}
    describe_computation_model("test-computation_model_id", region_name=REGION)
    mock_client.describe_computation_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_computation_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_computation_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_computation_model",
    )
    with pytest.raises(RuntimeError, match="Failed to describe computation model"):
        describe_computation_model("test-computation_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_computation_model_execution_summary(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_computation_model_execution_summary.return_value = {}
    describe_computation_model_execution_summary("test-computation_model_id", region_name=REGION)
    mock_client.describe_computation_model_execution_summary.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_computation_model_execution_summary_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_computation_model_execution_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_computation_model_execution_summary",
    )
    with pytest.raises(RuntimeError, match="Failed to describe computation model execution summary"):
        describe_computation_model_execution_summary("test-computation_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_dashboard(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dashboard.return_value = {}
    describe_dashboard("test-dashboard_id", region_name=REGION)
    mock_client.describe_dashboard.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_dashboard_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboard",
    )
    with pytest.raises(RuntimeError, match="Failed to describe dashboard"):
        describe_dashboard("test-dashboard_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_dataset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dataset.return_value = {}
    describe_dataset("test-dataset_id", region_name=REGION)
    mock_client.describe_dataset.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_dataset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dataset",
    )
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        describe_dataset("test-dataset_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_default_encryption_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_default_encryption_configuration.return_value = {}
    describe_default_encryption_configuration(region_name=REGION)
    mock_client.describe_default_encryption_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_default_encryption_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_default_encryption_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_default_encryption_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe default encryption configuration"):
        describe_default_encryption_configuration(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_execution.return_value = {}
    describe_execution("test-execution_id", region_name=REGION)
    mock_client.describe_execution.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to describe execution"):
        describe_execution("test-execution_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_gateway(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_gateway.return_value = {}
    describe_gateway("test-gateway_id", region_name=REGION)
    mock_client.describe_gateway.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_gateway_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_gateway",
    )
    with pytest.raises(RuntimeError, match="Failed to describe gateway"):
        describe_gateway("test-gateway_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_gateway_capability_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_gateway_capability_configuration.return_value = {}
    describe_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", region_name=REGION)
    mock_client.describe_gateway_capability_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_gateway_capability_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_gateway_capability_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_gateway_capability_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe gateway capability configuration"):
        describe_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_logging_options.return_value = {}
    describe_logging_options(region_name=REGION)
    mock_client.describe_logging_options.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to describe logging options"):
        describe_logging_options(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_project.return_value = {}
    describe_project("test-project_id", region_name=REGION)
    mock_client.describe_project.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_project",
    )
    with pytest.raises(RuntimeError, match="Failed to describe project"):
        describe_project("test-project_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_storage_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_storage_configuration.return_value = {}
    describe_storage_configuration(region_name=REGION)
    mock_client.describe_storage_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_storage_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_storage_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_storage_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe storage configuration"):
        describe_storage_configuration(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_describe_time_series(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_time_series.return_value = {}
    describe_time_series(region_name=REGION)
    mock_client.describe_time_series.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_describe_time_series_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_time_series.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_time_series",
    )
    with pytest.raises(RuntimeError, match="Failed to describe time series"):
        describe_time_series(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_disassociate_time_series_from_asset_property(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_time_series_from_asset_property.return_value = {}
    disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", region_name=REGION)
    mock_client.disassociate_time_series_from_asset_property.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_disassociate_time_series_from_asset_property_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_time_series_from_asset_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_time_series_from_asset_property",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate time series from asset property"):
        disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_execute_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.execute_action.return_value = {}
    execute_action({}, "test-action_definition_id", {}, region_name=REGION)
    mock_client.execute_action.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_execute_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.execute_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_action",
    )
    with pytest.raises(RuntimeError, match="Failed to execute action"):
        execute_action({}, "test-action_definition_id", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_execute_query(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.execute_query.return_value = {}
    execute_query("test-query_statement", region_name=REGION)
    mock_client.execute_query.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_execute_query_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.execute_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_query",
    )
    with pytest.raises(RuntimeError, match="Failed to execute query"):
        execute_query("test-query_statement", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_get_interpolated_asset_property_values(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_interpolated_asset_property_values.return_value = {}
    get_interpolated_asset_property_values(1, 1, "test-quality", 1, "test-type_value", region_name=REGION)
    mock_client.get_interpolated_asset_property_values.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_get_interpolated_asset_property_values_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_interpolated_asset_property_values.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_interpolated_asset_property_values",
    )
    with pytest.raises(RuntimeError, match="Failed to get interpolated asset property values"):
        get_interpolated_asset_property_values(1, 1, "test-quality", 1, "test-type_value", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_invoke_assistant(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.invoke_assistant.return_value = {}
    invoke_assistant("test-message", region_name=REGION)
    mock_client.invoke_assistant.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_invoke_assistant_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.invoke_assistant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "invoke_assistant",
    )
    with pytest.raises(RuntimeError, match="Failed to invoke assistant"):
        invoke_assistant("test-message", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_access_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_access_policies.return_value = {}
    list_access_policies(region_name=REGION)
    mock_client.list_access_policies.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_access_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_access_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to list access policies"):
        list_access_policies(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_actions.return_value = {}
    list_actions("test-target_resource_type", "test-target_resource_id", region_name=REGION)
    mock_client.list_actions.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to list actions"):
        list_actions("test-target_resource_type", "test-target_resource_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_model_composite_models(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_model_composite_models.return_value = {}
    list_asset_model_composite_models("test-asset_model_id", region_name=REGION)
    mock_client.list_asset_model_composite_models.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_model_composite_models_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_model_composite_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_model_composite_models",
    )
    with pytest.raises(RuntimeError, match="Failed to list asset model composite models"):
        list_asset_model_composite_models("test-asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_model_properties(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_model_properties.return_value = {}
    list_asset_model_properties("test-asset_model_id", region_name=REGION)
    mock_client.list_asset_model_properties.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_model_properties_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_model_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_model_properties",
    )
    with pytest.raises(RuntimeError, match="Failed to list asset model properties"):
        list_asset_model_properties("test-asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_properties(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_properties.return_value = {}
    list_asset_properties("test-asset_id", region_name=REGION)
    mock_client.list_asset_properties.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_properties_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_properties",
    )
    with pytest.raises(RuntimeError, match="Failed to list asset properties"):
        list_asset_properties("test-asset_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_relationships(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_relationships.return_value = {}
    list_asset_relationships("test-asset_id", "test-traversal_type", region_name=REGION)
    mock_client.list_asset_relationships.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_asset_relationships_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_asset_relationships.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_relationships",
    )
    with pytest.raises(RuntimeError, match="Failed to list asset relationships"):
        list_asset_relationships("test-asset_id", "test-traversal_type", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_associated_assets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_assets.return_value = {}
    list_associated_assets("test-asset_id", region_name=REGION)
    mock_client.list_associated_assets.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_associated_assets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_associated_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associated_assets",
    )
    with pytest.raises(RuntimeError, match="Failed to list associated assets"):
        list_associated_assets("test-asset_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_bulk_import_jobs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bulk_import_jobs.return_value = {}
    list_bulk_import_jobs(region_name=REGION)
    mock_client.list_bulk_import_jobs.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_bulk_import_jobs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_bulk_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bulk_import_jobs",
    )
    with pytest.raises(RuntimeError, match="Failed to list bulk import jobs"):
        list_bulk_import_jobs(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_composition_relationships(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_composition_relationships.return_value = {}
    list_composition_relationships("test-asset_model_id", region_name=REGION)
    mock_client.list_composition_relationships.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_composition_relationships_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_composition_relationships.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_composition_relationships",
    )
    with pytest.raises(RuntimeError, match="Failed to list composition relationships"):
        list_composition_relationships("test-asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_model_data_binding_usages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_model_data_binding_usages.return_value = {}
    list_computation_model_data_binding_usages({}, region_name=REGION)
    mock_client.list_computation_model_data_binding_usages.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_model_data_binding_usages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_model_data_binding_usages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_computation_model_data_binding_usages",
    )
    with pytest.raises(RuntimeError, match="Failed to list computation model data binding usages"):
        list_computation_model_data_binding_usages({}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_model_resolve_to_resources(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_model_resolve_to_resources.return_value = {}
    list_computation_model_resolve_to_resources("test-computation_model_id", region_name=REGION)
    mock_client.list_computation_model_resolve_to_resources.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_model_resolve_to_resources_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_model_resolve_to_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_computation_model_resolve_to_resources",
    )
    with pytest.raises(RuntimeError, match="Failed to list computation model resolve to resources"):
        list_computation_model_resolve_to_resources("test-computation_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_models(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_models.return_value = {}
    list_computation_models(region_name=REGION)
    mock_client.list_computation_models.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_computation_models_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_computation_models.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_computation_models",
    )
    with pytest.raises(RuntimeError, match="Failed to list computation models"):
        list_computation_models(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_datasets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_datasets.return_value = {}
    list_datasets("test-source_type", region_name=REGION)
    mock_client.list_datasets.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_datasets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_datasets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_datasets",
    )
    with pytest.raises(RuntimeError, match="Failed to list datasets"):
        list_datasets("test-source_type", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_executions.return_value = {}
    list_executions("test-target_resource_type", "test-target_resource_id", region_name=REGION)
    mock_client.list_executions.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list executions"):
        list_executions("test-target_resource_type", "test-target_resource_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_gateways(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_gateways.return_value = {}
    list_gateways(region_name=REGION)
    mock_client.list_gateways.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_gateways_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_gateways.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_gateways",
    )
    with pytest.raises(RuntimeError, match="Failed to list gateways"):
        list_gateways(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_interface_relationships(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_interface_relationships.return_value = {}
    list_interface_relationships("test-interface_asset_model_id", region_name=REGION)
    mock_client.list_interface_relationships.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_interface_relationships_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_interface_relationships.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_interface_relationships",
    )
    with pytest.raises(RuntimeError, match="Failed to list interface relationships"):
        list_interface_relationships("test-interface_asset_model_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_project_assets(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_project_assets.return_value = {}
    list_project_assets("test-project_id", region_name=REGION)
    mock_client.list_project_assets.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_project_assets_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_project_assets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_project_assets",
    )
    with pytest.raises(RuntimeError, match="Failed to list project assets"):
        list_project_assets("test-project_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_projects(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_projects.return_value = {}
    list_projects("test-portal_id", region_name=REGION)
    mock_client.list_projects.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_projects_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_projects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_projects",
    )
    with pytest.raises(RuntimeError, match="Failed to list projects"):
        list_projects("test-portal_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_list_time_series(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_time_series.return_value = {}
    list_time_series(region_name=REGION)
    mock_client.list_time_series.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_list_time_series_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_time_series.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_time_series",
    )
    with pytest.raises(RuntimeError, match="Failed to list time series"):
        list_time_series(region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_put_asset_model_interface_relationship(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_asset_model_interface_relationship.return_value = {}
    put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, region_name=REGION)
    mock_client.put_asset_model_interface_relationship.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_put_asset_model_interface_relationship_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_asset_model_interface_relationship.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_asset_model_interface_relationship",
    )
    with pytest.raises(RuntimeError, match="Failed to put asset model interface relationship"):
        put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_put_default_encryption_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_default_encryption_configuration.return_value = {}
    put_default_encryption_configuration("test-encryption_type", region_name=REGION)
    mock_client.put_default_encryption_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_put_default_encryption_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_default_encryption_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_default_encryption_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to put default encryption configuration"):
        put_default_encryption_configuration("test-encryption_type", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_put_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_logging_options.return_value = {}
    put_logging_options({}, region_name=REGION)
    mock_client.put_logging_options.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_put_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to put logging options"):
        put_logging_options({}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_put_storage_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_storage_configuration.return_value = {}
    put_storage_configuration("test-storage_type", region_name=REGION)
    mock_client.put_storage_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_put_storage_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_storage_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_storage_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to put storage configuration"):
        put_storage_configuration("test-storage_type", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_access_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_access_policy.return_value = {}
    update_access_policy("test-access_policy_id", {}, {}, "test-access_policy_permission", region_name=REGION)
    mock_client.update_access_policy.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_access_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_access_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to update access policy"):
        update_access_policy("test-access_policy_id", {}, {}, "test-access_policy_permission", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset.return_value = {}
    update_asset("test-asset_id", "test-asset_name", region_name=REGION)
    mock_client.update_asset.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_asset",
    )
    with pytest.raises(RuntimeError, match="Failed to update asset"):
        update_asset("test-asset_id", "test-asset_name", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_model.return_value = {}
    update_asset_model("test-asset_model_id", "test-asset_model_name", region_name=REGION)
    mock_client.update_asset_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_asset_model",
    )
    with pytest.raises(RuntimeError, match="Failed to update asset model"):
        update_asset_model("test-asset_model_id", "test-asset_model_name", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_model_composite_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_model_composite_model.return_value = {}
    update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", region_name=REGION)
    mock_client.update_asset_model_composite_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_model_composite_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_model_composite_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_asset_model_composite_model",
    )
    with pytest.raises(RuntimeError, match="Failed to update asset model composite model"):
        update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_property(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_property.return_value = {}
    update_asset_property("test-asset_id", "test-property_id", region_name=REGION)
    mock_client.update_asset_property.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_asset_property_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_asset_property.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_asset_property",
    )
    with pytest.raises(RuntimeError, match="Failed to update asset property"):
        update_asset_property("test-asset_id", "test-property_id", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_computation_model(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_computation_model.return_value = {}
    update_computation_model("test-computation_model_id", "test-computation_model_name", {}, {}, region_name=REGION)
    mock_client.update_computation_model.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_computation_model_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_computation_model.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_computation_model",
    )
    with pytest.raises(RuntimeError, match="Failed to update computation model"):
        update_computation_model("test-computation_model_id", "test-computation_model_name", {}, {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_dashboard(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dashboard.return_value = {}
    update_dashboard("test-dashboard_id", "test-dashboard_name", "test-dashboard_definition", region_name=REGION)
    mock_client.update_dashboard.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_dashboard_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard",
    )
    with pytest.raises(RuntimeError, match="Failed to update dashboard"):
        update_dashboard("test-dashboard_id", "test-dashboard_name", "test-dashboard_definition", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_dataset(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dataset.return_value = {}
    update_dataset("test-dataset_id", "test-dataset_name", {}, region_name=REGION)
    mock_client.update_dataset.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_dataset_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dataset.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dataset",
    )
    with pytest.raises(RuntimeError, match="Failed to update dataset"):
        update_dataset("test-dataset_id", "test-dataset_name", {}, region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_gateway(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_gateway.return_value = {}
    update_gateway("test-gateway_id", "test-gateway_name", region_name=REGION)
    mock_client.update_gateway.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_gateway_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_gateway",
    )
    with pytest.raises(RuntimeError, match="Failed to update gateway"):
        update_gateway("test-gateway_id", "test-gateway_name", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_gateway_capability_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_gateway_capability_configuration.return_value = {}
    update_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", "test-capability_configuration", region_name=REGION)
    mock_client.update_gateway_capability_configuration.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_gateway_capability_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_gateway_capability_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_gateway_capability_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update gateway capability configuration"):
        update_gateway_capability_configuration("test-gateway_id", "test-capability_namespace", "test-capability_configuration", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_portal(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_portal.return_value = {}
    update_portal("test-portal_id", "test-portal_name", "test-portal_contact_email", "test-role_arn", region_name=REGION)
    mock_client.update_portal.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_portal_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_portal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_portal",
    )
    with pytest.raises(RuntimeError, match="Failed to update portal"):
        update_portal("test-portal_id", "test-portal_name", "test-portal_contact_email", "test-role_arn", region_name=REGION)


@patch("aws_util.iot_sitewise.get_client")
def test_update_project(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project.return_value = {}
    update_project("test-project_id", "test-project_name", region_name=REGION)
    mock_client.update_project.assert_called_once()


@patch("aws_util.iot_sitewise.get_client")
def test_update_project_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_project.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_project",
    )
    with pytest.raises(RuntimeError, match="Failed to update project"):
        update_project("test-project_id", "test-project_name", region_name=REGION)


def test_associate_time_series_to_asset_property_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import associate_time_series_to_asset_property
    mock_client = MagicMock()
    mock_client.associate_time_series_to_asset_property.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    associate_time_series_to_asset_property("test-alias", "test-asset_id", "test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_time_series_to_asset_property.assert_called_once()

def test_batch_associate_project_assets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_associate_project_assets
    mock_client = MagicMock()
    mock_client.batch_associate_project_assets.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_associate_project_assets("test-project_id", "test-asset_ids", client_token="test-client_token", region_name="us-east-1")
    mock_client.batch_associate_project_assets.assert_called_once()

def test_batch_disassociate_project_assets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_disassociate_project_assets
    mock_client = MagicMock()
    mock_client.batch_disassociate_project_assets.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_disassociate_project_assets("test-project_id", "test-asset_ids", client_token="test-client_token", region_name="us-east-1")
    mock_client.batch_disassociate_project_assets.assert_called_once()

def test_batch_get_asset_property_aggregates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_get_asset_property_aggregates
    mock_client = MagicMock()
    mock_client.batch_get_asset_property_aggregates.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_get_asset_property_aggregates("test-entries", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.batch_get_asset_property_aggregates.assert_called_once()

def test_batch_get_asset_property_value_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_get_asset_property_value
    mock_client = MagicMock()
    mock_client.batch_get_asset_property_value.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_get_asset_property_value("test-entries", next_token="test-next_token", region_name="us-east-1")
    mock_client.batch_get_asset_property_value.assert_called_once()

def test_batch_get_asset_property_value_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_get_asset_property_value_history
    mock_client = MagicMock()
    mock_client.batch_get_asset_property_value_history.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_get_asset_property_value_history("test-entries", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.batch_get_asset_property_value_history.assert_called_once()

def test_batch_put_asset_property_value_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import batch_put_asset_property_value
    mock_client = MagicMock()
    mock_client.batch_put_asset_property_value.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    batch_put_asset_property_value("test-entries", enable_partial_entry_processing=True, region_name="us-east-1")
    mock_client.batch_put_asset_property_value.assert_called_once()

def test_create_access_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_access_policy
    mock_client = MagicMock()
    mock_client.create_access_policy.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_access_policy("test-access_policy_identity", "test-access_policy_resource", "test-access_policy_permission", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_access_policy.assert_called_once()

def test_create_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_asset_model_composite_model
    mock_client = MagicMock()
    mock_client.create_asset_model_composite_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_name", "test-asset_model_composite_model_type", asset_model_composite_model_external_id="test-asset_model_composite_model_external_id", parent_asset_model_composite_model_id="test-parent_asset_model_composite_model_id", asset_model_composite_model_id="test-asset_model_composite_model_id", asset_model_composite_model_description="test-asset_model_composite_model_description", client_token="test-client_token", composed_asset_model_id="test-composed_asset_model_id", asset_model_composite_model_properties={}, if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.create_asset_model_composite_model.assert_called_once()

def test_create_bulk_import_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_bulk_import_job
    mock_client = MagicMock()
    mock_client.create_bulk_import_job.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_bulk_import_job("test-job_name", "test-job_role_arn", "test-files", 1, {}, adaptive_ingestion="test-adaptive_ingestion", delete_files_after_import=True, region_name="us-east-1")
    mock_client.create_bulk_import_job.assert_called_once()

def test_create_computation_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_computation_model
    mock_client = MagicMock()
    mock_client.create_computation_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_computation_model("test-computation_model_name", {}, "test-computation_model_data_binding", computation_model_description="test-computation_model_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_computation_model.assert_called_once()

def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_dataset
    mock_client = MagicMock()
    mock_client.create_dataset.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_dataset("test-dataset_name", "test-dataset_source", dataset_id="test-dataset_id", dataset_description="test-dataset_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dataset.assert_called_once()

def test_create_gateway_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_gateway
    mock_client = MagicMock()
    mock_client.create_gateway.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_gateway("test-gateway_name", "test-gateway_platform", gateway_version="test-gateway_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_gateway.assert_called_once()

def test_create_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import create_project
    mock_client = MagicMock()
    mock_client.create_project.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    create_project(1, "test-project_name", project_description="test-project_description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_project.assert_called_once()

def test_delete_access_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_access_policy
    mock_client = MagicMock()
    mock_client.delete_access_policy.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_access_policy("test-access_policy_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_access_policy.assert_called_once()

def test_delete_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_asset_model_composite_model
    mock_client = MagicMock()
    mock_client.delete_asset_model_composite_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", client_token="test-client_token", if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.delete_asset_model_composite_model.assert_called_once()

def test_delete_asset_model_interface_relationship_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_asset_model_interface_relationship
    mock_client = MagicMock()
    mock_client.delete_asset_model_interface_relationship.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_asset_model_interface_relationship.assert_called_once()

def test_delete_computation_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_computation_model
    mock_client = MagicMock()
    mock_client.delete_computation_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_computation_model("test-computation_model_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_computation_model.assert_called_once()

def test_delete_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_dashboard
    mock_client = MagicMock()
    mock_client.delete_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_dashboard("test-dashboard_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_dashboard.assert_called_once()

def test_delete_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_dataset
    mock_client = MagicMock()
    mock_client.delete_dataset.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_dataset("test-dataset_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_dataset.assert_called_once()

def test_delete_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_project
    mock_client = MagicMock()
    mock_client.delete_project.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_project("test-project_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_project.assert_called_once()

def test_delete_time_series_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import delete_time_series
    mock_client = MagicMock()
    mock_client.delete_time_series.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    delete_time_series(alias="test-alias", asset_id="test-asset_id", property_id="test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_time_series.assert_called_once()

def test_describe_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import describe_asset_model_composite_model
    mock_client = MagicMock()
    mock_client.describe_asset_model_composite_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    describe_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.describe_asset_model_composite_model.assert_called_once()

def test_describe_computation_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import describe_computation_model
    mock_client = MagicMock()
    mock_client.describe_computation_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    describe_computation_model("test-computation_model_id", computation_model_version="test-computation_model_version", region_name="us-east-1")
    mock_client.describe_computation_model.assert_called_once()

def test_describe_computation_model_execution_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import describe_computation_model_execution_summary
    mock_client = MagicMock()
    mock_client.describe_computation_model_execution_summary.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    describe_computation_model_execution_summary("test-computation_model_id", resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", region_name="us-east-1")
    mock_client.describe_computation_model_execution_summary.assert_called_once()

def test_describe_time_series_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import describe_time_series
    mock_client = MagicMock()
    mock_client.describe_time_series.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    describe_time_series(alias="test-alias", asset_id="test-asset_id", property_id="test-property_id", region_name="us-east-1")
    mock_client.describe_time_series.assert_called_once()

def test_disassociate_time_series_from_asset_property_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import disassociate_time_series_from_asset_property
    mock_client = MagicMock()
    mock_client.disassociate_time_series_from_asset_property.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    disassociate_time_series_from_asset_property("test-alias", "test-asset_id", "test-property_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_time_series_from_asset_property.assert_called_once()

def test_execute_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import execute_action
    mock_client = MagicMock()
    mock_client.execute_action.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    execute_action("test-target_resource", {}, "test-action_payload", client_token="test-client_token", resolve_to="test-resolve_to", region_name="us-east-1")
    mock_client.execute_action.assert_called_once()

def test_execute_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import execute_query
    mock_client = MagicMock()
    mock_client.execute_query.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    execute_query("test-query_statement", next_token="test-next_token", max_results=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.execute_query.assert_called_once()

def test_get_interpolated_asset_property_values_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import get_interpolated_asset_property_values
    mock_client = MagicMock()
    mock_client.get_interpolated_asset_property_values.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    get_interpolated_asset_property_values("test-start_time_in_seconds", "test-end_time_in_seconds", "test-quality", "test-interval_in_seconds", "test-type_value", asset_id="test-asset_id", property_id="test-property_id", property_alias="test-property_alias", start_time_offset_in_nanos="test-start_time_offset_in_nanos", end_time_offset_in_nanos="test-end_time_offset_in_nanos", next_token="test-next_token", max_results=1, interval_window_in_seconds="test-interval_window_in_seconds", region_name="us-east-1")
    mock_client.get_interpolated_asset_property_values.assert_called_once()

def test_invoke_assistant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import invoke_assistant
    mock_client = MagicMock()
    mock_client.invoke_assistant.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    invoke_assistant("test-message", conversation_id="test-conversation_id", enable_trace=True, region_name="us-east-1")
    mock_client.invoke_assistant.assert_called_once()

def test_list_access_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_access_policies
    mock_client = MagicMock()
    mock_client.list_access_policies.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_access_policies(identity_type="test-identity_type", identity_id="test-identity_id", resource_type="test-resource_type", resource_id="test-resource_id", iam_arn="test-iam_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_access_policies.assert_called_once()

def test_list_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_actions
    mock_client = MagicMock()
    mock_client.list_actions.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_actions("test-target_resource_type", "test-target_resource_id", next_token="test-next_token", max_results=1, resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", region_name="us-east-1")
    mock_client.list_actions.assert_called_once()

def test_list_asset_model_composite_models_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_asset_model_composite_models
    mock_client = MagicMock()
    mock_client.list_asset_model_composite_models.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_asset_model_composite_models("test-asset_model_id", next_token="test-next_token", max_results=1, asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.list_asset_model_composite_models.assert_called_once()

def test_list_asset_model_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_asset_model_properties
    mock_client = MagicMock()
    mock_client.list_asset_model_properties.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_asset_model_properties("test-asset_model_id", next_token="test-next_token", max_results=1, filter="test-filter", asset_model_version="test-asset_model_version", region_name="us-east-1")
    mock_client.list_asset_model_properties.assert_called_once()

def test_list_asset_properties_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_asset_properties
    mock_client = MagicMock()
    mock_client.list_asset_properties.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_asset_properties("test-asset_id", next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.list_asset_properties.assert_called_once()

def test_list_asset_relationships_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_asset_relationships
    mock_client = MagicMock()
    mock_client.list_asset_relationships.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_asset_relationships("test-asset_id", "test-traversal_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_asset_relationships.assert_called_once()

def test_list_associated_assets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_associated_assets
    mock_client = MagicMock()
    mock_client.list_associated_assets.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_associated_assets("test-asset_id", hierarchy_id="test-hierarchy_id", traversal_direction="test-traversal_direction", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_associated_assets.assert_called_once()

def test_list_bulk_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_bulk_import_jobs
    mock_client = MagicMock()
    mock_client.list_bulk_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_bulk_import_jobs(next_token="test-next_token", max_results=1, filter="test-filter", region_name="us-east-1")
    mock_client.list_bulk_import_jobs.assert_called_once()

def test_list_composition_relationships_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_composition_relationships
    mock_client = MagicMock()
    mock_client.list_composition_relationships.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_composition_relationships("test-asset_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_composition_relationships.assert_called_once()

def test_list_computation_model_data_binding_usages_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_computation_model_data_binding_usages
    mock_client = MagicMock()
    mock_client.list_computation_model_data_binding_usages.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_computation_model_data_binding_usages([{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_computation_model_data_binding_usages.assert_called_once()

def test_list_computation_model_resolve_to_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_computation_model_resolve_to_resources
    mock_client = MagicMock()
    mock_client.list_computation_model_resolve_to_resources.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_computation_model_resolve_to_resources("test-computation_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_computation_model_resolve_to_resources.assert_called_once()

def test_list_computation_models_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_computation_models
    mock_client = MagicMock()
    mock_client.list_computation_models.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_computation_models(computation_model_type="test-computation_model_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_computation_models.assert_called_once()

def test_list_datasets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_datasets
    mock_client = MagicMock()
    mock_client.list_datasets.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_datasets("test-source_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_datasets.assert_called_once()

def test_list_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_executions
    mock_client = MagicMock()
    mock_client.list_executions.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_executions("test-target_resource_type", "test-target_resource_id", resolve_to_resource_type="test-resolve_to_resource_type", resolve_to_resource_id="test-resolve_to_resource_id", next_token="test-next_token", max_results=1, action_type="test-action_type", region_name="us-east-1")
    mock_client.list_executions.assert_called_once()

def test_list_gateways_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_gateways
    mock_client = MagicMock()
    mock_client.list_gateways.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_gateways(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_gateways.assert_called_once()

def test_list_interface_relationships_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_interface_relationships
    mock_client = MagicMock()
    mock_client.list_interface_relationships.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_interface_relationships("test-interface_asset_model_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_interface_relationships.assert_called_once()

def test_list_project_assets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_project_assets
    mock_client = MagicMock()
    mock_client.list_project_assets.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_project_assets("test-project_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_project_assets.assert_called_once()

def test_list_projects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_projects
    mock_client = MagicMock()
    mock_client.list_projects.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_projects(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_projects.assert_called_once()

def test_list_time_series_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import list_time_series
    mock_client = MagicMock()
    mock_client.list_time_series.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    list_time_series(next_token="test-next_token", max_results=1, asset_id="test-asset_id", alias_prefix="test-alias_prefix", time_series_type="test-time_series_type", region_name="us-east-1")
    mock_client.list_time_series.assert_called_once()

def test_put_asset_model_interface_relationship_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import put_asset_model_interface_relationship
    mock_client = MagicMock()
    mock_client.put_asset_model_interface_relationship.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    put_asset_model_interface_relationship("test-asset_model_id", "test-interface_asset_model_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.put_asset_model_interface_relationship.assert_called_once()

def test_put_default_encryption_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import put_default_encryption_configuration
    mock_client = MagicMock()
    mock_client.put_default_encryption_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    put_default_encryption_configuration("test-encryption_type", kms_key_id="test-kms_key_id", region_name="us-east-1")
    mock_client.put_default_encryption_configuration.assert_called_once()

def test_put_storage_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import put_storage_configuration
    mock_client = MagicMock()
    mock_client.put_storage_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    put_storage_configuration("test-storage_type", multi_layer_storage=True, disassociated_data_storage="test-disassociated_data_storage", retention_period="test-retention_period", warm_tier="test-warm_tier", warm_tier_retention_period="test-warm_tier_retention_period", disallow_ingest_null_na_n="test-disallow_ingest_null_na_n", region_name="us-east-1")
    mock_client.put_storage_configuration.assert_called_once()

def test_update_access_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_access_policy
    mock_client = MagicMock()
    mock_client.update_access_policy.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_access_policy("test-access_policy_id", "test-access_policy_identity", "test-access_policy_resource", "test-access_policy_permission", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_access_policy.assert_called_once()

def test_update_asset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_asset
    mock_client = MagicMock()
    mock_client.update_asset.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_asset("test-asset_id", "test-asset_name", asset_external_id="test-asset_external_id", client_token="test-client_token", asset_description="test-asset_description", region_name="us-east-1")
    mock_client.update_asset.assert_called_once()

def test_update_asset_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_asset_model
    mock_client = MagicMock()
    mock_client.update_asset_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_asset_model("test-asset_model_id", "test-asset_model_name", asset_model_external_id="test-asset_model_external_id", asset_model_description="test-asset_model_description", asset_model_properties={}, asset_model_hierarchies="test-asset_model_hierarchies", asset_model_composite_models="test-asset_model_composite_models", client_token="test-client_token", if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.update_asset_model.assert_called_once()

def test_update_asset_model_composite_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_asset_model_composite_model
    mock_client = MagicMock()
    mock_client.update_asset_model_composite_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_asset_model_composite_model("test-asset_model_id", "test-asset_model_composite_model_id", "test-asset_model_composite_model_name", asset_model_composite_model_external_id="test-asset_model_composite_model_external_id", asset_model_composite_model_description="test-asset_model_composite_model_description", client_token="test-client_token", asset_model_composite_model_properties={}, if_match="test-if_match", if_none_match="test-if_none_match", match_for_version_type="test-match_for_version_type", region_name="us-east-1")
    mock_client.update_asset_model_composite_model.assert_called_once()

def test_update_asset_property_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_asset_property
    mock_client = MagicMock()
    mock_client.update_asset_property.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_asset_property("test-asset_id", "test-property_id", property_alias="test-property_alias", property_notification_state="test-property_notification_state", client_token="test-client_token", property_unit="test-property_unit", region_name="us-east-1")
    mock_client.update_asset_property.assert_called_once()

def test_update_computation_model_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_computation_model
    mock_client = MagicMock()
    mock_client.update_computation_model.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_computation_model("test-computation_model_id", "test-computation_model_name", {}, "test-computation_model_data_binding", computation_model_description="test-computation_model_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_computation_model.assert_called_once()

def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_dashboard
    mock_client = MagicMock()
    mock_client.update_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_dashboard("test-dashboard_id", "test-dashboard_name", {}, dashboard_description="test-dashboard_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_dashboard.assert_called_once()

def test_update_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_dataset
    mock_client = MagicMock()
    mock_client.update_dataset.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_dataset("test-dataset_id", "test-dataset_name", "test-dataset_source", dataset_description="test-dataset_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_dataset.assert_called_once()

def test_update_portal_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_portal
    mock_client = MagicMock()
    mock_client.update_portal.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_portal(1, 1, 1, "test-role_arn", portal_description=1, portal_logo_image=1, client_token="test-client_token", notification_sender_email="test-notification_sender_email", alarms="test-alarms", portal_type=1, portal_type_configuration=1, region_name="us-east-1")
    mock_client.update_portal.assert_called_once()

def test_update_project_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_sitewise import update_project
    mock_client = MagicMock()
    mock_client.update_project.return_value = {}
    monkeypatch.setattr("aws_util.iot_sitewise.get_client", lambda *a, **kw: mock_client)
    update_project("test-project_id", "test-project_name", project_description="test-project_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_project.assert_called_once()
