"""Tests for aws_util.lex_runtime -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.lex_runtime import (
    LexMessage,
    LexSessionState,
    delete_session,
    get_session,
    put_session,
    recognize_text,
    recognize_utterance,
)

_ERR = ClientError({"Error": {"Code": "X", "Message": "fail"}}, "op")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_lex_message_minimal():
    m = LexMessage()
    assert m.content == ""
    assert m.image_response_card is None


def test_lex_message_full():
    m = LexMessage(
        content="hi", content_type="PlainText",
        image_response_card={"title": "t"},
    )
    assert m.content == "hi"


def test_lex_session_state_minimal():
    m = LexSessionState()
    assert m.session_id == ""
    assert m.session_attributes == {}


def test_lex_session_state_full():
    m = LexSessionState(
        session_id="s1", intent_name="Order",
        dialog_action_type="Close",
        session_attributes={"key": "val"},
    )
    assert m.intent_name == "Order"


# ---------------------------------------------------------------------------
# recognize_text
# ---------------------------------------------------------------------------


@patch("aws_util.lex_runtime.get_client")
def test_recognize_text_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_text.return_value = {"sessionId": "s1"}
    r = recognize_text("b1", "a1", "en_US", "s1", "hello")
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_recognize_text_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_text.return_value = {"sessionId": "s1"}
    r = recognize_text(
        "b1", "a1", "en_US", "s1", "hello",
        session_state={"k": "v"},
        request_attributes={"attr": "val"},
    )
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_recognize_text_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_text.side_effect = _ERR
    with pytest.raises(RuntimeError, match="recognize_text failed"):
        recognize_text("b1", "a1", "en_US", "s1", "hello")


# ---------------------------------------------------------------------------
# recognize_utterance
# ---------------------------------------------------------------------------


@patch("aws_util.lex_runtime.get_client")
def test_recognize_utterance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_utterance.return_value = {"sessionId": "s1"}
    r = recognize_utterance("b1", "a1", "en_US", "s1", "audio/l16")
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_recognize_utterance_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_utterance.return_value = {"sessionId": "s1"}
    r = recognize_utterance(
        "b1", "a1", "en_US", "s1", "audio/l16",
        input_stream=b"\x00",
        session_state='{"k":"v"}',
        request_attributes='{"a":"b"}',
        response_content_type="audio/mpeg",
    )
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_recognize_utterance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.recognize_utterance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="recognize_utterance failed"):
        recognize_utterance("b1", "a1", "en_US", "s1", "audio/l16")


# ---------------------------------------------------------------------------
# put_session
# ---------------------------------------------------------------------------


@patch("aws_util.lex_runtime.get_client")
def test_put_session_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.put_session.return_value = {"sessionId": "s1"}
    r = put_session("b1", "a1", "en_US", "s1", {"key": "val"})
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_put_session_with_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.put_session.return_value = {"sessionId": "s1"}
    r = put_session(
        "b1", "a1", "en_US", "s1", {"key": "val"},
        messages=[{"content": "hi"}],
        request_attributes={"a": "b"},
        response_content_type="audio/mpeg",
    )
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_put_session_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.put_session.side_effect = _ERR
    with pytest.raises(RuntimeError, match="put_session failed"):
        put_session("b1", "a1", "en_US", "s1", {"key": "val"})


# ---------------------------------------------------------------------------
# get_session
# ---------------------------------------------------------------------------


@patch("aws_util.lex_runtime.get_client")
def test_get_session_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_session.return_value = {"sessionId": "s1"}
    r = get_session("b1", "a1", "en_US", "s1")
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_get_session_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_session.side_effect = _ERR
    with pytest.raises(RuntimeError, match="get_session failed"):
        get_session("b1", "a1", "en_US", "s1")


# ---------------------------------------------------------------------------
# delete_session
# ---------------------------------------------------------------------------


@patch("aws_util.lex_runtime.get_client")
def test_delete_session_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_session.return_value = {"sessionId": "s1"}
    r = delete_session("b1", "a1", "en_US", "s1")
    assert r["sessionId"] == "s1"


@patch("aws_util.lex_runtime.get_client")
def test_delete_session_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_session.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_session failed"):
        delete_session("b1", "a1", "en_US", "s1")
