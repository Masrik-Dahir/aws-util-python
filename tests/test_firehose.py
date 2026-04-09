"""Tests for aws_util.firehose module."""
from __future__ import annotations

import json
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.firehose as firehose_mod
from aws_util.firehose import (
    FirehosePutResult,
    DeliveryStream,
    put_record,
    put_record_batch,
    list_delivery_streams,
    describe_delivery_stream,
    put_record_batch_with_retry,
    _encode,
    create_delivery_stream,
    delete_delivery_stream,
    list_tags_for_delivery_stream,
    start_delivery_stream_encryption,
    stop_delivery_stream_encryption,
    tag_delivery_stream,
    untag_delivery_stream,
    update_destination,
)

REGION = "us-east-1"
STREAM_NAME = "test-delivery-stream"


# ---------------------------------------------------------------------------
# _encode helper
# ---------------------------------------------------------------------------

def test_encode_bytes_passthrough():
    assert _encode(b"hello") == b"hello"


def test_encode_str_adds_newline():
    assert _encode("hello") == b"hello\n"


def test_encode_str_already_has_newline():
    assert _encode("hello\n") == b"hello\n"


def test_encode_dict():
    result = _encode({"key": "value"})
    assert result.endswith(b"\n")
    parsed = json.loads(result.decode("utf-8").strip())
    assert parsed == {"key": "value"}


def test_encode_list():
    result = _encode([1, 2, 3])
    assert result.endswith(b"\n")
    parsed = json.loads(result.decode("utf-8").strip())
    assert parsed == [1, 2, 3]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_firehose_put_result_all_succeeded():
    result = FirehosePutResult(failed_put_count=0, request_responses=[{"RecordId": "abc"}])
    assert result.all_succeeded is True


def test_firehose_put_result_not_all_succeeded():
    result = FirehosePutResult(
        failed_put_count=1,
        request_responses=[{"ErrorCode": "ServiceUnavailableException"}],
    )
    assert result.all_succeeded is False


def test_delivery_stream_model():
    ds = DeliveryStream(
        delivery_stream_name=STREAM_NAME,
        delivery_stream_arn="arn:aws:firehose:us-east-1:123:deliverystream/test",
        delivery_stream_status="ACTIVE",
        delivery_stream_type="DirectPut",
    )
    assert ds.delivery_stream_name == STREAM_NAME
    assert ds.create_timestamp is None


# ---------------------------------------------------------------------------
# put_record
# ---------------------------------------------------------------------------

def test_put_record_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record.return_value = {"RecordId": "record-123"}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_record(STREAM_NAME, {"event": "test"}, region_name=REGION)
    assert result == "record-123"


def test_put_record_bytes(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record.return_value = {"RecordId": "rec-abc"}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_record(STREAM_NAME, b"raw bytes", region_name=REGION)
    assert result == "rec-abc"


def test_put_record_string(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record.return_value = {"RecordId": "rec-str"}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_record(STREAM_NAME, "text data", region_name=REGION)
    assert result == "rec-str"


def test_put_record_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}}, "PutRecord"
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="put_record failed"):
        put_record(STREAM_NAME, b"data", region_name=REGION)


# ---------------------------------------------------------------------------
# put_record_batch
# ---------------------------------------------------------------------------

def test_put_record_batch_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record_batch.return_value = {
        "FailedPutCount": 0,
        "RequestResponses": [{"RecordId": "r1"}, {"RecordId": "r2"}],
    }
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_record_batch(STREAM_NAME, [b"msg1", b"msg2"], region_name=REGION)
    assert isinstance(result, FirehosePutResult)
    assert result.failed_put_count == 0
    assert result.all_succeeded is True


def test_put_record_batch_too_many_raises():
    with pytest.raises(ValueError, match="at most 500"):
        put_record_batch(STREAM_NAME, [b"x"] * 501)


def test_put_record_batch_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record_batch.side_effect = ClientError(
        {"Error": {"Code": "ServiceUnavailableException", "Message": "error"}}, "PutRecordBatch"
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="put_record_batch failed"):
        put_record_batch(STREAM_NAME, [b"data"], region_name=REGION)


def test_put_record_batch_mixed_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_record_batch.return_value = {
        "FailedPutCount": 0,
        "RequestResponses": [{"RecordId": "r1"}, {"RecordId": "r2"}, {"RecordId": "r3"}],
    }
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = put_record_batch(STREAM_NAME, [b"bytes", "string", {"key": "value"}], region_name=REGION)
    assert result.failed_put_count == 0


# ---------------------------------------------------------------------------
# list_delivery_streams
# ---------------------------------------------------------------------------

def test_list_delivery_streams_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delivery_streams.return_value = {
        "DeliveryStreamNames": ["stream-a", "stream-b"],
        "HasMoreDeliveryStreams": False,
    }
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_delivery_streams(region_name=REGION)
    assert result == ["stream-a", "stream-b"]


