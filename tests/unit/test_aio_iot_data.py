"""Tests for aws_util.aio.iot_data -- 100% line coverage."""
from __future__ import annotations

import io
import json
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.iot_data import (
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


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# publish
# ---------------------------------------------------------------------------


async def test_publish_no_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await publish("test/topic")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["topic"] == "test/topic"
    assert "payload" not in call_kwargs


async def test_publish_string_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await publish("test/topic", payload="hello")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["payload"] == b"hello"


async def test_publish_bytes_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await publish("test/topic", payload=b"raw")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["payload"] == b"raw"

async def test_publish_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="publish failed"):
        await publish("test/topic")


# ---------------------------------------------------------------------------
# get_thing_shadow
# ---------------------------------------------------------------------------


async def test_get_thing_shadow(monkeypatch):
    mock_client = AsyncMock()
    shadow_data = json.dumps({"state": {"desired": {"temp": 72}}})
    mock_client.call.return_value = {"payload": io.BytesIO(shadow_data.encode())}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_thing_shadow("my-thing")
    assert isinstance(result, ShadowResult)
    assert result.payload["state"]["desired"]["temp"] == 72


async def test_get_thing_shadow_with_shadow_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": io.BytesIO(b"{}")}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await get_thing_shadow("my-thing", shadow_name="named")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["shadowName"] == "named"


async def test_get_thing_shadow_no_payload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_thing_shadow("my-thing")
    assert result.payload == {}


async def test_get_thing_shadow_string_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": '{"a": 1}'}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_thing_shadow("my-thing")
    assert result.payload == {"a": 1}


async def test_get_thing_shadow_dict_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": {"a": 1}}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_thing_shadow("my-thing")
    assert result.payload == {"a": 1}


async def test_get_thing_shadow_empty_string_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": ""}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_thing_shadow("my-thing")
    assert result.payload == {}


async def test_get_thing_shadow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="get_thing_shadow failed"):
        await get_thing_shadow("my-thing")


# ---------------------------------------------------------------------------
# update_thing_shadow
# ---------------------------------------------------------------------------


async def test_update_thing_shadow(monkeypatch):
    mock_client = AsyncMock()
    result_data = json.dumps({"state": {"desired": {"temp": 72}}})
    mock_client.call.return_value = {"payload": io.BytesIO(result_data.encode())}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await update_thing_shadow("my-thing", payload={"state": {"desired": {"temp": 72}}})
    assert isinstance(result, ShadowResult)


async def test_update_thing_shadow_with_shadow_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": io.BytesIO(b"{}")}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await update_thing_shadow("my-thing", payload={}, shadow_name="named")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["shadowName"] == "named"


async def test_update_thing_shadow_no_payload_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await update_thing_shadow("my-thing", payload={"x": 1})
    assert result.payload == {}


async def test_update_thing_shadow_dict_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": {"y": 2}}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await update_thing_shadow("my-thing", payload={"x": 1})
    assert result.payload == {"y": 2}


async def test_update_thing_shadow_empty_body(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"payload": b""}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await update_thing_shadow("my-thing", payload={"x": 1})
    assert result.payload == {}


async def test_update_thing_shadow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="update_thing_shadow failed"):
        await update_thing_shadow("my-thing", payload={})


# ---------------------------------------------------------------------------
# delete_thing_shadow
# ---------------------------------------------------------------------------


async def test_delete_thing_shadow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await delete_thing_shadow("my-thing")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["thingName"] == "my-thing"


async def test_delete_thing_shadow_with_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    await delete_thing_shadow("my-thing", shadow_name="named")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["shadowName"] == "named"


async def test_delete_thing_shadow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="delete_thing_shadow failed"):
        await delete_thing_shadow("my-thing")


# ---------------------------------------------------------------------------
# list_named_shadows_for_thing
# ---------------------------------------------------------------------------


async def test_list_named_shadows_for_thing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"results": ["shadow1", "shadow2"]}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await list_named_shadows_for_thing("my-thing")
    assert result == ["shadow1", "shadow2"]


async def test_list_named_shadows_for_thing_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"results": ["s1"], "nextToken": "tok"},
        {"results": ["s2"]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await list_named_shadows_for_thing("my-thing")
    assert result == ["s1", "s2"]


async def test_list_named_shadows_for_thing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_named_shadows_for_thing("my-thing")


# ---------------------------------------------------------------------------
# get_retained_message
# ---------------------------------------------------------------------------


async def test_get_retained_message(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "topic": "test/topic",
        "payload": b"hello",
        "qos": 1,
        "lastModifiedTime": 1234567890,
        "ResponseMetadata": {},
    }
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_retained_message("test/topic")
    assert isinstance(result, RetainedMessageResult)
    assert result.payload == b"hello"


async def test_get_retained_message_streaming_body(monkeypatch):
    mock_client = AsyncMock()
    body = io.BytesIO(b"streamed")
    mock_client.call.return_value = {"topic": "t", "payload": body, "qos": 0, "lastModifiedTime": 0}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_retained_message("t")
    assert result.payload == b"streamed"


async def test_get_retained_message_non_bytes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"topic": "t", "payload": "not_bytes", "qos": 0, "lastModifiedTime": 0}
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_retained_message("t")
    assert result.payload == b""


async def test_get_retained_message_extra_fields(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "topic": "t", "payload": b"x", "qos": 0, "lastModifiedTime": 0,
        "userProperties": [{"k": "v"}],
    }
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await get_retained_message("t")
    assert "userProperties" in result.extra


async def test_get_retained_message_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="get_retained_message failed"):
        await get_retained_message("test/topic")


# ---------------------------------------------------------------------------
# list_retained_messages
# ---------------------------------------------------------------------------


async def test_list_retained_messages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "retainedTopics": [
            {"topic": "t1", "qos": 0, "lastModifiedTime": 100},
            {"topic": "t2", "qos": 1, "lastModifiedTime": 200},
        ],
    }
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await list_retained_messages()
    assert len(result) == 2


async def test_list_retained_messages_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"retainedTopics": [{"topic": "t1", "qos": 0, "lastModifiedTime": 0}], "nextToken": "tok"},
        {"retainedTopics": [{"topic": "t2", "qos": 0, "lastModifiedTime": 0}]},
    ]
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    result = await list_retained_messages()
    assert len(result) == 2


async def test_list_retained_messages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="list_retained_messages failed"):
        await list_retained_messages()


async def test_delete_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_connection("test-client_id", )
    mock_client.call.assert_called_once()


async def test_delete_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connection("test-client_id", )


@pytest.mark.asyncio
async def test_publish_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_data import publish
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", lambda *a, **kw: mock_client)
    await publish("test-topic", payload="test-payload", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_thing_shadow_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_data import delete_thing_shadow
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", lambda *a, **kw: mock_client)
    await delete_thing_shadow("test-thing_name", shadow_name="test-shadow_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot_data import delete_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot_data.async_client", lambda *a, **kw: mock_client)
    await delete_connection("test-client_id", clean_session="test-clean_session", prevent_will_message="test-prevent_will_message", region_name="us-east-1")
    mock_client.call.assert_called_once()
