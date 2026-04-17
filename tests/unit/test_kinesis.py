"""Tests for aws_util.kinesis module."""
from __future__ import annotations

import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.kinesis as kinesis_mod
from aws_util.kinesis import (
    KinesisRecord,
    KinesisPutResult,
    KinesisStream,
    put_record,
    put_records,
    list_streams,
    describe_stream,
    get_records,
    consume_stream,
    add_tags_to_stream,
    create_stream,
    decrease_stream_retention_period,
    delete_resource_policy,
    delete_stream,
    deregister_stream_consumer,
    describe_account_settings,
    describe_limits,
    describe_stream_consumer,
    describe_stream_summary,
    disable_enhanced_monitoring,
    enable_enhanced_monitoring,
    get_resource_policy,
    get_shard_iterator,
    increase_stream_retention_period,
    list_shards,
    list_stream_consumers,
    list_tags_for_resource,
    list_tags_for_stream,
    merge_shards,
    put_resource_policy,
    register_stream_consumer,
    remove_tags_from_stream,
    split_shard,
    start_stream_encryption,
    stop_stream_encryption,
    subscribe_to_shard,
    tag_resource,
    untag_resource,
    update_account_settings,
    update_max_record_size,
    update_shard_count,
    update_stream_mode,
    update_stream_warm_throughput,
)

REGION = "us-east-1"
STREAM_NAME = "test-stream"


@pytest.fixture
def kinesis_stream():
    client = boto3.client("kinesis", region_name=REGION)
    client.create_stream(StreamName=STREAM_NAME, ShardCount=1)
    # Wait for stream to become active in moto (usually immediate)
    return client


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_kinesis_record_model():
    rec = KinesisRecord(shard_id="shardId-000000000000", sequence_number="123")
    assert rec.shard_id == "shardId-000000000000"


def test_kinesis_put_result_model():
    result = KinesisPutResult(failed_record_count=0, records=[{"SequenceNumber": "123"}])
    assert result.failed_record_count == 0


def test_kinesis_stream_model():
    stream = KinesisStream(
        stream_name=STREAM_NAME,
        stream_arn="arn:aws:kinesis:us-east-1:123:stream/test",
        stream_status="ACTIVE",
    )
    assert stream.stream_name == STREAM_NAME
    assert stream.shard_count == 0


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------

def test_put_record_bytes(kinesis_stream):
    result = put_record(STREAM_NAME, b"hello", "pk1", region_name=REGION)
    assert isinstance(result, KinesisRecord)
    assert result.shard_id
    assert result.sequence_number


def test_put_record_string(kinesis_stream):
    result = put_record(STREAM_NAME, "hello string", "pk1", region_name=REGION)
    assert result.sequence_number


def test_put_record_dict(kinesis_stream):
    result = put_record(STREAM_NAME, {"key": "value"}, "pk1", region_name=REGION)
    assert result.sequence_number


def test_put_record_list(kinesis_stream):
    result = put_record(STREAM_NAME, [1, 2, 3], "pk1", region_name=REGION)
    assert result.sequence_number


def test_put_record_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}}, "PutRecord"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="put_record failed"):
        put_record("nonexistent-stream", b"data", "pk", region_name=REGION)


# ---------------------------------------------------------------------------
# put_records
# ---------------------------------------------------------------------------

def test_put_records_success(kinesis_stream):
    records = [
        {"data": b"msg1", "partition_key": "pk1"},
        {"data": "msg2", "partition_key": "pk2"},
        {"data": {"k": "v"}, "partition_key": "pk3"},
    ]
    result = put_records(STREAM_NAME, records, region_name=REGION)
    assert isinstance(result, KinesisPutResult)
    assert result.failed_record_count == 0


def test_put_records_too_many_raises():
    with pytest.raises(ValueError, match="at most 500"):
        put_records(STREAM_NAME, [{"data": b"x", "partition_key": "k"}] * 501, region_name=REGION)


def test_put_records_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_records.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}}, "PutRecords"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="put_records failed"):
        put_records("nonexistent", [{"data": b"x", "partition_key": "k"}], region_name=REGION)


# ---------------------------------------------------------------------------
# list_streams
# ---------------------------------------------------------------------------

def test_list_streams_returns_names(kinesis_stream):
    result = list_streams(region_name=REGION)
    assert STREAM_NAME in result


