"""Tests for aws_util.kinesis_analytics module."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.kinesis_analytics as ka_mod
from aws_util.kinesis_analytics import (
    ApplicationDetail,
    ApplicationInputResult,
    ApplicationOutputResult,
    ApplicationSummary,
    add_application_input,
    add_application_output,
    create_application,
    delete_application,
    describe_application,
    list_applications,
    start_application,
    stop_application,
    update_application,
    add_application_cloud_watch_logging_option,
    add_application_input_processing_configuration,
    add_application_reference_data_source,
    add_application_vpc_configuration,
    create_application_presigned_url,
    create_application_snapshot,
    delete_application_cloud_watch_logging_option,
    delete_application_input_processing_configuration,
    delete_application_output,
    delete_application_reference_data_source,
    delete_application_snapshot,
    delete_application_vpc_configuration,
    describe_application_operation,
    describe_application_snapshot,
    describe_application_version,
    discover_input_schema,
    list_application_operations,
    list_application_snapshots,
    list_application_versions,
    list_tags_for_resource,
    rollback_application,
    tag_resource,
    untag_resource,
    update_application_maintenance_configuration,
)

REGION = "us-east-1"
APP_NAME = "test-app"
APP_ARN = "arn:aws:kinesisanalytics:us-east-1:123456789012:application/test-app"
ROLE_ARN = "arn:aws:iam::123456789012:role/test-role"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str = "ResourceNotFoundException", msg: str = "not found") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "Operation"
    )


def _mock_app_detail(
    name: str = APP_NAME,
    arn: str = APP_ARN,
    status: str = "READY",
    version: int = 1,
) -> dict[str, Any]:
    return {
        "ApplicationName": name,
        "ApplicationARN": arn,
        "ApplicationStatus": status,
        "ApplicationVersionId": version,
        "RuntimeEnvironment": "SQL-1_0",
        "ServiceExecutionRole": ROLE_ARN,
        "CreateTimestamp": datetime(2024, 1, 1),
        "LastUpdateTimestamp": datetime(2024, 1, 2),
        "ApplicationDescription": "A test app",
        "ApplicationConfigurationDescription": {"SqlConfig": {}},
    }


def _mock_app_summary(
    name: str = APP_NAME,
    arn: str = APP_ARN,
    status: str = "READY",
) -> dict[str, Any]:
    return {
        "ApplicationName": name,
        "ApplicationARN": arn,
        "ApplicationStatus": status,
        "ApplicationVersionId": 1,
        "RuntimeEnvironment": "SQL-1_0",
    }


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_application_summary_model() -> None:
    s = ApplicationSummary(
        application_name=APP_NAME,
        application_arn=APP_ARN,
        application_status="READY",
    )
    assert s.application_name == APP_NAME
    assert s.application_version_id is None
    assert s.runtime_environment is None


def test_application_detail_model() -> None:
    d = ApplicationDetail(
        application_name=APP_NAME,
        application_arn=APP_ARN,
        application_status="RUNNING",
        application_version_id=3,
    )
    assert d.application_name == APP_NAME
    assert d.application_version_id == 3
    assert d.application_description is None
    assert d.extra == {}


def test_application_input_result_model() -> None:
    r = ApplicationInputResult(
        application_arn=APP_ARN,
        application_version_id=2,
    )
    assert r.application_arn == APP_ARN
    assert r.input_descriptions == []


def test_application_output_result_model() -> None:
    r = ApplicationOutputResult(
        application_arn=APP_ARN,
        application_version_id=2,
    )
    assert r.application_arn == APP_ARN
    assert r.output_descriptions == []


# ---------------------------------------------------------------------------
# create_application
# ---------------------------------------------------------------------------


def test_create_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.create_application.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_application(
        APP_NAME,
        runtime_environment="SQL-1_0",
        service_execution_role=ROLE_ARN,
        region_name=REGION,
    )
    assert isinstance(result, ApplicationDetail)
    assert result.application_name == APP_NAME
    assert result.application_status == "READY"
    assert result.runtime_environment == "SQL-1_0"


def test_create_application_with_optionals(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.create_application.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = create_application(
        APP_NAME,
        runtime_environment="SQL-1_0",
        service_execution_role=ROLE_ARN,
        application_configuration={"SqlConfig": {}},
        application_description="desc",
        tags=[{"Key": "env", "Value": "test"}],
        region_name=REGION,
    )
    assert isinstance(result, ApplicationDetail)
    call_kwargs = mock_client.create_application.call_args[1]
    assert call_kwargs["ApplicationConfiguration"] == {"SqlConfig": {}}
    assert call_kwargs["ApplicationDescription"] == "desc"
    assert call_kwargs["Tags"] == [{"Key": "env", "Value": "test"}]


def test_create_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.create_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="create_application failed"):
        create_application(
            APP_NAME,
            runtime_environment="SQL-1_0",
            service_execution_role=ROLE_ARN,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# describe_application
# ---------------------------------------------------------------------------


def test_describe_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.describe_application.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_application(APP_NAME, region_name=REGION)
    assert isinstance(result, ApplicationDetail)
    assert result.application_name == APP_NAME
    assert result.application_description == "A test app"


def test_describe_application_include_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.describe_application.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    describe_application(
        APP_NAME, include_additional_details=True, region_name=REGION
    )
    call_kwargs = mock_client.describe_application.call_args[1]
    assert call_kwargs["IncludeAdditionalDetails"] is True


def test_describe_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.describe_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_application failed"):
        describe_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# list_applications
# ---------------------------------------------------------------------------


def test_list_applications_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.list_applications.return_value = {
        "ApplicationSummaries": [_mock_app_summary()],
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_applications(region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0], ApplicationSummary)
    assert result[0].application_name == APP_NAME


def test_list_applications_with_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.list_applications.return_value = {
        "ApplicationSummaries": [_mock_app_summary()],
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    list_applications(limit=10, region_name=REGION)
    call_kwargs = mock_client.list_applications.call_args[1]
    assert call_kwargs["Limit"] == 10


def test_list_applications_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    call_count = {"n": 0}

    def fake_list(**kwargs: Any) -> dict[str, Any]:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return {
                "ApplicationSummaries": [_mock_app_summary("app-1", APP_ARN)],
                "NextToken": "token-1",
            }
        return {
            "ApplicationSummaries": [_mock_app_summary("app-2", APP_ARN)],
        }

    mock_client.list_applications.side_effect = fake_list
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_applications(region_name=REGION)
    assert len(result) == 2
    assert result[0].application_name == "app-1"
    assert result[1].application_name == "app-2"


def test_list_applications_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.list_applications.side_effect = _client_error("AccessDenied")
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_applications failed"):
        list_applications(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_application
# ---------------------------------------------------------------------------


def test_delete_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.delete_application.return_value = {}
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    delete_application(
        APP_NAME, create_timestamp=datetime(2024, 1, 1), region_name=REGION
    )
    mock_client.delete_application.assert_called_once()


def test_delete_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.delete_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="delete_application failed"):
        delete_application(
            APP_NAME, create_timestamp=datetime(2024, 1, 1), region_name=REGION
        )


# ---------------------------------------------------------------------------
# start_application
# ---------------------------------------------------------------------------


def test_start_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.start_application.return_value = {}
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    start_application(APP_NAME, region_name=REGION)
    mock_client.start_application.assert_called_once()


def test_start_application_with_run_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.start_application.return_value = {}
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    run_config = {"SqlRunConfigurations": []}
    start_application(
        APP_NAME, run_configuration=run_config, region_name=REGION
    )
    call_kwargs = mock_client.start_application.call_args[1]
    assert call_kwargs["RunConfiguration"] == run_config


def test_start_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.start_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="start_application failed"):
        start_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# stop_application
# ---------------------------------------------------------------------------


def test_stop_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.stop_application.return_value = {}
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    stop_application(APP_NAME, region_name=REGION)
    mock_client.stop_application.assert_called_once()


def test_stop_application_force(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.stop_application.return_value = {}
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    stop_application(APP_NAME, force=True, region_name=REGION)
    call_kwargs = mock_client.stop_application.call_args[1]
    assert call_kwargs["Force"] is True


def test_stop_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.stop_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="stop_application failed"):
        stop_application(APP_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# add_application_input
# ---------------------------------------------------------------------------


def test_add_application_input_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.add_application_input.return_value = {
        "ApplicationARN": APP_ARN,
        "ApplicationVersionId": 2,
        "InputDescriptions": [{"InputId": "1.1"}],
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = add_application_input(
        APP_NAME,
        current_application_version_id=1,
        input_config={"NamePrefix": "src", "InputSchema": {}},
        region_name=REGION,
    )
    assert isinstance(result, ApplicationInputResult)
    assert result.application_arn == APP_ARN
    assert result.application_version_id == 2
    assert len(result.input_descriptions) == 1


def test_add_application_input_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.add_application_input.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="add_application_input failed"):
        add_application_input(
            APP_NAME,
            current_application_version_id=1,
            input_config={},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# add_application_output
# ---------------------------------------------------------------------------


def test_add_application_output_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.add_application_output.return_value = {
        "ApplicationARN": APP_ARN,
        "ApplicationVersionId": 3,
        "OutputDescriptions": [{"OutputId": "2.1"}],
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = add_application_output(
        APP_NAME,
        current_application_version_id=2,
        output_config={"Name": "dest", "DestinationSchema": {}},
        region_name=REGION,
    )
    assert isinstance(result, ApplicationOutputResult)
    assert result.application_arn == APP_ARN
    assert result.application_version_id == 3
    assert len(result.output_descriptions) == 1


def test_add_application_output_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.add_application_output.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="add_application_output failed"):
        add_application_output(
            APP_NAME,
            current_application_version_id=1,
            output_config={},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# update_application
# ---------------------------------------------------------------------------


def test_update_application_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.update_application.return_value = {
        "ApplicationDetail": _mock_app_detail(version=2),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = update_application(
        APP_NAME,
        current_application_version_id=1,
        region_name=REGION,
    )
    assert isinstance(result, ApplicationDetail)
    assert result.application_version_id == 2


def test_update_application_with_optionals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = MagicMock()
    mock_client.update_application.return_value = {
        "ApplicationDetail": _mock_app_detail(version=2),
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    update_application(
        APP_NAME,
        current_application_version_id=1,
        application_configuration_update={"SqlUpdate": {}},
        service_execution_role_update="arn:aws:iam::123:role/new-role",
        run_configuration_update={"FlinkRunConfig": {}},
        region_name=REGION,
    )
    call_kwargs = mock_client.update_application.call_args[1]
    assert call_kwargs["ApplicationConfigurationUpdate"] == {"SqlUpdate": {}}
    assert call_kwargs["ServiceExecutionRoleUpdate"] == (
        "arn:aws:iam::123:role/new-role"
    )
    assert call_kwargs["RunConfigurationUpdate"] == {"FlinkRunConfig": {}}


def test_update_application_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = MagicMock()
    mock_client.update_application.side_effect = _client_error()
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="update_application failed"):
        update_application(
            APP_NAME,
            current_application_version_id=1,
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# _parse_detail edge cases
# ---------------------------------------------------------------------------


def test_parse_detail_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test _parse_detail with minimal data and extra keys."""
    mock_client = MagicMock()
    mock_client.describe_application.return_value = {
        "ApplicationDetail": {
            "ApplicationName": APP_NAME,
            "ApplicationARN": APP_ARN,
            "UnknownExtraKey": "extra-value",
        },
    }
    monkeypatch.setattr(ka_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_application(APP_NAME, region_name=REGION)
    assert result.application_status == "UNKNOWN"
    assert result.application_version_id == 0
    assert result.application_description is None
    assert result.runtime_environment is None
    assert result.service_execution_role is None
    assert result.create_timestamp is None
    assert result.last_update_timestamp is None
    assert result.application_configuration_description is None
    assert result.extra == {"UnknownExtraKey": "extra-value"}


def test_parse_summary_defaults() -> None:
    """Test _parse_summary with minimal data."""
    summary = ka_mod._parse_summary({
        "ApplicationName": "min-app",
        "ApplicationARN": "arn:min",
    })
    assert summary.application_status == "UNKNOWN"
    assert summary.application_version_id is None
    assert summary.runtime_environment is None


def test_add_application_cloud_watch_logging_option(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_cloud_watch_logging_option.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_cloud_watch_logging_option("test-application_name", {}, region_name=REGION)
    mock_client.add_application_cloud_watch_logging_option.assert_called_once()


def test_add_application_cloud_watch_logging_option_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_cloud_watch_logging_option.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_application_cloud_watch_logging_option",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add application cloud watch logging option"):
        add_application_cloud_watch_logging_option("test-application_name", {}, region_name=REGION)


def test_add_application_input_processing_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_input_processing_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_input_processing_configuration("test-application_name", 1, "test-input_id", {}, region_name=REGION)
    mock_client.add_application_input_processing_configuration.assert_called_once()


def test_add_application_input_processing_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_input_processing_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_application_input_processing_configuration",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add application input processing configuration"):
        add_application_input_processing_configuration("test-application_name", 1, "test-input_id", {}, region_name=REGION)


