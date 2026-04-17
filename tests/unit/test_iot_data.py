"""Tests for aws_util.iot_data -- 100% line coverage."""
from __future__ import annotations

import io
import json
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.iot_data import (
    RetainedMessageResult,
    ShadowResult,
    delete_thing_shadow,
    get_retained_message,
    get_thing_shadow,
    list_named_shadows_for_thing,
    list_retained_messages,
    publish,
    update_thing_shadow,
    delete_connection,
)


def _client_error(code: str = "ValidationException") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": "boom"}}, "Op"
    )


# ---------------------------------------------------------------------------
# publish
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_publish_no_payload(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    publish("test/topic")
    call_kwargs = client.publish.call_args[1]
    assert call_kwargs["topic"] == "test/topic"
    assert "payload" not in call_kwargs


@patch("aws_util.iot_data.get_client")
def test_publish_string_payload(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    publish("test/topic", payload="hello")
    call_kwargs = client.publish.call_args[1]
    assert call_kwargs["payload"] == b"hello"


@patch("aws_util.iot_data.get_client")
def test_publish_bytes_payload(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    publish("test/topic", payload=b"raw")
    call_kwargs = client.publish.call_args[1]
    assert call_kwargs["payload"] == b"raw"


@patch("aws_util.iot_data.get_client")
def test_publish_error(mock_gc):
    client = MagicMock()
    client.publish.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="publish failed"):
        publish("test/topic")


# ---------------------------------------------------------------------------
# get_thing_shadow
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_get_thing_shadow(mock_gc):
    client = MagicMock()
    shadow_data = json.dumps({"state": {"desired": {"temp": 72}}})
    client.get_thing_shadow.return_value = {
        "payload": io.BytesIO(shadow_data.encode()),
    }
    mock_gc.return_value = client
    result = get_thing_shadow("my-thing")
    assert isinstance(result, ShadowResult)
    assert result.payload["state"]["desired"]["temp"] == 72


@patch("aws_util.iot_data.get_client")
def test_get_thing_shadow_with_shadow_name(mock_gc):
    client = MagicMock()
    client.get_thing_shadow.return_value = {"payload": io.BytesIO(b"{}")}
    mock_gc.return_value = client
    get_thing_shadow("my-thing", shadow_name="named")
    call_kwargs = client.get_thing_shadow.call_args[1]
    assert call_kwargs["shadowName"] == "named"


@patch("aws_util.iot_data.get_client")
def test_get_thing_shadow_no_payload(mock_gc):
    client = MagicMock()
    client.get_thing_shadow.return_value = {}
    mock_gc.return_value = client
    result = get_thing_shadow("my-thing")
    assert result.payload == {}


@patch("aws_util.iot_data.get_client")
def test_get_thing_shadow_empty_body(mock_gc):
    client = MagicMock()
    client.get_thing_shadow.return_value = {"payload": io.BytesIO(b"")}
    mock_gc.return_value = client
    result = get_thing_shadow("my-thing")
    assert result.payload == {}


@patch("aws_util.iot_data.get_client")
def test_get_thing_shadow_error(mock_gc):
    client = MagicMock()
    client.get_thing_shadow.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="get_thing_shadow failed"):
        get_thing_shadow("my-thing")


# ---------------------------------------------------------------------------
# update_thing_shadow
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_update_thing_shadow(mock_gc):
    client = MagicMock()
    result_data = json.dumps({"state": {"desired": {"temp": 72}}})
    client.update_thing_shadow.return_value = {
        "payload": io.BytesIO(result_data.encode()),
    }
    mock_gc.return_value = client
    result = update_thing_shadow("my-thing", payload={"state": {"desired": {"temp": 72}}})
    assert isinstance(result, ShadowResult)
    assert result.payload["state"]["desired"]["temp"] == 72


@patch("aws_util.iot_data.get_client")
def test_update_thing_shadow_with_shadow_name(mock_gc):
    client = MagicMock()
    client.update_thing_shadow.return_value = {"payload": io.BytesIO(b"{}")}
    mock_gc.return_value = client
    update_thing_shadow("my-thing", payload={}, shadow_name="named")
    call_kwargs = client.update_thing_shadow.call_args[1]
    assert call_kwargs["shadowName"] == "named"


@patch("aws_util.iot_data.get_client")
def test_update_thing_shadow_no_payload_body(mock_gc):
    client = MagicMock()
    client.update_thing_shadow.return_value = {}
    mock_gc.return_value = client
    result = update_thing_shadow("my-thing", payload={"x": 1})
    assert result.payload == {}


@patch("aws_util.iot_data.get_client")
def test_update_thing_shadow_empty_body(mock_gc):
    client = MagicMock()
    client.update_thing_shadow.return_value = {"payload": io.BytesIO(b"")}
    mock_gc.return_value = client
    result = update_thing_shadow("my-thing", payload={"x": 1})
    assert result.payload == {}


@patch("aws_util.iot_data.get_client")
def test_update_thing_shadow_error(mock_gc):
    client = MagicMock()
    client.update_thing_shadow.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="update_thing_shadow failed"):
        update_thing_shadow("my-thing", payload={})


