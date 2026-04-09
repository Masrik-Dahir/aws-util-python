"""Native async Lex V2 Runtime utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.lex_runtime import (
    LexMessage,
    LexSessionState,
)

__all__ = [
    "LexMessage",
    "LexSessionState",
    "delete_session",
    "get_session",
    "put_session",
    "recognize_text",
    "recognize_utterance",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def recognize_text(
    bot_id: str,
    bot_alias_id: str,
    locale_id: str,
    session_id: str,
    text: str,
    session_state: dict[str, Any] | None = None,
    request_attributes: dict[str, str] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Send text to a Lex V2 bot and get a response.

    Args:
        bot_id: The bot identifier.
        bot_alias_id: The bot alias identifier.
        locale_id: The locale (e.g. ``"en_US"``).
        session_id: The session identifier.
        text: The user input text.
        session_state: Optional session state to send.
        request_attributes: Optional request attributes.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the call fails.
    """
    client = async_client("lexv2-runtime", region_name)
    kwargs: dict[str, Any] = {
        "botId": bot_id,
        "botAliasId": bot_alias_id,
        "localeId": locale_id,
        "sessionId": session_id,
        "text": text,
    }
    if session_state is not None:
        kwargs["sessionState"] = session_state
    if request_attributes is not None:
        kwargs["requestAttributes"] = request_attributes
    try:
        return await client.call("RecognizeText", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "recognize_text failed") from exc


async def recognize_utterance(
    bot_id: str,
    bot_alias_id: str,
    locale_id: str,
    session_id: str,
    request_content_type: str,
    input_stream: bytes | None = None,
    session_state: str | None = None,
    request_attributes: str | None = None,
    response_content_type: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Send an utterance (audio or DTMF) to a Lex V2 bot.

    Args:
        bot_id: The bot identifier.
        bot_alias_id: The bot alias identifier.
        locale_id: The locale identifier.
        session_id: The session identifier.
        request_content_type: MIME type of the input.
        input_stream: Audio bytes or DTMF input.
        session_state: JSON-encoded session state string.
        request_attributes: JSON-encoded request attributes string.
        response_content_type: Desired response content type.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the call fails.
    """
    client = async_client("lexv2-runtime", region_name)
    kwargs: dict[str, Any] = {
        "botId": bot_id,
        "botAliasId": bot_alias_id,
        "localeId": locale_id,
        "sessionId": session_id,
        "requestContentType": request_content_type,
    }
    if input_stream is not None:
        kwargs["inputStream"] = input_stream
    if session_state is not None:
        kwargs["sessionState"] = session_state
    if request_attributes is not None:
        kwargs["requestAttributes"] = request_attributes
    if response_content_type is not None:
        kwargs["responseContentType"] = response_content_type
    try:
        return await client.call("RecognizeUtterance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "recognize_utterance failed") from exc


async def put_session(
    bot_id: str,
    bot_alias_id: str,
    locale_id: str,
    session_id: str,
    session_state: dict[str, Any],
    messages: list[dict[str, Any]] | None = None,
    request_attributes: dict[str, str] | None = None,
    response_content_type: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Set the state of a Lex V2 session.

    Args:
        bot_id: The bot identifier.
        bot_alias_id: The bot alias identifier.
        locale_id: The locale identifier.
        session_id: The session identifier.
        session_state: The session state to set.
        messages: Optional messages to include.
        request_attributes: Optional request attributes.
        response_content_type: Desired response content type.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the call fails.
    """
    client = async_client("lexv2-runtime", region_name)
    kwargs: dict[str, Any] = {
        "botId": bot_id,
        "botAliasId": bot_alias_id,
        "localeId": locale_id,
        "sessionId": session_id,
        "sessionState": session_state,
    }
    if messages is not None:
        kwargs["messages"] = messages
    if request_attributes is not None:
        kwargs["requestAttributes"] = request_attributes
    if response_content_type is not None:
        kwargs["responseContentType"] = response_content_type
    try:
        return await client.call("PutSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "put_session failed") from exc


async def get_session(
    bot_id: str,
    bot_alias_id: str,
    locale_id: str,
    session_id: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Get the current state of a Lex V2 session.

    Args:
        bot_id: The bot identifier.
        bot_alias_id: The bot alias identifier.
        locale_id: The locale identifier.
        session_id: The session identifier.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the call fails.
    """
    client = async_client("lexv2-runtime", region_name)
    try:
        return await client.call(
            "GetSession",
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_id,
            sessionId=session_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "get_session failed") from exc


async def delete_session(
    bot_id: str,
    bot_alias_id: str,
    locale_id: str,
    session_id: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete a Lex V2 session.

    Args:
        bot_id: The bot identifier.
        bot_alias_id: The bot alias identifier.
        locale_id: The locale identifier.
        session_id: The session identifier.
        region_name: AWS region override.

    Returns:
        The full API response dict.

    Raises:
        RuntimeError: If the call fails.
    """
    client = async_client("lexv2-runtime", region_name)
    try:
        return await client.call(
            "DeleteSession",
            botId=bot_id,
            botAliasId=bot_alias_id,
            localeId=locale_id,
            sessionId=session_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_session failed") from exc