def test_add_application_reference_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_reference_data_source.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_reference_data_source("test-application_name", 1, {}, region_name=REGION)
    mock_client.add_application_reference_data_source.assert_called_once()


def test_add_application_reference_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_reference_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_application_reference_data_source",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add application reference data source"):
        add_application_reference_data_source("test-application_name", 1, {}, region_name=REGION)


def test_add_application_vpc_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_vpc_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_vpc_configuration("test-application_name", {}, region_name=REGION)
    mock_client.add_application_vpc_configuration.assert_called_once()


def test_add_application_vpc_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_application_vpc_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_application_vpc_configuration",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add application vpc configuration"):
        add_application_vpc_configuration("test-application_name", {}, region_name=REGION)


def test_create_application_presigned_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_presigned_url.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    create_application_presigned_url("test-application_name", "test-url_type", region_name=REGION)
    mock_client.create_application_presigned_url.assert_called_once()


def test_create_application_presigned_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_presigned_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_application_presigned_url",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create application presigned url"):
        create_application_presigned_url("test-application_name", "test-url_type", region_name=REGION)


def test_create_application_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    create_application_snapshot("test-application_name", "test-snapshot_name", region_name=REGION)
    mock_client.create_application_snapshot.assert_called_once()


def test_create_application_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_application_snapshot",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create application snapshot"):
        create_application_snapshot("test-application_name", "test-snapshot_name", region_name=REGION)


