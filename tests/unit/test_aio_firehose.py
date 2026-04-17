from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.firehose import (
    DeliveryStream,
    FirehosePutResult,
    _encode,
    describe_delivery_stream,
    list_delivery_streams,
    put_record,
    put_record_batch,
    put_record_batch_with_retry,
    create_delivery_stream,
    delete_delivery_stream,
    list_tags_for_delivery_stream,
    start_delivery_stream_encryption,
    stop_delivery_stream_encryption,
    tag_delivery_stream,
    untag_delivery_stream,
    update_destination,
)


# ---------------------------------------------------------------------------
# _encode helper
# ---------------------------------------------------------------------------


def test_encode_bytes() -> None:
    assert _encode(b"hello") == b"hello"


def test_encode_dict() -> None:
    result = _encode({"key": "val"})
    assert result == (json.dumps({"key": "val"}) + "\n").encode("utf-8")


def test_encode_list() -> None:
    result = _encode([1, 2])
    assert result == (json.dumps([1, 2]) + "\n").encode("utf-8")


def test_encode_str_with_newline() -> None:
    assert _encode("hello\n") == b"hello\n"


def test_encode_str_without_newline() -> None:
    assert _encode("hello") == b"hello\n"


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------


async def test_put_record_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"RecordId": "rec-1"}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await put_record("my-stream", b"data")
    assert result == "rec-1"


async def test_put_record_with_dict(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"RecordId": "rec-2"}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await put_record("my-stream", {"a": 1}, region_name="us-west-2")
    assert result == "rec-2"


async def test_put_record_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="put_record failed"):
        await put_record("my-stream", b"data")


# ---------------------------------------------------------------------------
# put_record_batch
# ---------------------------------------------------------------------------


