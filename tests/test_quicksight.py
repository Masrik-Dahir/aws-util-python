"""Tests for aws_util.quicksight module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.quicksight as qs_mod
from aws_util.quicksight import (
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
ACCOUNT_ID = "123456789012"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _make_client_error(code: str, message: str, op: str) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}}, op
    )


def _mock_qs(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    monkeypatch.setattr(qs_mod, "get_client", lambda *a, **kw: mock)
    return mock


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_dashboard_result_model():
    m = DashboardResult(dashboard_id="d-1", name="My Dashboard")
    assert m.dashboard_id == "d-1"
    assert m.name == "My Dashboard"
    assert m.arn is None


def test_dataset_result_model():
    m = DataSetResult(dataset_id="ds-1", name="My DataSet")
    assert m.dataset_id == "ds-1"
    assert m.arn is None


def test_analysis_result_model():
    m = AnalysisResult(analysis_id="a-1", name="My Analysis")
    assert m.analysis_id == "a-1"
    assert m.status is None


def test_data_source_result_model():
    m = DataSourceResult(data_source_id="src-1", name="My Source")
    assert m.data_source_id == "src-1"


def test_quicksight_user_model():
    m = QuickSightUser(user_name="alice", email="alice@example.com", role="ADMIN")
    assert m.user_name == "alice"
    assert m.active is None


# ---------------------------------------------------------------------------
# create_dashboard
# ---------------------------------------------------------------------------


def test_create_dashboard_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_dashboard.return_value = {
        "DashboardId": "d-1",
        "Arn": "arn:aws:quicksight:us-east-1:123:dashboard/d-1",
        "Status": 200,
        "RequestId": "req-1",
    }
    result = create_dashboard(
        ACCOUNT_ID, "d-1", "Test Dashboard",
        {"SourceTemplate": {"Arn": "arn:template"}},
        region_name=REGION,
    )
    assert isinstance(result, DashboardResult)
    assert result.dashboard_id == "d-1"
    assert result.status == 200


def test_create_dashboard_with_permissions_and_tags(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_dashboard.return_value = {
        "DashboardId": "d-1",
        "Arn": "arn:aws:quicksight:us-east-1:123:dashboard/d-1",
        "Status": 200,
    }
    result = create_dashboard(
        ACCOUNT_ID, "d-1", "Test",
        {"SourceTemplate": {"Arn": "arn:template"}},
        permissions=[{"Principal": "arn:user", "Actions": ["View"]}],
        tags=[{"Key": "env", "Value": "test"}],
        region_name=REGION,
    )
    assert result.dashboard_id == "d-1"
    call_kwargs = mock.create_dashboard.call_args[1]
    assert "Permissions" in call_kwargs
    assert "Tags" in call_kwargs


def test_create_dashboard_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_dashboard.side_effect = _make_client_error(
        "InvalidParameterValue", "bad", "CreateDashboard"
    )
    with pytest.raises(RuntimeError, match="Failed to create dashboard"):
        create_dashboard(
            ACCOUNT_ID, "d-1", "Test",
            {"SourceTemplate": {"Arn": "arn:template"}},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# describe_dashboard
# ---------------------------------------------------------------------------


def test_describe_dashboard_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_dashboard.return_value = {
        "Dashboard": {
            "DashboardId": "d-1",
            "Name": "My Dashboard",
            "Arn": "arn:aws:quicksight:us-east-1:123:dashboard/d-1",
        },
        "Status": 200,
        "RequestId": "req-1",
    }
    result = describe_dashboard(ACCOUNT_ID, "d-1", region_name=REGION)
    assert result.name == "My Dashboard"
    assert result.status == 200


def test_describe_dashboard_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_dashboard.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DescribeDashboard"
    )
    with pytest.raises(RuntimeError, match="Failed to describe dashboard"):
        describe_dashboard(ACCOUNT_ID, "d-1", region_name=REGION)


# ---------------------------------------------------------------------------
# list_dashboards
# ---------------------------------------------------------------------------


def test_list_dashboards_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_dashboards.return_value = {
        "DashboardSummaryList": [
            {"DashboardId": "d-1", "Name": "Dash 1", "Arn": "arn:d-1"},
        ],
    }
    result = list_dashboards(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 1
    assert result[0].dashboard_id == "d-1"


def test_list_dashboards_pagination(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_dashboards.side_effect = [
        {
            "DashboardSummaryList": [{"DashboardId": "d-1", "Name": "A"}],
            "NextToken": "tok",
        },
        {
            "DashboardSummaryList": [{"DashboardId": "d-2", "Name": "B"}],
        },
    ]
    result = list_dashboards(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 2


def test_list_dashboards_empty(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_dashboards.return_value = {"DashboardSummaryList": []}
    result = list_dashboards(ACCOUNT_ID, region_name=REGION)
    assert result == []


def test_list_dashboards_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_dashboards.side_effect = _make_client_error(
        "AccessDeniedException", "denied", "ListDashboards"
    )
    with pytest.raises(RuntimeError, match="list_dashboards failed"):
        list_dashboards(ACCOUNT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_dashboard
# ---------------------------------------------------------------------------


def test_delete_dashboard_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_dashboard.return_value = {}
    delete_dashboard(ACCOUNT_ID, "d-1", region_name=REGION)
    mock.delete_dashboard.assert_called_once()


def test_delete_dashboard_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_dashboard.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DeleteDashboard"
    )
    with pytest.raises(RuntimeError, match="Failed to delete dashboard"):
        delete_dashboard(ACCOUNT_ID, "d-1", region_name=REGION)


# ---------------------------------------------------------------------------
# create_dataset
# ---------------------------------------------------------------------------


def test_create_dataset_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_data_set.return_value = {
        "DataSetId": "ds-1",
        "Arn": "arn:aws:quicksight:us-east-1:123:dataset/ds-1",
        "Status": 201,
        "RequestId": "req-ds",
    }
    result = create_dataset(
        ACCOUNT_ID, "ds-1", "Test DataSet",
        {"table1": {"S3Source": {"DataSourceArn": "arn:src"}}},
        region_name=REGION,
    )
    assert isinstance(result, DataSetResult)
    assert result.dataset_id == "ds-1"

def test_create_dataset_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_data_set.side_effect = _make_client_error(
        "ConflictException", "exists", "CreateDataSet"
    )
    with pytest.raises(RuntimeError, match="Failed to create dataset"):
        create_dataset(
            ACCOUNT_ID, "ds-1", "Test",
            {"t": {}},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# describe_dataset
# ---------------------------------------------------------------------------


def test_describe_dataset_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_data_set.return_value = {
        "DataSet": {
            "DataSetId": "ds-1",
            "Name": "My DS",
            "Arn": "arn:ds-1",
        },
        "Status": 200,
        "RequestId": "req-1",
    }
    result = describe_dataset(ACCOUNT_ID, "ds-1", region_name=REGION)
    assert result.name == "My DS"


def test_describe_dataset_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_data_set.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DescribeDataSet"
    )
    with pytest.raises(RuntimeError, match="Failed to describe dataset"):
        describe_dataset(ACCOUNT_ID, "ds-1", region_name=REGION)


# ---------------------------------------------------------------------------
# list_datasets
# ---------------------------------------------------------------------------


def test_list_datasets_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sets.return_value = {
        "DataSetSummaries": [
            {"DataSetId": "ds-1", "Name": "DS 1"},
        ],
    }
    result = list_datasets(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 1


def test_list_datasets_pagination(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sets.side_effect = [
        {
            "DataSetSummaries": [{"DataSetId": "ds-1", "Name": "A"}],
            "NextToken": "tok",
        },
        {
            "DataSetSummaries": [{"DataSetId": "ds-2", "Name": "B"}],
        },
    ]
    result = list_datasets(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 2


def test_list_datasets_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sets.side_effect = _make_client_error(
        "AccessDeniedException", "denied", "ListDataSets"
    )
    with pytest.raises(RuntimeError, match="list_datasets failed"):
        list_datasets(ACCOUNT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# delete_dataset
# ---------------------------------------------------------------------------


def test_delete_dataset_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_data_set.return_value = {}
    delete_dataset(ACCOUNT_ID, "ds-1", region_name=REGION)
    mock.delete_data_set.assert_called_once()


def test_delete_dataset_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_data_set.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DeleteDataSet"
    )
    with pytest.raises(RuntimeError, match="Failed to delete dataset"):
        delete_dataset(ACCOUNT_ID, "ds-1", region_name=REGION)


# ---------------------------------------------------------------------------
# create_analysis
# ---------------------------------------------------------------------------


def test_create_analysis_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_analysis.return_value = {
        "AnalysisId": "a-1",
        "Arn": "arn:aws:quicksight:us-east-1:123:analysis/a-1",
        "Status": 200,
        "RequestId": "req-a",
    }
    result = create_analysis(
        ACCOUNT_ID, "a-1", "Test Analysis",
        {"SourceTemplate": {"Arn": "arn:template"}},
        region_name=REGION,
    )
    assert isinstance(result, AnalysisResult)
    assert result.analysis_id == "a-1"

def test_create_analysis_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_analysis.side_effect = _make_client_error(
        "ConflictException", "exists", "CreateAnalysis"
    )
    with pytest.raises(RuntimeError, match="Failed to create analysis"):
        create_analysis(
            ACCOUNT_ID, "a-1", "Test",
            {"SourceTemplate": {"Arn": "arn:template"}},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# list_analyses
# ---------------------------------------------------------------------------


def test_list_analyses_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_analyses.return_value = {
        "AnalysisSummaryList": [
            {"AnalysisId": "a-1", "Name": "Analysis 1"},
        ],
    }
    result = list_analyses(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 1


def test_list_analyses_pagination(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_analyses.side_effect = [
        {
            "AnalysisSummaryList": [{"AnalysisId": "a-1", "Name": "A"}],
            "NextToken": "tok",
        },
        {
            "AnalysisSummaryList": [{"AnalysisId": "a-2", "Name": "B"}],
        },
    ]
    result = list_analyses(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 2


def test_list_analyses_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_analyses.side_effect = _make_client_error(
        "AccessDeniedException", "denied", "ListAnalyses"
    )
    with pytest.raises(RuntimeError, match="list_analyses failed"):
        list_analyses(ACCOUNT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# create_data_source
# ---------------------------------------------------------------------------


def test_create_data_source_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_data_source.return_value = {
        "DataSourceId": "src-1",
        "Arn": "arn:aws:quicksight:us-east-1:123:datasource/src-1",
        "Status": 201,
        "RequestId": "req-src",
    }
    result = create_data_source(
        ACCOUNT_ID, "src-1", "Test Source", "ATHENA",
        {"AthenaParameters": {"WorkGroup": "primary"}},
        region_name=REGION,
    )
    assert isinstance(result, DataSourceResult)
    assert result.data_source_id == "src-1"

def test_create_data_source_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.create_data_source.side_effect = _make_client_error(
        "ConflictException", "exists", "CreateDataSource"
    )
    with pytest.raises(RuntimeError, match="Failed to create data source"):
        create_data_source(
            ACCOUNT_ID, "src-1", "Test", "ATHENA",
            {"AthenaParameters": {"WorkGroup": "primary"}},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# list_data_sources
# ---------------------------------------------------------------------------


def test_list_data_sources_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sources.return_value = {
        "DataSources": [
            {"DataSourceId": "src-1", "Name": "Source 1"},
        ],
    }
    result = list_data_sources(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 1


def test_list_data_sources_pagination(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sources.side_effect = [
        {
            "DataSources": [{"DataSourceId": "src-1", "Name": "A"}],
            "NextToken": "tok",
        },
        {
            "DataSources": [{"DataSourceId": "src-2", "Name": "B"}],
        },
    ]
    result = list_data_sources(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 2


def test_list_data_sources_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_data_sources.side_effect = _make_client_error(
        "AccessDeniedException", "denied", "ListDataSources"
    )
    with pytest.raises(RuntimeError, match="list_data_sources failed"):
        list_data_sources(ACCOUNT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# describe_user
# ---------------------------------------------------------------------------


def test_describe_user_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_user.return_value = {
        "User": {
            "UserName": "alice",
            "Email": "alice@example.com",
            "Role": "ADMIN",
            "Arn": "arn:user/alice",
            "IdentityType": "QUICKSIGHT",
            "Active": True,
            "PrincipalId": "pid-1",
        },
    }
    result = describe_user(ACCOUNT_ID, "alice", region_name=REGION)
    assert result.user_name == "alice"
    assert result.email == "alice@example.com"
    assert result.role == "ADMIN"
    assert result.active is True


def test_describe_user_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.describe_user.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DescribeUser"
    )
    with pytest.raises(RuntimeError, match="Failed to describe user"):
        describe_user(ACCOUNT_ID, "alice", region_name=REGION)


# ---------------------------------------------------------------------------
# list_users
# ---------------------------------------------------------------------------


def test_list_users_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_users.return_value = {
        "UserList": [
            {
                "UserName": "alice",
                "Email": "alice@example.com",
                "Role": "ADMIN",
            },
        ],
    }
    result = list_users(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 1
    assert result[0].user_name == "alice"


def test_list_users_pagination(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_users.side_effect = [
        {
            "UserList": [{"UserName": "alice", "Role": "ADMIN"}],
            "NextToken": "tok",
        },
        {
            "UserList": [{"UserName": "bob", "Role": "READER"}],
        },
    ]
    result = list_users(ACCOUNT_ID, region_name=REGION)
    assert len(result) == 2


def test_list_users_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.list_users.side_effect = _make_client_error(
        "AccessDeniedException", "denied", "ListUsers"
    )
    with pytest.raises(RuntimeError, match="list_users failed"):
        list_users(ACCOUNT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# register_user
# ---------------------------------------------------------------------------


def test_register_user_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.register_user.return_value = {
        "User": {
            "UserName": "alice",
            "Email": "alice@example.com",
            "Role": "AUTHOR",
            "Arn": "arn:user/alice",
            "IdentityType": "QUICKSIGHT",
            "Active": True,
            "PrincipalId": "pid-1",
        },
    }
    result = register_user(
        ACCOUNT_ID, "alice@example.com", "QUICKSIGHT", "AUTHOR",
        region_name=REGION,
    )
    assert isinstance(result, QuickSightUser)
    assert result.email == "alice@example.com"


def test_register_user_with_iam(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.register_user.return_value = {
        "User": {
            "UserName": "iam-user",
            "Email": "iam@example.com",
            "Role": "ADMIN",
            "IdentityType": "IAM",
        },
    }
    register_user(
        ACCOUNT_ID, "iam@example.com", "IAM", "ADMIN",
        iam_arn="arn:aws:iam::123:user/iam-user",
        session_name="my-session",
        region_name=REGION,
    )
    call_kwargs = mock.register_user.call_args[1]
    assert call_kwargs["IamArn"] == "arn:aws:iam::123:user/iam-user"
    assert call_kwargs["SessionName"] == "my-session"


def test_register_user_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.register_user.side_effect = _make_client_error(
        "ConflictException", "exists", "RegisterUser"
    )
    with pytest.raises(RuntimeError, match="Failed to register user"):
        register_user(
            ACCOUNT_ID, "alice@example.com", "QUICKSIGHT", "AUTHOR",
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# delete_user
# ---------------------------------------------------------------------------


def test_delete_user_success(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_user.return_value = {}
    delete_user(ACCOUNT_ID, "alice", region_name=REGION)
    mock.delete_user.assert_called_once()


def test_delete_user_error(monkeypatch):
    mock = _mock_qs(monkeypatch)
    mock.delete_user.side_effect = _make_client_error(
        "ResourceNotFoundException", "not found", "DeleteUser"
    )
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        delete_user(ACCOUNT_ID, "alice", region_name=REGION)


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    assert "DashboardResult" in qs_mod.__all__
    assert "DataSetResult" in qs_mod.__all__
    assert "AnalysisResult" in qs_mod.__all__
    assert "DataSourceResult" in qs_mod.__all__
    assert "QuickSightUser" in qs_mod.__all__
    assert "create_dashboard" in qs_mod.__all__
    assert "list_users" in qs_mod.__all__
    assert "register_user" in qs_mod.__all__


def test_batch_create_topic_reviewed_answer(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_create_topic_reviewed_answer.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    batch_create_topic_reviewed_answer("test-aws_account_id", "test-topic_id", [], region_name=REGION)
    mock_client.batch_create_topic_reviewed_answer.assert_called_once()


def test_batch_create_topic_reviewed_answer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_create_topic_reviewed_answer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_create_topic_reviewed_answer",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch create topic reviewed answer"):
        batch_create_topic_reviewed_answer("test-aws_account_id", "test-topic_id", [], region_name=REGION)


def test_batch_delete_topic_reviewed_answer(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_topic_reviewed_answer.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    batch_delete_topic_reviewed_answer("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.batch_delete_topic_reviewed_answer.assert_called_once()


def test_batch_delete_topic_reviewed_answer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_topic_reviewed_answer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_topic_reviewed_answer",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete topic reviewed answer"):
        batch_delete_topic_reviewed_answer("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_cancel_ingestion(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    cancel_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", region_name=REGION)
    mock_client.cancel_ingestion.assert_called_once()


def test_cancel_ingestion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_ingestion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_ingestion",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel ingestion"):
        cancel_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", region_name=REGION)


def test_create_account_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_account_customization("test-aws_account_id", {}, region_name=REGION)
    mock_client.create_account_customization.assert_called_once()


def test_create_account_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_account_customization",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create account customization"):
        create_account_customization("test-aws_account_id", {}, region_name=REGION)


def test_create_account_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_subscription.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_account_subscription("test-authentication_method", "test-aws_account_id", "test-account_name", "test-notification_email", region_name=REGION)
    mock_client.create_account_subscription.assert_called_once()


def test_create_account_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_account_subscription",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create account subscription"):
        create_account_subscription("test-authentication_method", "test-aws_account_id", "test-account_name", "test-notification_email", region_name=REGION)


def test_create_action_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", "test-type_value", {}, region_name=REGION)
    mock_client.create_action_connector.assert_called_once()


def test_create_action_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_action_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_action_connector",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create action connector"):
        create_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", "test-type_value", {}, region_name=REGION)


def test_create_brand(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_brand("test-aws_account_id", "test-brand_id", region_name=REGION)
    mock_client.create_brand.assert_called_once()


def test_create_brand_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_brand.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_brand",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create brand"):
        create_brand("test-aws_account_id", "test-brand_id", region_name=REGION)


def test_create_custom_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)
    mock_client.create_custom_permissions.assert_called_once()


def test_create_custom_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom permissions"):
        create_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)


def test_create_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", region_name=REGION)
    mock_client.create_data_set.assert_called_once()


def test_create_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_set",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create data set"):
        create_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", region_name=REGION)


def test_create_folder(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_folder.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_folder("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.create_folder.assert_called_once()


def test_create_folder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_folder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_folder",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create folder"):
        create_folder("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_create_folder_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_folder_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", region_name=REGION)
    mock_client.create_folder_membership.assert_called_once()


def test_create_folder_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_folder_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_folder_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create folder membership"):
        create_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", region_name=REGION)


def test_create_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.create_group.assert_called_once()


def test_create_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_group",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create group"):
        create_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_create_group_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.create_group_membership.assert_called_once()


def test_create_group_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_group_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create group membership"):
        create_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_create_iam_policy_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-assignment_status", "test-namespace", region_name=REGION)
    mock_client.create_iam_policy_assignment.assert_called_once()


def test_create_iam_policy_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_iam_policy_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_iam_policy_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create iam policy assignment"):
        create_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-assignment_status", "test-namespace", region_name=REGION)


def test_create_ingestion(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_ingestion("test-data_set_id", "test-ingestion_id", "test-aws_account_id", region_name=REGION)
    mock_client.create_ingestion.assert_called_once()


def test_create_ingestion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ingestion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ingestion",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ingestion"):
        create_ingestion("test-data_set_id", "test-ingestion_id", "test-aws_account_id", region_name=REGION)


def test_create_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_namespace.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_namespace("test-aws_account_id", "test-namespace", "test-identity_store", region_name=REGION)
    mock_client.create_namespace.assert_called_once()


def test_create_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_namespace",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create namespace"):
        create_namespace("test-aws_account_id", "test-namespace", "test-identity_store", region_name=REGION)


def test_create_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, region_name=REGION)
    mock_client.create_refresh_schedule.assert_called_once()


def test_create_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create refresh schedule"):
        create_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, region_name=REGION)


def test_create_role_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_role_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_role_membership("test-member_name", "test-aws_account_id", "test-namespace", "test-role", region_name=REGION)
    mock_client.create_role_membership.assert_called_once()


def test_create_role_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_role_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_role_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create role membership"):
        create_role_membership("test-member_name", "test-aws_account_id", "test-namespace", "test-role", region_name=REGION)


def test_create_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_template("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.create_template.assert_called_once()


def test_create_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_template",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create template"):
        create_template("test-aws_account_id", "test-template_id", region_name=REGION)


def test_create_template_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, region_name=REGION)
    mock_client.create_template_alias.assert_called_once()


def test_create_template_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_template_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_template_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create template alias"):
        create_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, region_name=REGION)


def test_create_theme(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_theme("test-aws_account_id", "test-theme_id", "test-name", "test-base_theme_id", {}, region_name=REGION)
    mock_client.create_theme.assert_called_once()


def test_create_theme_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_theme.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_theme",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create theme"):
        create_theme("test-aws_account_id", "test-theme_id", "test-name", "test-base_theme_id", {}, region_name=REGION)


def test_create_theme_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_theme_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, region_name=REGION)
    mock_client.create_theme_alias.assert_called_once()


def test_create_theme_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_theme_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_theme_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create theme alias"):
        create_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, region_name=REGION)


def test_create_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_topic("test-aws_account_id", "test-topic_id", {}, region_name=REGION)
    mock_client.create_topic.assert_called_once()


def test_create_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_topic",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create topic"):
        create_topic("test-aws_account_id", "test-topic_id", {}, region_name=REGION)


def test_create_topic_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_arn", {}, region_name=REGION)
    mock_client.create_topic_refresh_schedule.assert_called_once()


def test_create_topic_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_topic_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_topic_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create topic refresh schedule"):
        create_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_arn", {}, region_name=REGION)


def test_create_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", region_name=REGION)
    mock_client.create_vpc_connection.assert_called_once()


def test_create_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_connection",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc connection"):
        create_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", region_name=REGION)


def test_delete_account_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_account_custom_permission("test-aws_account_id", region_name=REGION)
    mock_client.delete_account_custom_permission.assert_called_once()


def test_delete_account_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account custom permission"):
        delete_account_custom_permission("test-aws_account_id", region_name=REGION)


def test_delete_account_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_account_customization("test-aws_account_id", region_name=REGION)
    mock_client.delete_account_customization.assert_called_once()


def test_delete_account_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_customization",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account customization"):
        delete_account_customization("test-aws_account_id", region_name=REGION)


def test_delete_account_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_subscription.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_account_subscription("test-aws_account_id", region_name=REGION)
    mock_client.delete_account_subscription.assert_called_once()


def test_delete_account_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_subscription",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account subscription"):
        delete_account_subscription("test-aws_account_id", region_name=REGION)


def test_delete_action_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_action_connector("test-aws_account_id", "test-action_connector_id", region_name=REGION)
    mock_client.delete_action_connector.assert_called_once()


def test_delete_action_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_action_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_action_connector",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete action connector"):
        delete_action_connector("test-aws_account_id", "test-action_connector_id", region_name=REGION)


def test_delete_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.delete_analysis.assert_called_once()


def test_delete_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_analysis",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete analysis"):
        delete_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_delete_brand(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_brand("test-aws_account_id", "test-brand_id", region_name=REGION)
    mock_client.delete_brand.assert_called_once()


def test_delete_brand_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_brand.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_brand",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete brand"):
        delete_brand("test-aws_account_id", "test-brand_id", region_name=REGION)


def test_delete_brand_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_brand_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_brand_assignment("test-aws_account_id", region_name=REGION)
    mock_client.delete_brand_assignment.assert_called_once()


def test_delete_brand_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_brand_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_brand_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete brand assignment"):
        delete_brand_assignment("test-aws_account_id", region_name=REGION)


def test_delete_custom_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)
    mock_client.delete_custom_permissions.assert_called_once()


def test_delete_custom_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom permissions"):
        delete_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)


def test_delete_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_data_set("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.delete_data_set.assert_called_once()


def test_delete_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_set",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data set"):
        delete_data_set("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_delete_data_set_refresh_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_set_refresh_properties.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.delete_data_set_refresh_properties.assert_called_once()


def test_delete_data_set_refresh_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_set_refresh_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_set_refresh_properties",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data set refresh properties"):
        delete_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_delete_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_source.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_data_source("test-aws_account_id", "test-data_source_id", region_name=REGION)
    mock_client.delete_data_source.assert_called_once()


def test_delete_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_source",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data source"):
        delete_data_source("test-aws_account_id", "test-data_source_id", region_name=REGION)


def test_delete_default_q_business_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_default_q_business_application("test-aws_account_id", region_name=REGION)
    mock_client.delete_default_q_business_application.assert_called_once()


def test_delete_default_q_business_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_default_q_business_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_default_q_business_application",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete default q business application"):
        delete_default_q_business_application("test-aws_account_id", region_name=REGION)


def test_delete_folder(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_folder.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_folder("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.delete_folder.assert_called_once()


def test_delete_folder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_folder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_folder",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete folder"):
        delete_folder("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_delete_folder_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_folder_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", region_name=REGION)
    mock_client.delete_folder_membership.assert_called_once()


def test_delete_folder_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_folder_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_folder_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete folder membership"):
        delete_folder_membership("test-aws_account_id", "test-folder_id", "test-member_id", "test-member_type", region_name=REGION)


def test_delete_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_group.assert_called_once()


def test_delete_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_group",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete group"):
        delete_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_group_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_group_membership.assert_called_once()


def test_delete_group_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_group_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete group membership"):
        delete_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_iam_policy_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)
    mock_client.delete_iam_policy_assignment.assert_called_once()


def test_delete_iam_policy_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_iam_policy_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_iam_policy_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete iam policy assignment"):
        delete_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)


def test_delete_identity_propagation_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_propagation_config.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_identity_propagation_config("test-aws_account_id", "test-service", region_name=REGION)
    mock_client.delete_identity_propagation_config.assert_called_once()


def test_delete_identity_propagation_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_propagation_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_identity_propagation_config",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete identity propagation config"):
        delete_identity_propagation_config("test-aws_account_id", "test-service", region_name=REGION)


def test_delete_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_namespace.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_namespace("test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_namespace.assert_called_once()


def test_delete_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_namespace",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete namespace"):
        delete_namespace("test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_refresh_schedule("test-data_set_id", "test-aws_account_id", "test-schedule_id", region_name=REGION)
    mock_client.delete_refresh_schedule.assert_called_once()


def test_delete_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete refresh schedule"):
        delete_refresh_schedule("test-data_set_id", "test-aws_account_id", "test-schedule_id", region_name=REGION)


def test_delete_role_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_role_custom_permission.assert_called_once()


def test_delete_role_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_role_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete role custom permission"):
        delete_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_role_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_role_membership("test-member_name", "test-role", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_role_membership.assert_called_once()


def test_delete_role_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_role_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete role membership"):
        delete_role_membership("test-member_name", "test-role", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_template("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.delete_template.assert_called_once()


def test_delete_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_template",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete template"):
        delete_template("test-aws_account_id", "test-template_id", region_name=REGION)


def test_delete_template_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", region_name=REGION)
    mock_client.delete_template_alias.assert_called_once()


def test_delete_template_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_template_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_template_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete template alias"):
        delete_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", region_name=REGION)


def test_delete_theme(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_theme("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.delete_theme.assert_called_once()


def test_delete_theme_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_theme.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_theme",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete theme"):
        delete_theme("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_delete_theme_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_theme_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", region_name=REGION)
    mock_client.delete_theme_alias.assert_called_once()


def test_delete_theme_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_theme_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_theme_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete theme alias"):
        delete_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", region_name=REGION)


def test_delete_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_topic("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.delete_topic.assert_called_once()


def test_delete_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_topic",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete topic"):
        delete_topic("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_delete_topic_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", region_name=REGION)
    mock_client.delete_topic_refresh_schedule.assert_called_once()


def test_delete_topic_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_topic_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_topic_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete topic refresh schedule"):
        delete_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", region_name=REGION)


def test_delete_user_by_principal_id(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_by_principal_id.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_user_by_principal_id("test-principal_id", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_user_by_principal_id.assert_called_once()


def test_delete_user_by_principal_id_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_by_principal_id.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_by_principal_id",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user by principal id"):
        delete_user_by_principal_id("test-principal_id", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_user_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.delete_user_custom_permission.assert_called_once()


def test_delete_user_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user custom permission"):
        delete_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_delete_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_vpc_connection("test-aws_account_id", "test-vpc_connection_id", region_name=REGION)
    mock_client.delete_vpc_connection.assert_called_once()


def test_delete_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_connection",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc connection"):
        delete_vpc_connection("test-aws_account_id", "test-vpc_connection_id", region_name=REGION)


def test_describe_account_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_account_custom_permission("test-aws_account_id", region_name=REGION)
    mock_client.describe_account_custom_permission.assert_called_once()


def test_describe_account_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account custom permission"):
        describe_account_custom_permission("test-aws_account_id", region_name=REGION)


def test_describe_account_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_account_customization("test-aws_account_id", region_name=REGION)
    mock_client.describe_account_customization.assert_called_once()


def test_describe_account_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_customization",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account customization"):
        describe_account_customization("test-aws_account_id", region_name=REGION)


def test_describe_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_account_settings("test-aws_account_id", region_name=REGION)
    mock_client.describe_account_settings.assert_called_once()


def test_describe_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_settings",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account settings"):
        describe_account_settings("test-aws_account_id", region_name=REGION)


def test_describe_account_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_subscription.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_account_subscription("test-aws_account_id", region_name=REGION)
    mock_client.describe_account_subscription.assert_called_once()


def test_describe_account_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_subscription",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account subscription"):
        describe_account_subscription("test-aws_account_id", region_name=REGION)


def test_describe_action_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_action_connector("test-aws_account_id", "test-action_connector_id", region_name=REGION)
    mock_client.describe_action_connector.assert_called_once()


def test_describe_action_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_action_connector",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe action connector"):
        describe_action_connector("test-aws_account_id", "test-action_connector_id", region_name=REGION)


def test_describe_action_connector_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_connector_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_action_connector_permissions("test-aws_account_id", "test-action_connector_id", region_name=REGION)
    mock_client.describe_action_connector_permissions.assert_called_once()


def test_describe_action_connector_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_connector_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_action_connector_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe action connector permissions"):
        describe_action_connector_permissions("test-aws_account_id", "test-action_connector_id", region_name=REGION)


def test_describe_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.describe_analysis.assert_called_once()


def test_describe_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_analysis",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe analysis"):
        describe_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_describe_analysis_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis_definition.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_analysis_definition("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.describe_analysis_definition.assert_called_once()


def test_describe_analysis_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_analysis_definition",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe analysis definition"):
        describe_analysis_definition("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_describe_analysis_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_analysis_permissions("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.describe_analysis_permissions.assert_called_once()


def test_describe_analysis_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_analysis_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_analysis_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe analysis permissions"):
        describe_analysis_permissions("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_describe_asset_bundle_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_asset_bundle_export_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", region_name=REGION)
    mock_client.describe_asset_bundle_export_job.assert_called_once()


def test_describe_asset_bundle_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_asset_bundle_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_bundle_export_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe asset bundle export job"):
        describe_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", region_name=REGION)


def test_describe_asset_bundle_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_asset_bundle_import_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", region_name=REGION)
    mock_client.describe_asset_bundle_import_job.assert_called_once()


def test_describe_asset_bundle_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_asset_bundle_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_asset_bundle_import_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe asset bundle import job"):
        describe_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", region_name=REGION)


def test_describe_brand(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_brand("test-aws_account_id", "test-brand_id", region_name=REGION)
    mock_client.describe_brand.assert_called_once()


def test_describe_brand_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_brand",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe brand"):
        describe_brand("test-aws_account_id", "test-brand_id", region_name=REGION)


def test_describe_brand_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_brand_assignment("test-aws_account_id", region_name=REGION)
    mock_client.describe_brand_assignment.assert_called_once()


def test_describe_brand_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_brand_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe brand assignment"):
        describe_brand_assignment("test-aws_account_id", region_name=REGION)


def test_describe_brand_published_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand_published_version.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_brand_published_version("test-aws_account_id", "test-brand_id", region_name=REGION)
    mock_client.describe_brand_published_version.assert_called_once()


def test_describe_brand_published_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_brand_published_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_brand_published_version",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe brand published version"):
        describe_brand_published_version("test-aws_account_id", "test-brand_id", region_name=REGION)


def test_describe_custom_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)
    mock_client.describe_custom_permissions.assert_called_once()


def test_describe_custom_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe custom permissions"):
        describe_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)


def test_describe_dashboard_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_definition.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboard_definition("test-aws_account_id", "test-dashboard_id", region_name=REGION)
    mock_client.describe_dashboard_definition.assert_called_once()


def test_describe_dashboard_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboard_definition",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dashboard definition"):
        describe_dashboard_definition("test-aws_account_id", "test-dashboard_id", region_name=REGION)


def test_describe_dashboard_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboard_permissions("test-aws_account_id", "test-dashboard_id", region_name=REGION)
    mock_client.describe_dashboard_permissions.assert_called_once()


def test_describe_dashboard_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboard_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dashboard permissions"):
        describe_dashboard_permissions("test-aws_account_id", "test-dashboard_id", region_name=REGION)


def test_describe_dashboard_snapshot_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_snapshot_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", region_name=REGION)
    mock_client.describe_dashboard_snapshot_job.assert_called_once()


def test_describe_dashboard_snapshot_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_snapshot_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboard_snapshot_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dashboard snapshot job"):
        describe_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", region_name=REGION)


def test_describe_dashboard_snapshot_job_result(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_snapshot_job_result.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboard_snapshot_job_result("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", region_name=REGION)
    mock_client.describe_dashboard_snapshot_job_result.assert_called_once()


def test_describe_dashboard_snapshot_job_result_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboard_snapshot_job_result.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboard_snapshot_job_result",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dashboard snapshot job result"):
        describe_dashboard_snapshot_job_result("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", region_name=REGION)


def test_describe_dashboards_qa_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboards_qa_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboards_qa_configuration("test-aws_account_id", region_name=REGION)
    mock_client.describe_dashboards_qa_configuration.assert_called_once()


def test_describe_dashboards_qa_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_dashboards_qa_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dashboards_qa_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe dashboards qa configuration"):
        describe_dashboards_qa_configuration("test-aws_account_id", region_name=REGION)


def test_describe_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_data_set("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.describe_data_set.assert_called_once()


def test_describe_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_set",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data set"):
        describe_data_set("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_describe_data_set_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_data_set_permissions("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.describe_data_set_permissions.assert_called_once()


def test_describe_data_set_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_set_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data set permissions"):
        describe_data_set_permissions("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_describe_data_set_refresh_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set_refresh_properties.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.describe_data_set_refresh_properties.assert_called_once()


def test_describe_data_set_refresh_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_set_refresh_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_set_refresh_properties",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data set refresh properties"):
        describe_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_describe_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_source.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_data_source("test-aws_account_id", "test-data_source_id", region_name=REGION)
    mock_client.describe_data_source.assert_called_once()


def test_describe_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_source",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data source"):
        describe_data_source("test-aws_account_id", "test-data_source_id", region_name=REGION)


def test_describe_data_source_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_source_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_data_source_permissions("test-aws_account_id", "test-data_source_id", region_name=REGION)
    mock_client.describe_data_source_permissions.assert_called_once()


def test_describe_data_source_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_source_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_source_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data source permissions"):
        describe_data_source_permissions("test-aws_account_id", "test-data_source_id", region_name=REGION)


def test_describe_default_q_business_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_default_q_business_application("test-aws_account_id", region_name=REGION)
    mock_client.describe_default_q_business_application.assert_called_once()


def test_describe_default_q_business_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_default_q_business_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_default_q_business_application",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe default q business application"):
        describe_default_q_business_application("test-aws_account_id", region_name=REGION)


def test_describe_folder(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_folder("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.describe_folder.assert_called_once()


def test_describe_folder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_folder",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe folder"):
        describe_folder("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_describe_folder_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_folder_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.describe_folder_permissions.assert_called_once()


def test_describe_folder_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_folder_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe folder permissions"):
        describe_folder_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_describe_folder_resolved_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder_resolved_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_folder_resolved_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.describe_folder_resolved_permissions.assert_called_once()


def test_describe_folder_resolved_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_folder_resolved_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_folder_resolved_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe folder resolved permissions"):
        describe_folder_resolved_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_describe_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.describe_group.assert_called_once()


def test_describe_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_group",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe group"):
        describe_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_describe_group_membership(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_group_membership.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.describe_group_membership.assert_called_once()


def test_describe_group_membership_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_group_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_group_membership",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe group membership"):
        describe_group_membership("test-member_name", "test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_describe_iam_policy_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)
    mock_client.describe_iam_policy_assignment.assert_called_once()


def test_describe_iam_policy_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_iam_policy_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_iam_policy_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe iam policy assignment"):
        describe_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)


def test_describe_ingestion(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", region_name=REGION)
    mock_client.describe_ingestion.assert_called_once()


def test_describe_ingestion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ingestion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ingestion",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ingestion"):
        describe_ingestion("test-aws_account_id", "test-data_set_id", "test-ingestion_id", region_name=REGION)


def test_describe_ip_restriction(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ip_restriction.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_ip_restriction("test-aws_account_id", region_name=REGION)
    mock_client.describe_ip_restriction.assert_called_once()


def test_describe_ip_restriction_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_ip_restriction.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ip_restriction",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe ip restriction"):
        describe_ip_restriction("test-aws_account_id", region_name=REGION)


def test_describe_key_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_registration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_key_registration("test-aws_account_id", region_name=REGION)
    mock_client.describe_key_registration.assert_called_once()


def test_describe_key_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_key_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_key_registration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe key registration"):
        describe_key_registration("test-aws_account_id", region_name=REGION)


def test_describe_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_namespace.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_namespace("test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.describe_namespace.assert_called_once()


def test_describe_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_namespace",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe namespace"):
        describe_namespace("test-aws_account_id", "test-namespace", region_name=REGION)


def test_describe_q_personalization_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_q_personalization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_q_personalization_configuration("test-aws_account_id", region_name=REGION)
    mock_client.describe_q_personalization_configuration.assert_called_once()


def test_describe_q_personalization_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_q_personalization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_q_personalization_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe q personalization configuration"):
        describe_q_personalization_configuration("test-aws_account_id", region_name=REGION)


def test_describe_quick_sight_q_search_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_quick_sight_q_search_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_quick_sight_q_search_configuration("test-aws_account_id", region_name=REGION)
    mock_client.describe_quick_sight_q_search_configuration.assert_called_once()


def test_describe_quick_sight_q_search_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_quick_sight_q_search_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_quick_sight_q_search_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe quick sight q search configuration"):
        describe_quick_sight_q_search_configuration("test-aws_account_id", region_name=REGION)


def test_describe_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_refresh_schedule("test-aws_account_id", "test-data_set_id", "test-schedule_id", region_name=REGION)
    mock_client.describe_refresh_schedule.assert_called_once()


def test_describe_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe refresh schedule"):
        describe_refresh_schedule("test-aws_account_id", "test-data_set_id", "test-schedule_id", region_name=REGION)


def test_describe_role_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_role_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.describe_role_custom_permission.assert_called_once()


def test_describe_role_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_role_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_role_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe role custom permission"):
        describe_role_custom_permission("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_describe_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.describe_template.assert_called_once()


def test_describe_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_template",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe template"):
        describe_template("test-aws_account_id", "test-template_id", region_name=REGION)


def test_describe_template_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", region_name=REGION)
    mock_client.describe_template_alias.assert_called_once()


def test_describe_template_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_template_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe template alias"):
        describe_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", region_name=REGION)


def test_describe_template_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_definition.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template_definition("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.describe_template_definition.assert_called_once()


def test_describe_template_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_template_definition",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe template definition"):
        describe_template_definition("test-aws_account_id", "test-template_id", region_name=REGION)


def test_describe_template_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template_permissions("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.describe_template_permissions.assert_called_once()


def test_describe_template_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_template_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_template_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe template permissions"):
        describe_template_permissions("test-aws_account_id", "test-template_id", region_name=REGION)


def test_describe_theme(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_theme("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.describe_theme.assert_called_once()


def test_describe_theme_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_theme",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe theme"):
        describe_theme("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_describe_theme_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", region_name=REGION)
    mock_client.describe_theme_alias.assert_called_once()


def test_describe_theme_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_theme_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe theme alias"):
        describe_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", region_name=REGION)


def test_describe_theme_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_theme_permissions("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.describe_theme_permissions.assert_called_once()


def test_describe_theme_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_theme_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_theme_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe theme permissions"):
        describe_theme_permissions("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_describe_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_topic("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.describe_topic.assert_called_once()


def test_describe_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_topic",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe topic"):
        describe_topic("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_describe_topic_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_topic_permissions("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.describe_topic_permissions.assert_called_once()


def test_describe_topic_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_topic_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe topic permissions"):
        describe_topic_permissions("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_describe_topic_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_refresh.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_topic_refresh("test-aws_account_id", "test-topic_id", "test-refresh_id", region_name=REGION)
    mock_client.describe_topic_refresh.assert_called_once()


def test_describe_topic_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_topic_refresh",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe topic refresh"):
        describe_topic_refresh("test-aws_account_id", "test-topic_id", "test-refresh_id", region_name=REGION)


def test_describe_topic_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", region_name=REGION)
    mock_client.describe_topic_refresh_schedule.assert_called_once()


def test_describe_topic_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_topic_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_topic_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe topic refresh schedule"):
        describe_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", region_name=REGION)


def test_describe_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_vpc_connection("test-aws_account_id", "test-vpc_connection_id", region_name=REGION)
    mock_client.describe_vpc_connection.assert_called_once()


def test_describe_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_connection",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc connection"):
        describe_vpc_connection("test-aws_account_id", "test-vpc_connection_id", region_name=REGION)


def test_generate_embed_url_for_anonymous_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_anonymous_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_anonymous_user("test-aws_account_id", "test-namespace", [], {}, region_name=REGION)
    mock_client.generate_embed_url_for_anonymous_user.assert_called_once()


def test_generate_embed_url_for_anonymous_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_anonymous_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_embed_url_for_anonymous_user",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate embed url for anonymous user"):
        generate_embed_url_for_anonymous_user("test-aws_account_id", "test-namespace", [], {}, region_name=REGION)


def test_generate_embed_url_for_registered_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_registered_user("test-aws_account_id", "test-user_arn", {}, region_name=REGION)
    mock_client.generate_embed_url_for_registered_user.assert_called_once()


def test_generate_embed_url_for_registered_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_embed_url_for_registered_user",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate embed url for registered user"):
        generate_embed_url_for_registered_user("test-aws_account_id", "test-user_arn", {}, region_name=REGION)


def test_generate_embed_url_for_registered_user_with_identity(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user_with_identity.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_registered_user_with_identity("test-aws_account_id", {}, region_name=REGION)
    mock_client.generate_embed_url_for_registered_user_with_identity.assert_called_once()


def test_generate_embed_url_for_registered_user_with_identity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user_with_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_embed_url_for_registered_user_with_identity",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate embed url for registered user with identity"):
        generate_embed_url_for_registered_user_with_identity("test-aws_account_id", {}, region_name=REGION)


def test_get_dashboard_embed_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dashboard_embed_url.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_dashboard_embed_url("test-aws_account_id", "test-dashboard_id", "test-identity_type", region_name=REGION)
    mock_client.get_dashboard_embed_url.assert_called_once()


def test_get_dashboard_embed_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dashboard_embed_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dashboard_embed_url",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dashboard embed url"):
        get_dashboard_embed_url("test-aws_account_id", "test-dashboard_id", "test-identity_type", region_name=REGION)


def test_get_flow_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_metadata.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_flow_metadata("test-aws_account_id", "test-flow_id", region_name=REGION)
    mock_client.get_flow_metadata.assert_called_once()


def test_get_flow_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_metadata",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow metadata"):
        get_flow_metadata("test-aws_account_id", "test-flow_id", region_name=REGION)


def test_get_flow_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_flow_permissions("test-aws_account_id", "test-flow_id", region_name=REGION)
    mock_client.get_flow_permissions.assert_called_once()


def test_get_flow_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow permissions"):
        get_flow_permissions("test-aws_account_id", "test-flow_id", region_name=REGION)


def test_get_session_embed_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_embed_url.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_session_embed_url("test-aws_account_id", region_name=REGION)
    mock_client.get_session_embed_url.assert_called_once()


def test_get_session_embed_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_embed_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session_embed_url",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session embed url"):
        get_session_embed_url("test-aws_account_id", region_name=REGION)


def test_list_action_connectors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_action_connectors.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_action_connectors("test-aws_account_id", region_name=REGION)
    mock_client.list_action_connectors.assert_called_once()


def test_list_action_connectors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_action_connectors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_action_connectors",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list action connectors"):
        list_action_connectors("test-aws_account_id", region_name=REGION)


def test_list_asset_bundle_export_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_asset_bundle_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_asset_bundle_export_jobs("test-aws_account_id", region_name=REGION)
    mock_client.list_asset_bundle_export_jobs.assert_called_once()


def test_list_asset_bundle_export_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_asset_bundle_export_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_bundle_export_jobs",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list asset bundle export jobs"):
        list_asset_bundle_export_jobs("test-aws_account_id", region_name=REGION)


def test_list_asset_bundle_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_asset_bundle_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_asset_bundle_import_jobs("test-aws_account_id", region_name=REGION)
    mock_client.list_asset_bundle_import_jobs.assert_called_once()


def test_list_asset_bundle_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_asset_bundle_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_asset_bundle_import_jobs",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list asset bundle import jobs"):
        list_asset_bundle_import_jobs("test-aws_account_id", region_name=REGION)


def test_list_brands(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_brands.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_brands("test-aws_account_id", region_name=REGION)
    mock_client.list_brands.assert_called_once()


def test_list_brands_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_brands.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_brands",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list brands"):
        list_brands("test-aws_account_id", region_name=REGION)


def test_list_custom_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_custom_permissions("test-aws_account_id", region_name=REGION)
    mock_client.list_custom_permissions.assert_called_once()


def test_list_custom_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_custom_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list custom permissions"):
        list_custom_permissions("test-aws_account_id", region_name=REGION)


def test_list_dashboard_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dashboard_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_dashboard_versions("test-aws_account_id", "test-dashboard_id", region_name=REGION)
    mock_client.list_dashboard_versions.assert_called_once()


def test_list_dashboard_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dashboard_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dashboard_versions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dashboard versions"):
        list_dashboard_versions("test-aws_account_id", "test-dashboard_id", region_name=REGION)


def test_list_data_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_data_sets("test-aws_account_id", region_name=REGION)
    mock_client.list_data_sets.assert_called_once()


def test_list_data_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_sets",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data sets"):
        list_data_sets("test-aws_account_id", region_name=REGION)


def test_list_flows(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flows.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_flows("test-aws_account_id", region_name=REGION)
    mock_client.list_flows.assert_called_once()


def test_list_flows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flows",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flows"):
        list_flows("test-aws_account_id", region_name=REGION)


def test_list_folder_members(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folder_members.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folder_members("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.list_folder_members.assert_called_once()


def test_list_folder_members_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folder_members.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_folder_members",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list folder members"):
        list_folder_members("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_list_folders(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folders.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folders("test-aws_account_id", region_name=REGION)
    mock_client.list_folders.assert_called_once()


def test_list_folders_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folders.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_folders",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list folders"):
        list_folders("test-aws_account_id", region_name=REGION)


def test_list_folders_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folders_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folders_for_resource("test-aws_account_id", "test-resource_arn", region_name=REGION)
    mock_client.list_folders_for_resource.assert_called_once()


def test_list_folders_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_folders_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_folders_for_resource",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list folders for resource"):
        list_folders_for_resource("test-aws_account_id", "test-resource_arn", region_name=REGION)


def test_list_group_memberships(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_group_memberships.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_group_memberships("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.list_group_memberships.assert_called_once()


def test_list_group_memberships_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_group_memberships.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_group_memberships",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list group memberships"):
        list_group_memberships("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_list_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_groups("test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.list_groups.assert_called_once()


def test_list_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_groups",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list groups"):
        list_groups("test-aws_account_id", "test-namespace", region_name=REGION)


def test_list_iam_policy_assignments(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_iam_policy_assignments("test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.list_iam_policy_assignments.assert_called_once()


def test_list_iam_policy_assignments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_iam_policy_assignments",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list iam policy assignments"):
        list_iam_policy_assignments("test-aws_account_id", "test-namespace", region_name=REGION)


def test_list_iam_policy_assignments_for_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments_for_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_iam_policy_assignments_for_user("test-aws_account_id", "test-user_name", "test-namespace", region_name=REGION)
    mock_client.list_iam_policy_assignments_for_user.assert_called_once()


def test_list_iam_policy_assignments_for_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments_for_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_iam_policy_assignments_for_user",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list iam policy assignments for user"):
        list_iam_policy_assignments_for_user("test-aws_account_id", "test-user_name", "test-namespace", region_name=REGION)


def test_list_identity_propagation_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_propagation_configs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_identity_propagation_configs("test-aws_account_id", region_name=REGION)
    mock_client.list_identity_propagation_configs.assert_called_once()


def test_list_identity_propagation_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_propagation_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_identity_propagation_configs",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list identity propagation configs"):
        list_identity_propagation_configs("test-aws_account_id", region_name=REGION)


def test_list_ingestions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ingestions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_ingestions("test-data_set_id", "test-aws_account_id", region_name=REGION)
    mock_client.list_ingestions.assert_called_once()


def test_list_ingestions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ingestions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ingestions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ingestions"):
        list_ingestions("test-data_set_id", "test-aws_account_id", region_name=REGION)


def test_list_namespaces(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_namespaces.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_namespaces("test-aws_account_id", region_name=REGION)
    mock_client.list_namespaces.assert_called_once()


def test_list_namespaces_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_namespaces.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_namespaces",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list namespaces"):
        list_namespaces("test-aws_account_id", region_name=REGION)


def test_list_refresh_schedules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_refresh_schedules.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_refresh_schedules("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.list_refresh_schedules.assert_called_once()


def test_list_refresh_schedules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_refresh_schedules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_refresh_schedules",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list refresh schedules"):
        list_refresh_schedules("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_list_role_memberships(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_memberships.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_role_memberships("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.list_role_memberships.assert_called_once()


def test_list_role_memberships_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_memberships.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_role_memberships",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list role memberships"):
        list_role_memberships("test-role", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_template_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_template_aliases.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_template_aliases("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.list_template_aliases.assert_called_once()


def test_list_template_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_template_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_template_aliases",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list template aliases"):
        list_template_aliases("test-aws_account_id", "test-template_id", region_name=REGION)


def test_list_template_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_template_versions("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.list_template_versions.assert_called_once()


def test_list_template_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_template_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_template_versions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list template versions"):
        list_template_versions("test-aws_account_id", "test-template_id", region_name=REGION)


def test_list_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_templates.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_templates("test-aws_account_id", region_name=REGION)
    mock_client.list_templates.assert_called_once()


def test_list_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_templates",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list templates"):
        list_templates("test-aws_account_id", region_name=REGION)


def test_list_theme_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_theme_aliases.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_theme_aliases("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.list_theme_aliases.assert_called_once()


def test_list_theme_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_theme_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_theme_aliases",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list theme aliases"):
        list_theme_aliases("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_list_theme_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_theme_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_theme_versions("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.list_theme_versions.assert_called_once()


def test_list_theme_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_theme_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_theme_versions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list theme versions"):
        list_theme_versions("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_list_themes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_themes.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_themes("test-aws_account_id", region_name=REGION)
    mock_client.list_themes.assert_called_once()


def test_list_themes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_themes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_themes",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list themes"):
        list_themes("test-aws_account_id", region_name=REGION)


def test_list_topic_refresh_schedules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topic_refresh_schedules.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_topic_refresh_schedules("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.list_topic_refresh_schedules.assert_called_once()


def test_list_topic_refresh_schedules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topic_refresh_schedules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topic_refresh_schedules",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list topic refresh schedules"):
        list_topic_refresh_schedules("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_list_topic_reviewed_answers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topic_reviewed_answers.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_topic_reviewed_answers("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.list_topic_reviewed_answers.assert_called_once()


def test_list_topic_reviewed_answers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topic_reviewed_answers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topic_reviewed_answers",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list topic reviewed answers"):
        list_topic_reviewed_answers("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_list_topics(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_topics("test-aws_account_id", region_name=REGION)
    mock_client.list_topics.assert_called_once()


def test_list_topics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_topics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topics",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list topics"):
        list_topics("test-aws_account_id", region_name=REGION)


def test_list_user_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_user_groups("test-user_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.list_user_groups.assert_called_once()


def test_list_user_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_groups",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user groups"):
        list_user_groups("test-user_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_list_vpc_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connections.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_vpc_connections("test-aws_account_id", region_name=REGION)
    mock_client.list_vpc_connections.assert_called_once()


def test_list_vpc_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_connections",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc connections"):
        list_vpc_connections("test-aws_account_id", region_name=REGION)


def test_predict_qa_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.predict_qa_results.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    predict_qa_results("test-aws_account_id", "test-query_text", region_name=REGION)
    mock_client.predict_qa_results.assert_called_once()


def test_predict_qa_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.predict_qa_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "predict_qa_results",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to predict qa results"):
        predict_qa_results("test-aws_account_id", "test-query_text", region_name=REGION)


def test_put_data_set_refresh_properties(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_set_refresh_properties.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    put_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", {}, region_name=REGION)
    mock_client.put_data_set_refresh_properties.assert_called_once()


def test_put_data_set_refresh_properties_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_data_set_refresh_properties.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_data_set_refresh_properties",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put data set refresh properties"):
        put_data_set_refresh_properties("test-aws_account_id", "test-data_set_id", {}, region_name=REGION)


def test_restore_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    restore_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.restore_analysis.assert_called_once()


def test_restore_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_analysis",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore analysis"):
        restore_analysis("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_search_action_connectors(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_action_connectors.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_action_connectors("test-aws_account_id", [], region_name=REGION)
    mock_client.search_action_connectors.assert_called_once()


def test_search_action_connectors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_action_connectors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_action_connectors",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search action connectors"):
        search_action_connectors("test-aws_account_id", [], region_name=REGION)


def test_search_analyses(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_analyses.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_analyses("test-aws_account_id", [], region_name=REGION)
    mock_client.search_analyses.assert_called_once()


def test_search_analyses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_analyses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_analyses",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search analyses"):
        search_analyses("test-aws_account_id", [], region_name=REGION)


def test_search_dashboards(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_dashboards.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_dashboards("test-aws_account_id", [], region_name=REGION)
    mock_client.search_dashboards.assert_called_once()


def test_search_dashboards_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_dashboards.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_dashboards",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search dashboards"):
        search_dashboards("test-aws_account_id", [], region_name=REGION)


def test_search_data_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_data_sets("test-aws_account_id", [], region_name=REGION)
    mock_client.search_data_sets.assert_called_once()


def test_search_data_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_data_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_data_sets",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search data sets"):
        search_data_sets("test-aws_account_id", [], region_name=REGION)


def test_search_data_sources(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_data_sources.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_data_sources("test-aws_account_id", [], region_name=REGION)
    mock_client.search_data_sources.assert_called_once()


def test_search_data_sources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_data_sources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_data_sources",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search data sources"):
        search_data_sources("test-aws_account_id", [], region_name=REGION)


def test_search_flows(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_flows.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_flows("test-aws_account_id", [], region_name=REGION)
    mock_client.search_flows.assert_called_once()


def test_search_flows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_flows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_flows",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search flows"):
        search_flows("test-aws_account_id", [], region_name=REGION)


def test_search_folders(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_folders.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_folders("test-aws_account_id", [], region_name=REGION)
    mock_client.search_folders.assert_called_once()


def test_search_folders_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_folders.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_folders",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search folders"):
        search_folders("test-aws_account_id", [], region_name=REGION)


def test_search_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_groups("test-aws_account_id", "test-namespace", [], region_name=REGION)
    mock_client.search_groups.assert_called_once()


def test_search_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_groups",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search groups"):
        search_groups("test-aws_account_id", "test-namespace", [], region_name=REGION)


def test_search_topics(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_topics.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_topics("test-aws_account_id", [], region_name=REGION)
    mock_client.search_topics.assert_called_once()


def test_search_topics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_topics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_topics",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search topics"):
        search_topics("test-aws_account_id", [], region_name=REGION)


def test_start_asset_bundle_export_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_asset_bundle_export_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", [], "test-export_format", region_name=REGION)
    mock_client.start_asset_bundle_export_job.assert_called_once()


def test_start_asset_bundle_export_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_asset_bundle_export_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_asset_bundle_export_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start asset bundle export job"):
        start_asset_bundle_export_job("test-aws_account_id", "test-asset_bundle_export_job_id", [], "test-export_format", region_name=REGION)


def test_start_asset_bundle_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_asset_bundle_import_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", {}, region_name=REGION)
    mock_client.start_asset_bundle_import_job.assert_called_once()


def test_start_asset_bundle_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_asset_bundle_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_asset_bundle_import_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start asset bundle import job"):
        start_asset_bundle_import_job("test-aws_account_id", "test-asset_bundle_import_job_id", {}, region_name=REGION)


def test_start_dashboard_snapshot_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_snapshot_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", {}, {}, region_name=REGION)
    mock_client.start_dashboard_snapshot_job.assert_called_once()


def test_start_dashboard_snapshot_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_snapshot_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_dashboard_snapshot_job",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start dashboard snapshot job"):
        start_dashboard_snapshot_job("test-aws_account_id", "test-dashboard_id", "test-snapshot_job_id", {}, {}, region_name=REGION)


def test_start_dashboard_snapshot_job_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_snapshot_job_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_dashboard_snapshot_job_schedule("test-aws_account_id", "test-dashboard_id", "test-schedule_id", region_name=REGION)
    mock_client.start_dashboard_snapshot_job_schedule.assert_called_once()


def test_start_dashboard_snapshot_job_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_snapshot_job_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_dashboard_snapshot_job_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start dashboard snapshot job schedule"):
        start_dashboard_snapshot_job_schedule("test-aws_account_id", "test-dashboard_id", "test-schedule_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_account_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_account_custom_permission("test-custom_permissions_name", "test-aws_account_id", region_name=REGION)
    mock_client.update_account_custom_permission.assert_called_once()


def test_update_account_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account custom permission"):
        update_account_custom_permission("test-custom_permissions_name", "test-aws_account_id", region_name=REGION)


def test_update_account_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_account_customization("test-aws_account_id", {}, region_name=REGION)
    mock_client.update_account_customization.assert_called_once()


def test_update_account_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_customization",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account customization"):
        update_account_customization("test-aws_account_id", {}, region_name=REGION)


def test_update_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_account_settings("test-aws_account_id", "test-default_namespace", region_name=REGION)
    mock_client.update_account_settings.assert_called_once()


def test_update_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_settings",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account settings"):
        update_account_settings("test-aws_account_id", "test-default_namespace", region_name=REGION)


def test_update_action_connector(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", {}, region_name=REGION)
    mock_client.update_action_connector.assert_called_once()


def test_update_action_connector_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_connector.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_action_connector",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update action connector"):
        update_action_connector("test-aws_account_id", "test-action_connector_id", "test-name", {}, region_name=REGION)


def test_update_action_connector_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_connector_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_action_connector_permissions("test-aws_account_id", "test-action_connector_id", region_name=REGION)
    mock_client.update_action_connector_permissions.assert_called_once()


def test_update_action_connector_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_connector_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_action_connector_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update action connector permissions"):
        update_action_connector_permissions("test-aws_account_id", "test-action_connector_id", region_name=REGION)


def test_update_analysis(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_analysis("test-aws_account_id", "test-analysis_id", "test-name", region_name=REGION)
    mock_client.update_analysis.assert_called_once()


def test_update_analysis_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_analysis.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_analysis",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update analysis"):
        update_analysis("test-aws_account_id", "test-analysis_id", "test-name", region_name=REGION)


def test_update_analysis_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_analysis_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_analysis_permissions("test-aws_account_id", "test-analysis_id", region_name=REGION)
    mock_client.update_analysis_permissions.assert_called_once()


def test_update_analysis_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_analysis_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_analysis_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update analysis permissions"):
        update_analysis_permissions("test-aws_account_id", "test-analysis_id", region_name=REGION)


def test_update_application_with_token_exchange_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application_with_token_exchange_grant.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_application_with_token_exchange_grant("test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.update_application_with_token_exchange_grant.assert_called_once()


def test_update_application_with_token_exchange_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application_with_token_exchange_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application_with_token_exchange_grant",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update application with token exchange grant"):
        update_application_with_token_exchange_grant("test-aws_account_id", "test-namespace", region_name=REGION)


def test_update_brand(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_brand("test-aws_account_id", "test-brand_id", region_name=REGION)
    mock_client.update_brand.assert_called_once()


def test_update_brand_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_brand",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update brand"):
        update_brand("test-aws_account_id", "test-brand_id", region_name=REGION)


def test_update_brand_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_brand_assignment("test-aws_account_id", "test-brand_arn", region_name=REGION)
    mock_client.update_brand_assignment.assert_called_once()


def test_update_brand_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_brand_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update brand assignment"):
        update_brand_assignment("test-aws_account_id", "test-brand_arn", region_name=REGION)


def test_update_brand_published_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand_published_version.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_brand_published_version("test-aws_account_id", "test-brand_id", "test-version_id", region_name=REGION)
    mock_client.update_brand_published_version.assert_called_once()


def test_update_brand_published_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_brand_published_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_brand_published_version",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update brand published version"):
        update_brand_published_version("test-aws_account_id", "test-brand_id", "test-version_id", region_name=REGION)


def test_update_custom_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)
    mock_client.update_custom_permissions.assert_called_once()


def test_update_custom_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_custom_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update custom permissions"):
        update_custom_permissions("test-aws_account_id", "test-custom_permissions_name", region_name=REGION)


def test_update_dashboard(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard("test-aws_account_id", "test-dashboard_id", "test-name", region_name=REGION)
    mock_client.update_dashboard.assert_called_once()


def test_update_dashboard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboard"):
        update_dashboard("test-aws_account_id", "test-dashboard_id", "test-name", region_name=REGION)


def test_update_dashboard_links(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_links.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard_links("test-aws_account_id", "test-dashboard_id", [], region_name=REGION)
    mock_client.update_dashboard_links.assert_called_once()


def test_update_dashboard_links_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_links.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard_links",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboard links"):
        update_dashboard_links("test-aws_account_id", "test-dashboard_id", [], region_name=REGION)


def test_update_dashboard_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard_permissions("test-aws_account_id", "test-dashboard_id", region_name=REGION)
    mock_client.update_dashboard_permissions.assert_called_once()


def test_update_dashboard_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboard permissions"):
        update_dashboard_permissions("test-aws_account_id", "test-dashboard_id", region_name=REGION)


def test_update_dashboard_published_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_published_version.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard_published_version("test-aws_account_id", "test-dashboard_id", 1, region_name=REGION)
    mock_client.update_dashboard_published_version.assert_called_once()


def test_update_dashboard_published_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard_published_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard_published_version",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboard published version"):
        update_dashboard_published_version("test-aws_account_id", "test-dashboard_id", 1, region_name=REGION)


def test_update_dashboards_qa_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboards_qa_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboards_qa_configuration("test-aws_account_id", "test-dashboards_qa_status", region_name=REGION)
    mock_client.update_dashboards_qa_configuration.assert_called_once()


def test_update_dashboards_qa_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboards_qa_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboards_qa_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboards qa configuration"):
        update_dashboards_qa_configuration("test-aws_account_id", "test-dashboards_qa_status", region_name=REGION)


def test_update_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", region_name=REGION)
    mock_client.update_data_set.assert_called_once()


def test_update_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_set",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data set"):
        update_data_set("test-aws_account_id", "test-data_set_id", "test-name", {}, "test-import_mode", region_name=REGION)


def test_update_data_set_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_set_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_set_permissions("test-aws_account_id", "test-data_set_id", region_name=REGION)
    mock_client.update_data_set_permissions.assert_called_once()


def test_update_data_set_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_set_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_set_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data set permissions"):
        update_data_set_permissions("test-aws_account_id", "test-data_set_id", region_name=REGION)


def test_update_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_source("test-aws_account_id", "test-data_source_id", "test-name", region_name=REGION)
    mock_client.update_data_source.assert_called_once()


def test_update_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_source",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data source"):
        update_data_source("test-aws_account_id", "test-data_source_id", "test-name", region_name=REGION)


def test_update_data_source_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_source_permissions("test-aws_account_id", "test-data_source_id", region_name=REGION)
    mock_client.update_data_source_permissions.assert_called_once()


def test_update_data_source_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_source_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_source_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data source permissions"):
        update_data_source_permissions("test-aws_account_id", "test-data_source_id", region_name=REGION)


def test_update_default_q_business_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_default_q_business_application("test-aws_account_id", "test-application_id", region_name=REGION)
    mock_client.update_default_q_business_application.assert_called_once()


def test_update_default_q_business_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_default_q_business_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_default_q_business_application",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update default q business application"):
        update_default_q_business_application("test-aws_account_id", "test-application_id", region_name=REGION)


def test_update_flow_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_flow_permissions("test-aws_account_id", "test-flow_id", region_name=REGION)
    mock_client.update_flow_permissions.assert_called_once()


def test_update_flow_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_flow_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_flow_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update flow permissions"):
        update_flow_permissions("test-aws_account_id", "test-flow_id", region_name=REGION)


def test_update_folder(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_folder.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_folder("test-aws_account_id", "test-folder_id", "test-name", region_name=REGION)
    mock_client.update_folder.assert_called_once()


def test_update_folder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_folder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_folder",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update folder"):
        update_folder("test-aws_account_id", "test-folder_id", "test-name", region_name=REGION)


def test_update_folder_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_folder_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_folder_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)
    mock_client.update_folder_permissions.assert_called_once()


def test_update_folder_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_folder_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_folder_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update folder permissions"):
        update_folder_permissions("test-aws_account_id", "test-folder_id", region_name=REGION)


def test_update_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.update_group.assert_called_once()


def test_update_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_group",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update group"):
        update_group("test-group_name", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_update_iam_policy_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)
    mock_client.update_iam_policy_assignment.assert_called_once()


def test_update_iam_policy_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_iam_policy_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_iam_policy_assignment",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update iam policy assignment"):
        update_iam_policy_assignment("test-aws_account_id", "test-assignment_name", "test-namespace", region_name=REGION)


def test_update_identity_propagation_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_identity_propagation_config.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_identity_propagation_config("test-aws_account_id", "test-service", region_name=REGION)
    mock_client.update_identity_propagation_config.assert_called_once()


def test_update_identity_propagation_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_identity_propagation_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_identity_propagation_config",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update identity propagation config"):
        update_identity_propagation_config("test-aws_account_id", "test-service", region_name=REGION)


def test_update_ip_restriction(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ip_restriction.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_ip_restriction("test-aws_account_id", region_name=REGION)
    mock_client.update_ip_restriction.assert_called_once()


def test_update_ip_restriction_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ip_restriction.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ip_restriction",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update ip restriction"):
        update_ip_restriction("test-aws_account_id", region_name=REGION)


def test_update_key_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_registration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_key_registration("test-aws_account_id", [], region_name=REGION)
    mock_client.update_key_registration.assert_called_once()


def test_update_key_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_key_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_key_registration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update key registration"):
        update_key_registration("test-aws_account_id", [], region_name=REGION)


def test_update_public_sharing_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_public_sharing_settings.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_public_sharing_settings("test-aws_account_id", region_name=REGION)
    mock_client.update_public_sharing_settings.assert_called_once()


def test_update_public_sharing_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_public_sharing_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_public_sharing_settings",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update public sharing settings"):
        update_public_sharing_settings("test-aws_account_id", region_name=REGION)


def test_update_q_personalization_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_q_personalization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_q_personalization_configuration("test-aws_account_id", "test-personalization_mode", region_name=REGION)
    mock_client.update_q_personalization_configuration.assert_called_once()


def test_update_q_personalization_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_q_personalization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_q_personalization_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update q personalization configuration"):
        update_q_personalization_configuration("test-aws_account_id", "test-personalization_mode", region_name=REGION)


def test_update_quick_sight_q_search_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_sight_q_search_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_quick_sight_q_search_configuration("test-aws_account_id", "test-q_search_status", region_name=REGION)
    mock_client.update_quick_sight_q_search_configuration.assert_called_once()


def test_update_quick_sight_q_search_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_sight_q_search_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_quick_sight_q_search_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update quick sight q search configuration"):
        update_quick_sight_q_search_configuration("test-aws_account_id", "test-q_search_status", region_name=REGION)


def test_update_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, region_name=REGION)
    mock_client.update_refresh_schedule.assert_called_once()


def test_update_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update refresh schedule"):
        update_refresh_schedule("test-data_set_id", "test-aws_account_id", {}, region_name=REGION)


def test_update_role_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_role_custom_permission("test-custom_permissions_name", "test-role", "test-aws_account_id", "test-namespace", region_name=REGION)
    mock_client.update_role_custom_permission.assert_called_once()


def test_update_role_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_role_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update role custom permission"):
        update_role_custom_permission("test-custom_permissions_name", "test-role", "test-aws_account_id", "test-namespace", region_name=REGION)


def test_update_spice_capacity_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_spice_capacity_configuration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_spice_capacity_configuration("test-aws_account_id", "test-purchase_mode", region_name=REGION)
    mock_client.update_spice_capacity_configuration.assert_called_once()


def test_update_spice_capacity_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_spice_capacity_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_spice_capacity_configuration",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update spice capacity configuration"):
        update_spice_capacity_configuration("test-aws_account_id", "test-purchase_mode", region_name=REGION)


def test_update_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_template("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.update_template.assert_called_once()


def test_update_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_template",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update template"):
        update_template("test-aws_account_id", "test-template_id", region_name=REGION)


def test_update_template_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, region_name=REGION)
    mock_client.update_template_alias.assert_called_once()


def test_update_template_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_template_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update template alias"):
        update_template_alias("test-aws_account_id", "test-template_id", "test-alias_name", 1, region_name=REGION)


def test_update_template_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_template_permissions("test-aws_account_id", "test-template_id", region_name=REGION)
    mock_client.update_template_permissions.assert_called_once()


def test_update_template_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_template_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_template_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update template permissions"):
        update_template_permissions("test-aws_account_id", "test-template_id", region_name=REGION)


def test_update_theme(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_theme("test-aws_account_id", "test-theme_id", "test-base_theme_id", region_name=REGION)
    mock_client.update_theme.assert_called_once()


def test_update_theme_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_theme",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update theme"):
        update_theme("test-aws_account_id", "test-theme_id", "test-base_theme_id", region_name=REGION)


def test_update_theme_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme_alias.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, region_name=REGION)
    mock_client.update_theme_alias.assert_called_once()


def test_update_theme_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_theme_alias",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update theme alias"):
        update_theme_alias("test-aws_account_id", "test-theme_id", "test-alias_name", 1, region_name=REGION)


def test_update_theme_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_theme_permissions("test-aws_account_id", "test-theme_id", region_name=REGION)
    mock_client.update_theme_permissions.assert_called_once()


def test_update_theme_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_theme_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_theme_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update theme permissions"):
        update_theme_permissions("test-aws_account_id", "test-theme_id", region_name=REGION)


def test_update_topic(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_topic("test-aws_account_id", "test-topic_id", {}, region_name=REGION)
    mock_client.update_topic.assert_called_once()


def test_update_topic_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_topic",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update topic"):
        update_topic("test-aws_account_id", "test-topic_id", {}, region_name=REGION)


def test_update_topic_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_topic_permissions("test-aws_account_id", "test-topic_id", region_name=REGION)
    mock_client.update_topic_permissions.assert_called_once()


def test_update_topic_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_topic_permissions",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update topic permissions"):
        update_topic_permissions("test-aws_account_id", "test-topic_id", region_name=REGION)


def test_update_topic_refresh_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", {}, region_name=REGION)
    mock_client.update_topic_refresh_schedule.assert_called_once()


def test_update_topic_refresh_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_topic_refresh_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_topic_refresh_schedule",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update topic refresh schedule"):
        update_topic_refresh_schedule("test-aws_account_id", "test-topic_id", "test-dataset_id", {}, region_name=REGION)


def test_update_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_user("test-user_name", "test-aws_account_id", "test-namespace", "test-email", "test-role", region_name=REGION)
    mock_client.update_user.assert_called_once()


def test_update_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user"):
        update_user("test-user_name", "test-aws_account_id", "test-namespace", "test-email", "test-role", region_name=REGION)


def test_update_user_custom_permission(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_custom_permission.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", "test-custom_permissions_name", region_name=REGION)
    mock_client.update_user_custom_permission.assert_called_once()


def test_update_user_custom_permission_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_custom_permission.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_custom_permission",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user custom permission"):
        update_user_custom_permission("test-user_name", "test-aws_account_id", "test-namespace", "test-custom_permissions_name", region_name=REGION)


def test_update_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", region_name=REGION)
    mock_client.update_vpc_connection.assert_called_once()


def test_update_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vpc_connection",
    )
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vpc connection"):
        update_vpc_connection("test-aws_account_id", "test-vpc_connection_id", "test-name", [], [], "test-role_arn", region_name=REGION)


def test_create_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_dashboard
    mock_client = MagicMock()
    mock_client.create_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_dashboard(1, "test-dashboard_id", "test-name", "test-source_entity", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dashboard.assert_called_once()

def test_create_dataset_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_dataset
    mock_client = MagicMock()
    mock_client.create_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_dataset(1, "test-dataset_id", "test-name", "test-physical_table_map", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_data_set.assert_called_once()

def test_create_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_analysis
    mock_client = MagicMock()
    mock_client.create_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_analysis(1, "test-analysis_id", "test-name", "test-source_entity", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_analysis.assert_called_once()

def test_create_data_source_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_data_source
    mock_client = MagicMock()
    mock_client.create_data_source.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_data_source(1, "test-data_source_id", "test-name", "test-data_source_type", "test-data_source_parameters", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_data_source.assert_called_once()

def test_register_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import register_user
    mock_client = MagicMock()
    mock_client.register_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    register_user(1, "test-email", "test-identity_type", "test-user_role", iam_arn="test-iam_arn", session_name="test-session_name", region_name="us-east-1")
    mock_client.register_user.assert_called_once()

def test_batch_delete_topic_reviewed_answer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import batch_delete_topic_reviewed_answer
    mock_client = MagicMock()
    mock_client.batch_delete_topic_reviewed_answer.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    batch_delete_topic_reviewed_answer(1, "test-topic_id", answer_ids="test-answer_ids", region_name="us-east-1")
    mock_client.batch_delete_topic_reviewed_answer.assert_called_once()

def test_create_account_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_account_customization
    mock_client = MagicMock()
    mock_client.create_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_account_customization(1, 1, namespace="test-namespace", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_account_customization.assert_called_once()

def test_create_account_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_account_subscription
    mock_client = MagicMock()
    mock_client.create_account_subscription.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_account_subscription("test-authentication_method", 1, 1, "test-notification_email", edition="test-edition", active_directory_name="test-active_directory_name", realm="test-realm", directory_id="test-directory_id", admin_group="test-admin_group", author_group="test-author_group", reader_group="test-reader_group", admin_pro_group="test-admin_pro_group", author_pro_group="test-author_pro_group", reader_pro_group="test-reader_pro_group", first_name="test-first_name", last_name="test-last_name", email_address="test-email_address", contact_number="test-contact_number", iam_identity_center_instance_arn="test-iam_identity_center_instance_arn", region_name="us-east-1")
    mock_client.create_account_subscription.assert_called_once()

def test_create_action_connector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_action_connector
    mock_client = MagicMock()
    mock_client.create_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_action_connector(1, "test-action_connector_id", "test-name", "test-type_value", {}, description="test-description", permissions="test-permissions", vpc_connection_arn="test-vpc_connection_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_action_connector.assert_called_once()

def test_create_brand_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_brand
    mock_client = MagicMock()
    mock_client.create_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_brand(1, "test-brand_id", brand_definition={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_brand.assert_called_once()

def test_create_custom_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_custom_permissions
    mock_client = MagicMock()
    mock_client.create_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_custom_permissions(1, "test-custom_permissions_name", capabilities="test-capabilities", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_permissions.assert_called_once()

def test_create_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_data_set
    mock_client = MagicMock()
    mock_client.create_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_data_set(1, "test-data_set_id", "test-name", "test-physical_table_map", 1, logical_table_map="test-logical_table_map", column_groups="test-column_groups", field_folders="test-field_folders", permissions="test-permissions", row_level_permission_data_set="test-row_level_permission_data_set", row_level_permission_tag_configuration={}, column_level_permission_rules="test-column_level_permission_rules", tags=[{"Key": "k", "Value": "v"}], data_set_usage_configuration={}, dataset_parameters="test-dataset_parameters", folder_arns="test-folder_arns", performance_configuration={}, use_as=True, data_prep_configuration={}, semantic_model_configuration={}, region_name="us-east-1")
    mock_client.create_data_set.assert_called_once()

def test_create_folder_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_folder
    mock_client = MagicMock()
    mock_client.create_folder.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_folder(1, "test-folder_id", name="test-name", folder_type="test-folder_type", parent_folder_arn="test-parent_folder_arn", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], sharing_model="test-sharing_model", region_name="us-east-1")
    mock_client.create_folder.assert_called_once()

def test_create_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_group
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", 1, "test-namespace", description="test-description", region_name="us-east-1")
    mock_client.create_group.assert_called_once()

def test_create_iam_policy_assignment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_iam_policy_assignment
    mock_client = MagicMock()
    mock_client.create_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_iam_policy_assignment(1, "test-assignment_name", "test-assignment_status", "test-namespace", policy_arn="test-policy_arn", identities="test-identities", region_name="us-east-1")
    mock_client.create_iam_policy_assignment.assert_called_once()

def test_create_ingestion_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_ingestion
    mock_client = MagicMock()
    mock_client.create_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_ingestion("test-data_set_id", "test-ingestion_id", 1, ingestion_type="test-ingestion_type", region_name="us-east-1")
    mock_client.create_ingestion.assert_called_once()

def test_create_namespace_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_namespace
    mock_client = MagicMock()
    mock_client.create_namespace.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_namespace(1, "test-namespace", "test-identity_store", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_namespace.assert_called_once()

def test_create_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_template
    mock_client = MagicMock()
    mock_client.create_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_template(1, "test-template_id", name="test-name", permissions="test-permissions", source_entity="test-source_entity", tags=[{"Key": "k", "Value": "v"}], version_description="test-version_description", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.create_template.assert_called_once()

def test_create_theme_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_theme
    mock_client = MagicMock()
    mock_client.create_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_theme(1, "test-theme_id", "test-name", "test-base_theme_id", {}, version_description="test-version_description", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_theme.assert_called_once()

def test_create_topic_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_topic
    mock_client = MagicMock()
    mock_client.create_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_topic(1, "test-topic_id", "test-topic", tags=[{"Key": "k", "Value": "v"}], folder_arns="test-folder_arns", custom_instructions="test-custom_instructions", region_name="us-east-1")
    mock_client.create_topic.assert_called_once()

def test_create_topic_refresh_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_topic_refresh_schedule
    mock_client = MagicMock()
    mock_client.create_topic_refresh_schedule.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_topic_refresh_schedule(1, "test-topic_id", "test-dataset_arn", "test-refresh_schedule", dataset_name="test-dataset_name", region_name="us-east-1")
    mock_client.create_topic_refresh_schedule.assert_called_once()

def test_create_vpc_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import create_vpc_connection
    mock_client = MagicMock()
    mock_client.create_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    create_vpc_connection(1, "test-vpc_connection_id", "test-name", "test-subnet_ids", "test-security_group_ids", "test-role_arn", dns_resolvers="test-dns_resolvers", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vpc_connection.assert_called_once()

def test_delete_account_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import delete_account_customization
    mock_client = MagicMock()
    mock_client.delete_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_account_customization(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.delete_account_customization.assert_called_once()

def test_delete_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import delete_analysis
    mock_client = MagicMock()
    mock_client.delete_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_analysis(1, "test-analysis_id", recovery_window_in_days="test-recovery_window_in_days", force_delete_without_recovery=True, region_name="us-east-1")
    mock_client.delete_analysis.assert_called_once()

def test_delete_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import delete_default_q_business_application
    mock_client = MagicMock()
    mock_client.delete_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_default_q_business_application(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.delete_default_q_business_application.assert_called_once()

def test_delete_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import delete_template
    mock_client = MagicMock()
    mock_client.delete_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_template(1, "test-template_id", version_number="test-version_number", region_name="us-east-1")
    mock_client.delete_template.assert_called_once()

def test_delete_theme_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import delete_theme
    mock_client = MagicMock()
    mock_client.delete_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    delete_theme(1, "test-theme_id", version_number="test-version_number", region_name="us-east-1")
    mock_client.delete_theme.assert_called_once()

def test_describe_account_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_account_customization
    mock_client = MagicMock()
    mock_client.describe_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_account_customization(1, namespace="test-namespace", resolved="test-resolved", region_name="us-east-1")
    mock_client.describe_account_customization.assert_called_once()

def test_describe_brand_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_brand
    mock_client = MagicMock()
    mock_client.describe_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_brand(1, "test-brand_id", version_id="test-version_id", region_name="us-east-1")
    mock_client.describe_brand.assert_called_once()

def test_describe_dashboard_definition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_dashboard_definition
    mock_client = MagicMock()
    mock_client.describe_dashboard_definition.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_dashboard_definition(1, "test-dashboard_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.describe_dashboard_definition.assert_called_once()

def test_describe_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_default_q_business_application
    mock_client = MagicMock()
    mock_client.describe_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_default_q_business_application(1, namespace="test-namespace", region_name="us-east-1")
    mock_client.describe_default_q_business_application.assert_called_once()

def test_describe_folder_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_folder_permissions
    mock_client = MagicMock()
    mock_client.describe_folder_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_folder_permissions(1, "test-folder_id", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_folder_permissions.assert_called_once()

def test_describe_folder_resolved_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_folder_resolved_permissions
    mock_client = MagicMock()
    mock_client.describe_folder_resolved_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_folder_resolved_permissions(1, "test-folder_id", namespace="test-namespace", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_folder_resolved_permissions.assert_called_once()

def test_describe_key_registration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_key_registration
    mock_client = MagicMock()
    mock_client.describe_key_registration.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_key_registration(1, default_key_only="test-default_key_only", region_name="us-east-1")
    mock_client.describe_key_registration.assert_called_once()

def test_describe_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_template
    mock_client = MagicMock()
    mock_client.describe_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template(1, "test-template_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.describe_template.assert_called_once()

def test_describe_template_definition_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_template_definition
    mock_client = MagicMock()
    mock_client.describe_template_definition.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_template_definition(1, "test-template_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.describe_template_definition.assert_called_once()

def test_describe_theme_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import describe_theme
    mock_client = MagicMock()
    mock_client.describe_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    describe_theme(1, "test-theme_id", version_number="test-version_number", alias_name="test-alias_name", region_name="us-east-1")
    mock_client.describe_theme.assert_called_once()

def test_generate_embed_url_for_anonymous_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import generate_embed_url_for_anonymous_user
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_anonymous_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_anonymous_user(1, "test-namespace", "test-authorized_resource_arns", {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", session_tags=[{"Key": "k", "Value": "v"}], allowed_domains=True, region_name="us-east-1")
    mock_client.generate_embed_url_for_anonymous_user.assert_called_once()

def test_generate_embed_url_for_registered_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import generate_embed_url_for_registered_user
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_registered_user(1, "test-user_arn", {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", allowed_domains=True, region_name="us-east-1")
    mock_client.generate_embed_url_for_registered_user.assert_called_once()

def test_generate_embed_url_for_registered_user_with_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import generate_embed_url_for_registered_user_with_identity
    mock_client = MagicMock()
    mock_client.generate_embed_url_for_registered_user_with_identity.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    generate_embed_url_for_registered_user_with_identity(1, {}, session_lifetime_in_minutes="test-session_lifetime_in_minutes", allowed_domains=True, region_name="us-east-1")
    mock_client.generate_embed_url_for_registered_user_with_identity.assert_called_once()

def test_get_dashboard_embed_url_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import get_dashboard_embed_url
    mock_client = MagicMock()
    mock_client.get_dashboard_embed_url.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_dashboard_embed_url(1, "test-dashboard_id", "test-identity_type", session_lifetime_in_minutes="test-session_lifetime_in_minutes", undo_redo_disabled="test-undo_redo_disabled", reset_disabled="test-reset_disabled", state_persistence_enabled="test-state_persistence_enabled", user_arn="test-user_arn", namespace="test-namespace", additional_dashboard_ids="test-additional_dashboard_ids", region_name="us-east-1")
    mock_client.get_dashboard_embed_url.assert_called_once()

def test_get_session_embed_url_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import get_session_embed_url
    mock_client = MagicMock()
    mock_client.get_session_embed_url.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    get_session_embed_url(1, entry_point="test-entry_point", session_lifetime_in_minutes="test-session_lifetime_in_minutes", user_arn="test-user_arn", region_name="us-east-1")
    mock_client.get_session_embed_url.assert_called_once()

def test_list_action_connectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_action_connectors
    mock_client = MagicMock()
    mock_client.list_action_connectors.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_action_connectors(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_action_connectors.assert_called_once()

def test_list_asset_bundle_export_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_asset_bundle_export_jobs
    mock_client = MagicMock()
    mock_client.list_asset_bundle_export_jobs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_asset_bundle_export_jobs(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_asset_bundle_export_jobs.assert_called_once()

def test_list_asset_bundle_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_asset_bundle_import_jobs
    mock_client = MagicMock()
    mock_client.list_asset_bundle_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_asset_bundle_import_jobs(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_asset_bundle_import_jobs.assert_called_once()

def test_list_brands_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_brands
    mock_client = MagicMock()
    mock_client.list_brands.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_brands(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_brands.assert_called_once()

def test_list_custom_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_custom_permissions
    mock_client = MagicMock()
    mock_client.list_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_custom_permissions(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_custom_permissions.assert_called_once()

def test_list_dashboard_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_dashboard_versions
    mock_client = MagicMock()
    mock_client.list_dashboard_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_dashboard_versions(1, "test-dashboard_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dashboard_versions.assert_called_once()

def test_list_data_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_data_sets
    mock_client = MagicMock()
    mock_client.list_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_data_sets(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_data_sets.assert_called_once()

def test_list_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_flows
    mock_client = MagicMock()
    mock_client.list_flows.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_flows(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_flows.assert_called_once()

def test_list_folder_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_folder_members
    mock_client = MagicMock()
    mock_client.list_folder_members.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folder_members(1, "test-folder_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_folder_members.assert_called_once()

def test_list_folders_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_folders
    mock_client = MagicMock()
    mock_client.list_folders.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folders(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_folders.assert_called_once()

def test_list_folders_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_folders_for_resource
    mock_client = MagicMock()
    mock_client.list_folders_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_folders_for_resource(1, "test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_folders_for_resource.assert_called_once()

def test_list_group_memberships_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_group_memberships
    mock_client = MagicMock()
    mock_client.list_group_memberships.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_group_memberships("test-group_name", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_group_memberships.assert_called_once()

def test_list_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_groups
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_groups(1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_groups.assert_called_once()

def test_list_iam_policy_assignments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_iam_policy_assignments
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_iam_policy_assignments(1, "test-namespace", assignment_status="test-assignment_status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_iam_policy_assignments.assert_called_once()

def test_list_iam_policy_assignments_for_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_iam_policy_assignments_for_user
    mock_client = MagicMock()
    mock_client.list_iam_policy_assignments_for_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_iam_policy_assignments_for_user(1, "test-user_name", "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_iam_policy_assignments_for_user.assert_called_once()

def test_list_identity_propagation_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_identity_propagation_configs
    mock_client = MagicMock()
    mock_client.list_identity_propagation_configs.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_identity_propagation_configs(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_identity_propagation_configs.assert_called_once()

def test_list_ingestions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_ingestions
    mock_client = MagicMock()
    mock_client.list_ingestions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_ingestions("test-data_set_id", 1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_ingestions.assert_called_once()

def test_list_namespaces_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_namespaces
    mock_client = MagicMock()
    mock_client.list_namespaces.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_namespaces(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_namespaces.assert_called_once()

def test_list_role_memberships_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_role_memberships
    mock_client = MagicMock()
    mock_client.list_role_memberships.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_role_memberships("test-role", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_role_memberships.assert_called_once()

def test_list_template_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_template_aliases
    mock_client = MagicMock()
    mock_client.list_template_aliases.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_template_aliases(1, "test-template_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_template_aliases.assert_called_once()

def test_list_template_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_template_versions
    mock_client = MagicMock()
    mock_client.list_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_template_versions(1, "test-template_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_template_versions.assert_called_once()

def test_list_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_templates
    mock_client = MagicMock()
    mock_client.list_templates.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_templates(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_templates.assert_called_once()

def test_list_theme_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_theme_aliases
    mock_client = MagicMock()
    mock_client.list_theme_aliases.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_theme_aliases(1, "test-theme_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_theme_aliases.assert_called_once()

def test_list_theme_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_theme_versions
    mock_client = MagicMock()
    mock_client.list_theme_versions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_theme_versions(1, "test-theme_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_theme_versions.assert_called_once()

def test_list_themes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_themes
    mock_client = MagicMock()
    mock_client.list_themes.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_themes(1, next_token="test-next_token", max_results=1, type_value="test-type_value", region_name="us-east-1")
    mock_client.list_themes.assert_called_once()

def test_list_topics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_topics
    mock_client = MagicMock()
    mock_client.list_topics.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_topics(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_topics.assert_called_once()

def test_list_user_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_user_groups
    mock_client = MagicMock()
    mock_client.list_user_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_user_groups("test-user_name", 1, "test-namespace", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_user_groups.assert_called_once()

def test_list_vpc_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import list_vpc_connections
    mock_client = MagicMock()
    mock_client.list_vpc_connections.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    list_vpc_connections(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_vpc_connections.assert_called_once()

def test_predict_qa_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import predict_qa_results
    mock_client = MagicMock()
    mock_client.predict_qa_results.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    predict_qa_results(1, "test-query_text", include_quick_sight_q_index=True, include_generated_answer=True, max_topics_to_consider=1, region_name="us-east-1")
    mock_client.predict_qa_results.assert_called_once()

def test_restore_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import restore_analysis
    mock_client = MagicMock()
    mock_client.restore_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    restore_analysis(1, "test-analysis_id", restore_to_folders="test-restore_to_folders", region_name="us-east-1")
    mock_client.restore_analysis.assert_called_once()

def test_search_action_connectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_action_connectors
    mock_client = MagicMock()
    mock_client.search_action_connectors.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_action_connectors(1, [{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.search_action_connectors.assert_called_once()

def test_search_analyses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_analyses
    mock_client = MagicMock()
    mock_client.search_analyses.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_analyses(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_analyses.assert_called_once()

def test_search_dashboards_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_dashboards
    mock_client = MagicMock()
    mock_client.search_dashboards.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_dashboards(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_dashboards.assert_called_once()

def test_search_data_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_data_sets
    mock_client = MagicMock()
    mock_client.search_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_data_sets(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_data_sets.assert_called_once()

def test_search_data_sources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_data_sources
    mock_client = MagicMock()
    mock_client.search_data_sources.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_data_sources(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_data_sources.assert_called_once()

def test_search_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_flows
    mock_client = MagicMock()
    mock_client.search_flows.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_flows(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_flows.assert_called_once()

def test_search_folders_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_folders
    mock_client = MagicMock()
    mock_client.search_folders.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_folders(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_folders.assert_called_once()

def test_search_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_groups
    mock_client = MagicMock()
    mock_client.search_groups.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_groups(1, "test-namespace", [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_groups.assert_called_once()

def test_search_topics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import search_topics
    mock_client = MagicMock()
    mock_client.search_topics.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    search_topics(1, [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.search_topics.assert_called_once()

def test_start_asset_bundle_export_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import start_asset_bundle_export_job
    mock_client = MagicMock()
    mock_client.start_asset_bundle_export_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_asset_bundle_export_job(1, 1, "test-resource_arns", 1, include_all_dependencies=True, cloud_formation_override_property_configuration={}, include_permissions=True, include_tags=True, validation_strategy="test-validation_strategy", include_folder_memberships=True, include_folder_members=True, region_name="us-east-1")
    mock_client.start_asset_bundle_export_job.assert_called_once()

def test_start_asset_bundle_import_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import start_asset_bundle_import_job
    mock_client = MagicMock()
    mock_client.start_asset_bundle_import_job.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    start_asset_bundle_import_job(1, 1, 1, override_parameters="test-override_parameters", failure_action="test-failure_action", override_permissions="test-override_permissions", override_tags=[{"Key": "k", "Value": "v"}], override_validation_strategy="test-override_validation_strategy", region_name="us-east-1")
    mock_client.start_asset_bundle_import_job.assert_called_once()

def test_update_account_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_account_customization
    mock_client = MagicMock()
    mock_client.update_account_customization.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_account_customization(1, 1, namespace="test-namespace", region_name="us-east-1")
    mock_client.update_account_customization.assert_called_once()

def test_update_account_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_account_settings
    mock_client = MagicMock()
    mock_client.update_account_settings.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_account_settings(1, "test-default_namespace", notification_email="test-notification_email", termination_protection_enabled="test-termination_protection_enabled", region_name="us-east-1")
    mock_client.update_account_settings.assert_called_once()

def test_update_action_connector_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_action_connector
    mock_client = MagicMock()
    mock_client.update_action_connector.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_action_connector(1, "test-action_connector_id", "test-name", {}, description="test-description", vpc_connection_arn="test-vpc_connection_arn", region_name="us-east-1")
    mock_client.update_action_connector.assert_called_once()

def test_update_action_connector_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_action_connector_permissions
    mock_client = MagicMock()
    mock_client.update_action_connector_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_action_connector_permissions(1, "test-action_connector_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_action_connector_permissions.assert_called_once()

def test_update_analysis_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_analysis
    mock_client = MagicMock()
    mock_client.update_analysis.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_analysis(1, "test-analysis_id", "test-name", parameters="test-parameters", source_entity="test-source_entity", theme_arn="test-theme_arn", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.update_analysis.assert_called_once()

def test_update_analysis_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_analysis_permissions
    mock_client = MagicMock()
    mock_client.update_analysis_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_analysis_permissions(1, "test-analysis_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_analysis_permissions.assert_called_once()

def test_update_brand_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_brand
    mock_client = MagicMock()
    mock_client.update_brand.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_brand(1, "test-brand_id", brand_definition={}, region_name="us-east-1")
    mock_client.update_brand.assert_called_once()

def test_update_custom_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_custom_permissions
    mock_client = MagicMock()
    mock_client.update_custom_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_custom_permissions(1, "test-custom_permissions_name", capabilities="test-capabilities", region_name="us-east-1")
    mock_client.update_custom_permissions.assert_called_once()

def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_dashboard
    mock_client = MagicMock()
    mock_client.update_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard(1, "test-dashboard_id", "test-name", source_entity="test-source_entity", parameters="test-parameters", version_description="test-version_description", dashboard_publish_options={}, theme_arn="test-theme_arn", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.update_dashboard.assert_called_once()

def test_update_dashboard_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_dashboard_permissions
    mock_client = MagicMock()
    mock_client.update_dashboard_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_dashboard_permissions(1, "test-dashboard_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", grant_link_permissions="test-grant_link_permissions", revoke_link_permissions="test-revoke_link_permissions", region_name="us-east-1")
    mock_client.update_dashboard_permissions.assert_called_once()

def test_update_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_data_set
    mock_client = MagicMock()
    mock_client.update_data_set.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_set(1, "test-data_set_id", "test-name", "test-physical_table_map", 1, logical_table_map="test-logical_table_map", column_groups="test-column_groups", field_folders="test-field_folders", row_level_permission_data_set="test-row_level_permission_data_set", row_level_permission_tag_configuration={}, column_level_permission_rules="test-column_level_permission_rules", data_set_usage_configuration={}, dataset_parameters="test-dataset_parameters", performance_configuration={}, data_prep_configuration={}, semantic_model_configuration={}, region_name="us-east-1")
    mock_client.update_data_set.assert_called_once()

def test_update_data_set_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_data_set_permissions
    mock_client = MagicMock()
    mock_client.update_data_set_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_set_permissions(1, "test-data_set_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_data_set_permissions.assert_called_once()

def test_update_data_source_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_data_source
    mock_client = MagicMock()
    mock_client.update_data_source.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_source(1, "test-data_source_id", "test-name", data_source_parameters="test-data_source_parameters", credentials="test-credentials", vpc_connection_properties={}, ssl_properties={}, region_name="us-east-1")
    mock_client.update_data_source.assert_called_once()

def test_update_data_source_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_data_source_permissions
    mock_client = MagicMock()
    mock_client.update_data_source_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_data_source_permissions(1, "test-data_source_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_data_source_permissions.assert_called_once()

def test_update_default_q_business_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_default_q_business_application
    mock_client = MagicMock()
    mock_client.update_default_q_business_application.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_default_q_business_application(1, "test-application_id", namespace="test-namespace", region_name="us-east-1")
    mock_client.update_default_q_business_application.assert_called_once()

def test_update_flow_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_flow_permissions
    mock_client = MagicMock()
    mock_client.update_flow_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_flow_permissions(1, "test-flow_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_flow_permissions.assert_called_once()

def test_update_folder_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_folder_permissions
    mock_client = MagicMock()
    mock_client.update_folder_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_folder_permissions(1, "test-folder_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_folder_permissions.assert_called_once()

def test_update_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_group
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", 1, "test-namespace", description="test-description", region_name="us-east-1")
    mock_client.update_group.assert_called_once()

def test_update_iam_policy_assignment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_iam_policy_assignment
    mock_client = MagicMock()
    mock_client.update_iam_policy_assignment.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_iam_policy_assignment(1, "test-assignment_name", "test-namespace", assignment_status="test-assignment_status", policy_arn="test-policy_arn", identities="test-identities", region_name="us-east-1")
    mock_client.update_iam_policy_assignment.assert_called_once()

def test_update_identity_propagation_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_identity_propagation_config
    mock_client = MagicMock()
    mock_client.update_identity_propagation_config.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_identity_propagation_config(1, "test-service", authorized_targets="test-authorized_targets", region_name="us-east-1")
    mock_client.update_identity_propagation_config.assert_called_once()

def test_update_ip_restriction_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_ip_restriction
    mock_client = MagicMock()
    mock_client.update_ip_restriction.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_ip_restriction(1, ip_restriction_rule_map="test-ip_restriction_rule_map", vpc_id_restriction_rule_map="test-vpc_id_restriction_rule_map", vpc_endpoint_id_restriction_rule_map="test-vpc_endpoint_id_restriction_rule_map", enabled=True, region_name="us-east-1")
    mock_client.update_ip_restriction.assert_called_once()

def test_update_public_sharing_settings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_public_sharing_settings
    mock_client = MagicMock()
    mock_client.update_public_sharing_settings.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_public_sharing_settings(1, public_sharing_enabled="test-public_sharing_enabled", region_name="us-east-1")
    mock_client.update_public_sharing_settings.assert_called_once()

def test_update_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_template
    mock_client = MagicMock()
    mock_client.update_template.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_template(1, "test-template_id", source_entity="test-source_entity", version_description="test-version_description", name="test-name", definition={}, validation_strategy="test-validation_strategy", region_name="us-east-1")
    mock_client.update_template.assert_called_once()

def test_update_template_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_template_permissions
    mock_client = MagicMock()
    mock_client.update_template_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_template_permissions(1, "test-template_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_template_permissions.assert_called_once()

def test_update_theme_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_theme
    mock_client = MagicMock()
    mock_client.update_theme.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_theme(1, "test-theme_id", "test-base_theme_id", name="test-name", version_description="test-version_description", configuration={}, region_name="us-east-1")
    mock_client.update_theme.assert_called_once()

def test_update_theme_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_theme_permissions
    mock_client = MagicMock()
    mock_client.update_theme_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_theme_permissions(1, "test-theme_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_theme_permissions.assert_called_once()

def test_update_topic_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_topic
    mock_client = MagicMock()
    mock_client.update_topic.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_topic(1, "test-topic_id", "test-topic", custom_instructions="test-custom_instructions", region_name="us-east-1")
    mock_client.update_topic.assert_called_once()

def test_update_topic_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_topic_permissions
    mock_client = MagicMock()
    mock_client.update_topic_permissions.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_topic_permissions(1, "test-topic_id", grant_permissions="test-grant_permissions", revoke_permissions="test-revoke_permissions", region_name="us-east-1")
    mock_client.update_topic_permissions.assert_called_once()

def test_update_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_user
    mock_client = MagicMock()
    mock_client.update_user.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_user("test-user_name", 1, "test-namespace", "test-email", "test-role", custom_permissions_name="test-custom_permissions_name", unapply_custom_permissions="test-unapply_custom_permissions", external_login_federation_provider_type="test-external_login_federation_provider_type", custom_federation_provider_url="test-custom_federation_provider_url", external_login_id="test-external_login_id", region_name="us-east-1")
    mock_client.update_user.assert_called_once()

def test_update_vpc_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.quicksight import update_vpc_connection
    mock_client = MagicMock()
    mock_client.update_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.quicksight.get_client", lambda *a, **kw: mock_client)
    update_vpc_connection(1, "test-vpc_connection_id", "test-name", "test-subnet_ids", "test-security_group_ids", "test-role_arn", dns_resolvers="test-dns_resolvers", region_name="us-east-1")
    mock_client.update_vpc_connection.assert_called_once()