def test_list_delivery_streams_with_type_filter(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delivery_streams.return_value = {
        "DeliveryStreamNames": ["stream-a"],
        "HasMoreDeliveryStreams": False,
    }
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_delivery_streams(delivery_stream_type="DirectPut", region_name=REGION)
    assert result == ["stream-a"]
    call_kwargs = mock_client.list_delivery_streams.call_args[1]
    assert call_kwargs.get("DeliveryStreamType") == "DirectPut"


def test_list_delivery_streams_pagination(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delivery_streams.side_effect = [
        {"DeliveryStreamNames": ["stream-a"], "HasMoreDeliveryStreams": True},
        {"DeliveryStreamNames": ["stream-b"], "HasMoreDeliveryStreams": False},
    ]
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_delivery_streams(region_name=REGION)
    assert result == ["stream-a", "stream-b"]


def test_list_delivery_streams_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delivery_streams.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "denied"}}, "ListDeliveryStreams"
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_delivery_streams failed"):
        list_delivery_streams(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_delivery_stream
# ---------------------------------------------------------------------------

def test_describe_delivery_stream_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_stream.return_value = {
        "DeliveryStreamDescription": {
            "DeliveryStreamName": STREAM_NAME,
            "DeliveryStreamARN": "arn:aws:firehose:us-east-1:123:deliverystream/test",
            "DeliveryStreamStatus": "ACTIVE",
            "DeliveryStreamType": "DirectPut",
            "CreateTimestamp": None,
        }
    }
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    result = describe_delivery_stream(STREAM_NAME, region_name=REGION)
    assert isinstance(result, DeliveryStream)
    assert result.delivery_stream_name == STREAM_NAME
    assert result.delivery_stream_status == "ACTIVE"


def test_describe_delivery_stream_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "DescribeDeliveryStream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="describe_delivery_stream failed"):
        describe_delivery_stream("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# put_record_batch_with_retry
# ---------------------------------------------------------------------------

def test_put_record_batch_with_retry_all_success(monkeypatch):
    mock_result = FirehosePutResult(
        failed_put_count=0,
        request_responses=[{"RecordId": "r1"}, {"RecordId": "r2"}],
    )
    monkeypatch.setattr(firehose_mod, "put_record_batch", lambda *a, **kw: mock_result)
    count = put_record_batch_with_retry(STREAM_NAME, [b"a", b"b"], region_name=REGION)
    assert count == 2


def test_put_record_batch_with_retry_partial_failure_then_success(monkeypatch):
    call_count = {"n": 0}

    def fake_put(name, records, region_name=None):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return FirehosePutResult(
                failed_put_count=1,
                request_responses=[{"RecordId": "r1"}, {"ErrorCode": "ProvisionedThroughputExceededException"}],
            )
        return FirehosePutResult(
            failed_put_count=0,
            request_responses=[{"RecordId": "r2"}],
        )

    monkeypatch.setattr(firehose_mod, "put_record_batch", fake_put)
    count = put_record_batch_with_retry(STREAM_NAME, [b"a", b"b"], max_retries=3, region_name=REGION)
    assert count == 2


def test_put_record_batch_with_retry_exhausted(monkeypatch):
    mock_result = FirehosePutResult(
        failed_put_count=1,
        request_responses=[{"ErrorCode": "ServiceUnavailableException"}],
    )
    monkeypatch.setattr(firehose_mod, "put_record_batch", lambda *a, **kw: mock_result)
    with pytest.raises(RuntimeError, match="still failing after"):
        put_record_batch_with_retry(STREAM_NAME, [b"a"], max_retries=1, region_name=REGION)


def test_put_record_batch_with_retry_empty():
    count = put_record_batch_with_retry(STREAM_NAME, [], region_name=REGION)
    assert count == 0


def test_create_delivery_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delivery_stream.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    create_delivery_stream("test-delivery_stream_name", region_name=REGION)
    mock_client.create_delivery_stream.assert_called_once()


def test_create_delivery_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_delivery_stream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create delivery stream"):
        create_delivery_stream("test-delivery_stream_name", region_name=REGION)


def test_delete_delivery_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_delivery_stream.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    delete_delivery_stream("test-delivery_stream_name", region_name=REGION)
    mock_client.delete_delivery_stream.assert_called_once()


def test_delete_delivery_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_delivery_stream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete delivery stream"):
        delete_delivery_stream("test-delivery_stream_name", region_name=REGION)


def test_list_tags_for_delivery_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_delivery_stream.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_delivery_stream("test-delivery_stream_name", region_name=REGION)
    mock_client.list_tags_for_delivery_stream.assert_called_once()


def test_list_tags_for_delivery_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_delivery_stream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for delivery stream"):
        list_tags_for_delivery_stream("test-delivery_stream_name", region_name=REGION)


def test_start_delivery_stream_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_delivery_stream_encryption.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    start_delivery_stream_encryption("test-delivery_stream_name", region_name=REGION)
    mock_client.start_delivery_stream_encryption.assert_called_once()


def test_start_delivery_stream_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_delivery_stream_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_delivery_stream_encryption",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start delivery stream encryption"):
        start_delivery_stream_encryption("test-delivery_stream_name", region_name=REGION)


def test_stop_delivery_stream_encryption(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_delivery_stream_encryption.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    stop_delivery_stream_encryption("test-delivery_stream_name", region_name=REGION)
    mock_client.stop_delivery_stream_encryption.assert_called_once()


def test_stop_delivery_stream_encryption_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_delivery_stream_encryption.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_delivery_stream_encryption",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop delivery stream encryption"):
        stop_delivery_stream_encryption("test-delivery_stream_name", region_name=REGION)


def test_tag_delivery_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_delivery_stream.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    tag_delivery_stream("test-delivery_stream_name", [], region_name=REGION)
    mock_client.tag_delivery_stream.assert_called_once()


def test_tag_delivery_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_delivery_stream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag delivery stream"):
        tag_delivery_stream("test-delivery_stream_name", [], region_name=REGION)


def test_untag_delivery_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_delivery_stream.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    untag_delivery_stream("test-delivery_stream_name", [], region_name=REGION)
    mock_client.untag_delivery_stream.assert_called_once()


def test_untag_delivery_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_delivery_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_delivery_stream",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag delivery stream"):
        untag_delivery_stream("test-delivery_stream_name", [], region_name=REGION)


