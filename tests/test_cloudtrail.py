"""Tests for aws_util.cloudtrail module — 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.cloudtrail as ct_mod
from aws_util.cloudtrail import (
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


def _client_error(
    code: str = "AccessDenied", msg: str = "denied"
) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, "op"
    )


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
# Models
# ---------------------------------------------------------------------------


def test_trail_result_model():
    result = TrailResult(
        name="t", arn="arn:t", s3_bucket_name="b"
    )
    assert result.name == "t"
    assert result.arn == "arn:t"
    assert result.is_multi_region_trail is False


def test_trail_status_model():
    status = TrailStatus(is_logging=True)
    assert status.is_logging is True


def test_trail_summary_model():
    s = TrailSummary(
        trail_arn="arn:t", name="t", home_region="us-east-1"
    )
    assert s.trail_arn == "arn:t"


def test_lookup_event_model():
    e = LookupEvent(event_id="e1", event_name="CreateBucket")
    assert e.event_id == "e1"


def test_event_data_store_result_model():
    eds = EventDataStoreResult(
        event_data_store_arn="arn:eds", name="eds"
    )
    assert eds.event_data_store_arn == "arn:eds"


def test_query_result_model():
    q = QueryResult(query_id="q1", query_status="COMPLETE")
    assert q.query_id == "q1"


def test_event_selector_result_model():
    es = EventSelectorResult(
        trail_arn="arn:t", event_selectors=[]
    )
    assert es.trail_arn == "arn:t"


def test_insight_selector_result_model():
    i = InsightSelectorResult(
        trail_arn="arn:t", insight_selectors=[]
    )
    assert i.trail_arn == "arn:t"


# ---------------------------------------------------------------------------
# create_trail
# ---------------------------------------------------------------------------


def test_create_trail_basic(monkeypatch):
    mock = MagicMock()
    mock.create_trail.return_value = _trail_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = create_trail("my-trail", s3_bucket_name="my-bucket")
    assert isinstance(result, TrailResult)
    assert result.name == "my-trail"
    assert result.extra.get("HasCustomEventSelectors") is True


def test_create_trail_all_options(monkeypatch):
    mock = MagicMock()
    mock.create_trail.return_value = _trail_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = create_trail(
        "my-trail",
        s3_bucket_name="b",
        s3_key_prefix="logs",
        sns_topic_name="my-topic",
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
    kw = mock.create_trail.call_args[1]
    assert "S3KeyPrefix" in kw
    assert "SnsTopicName" in kw
    assert "CloudWatchLogsLogGroupArn" in kw
    assert "CloudWatchLogsRoleArn" in kw
    assert "KmsKeyId" in kw
    assert "TagsList" in kw


def test_create_trail_error(monkeypatch):
    mock = MagicMock()
    mock.create_trail.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="create_trail failed"):
        create_trail("x", s3_bucket_name="b")


# ---------------------------------------------------------------------------
# describe_trails
# ---------------------------------------------------------------------------


def test_describe_trails_basic(monkeypatch):
    mock = MagicMock()
    mock.describe_trails.return_value = {
        "trailList": [_trail_dict()]
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = describe_trails()
    assert len(result) == 1
    assert result[0].name == "my-trail"


def test_describe_trails_with_names(monkeypatch):
    mock = MagicMock()
    mock.describe_trails.return_value = {
        "trailList": [_trail_dict()]
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = describe_trails(
        trail_name_list=["my-trail"],
        include_shadow_trails=False,
        region_name="us-east-1",
    )
    assert len(result) == 1
    kw = mock.describe_trails.call_args[1]
    assert "trailNameList" in kw


def test_describe_trails_empty(monkeypatch):
    mock = MagicMock()
    mock.describe_trails.return_value = {"trailList": []}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = describe_trails()
    assert result == []


def test_describe_trails_error(monkeypatch):
    mock = MagicMock()
    mock.describe_trails.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="describe_trails failed"):
        describe_trails()


# ---------------------------------------------------------------------------
# get_trail
# ---------------------------------------------------------------------------


def test_get_trail_success(monkeypatch):
    mock = MagicMock()
    mock.get_trail.return_value = {"Trail": _trail_dict()}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = get_trail("my-trail")
    assert result.name == "my-trail"


def test_get_trail_error(monkeypatch):
    mock = MagicMock()
    mock.get_trail.side_effect = _client_error(
        "TrailNotFoundException", "not found"
    )
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="get_trail failed"):
        get_trail("missing", region_name="us-east-1")


# ---------------------------------------------------------------------------
# update_trail
# ---------------------------------------------------------------------------


def test_update_trail_basic(monkeypatch):
    mock = MagicMock()
    mock.update_trail.return_value = _trail_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = update_trail("my-trail")
    assert result.name == "my-trail"


def test_update_trail_all_options(monkeypatch):
    mock = MagicMock()
    mock.update_trail.return_value = _trail_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = update_trail(
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
    kw = mock.update_trail.call_args[1]
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


def test_update_trail_error(monkeypatch):
    mock = MagicMock()
    mock.update_trail.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="update_trail failed"):
        update_trail("x")


# ---------------------------------------------------------------------------
# delete_trail
# ---------------------------------------------------------------------------


def test_delete_trail_success(monkeypatch):
    mock = MagicMock()
    mock.delete_trail.return_value = {}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    delete_trail("my-trail")
    mock.delete_trail.assert_called_once()


def test_delete_trail_error(monkeypatch):
    mock = MagicMock()
    mock.delete_trail.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="delete_trail failed"):
        delete_trail("x", region_name="us-east-1")


# ---------------------------------------------------------------------------
# start_logging
# ---------------------------------------------------------------------------


def test_start_logging_success(monkeypatch):
    mock = MagicMock()
    mock.start_logging.return_value = {}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    start_logging("my-trail")
    mock.start_logging.assert_called_once()


def test_start_logging_error(monkeypatch):
    mock = MagicMock()
    mock.start_logging.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="start_logging failed"):
        start_logging("x", region_name="us-east-1")


# ---------------------------------------------------------------------------
# stop_logging
# ---------------------------------------------------------------------------


def test_stop_logging_success(monkeypatch):
    mock = MagicMock()
    mock.stop_logging.return_value = {}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    stop_logging("my-trail")
    mock.stop_logging.assert_called_once()


def test_stop_logging_error(monkeypatch):
    mock = MagicMock()
    mock.stop_logging.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="stop_logging failed"):
        stop_logging("x", region_name="us-east-1")


# ---------------------------------------------------------------------------
# get_trail_status
# ---------------------------------------------------------------------------


def test_get_trail_status_success(monkeypatch):
    mock = MagicMock()
    mock.get_trail_status.return_value = _status_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = get_trail_status("my-trail")
    assert isinstance(result, TrailStatus)
    assert result.is_logging is True
    assert result.extra.get("TimeLoggingStarted") == "2024-01-01"


def test_get_trail_status_error(monkeypatch):
    mock = MagicMock()
    mock.get_trail_status.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="get_trail_status failed"
    ):
        get_trail_status("x", region_name="us-east-1")


# ---------------------------------------------------------------------------
# lookup_events
# ---------------------------------------------------------------------------


def test_lookup_events_basic(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"Events": [_event_dict()]}
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = lookup_events()
    assert len(result) == 1
    assert result[0].event_id == "evt-1"
    assert result[0].extra.get("AccessKeyId") == "AKIA123"


def test_lookup_events_with_filters(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"Events": [_event_dict()]}
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = lookup_events(
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
    kw = paginator.paginate.call_args[1]
    assert "LookupAttributes" in kw
    assert "StartTime" in kw
    assert "EndTime" in kw
    assert "MaxResults" in kw


def test_lookup_events_empty(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"Events": []}]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = lookup_events()
    assert result == []


def test_lookup_events_error(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _client_error()
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="lookup_events failed"):
        lookup_events()


# ---------------------------------------------------------------------------
# list_trails
# ---------------------------------------------------------------------------


def test_list_trails_basic(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {
            "Trails": [
                {
                    "TrailARN": "arn:trail",
                    "Name": "t1",
                    "HomeRegion": "us-east-1",
                }
            ]
        }
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_trails()
    assert len(result) == 1
    assert result[0].name == "t1"
    assert isinstance(result[0], TrailSummary)


def test_list_trails_empty(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"Trails": []}]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_trails(region_name="us-east-1")
    assert result == []


def test_list_trails_error(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _client_error()
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="list_trails failed"):
        list_trails()


# ---------------------------------------------------------------------------
# create_event_data_store
# ---------------------------------------------------------------------------


def test_create_event_data_store_basic(monkeypatch):
    mock = MagicMock()
    mock.create_event_data_store.return_value = _eds_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = create_event_data_store("my-eds")
    assert isinstance(result, EventDataStoreResult)
    assert result.name == "my-eds"
    assert result.extra.get("BillingMode") == (
        "FIXED_RETENTION_PRICING"
    )


def test_create_event_data_store_all_options(monkeypatch):
    mock = MagicMock()
    mock.create_event_data_store.return_value = _eds_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = create_event_data_store(
        "my-eds",
        retention_period=90,
        multi_region_enabled=False,
        organization_enabled=True,
        advanced_event_selectors=[{"Name": "sel"}],
        tags=[{"Key": "env", "Value": "dev"}],
        region_name="us-east-1",
    )
    assert result.name == "my-eds"
    kw = mock.create_event_data_store.call_args[1]
    assert kw["RetentionPeriod"] == 90
    assert "AdvancedEventSelectors" in kw
    assert "TagsList" in kw


def test_create_event_data_store_error(monkeypatch):
    mock = MagicMock()
    mock.create_event_data_store.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="create_event_data_store failed"
    ):
        create_event_data_store("x")


# ---------------------------------------------------------------------------
# describe_event_data_store
# ---------------------------------------------------------------------------


def test_describe_event_data_store_success(monkeypatch):
    mock = MagicMock()
    mock.describe_event_data_store.return_value = _eds_dict()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = describe_event_data_store("arn:eds")
    assert result.name == "my-eds"


def test_describe_event_data_store_error(monkeypatch):
    mock = MagicMock()
    mock.describe_event_data_store.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="describe_event_data_store failed"
    ):
        describe_event_data_store(
            "arn:eds", region_name="us-east-1"
        )


# ---------------------------------------------------------------------------
# list_event_data_stores
# ---------------------------------------------------------------------------


def test_list_event_data_stores_basic(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"EventDataStores": [_eds_dict()]}
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_event_data_stores()
    assert len(result) == 1
    assert result[0].name == "my-eds"


def test_list_event_data_stores_empty(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"EventDataStores": []}
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_event_data_stores(region_name="us-east-1")
    assert result == []


def test_list_event_data_stores_error(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _client_error()
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="list_event_data_stores failed"
    ):
        list_event_data_stores()


# ---------------------------------------------------------------------------
# delete_event_data_store
# ---------------------------------------------------------------------------


def test_delete_event_data_store_success(monkeypatch):
    mock = MagicMock()
    mock.delete_event_data_store.return_value = {}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    delete_event_data_store("arn:eds")
    mock.delete_event_data_store.assert_called_once()


def test_delete_event_data_store_error(monkeypatch):
    mock = MagicMock()
    mock.delete_event_data_store.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="delete_event_data_store failed"
    ):
        delete_event_data_store(
            "arn:eds", region_name="us-east-1"
        )


# ---------------------------------------------------------------------------
# start_query
# ---------------------------------------------------------------------------


def test_start_query_success(monkeypatch):
    mock = MagicMock()
    mock.start_query.return_value = {"QueryId": "q-123"}
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = start_query("SELECT * FROM eds")
    assert result == "q-123"


def test_start_query_error(monkeypatch):
    mock = MagicMock()
    mock.start_query.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="start_query failed"):
        start_query("SELECT *", region_name="us-east-1")


# ---------------------------------------------------------------------------
# get_query_results
# ---------------------------------------------------------------------------


def test_get_query_results_basic(monkeypatch):
    mock = MagicMock()
    mock.get_query_results.return_value = {
        "QueryStatus": "COMPLETE",
        "QueryStatistics": {"TotalResultsCount": 1},
        "QueryResultRows": [
            [{"key": "eventId", "value": "e1"}]
        ],
        "ResponseMetadata": {},
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = get_query_results("q-123")
    assert isinstance(result, QueryResult)
    assert result.query_status == "COMPLETE"
    assert len(result.query_result_rows) == 1

def test_get_query_results_error(monkeypatch):
    mock = MagicMock()
    mock.get_query_results.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="get_query_results failed"
    ):
        get_query_results("q-bad")


# ---------------------------------------------------------------------------
# list_queries
# ---------------------------------------------------------------------------


def test_list_queries_basic(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {
            "Queries": [
                {
                    "QueryId": "q-1",
                    "QueryStatus": "COMPLETE",
                }
            ]
        }
    ]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_queries("arn:eds")
    assert len(result) == 1
    assert result[0]["QueryId"] == "q-1"


def test_list_queries_with_filters(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = [{"Queries": []}]
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = list_queries(
        "arn:eds",
        start_time="2024-01-01",
        end_time="2024-01-02",
        query_status="COMPLETE",
        region_name="us-east-1",
    )
    assert result == []
    kw = paginator.paginate.call_args[1]
    assert "StartTime" in kw
    assert "EndTime" in kw
    assert "QueryStatus" in kw


def test_list_queries_error(monkeypatch):
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.side_effect = _client_error()
    mock.get_paginator.return_value = paginator
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(RuntimeError, match="list_queries failed"):
        list_queries("arn:eds")


# ---------------------------------------------------------------------------
# put_event_selectors
# ---------------------------------------------------------------------------


def test_put_event_selectors_basic(monkeypatch):
    mock = MagicMock()
    mock.put_event_selectors.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [{"ReadWriteType": "All"}],
        "AdvancedEventSelectors": [],
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = put_event_selectors(
        "my-trail",
        event_selectors=[{"ReadWriteType": "All"}],
    )
    assert isinstance(result, EventSelectorResult)
    assert result.trail_arn == "arn:trail"
    assert len(result.event_selectors) == 1


def test_put_event_selectors_advanced(monkeypatch):
    mock = MagicMock()
    mock.put_event_selectors.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [],
        "AdvancedEventSelectors": [{"Name": "sel1"}],
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = put_event_selectors(
        "my-trail",
        advanced_event_selectors=[{"Name": "sel1"}],
        region_name="us-east-1",
    )
    assert len(result.advanced_event_selectors) == 1


def test_put_event_selectors_error(monkeypatch):
    mock = MagicMock()
    mock.put_event_selectors.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="put_event_selectors failed"
    ):
        put_event_selectors("x")


# ---------------------------------------------------------------------------
# get_event_selectors
# ---------------------------------------------------------------------------


def test_get_event_selectors_success(monkeypatch):
    mock = MagicMock()
    mock.get_event_selectors.return_value = {
        "TrailARN": "arn:trail",
        "EventSelectors": [{"ReadWriteType": "All"}],
        "AdvancedEventSelectors": [],
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = get_event_selectors("my-trail")
    assert isinstance(result, EventSelectorResult)
    assert result.trail_arn == "arn:trail"


def test_get_event_selectors_error(monkeypatch):
    mock = MagicMock()
    mock.get_event_selectors.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="get_event_selectors failed"
    ):
        get_event_selectors("x", region_name="us-east-1")


# ---------------------------------------------------------------------------
# put_insight_selectors
# ---------------------------------------------------------------------------


def test_put_insight_selectors_success(monkeypatch):
    mock = MagicMock()
    mock.put_insight_selectors.return_value = {
        "TrailARN": "arn:trail",
        "InsightSelectors": [
            {"InsightType": "ApiCallRateInsight"}
        ],
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = put_insight_selectors(
        "my-trail",
        insight_selectors=[
            {"InsightType": "ApiCallRateInsight"}
        ],
    )
    assert isinstance(result, InsightSelectorResult)
    assert result.trail_arn == "arn:trail"
    assert len(result.insight_selectors) == 1


def test_put_insight_selectors_error(monkeypatch):
    mock = MagicMock()
    mock.put_insight_selectors.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="put_insight_selectors failed"
    ):
        put_insight_selectors(
            "x",
            insight_selectors=[],
            region_name="us-east-1",
        )


# ---------------------------------------------------------------------------
# get_insight_selectors
# ---------------------------------------------------------------------------


def test_get_insight_selectors_success(monkeypatch):
    mock = MagicMock()
    mock.get_insight_selectors.return_value = {
        "TrailARN": "arn:trail",
        "InsightSelectors": [
            {"InsightType": "ApiCallRateInsight"}
        ],
    }
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    result = get_insight_selectors("my-trail")
    assert isinstance(result, InsightSelectorResult)
    assert len(result.insight_selectors) == 1


def test_get_insight_selectors_error(monkeypatch):
    mock = MagicMock()
    mock.get_insight_selectors.side_effect = _client_error()
    monkeypatch.setattr(
        ct_mod, "get_client", lambda *a, **kw: mock
    )
    with pytest.raises(
        RuntimeError, match="get_insight_selectors failed"
    ):
        get_insight_selectors("x", region_name="us-east-1")


REGION = "us-east-1"


def test_add_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    add_tags("test-resource_id", [], region_name=REGION)
    mock_client.add_tags.assert_called_once()


def test_add_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags"):
        add_tags("test-resource_id", [], region_name=REGION)


def test_cancel_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_query.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    cancel_query("test-query_id", region_name=REGION)
    mock_client.cancel_query.assert_called_once()


def test_cancel_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_query",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel query"):
        cancel_query("test-query_id", region_name=REGION)


def test_create_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    create_channel("test-name", "test-source", [], region_name=REGION)
    mock_client.create_channel.assert_called_once()


def test_create_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_channel",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create channel"):
        create_channel("test-name", "test-source", [], region_name=REGION)


def test_create_dashboard(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    create_dashboard("test-name", region_name=REGION)
    mock_client.create_dashboard.assert_called_once()


def test_create_dashboard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dashboard",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create dashboard"):
        create_dashboard("test-name", region_name=REGION)


def test_delete_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    delete_channel("test-channel", region_name=REGION)
    mock_client.delete_channel.assert_called_once()


def test_delete_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_channel",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete channel"):
        delete_channel("test-channel", region_name=REGION)


def test_delete_dashboard(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    delete_dashboard("test-dashboard_id", region_name=REGION)
    mock_client.delete_dashboard.assert_called_once()


def test_delete_dashboard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dashboard",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete dashboard"):
        delete_dashboard("test-dashboard_id", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_deregister_organization_delegated_admin(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_organization_delegated_admin.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    deregister_organization_delegated_admin("test-delegated_admin_account_id", region_name=REGION)
    mock_client.deregister_organization_delegated_admin.assert_called_once()


def test_deregister_organization_delegated_admin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_organization_delegated_admin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_organization_delegated_admin",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister organization delegated admin"):
        deregister_organization_delegated_admin("test-delegated_admin_account_id", region_name=REGION)


def test_describe_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_query.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    describe_query(region_name=REGION)
    mock_client.describe_query.assert_called_once()


def test_describe_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_query",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe query"):
        describe_query(region_name=REGION)


def test_disable_federation(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_federation.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    disable_federation("test-event_data_store", region_name=REGION)
    mock_client.disable_federation.assert_called_once()


def test_disable_federation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_federation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_federation",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable federation"):
        disable_federation("test-event_data_store", region_name=REGION)


def test_enable_federation(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_federation.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    enable_federation("test-event_data_store", "test-federation_role_arn", region_name=REGION)
    mock_client.enable_federation.assert_called_once()


def test_enable_federation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_federation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_federation",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable federation"):
        enable_federation("test-event_data_store", "test-federation_role_arn", region_name=REGION)


def test_generate_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_query.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    generate_query([], "test-prompt", region_name=REGION)
    mock_client.generate_query.assert_called_once()


def test_generate_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_query",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate query"):
        generate_query([], "test-prompt", region_name=REGION)


def test_get_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_channel("test-channel", region_name=REGION)
    mock_client.get_channel.assert_called_once()


def test_get_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_channel",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get channel"):
        get_channel("test-channel", region_name=REGION)


def test_get_dashboard(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_dashboard("test-dashboard_id", region_name=REGION)
    mock_client.get_dashboard.assert_called_once()


def test_get_dashboard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_dashboard",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get dashboard"):
        get_dashboard("test-dashboard_id", region_name=REGION)


def test_get_event_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_event_configuration(region_name=REGION)
    mock_client.get_event_configuration.assert_called_once()


def test_get_event_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_event_configuration",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get event configuration"):
        get_event_configuration(region_name=REGION)


def test_get_event_data_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_data_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_event_data_store("test-event_data_store", region_name=REGION)
    mock_client.get_event_data_store.assert_called_once()


def test_get_event_data_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_event_data_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_event_data_store",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get event data store"):
        get_event_data_store("test-event_data_store", region_name=REGION)


def test_get_import(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_import.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_import("test-import_id", region_name=REGION)
    mock_client.get_import.assert_called_once()


def test_get_import_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_import",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get import"):
        get_import("test-import_id", region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_list_channels(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_channels.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_channels(region_name=REGION)
    mock_client.list_channels.assert_called_once()


def test_list_channels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_channels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_channels",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list channels"):
        list_channels(region_name=REGION)


def test_list_dashboards(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dashboards.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_dashboards(region_name=REGION)
    mock_client.list_dashboards.assert_called_once()


def test_list_dashboards_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_dashboards.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dashboards",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list dashboards"):
        list_dashboards(region_name=REGION)


def test_list_import_failures(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_import_failures.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_import_failures("test-import_id", region_name=REGION)
    mock_client.list_import_failures.assert_called_once()


def test_list_import_failures_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_import_failures.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_import_failures",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list import failures"):
        list_import_failures("test-import_id", region_name=REGION)


def test_list_imports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_imports(region_name=REGION)
    mock_client.list_imports.assert_called_once()


def test_list_imports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_imports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_imports",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list imports"):
        list_imports(region_name=REGION)


def test_list_insights_metric_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_insights_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", region_name=REGION)
    mock_client.list_insights_metric_data.assert_called_once()


def test_list_insights_metric_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_insights_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_insights_metric_data",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list insights metric data"):
        list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", region_name=REGION)


def test_list_public_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_public_keys(region_name=REGION)
    mock_client.list_public_keys.assert_called_once()


def test_list_public_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_public_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_public_keys",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list public keys"):
        list_public_keys(region_name=REGION)


def test_list_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_tags([], region_name=REGION)
    mock_client.list_tags.assert_called_once()


def test_list_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags"):
        list_tags([], region_name=REGION)


def test_put_event_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_event_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    put_event_configuration("test-max_event_size", [], region_name=REGION)
    mock_client.put_event_configuration.assert_called_once()


def test_put_event_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_event_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_event_configuration",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put event configuration"):
        put_event_configuration("test-max_event_size", [], region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-resource_policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-resource_policy", region_name=REGION)


def test_register_organization_delegated_admin(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_organization_delegated_admin.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    register_organization_delegated_admin("test-member_account_id", region_name=REGION)
    mock_client.register_organization_delegated_admin.assert_called_once()


def test_register_organization_delegated_admin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_organization_delegated_admin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_organization_delegated_admin",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register organization delegated admin"):
        register_organization_delegated_admin("test-member_account_id", region_name=REGION)


def test_remove_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    remove_tags("test-resource_id", [], region_name=REGION)
    mock_client.remove_tags.assert_called_once()


def test_remove_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags"):
        remove_tags("test-resource_id", [], region_name=REGION)


def test_restore_event_data_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_event_data_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    restore_event_data_store("test-event_data_store", region_name=REGION)
    mock_client.restore_event_data_store.assert_called_once()


def test_restore_event_data_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_event_data_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_event_data_store",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore event data store"):
        restore_event_data_store("test-event_data_store", region_name=REGION)


def test_search_sample_queries(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_sample_queries.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    search_sample_queries("test-search_phrase", region_name=REGION)
    mock_client.search_sample_queries.assert_called_once()


def test_search_sample_queries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_sample_queries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_sample_queries",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search sample queries"):
        search_sample_queries("test-search_phrase", region_name=REGION)


def test_start_dashboard_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_refresh.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    start_dashboard_refresh("test-dashboard_id", region_name=REGION)
    mock_client.start_dashboard_refresh.assert_called_once()


def test_start_dashboard_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_dashboard_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_dashboard_refresh",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start dashboard refresh"):
        start_dashboard_refresh("test-dashboard_id", region_name=REGION)


def test_start_event_data_store_ingestion(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_event_data_store_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    start_event_data_store_ingestion("test-event_data_store", region_name=REGION)
    mock_client.start_event_data_store_ingestion.assert_called_once()


def test_start_event_data_store_ingestion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_event_data_store_ingestion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_event_data_store_ingestion",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start event data store ingestion"):
        start_event_data_store_ingestion("test-event_data_store", region_name=REGION)


def test_start_import(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    start_import(region_name=REGION)
    mock_client.start_import.assert_called_once()


def test_start_import_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_import",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start import"):
        start_import(region_name=REGION)


def test_stop_event_data_store_ingestion(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_event_data_store_ingestion.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    stop_event_data_store_ingestion("test-event_data_store", region_name=REGION)
    mock_client.stop_event_data_store_ingestion.assert_called_once()


def test_stop_event_data_store_ingestion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_event_data_store_ingestion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_event_data_store_ingestion",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop event data store ingestion"):
        stop_event_data_store_ingestion("test-event_data_store", region_name=REGION)


def test_stop_import(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_import.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    stop_import("test-import_id", region_name=REGION)
    mock_client.stop_import.assert_called_once()


def test_stop_import_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_import.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_import",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop import"):
        stop_import("test-import_id", region_name=REGION)


def test_update_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_channel("test-channel", region_name=REGION)
    mock_client.update_channel.assert_called_once()


def test_update_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_channel",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update channel"):
        update_channel("test-channel", region_name=REGION)


def test_update_dashboard(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_dashboard("test-dashboard_id", region_name=REGION)
    mock_client.update_dashboard.assert_called_once()


def test_update_dashboard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_dashboard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dashboard",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update dashboard"):
        update_dashboard("test-dashboard_id", region_name=REGION)


def test_update_event_data_store(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_data_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_event_data_store("test-event_data_store", region_name=REGION)
    mock_client.update_event_data_store.assert_called_once()


def test_update_event_data_store_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_event_data_store.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_event_data_store",
    )
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update event data store"):
        update_event_data_store("test-event_data_store", region_name=REGION)


def test_describe_trails_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import describe_trails
    mock_client = MagicMock()
    mock_client.describe_trails.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    describe_trails(trail_name_list="test-trail_name_list", region_name="us-east-1")
    mock_client.describe_trails.assert_called_once()

def test_update_trail_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import update_trail
    mock_client = MagicMock()
    mock_client.update_trail.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_trail("test-name", s3_bucket_name="test-s3_bucket_name", s3_key_prefix="test-s3_key_prefix", sns_topic_name="test-sns_topic_name", include_global_service_events=True, is_multi_region_trail=True, enable_log_file_validation=True, cloud_watch_logs_log_group_arn="test-cloud_watch_logs_log_group_arn", cloud_watch_logs_role_arn="test-cloud_watch_logs_role_arn", kms_key_id="test-kms_key_id", is_organization_trail=True, region_name="us-east-1")
    mock_client.update_trail.assert_called_once()

def test_create_event_data_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import create_event_data_store
    mock_client = MagicMock()
    mock_client.create_event_data_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    create_event_data_store("test-name", retention_period="test-retention_period", advanced_event_selectors="test-advanced_event_selectors", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_data_store.assert_called_once()

def test_get_query_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import get_query_results
    mock_client = MagicMock()
    mock_client.get_query_results.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_query_results("test-query_id", event_data_store="test-event_data_store", max_query_results=1, region_name="us-east-1")
    mock_client.get_query_results.assert_called_once()

def test_put_event_selectors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import put_event_selectors
    mock_client = MagicMock()
    mock_client.put_event_selectors.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    put_event_selectors("test-trail_name", event_selectors="test-event_selectors", advanced_event_selectors="test-advanced_event_selectors", region_name="us-east-1")
    mock_client.put_event_selectors.assert_called_once()

def test_cancel_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import cancel_query
    mock_client = MagicMock()
    mock_client.cancel_query.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    cancel_query("test-query_id", event_data_store="test-event_data_store", event_data_store_owner_account_id=1, region_name="us-east-1")
    mock_client.cancel_query.assert_called_once()

def test_create_channel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import create_channel
    mock_client = MagicMock()
    mock_client.create_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    create_channel("test-name", "test-source", "test-destinations", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_channel.assert_called_once()

def test_create_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import create_dashboard
    mock_client = MagicMock()
    mock_client.create_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    create_dashboard("test-name", refresh_schedule="test-refresh_schedule", tags_list=[{"Key": "k", "Value": "v"}], termination_protection_enabled="test-termination_protection_enabled", widgets="test-widgets", region_name="us-east-1")
    mock_client.create_dashboard.assert_called_once()

def test_describe_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import describe_query
    mock_client = MagicMock()
    mock_client.describe_query.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    describe_query(event_data_store="test-event_data_store", query_id="test-query_id", query_alias="test-query_alias", refresh_id="test-refresh_id", event_data_store_owner_account_id=1, region_name="us-east-1")
    mock_client.describe_query.assert_called_once()

def test_get_event_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import get_event_configuration
    mock_client = MagicMock()
    mock_client.get_event_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    get_event_configuration(event_data_store="test-event_data_store", region_name="us-east-1")
    mock_client.get_event_configuration.assert_called_once()

def test_list_channels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_channels
    mock_client = MagicMock()
    mock_client.list_channels.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_channels(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_channels.assert_called_once()

def test_list_dashboards_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_dashboards
    mock_client = MagicMock()
    mock_client.list_dashboards.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_dashboards(name_prefix="test-name_prefix", type_value="test-type_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dashboards.assert_called_once()

def test_list_import_failures_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_import_failures
    mock_client = MagicMock()
    mock_client.list_import_failures.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_import_failures(1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_import_failures.assert_called_once()

def test_list_imports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_imports
    mock_client = MagicMock()
    mock_client.list_imports.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_imports(max_results=1, destination="test-destination", import_status=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_imports.assert_called_once()

def test_list_insights_metric_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_insights_metric_data
    mock_client = MagicMock()
    mock_client.list_insights_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_insights_metric_data("test-event_source", "test-event_name", "test-insight_type", error_code="test-error_code", start_time="test-start_time", end_time="test-end_time", period="test-period", data_type="test-data_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_insights_metric_data.assert_called_once()

def test_list_public_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_public_keys
    mock_client = MagicMock()
    mock_client.list_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_public_keys(start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_public_keys.assert_called_once()

def test_list_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import list_tags
    mock_client = MagicMock()
    mock_client.list_tags.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    list_tags("test-resource_id_list", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags.assert_called_once()

def test_put_event_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import put_event_configuration
    mock_client = MagicMock()
    mock_client.put_event_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    put_event_configuration(1, {}, event_data_store="test-event_data_store", region_name="us-east-1")
    mock_client.put_event_configuration.assert_called_once()

def test_search_sample_queries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import search_sample_queries
    mock_client = MagicMock()
    mock_client.search_sample_queries.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    search_sample_queries("test-search_phrase", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.search_sample_queries.assert_called_once()

def test_start_dashboard_refresh_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import start_dashboard_refresh
    mock_client = MagicMock()
    mock_client.start_dashboard_refresh.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    start_dashboard_refresh("test-dashboard_id", query_parameter_values="test-query_parameter_values", region_name="us-east-1")
    mock_client.start_dashboard_refresh.assert_called_once()

def test_start_import_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import start_import
    mock_client = MagicMock()
    mock_client.start_import.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    start_import(destinations="test-destinations", import_source=1, start_event_time="test-start_event_time", end_event_time="test-end_event_time", import_id=1, region_name="us-east-1")
    mock_client.start_import.assert_called_once()

def test_update_channel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import update_channel
    mock_client = MagicMock()
    mock_client.update_channel.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_channel("test-channel", destinations="test-destinations", name="test-name", region_name="us-east-1")
    mock_client.update_channel.assert_called_once()

def test_update_dashboard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import update_dashboard
    mock_client = MagicMock()
    mock_client.update_dashboard.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_dashboard("test-dashboard_id", widgets="test-widgets", refresh_schedule="test-refresh_schedule", termination_protection_enabled="test-termination_protection_enabled", region_name="us-east-1")
    mock_client.update_dashboard.assert_called_once()

def test_update_event_data_store_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cloudtrail import update_event_data_store
    mock_client = MagicMock()
    mock_client.update_event_data_store.return_value = {}
    monkeypatch.setattr("aws_util.cloudtrail.get_client", lambda *a, **kw: mock_client)
    update_event_data_store("test-event_data_store", name="test-name", advanced_event_selectors="test-advanced_event_selectors", multi_region_enabled=True, organization_enabled="test-organization_enabled", retention_period="test-retention_period", termination_protection_enabled="test-termination_protection_enabled", kms_key_id="test-kms_key_id", billing_mode="test-billing_mode", region_name="us-east-1")
    mock_client.update_event_data_store.assert_called_once()
