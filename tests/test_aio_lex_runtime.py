"""Tests for aws_util.aio.lex_runtime -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.lex_runtime import (
    LexMessage,
    LexSessionState,
    delete_session,
    get_session,
    put_session,
    recognize_text,
    recognize_utterance,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# recognize_text
# ---------------------------------------------------------------------------


async def test_recognize_text_ok(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await recognize_text("b1", "a1", "en_US", "s1", "hello")
    assert r["sessionId"] == "s1"


async def test_recognize_text_with_opts(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await recognize_text(
        "b1", "a1", "en_US", "s1", "hello",
        session_state={"k": "v"},
        request_attributes={"a": "b"},
    )
    assert r["sessionId"] == "s1"


async def test_recognize_text_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="recognize_text failed"):
        await recognize_text("b1", "a1", "en_US", "s1", "hello")


# ---------------------------------------------------------------------------
# recognize_utterance
# ---------------------------------------------------------------------------


async def test_recognize_utterance_ok(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await recognize_utterance("b1", "a1", "en_US", "s1", "audio/l16")
    assert r["sessionId"] == "s1"


async def test_recognize_utterance_with_opts(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await recognize_utterance(
        "b1", "a1", "en_US", "s1", "audio/l16",
        input_stream=b"\x00",
        session_state='{"k":"v"}',
        request_attributes='{"a":"b"}',
        response_content_type="audio/mpeg",
    )
    assert r["sessionId"] == "s1"


async def test_recognize_utterance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="recognize_utterance failed"):
        await recognize_utterance("b1", "a1", "en_US", "s1", "audio/l16")


# ---------------------------------------------------------------------------
# put_session
# ---------------------------------------------------------------------------


async def test_put_session_ok(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await put_session("b1", "a1", "en_US", "s1", {"key": "val"})
    assert r["sessionId"] == "s1"


async def test_put_session_with_opts(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await put_session(
        "b1", "a1", "en_US", "s1", {"key": "val"},
        messages=[{"content": "hi"}],
        request_attributes={"a": "b"},
        response_content_type="audio/mpeg",
    )
    assert r["sessionId"] == "s1"


async def test_put_session_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="put_session failed"):
        await put_session("b1", "a1", "en_US", "s1", {"key": "val"})


# ---------------------------------------------------------------------------
# get_session
# ---------------------------------------------------------------------------


async def test_get_session_ok(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await get_session("b1", "a1", "en_US", "s1")
    assert r["sessionId"] == "s1"


async def test_get_session_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="get_session failed"):
        await get_session("b1", "a1", "en_US", "s1")


# ---------------------------------------------------------------------------
# delete_session
# ---------------------------------------------------------------------------


async def test_delete_session_ok(monkeypatch):
    mc = _mc({"sessionId": "s1"})
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    r = await delete_session("b1", "a1", "en_US", "s1")
    assert r["sessionId"] == "s1"


async def test_delete_session_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr("aws_util.aio.lex_runtime.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_session failed"):
        await delete_session("b1", "a1", "en_US", "s1")