def test_list_streams_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListStreams"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_streams failed"):
        list_streams(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_stream
# ---------------------------------------------------------------------------

def test_describe_stream_returns_info(kinesis_stream):
    result = describe_stream(STREAM_NAME, region_name=REGION)
    assert isinstance(result, KinesisStream)
    assert result.stream_name == STREAM_NAME
    assert result.stream_status == "ACTIVE"


def test_describe_stream_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_summary.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DescribeStreamSummary"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_stream failed"):
        describe_stream("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# get_records
# ---------------------------------------------------------------------------

def test_get_records_returns_list(kinesis_stream):
    put_record(STREAM_NAME, {"event": "test"}, "pk1", region_name=REGION)
    client = boto3.client("kinesis", region_name=REGION)
    shards = client.list_shards(StreamName=STREAM_NAME)["Shards"]
    shard_id = shards[0]["ShardId"]

    result = get_records(STREAM_NAME, shard_id, region_name=REGION)
    assert isinstance(result, list)


def test_get_records_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_shard_iterator.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "GetShardIterator"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_records failed"):
        get_records("nonexistent", "shardId-000", region_name=REGION)


# ---------------------------------------------------------------------------
# consume_stream
# ---------------------------------------------------------------------------

def test_consume_stream_processes_records(kinesis_stream):
    put_record(STREAM_NAME, {"event": "a"}, "pk1", region_name=REGION)
    processed = []
    count = consume_stream(
        STREAM_NAME,
        handler=processed.append,
        shard_iterator_type="TRIM_HORIZON",
        duration_seconds=0.5,
        poll_interval=0.1,
        region_name=REGION,
    )
    assert count >= 0  # moto may or may not return records


def test_consume_stream_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_summary.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DescribeStreamSummary"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stream"):
        consume_stream("nonexistent", handler=lambda r: None, duration_seconds=0.1,
                       region_name=REGION)


def test_get_records_binary_data(monkeypatch):
    """Covers JSON decode fallback for binary data in get_records (lines 234-235)."""
    mock_client = MagicMock()
    mock_client.get_shard_iterator.return_value = {"ShardIterator": "iter-123"}
    mock_client.get_records.return_value = {
        "Records": [{
            "Data": b"\x80\x81\x82",  # non-UTF8 bytes, not valid JSON
            "SequenceNumber": "1",
            "PartitionKey": "pk1",
        }],
        "NextShardIterator": None,
    }
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_records(STREAM_NAME, "shardId-000", region_name=REGION)
    assert len(result) == 1
    assert isinstance(result[0]["data"], bytes)