def test_update_destination(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_destination.return_value = {}
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", region_name=REGION)
    mock_client.update_destination.assert_called_once()


def test_update_destination_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_destination",
    )
    monkeypatch.setattr(firehose_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update destination"):
        update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", region_name=REGION)


def test_create_delivery_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.firehose import create_delivery_stream
    mock_client = MagicMock()
    mock_client.create_delivery_stream.return_value = {}
    monkeypatch.setattr("aws_util.firehose.get_client", lambda *a, **kw: mock_client)
    create_delivery_stream("test-delivery_stream_name", delivery_stream_type="test-delivery_stream_type", direct_put_source_configuration={}, kinesis_stream_source_configuration={}, delivery_stream_encryption_configuration_input={}, s3_destination_configuration={}, extended_s3_destination_configuration={}, redshift_destination_configuration={}, elasticsearch_destination_configuration={}, amazonopensearchservice_destination_configuration={}, splunk_destination_configuration={}, http_endpoint_destination_configuration={}, tags=[{"Key": "k", "Value": "v"}], amazon_open_search_serverless_destination_configuration={}, msk_source_configuration={}, snowflake_destination_configuration={}, iceberg_destination_configuration={}, database_source_configuration={}, region_name="us-east-1")
    mock_client.create_delivery_stream.assert_called_once()

def test_delete_delivery_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.firehose import delete_delivery_stream
    mock_client = MagicMock()
    mock_client.delete_delivery_stream.return_value = {}
    monkeypatch.setattr("aws_util.firehose.get_client", lambda *a, **kw: mock_client)
    delete_delivery_stream("test-delivery_stream_name", allow_force_delete=True, region_name="us-east-1")
    mock_client.delete_delivery_stream.assert_called_once()

def test_list_tags_for_delivery_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.firehose import list_tags_for_delivery_stream
    mock_client = MagicMock()
    mock_client.list_tags_for_delivery_stream.return_value = {}
    monkeypatch.setattr("aws_util.firehose.get_client", lambda *a, **kw: mock_client)
    list_tags_for_delivery_stream("test-delivery_stream_name", exclusive_start_tag_key="test-exclusive_start_tag_key", limit=1, region_name="us-east-1")
    mock_client.list_tags_for_delivery_stream.assert_called_once()

def test_start_delivery_stream_encryption_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.firehose import start_delivery_stream_encryption
    mock_client = MagicMock()
    mock_client.start_delivery_stream_encryption.return_value = {}
    monkeypatch.setattr("aws_util.firehose.get_client", lambda *a, **kw: mock_client)
    start_delivery_stream_encryption("test-delivery_stream_name", delivery_stream_encryption_configuration_input={}, region_name="us-east-1")
    mock_client.start_delivery_stream_encryption.assert_called_once()

def test_update_destination_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.firehose import update_destination
    mock_client = MagicMock()
    mock_client.update_destination.return_value = {}
    monkeypatch.setattr("aws_util.firehose.get_client", lambda *a, **kw: mock_client)
    update_destination("test-delivery_stream_name", "test-current_delivery_stream_version_id", "test-destination_id", s3_destination_update="test-s3_destination_update", extended_s3_destination_update="test-extended_s3_destination_update", redshift_destination_update="test-redshift_destination_update", elasticsearch_destination_update="test-elasticsearch_destination_update", amazonopensearchservice_destination_update="test-amazonopensearchservice_destination_update", splunk_destination_update="test-splunk_destination_update", http_endpoint_destination_update="test-http_endpoint_destination_update", amazon_open_search_serverless_destination_update="test-amazon_open_search_serverless_destination_update", snowflake_destination_update="test-snowflake_destination_update", iceberg_destination_update="test-iceberg_destination_update", region_name="us-east-1")
    mock_client.update_destination.assert_called_once()
