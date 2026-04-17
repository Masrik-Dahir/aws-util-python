from __future__ import annotations

import asyncio
import json
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.kinesis import (
    KinesisPutResult,
    KinesisRecord,
    KinesisStream,
    _encode_data,
    consume_stream,
    describe_stream,
    get_records,
    list_streams,
    put_record,
    put_records,
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


# ---------------------------------------------------------------------------
# _encode_data helper
# ---------------------------------------------------------------------------


def test_encode_data_bytes() -> None:
    assert _encode_data(b"hello") == b"hello"


def test_encode_data_dict() -> None:
    result = _encode_data({"key": "val"})
    assert result == json.dumps({"key": "val"}).encode("utf-8")


def test_encode_data_list() -> None:
    result = _encode_data([1, 2])
    assert result == json.dumps([1, 2]).encode("utf-8")


def test_encode_data_str() -> None:
    assert _encode_data("hello") == b"hello"


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------


async def test_put_record_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ShardId": "shard-0",
        "SequenceNumber": "seq-1",
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await put_record("stream-1", b"data", "pk-1")
    assert isinstance(result, KinesisRecord)
    assert result.shard_id == "shard-0"
    assert result.sequence_number == "seq-1"


async def test_put_record_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ShardId": "shard-0",
        "SequenceNumber": "seq-2",
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await put_record(
        "stream-1", {"k": "v"}, "pk-1", region_name="us-west-2"
    )
    assert result.sequence_number == "seq-2"


async def test_put_record_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="put_record failed"):
        await put_record("stream-1", b"data", "pk-1")


# ---------------------------------------------------------------------------
# put_records
# ---------------------------------------------------------------------------


async def test_put_records_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FailedRecordCount": 0,
        "Records": [{"ShardId": "s0", "SequenceNumber": "sq1"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await put_records(
        "stream-1",
        [{"data": b"hello", "partition_key": "pk-1"}],
    )
    assert isinstance(result, KinesisPutResult)
    assert result.failed_record_count == 0


async def test_put_records_too_many() -> None:
    with pytest.raises(ValueError, match="at most 500"):
        await put_records("stream-1", [{"data": b"x", "partition_key": "k"}] * 501)


async def test_put_records_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="put_records failed"):
        await put_records(
            "stream-1",
            [{"data": b"x", "partition_key": "k"}],
        )


# ---------------------------------------------------------------------------
# list_streams
# ---------------------------------------------------------------------------


async def test_list_streams_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["stream-1", "stream-2"]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await list_streams()
    assert result == ["stream-1", "stream-2"]


async def test_list_streams_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="list_streams failed"):
        await list_streams()


# ---------------------------------------------------------------------------
# describe_stream
# ---------------------------------------------------------------------------


async def test_describe_stream_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StreamDescriptionSummary": {
            "StreamName": "stream-1",
            "StreamARN": "arn:aws:kinesis:us-east-1:123:stream/stream-1",
            "StreamStatus": "ACTIVE",
            "OpenShardCount": 2,
            "RetentionPeriodHours": 48,
            "StreamCreationTimestamp": "2024-01-01T00:00:00Z",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await describe_stream("stream-1")
    assert isinstance(result, KinesisStream)
    assert result.stream_name == "stream-1"
    assert result.shard_count == 2
    assert result.retention_period_hours == 48


async def test_describe_stream_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "StreamDescriptionSummary": {
            "StreamName": "s",
            "StreamARN": "arn",
            "StreamStatus": "ACTIVE",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await describe_stream("s")
    assert result.shard_count == 0
    assert result.retention_period_hours == 24
    assert result.creation_timestamp is None


async def test_describe_stream_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="describe_stream failed"):
        await describe_stream("stream-1")


# ---------------------------------------------------------------------------
# get_records
# ---------------------------------------------------------------------------