def test_delete_application_cloud_watch_logging_option(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_cloud_watch_logging_option.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", region_name=REGION)
    mock_client.delete_application_cloud_watch_logging_option.assert_called_once()


def test_delete_application_cloud_watch_logging_option_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_cloud_watch_logging_option.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_cloud_watch_logging_option",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application cloud watch logging option"):
        delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", region_name=REGION)


def test_delete_application_input_processing_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_input_processing_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_input_processing_configuration("test-application_name", 1, "test-input_id", region_name=REGION)
    mock_client.delete_application_input_processing_configuration.assert_called_once()


def test_delete_application_input_processing_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_input_processing_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_input_processing_configuration",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application input processing configuration"):
        delete_application_input_processing_configuration("test-application_name", 1, "test-input_id", region_name=REGION)


def test_delete_application_output(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_output.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_output("test-application_name", 1, "test-output_id", region_name=REGION)
    mock_client.delete_application_output.assert_called_once()


def test_delete_application_output_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_output.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_output",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application output"):
        delete_application_output("test-application_name", 1, "test-output_id", region_name=REGION)


def test_delete_application_reference_data_source(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_reference_data_source.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_reference_data_source("test-application_name", 1, "test-reference_id", region_name=REGION)
    mock_client.delete_application_reference_data_source.assert_called_once()


def test_delete_application_reference_data_source_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_reference_data_source.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_reference_data_source",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application reference data source"):
        delete_application_reference_data_source("test-application_name", 1, "test-reference_id", region_name=REGION)


