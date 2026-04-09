"""Tests for aws_util.aio.cloudtrail — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.cloudtrail import (
    EventDataStoreResult,
    EventSelectorResult,
    InsightSelectorResult,
    LookupEvent,
    QueryResult,
    TrailResult,
    TrailStatus,
    TrailSummary,
    create_event_data_store,
    create_trail,
    delete_event_data_store,
    delete_trail,
    describe_event_data_store,
    describe_trails,
    get_event_selectors,
    get_insight_selectors,
    get_query_results,
    get_trail,
    get_trail_status,
    list_event_data_stores,
    list_queries,
    list_trails,
    lookup_events,
    put_event_selectors,
    put_insight_selectors,
    start_logging,
    start_query,
    stop_logging,
    update_trail,
    add_tags,
    cancel_query,
    create_channel,
    create_dashboard,
    delete_channel,
    delete_dashboard,
    delete_resource_policy,
    deregister_organization_delegated_admin,
    describe_query,
    disable_federation,
    enable_federation,
    generate_query,
    get_channel,
    get_dashboard,
    get_event_configuration,
    get_event_data_store,
    get_import,
    get_resource_policy,
    list_channels,
    list_dashboards,
    list_import_failures,
    list_imports,
    list_insights_metric_data,
    list_public_keys,
    list_tags,
    put_event_configuration,
    put_resource_policy,
    register_organization_delegated_admin,
    remove_tags,
    restore_event_data_store,
    search_sample_queries,
    start_dashboard_refresh,
    start_event_data_store_ingestion,
    start_import,
    stop_event_data_store_ingestion,
    stop_import,
    update_channel,
    update_dashboard,
    update_event_data_store,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _trail_dict(
    name: str = "my-trail",
    arn: str = "arn:aws:cloudtrail:us-east-1:123456789012:"
    "trail/my-trail",
) -> dict:
    return {
        "Name": name,
        "TrailARN": arn,
        "S3BucketName": "my-bucket",
        "S3KeyPrefix": "logs",
        "SnsTopicARN": "arn:aws:sns:us-east-1:123:topic",
        "IncludeGlobalServiceEvents": True,
        "IsMultiRegionTrail": True,
        "HomeRegion": "us-east-1",
        "LogFileValidationEnabled": True,
        "CloudWatchLogsLogGroupArn": "arn:aws:logs:us-east-1:123:lg",
        "CloudWatchLogsRoleArn": "arn:aws:iam::123:role/ct",
        "KmsKeyId": "arn:aws:kms:us-east-1:123:key/abc",
        "IsOrganizationTrail": False,
        "HasCustomEventSelectors": True,
    }


def _status_dict() -> dict:
    return {
        "IsLogging": True,
        "LatestDeliveryTime": "2024-01-01T00:00:00Z",
        "LatestNotificationTime": "2024-01-01T00:00:00Z",
        "LatestCloudWatchLogsDeliveryTime": "2024-01-01",
        "StartLoggingTime": "2024-01-01T00:00:00Z",
        "StopLoggingTime": None,
        "LatestDeliveryError": None,
        "LatestNotificationError": None,
        "LatestDigestDeliveryTime": "2024-01-01T00:00:00Z",
        "TimeLoggingStarted": "2024-01-01",
    }


def _event_dict(event_id: str = "evt-1") -> dict:
    return {
        "EventId": event_id,
        "EventName": "CreateBucket",
        "EventSource": "s3.amazonaws.com",
        "EventTime": "2024-01-01T00:00:00Z",
        "Username": "admin",
        "CloudTrailEvent": '{"key": "value"}',
        "Resources": [{"ResourceType": "AWS::S3::Bucket"}],
        "AccessKeyId": "AKIA123",
    }


def _eds_dict(
    arn: str = "arn:aws:cloudtrail:us-east-1:123:eventdatastore/abc",
    name: str = "my-eds",
) -> dict:
    return {
        "EventDataStoreArn": arn,
        "Name": name,
        "Status": "ENABLED",
        "RetentionPeriod": 2557,
        "MultiRegionEnabled": True,
        "OrganizationEnabled": False,
        "CreatedTimestamp": "2024-01-01T00:00:00Z",
        "UpdatedTimestamp": "2024-01-01T00:00:00Z",
        "AdvancedEventSelectors": [],
        "BillingMode": "FIXED_RETENTION_PRICING",
    }


# ---------------------------------------------------------------------------
# create_trail
# ---------------------------------------------------------------------------


async def test_create_trail_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _trail_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await create_trail(
        "my-trail", s3_bucket_name="my-bucket"
    )
    assert isinstance(result, TrailResult)
    assert result.name == "my-trail"


async def test_create_trail_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _trail_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await create_trail(
        "my-trail",
        s3_bucket_name="b",
        s3_key_prefix="logs",
        sns_topic_name="topic",
        include_global_service_events=True,
        is_multi_region_trail=True,
        enable_log_file_validation=True,
        cloud_watch_logs_log_group_arn="arn:lg",
        cloud_watch_logs_role_arn="arn:role",
        kms_key_id="arn:key",
        is_organization_trail=True,
        tags=[{"Key": "env", "Value": "prod"}],
        region_name="us-east-1",
    )
    assert result.name == "my-trail"
    kw = mock_client.call.call_args[1]
    assert "S3KeyPrefix" in kw
    assert "SnsTopicName" in kw
    assert "CloudWatchLogsLogGroupArn" in kw
    assert "CloudWatchLogsRoleArn" in kw
    assert "KmsKeyId" in kw
    assert "TagsList" in kw


async def test_create_trail_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="denied"):
        await create_trail("x", s3_bucket_name="b")


async def test_create_trail_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="create_trail failed"
    ):
        await create_trail("x", s3_bucket_name="b")


# ---------------------------------------------------------------------------
# describe_trails
# ---------------------------------------------------------------------------


async def test_describe_trails_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "trailList": [_trail_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_trails()
    assert len(result) == 1
    assert result[0].name == "my-trail"


async def test_describe_trails_with_names(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "trailList": [_trail_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_trails(
        trail_name_list=["my-trail"],
        include_shadow_trails=False,
        region_name="us-east-1",
    )
    assert len(result) == 1
    kw = mock_client.call.call_args[1]
    assert "trailNameList" in kw


async def test_describe_trails_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"trailList": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_trails()
    assert result == []


async def test_describe_trails_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await describe_trails()


async def test_describe_trails_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_trails failed"
    ):
        await describe_trails()


# ---------------------------------------------------------------------------
# get_trail
# ---------------------------------------------------------------------------


async def test_get_trail_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Trail": _trail_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await get_trail("my-trail")
    assert result.name == "my-trail"


async def test_get_trail_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("not found")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="not found"):
        await get_trail("missing", region_name="us-east-1")


async def test_get_trail_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="get_trail failed"
    ):
        await get_trail("x")


# ---------------------------------------------------------------------------
# update_trail
# ---------------------------------------------------------------------------


async def test_update_trail_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _trail_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await update_trail("my-trail")
    assert result.name == "my-trail"


async def test_update_trail_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _trail_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await update_trail(
        "my-trail",
        s3_bucket_name="new-bucket",
        s3_key_prefix="new-prefix",
        sns_topic_name="new-topic",
        include_global_service_events=False,
        is_multi_region_trail=True,
        enable_log_file_validation=True,
        cloud_watch_logs_log_group_arn="arn:lg2",
        cloud_watch_logs_role_arn="arn:role2",
        kms_key_id="arn:key2",
        is_organization_trail=True,
        region_name="us-east-1",
    )
    assert result.name == "my-trail"
    kw = mock_client.call.call_args[1]
    assert kw["S3BucketName"] == "new-bucket"
    assert kw["S3KeyPrefix"] == "new-prefix"
    assert kw["SnsTopicName"] == "new-topic"
    assert kw["IncludeGlobalServiceEvents"] is False
    assert kw["IsMultiRegionTrail"] is True
    assert kw["EnableLogFileValidation"] is True
    assert kw["CloudWatchLogsLogGroupArn"] == "arn:lg2"
    assert kw["CloudWatchLogsRoleArn"] == "arn:role2"
    assert kw["KmsKeyId"] == "arn:key2"
    assert kw["IsOrganizationTrail"] is True


async def test_update_trail_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_trail("x")


async def test_update_trail_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="update_trail failed"
    ):
        await update_trail("x")


# ---------------------------------------------------------------------------
# delete_trail
# ---------------------------------------------------------------------------


async def test_delete_trail_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    await delete_trail("my-trail")
    mock_client.call.assert_awaited_once()


async def test_delete_trail_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_trail("x", region_name="us-east-1")


async def test_delete_trail_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="delete_trail failed"
    ):
        await delete_trail("x")


# ---------------------------------------------------------------------------
# start_logging
# ---------------------------------------------------------------------------


async def test_start_logging_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    await start_logging("my-trail")
    mock_client.call.assert_awaited_once()


async def test_start_logging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await start_logging("x", region_name="us-east-1")


async def test_start_logging_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="start_logging failed"
    ):
        await start_logging("x")


# ---------------------------------------------------------------------------
# stop_logging
# ---------------------------------------------------------------------------


async def test_stop_logging_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    await stop_logging("my-trail")
    mock_client.call.assert_awaited_once()


async def test_stop_logging_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await stop_logging("x", region_name="us-east-1")


async def test_stop_logging_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="stop_logging failed"
    ):
        await stop_logging("x")


# ---------------------------------------------------------------------------
# get_trail_status
# ---------------------------------------------------------------------------


async def test_get_trail_status_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _status_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await get_trail_status("my-trail")
    assert isinstance(result, TrailStatus)
    assert result.is_logging is True


async def test_get_trail_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_trail_status("x", region_name="us-east-1")


async def test_get_trail_status_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="get_trail_status failed"
    ):
        await get_trail_status("x")


# ---------------------------------------------------------------------------
# lookup_events
# ---------------------------------------------------------------------------


async def test_lookup_events_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Events": [_event_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await lookup_events()
    assert len(result) == 1
    assert result[0].event_id == "evt-1"


async def test_lookup_events_with_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Events": [_event_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await lookup_events(
        lookup_attributes=[
            {
                "AttributeKey": "EventName",
                "AttributeValue": "CreateBucket",
            }
        ],
        start_time="2024-01-01",
        end_time="2024-01-02",
        max_results=10,
        region_name="us-east-1",
    )
    assert len(result) == 1
    kw = mock_client.call.call_args[1]
    assert "LookupAttributes" in kw
    assert "StartTime" in kw
    assert "EndTime" in kw
    assert "MaxResults" in kw


async def test_lookup_events_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Events": [_event_dict("e1")],
            "NextToken": "tok",
        },
        {"Events": [_event_dict("e2")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await lookup_events()
    assert len(result) == 2


async def test_lookup_events_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Events": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await lookup_events()
    assert result == []


async def test_lookup_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await lookup_events()


async def test_lookup_events_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="lookup_events failed"
    ):
        await lookup_events()


# ---------------------------------------------------------------------------
# list_trails
# ---------------------------------------------------------------------------


async def test_list_trails_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Trails": [
            {
                "TrailARN": "arn:trail",
                "Name": "t1",
                "HomeRegion": "us-east-1",
            }
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_trails()
    assert len(result) == 1
    assert result[0].name == "t1"
    assert isinstance(result[0], TrailSummary)


async def test_list_trails_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Trails": [
                {"TrailARN": "arn:1", "Name": "t1"}
            ],
            "NextToken": "tok",
        },
        {
            "Trails": [
                {"TrailARN": "arn:2", "Name": "t2"}
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_trails()
    assert len(result) == 2


async def test_list_trails_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Trails": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_trails(region_name="us-east-1")
    assert result == []


async def test_list_trails_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_trails()


async def test_list_trails_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_trails failed"
    ):
        await list_trails()


# ---------------------------------------------------------------------------
# create_event_data_store
# ---------------------------------------------------------------------------


async def test_create_event_data_store_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = _eds_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await create_event_data_store("my-eds")
    assert isinstance(result, EventDataStoreResult)
    assert result.name == "my-eds"


async def test_create_event_data_store_all_options(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.return_value = _eds_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await create_event_data_store(
        "my-eds",
        retention_period=90,
        multi_region_enabled=False,
        organization_enabled=True,
        advanced_event_selectors=[{"Name": "sel"}],
        tags=[{"Key": "env", "Value": "dev"}],
        region_name="us-east-1",
    )
    assert result.name == "my-eds"
    kw = mock_client.call.call_args[1]
    assert kw["RetentionPeriod"] == 90
    assert "AdvancedEventSelectors" in kw
    assert "TagsList" in kw


async def test_create_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await create_event_data_store("x")


async def test_create_event_data_store_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="create_event_data_store failed",
    ):
        await create_event_data_store("x")


# ---------------------------------------------------------------------------
# describe_event_data_store
# ---------------------------------------------------------------------------


async def test_describe_event_data_store_success(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.return_value = _eds_dict()
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_event_data_store("arn:eds")
    assert result.name == "my-eds"


async def test_describe_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_event_data_store(
            "arn:eds", region_name="us-east-1"
        )


async def test_describe_event_data_store_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="describe_event_data_store failed",
    ):
        await describe_event_data_store("arn:eds")


# ---------------------------------------------------------------------------
# list_event_data_stores
# ---------------------------------------------------------------------------


async def test_list_event_data_stores_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "EventDataStores": [_eds_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_event_data_stores()
    assert len(result) == 1
    assert result[0].name == "my-eds"


async def test_list_event_data_stores_pagination(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "EventDataStores": [
                _eds_dict(arn="arn:1", name="e1")
            ],
            "NextToken": "tok",
        },
        {
            "EventDataStores": [
                _eds_dict(arn="arn:2", name="e2")
            ],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_event_data_stores()
    assert len(result) == 2


async def test_list_event_data_stores_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "EventDataStores": []
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_event_data_stores(
        region_name="us-east-1"
    )
    assert result == []


async def test_list_event_data_stores_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_event_data_stores()


async def test_list_event_data_stores_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="list_event_data_stores failed",
    ):
        await list_event_data_stores()


# ---------------------------------------------------------------------------
# delete_event_data_store
# ---------------------------------------------------------------------------


async def test_delete_event_data_store_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    await delete_event_data_store("arn:eds")
    mock_client.call.assert_awaited_once()


async def test_delete_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_event_data_store(
            "arn:eds", region_name="us-east-1"
        )


async def test_delete_event_data_store_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("io")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="delete_event_data_store failed",
    ):
        await delete_event_data_store("arn:eds")


# ---------------------------------------------------------------------------
# start_query
# ---------------------------------------------------------------------------


async def test_start_query_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"QueryId": "q-123"}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await start_query("SELECT * FROM eds")
    assert result == "q-123"


async def test_start_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await start_query(
            "SELECT *", region_name="us-east-1"
        )


async def test_start_query_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="start_query failed"
    ):
        await start_query("SELECT *")


# ---------------------------------------------------------------------------
# get_query_results
# ---------------------------------------------------------------------------


async def test_get_query_results_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "QueryStatus": "COMPLETE",
        "QueryStatistics": {"TotalResultsCount": 1},
        "QueryResultRows": [
            [{"key": "eventId", "value": "e1"}]
        ],
        "ResponseMetadata": {},
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await get_query_results("q-123")
    assert isinstance(result, QueryResult)
    assert result.query_status == "COMPLETE"
    assert len(result.query_result_rows) == 1

async def test_get_query_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_query_results("q-bad")


async def test_get_query_results_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="get_query_results failed"
    ):
        await get_query_results("q-bad")


# ---------------------------------------------------------------------------
# list_queries
# ---------------------------------------------------------------------------


async def test_list_queries_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Queries": [
            {"QueryId": "q-1", "QueryStatus": "COMPLETE"}
        ]
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_queries("arn:eds")
    assert len(result) == 1
    assert result[0]["QueryId"] == "q-1"


async def test_list_queries_with_filters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Queries": []}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_queries(
        "arn:eds",
        start_time="2024-01-01",
        end_time="2024-01-02",
        query_status="COMPLETE",
        region_name="us-east-1",
    )
    assert result == []
    kw = mock_client.call.call_args[1]
    assert "StartTime" in kw
    assert "EndTime" in kw
    assert "QueryStatus" in kw


async def test_list_queries_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Queries": [{"QueryId": "q-1"}],
            "NextToken": "tok",
        },
        {"Queries": [{"QueryId": "q-2"}]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await list_queries("arn:eds")
    assert len(result) == 2


async def test_list_queries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_queries("arn:eds")


async def test_list_queries_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_queries failed"
    ):
        await list_queries("arn:eds")


# ---------------------------------------------------------------------------
# put_event_selectors
# ---------------------------------------------------------------------------


async def test_put_event_selectors_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [{"ReadWriteType": "All"}],
        "AdvancedEventSelectors": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await put_event_selectors(
        "my-trail",
        event_selectors=[{"ReadWriteType": "All"}],
    )
    assert isinstance(result, EventSelectorResult)
    assert result.trail_arn == "arn:trail"


async def test_put_event_selectors_advanced(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [],
        "AdvancedEventSelectors": [{"Name": "sel1"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await put_event_selectors(
        "my-trail",
        advanced_event_selectors=[{"Name": "sel1"}],
        region_name="us-east-1",
    )
    assert len(result.advanced_event_selectors) == 1


async def test_put_event_selectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await put_event_selectors("x")


async def test_put_event_selectors_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="put_event_selectors failed"
    ):
        await put_event_selectors("x")


# ---------------------------------------------------------------------------
# get_event_selectors
# ---------------------------------------------------------------------------


async def test_get_event_selectors_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [{"ReadWriteType": "All"}],
        "AdvancedEventSelectors": [],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await get_event_selectors("my-trail")
    assert isinstance(result, EventSelectorResult)
    assert result.trail_arn == "arn:trail"


async def test_get_event_selectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_event_selectors(
            "x", region_name="us-east-1"
        )


async def test_get_event_selectors_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="get_event_selectors failed"
    ):
        await get_event_selectors("x")


# ---------------------------------------------------------------------------
# put_insight_selectors
# ---------------------------------------------------------------------------


async def test_put_insight_selectors_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TrailARN": "arn:trail",
        "InsightSelectors": [
            {"InsightType": "ApiCallRateInsight"}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await put_insight_selectors(
        "my-trail",
        insight_selectors=[
            {"InsightType": "ApiCallRateInsight"}
        ],
    )
    assert isinstance(result, InsightSelectorResult)
    assert result.trail_arn == "arn:trail"
    assert len(result.insight_selectors) == 1


async def test_put_insight_selectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await put_insight_selectors(
            "x",
            insight_selectors=[],
            region_name="us-east-1",
        )


async def test_put_insight_selectors_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="put_insight_selectors failed",
    ):
        await put_insight_selectors(
            "x", insight_selectors=[]
        )


# ---------------------------------------------------------------------------
# get_insight_selectors
# ---------------------------------------------------------------------------


async def test_get_insight_selectors_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "TrailARN": "arn:trail",
        "InsightSelectors": [
            {"InsightType": "ApiCallRateInsight"}
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    result = await get_insight_selectors("my-trail")
    assert isinstance(result, InsightSelectorResult)
    assert len(result.insight_selectors) == 1


async def test_get_insight_selectors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_insight_selectors(
            "x", region_name="us-east-1"
        )


async def test_get_insight_selectors_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="get_insight_selectors failed",
    ):
        await get_insight_selectors("x")


async def test_add_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags("test-resource_id", [], )


async def test_cancel_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_query("test-query_id", )
    mock_client.call.assert_called_once()


async def test_cancel_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_query("test-query_id", )


async def test_create_channel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_channel("test-name", "test-source", [], )
    mock_client.call.assert_called_once()


async def test_create_channel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_channel("test-name", "test-source", [], )


async def test_create_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dashboard("test-name", )
    mock_client.call.assert_called_once()


async def test_create_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dashboard("test-name", )


async def test_delete_channel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_channel("test-channel", )
    mock_client.call.assert_called_once()


async def test_delete_channel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_channel("test-channel", )


async def test_delete_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dashboard("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_delete_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dashboard("test-dashboard_id", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_deregister_organization_delegated_admin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_organization_delegated_admin("test-delegated_admin_account_id", )
    mock_client.call.assert_called_once()


async def test_deregister_organization_delegated_admin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_organization_delegated_admin("test-delegated_admin_account_id", )


async def test_describe_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_query()
    mock_client.call.assert_called_once()


async def test_describe_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_query()


async def test_disable_federation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_federation("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_disable_federation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_federation("test-event_data_store", )


async def test_enable_federation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_federation("test-event_data_store", "test-federation_role_arn", )
    mock_client.call.assert_called_once()


async def test_enable_federation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_federation("test-event_data_store", "test-federation_role_arn", )


async def test_generate_query(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_query([], "test-prompt", )
    mock_client.call.assert_called_once()


async def test_generate_query_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_query([], "test-prompt", )


async def test_get_channel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_channel("test-channel", )
    mock_client.call.assert_called_once()


async def test_get_channel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_channel("test-channel", )


async def test_get_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_dashboard("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_get_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_dashboard("test-dashboard_id", )


async def test_get_event_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_event_configuration()
    mock_client.call.assert_called_once()


async def test_get_event_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_event_configuration()


async def test_get_event_data_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_event_data_store("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_get_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_event_data_store("test-event_data_store", )


async def test_get_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_import("test-import_id", )
    mock_client.call.assert_called_once()


async def test_get_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_import("test-import_id", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_list_channels(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_channels()
    mock_client.call.assert_called_once()


async def test_list_channels_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_channels()


async def test_list_dashboards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dashboards()
    mock_client.call.assert_called_once()


async def test_list_dashboards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dashboards()


async def test_list_import_failures(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_import_failures("test-import_id", )
    mock_client.call.assert_called_once()


async def test_list_import_failures_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_import_failures("test-import_id", )


async def test_list_imports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_imports()
    mock_client.call.assert_called_once()


async def test_list_imports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_imports()


async def test_list_insights_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", )
    mock_client.call.assert_called_once()


async def test_list_insights_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", )


async def test_list_public_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_public_keys()
    mock_client.call.assert_called_once()


async def test_list_public_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_public_keys()


async def test_list_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags([], )
    mock_client.call.assert_called_once()


async def test_list_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags([], )


async def test_put_event_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_event_configuration("test-max_event_size", [], )
    mock_client.call.assert_called_once()


async def test_put_event_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_event_configuration("test-max_event_size", [], )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-resource_policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-resource_policy", )


async def test_register_organization_delegated_admin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_organization_delegated_admin("test-member_account_id", )
    mock_client.call.assert_called_once()


async def test_register_organization_delegated_admin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_organization_delegated_admin("test-member_account_id", )


async def test_remove_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags("test-resource_id", [], )


async def test_restore_event_data_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_event_data_store("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_restore_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_event_data_store("test-event_data_store", )


async def test_search_sample_queries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_sample_queries("test-search_phrase", )
    mock_client.call.assert_called_once()


async def test_search_sample_queries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_sample_queries("test-search_phrase", )


async def test_start_dashboard_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_dashboard_refresh("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_start_dashboard_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_dashboard_refresh("test-dashboard_id", )


async def test_start_event_data_store_ingestion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_event_data_store_ingestion("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_start_event_data_store_ingestion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_event_data_store_ingestion("test-event_data_store", )


async def test_start_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_import()
    mock_client.call.assert_called_once()


async def test_start_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_import()


async def test_stop_event_data_store_ingestion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_event_data_store_ingestion("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_stop_event_data_store_ingestion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_event_data_store_ingestion("test-event_data_store", )


async def test_stop_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_import("test-import_id", )
    mock_client.call.assert_called_once()


async def test_stop_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_import("test-import_id", )


async def test_update_channel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_channel("test-channel", )
    mock_client.call.assert_called_once()


async def test_update_channel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_channel("test-channel", )


async def test_update_dashboard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dashboard("test-dashboard_id", )
    mock_client.call.assert_called_once()


async def test_update_dashboard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dashboard("test-dashboard_id", )


async def test_update_event_data_store(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_event_data_store("test-event_data_store", )
    mock_client.call.assert_called_once()


async def test_update_event_data_store_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cloudtrail.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_event_data_store("test-event_data_store", )


@pytest.mark.asyncio
async def test_describe_trails_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import describe_trails
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await describe_trails(trail_name_list="test-trail_name_list", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_trail_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import update_trail
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await update_trail("test-name", s3_bucket_name="test-s3_bucket_name", s3_key_prefix="test-s3_key_prefix", sns_topic_name="test-sns_topic_name", include_global_service_events=True, is_multi_region_trail=True, enable_log_file_validation=True, cloud_watch_logs_log_group_arn="test-cloud_watch_logs_log_group_arn", cloud_watch_logs_role_arn="test-cloud_watch_logs_role_arn", kms_key_id="test-kms_key_id", is_organization_trail=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_lookup_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import lookup_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await lookup_events(lookup_attributes="test-lookup_attributes", start_time="test-start_time", end_time="test-end_time", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_data_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import create_event_data_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await create_event_data_store("test-name", retention_period="test-retention_period", advanced_event_selectors="test-advanced_event_selectors", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_query_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import get_query_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await get_query_results("test-query_id", event_data_store="test-event_data_store", max_query_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_queries("test-event_data_store", start_time="test-start_time", end_time="test-end_time", query_status="test-query_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_event_selectors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import put_event_selectors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await put_event_selectors("test-trail_name", event_selectors="test-event_selectors", advanced_event_selectors="test-advanced_event_selectors", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import cancel_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await cancel_query("test-query_id", event_data_store="test-event_data_store", event_data_store_owner_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_channel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import create_channel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await create_channel("test-name", "test-source", "test-destinations", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import create_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await create_dashboard("test-name", refresh_schedule="test-refresh_schedule", tags_list=[{"Key": "k", "Value": "v"}], termination_protection_enabled="test-termination_protection_enabled", widgets="test-widgets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import describe_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await describe_query(event_data_store="test-event_data_store", query_id="test-query_id", query_alias="test-query_alias", refresh_id="test-refresh_id", event_data_store_owner_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_event_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import get_event_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await get_event_configuration(event_data_store="test-event_data_store", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_channels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_channels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_channels(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dashboards_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_dashboards
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_dashboards(name_prefix="test-name_prefix", type_value="test-type_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_import_failures_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_import_failures
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_import_failures(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_imports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_imports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_imports(max_results=1, destination="test-destination", import_status=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_insights_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_insights_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", error_code="test-error_code", start_time="test-start_time", end_time="test-end_time", period="test-period", data_type="test-data_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_public_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_public_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_public_keys(start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import list_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await list_tags("test-resource_id_list", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_event_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import put_event_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await put_event_configuration(1, {}, event_data_store="test-event_data_store", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_sample_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import search_sample_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await search_sample_queries("test-search_phrase", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_dashboard_refresh_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import start_dashboard_refresh
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await start_dashboard_refresh("test-dashboard_id", query_parameter_values="test-query_parameter_values", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_import_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import start_import
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await start_import(destinations="test-destinations", import_source=1, start_event_time="test-start_event_time", end_event_time="test-end_event_time", import_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_channel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import update_channel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await update_channel("test-channel", destinations="test-destinations", name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import update_dashboard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await update_dashboard("test-dashboard_id", widgets="test-widgets", refresh_schedule="test-refresh_schedule", termination_protection_enabled="test-termination_protection_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_event_data_store_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cloudtrail import update_event_data_store
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cloudtrail.async_client", lambda *a, **kw: mock_client)
    await update_event_data_store("test-event_data_store", name="test-name", advanced_event_selectors="test-advanced_event_selectors", multi_region_enabled=True, organization_enabled="test-organization_enabled", retention_period="test-retention_period", termination_protection_enabled="test-termination_protection_enabled", kms_key_id="test-kms_key_id", billing_mode="test-billing_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()