# ---------------------------------------------------------------------------
# delete_thing_shadow
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_delete_thing_shadow(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_thing_shadow("my-thing")
    call_kwargs = client.delete_thing_shadow.call_args[1]
    assert call_kwargs["thingName"] == "my-thing"


@patch("aws_util.iot_data.get_client")
def test_delete_thing_shadow_with_name(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_thing_shadow("my-thing", shadow_name="named")
    call_kwargs = client.delete_thing_shadow.call_args[1]
    assert call_kwargs["shadowName"] == "named"


@patch("aws_util.iot_data.get_client")
def test_delete_thing_shadow_error(mock_gc):
    client = MagicMock()
    client.delete_thing_shadow.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="delete_thing_shadow failed"):
        delete_thing_shadow("my-thing")


# ---------------------------------------------------------------------------
# list_named_shadows_for_thing
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_list_named_shadows_for_thing(mock_gc):
    client = MagicMock()
    client.list_named_shadows_for_thing.return_value = {
        "results": ["shadow1", "shadow2"],
    }
    mock_gc.return_value = client
    result = list_named_shadows_for_thing("my-thing")
    assert result == ["shadow1", "shadow2"]


@patch("aws_util.iot_data.get_client")
def test_list_named_shadows_for_thing_pagination(mock_gc):
    client = MagicMock()
    client.list_named_shadows_for_thing.side_effect = [
        {"results": ["s1"], "nextToken": "tok"},
        {"results": ["s2"]},
    ]
    mock_gc.return_value = client
    result = list_named_shadows_for_thing("my-thing")
    assert result == ["s1", "s2"]


@patch("aws_util.iot_data.get_client")
def test_list_named_shadows_for_thing_error(mock_gc):
    client = MagicMock()
    client.list_named_shadows_for_thing.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_named_shadows_for_thing("my-thing")


# ---------------------------------------------------------------------------
# get_retained_message
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_get_retained_message(mock_gc):
    client = MagicMock()
    client.get_retained_message.return_value = {
        "topic": "test/topic",
        "payload": b"hello",
        "qos": 1,
        "lastModifiedTime": 1234567890,
        "ResponseMetadata": {},
    }
    mock_gc.return_value = client
    result = get_retained_message("test/topic")
    assert isinstance(result, RetainedMessageResult)
    assert result.topic == "test/topic"
    assert result.payload == b"hello"
    assert result.qos == 1


@patch("aws_util.iot_data.get_client")
def test_get_retained_message_streaming_body(mock_gc):
    client = MagicMock()
    body = io.BytesIO(b"streamed")
    client.get_retained_message.return_value = {
        "topic": "t",
        "payload": body,
        "qos": 0,
        "lastModifiedTime": 0,
    }
    mock_gc.return_value = client
    result = get_retained_message("t")
    assert result.payload == b"streamed"


@patch("aws_util.iot_data.get_client")
def test_get_retained_message_non_bytes_payload(mock_gc):
    client = MagicMock()
    client.get_retained_message.return_value = {
        "topic": "t",
        "payload": "not_bytes",
        "qos": 0,
        "lastModifiedTime": 0,
    }
    mock_gc.return_value = client
    result = get_retained_message("t")
    assert result.payload == b""


@patch("aws_util.iot_data.get_client")
def test_get_retained_message_extra_fields(mock_gc):
    client = MagicMock()
    client.get_retained_message.return_value = {
        "topic": "t",
        "payload": b"x",
        "qos": 0,
        "lastModifiedTime": 0,
        "userProperties": [{"k": "v"}],
    }
    mock_gc.return_value = client
    result = get_retained_message("t")
    assert "userProperties" in result.extra


@patch("aws_util.iot_data.get_client")
def test_get_retained_message_error(mock_gc):
    client = MagicMock()
    client.get_retained_message.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="get_retained_message failed"):
        get_retained_message("test/topic")


