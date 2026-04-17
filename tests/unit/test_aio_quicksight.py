"""Tests for aws_util.aio.quicksight module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.quicksight import (
    AnalysisResult,
    DashboardResult,
    DataSetResult,
    DataSourceResult,
    QuickSightUser,
    create_analysis,
    create_dashboard,
    create_data_source,
    create_dataset,
    delete_dashboard,
    delete_dataset,
    delete_user,
    describe_dashboard,
    describe_dataset,
    describe_user,
    list_analyses,
    list_dashboards,
    list_data_sources,
    list_datasets,
    list_users,
    register_user,
    batch_create_topic_reviewed_answer,
    batch_delete_topic_reviewed_answer,
    cancel_ingestion,
    create_account_customization,
    create_account_subscription,
    create_action_connector,
    create_brand,
    create_custom_permissions,
    create_data_set,
    create_folder,
    create_folder_membership,
    create_group,
    create_group_membership,
    create_iam_policy_assignment,
    create_ingestion,
    create_namespace,
    create_refresh_schedule,
    create_role_membership,
    create_template,
    create_template_alias,
    create_theme,
    create_theme_alias,
    create_topic,
    create_topic_refresh_schedule,
    create_vpc_connection,
    delete_account_custom_permission,
    delete_account_customization,
    delete_account_subscription,
    delete_action_connector,
    delete_analysis,
    delete_brand,
    delete_brand_assignment,
    delete_custom_permissions,
    delete_data_set,
    delete_data_set_refresh_properties,
    delete_data_source,
    delete_default_q_business_application,
    delete_folder,
    delete_folder_membership,
    delete_group,
    delete_group_membership,
    delete_iam_policy_assignment,
    delete_identity_propagation_config,
    delete_namespace,
    delete_refresh_schedule,
    delete_role_custom_permission,
    delete_role_membership,
    delete_template,
    delete_template_alias,
    delete_theme,
    delete_theme_alias,
    delete_topic,
    delete_topic_refresh_schedule,
    delete_user_by_principal_id,
    delete_user_custom_permission,
    delete_vpc_connection,
    describe_account_custom_permission,
    describe_account_customization,
    describe_account_settings,
    describe_account_subscription,
    describe_action_connector,
    describe_action_connector_permissions,
    describe_analysis,
    describe_analysis_definition,
    describe_analysis_permissions,
    describe_asset_bundle_export_job,
    describe_asset_bundle_import_job,
    describe_brand,
    describe_brand_assignment,
    describe_brand_published_version,
    describe_custom_permissions,
    describe_dashboard_definition,
    describe_dashboard_permissions,
    describe_dashboard_snapshot_job,
    describe_dashboard_snapshot_job_result,
    describe_dashboards_qa_configuration,
    describe_data_set,
    describe_data_set_permissions,
    describe_data_set_refresh_properties,
    describe_data_source,
    describe_data_source_permissions,
    describe_default_q_business_application,
    describe_folder,
    describe_folder_permissions,
    describe_folder_resolved_permissions,
    describe_group,
    describe_group_membership,
    describe_iam_policy_assignment,
    describe_ingestion,
    describe_ip_restriction,
    describe_key_registration,
    describe_namespace,
    describe_q_personalization_configuration,
    describe_quick_sight_q_search_configuration,
    describe_refresh_schedule,
    describe_role_custom_permission,
    describe_template,
    describe_template_alias,
    describe_template_definition,
    describe_template_permissions,
    describe_theme,
    describe_theme_alias,
    describe_theme_permissions,
    describe_topic,
    describe_topic_permissions,
    describe_topic_refresh,
    describe_topic_refresh_schedule,
    describe_vpc_connection,
    generate_embed_url_for_anonymous_user,
    generate_embed_url_for_registered_user,
    generate_embed_url_for_registered_user_with_identity,
    get_dashboard_embed_url,
    get_flow_metadata,
    get_flow_permissions,
    get_session_embed_url,
    list_action_connectors,
    list_asset_bundle_export_jobs,
    list_asset_bundle_import_jobs,
    list_brands,
    list_custom_permissions,
    list_dashboard_versions,
    list_data_sets,
    list_flows,
    list_folder_members,
    list_folders,
    list_folders_for_resource,
    list_group_memberships,
    list_groups,
    list_iam_policy_assignments,
    list_iam_policy_assignments_for_user,
    list_identity_propagation_configs,
    list_ingestions,
    list_namespaces,
    list_refresh_schedules,
    list_role_memberships,
    list_tags_for_resource,
    list_template_aliases,
    list_template_versions,
    list_templates,
    list_theme_aliases,
    list_theme_versions,
    list_themes,
    list_topic_refresh_schedules,
    list_topic_reviewed_answers,
    list_topics,
    list_user_groups,
    list_vpc_connections,
    predict_qa_results,
    put_data_set_refresh_properties,
    restore_analysis,
    search_action_connectors,
    search_analyses,
    search_dashboards,
    search_data_sets,
    search_data_sources,
    search_flows,
    search_folders,
    search_groups,
    search_topics,
    start_asset_bundle_export_job,
    start_asset_bundle_import_job,
    start_dashboard_snapshot_job,
    start_dashboard_snapshot_job_schedule,
    tag_resource,
    untag_resource,
    update_account_custom_permission,
    update_account_customization,
    update_account_settings,
    update_action_connector,
    update_action_connector_permissions,
    update_analysis,
    update_analysis_permissions,
    update_application_with_token_exchange_grant,
    update_brand,
    update_brand_assignment,
    update_brand_published_version,
    update_custom_permissions,
    update_dashboard,
    update_dashboard_links,
    update_dashboard_permissions,
    update_dashboard_published_version,
    update_dashboards_qa_configuration,
    update_data_set,
    update_data_set_permissions,
    update_data_source,
    update_data_source_permissions,
    update_default_q_business_application,
    update_flow_permissions,
    update_folder,
    update_folder_permissions,
    update_group,
    update_iam_policy_assignment,
    update_identity_propagation_config,
    update_ip_restriction,
    update_key_registration,
    update_public_sharing_settings,
    update_q_personalization_configuration,
    update_quick_sight_q_search_configuration,
    update_refresh_schedule,
    update_role_custom_permission,
    update_spice_capacity_configuration,
    update_template,
    update_template_alias,
    update_template_permissions,
    update_theme,
    update_theme_alias,
    update_theme_permissions,
    update_topic,
    update_topic_permissions,
    update_topic_refresh_schedule,
    update_user,
    update_user_custom_permission,
    update_vpc_connection,
)



REGION = "us-east-1"
ACCT = "123456789012"
DASH_ID = "dash-001"
DS_ID = "ds-001"
ANALYSIS_ID = "analysis-001"
SOURCE = {"SourceTemplate": {"Arn": "arn:..."}}


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# Dashboard operations
# ---------------------------------------------------------------------------


async def test_create_dashboard_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DashboardId": DASH_ID, "Arn": "arn:...", "Status": "200",
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await create_dashboard(ACCT, DASH_ID, "My Dash", SOURCE, region_name=REGION)
    assert result.dashboard_id == DASH_ID

async def test_create_dashboard_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_dashboard(ACCT, DASH_ID, "My Dash", SOURCE, region_name=REGION)


async def test_describe_dashboard_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Dashboard": {"DashboardId": DASH_ID, "Name": "d", "Arn": "arn:..."},
        "Status": "200",
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await describe_dashboard(ACCT, DASH_ID, region_name=REGION)
    assert result.dashboard_id == DASH_ID


async def test_describe_dashboard_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_dashboard(ACCT, DASH_ID, region_name=REGION)


async def test_list_dashboards_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DashboardSummaryList": [{"DashboardId": DASH_ID, "Name": "d"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_dashboards(ACCT, region_name=REGION)
    assert len(result) == 1


async def test_list_dashboards_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "DashboardSummaryList": [{"DashboardId": "d1", "Name": "d1"}],
            "NextToken": "tok",
        },
        {
            "DashboardSummaryList": [{"DashboardId": "d2", "Name": "d2"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_dashboards(ACCT, region_name=REGION)
    assert len(result) == 2


async def test_list_dashboards_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_dashboards(ACCT, region_name=REGION)


async def test_delete_dashboard_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    await delete_dashboard(ACCT, DASH_ID, region_name=REGION)


async def test_delete_dashboard_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_dashboard(ACCT, DASH_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Dataset operations
# ---------------------------------------------------------------------------


async def test_create_dataset_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DataSetId": DS_ID, "Arn": "arn:..."}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await create_dataset(
        ACCT, DS_ID, "My DS", {"t1": {}}, region_name=REGION,
    )
    assert result.dataset_id == DS_ID

async def test_create_dataset_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_dataset(ACCT, DS_ID, "ds", {"t": {}}, region_name=REGION)


async def test_describe_dataset_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DataSet": {"DataSetId": DS_ID, "Name": "ds"},
        "Status": "200",
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await describe_dataset(ACCT, DS_ID, region_name=REGION)
    assert result.dataset_id == DS_ID


async def test_describe_dataset_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_dataset(ACCT, DS_ID, region_name=REGION)


async def test_list_datasets_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DataSetSummaries": [{"DataSetId": DS_ID, "Name": "ds"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_datasets(ACCT, region_name=REGION)
    assert len(result) == 1


async def test_list_datasets_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "DataSetSummaries": [{"DataSetId": "ds1", "Name": "ds1"}],
            "NextToken": "tok",
        },
        {
            "DataSetSummaries": [{"DataSetId": "ds2", "Name": "ds2"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_datasets(ACCT, region_name=REGION)
    assert len(result) == 2


async def test_list_datasets_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_datasets(ACCT, region_name=REGION)


async def test_delete_dataset_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    await delete_dataset(ACCT, DS_ID, region_name=REGION)


async def test_delete_dataset_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_dataset(ACCT, DS_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Analysis operations
# ---------------------------------------------------------------------------


async def test_create_analysis_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"AnalysisId": ANALYSIS_ID, "Arn": "arn:..."}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await create_analysis(
        ACCT, ANALYSIS_ID, "My Analysis", SOURCE, region_name=REGION,
    )
    assert result.analysis_id == ANALYSIS_ID

async def test_create_analysis_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_analysis(ACCT, ANALYSIS_ID, "a", SOURCE, region_name=REGION)


async def test_list_analyses_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "AnalysisSummaryList": [{"AnalysisId": ANALYSIS_ID, "Name": "a"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_analyses(ACCT, region_name=REGION)
    assert len(result) == 1


async def test_list_analyses_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "AnalysisSummaryList": [{"AnalysisId": "a1", "Name": "a1"}],
            "NextToken": "tok",
        },
        {
            "AnalysisSummaryList": [{"AnalysisId": "a2", "Name": "a2"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_analyses(ACCT, region_name=REGION)
    assert len(result) == 2


async def test_list_analyses_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_analyses(ACCT, region_name=REGION)


# ---------------------------------------------------------------------------
# Data source operations
# ---------------------------------------------------------------------------


async def test_create_data_source_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DataSourceId": "dsrc-1", "Arn": "arn:..."}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await create_data_source(
        ACCT, "dsrc-1", "My Source", "ATHENA", {}, region_name=REGION,
    )
    assert result.data_source_id == "dsrc-1"

async def test_create_data_source_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_data_source(
            ACCT, "dsrc-1", "src", "S3", {}, region_name=REGION,
        )


async def test_list_data_sources_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DataSources": [{"DataSourceId": "dsrc-1", "Name": "s"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_data_sources(ACCT, region_name=REGION)
    assert len(result) == 1


async def test_list_data_sources_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "DataSources": [{"DataSourceId": "dsrc1", "Name": "s1"}],
            "NextToken": "tok",
        },
        {
            "DataSources": [{"DataSourceId": "dsrc2", "Name": "s2"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_data_sources(ACCT, region_name=REGION)
    assert len(result) == 2


async def test_list_data_sources_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_data_sources(ACCT, region_name=REGION)


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


async def test_describe_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "User": {
            "UserName": "alice", "Email": "alice@example.com",
            "Role": "ADMIN", "Arn": "arn:...",
            "IdentityType": "IAM", "Active": True,
            "PrincipalId": "p-123",
        },
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await describe_user(ACCT, "alice", region_name=REGION)
    assert result.user_name == "alice"


async def test_describe_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_user(ACCT, "alice", region_name=REGION)


async def test_list_users_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "UserList": [{"UserName": "alice", "Email": "a@e.com"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_users(ACCT, region_name=REGION)
    assert len(result) == 1


async def test_list_users_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {
            "UserList": [{"UserName": "alice", "Email": "a@e.com"}],
            "NextToken": "tok",
        },
        {
            "UserList": [{"UserName": "bob", "Email": "b@e.com"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await list_users(ACCT, region_name=REGION)
    assert len(result) == 2


async def test_list_users_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_users(ACCT, region_name=REGION)


async def test_register_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "User": {"UserName": "bob", "Email": "bob@e.com"},
    }
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await register_user(
        ACCT, "bob@e.com", "IAM", "READER", region_name=REGION,
    )
    assert result.user_name == "bob"


async def test_register_user_with_iam(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"User": {"UserName": "bob"}}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    result = await register_user(
        ACCT, "bob@e.com", "IAM", "READER",
        iam_arn="arn:aws:iam::123:user/bob",
        session_name="sess",
        region_name=REGION,
    )
    assert result.user_name == "bob"


async def test_register_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await register_user(
            ACCT, "bob@e.com", "IAM", "READER", region_name=REGION,
        )


async def test_delete_user_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    await delete_user(ACCT, "alice", region_name=REGION)


async def test_delete_user_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_user(ACCT, "alice", region_name=REGION)


async def test_batch_create_topic_reviewed_answer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_create_topic_reviewed_answer("test-aws_account_id", "test-topic_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_create_topic_reviewed_answer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_create_topic_reviewed_answer("test-aws_account_id", "test-topic_id", [], )


async def test_batch_delete_topic_reviewed_answer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_delete_topic_reviewed_answer("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_batch_delete_topic_reviewed_answer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_topic_reviewed_answer("test-aws_account_id", "test-topic_id", )


async def test_cancel_ingestion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", )
    mock_client.call.assert_called_once()


async def test_cancel_ingestion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", )


async def test_create_account_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_account_customization("test-aws_account_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_account_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_account_customization("test-aws_account_id", {}, )


async def test_create_account_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_account_subscription("test-authentication_method", "test-aws_account_id", "test-account_name", "test-notification_email", )
    mock_client.call.assert_called_once()


async def test_create_account_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_account_subscription("test-authentication_method", "test-aws_account_id", "test-account_name", "test-notification_email", )


async def test_create_action_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", "test-type_value", {}, )
    mock_client.call.assert_called_once()


async def test_create_action_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", "test-type_value", {}, )


async def test_create_brand(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_brand("test-aws_account_id", "test-brand_id", )
    mock_client.call.assert_called_once()


async def test_create_brand_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_brand("test-aws_account_id", "test-brand_id", )


async def test_create_custom_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )
    mock_client.call.assert_called_once()


async def test_create_custom_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )


async def test_create_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", )
    mock_client.call.assert_called_once()


async def test_create_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", )


async def test_create_folder(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_folder("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_create_folder_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_folder("test-aws_account_id", "test-folder_id", )


async def test_create_folder_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", )
    mock_client.call.assert_called_once()


async def test_create_folder_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", )


async def test_create_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_group("test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_create_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_group("test-group_name", "test-aws_account_id", "test-namespace", )


async def test_create_group_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_create_group_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )


async def test_create_iam_policy_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-assignment_status", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_create_iam_policy_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-assignment_status", "test-namespace", )


async def test_create_ingestion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ingestion("test-data_set_id", "test-ingestion_id", "test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_create_ingestion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ingestion("test-data_set_id", "test-ingestion_id", "test-aws_account_id", )


async def test_create_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_namespace("test-aws_account_id", "test-namespace", "test-identity_store", )
    mock_client.call.assert_called_once()


async def test_create_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_namespace("test-aws_account_id", "test-namespace", "test-identity_store", )


async def test_create_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, )


async def test_create_role_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_role_membership("test-member_name", "test-aws_account_id", "test-namespace", "test-role", )
    mock_client.call.assert_called_once()


async def test_create_role_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_role_membership("test-member_name", "test-aws_account_id", "test-namespace", "test-role", )


async def test_create_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_template("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_create_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_template("test-aws_account_id", "test-template_id", )


async def test_create_template_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, )
    mock_client.call.assert_called_once()


async def test_create_template_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, )


async def test_create_theme(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_theme("test-aws_account_id", "test-theme_id", "test-name", "test-base_theme_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_theme_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_theme("test-aws_account_id", "test-theme_id", "test-name", "test-base_theme_id", {}, )


async def test_create_theme_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, )
    mock_client.call.assert_called_once()


async def test_create_theme_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, )


async def test_create_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_topic("test-aws_account_id", "test-topic_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_topic("test-aws_account_id", "test-topic_id", {}, )


async def test_create_topic_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_topic_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_arn", {}, )


async def test_create_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", )


async def test_delete_account_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_custom_permission("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_delete_account_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_custom_permission("test-aws_account_id", )


async def test_delete_account_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_customization("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_delete_account_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_customization("test-aws_account_id", )


async def test_delete_account_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_subscription("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_delete_account_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_subscription("test-aws_account_id", )


async def test_delete_action_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_action_connector("test-aws_account_id", "test-action_connector_id", )
    mock_client.call.assert_called_once()


async def test_delete_action_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_action_connector("test-aws_account_id", "test-action_connector_id", )


async def test_delete_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_analysis("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_delete_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_analysis("test-aws_account_id", "test-analysis_id", )


async def test_delete_brand(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_brand("test-aws_account_id", "test-brand_id", )
    mock_client.call.assert_called_once()


async def test_delete_brand_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_brand("test-aws_account_id", "test-brand_id", )


async def test_delete_brand_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_brand_assignment("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_delete_brand_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_brand_assignment("test-aws_account_id", )


async def test_delete_custom_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )


async def test_delete_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_set("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_delete_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_set("test-aws_account_id", "test-data_set_id", )


async def test_delete_data_set_refresh_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_delete_data_set_refresh_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", )


async def test_delete_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_source("test-aws_account_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_delete_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_source("test-aws_account_id", "test-data_source_id", )


async def test_delete_default_q_business_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_default_q_business_application("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_delete_default_q_business_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_default_q_business_application("test-aws_account_id", )


async def test_delete_folder(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_folder("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_delete_folder_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_folder("test-aws_account_id", "test-folder_id", )


async def test_delete_folder_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", )
    mock_client.call.assert_called_once()


async def test_delete_folder_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", )


async def test_delete_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_group("test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_group("test-group_name", "test-aws_account_id", "test-namespace", )


async def test_delete_group_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_group_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )


async def test_delete_iam_policy_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_iam_policy_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )


async def test_delete_identity_propagation_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_identity_propagation_config("test-aws_account_id", "test-service", )
    mock_client.call.assert_called_once()


async def test_delete_identity_propagation_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_identity_propagation_config("test-aws_account_id", "test-service", )


async def test_delete_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_namespace("test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_namespace("test-aws_account_id", "test-namespace", )


async def test_delete_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_refresh_schedule("test-data_set_id", "test-aws_account_id", "test-schedule_id", )
    mock_client.call.assert_called_once()


async def test_delete_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_refresh_schedule("test-data_set_id", "test-aws_account_id", "test-schedule_id", )


async def test_delete_role_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_role_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", )


async def test_delete_role_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role_membership("test-member_name", "test-role", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_role_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role_membership("test-member_name", "test-role", "test-aws_account_id", "test-namespace", )


async def test_delete_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_template("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_delete_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_template("test-aws_account_id", "test-template_id", )


async def test_delete_template_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", )
    mock_client.call.assert_called_once()


async def test_delete_template_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", )


async def test_delete_theme(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_theme("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_delete_theme_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_theme("test-aws_account_id", "test-theme_id", )


async def test_delete_theme_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", )
    mock_client.call.assert_called_once()


async def test_delete_theme_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", )


async def test_delete_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_topic("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_delete_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_topic("test-aws_account_id", "test-topic_id", )


async def test_delete_topic_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", )
    mock_client.call.assert_called_once()


async def test_delete_topic_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", )


async def test_delete_user_by_principal_id(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_by_principal_id("test-principal_id", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_user_by_principal_id_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_by_principal_id("test-principal_id", "test-aws_account_id", "test-namespace", )


async def test_delete_user_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_delete_user_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", )


async def test_delete_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_connection("test-aws_account_id", "test-vpc_connection_id", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_connection("test-aws_account_id", "test-vpc_connection_id", )


async def test_describe_account_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_custom_permission("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_custom_permission("test-aws_account_id", )


async def test_describe_account_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_customization("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_customization("test-aws_account_id", )


async def test_describe_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_settings("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_settings("test-aws_account_id", )


async def test_describe_account_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_subscription("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_subscription("test-aws_account_id", )


async def test_describe_action_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_action_connector("test-aws_account_id", "test-action_connector_id", )
    mock_client.call.assert_called_once()


async def test_describe_action_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_action_connector("test-aws_account_id", "test-action_connector_id", )


async def test_describe_action_connector_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_action_connector_permissions("test-aws_account_id", "test-action_connector_id", )
    mock_client.call.assert_called_once()


async def test_describe_action_connector_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_action_connector_permissions("test-aws_account_id", "test-action_connector_id", )


async def test_describe_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_analysis("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_describe_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_analysis("test-aws_account_id", "test-analysis_id", )


async def test_describe_analysis_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_analysis_definition("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_describe_analysis_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_analysis_definition("test-aws_account_id", "test-analysis_id", )


async def test_describe_analysis_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_analysis_permissions("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_describe_analysis_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_analysis_permissions("test-aws_account_id", "test-analysis_id", )


async def test_describe_asset_bundle_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_bundle_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", )


async def test_describe_asset_bundle_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", )
    mock_client.call.assert_called_once()


async def test_describe_asset_bundle_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", )


async def test_describe_brand(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_brand("test-aws_account_id", "test-brand_id", )
    mock_client.call.assert_called_once()


async def test_describe_brand_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_brand("test-aws_account_id", "test-brand_id", )


async def test_describe_brand_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_brand_assignment("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_brand_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_brand_assignment("test-aws_account_id", )


async def test_describe_brand_published_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_brand_published_version("test-aws_account_id", "test-brand_id", )
    mock_client.call.assert_called_once()


async def test_describe_brand_published_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_brand_published_version("test-aws_account_id", "test-brand_id", )


async def test_describe_custom_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )
    mock_client.call.assert_called_once()


async def test_describe_custom_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )


async def test_describe_dashboard_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboard_definition("test-aws_account_id", "test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboard_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboard_definition("test-aws_account_id", "test-dashboard_id", )


async def test_describe_dashboard_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboard_permissions("test-aws_account_id", "test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboard_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboard_permissions("test-aws_account_id", "test-dashboard_id", )


async def test_describe_dashboard_snapshot_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboard_snapshot_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", )


async def test_describe_dashboard_snapshot_job_result(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboard_snapshot_job_result("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboard_snapshot_job_result_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboard_snapshot_job_result("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", )


async def test_describe_dashboards_qa_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dashboards_qa_configuration("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_dashboards_qa_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dashboards_qa_configuration("test-aws_account_id", )


async def test_describe_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_set("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_describe_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_set("test-aws_account_id", "test-data_set_id", )


async def test_describe_data_set_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_set_permissions("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_describe_data_set_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_set_permissions("test-aws_account_id", "test-data_set_id", )


async def test_describe_data_set_refresh_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_describe_data_set_refresh_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", )


async def test_describe_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_source("test-aws_account_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_describe_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_source("test-aws_account_id", "test-data_source_id", )


async def test_describe_data_source_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_data_source_permissions("test-aws_account_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_describe_data_source_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_data_source_permissions("test-aws_account_id", "test-data_source_id", )


async def test_describe_default_q_business_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_default_q_business_application("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_default_q_business_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_default_q_business_application("test-aws_account_id", )


async def test_describe_folder(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_folder("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_describe_folder_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_folder("test-aws_account_id", "test-folder_id", )


async def test_describe_folder_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_folder_permissions("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_describe_folder_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_folder_permissions("test-aws_account_id", "test-folder_id", )


async def test_describe_folder_resolved_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_folder_resolved_permissions("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_describe_folder_resolved_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_folder_resolved_permissions("test-aws_account_id", "test-folder_id", )


async def test_describe_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_group("test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_group("test-group_name", "test-aws_account_id", "test-namespace", )


async def test_describe_group_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_group_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", )


async def test_describe_iam_policy_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_iam_policy_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )


async def test_describe_ingestion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", )
    mock_client.call.assert_called_once()


async def test_describe_ingestion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", )


async def test_describe_ip_restriction(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ip_restriction("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_ip_restriction_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ip_restriction("test-aws_account_id", )


async def test_describe_key_registration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_key_registration("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_key_registration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_key_registration("test-aws_account_id", )


async def test_describe_namespace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_namespace("test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_namespace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_namespace("test-aws_account_id", "test-namespace", )


async def test_describe_q_personalization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_q_personalization_configuration("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_q_personalization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_q_personalization_configuration("test-aws_account_id", )


async def test_describe_quick_sight_q_search_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_quick_sight_q_search_configuration("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_describe_quick_sight_q_search_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_quick_sight_q_search_configuration("test-aws_account_id", )


async def test_describe_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_refresh_schedule("test-aws_account_id", "test-data_set_id", "test-schedule_id", )
    mock_client.call.assert_called_once()


async def test_describe_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_refresh_schedule("test-aws_account_id", "test-data_set_id", "test-schedule_id", )


async def test_describe_role_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_describe_role_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", )


async def test_describe_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_template("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_describe_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_template("test-aws_account_id", "test-template_id", )


async def test_describe_template_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", )
    mock_client.call.assert_called_once()


async def test_describe_template_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", )


async def test_describe_template_definition(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_template_definition("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_describe_template_definition_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_template_definition("test-aws_account_id", "test-template_id", )


async def test_describe_template_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_template_permissions("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_describe_template_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_template_permissions("test-aws_account_id", "test-template_id", )


async def test_describe_theme(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_theme("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_describe_theme_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_theme("test-aws_account_id", "test-theme_id", )


async def test_describe_theme_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", )
    mock_client.call.assert_called_once()


async def test_describe_theme_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", )


async def test_describe_theme_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_theme_permissions("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_describe_theme_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_theme_permissions("test-aws_account_id", "test-theme_id", )


async def test_describe_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_topic("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_describe_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_topic("test-aws_account_id", "test-topic_id", )


async def test_describe_topic_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_topic_permissions("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_describe_topic_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_topic_permissions("test-aws_account_id", "test-topic_id", )


async def test_describe_topic_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_topic_refresh("test-aws_account_id", "test-topic_id", "test-refresh_id", )
    mock_client.call.assert_called_once()


async def test_describe_topic_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_topic_refresh("test-aws_account_id", "test-topic_id", "test-refresh_id", )


async def test_describe_topic_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", )
    mock_client.call.assert_called_once()


async def test_describe_topic_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", )


async def test_describe_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_connection("test-aws_account_id", "test-vpc_connection_id", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_connection("test-aws_account_id", "test-vpc_connection_id", )


async def test_generate_embed_url_for_anonymous_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_embed_url_for_anonymous_user("test-aws_account_id", "test-namespace", [], {}, )
    mock_client.call.assert_called_once()


async def test_generate_embed_url_for_anonymous_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_embed_url_for_anonymous_user("test-aws_account_id", "test-namespace", [], {}, )


async def test_generate_embed_url_for_registered_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_embed_url_for_registered_user("test-aws_account_id", "test-user_arn", {}, )
    mock_client.call.assert_called_once()


async def test_generate_embed_url_for_registered_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_embed_url_for_registered_user("test-aws_account_id", "test-user_arn", {}, )


async def test_generate_embed_url_for_registered_user_with_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_embed_url_for_registered_user_with_identity("test-aws_account_id", {}, )
    mock_client.call.assert_called_once()


async def test_generate_embed_url_for_registered_user_with_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_embed_url_for_registered_user_with_identity("test-aws_account_id", {}, )


async def test_get_dashboard_embed_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dashboard_embed_url("test-aws_account_id", "test-dashboard_id", "test-identity_type", )
    mock_client.call.assert_called_once()


async def test_get_dashboard_embed_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dashboard_embed_url("test-aws_account_id", "test-dashboard_id", "test-identity_type", )


async def test_get_flow_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_metadata("test-aws_account_id", "test-flow_id", )
    mock_client.call.assert_called_once()


async def test_get_flow_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_metadata("test-aws_account_id", "test-flow_id", )


async def test_get_flow_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_permissions("test-aws_account_id", "test-flow_id", )
    mock_client.call.assert_called_once()


async def test_get_flow_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_permissions("test-aws_account_id", "test-flow_id", )


async def test_get_session_embed_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_session_embed_url("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_get_session_embed_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_session_embed_url("test-aws_account_id", )


async def test_list_action_connectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_action_connectors("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_action_connectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_action_connectors("test-aws_account_id", )


async def test_list_asset_bundle_export_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_bundle_export_jobs("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_asset_bundle_export_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_bundle_export_jobs("test-aws_account_id", )


async def test_list_asset_bundle_import_jobs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_asset_bundle_import_jobs("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_asset_bundle_import_jobs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_asset_bundle_import_jobs("test-aws_account_id", )


async def test_list_brands(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_brands("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_brands_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_brands("test-aws_account_id", )


async def test_list_custom_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_permissions("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_custom_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_permissions("test-aws_account_id", )


async def test_list_dashboard_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dashboard_versions("test-aws_account_id", "test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_list_dashboard_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dashboard_versions("test-aws_account_id", "test-dashboard_id", )


async def test_list_data_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_data_sets("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_data_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_sets("test-aws_account_id", )


async def test_list_flows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_flows("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_flows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_flows("test-aws_account_id", )


async def test_list_folder_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_folder_members("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_list_folder_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_folder_members("test-aws_account_id", "test-folder_id", )


async def test_list_folders(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_folders("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_folders_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_folders("test-aws_account_id", )


async def test_list_folders_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_folders_for_resource("test-aws_account_id", "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_folders_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_folders_for_resource("test-aws_account_id", "test-resource_arn", )


async def test_list_group_memberships(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_group_memberships("test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_group_memberships_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_group_memberships("test-group_name", "test-aws_account_id", "test-namespace", )


async def test_list_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_groups("test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_groups("test-aws_account_id", "test-namespace", )


async def test_list_iam_policy_assignments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_iam_policy_assignments("test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_iam_policy_assignments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_iam_policy_assignments("test-aws_account_id", "test-namespace", )


async def test_list_iam_policy_assignments_for_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_iam_policy_assignments_for_user("test-aws_account_id", "test-user_name", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_iam_policy_assignments_for_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_iam_policy_assignments_for_user("test-aws_account_id", "test-user_name", "test-namespace", )


async def test_list_identity_propagation_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_identity_propagation_configs("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_identity_propagation_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_identity_propagation_configs("test-aws_account_id", )


async def test_list_ingestions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ingestions("test-data_set_id", "test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_ingestions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ingestions("test-data_set_id", "test-aws_account_id", )


async def test_list_namespaces(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_namespaces("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_namespaces_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_namespaces("test-aws_account_id", )


async def test_list_refresh_schedules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_refresh_schedules("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_list_refresh_schedules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_refresh_schedules("test-aws_account_id", "test-data_set_id", )


async def test_list_role_memberships(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_role_memberships("test-role", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_role_memberships_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_role_memberships("test-role", "test-aws_account_id", "test-namespace", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_template_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_template_aliases("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_list_template_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_template_aliases("test-aws_account_id", "test-template_id", )


async def test_list_template_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_template_versions("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_list_template_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_template_versions("test-aws_account_id", "test-template_id", )


async def test_list_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_templates("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_templates("test-aws_account_id", )


async def test_list_theme_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_theme_aliases("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_list_theme_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_theme_aliases("test-aws_account_id", "test-theme_id", )


async def test_list_theme_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_theme_versions("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_list_theme_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_theme_versions("test-aws_account_id", "test-theme_id", )


async def test_list_themes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_themes("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_themes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_themes("test-aws_account_id", )


async def test_list_topic_refresh_schedules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_topic_refresh_schedules("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_list_topic_refresh_schedules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_topic_refresh_schedules("test-aws_account_id", "test-topic_id", )


async def test_list_topic_reviewed_answers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_topic_reviewed_answers("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_list_topic_reviewed_answers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_topic_reviewed_answers("test-aws_account_id", "test-topic_id", )


async def test_list_topics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_topics("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_topics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_topics("test-aws_account_id", )


async def test_list_user_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_user_groups("test-user_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_list_user_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_groups("test-user_name", "test-aws_account_id", "test-namespace", )


async def test_list_vpc_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vpc_connections("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_list_vpc_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_connections("test-aws_account_id", )


async def test_predict_qa_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await predict_qa_results("test-aws_account_id", "test-query_text", )
    mock_client.call.assert_called_once()


async def test_predict_qa_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await predict_qa_results("test-aws_account_id", "test-query_text", )


async def test_put_data_set_refresh_properties(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_data_set_refresh_properties_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", {}, )


async def test_restore_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_analysis("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_restore_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_analysis("test-aws_account_id", "test-analysis_id", )


async def test_search_action_connectors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_action_connectors("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_action_connectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_action_connectors("test-aws_account_id", [], )


async def test_search_analyses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_analyses("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_analyses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_analyses("test-aws_account_id", [], )


async def test_search_dashboards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_dashboards("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_dashboards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_dashboards("test-aws_account_id", [], )


async def test_search_data_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_data_sets("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_data_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_data_sets("test-aws_account_id", [], )


async def test_search_data_sources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_data_sources("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_data_sources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_data_sources("test-aws_account_id", [], )


async def test_search_flows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_flows("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_flows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_flows("test-aws_account_id", [], )


async def test_search_folders(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_folders("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_folders_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_folders("test-aws_account_id", [], )


async def test_search_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_groups("test-aws_account_id", "test-namespace", [], )
    mock_client.call.assert_called_once()


async def test_search_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_groups("test-aws_account_id", "test-namespace", [], )


async def test_search_topics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_topics("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_search_topics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_topics("test-aws_account_id", [], )


async def test_start_asset_bundle_export_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", [], "test-export_format", )
    mock_client.call.assert_called_once()


async def test_start_asset_bundle_export_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", [], "test-export_format", )


async def test_start_asset_bundle_import_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_asset_bundle_import_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", {}, )


async def test_start_dashboard_snapshot_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", {}, {}, )
    mock_client.call.assert_called_once()


async def test_start_dashboard_snapshot_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", {}, {}, )


async def test_start_dashboard_snapshot_job_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_dashboard_snapshot_job_schedule("test-aws_account_id", "test-dashboard_id", "test-schedule_id", )
    mock_client.call.assert_called_once()


async def test_start_dashboard_snapshot_job_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_dashboard_snapshot_job_schedule("test-aws_account_id", "test-dashboard_id", "test-schedule_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_account_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_custom_permission("test-custom_permissions_name", "test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_update_account_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_custom_permission("test-custom_permissions_name", "test-aws_account_id", )


async def test_update_account_customization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_customization("test-aws_account_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_account_customization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_customization("test-aws_account_id", {}, )


async def test_update_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_settings("test-aws_account_id", "test-default_namespace", )
    mock_client.call.assert_called_once()


async def test_update_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_settings("test-aws_account_id", "test-default_namespace", )


async def test_update_action_connector(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", {}, )
    mock_client.call.assert_called_once()


async def test_update_action_connector_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", {}, )


async def test_update_action_connector_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_action_connector_permissions("test-aws_account_id", "test-action_connector_id", )
    mock_client.call.assert_called_once()


async def test_update_action_connector_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_action_connector_permissions("test-aws_account_id", "test-action_connector_id", )


async def test_update_analysis(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_analysis("test-aws_account_id", "test-analysis_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_analysis_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_analysis("test-aws_account_id", "test-analysis_id", "test-name", )


async def test_update_analysis_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_analysis_permissions("test-aws_account_id", "test-analysis_id", )
    mock_client.call.assert_called_once()


async def test_update_analysis_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_analysis_permissions("test-aws_account_id", "test-analysis_id", )


async def test_update_application_with_token_exchange_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application_with_token_exchange_grant("test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_update_application_with_token_exchange_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application_with_token_exchange_grant("test-aws_account_id", "test-namespace", )


async def test_update_brand(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_brand("test-aws_account_id", "test-brand_id", )
    mock_client.call.assert_called_once()


async def test_update_brand_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_brand("test-aws_account_id", "test-brand_id", )


async def test_update_brand_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_brand_assignment("test-aws_account_id", "test-brand_arn", )
    mock_client.call.assert_called_once()


async def test_update_brand_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_brand_assignment("test-aws_account_id", "test-brand_arn", )


async def test_update_brand_published_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_brand_published_version("test-aws_account_id", "test-brand_id", "test-version_id", )
    mock_client.call.assert_called_once()


async def test_update_brand_published_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_brand_published_version("test-aws_account_id", "test-brand_id", "test-version_id", )


async def test_update_custom_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )
    mock_client.call.assert_called_once()


async def test_update_custom_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_permissions("test-aws_account_id", "test-custom_permissions_name", )


async def test_update_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard("test-aws_account_id", "test-dashboard_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard("test-aws_account_id", "test-dashboard_id", "test-name", )


async def test_update_dashboard_links(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard_links("test-aws_account_id", "test-dashboard_id", [], )
    mock_client.call.assert_called_once()


async def test_update_dashboard_links_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard_links("test-aws_account_id", "test-dashboard_id", [], )


async def test_update_dashboard_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard_permissions("test-aws_account_id", "test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_update_dashboard_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard_permissions("test-aws_account_id", "test-dashboard_id", )


async def test_update_dashboard_published_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard_published_version("test-aws_account_id", "test-dashboard_id", 1, )
    mock_client.call.assert_called_once()


async def test_update_dashboard_published_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard_published_version("test-aws_account_id", "test-dashboard_id", 1, )


async def test_update_dashboards_qa_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboards_qa_configuration("test-aws_account_id", "test-dashboards_qa_status", )
    mock_client.call.assert_called_once()


async def test_update_dashboards_qa_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboards_qa_configuration("test-aws_account_id", "test-dashboards_qa_status", )


async def test_update_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", )
    mock_client.call.assert_called_once()


async def test_update_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", )


async def test_update_data_set_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_set_permissions("test-aws_account_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_update_data_set_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_set_permissions("test-aws_account_id", "test-data_set_id", )


async def test_update_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_source("test-aws_account_id", "test-data_source_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_source("test-aws_account_id", "test-data_source_id", "test-name", )


async def test_update_data_source_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_source_permissions("test-aws_account_id", "test-data_source_id", )
    mock_client.call.assert_called_once()


async def test_update_data_source_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_source_permissions("test-aws_account_id", "test-data_source_id", )


async def test_update_default_q_business_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_default_q_business_application("test-aws_account_id", "test-application_id", )
    mock_client.call.assert_called_once()


async def test_update_default_q_business_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_default_q_business_application("test-aws_account_id", "test-application_id", )


async def test_update_flow_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_flow_permissions("test-aws_account_id", "test-flow_id", )
    mock_client.call.assert_called_once()


async def test_update_flow_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_flow_permissions("test-aws_account_id", "test-flow_id", )


async def test_update_folder(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_folder("test-aws_account_id", "test-folder_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_folder_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_folder("test-aws_account_id", "test-folder_id", "test-name", )


async def test_update_folder_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_folder_permissions("test-aws_account_id", "test-folder_id", )
    mock_client.call.assert_called_once()


async def test_update_folder_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_folder_permissions("test-aws_account_id", "test-folder_id", )


async def test_update_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_group("test-group_name", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_update_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_group("test-group_name", "test-aws_account_id", "test-namespace", )


async def test_update_iam_policy_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_update_iam_policy_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", )


async def test_update_identity_propagation_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_identity_propagation_config("test-aws_account_id", "test-service", )
    mock_client.call.assert_called_once()


async def test_update_identity_propagation_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_identity_propagation_config("test-aws_account_id", "test-service", )


async def test_update_ip_restriction(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ip_restriction("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_update_ip_restriction_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ip_restriction("test-aws_account_id", )


async def test_update_key_registration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_key_registration("test-aws_account_id", [], )
    mock_client.call.assert_called_once()


async def test_update_key_registration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_key_registration("test-aws_account_id", [], )


async def test_update_public_sharing_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_public_sharing_settings("test-aws_account_id", )
    mock_client.call.assert_called_once()


async def test_update_public_sharing_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_public_sharing_settings("test-aws_account_id", )


async def test_update_q_personalization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_q_personalization_configuration("test-aws_account_id", "test-personalization_mode", )
    mock_client.call.assert_called_once()


async def test_update_q_personalization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_q_personalization_configuration("test-aws_account_id", "test-personalization_mode", )


async def test_update_quick_sight_q_search_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_quick_sight_q_search_configuration("test-aws_account_id", "test-q_search_status", )
    mock_client.call.assert_called_once()


async def test_update_quick_sight_q_search_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_quick_sight_q_search_configuration("test-aws_account_id", "test-q_search_status", )


async def test_update_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, )


async def test_update_role_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_role_custom_permission("test-custom_permissions_name", "test-role", "test-aws_account_id", "test-namespace", )
    mock_client.call.assert_called_once()


async def test_update_role_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_role_custom_permission("test-custom_permissions_name", "test-role", "test-aws_account_id", "test-namespace", )


async def test_update_spice_capacity_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_spice_capacity_configuration("test-aws_account_id", "test-purchase_mode", )
    mock_client.call.assert_called_once()


async def test_update_spice_capacity_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_spice_capacity_configuration("test-aws_account_id", "test-purchase_mode", )


async def test_update_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_template("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_update_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_template("test-aws_account_id", "test-template_id", )


async def test_update_template_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, )
    mock_client.call.assert_called_once()


async def test_update_template_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, )


async def test_update_template_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_template_permissions("test-aws_account_id", "test-template_id", )
    mock_client.call.assert_called_once()


async def test_update_template_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_template_permissions("test-aws_account_id", "test-template_id", )


async def test_update_theme(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_theme("test-aws_account_id", "test-theme_id", "test-base_theme_id", )
    mock_client.call.assert_called_once()


async def test_update_theme_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_theme("test-aws_account_id", "test-theme_id", "test-base_theme_id", )


async def test_update_theme_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, )
    mock_client.call.assert_called_once()


async def test_update_theme_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, )


async def test_update_theme_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_theme_permissions("test-aws_account_id", "test-theme_id", )
    mock_client.call.assert_called_once()


async def test_update_theme_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_theme_permissions("test-aws_account_id", "test-theme_id", )


async def test_update_topic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_topic("test-aws_account_id", "test-topic_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_topic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_topic("test-aws_account_id", "test-topic_id", {}, )


async def test_update_topic_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_topic_permissions("test-aws_account_id", "test-topic_id", )
    mock_client.call.assert_called_once()


async def test_update_topic_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_topic_permissions("test-aws_account_id", "test-topic_id", )


async def test_update_topic_refresh_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_topic_refresh_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", {}, )


async def test_update_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user("test-user_name", "test-aws_account_id", "test-namespace", "test-email", "test-role", )
    mock_client.call.assert_called_once()


async def test_update_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user("test-user_name", "test-aws_account_id", "test-namespace", "test-email", "test-role", )


async def test_update_user_custom_permission(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", "test-custom_permissions_name", )
    mock_client.call.assert_called_once()


async def test_update_user_custom_permission_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", "test-custom_permissions_name", )


async def test_update_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_update_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.quicksight.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", )


@pytest.mark.asyncio
async def test_create_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_dashboard(1, "test-dashboard_id", "test-name", "test-source_entity", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_dataset
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_dataset(1, "test-dataset_id", "test-name", "test-physical_table_map", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_analysis(1, "test-analysis_id", "test-name", "test-source_entity", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_source_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_data_source
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_data_source(1, "test-data_source_id", "test-name", "test-data_source_type", "test-data_source_parameters", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import register_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await register_user(1, "test-email", "test-identity_type", "test-user_role", iam_arn="test-iam_arn", session_name="test-session_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_delete_topic_reviewed_answer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import batch_delete_topic_reviewed_answer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await batch_delete_topic_reviewed_answer(1, "test-topic_id", answer_ids="test-answer_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_account_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_account_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_account_customization(1, 1, namespace="test-namespace", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_account_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_account_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_account_subscription("test-authentication_method", 1, 1, "test-notification_email", edition="test-edition", active_directory_name="test-active_directory_name", realm="test-realm", directory_id="test-directory_id", admin_group="test-admin_group", author_group="test-author_group", reader_group="test-reader_group", admin_pro_group="test-admin_pro_group", author_pro_group="test-author_pro_group", reader_pro_group="test-reader_pro_group", first_name="test-first_name", last_name="test-last_name", email_address="test-email_address", contact_number="test-contact_number", iam_identity_center_instance_arn="test-iam_identity_center_instance_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_action_connector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_action_connector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_action_connector(1, "test-action_connector_id", "test-name", "test-type_value", {}, description="test-description", permissions="test-permissions", vpc_connection_arn="test-vpc_connection_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_brand_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_brand
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_brand(1, "test-brand_id", brand_definition={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_custom_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_custom_permissions(1, "test-custom_permissions_name", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_data_set(1, "test-data_set_id", "test-name", "test-physical_table_map", 1, logical_table_map="test-logical_table_map", column_groups="test-column_groups", field_folders="test-field_folders", permissions="test-permissions", row_level_permission_data_set="test-row_level_permission_data_set", row_level_permission_tag_configuration={}, column_level_permission_rules="test-column_level_permission_rules", tags=[{"Key": "k", "Value": "v"}], data_set_usage_configuration={}, dataset_parameters="test-dataset_parameters", folder_arns="test-folder_arns", performance_configuration={}, use_as=True, data_prep_configuration={}, semantic_model_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_folder_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_folder
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_folder(1, "test-folder_id", name="test-name", folder_type="test-folder_type", parent_folder_arn="test-parent_folder_arn", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], sharing_model="test-sharing_model", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_group("test-group_name", 1, "test-namespace", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_iam_policy_assignment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_iam_policy_assignment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_iam_policy_assignment(1, "test-assignment_name", "test-assignment_status", "test-namespace", policy_arn="test-policy_arn", identities="test-identities", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ingestion_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_ingestion
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_ingestion("test-data_set_id", "test-ingestion_id", 1, ingestion_type="test-ingestion_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_namespace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_namespace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_namespace(1, "test-namespace", "test-identity_store", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_template(1, "test-template_id", name="test-name", permissions="test-permissions", source_entity="test-source_entity", tags=[{"Key": "k", "Value": "v"}], version_description="test-version_description", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_theme_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_theme
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_theme(1, "test-theme_id", "test-name", "test-base_theme_id", {}, version_description="test-version_description", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_topic_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_topic
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_topic(1, "test-topic_id", "test-topic", tags=[{"Key": "k", "Value": "v"}], folder_arns="test-folder_arns", custom_instructions="test-custom_instructions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_topic_refresh_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_topic_refresh_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_topic_refresh_schedule(1, "test-topic_id", "test-dataset_arn", "test-refresh_schedule", dataset_name="test-dataset_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import create_vpc_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await create_vpc_connection(1, "test-vpc_connection_id", "test-name", "test-subnet_ids", "test-security_group_ids", "test-role_arn", dns_resolvers="test-dns_resolvers", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_account_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import delete_account_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await delete_account_customization(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import delete_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await delete_analysis(1, "test-analysis_id", recovery_window_in_days="test-recovery_window_in_days", force_delete_without_recovery=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import delete_default_q_business_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await delete_default_q_business_application(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import delete_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await delete_template(1, "test-template_id", version_number="test-version_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_theme_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import delete_theme
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await delete_theme(1, "test-theme_id", version_number="test-version_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_account_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_account_customization(1, namespace="test-namespace", resolved="test-resolved", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_brand_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_brand
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_brand(1, "test-brand_id", version_id="test-version_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_dashboard_definition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_dashboard_definition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_dashboard_definition(1, "test-dashboard_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_default_q_business_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_default_q_business_application(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_folder_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_folder_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_folder_permissions(1, "test-folder_id", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_folder_resolved_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_folder_resolved_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_folder_resolved_permissions(1, "test-folder_id", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_key_registration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_key_registration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_key_registration(1, default_key_only="test-default_key_only", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_template(1, "test-template_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_template_definition_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_template_definition
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_template_definition(1, "test-template_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_theme_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import describe_theme
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await describe_theme(1, "test-theme_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_embed_url_for_anonymous_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import generate_embed_url_for_anonymous_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await generate_embed_url_for_anonymous_user(1, "test-namespace", "test-authorized_resource_arns", {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", session_tags=[{"Key": "k", "Value": "v"}], allowed_domains=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_embed_url_for_registered_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import generate_embed_url_for_registered_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await generate_embed_url_for_registered_user(1, "test-user_arn", {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", allowed_domains=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_embed_url_for_registered_user_with_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import generate_embed_url_for_registered_user_with_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await generate_embed_url_for_registered_user_with_identity(1, {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", allowed_domains=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_dashboard_embed_url_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import get_dashboard_embed_url
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await get_dashboard_embed_url(1, "test-dashboard_id", "test-identity_type", session_lifetime_in_minutes="test-session_lifetime_in_minutes", undo_redo_disabled="test-undo_redo_disabled", reset_disabled="test-reset_disabled", state_persistence_enabled="test-state_persistence_enabled", user_arn="test-user_arn", namespace="test-namespace", additional_dashboard_ids="test-additional_dashboard_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_session_embed_url_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import get_session_embed_url
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await get_session_embed_url(1, entry_point="test-entry_point", session_lifetime_in_minutes="test-session_lifetime_in_minutes", user_arn="test-user_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_action_connectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_action_connectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_action_connectors(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_bundle_export_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_asset_bundle_export_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_asset_bundle_export_jobs(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_asset_bundle_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_asset_bundle_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_asset_bundle_import_jobs(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_brands_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_brands
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_brands(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_custom_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_custom_permissions(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dashboard_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_dashboard_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_dashboard_versions(1, "test-dashboard_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_data_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_data_sets(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_flows(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_folder_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_folder_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_folder_members(1, "test-folder_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_folders_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_folders
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_folders(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_folders_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_folders_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_folders_for_resource(1, "test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_group_memberships_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_group_memberships
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_group_memberships("test-group_name", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_groups(1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_iam_policy_assignments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_iam_policy_assignments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_iam_policy_assignments(1, "test-namespace", assignment_status="test-assignment_status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_iam_policy_assignments_for_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_iam_policy_assignments_for_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_iam_policy_assignments_for_user(1, "test-user_name", "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_identity_propagation_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_identity_propagation_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_identity_propagation_configs(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ingestions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_ingestions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_ingestions("test-data_set_id", 1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_namespaces_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_namespaces
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_namespaces(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_role_memberships_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_role_memberships
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_role_memberships("test-role", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_template_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_template_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_template_aliases(1, "test-template_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_template_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_template_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_template_versions(1, "test-template_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_templates(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_theme_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_theme_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_theme_aliases(1, "test-theme_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_theme_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_theme_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_theme_versions(1, "test-theme_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_themes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_themes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_themes(1, next_token="test-next_token", max_results=1, type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_topics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_topics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_topics(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_user_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_user_groups("test-user_name", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import list_vpc_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await list_vpc_connections(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_predict_qa_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import predict_qa_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await predict_qa_results(1, "test-query_text", include_quick_sight_q_index=True, include_generated_answer=True, max_topics_to_consider=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import restore_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await restore_analysis(1, "test-analysis_id", restore_to_folders="test-restore_to_folders", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_action_connectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_action_connectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_action_connectors(1, [{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_analyses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_analyses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_analyses(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_dashboards_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_dashboards
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_dashboards(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_data_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_data_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_data_sets(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_data_sources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_data_sources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_data_sources(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_flows(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_folders_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_folders
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_folders(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_groups(1, "test-namespace", [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_topics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import search_topics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await search_topics(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_asset_bundle_export_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import start_asset_bundle_export_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await start_asset_bundle_export_job(1, 1, "test-resource_arns", 1, include_all_dependencies=True, cloud_formation_override_property_configuration={}, include_permissions=True, include_tags=True, validation_strategy="test-validation_strategy", include_folder_memberships=True, include_folder_members=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_asset_bundle_import_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import start_asset_bundle_import_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await start_asset_bundle_import_job(1, 1, 1, override_parameters="test-override_parameters", failure_action="test-failure_action", override_permissions="test-override_permissions", override_tags=[{"Key": "k", "Value": "v"}], override_validation_strategy="test-override_validation_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_account_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_account_customization(1, 1, namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_account_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_account_settings(1, "test-default_namespace", notification_email="test-notification_email", termination_protection_enabled="test-termination_protection_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_action_connector_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_action_connector
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_action_connector(1, "test-action_connector_id", "test-name", {}, description="test-description", vpc_connection_arn="test-vpc_connection_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_action_connector_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_action_connector_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_action_connector_permissions(1, "test-action_connector_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_analysis_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_analysis
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_analysis(1, "test-analysis_id", "test-name", parameters="test-parameters", source_entity="test-source_entity", theme_arn="test-theme_arn", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_analysis_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_analysis_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_analysis_permissions(1, "test-analysis_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_brand_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_brand
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_brand(1, "test-brand_id", brand_definition={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_custom_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_custom_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_custom_permissions(1, "test-custom_permissions_name", capabilities="test-capabilities", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_dashboard(1, "test-dashboard_id", "test-name", source_entity="test-source_entity", parameters="test-parameters", version_description="test-version_description", dashboard_publish_options={}, theme_arn="test-theme_arn", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dashboard_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_dashboard_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_dashboard_permissions(1, "test-dashboard_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", grant_link_permissions="test-grant_link_permissions", revoke_link_permissions="test-revoke_link_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_data_set(1, "test-data_set_id", "test-name", "test-physical_table_map", 1, logical_table_map="test-logical_table_map", column_groups="test-column_groups", field_folders="test-field_folders", row_level_permission_data_set="test-row_level_permission_data_set", row_level_permission_tag_configuration={}, column_level_permission_rules="test-column_level_permission_rules", data_set_usage_configuration={}, dataset_parameters="test-dataset_parameters", performance_configuration={}, data_prep_configuration={}, semantic_model_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_set_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_data_set_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_data_set_permissions(1, "test-data_set_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_source_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_data_source
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_data_source(1, "test-data_source_id", "test-name", data_source_parameters="test-data_source_parameters", credentials="test-credentials", vpc_connection_properties={}, ssl_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_source_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_data_source_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_data_source_permissions(1, "test-data_source_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_default_q_business_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_default_q_business_application(1, "test-application_id", namespace="test-namespace", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_flow_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_flow_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_flow_permissions(1, "test-flow_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_folder_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_folder_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_folder_permissions(1, "test-folder_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_group("test-group_name", 1, "test-namespace", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_iam_policy_assignment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_iam_policy_assignment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_iam_policy_assignment(1, "test-assignment_name", "test-namespace", assignment_status="test-assignment_status", policy_arn="test-policy_arn", identities="test-identities", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_identity_propagation_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_identity_propagation_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_identity_propagation_config(1, "test-service", authorized_targets="test-authorized_targets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ip_restriction_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_ip_restriction
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_ip_restriction(1, ip_restriction_rule_map="test-ip_restriction_rule_map", vpc_id_restriction_rule_map="test-vpc_id_restriction_rule_map", vpc_endpoint_id_restriction_rule_map="test-vpc_endpoint_id_restriction_rule_map", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_public_sharing_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_public_sharing_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_public_sharing_settings(1, public_sharing_enabled="test-public_sharing_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_template(1, "test-template_id", source_entity="test-source_entity", version_description="test-version_description", name="test-name", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_template_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_template_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_template_permissions(1, "test-template_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_theme_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_theme
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_theme(1, "test-theme_id", "test-base_theme_id", name="test-name", version_description="test-version_description", configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_theme_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_theme_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_theme_permissions(1, "test-theme_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_topic_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_topic
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_topic(1, "test-topic_id", "test-topic", custom_instructions="test-custom_instructions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_topic_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_topic_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_topic_permissions(1, "test-topic_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_user("test-user_name", 1, "test-namespace", "test-email", "test-role", custom_permissions_name="test-custom_permissions_name", unapply_custom_permissions="test-unapply_custom_permissions", external_login_federation_provider_type="test-external_login_federation_provider_type", custom_federation_provider_url="test-custom_federation_provider_url", external_login_id="test-external_login_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_vpc_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.quicksight import update_vpc_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.quicksight.async_client", lambda *a, **kw: mock_client)
    await update_vpc_connection(1, "test-vpc_connection_id", "test-name", "test-subnet_ids", "test-security_group_ids", "test-role_arn", dns_resolvers="test-dns_resolvers", region_name="us-east-1")
    mock_client.call.assert_called_once()