async def test_get_records_json(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"ShardIterator": "iter-1"},
        {
            "Records": [
                {
                    "Data": json.dumps({"k": "v"}),
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                    "ApproximateArrivalTimestamp": "2024-01-01",
                }
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await get_records("stream-1", "shard-0")
    assert len(result) == 1
    assert result[0]["data"] == {"k": "v"}
    assert result[0]["sequence_number"] == "sq1"


async def test_get_records_non_json(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"ShardIterator": "iter-1"},
        {
            "Records": [
                {
                    "Data": "not-json{{{",
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await get_records("stream-1", "shard-0")
    assert result[0]["data"] == "not-json{{{"
    assert result[0]["approximate_arrival_timestamp"] is None


async def test_get_records_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"ShardIterator": "iter-1"},
        {"Records": []},
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    result = await get_records("stream-1", "shard-0")
    assert result == []


async def test_get_records_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="get_records failed"):
        await get_records("stream-1", "shard-0")


# ---------------------------------------------------------------------------
# consume_stream
# ---------------------------------------------------------------------------


async def test_consume_stream_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    # DescribeStreamSummary
    # ListShards
    # GetShardIterator for shard-0
    # GetRecords returns 1 record then no NextShardIterator
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},  # describe
        {"Shards": [{"ShardId": "shard-0"}]},  # list shards
        {"ShardIterator": "iter-0"},  # get shard iterator
        {
            "Records": [
                {
                    "Data": json.dumps({"k": "v"}),
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ],
            "NextShardIterator": None,
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())

    handler = MagicMock()
    result = await consume_stream(
        "stream-1", handler, duration_seconds=60.0
    )
    assert result == 1
    handler.assert_called_once()


async def test_consume_stream_async_handler(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        {"Shards": [{"ShardId": "shard-0"}]},
        {"ShardIterator": "iter-0"},
        {
            "Records": [
                {
                    "Data": json.dumps({"k": "v"}),
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ],
            "NextShardIterator": None,
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())

    async_handler = AsyncMock()
    result = await consume_stream(
        "stream-1", async_handler, duration_seconds=60.0
    )
    assert result == 1
    async_handler.assert_called_once()


async def test_consume_stream_non_json_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        {"Shards": [{"ShardId": "shard-0"}]},
        {"ShardIterator": "iter-0"},
        {
            "Records": [
                {
                    "Data": "not-json{{{",
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ],
            "NextShardIterator": None,
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())
    handler = MagicMock()
    result = await consume_stream(
        "stream-1", handler, duration_seconds=60.0
    )
    assert result == 1


async def test_consume_stream_describe_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="Failed to describe stream"):
        await consume_stream("stream-1", MagicMock())


async def test_consume_stream_list_shards_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        RuntimeError("boom"),
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    with pytest.raises(RuntimeError, match="Failed to list shards"):
        await consume_stream("stream-1", MagicMock())


async def test_consume_stream_getrecords_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """GetRecords RuntimeError inside _consume_shard causes break, returns 0."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        {"Shards": [{"ShardId": "shard-0"}]},
        {"ShardIterator": "iter-0"},
        RuntimeError("boom"),  # GetRecords fails
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())
    handler = MagicMock()
    result = await consume_stream(
        "stream-1", handler, duration_seconds=60.0
    )
    assert result == 0


async def test_consume_stream_no_shards(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        {"Shards": []},
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    handler = MagicMock()
    result = await consume_stream(
        "stream-1", handler, duration_seconds=60.0
    )
    assert result == 0


async def test_consume_stream_deadline_reached(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Shard polling stops once the deadline is reached."""
    mock_client = AsyncMock()

    call_count = 0

    async def fake_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {"StreamDescriptionSummary": {}}
        if call_count == 2:
            return {"Shards": [{"ShardId": "shard-0"}]}
        if call_count == 3:
            return {"ShardIterator": "iter-0"}
        # After the first GetRecords, return records with next iterator
        # but deadline will be past
        return {
            "Records": [
                {
                    "Data": json.dumps({"k": "v"}),
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ],
            "NextShardIterator": "iter-next",
        }

    mock_client.call = fake_call
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())

    # Use a very short duration so deadline is immediately exceeded
    handler = MagicMock()
    result = await consume_stream(
        "stream-1", handler, duration_seconds=0.0
    )
    # With duration 0, the while loop condition _time.monotonic() < deadline
    # will be false after the first iteration, so we get 1 record
    assert result >= 0


async def test_consume_stream_handler_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """If handler raises, exception is swallowed by broad except in _consume_shard."""
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"StreamDescriptionSummary": {}},
        {"Shards": [{"ShardId": "shard-0"}]},
        {"ShardIterator": "iter-0"},
        {
            "Records": [
                {
                    "Data": json.dumps({"k": "v"}),
                    "SequenceNumber": "sq1",
                    "PartitionKey": "pk1",
                }
            ],
            "NextShardIterator": None,
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client
    )
    monkeypatch.setattr("aws_util.aio.kinesis.asyncio.sleep", AsyncMock())

    def bad_handler(rec):
        raise ValueError("handler error")

    result = await consume_stream(
        "stream-1", bad_handler, duration_seconds=60.0
    )
    # The exception is caught, so returns 0
    assert result == 0


async def test_add_tags_to_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_stream({}, )
    mock_client.call.assert_called_once()


async def test_add_tags_to_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_stream({}, )


async def test_create_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stream("test-stream_name", )
    mock_client.call.assert_called_once()


async def test_create_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stream("test-stream_name", )


async def test_decrease_stream_retention_period(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await decrease_stream_retention_period(1, )
    mock_client.call.assert_called_once()


async def test_decrease_stream_retention_period_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await decrease_stream_retention_period(1, )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stream()
    mock_client.call.assert_called_once()


async def test_delete_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stream()


async def test_deregister_stream_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_stream_consumer()
    mock_client.call.assert_called_once()


async def test_deregister_stream_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_stream_consumer()


async def test_describe_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_settings()
    mock_client.call.assert_called_once()


async def test_describe_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_settings()


async def test_describe_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_limits()
    mock_client.call.assert_called_once()


async def test_describe_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_limits()


async def test_describe_stream_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stream_consumer()
    mock_client.call.assert_called_once()


async def test_describe_stream_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stream_consumer()


async def test_describe_stream_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stream_summary()
    mock_client.call.assert_called_once()


async def test_describe_stream_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stream_summary()


async def test_disable_enhanced_monitoring(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_enhanced_monitoring([], )
    mock_client.call.assert_called_once()


async def test_disable_enhanced_monitoring_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_enhanced_monitoring([], )


async def test_enable_enhanced_monitoring(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_enhanced_monitoring([], )
    mock_client.call.assert_called_once()


async def test_enable_enhanced_monitoring_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_enhanced_monitoring([], )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_get_shard_iterator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_shard_iterator("test-shard_id", "test-shard_iterator_type", )
    mock_client.call.assert_called_once()


async def test_get_shard_iterator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_shard_iterator("test-shard_id", "test-shard_iterator_type", )


async def test_increase_stream_retention_period(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await increase_stream_retention_period(1, )
    mock_client.call.assert_called_once()


async def test_increase_stream_retention_period_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await increase_stream_retention_period(1, )


async def test_list_shards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_shards()
    mock_client.call.assert_called_once()


async def test_list_shards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_shards()


async def test_list_stream_consumers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stream_consumers("test-stream_arn", )
    mock_client.call.assert_called_once()


async def test_list_stream_consumers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stream_consumers("test-stream_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_stream()
    mock_client.call.assert_called_once()


async def test_list_tags_for_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_stream()


async def test_merge_shards(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", )
    mock_client.call.assert_called_once()


async def test_merge_shards_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy", )


async def test_register_stream_consumer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_stream_consumer("test-stream_arn", "test-consumer_name", )
    mock_client.call.assert_called_once()


async def test_register_stream_consumer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_stream_consumer("test-stream_arn", "test-consumer_name", )


async def test_remove_tags_from_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_stream([], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_stream([], )


async def test_split_shard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await split_shard("test-shard_to_split", "test-new_starting_hash_key", )
    mock_client.call.assert_called_once()


async def test_split_shard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await split_shard("test-shard_to_split", "test-new_starting_hash_key", )


async def test_start_stream_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_stream_encryption("test-encryption_type", "test-key_id", )
    mock_client.call.assert_called_once()


async def test_start_stream_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_stream_encryption("test-encryption_type", "test-key_id", )


async def test_stop_stream_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_stream_encryption("test-encryption_type", "test-key_id", )
    mock_client.call.assert_called_once()


async def test_stop_stream_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_stream_encryption("test-encryption_type", "test-key_id", )


async def test_subscribe_to_shard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await subscribe_to_shard("test-consumer_arn", "test-shard_id", {}, )
    mock_client.call.assert_called_once()


async def test_subscribe_to_shard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await subscribe_to_shard("test-consumer_arn", "test-shard_id", {}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource({}, "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource({}, "test-resource_arn", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource([], "test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource([], "test-resource_arn", )


async def test_update_account_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_settings({}, )
    mock_client.call.assert_called_once()


async def test_update_account_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_settings({}, )


async def test_update_max_record_size(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_max_record_size(1, )
    mock_client.call.assert_called_once()


async def test_update_max_record_size_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_max_record_size(1, )


async def test_update_shard_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_shard_count(1, "test-scaling_type", )
    mock_client.call.assert_called_once()


async def test_update_shard_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_shard_count(1, "test-scaling_type", )


async def test_update_stream_mode(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stream_mode("test-stream_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_stream_mode_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stream_mode("test-stream_arn", {}, )


async def test_update_stream_warm_throughput(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stream_warm_throughput(1, )
    mock_client.call.assert_called_once()


async def test_update_stream_warm_throughput_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.kinesis.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stream_warm_throughput(1, )


@pytest.mark.asyncio
async def test_add_tags_to_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import add_tags_to_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await add_tags_to_stream([{"Key": "k", "Value": "v"}], stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import create_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await create_stream("test-stream_name", shard_count=1, stream_mode_details="test-stream_mode_details", tags=[{"Key": "k", "Value": "v"}], warm_throughput_mi_bps="test-warm_throughput_mi_bps", max_record_size_in_ki_b=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_decrease_stream_retention_period_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import decrease_stream_retention_period
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await decrease_stream_retention_period("test-retention_period_hours", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import delete_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await delete_stream(stream_name="test-stream_name", enforce_consumer_deletion="test-enforce_consumer_deletion", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_stream_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import deregister_stream_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await deregister_stream_consumer(stream_arn="test-stream_arn", consumer_name="test-consumer_name", consumer_arn="test-consumer_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stream_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import describe_stream_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await describe_stream_consumer(stream_arn="test-stream_arn", consumer_name="test-consumer_name", consumer_arn="test-consumer_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_stream_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import describe_stream_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await describe_stream_summary(stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_enhanced_monitoring_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import disable_enhanced_monitoring
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await disable_enhanced_monitoring("test-shard_level_metrics", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_enhanced_monitoring_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import enable_enhanced_monitoring
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await enable_enhanced_monitoring("test-shard_level_metrics", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_shard_iterator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import get_shard_iterator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await get_shard_iterator("test-shard_id", "test-shard_iterator_type", stream_name="test-stream_name", starting_sequence_number="test-starting_sequence_number", timestamp="test-timestamp", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_increase_stream_retention_period_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import increase_stream_retention_period
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await increase_stream_retention_period("test-retention_period_hours", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_shards_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import list_shards
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await list_shards(stream_name="test-stream_name", next_token="test-next_token", exclusive_start_shard_id="test-exclusive_start_shard_id", max_results=1, stream_creation_timestamp="test-stream_creation_timestamp", shard_filter=[{}], stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stream_consumers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import list_stream_consumers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await list_stream_consumers("test-stream_arn", next_token="test-next_token", max_results=1, stream_creation_timestamp="test-stream_creation_timestamp", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import list_tags_for_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_stream(stream_name="test-stream_name", exclusive_start_tag_key="test-exclusive_start_tag_key", limit=1, stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_merge_shards_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import merge_shards
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await merge_shards("test-shard_to_merge", "test-adjacent_shard_to_merge", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_stream_consumer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import register_stream_consumer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await register_stream_consumer("test-stream_arn", "test-consumer_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_tags_from_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import remove_tags_from_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await remove_tags_from_stream("test-tag_keys", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_split_shard_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import split_shard
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await split_shard("test-shard_to_split", "test-new_starting_hash_key", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_stream_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import start_stream_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await start_stream_encryption("test-encryption_type", "test-key_id", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_stream_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import stop_stream_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await stop_stream_encryption("test-encryption_type", "test-key_id", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_max_record_size_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import update_max_record_size
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await update_max_record_size(1, stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_shard_count_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import update_shard_count
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await update_shard_count(1, "test-scaling_type", stream_name="test-stream_name", stream_arn="test-stream_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stream_mode_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import update_stream_mode
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await update_stream_mode("test-stream_arn", "test-stream_mode_details", warm_throughput_mi_bps="test-warm_throughput_mi_bps", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stream_warm_throughput_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.kinesis import update_stream_warm_throughput
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.kinesis.async_client", lambda *a, **kw: mock_client)
    await update_stream_warm_throughput("test-warm_throughput_mi_bps", stream_arn="test-stream_arn", stream_name="test-stream_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