# ---------------------------------------------------------------------------
# list_retained_messages
# ---------------------------------------------------------------------------


@patch("aws_util.iot_data.get_client")
def test_list_retained_messages(mock_gc):
    client = MagicMock()
    client.list_retained_messages.return_value = {
        "retainedTopics": [
            {"topic": "t1", "qos": 0, "lastModifiedTime": 100},
            {"topic": "t2", "qos": 1, "lastModifiedTime": 200},
        ],
    }
    mock_gc.return_value = client
    result = list_retained_messages()
    assert len(result) == 2
    assert all(isinstance(r, RetainedMessageResult) for r in result)


@patch("aws_util.iot_data.get_client")
def test_list_retained_messages_pagination(mock_gc):
    client = MagicMock()
    client.list_retained_messages.side_effect = [
        {"retainedTopics": [{"topic": "t1", "qos": 0, "lastModifiedTime": 0}], "nextToken": "tok"},
        {"retainedTopics": [{"topic": "t2", "qos": 0, "lastModifiedTime": 0}]},
    ]
    mock_gc.return_value = client
    result = list_retained_messages()
    assert len(result) == 2


@patch("aws_util.iot_data.get_client")
def test_list_retained_messages_error(mock_gc):
    client = MagicMock()
    client.list_retained_messages.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="list_retained_messages failed"):
        list_retained_messages()


REGION = "us-east-1"


@patch("aws_util.iot_data.get_client")
def test_delete_connection(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_connection.return_value = {}
    delete_connection("test-client_id", region_name=REGION)
    mock_client.delete_connection.assert_called_once()


@patch("aws_util.iot_data.get_client")
def test_delete_connection_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connection",
    )
    with pytest.raises(RuntimeError, match="Failed to delete connection"):
        delete_connection("test-client_id", region_name=REGION)


def test_publish_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_data import publish
    mock_client = MagicMock()
    mock_client.publish.return_value = {}
    monkeypatch.setattr("aws_util.iot_data.get_client", lambda *a, **kw: mock_client)
    publish("test-topic", payload="test-payload", region_name="us-east-1")
    mock_client.publish.assert_called_once()

def test_delete_thing_shadow_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_data import delete_thing_shadow
    mock_client = MagicMock()
    mock_client.delete_thing_shadow.return_value = {}
    monkeypatch.setattr("aws_util.iot_data.get_client", lambda *a, **kw: mock_client)
    delete_thing_shadow("test-thing_name", shadow_name="test-shadow_name", region_name="us-east-1")
    mock_client.delete_thing_shadow.assert_called_once()

def test_delete_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot_data import delete_connection
    mock_client = MagicMock()
    mock_client.delete_connection.return_value = {}
    monkeypatch.setattr("aws_util.iot_data.get_client", lambda *a, **kw: mock_client)
    delete_connection("test-client_id", clean_session="test-clean_session", prevent_will_message="test-prevent_will_message", region_name="us-east-1")
    mock_client.delete_connection.assert_called_once()