async def test_put_record_batch_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FailedPutCount": 0,
        "RequestResponses": [{"RecordId": "r1"}, {"RecordId": "r2"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await put_record_batch("my-stream", [b"a", "b"])
    assert isinstance(result, FirehosePutResult)
    assert result.failed_put_count == 0
    assert result.all_succeeded is True


async def test_put_record_batch_too_many() -> None:
    with pytest.raises(ValueError, match="at most 500"):
        await put_record_batch("my-stream", [b"x"] * 501)


async def test_put_record_batch_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="put_record_batch failed"):
        await put_record_batch("my-stream", [b"a"])


# ---------------------------------------------------------------------------
# list_delivery_streams
# ---------------------------------------------------------------------------


async def test_list_delivery_streams_single_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "DeliveryStreamNames": ["s1", "s2"],
        "HasMoreDeliveryStreams": False,
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_delivery_streams()
    assert result == ["s1", "s2"]


async def test_list_delivery_streams_paginated(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "DeliveryStreamNames": ["s1"],
            "HasMoreDeliveryStreams": True,
        },
        {
            "DeliveryStreamNames": ["s2"],
            "HasMoreDeliveryStreams": False,
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_delivery_streams(delivery_stream_type="DirectPut")
    assert result == ["s1", "s2"]


async def test_list_delivery_streams_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_delivery_streams failed"):
        await list_delivery_streams()


# ---------------------------------------------------------------------------
# describe_delivery_stream
# ---------------------------------------------------------------------------


async def test_describe_delivery_stream_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "DeliveryStreamDescription": {
            "DeliveryStreamName": "my-stream",
            "DeliveryStreamARN": "arn:aws:firehose:us-east-1:123:deliverystream/my-stream",
            "DeliveryStreamStatus": "ACTIVE",
            "DeliveryStreamType": "DirectPut",
            "CreateTimestamp": "2024-01-01T00:00:00Z",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_delivery_stream("my-stream")
    assert isinstance(result, DeliveryStream)
    assert result.delivery_stream_name == "my-stream"
    assert result.create_timestamp is not None


async def test_describe_delivery_stream_no_timestamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "DeliveryStreamDescription": {
            "DeliveryStreamName": "my-stream",
            "DeliveryStreamARN": "arn:aws:firehose:us-east-1:123:deliverystream/my-stream",
            "DeliveryStreamStatus": "ACTIVE",
            "DeliveryStreamType": "DirectPut",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await describe_delivery_stream("my-stream")
    assert result.create_timestamp is None


async def test_describe_delivery_stream_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="describe_delivery_stream failed"):
        await describe_delivery_stream("my-stream")


# ---------------------------------------------------------------------------
# put_record_batch_with_retry
# ---------------------------------------------------------------------------


async def test_put_record_batch_with_retry_all_succeed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FailedPutCount": 0,
        "RequestResponses": [{"RecordId": "r1"}, {"RecordId": "r2"}],
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await put_record_batch_with_retry("my-stream", [b"a", b"b"])
    assert result == 2


async def test_put_record_batch_with_retry_partial_then_succeed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    # First call: 1 fails, 1 succeeds
    # Second call: remaining 1 succeeds
    mock_client.call.side_effect = [
        {
            "FailedPutCount": 1,
            "RequestResponses": [
                {"RecordId": "r1"},
                {"ErrorCode": "InternalFailure", "ErrorMessage": "err"},
            ],
        },
        {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": "r2"}],
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await put_record_batch_with_retry("my-stream", [b"a", b"b"])
    assert result == 2


async def test_put_record_batch_with_retry_exhausted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FailedPutCount": 1,
        "RequestResponses": [
            {"ErrorCode": "InternalFailure", "ErrorMessage": "err"},
        ],
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="still failing after"):
        await put_record_batch_with_retry(
            "my-stream", [b"a"], max_retries=1
        )


async def test_put_record_batch_with_retry_chunked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify records are split into 500-record chunks."""
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "FailedPutCount": 0,
        "RequestResponses": [{"RecordId": f"r{i}"} for i in range(500)],
    }
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    records = [b"x"] * 600
    # Second chunk has 100 records
    mock_client.call.side_effect = [
        {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": f"r{i}"} for i in range(500)],
        },
        {
            "FailedPutCount": 0,
            "RequestResponses": [{"RecordId": f"r{i}"} for i in range(100)],
        },
    ]
    result = await put_record_batch_with_retry("my-stream", records)
    assert result == 600


async def test_create_delivery_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_delivery_stream("test-delivery_stream_name", )
    mock_client.call.assert_called_once()


async def test_create_delivery_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_delivery_stream("test-delivery_stream_name", )


async def test_delete_delivery_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_delivery_stream("test-delivery_stream_name", )
    mock_client.call.assert_called_once()


async def test_delete_delivery_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_delivery_stream("test-delivery_stream_name", )


async def test_list_tags_for_delivery_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_delivery_stream("test-delivery_stream_name", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_delivery_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_delivery_stream("test-delivery_stream_name", )


async def test_start_delivery_stream_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_delivery_stream_encryption("test-delivery_stream_name", )
    mock_client.call.assert_called_once()


async def test_start_delivery_stream_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_delivery_stream_encryption("test-delivery_stream_name", )


async def test_stop_delivery_stream_encryption(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_delivery_stream_encryption("test-delivery_stream_name", )
    mock_client.call.assert_called_once()


async def test_stop_delivery_stream_encryption_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_delivery_stream_encryption("test-delivery_stream_name", )


async def test_tag_delivery_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_delivery_stream("test-delivery_stream_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_delivery_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_delivery_stream("test-delivery_stream_name", [], )


async def test_untag_delivery_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_delivery_stream("test-delivery_stream_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_delivery_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_delivery_stream("test-delivery_stream_name", [], )


async def test_update_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", )
    mock_client.call.assert_called_once()


async def test_update_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.firehose.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", )


@pytest.mark.asyncio
async def test_create_delivery_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.firehose import create_delivery_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.firehose.async_client", lambda *a, **kw: mock_client)
    await create_delivery_stream("test-delivery_stream_name", delivery_stream_type="test-delivery_stream_type", direct_put_source_configuration={}, kinesis_stream_source_configuration={}, delivery_stream_encryption_configuration_input={}, s3_destination_configuration={}, extended_s3_destination_configuration={}, redshift_destination_configuration={}, elasticsearch_destination_configuration={}, amazonopensearchservice_destination_configuration={}, splunk_destination_configuration={}, http_endpoint_destination_configuration={}, tags=[{"Key": "k", "Value": "v"}], amazon_open_search_serverless_destination_configuration={}, msk_source_configuration={}, snowflake_destination_configuration={}, iceberg_destination_configuration={}, database_source_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_delivery_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.firehose import delete_delivery_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.firehose.async_client", lambda *a, **kw: mock_client)
    await delete_delivery_stream("test-delivery_stream_name", allow_force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_delivery_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.firehose import list_tags_for_delivery_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.firehose.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_delivery_stream("test-delivery_stream_name", exclusive_start_tag_key="test-exclusive_start_tag_key", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_delivery_stream_encryption_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.firehose import start_delivery_stream_encryption
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.firehose.async_client", lambda *a, **kw: mock_client)
    await start_delivery_stream_encryption("test-delivery_stream_name", delivery_stream_encryption_configuration_input={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.firehose import update_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.firehose.async_client", lambda *a, **kw: mock_client)
    await update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", s3_destination_update="test-s3_destination_update", extended_s3_destination_update="test-extended_s3_destination_update", redshift_destination_update="test-redshift_destination_update", elasticsearch_destination_update="test-elasticsearch_destination_update", amazonopensearchservice_destination_update="test-amazonopensearchservice_destination_update", splunk_destination_update="test-splunk_destination_update", http_endpoint_destination_update="test-http_endpoint_destination_update", amazon_open_search_serverless_destination_update="test-amazon_open_search_serverless_destination_update", snowflake_destination_update="test-snowflake_destination_update", iceberg_destination_update="test-iceberg_destination_update", region_name="us-east-1")
    mock_client.call.assert_called_once()