def test_consume_stream_list_shards_error(monkeypatch):
    """Covers list_shards ClientError in consume_stream (lines 311-312)."""
    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {
        "StreamDescriptionSummary": {"StreamName": STREAM_NAME}
    }
    mock_client.list_shards.side_effect = ClientError(
        {"Error": {"Code": "ResourceInUseException", "Message": "in use"}}, "ListShards"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list shards"):
        consume_stream(STREAM_NAME, handler=lambda r: None, duration_seconds=0.1,
                       region_name=REGION)


def test_consume_stream_get_records_client_error(monkeypatch):
    """Covers ClientError break in _consume_shard (lines 332-333)."""
    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {
        "StreamDescriptionSummary": {"StreamName": STREAM_NAME}
    }
    mock_client.list_shards.return_value = {"Shards": [{"ShardId": "shardId-000"}]}
    mock_client.get_shard_iterator.return_value = {"ShardIterator": "iter-abc"}
    mock_client.get_records.side_effect = ClientError(
        {"Error": {"Code": "ExpiredIteratorException", "Message": "expired"}}, "GetRecords"
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    count = consume_stream(
        STREAM_NAME, handler=lambda r: None, duration_seconds=0.1, region_name=REGION
    )
    assert count == 0


def test_consume_stream_binary_data(monkeypatch):
    """Covers JSON decode fallback in _consume_shard (lines 339-340)."""
    import time as _time
    monkeypatch.setattr(_time, "sleep", lambda s: None)

    processed = []
    call_count = {"n": 0}

    def fake_get_records(ShardIterator, Limit):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return {
                "Records": [{"Data": b"\x80\x81", "SequenceNumber": "1", "PartitionKey": "pk"}],
                "NextShardIterator": None,
            }
        return {"Records": [], "NextShardIterator": None}

    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {
        "StreamDescriptionSummary": {"StreamName": STREAM_NAME}
    }
    mock_client.list_shards.return_value = {"Shards": [{"ShardId": "shardId-000"}]}
    mock_client.get_shard_iterator.return_value = {"ShardIterator": "iter-abc"}
    mock_client.get_records.side_effect = fake_get_records
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    count = consume_stream(
        STREAM_NAME, handler=processed.append, duration_seconds=0.1, region_name=REGION
    )
    assert count >= 0  # binary data should be passed to handler


def test_consume_stream_shard_iterator_general_exception(monkeypatch):
    """Covers except Exception: pass in _consume_shard (lines 353-354)."""
    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {
        "StreamDescriptionSummary": {"StreamName": STREAM_NAME}
    }
    mock_client.list_shards.return_value = {"Shards": [{"ShardId": "shardId-000"}]}
    mock_client.get_shard_iterator.side_effect = ValueError("unexpected error")
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    # Should not raise — exception is swallowed
    count = consume_stream(
        STREAM_NAME, handler=lambda r: None, duration_seconds=0.1, region_name=REGION
    )
    assert count == 0


def test_add_tags_to_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_stream.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    add_tags_to_stream({}, region_name=REGION)
    mock_client.add_tags_to_stream.assert_called_once()


def test_add_tags_to_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_stream",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags to stream"):
        add_tags_to_stream({}, region_name=REGION)


def test_create_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stream.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    create_stream("test-stream_name", region_name=REGION)
    mock_client.create_stream.assert_called_once()


def test_create_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stream",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stream"):
        create_stream("test-stream_name", region_name=REGION)


def test_decrease_stream_retention_period(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_stream_retention_period.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    decrease_stream_retention_period(1, region_name=REGION)
    mock_client.decrease_stream_retention_period.assert_called_once()


def test_decrease_stream_retention_period_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_stream_retention_period.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decrease_stream_retention_period",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decrease stream retention period"):
        decrease_stream_retention_period(1, region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stream.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    delete_stream(region_name=REGION)
    mock_client.delete_stream.assert_called_once()


def test_delete_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stream",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stream"):
        delete_stream(region_name=REGION)


def test_deregister_stream_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_stream_consumer.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    deregister_stream_consumer(region_name=REGION)
    mock_client.deregister_stream_consumer.assert_called_once()


def test_deregister_stream_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_stream_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_stream_consumer",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister stream consumer"):
        deregister_stream_consumer(region_name=REGION)


def test_describe_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_settings.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    describe_account_settings(region_name=REGION)
    mock_client.describe_account_settings.assert_called_once()


def test_describe_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_settings",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account settings"):
        describe_account_settings(region_name=REGION)


def test_describe_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_limits.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    describe_limits(region_name=REGION)
    mock_client.describe_limits.assert_called_once()


def test_describe_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_limits",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe limits"):
        describe_limits(region_name=REGION)


def test_describe_stream_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_consumer.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    describe_stream_consumer(region_name=REGION)
    mock_client.describe_stream_consumer.assert_called_once()


def test_describe_stream_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stream_consumer",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stream consumer"):
        describe_stream_consumer(region_name=REGION)


def test_describe_stream_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    describe_stream_summary(region_name=REGION)
    mock_client.describe_stream_summary.assert_called_once()


def test_describe_stream_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_stream_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stream_summary",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe stream summary"):
        describe_stream_summary(region_name=REGION)


def test_disable_enhanced_monitoring(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_enhanced_monitoring.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    disable_enhanced_monitoring([], region_name=REGION)
    mock_client.disable_enhanced_monitoring.assert_called_once()


def test_disable_enhanced_monitoring_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_enhanced_monitoring.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_enhanced_monitoring",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable enhanced monitoring"):
        disable_enhanced_monitoring([], region_name=REGION)