def test_delete_application_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_snapshot("test-application_name", "test-snapshot_name", "test-snapshot_creation_timestamp", region_name=REGION)
    mock_client.delete_application_snapshot.assert_called_once()


def test_delete_application_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_snapshot",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application snapshot"):
        delete_application_snapshot("test-application_name", "test-snapshot_name", "test-snapshot_creation_timestamp", region_name=REGION)


def test_delete_application_vpc_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_vpc_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_vpc_configuration("test-application_name", "test-vpc_configuration_id", region_name=REGION)
    mock_client.delete_application_vpc_configuration.assert_called_once()


def test_delete_application_vpc_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_vpc_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_vpc_configuration",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application vpc configuration"):
        delete_application_vpc_configuration("test-application_name", "test-vpc_configuration_id", region_name=REGION)


def test_describe_application_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_operation.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    describe_application_operation("test-application_name", "test-operation_id", region_name=REGION)
    mock_client.describe_application_operation.assert_called_once()


def test_describe_application_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application_operation",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application operation"):
        describe_application_operation("test-application_name", "test-operation_id", region_name=REGION)


def test_describe_application_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    describe_application_snapshot("test-application_name", "test-snapshot_name", region_name=REGION)
    mock_client.describe_application_snapshot.assert_called_once()


def test_describe_application_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application_snapshot",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application snapshot"):
        describe_application_snapshot("test-application_name", "test-snapshot_name", region_name=REGION)


def test_describe_application_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_version.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    describe_application_version("test-application_name", 1, region_name=REGION)
    mock_client.describe_application_version.assert_called_once()


def test_describe_application_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application_version",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application version"):
        describe_application_version("test-application_name", 1, region_name=REGION)


def test_discover_input_schema(monkeypatch):
    mock_client = MagicMock()
    mock_client.discover_input_schema.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    discover_input_schema("test-service_execution_role", region_name=REGION)
    mock_client.discover_input_schema.assert_called_once()


