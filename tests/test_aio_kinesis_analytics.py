"""Tests for aws_util.aio.kinesis_analytics module."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.kinesis_analytics import (
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

APP_NAME = "test-app"
APP_ARN = "arn:aws:kinesisanalytics:us-east-1:123456789012:application/test-app"
ROLE_ARN = "arn:aws:iam::123456789012:role/test-role"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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
# create_application
# ---------------------------------------------------------------------------


async def test_create_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_application(
        APP_NAME,
        runtime_environment="SQL-1_0",
        service_execution_role=ROLE_ARN,
    )
    assert isinstance(result, ApplicationDetail)
    assert result.application_name == APP_NAME
    assert result.application_status == "READY"


async def test_create_application_with_optionals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await create_application(
        APP_NAME,
        runtime_environment="SQL-1_0",
        service_execution_role=ROLE_ARN,
        application_configuration={"SqlConfig": {}},
        application_description="desc",
        tags=[{"Key": "env", "Value": "test"}],
        region_name="us-west-2",
    )
    assert isinstance(result, ApplicationDetail)


async def test_create_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="create_application failed"):
        await create_application(
            APP_NAME,
            runtime_environment="SQL-1_0",
            service_execution_role=ROLE_ARN,
        )


# ---------------------------------------------------------------------------
# describe_application
# ---------------------------------------------------------------------------


async def test_describe_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_application(APP_NAME)
    assert isinstance(result, ApplicationDetail)
    assert result.application_name == APP_NAME


async def test_describe_application_include_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application(
        APP_NAME, include_additional_details=True, region_name="eu-west-1"
    )
    mock_client.call.assert_called_once()


async def test_describe_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_application failed"):
        await describe_application(APP_NAME)


# ---------------------------------------------------------------------------
# list_applications
# ---------------------------------------------------------------------------


async def test_list_applications_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationSummaries": [_mock_app_summary()],
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_applications()
    assert len(result) == 1
    assert isinstance(result[0], ApplicationSummary)


async def test_list_applications_with_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationSummaries": [_mock_app_summary()],
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_applications(limit=5, region_name="us-west-2")
    mock_client.call.assert_called_once()


async def test_list_applications_pagination(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    call_count = {"n": 0}

    async def fake_call(*args: Any, **kwargs: Any) -> dict[str, Any]:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return {
                "ApplicationSummaries": [_mock_app_summary("app-1")],
                "NextToken": "tok-1",
            }
        return {
            "ApplicationSummaries": [_mock_app_summary("app-2")],
        }

    mock_client.call = fake_call
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_applications()
    assert len(result) == 2
    assert result[0].application_name == "app-1"
    assert result[1].application_name == "app-2"


async def test_list_applications_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_applications failed"):
        await list_applications()


# ---------------------------------------------------------------------------
# delete_application
# ---------------------------------------------------------------------------


async def test_delete_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application(
        APP_NAME, create_timestamp=datetime(2024, 1, 1)
    )
    mock_client.call.assert_called_once()


async def test_delete_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="delete_application failed"):
        await delete_application(
            APP_NAME, create_timestamp=datetime(2024, 1, 1)
        )


# ---------------------------------------------------------------------------
# start_application
# ---------------------------------------------------------------------------


async def test_start_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_application(APP_NAME)
    mock_client.call.assert_called_once()


async def test_start_application_with_run_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_application(
        APP_NAME,
        run_configuration={"SqlRunConfigurations": []},
        region_name="us-west-2",
    )
    mock_client.call.assert_called_once()


async def test_start_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="start_application failed"):
        await start_application(APP_NAME)


# ---------------------------------------------------------------------------
# stop_application
# ---------------------------------------------------------------------------


async def test_stop_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_application(APP_NAME)
    mock_client.call.assert_called_once()


async def test_stop_application_force(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_application(APP_NAME, force=True, region_name="eu-west-1")
    mock_client.call.assert_called_once()


async def test_stop_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="stop_application failed"):
        await stop_application(APP_NAME)


# ---------------------------------------------------------------------------
# add_application_input
# ---------------------------------------------------------------------------


async def test_add_application_input_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationARN": APP_ARN,
        "ApplicationVersionId": 2,
        "InputDescriptions": [{"InputId": "1.1"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await add_application_input(
        APP_NAME,
        current_application_version_id=1,
        input_config={"NamePrefix": "src"},
    )
    assert isinstance(result, ApplicationInputResult)
    assert result.application_arn == APP_ARN
    assert result.application_version_id == 2
    assert len(result.input_descriptions) == 1


async def test_add_application_input_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="add_application_input failed"):
        await add_application_input(
            APP_NAME,
            current_application_version_id=1,
            input_config={},
        )


# ---------------------------------------------------------------------------
# add_application_output
# ---------------------------------------------------------------------------


async def test_add_application_output_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationARN": APP_ARN,
        "ApplicationVersionId": 3,
        "OutputDescriptions": [{"OutputId": "2.1"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await add_application_output(
        APP_NAME,
        current_application_version_id=2,
        output_config={"Name": "dest"},
    )
    assert isinstance(result, ApplicationOutputResult)
    assert result.application_arn == APP_ARN
    assert result.application_version_id == 3
    assert len(result.output_descriptions) == 1


async def test_add_application_output_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="add_application_output failed"):
        await add_application_output(
            APP_NAME,
            current_application_version_id=1,
            output_config={},
        )


# ---------------------------------------------------------------------------
# update_application
# ---------------------------------------------------------------------------


async def test_update_application_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(version=2),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await update_application(
        APP_NAME, current_application_version_id=1
    )
    assert isinstance(result, ApplicationDetail)
    assert result.application_version_id == 2


async def test_update_application_with_optionals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ApplicationDetail": _mock_app_detail(version=2),
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application(
        APP_NAME,
        current_application_version_id=1,
        application_configuration_update={"SqlUpdate": {}},
        service_execution_role_update="arn:aws:iam::123:role/new-role",
        run_configuration_update={"FlinkRunConfig": {}},
        region_name="us-west-2",
    )
    mock_client.call.assert_called_once()


async def test_update_application_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="update_application failed"):
        await update_application(
            APP_NAME, current_application_version_id=1
        )


async def test_add_application_cloud_watch_logging_option(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_application_cloud_watch_logging_option("test-application_name", {}, )
    mock_client.call.assert_called_once()


async def test_add_application_cloud_watch_logging_option_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_application_cloud_watch_logging_option("test-application_name", {}, )


async def test_add_application_input_processing_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_application_input_processing_configuration("test-application_name", 1, "test-input_id", {}, )
    mock_client.call.assert_called_once()


async def test_add_application_input_processing_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_application_input_processing_configuration("test-application_name", 1, "test-input_id", {}, )


async def test_add_application_reference_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_application_reference_data_source("test-application_name", 1, {}, )
    mock_client.call.assert_called_once()


async def test_add_application_reference_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_application_reference_data_source("test-application_name", 1, {}, )


async def test_add_application_vpc_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_application_vpc_configuration("test-application_name", {}, )
    mock_client.call.assert_called_once()


async def test_add_application_vpc_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_application_vpc_configuration("test-application_name", {}, )


async def test_create_application_presigned_url(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_application_presigned_url("test-application_name", "test-url_type", )
    mock_client.call.assert_called_once()


async def test_create_application_presigned_url_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_application_presigned_url("test-application_name", "test-url_type", )


async def test_create_application_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_application_snapshot("test-application_name", "test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_create_application_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_application_snapshot("test-application_name", "test-snapshot_name", )


async def test_delete_application_cloud_watch_logging_option(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", )
    mock_client.call.assert_called_once()


async def test_delete_application_cloud_watch_logging_option_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", )


async def test_delete_application_input_processing_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_input_processing_configuration("test-application_name", 1, "test-input_id", )
    mock_client.call.assert_called_once()


async def test_delete_application_input_processing_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_input_processing_configuration("test-application_name", 1, "test-input_id", )


async def test_delete_application_output(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_output("test-application_name", 1, "test-output_id", )
    mock_client.call.assert_called_once()


async def test_delete_application_output_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_output("test-application_name", 1, "test-output_id", )


async def test_delete_application_reference_data_source(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_reference_data_source("test-application_name", 1, "test-reference_id", )
    mock_client.call.assert_called_once()


async def test_delete_application_reference_data_source_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_reference_data_source("test-application_name", 1, "test-reference_id", )


async def test_delete_application_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_snapshot("test-application_name", "test-snapshot_name", "test-snapshot_creation_timestamp", )
    mock_client.call.assert_called_once()


async def test_delete_application_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_snapshot("test-application_name", "test-snapshot_name", "test-snapshot_creation_timestamp", )


async def test_delete_application_vpc_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_vpc_configuration("test-application_name", "test-vpc_configuration_id", )
    mock_client.call.assert_called_once()


async def test_delete_application_vpc_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_vpc_configuration("test-application_name", "test-vpc_configuration_id", )


async def test_describe_application_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application_operation("test-application_name", "test-operation_id", )
    mock_client.call.assert_called_once()


async def test_describe_application_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_operation("test-application_name", "test-operation_id", )


async def test_describe_application_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application_snapshot("test-application_name", "test-snapshot_name", )
    mock_client.call.assert_called_once()


async def test_describe_application_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_snapshot("test-application_name", "test-snapshot_name", )


async def test_describe_application_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application_version("test-application_name", 1, )
    mock_client.call.assert_called_once()


async def test_describe_application_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_version("test-application_name", 1, )


async def test_discover_input_schema(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await discover_input_schema("test-service_execution_role", )
    mock_client.call.assert_called_once()


async def test_discover_input_schema_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await discover_input_schema("test-service_execution_role", )


async def test_list_application_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_operations("test-application_name", )
    mock_client.call.assert_called_once()


async def test_list_application_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_operations("test-application_name", )


async def test_list_application_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_snapshots("test-application_name", )
    mock_client.call.assert_called_once()


async def test_list_application_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_snapshots("test-application_name", )


async def test_list_application_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_versions("test-application_name", )
    mock_client.call.assert_called_once()


async def test_list_application_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_versions("test-application_name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_rollback_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await rollback_application("test-application_name", 1, )
    mock_client.call.assert_called_once()


async def test_rollback_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rollback_application("test-application_name", 1, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_application_maintenance_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application_maintenance_configuration("test-application_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_application_maintenance_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis_analytics.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application_maintenance_configuration("test-application_name", {}, )


@pytest.mark.asyncio
async def test_list_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import list_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await list_applications(limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import start_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await start_application("test-application_name", run_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_add_application_cloud_watch_logging_option_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import add_application_cloud_watch_logging_option
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await add_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option", current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_add_application_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import add_application_vpc_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await add_application_vpc_configuration("test-application_name", {}, current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_application_presigned_url_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import create_application_presigned_url
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await create_application_presigned_url("test-application_name", "test-url_type", session_expiration_duration_in_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_application_cloud_watch_logging_option_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import delete_application_cloud_watch_logging_option
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await delete_application_cloud_watch_logging_option("test-application_name", "test-cloud_watch_logging_option_id", current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_application_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import delete_application_vpc_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await delete_application_vpc_configuration("test-application_name", {}, current_application_version_id="test-current_application_version_id", conditional_token="test-conditional_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_discover_input_schema_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import discover_input_schema
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await discover_input_schema("test-service_execution_role", resource_arn="test-resource_arn", input_starting_position_configuration={}, s3_configuration={}, input_processing_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import list_application_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await list_application_operations("test-application_name", limit=1, next_token="test-next_token", operation="test-operation", operation_status="test-operation_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import list_application_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await list_application_snapshots("test-application_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis_analytics import list_application_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis_analytics.async_client", lambda *a, **kw: mock_client)
    await list_application_versions("test-application_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