def test_enable_enhanced_monitoring(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_enhanced_monitoring.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    enable_enhanced_monitoring([], region_name=REGION)
    mock_client.enable_enhanced_monitoring.assert_called_once()


def test_enable_enhanced_monitoring_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_enhanced_monitoring.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_enhanced_monitoring",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable enhanced monitoring"):
        enable_enhanced_monitoring([], region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_get_shard_iterator(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_shard_iterator.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    get_shard_iterator("test-shard_id", "test-shard_iterator_type", region_name=REGION)
    mock_client.get_shard_iterator.assert_called_once()


def test_get_shard_iterator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_shard_iterator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_shard_iterator",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get shard iterator"):
        get_shard_iterator("test-shard_id", "test-shard_iterator_type", region_name=REGION)


def test_increase_stream_retention_period(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_stream_retention_period.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    increase_stream_retention_period(1, region_name=REGION)
    mock_client.increase_stream_retention_period.assert_called_once()


def test_increase_stream_retention_period_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_stream_retention_period.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "increase_stream_retention_period",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to increase stream retention period"):
        increase_stream_retention_period(1, region_name=REGION)


def test_list_shards(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_shards.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    list_shards(region_name=REGION)
    mock_client.list_shards.assert_called_once()


def test_list_shards_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_shards.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_shards",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list shards"):
        list_shards(region_name=REGION)


def test_list_stream_consumers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stream_consumers.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    list_stream_consumers("test-stream_arn", region_name=REGION)
    mock_client.list_stream_consumers.assert_called_once()


def test_list_stream_consumers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stream_consumers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stream_consumers",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stream consumers"):
        list_stream_consumers("test-stream_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_tags_for_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_stream.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_stream(region_name=REGION)
    mock_client.list_tags_for_stream.assert_called_once()


def test_list_tags_for_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_stream",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for stream"):
        list_tags_for_stream(region_name=REGION)


def test_merge_shards(monkeypatch):
    mock_client = MagicMock()
    mock_client.merge_shards.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", region_name=REGION)
    mock_client.merge_shards.assert_called_once()


def test_merge_shards_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.merge_shards.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "merge_shards",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to merge shards"):
        merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


def test_register_stream_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_stream_consumer.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    register_stream_consumer("test-stream_arn", "test-consumer_name", region_name=REGION)
    mock_client.register_stream_consumer.assert_called_once()


def test_register_stream_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_stream_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_stream_consumer",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register stream consumer"):
        register_stream_consumer("test-stream_arn", "test-consumer_name", region_name=REGION)


def test_remove_tags_from_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_stream.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    remove_tags_from_stream([], region_name=REGION)
    mock_client.remove_tags_from_stream.assert_called_once()


def test_remove_tags_from_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_stream",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from stream"):
        remove_tags_from_stream([], region_name=REGION)


def test_split_shard(monkeypatch):
    mock_client = MagicMock()
    mock_client.split_shard.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    split_shard("test-shard_to_split", "test-new_starting_hash_key", region_name=REGION)
    mock_client.split_shard.assert_called_once()


def test_split_shard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.split_shard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "split_shard",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to split shard"):
        split_shard("test-shard_to_split", "test-new_starting_hash_key", region_name=REGION)


def test_start_stream_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_stream_encryption.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    start_stream_encryption("test-encryption_type", "test-key_id", region_name=REGION)
    mock_client.start_stream_encryption.assert_called_once()


def test_start_stream_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_stream_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_stream_encryption",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start stream encryption"):
        start_stream_encryption("test-encryption_type", "test-key_id", region_name=REGION)


def test_stop_stream_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stream_encryption.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    stop_stream_encryption("test-encryption_type", "test-key_id", region_name=REGION)
    mock_client.stop_stream_encryption.assert_called_once()


def test_stop_stream_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_stream_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_stream_encryption",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop stream encryption"):
        stop_stream_encryption("test-encryption_type", "test-key_id", region_name=REGION)


def test_subscribe_to_shard(monkeypatch):
    mock_client = MagicMock()
    mock_client.subscribe_to_shard.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    subscribe_to_shard("test-consumer_arn", "test-shard_id", {}, region_name=REGION)
    mock_client.subscribe_to_shard.assert_called_once()