def test_discover_input_schema_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.discover_input_schema.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "discover_input_schema",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to discover input schema"):
        discover_input_schema("test-service_execution_role", region_name=REGION)


def test_list_application_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_operations.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_operations("test-application_name", region_name=REGION)
    mock_client.list_application_operations.assert_called_once()


def test_list_application_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_operations",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application operations"):
        list_application_operations("test-application_name", region_name=REGION)


def test_list_application_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_snapshots("test-application_name", region_name=REGION)
    mock_client.list_application_snapshots.assert_called_once()


def test_list_application_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_snapshots",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application snapshots"):
        list_application_snapshots("test-application_name", region_name=REGION)


def test_list_application_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_versions.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_versions("test-application_name", region_name=REGION)
    mock_client.list_application_versions.assert_called_once()


def test_list_application_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_versions",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application versions"):
        list_application_versions("test-application_name", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_rollback_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_application.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    rollback_application("test-application_name", 1, region_name=REGION)
    mock_client.rollback_application.assert_called_once()


def test_rollback_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rollback_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rollback_application",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rollback application"):
        rollback_application("test-application_name", 1, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_application_maintenance_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application_maintenance_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    update_application_maintenance_configuration("test-application_name", {}, region_name=REGION)
    mock_client.update_application_maintenance_configuration.assert_called_once()


def test_update_application_maintenance_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application_maintenance_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application_maintenance_configuration",
    )
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update application maintenance configuration"):
        update_application_maintenance_configuration("test-application_name", {}, region_name=REGION)


def test_list_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import list_applications
    mock_client = MagicMock()
    mock_client.list_applications.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_applications(limit=1, region_name="us-east-1")
    mock_client.list_applications.assert_called_once()

def test_start_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import start_application
    mock_client = MagicMock()
    mock_client.start_application.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    start_application("test-application_name", run_configuration={}, region_name="us-east-1")
    mock_client.start_application.assert_called_once()

def test_add_application_cloud_watch_logging_option_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import add_application_cloud_watch_logging_option
    mock_client = MagicMock()
    mock_client.add_application_cloud_watch_logging_option.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option", current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.add_application_cloud_watch_logging_option.assert_called_once()

def test_add_application_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import add_application_vpc_configuration
    mock_client = MagicMock()
    mock_client.add_application_vpc_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    add_application_vpc_configuration("test-application_name", {}, current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.add_application_vpc_configuration.assert_called_once()

def test_create_application_presigned_url_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import create_application_presigned_url
    mock_client = MagicMock()
    mock_client.create_application_presigned_url.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    create_application_presigned_url("test-application_name", "test-url_type", session_expiration_duration_in_seconds=1, region_name="us-east-1")
    mock_client.create_application_presigned_url.assert_called_once()

def test_delete_application_cloud_watch_logging_option_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import delete_application_cloud_watch_logging_option
    mock_client = MagicMock()
    mock_client.delete_application_cloud_watch_logging_option.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.delete_application_cloud_watch_logging_option.assert_called_once()

def test_delete_application_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import delete_application_vpc_configuration
    mock_client = MagicMock()
    mock_client.delete_application_vpc_configuration.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    delete_application_vpc_configuration("test-application_name", {}, current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.delete_application_vpc_configuration.assert_called_once()

def test_discover_input_schema_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import discover_input_schema
    mock_client = MagicMock()
    mock_client.discover_input_schema.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    discover_input_schema("test-service_execution_role", resource_arn="test-resource_arn", input_starting_position_configuration={}, s3_configuration={}, input_processing_configuration={}, region_name="us-east-1")
    mock_client.discover_input_schema.assert_called_once()

def test_list_application_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import list_application_operations
    mock_client = MagicMock()
    mock_client.list_application_operations.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_operations("test-application_name", limit=1, next_token="test-next_token", operation="test-operation", operation_status="test-operation_status", region_name="us-east-1")
    mock_client.list_application_operations.assert_called_once()

def test_list_application_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import list_application_snapshots
    mock_client = MagicMock()
    mock_client.list_application_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_snapshots("test-application_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_snapshots.assert_called_once()

def test_list_application_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis_analytics import list_application_versions
    mock_client = MagicMock()
    mock_client.list_application_versions.return_value = {}
    monkeypatch.setattr("aws_util.kinesis_analytics.get_client", lambda *a, **kw: mock_client)
    list_application_versions("test-application_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_versions.assert_called_once()