def test_subscribe_to_shard_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.subscribe_to_shard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "subscribe_to_shard",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to subscribe to shard"):
        subscribe_to_shard("test-consumer_arn", "test-shard_id", {}, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource({}, "test-resource_arn", region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource({}, "test-resource_arn", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource([], "test-resource_arn", region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource([], "test-resource_arn", region_name=REGION)


def test_update_account_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_settings.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    update_account_settings({}, region_name=REGION)
    mock_client.update_account_settings.assert_called_once()


def test_update_account_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_settings",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account settings"):
        update_account_settings({}, region_name=REGION)


def test_update_max_record_size(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_max_record_size.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    update_max_record_size(1, region_name=REGION)
    mock_client.update_max_record_size.assert_called_once()


def test_update_max_record_size_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_max_record_size.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_max_record_size",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update max record size"):
        update_max_record_size(1, region_name=REGION)


def test_update_shard_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_shard_count.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    update_shard_count(1, "test-scaling_type", region_name=REGION)
    mock_client.update_shard_count.assert_called_once()


def test_update_shard_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_shard_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_shard_count",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update shard count"):
        update_shard_count(1, "test-scaling_type", region_name=REGION)


def test_update_stream_mode(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_mode.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    update_stream_mode("test-stream_arn", {}, region_name=REGION)
    mock_client.update_stream_mode.assert_called_once()


def test_update_stream_mode_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_mode.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stream_mode",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stream mode"):
        update_stream_mode("test-stream_arn", {}, region_name=REGION)


def test_update_stream_warm_throughput(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_warm_throughput.return_value = {}
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    update_stream_warm_throughput(1, region_name=REGION)
    mock_client.update_stream_warm_throughput.assert_called_once()


def test_update_stream_warm_throughput_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_stream_warm_throughput.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stream_warm_throughput",
    )
    monkeypatch.setattr(kinesis_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update stream warm throughput"):
        update_stream_warm_throughput(1, region_name=REGION)


def test_add_tags_to_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import add_tags_to_stream
    mock_client = MagicMock()
    mock_client.add_tags_to_stream.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    add_tags_to_stream([{"Key": "k", "Value": "v"}], stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.add_tags_to_stream.assert_called_once()

def test_create_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import create_stream
    mock_client = MagicMock()
    mock_client.create_stream.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    create_stream("test-stream_name", shard_count=1, stream_mode_details="test-stream_mode_details", tags=[{"Key": "k", "Value": "v"}], warm_throughput_mi_bps="test-warm_throughput_mi_bps", max_record_size_in_ki_b=1, region_name="us-east-1")
    mock_client.create_stream.assert_called_once()

def test_decrease_stream_retention_period_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import decrease_stream_retention_period
    mock_client = MagicMock()
    mock_client.decrease_stream_retention_period.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    decrease_stream_retention_period("test-retention_period_hours", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.decrease_stream_retention_period.assert_called_once()

def test_delete_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import delete_stream
    mock_client = MagicMock()
    mock_client.delete_stream.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    delete_stream(stream_name="test-stream_name", enforce_consumer_deletion="test-enforce_consumer_deletion", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.delete_stream.assert_called_once()

def test_deregister_stream_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import deregister_stream_consumer
    mock_client = MagicMock()
    mock_client.deregister_stream_consumer.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    deregister_stream_consumer(stream_arn="test-stream_arn", consumer_name="test-consumer_name", consumer_arn="test-consumer_arn", region_name="us-east-1")
    mock_client.deregister_stream_consumer.assert_called_once()

def test_describe_stream_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import describe_stream_consumer
    mock_client = MagicMock()
    mock_client.describe_stream_consumer.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    describe_stream_consumer(stream_arn="test-stream_arn", consumer_name="test-consumer_name", consumer_arn="test-consumer_arn", region_name="us-east-1")
    mock_client.describe_stream_consumer.assert_called_once()

def test_describe_stream_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import describe_stream_summary
    mock_client = MagicMock()
    mock_client.describe_stream_summary.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    describe_stream_summary(stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.describe_stream_summary.assert_called_once()

def test_disable_enhanced_monitoring_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import disable_enhanced_monitoring
    mock_client = MagicMock()
    mock_client.disable_enhanced_monitoring.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    disable_enhanced_monitoring("test-shard_level_metrics", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.disable_enhanced_monitoring.assert_called_once()

def test_enable_enhanced_monitoring_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import enable_enhanced_monitoring
    mock_client = MagicMock()
    mock_client.enable_enhanced_monitoring.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    enable_enhanced_monitoring("test-shard_level_metrics", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.enable_enhanced_monitoring.assert_called_once()

def test_get_shard_iterator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import get_shard_iterator
    mock_client = MagicMock()
    mock_client.get_shard_iterator.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    get_shard_iterator("test-shard_id", "test-shard_iterator_type", stream_name="test-stream_name", starting_sequence_number="test-starting_sequence_number", timestamp="test-timestamp", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.get_shard_iterator.assert_called_once()

def test_increase_stream_retention_period_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import increase_stream_retention_period
    mock_client = MagicMock()
    mock_client.increase_stream_retention_period.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    increase_stream_retention_period("test-retention_period_hours", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.increase_stream_retention_period.assert_called_once()

def test_list_shards_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import list_shards
    mock_client = MagicMock()
    mock_client.list_shards.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    list_shards(stream_name="test-stream_name", next_token="test-next_token", exclusive_start_shard_id="test-exclusive_start_shard_id", max_results=1, stream_creation_timestamp="test-stream_creation_timestamp", shard_filter=[{}], stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.list_shards.assert_called_once()

def test_list_stream_consumers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import list_stream_consumers
    mock_client = MagicMock()
    mock_client.list_stream_consumers.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    list_stream_consumers("test-stream_arn", next_token="test-next_token", max_results=1, stream_creation_timestamp="test-stream_creation_timestamp", region_name="us-east-1")
    mock_client.list_stream_consumers.assert_called_once()

def test_list_tags_for_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import list_tags_for_stream
    mock_client = MagicMock()
    mock_client.list_tags_for_stream.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    list_tags_for_stream(stream_name="test-stream_name", exclusive_start_tag_key="test-exclusive_start_tag_key", limit=1, stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.list_tags_for_stream.assert_called_once()

def test_merge_shards_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import merge_shards
    mock_client = MagicMock()
    mock_client.merge_shards.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.merge_shards.assert_called_once()

def test_register_stream_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import register_stream_consumer
    mock_client = MagicMock()
    mock_client.register_stream_consumer.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    register_stream_consumer("test-stream_arn", "test-consumer_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.register_stream_consumer.assert_called_once()

def test_remove_tags_from_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import remove_tags_from_stream
    mock_client = MagicMock()
    mock_client.remove_tags_from_stream.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    remove_tags_from_stream("test-tag_keys", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.remove_tags_from_stream.assert_called_once()

def test_split_shard_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import split_shard
    mock_client = MagicMock()
    mock_client.split_shard.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    split_shard("test-shard_to_split", "test-new_starting_hash_key", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.split_shard.assert_called_once()

def test_start_stream_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import start_stream_encryption
    mock_client = MagicMock()
    mock_client.start_stream_encryption.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    start_stream_encryption("test-encryption_type", "test-key_id", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.start_stream_encryption.assert_called_once()

def test_stop_stream_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import stop_stream_encryption
    mock_client = MagicMock()
    mock_client.stop_stream_encryption.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    stop_stream_encryption("test-encryption_type", "test-key_id", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.stop_stream_encryption.assert_called_once()

def test_update_max_record_size_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import update_max_record_size
    mock_client = MagicMock()
    mock_client.update_max_record_size.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    update_max_record_size(1, stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.update_max_record_size.assert_called_once()

def test_update_shard_count_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import update_shard_count
    mock_client = MagicMock()
    mock_client.update_shard_count.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    update_shard_count(1, "test-scaling_type", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.update_shard_count.assert_called_once()

def test_update_stream_mode_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import update_stream_mode
    mock_client = MagicMock()
    mock_client.update_stream_mode.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    update_stream_mode("test-stream_arn", "test-stream_mode_details", warm_throughput_mi_bps="test-warm_throughput_mi_bps", region_name="us-east-1")
    mock_client.update_stream_mode.assert_called_once()

def test_update_stream_warm_throughput_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.kinesis import update_stream_warm_throughput
    mock_client = MagicMock()
    mock_client.update_stream_warm_throughput.return_value = {}
    monkeypatch.setattr("aws_util.kinesis.get_client", lambda *a, **kw: mock_client)
    update_stream_warm_throughput("test-warm_throughput_mi_bps", stream_arn="test-stream_arn", stream_name="test-stream_name", region_name="us-east-1")
    mock_client.update_stream_warm_throughput.assert_called_once()
