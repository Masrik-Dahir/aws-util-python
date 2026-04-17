"""aws_util.iot_data --- AWS IoT Data Plane utilities.

Provides functions for interacting with the AWS IoT Data Plane (``iot-data``
boto3 service): publishing messages, managing device shadows, and working with
retained messages.
"""

from __future__ import annotations

import json
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "RetainedMessageResult",
    "ShadowResult",
    "delete_connection",
    "delete_thing_shadow",
    "get_retained_message",
    "get_thing_shadow",
    "list_named_shadows_for_thing",
    "list_retained_messages",
    "publish",
    "update_thing_shadow",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ShadowResult(BaseModel):
    """Metadata for an IoT thing shadow."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    payload: dict[str, Any] = {}
    extra: dict[str, Any] = {}


class RetainedMessageResult(BaseModel):
    """Metadata for a retained MQTT message."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    topic: str = ""
    payload: bytes = b""
    qos: int = 0
    last_modified_time: int = 0
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Publish
# ---------------------------------------------------------------------------


def publish(
    topic: str,
    *,
    payload: str | bytes | None = None,
    qos: int = 0,
    retain: bool = False,
    region_name: str | None = None,
) -> None:
    """Publish a message to an MQTT topic.

    Args:
        topic: The MQTT topic to publish to.
        payload: Message payload (string or bytes).
        qos: MQTT QoS level (0 or 1).
        retain: Whether to set the MQTT retain flag.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {"topic": topic, "qos": qos, "retain": retain}
    if payload is not None:
        if isinstance(payload, str):
            kwargs["payload"] = payload.encode("utf-8")
        else:
            kwargs["payload"] = payload
    try:
        client.publish(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"publish failed for topic {topic!r}") from exc


# ---------------------------------------------------------------------------
# Shadow operations
# ---------------------------------------------------------------------------


def get_thing_shadow(
    thing_name: str,
    *,
    shadow_name: str | None = None,
    region_name: str | None = None,
) -> ShadowResult:
    """Get the shadow for a thing.

    Args:
        thing_name: The IoT thing name.
        shadow_name: Named shadow name (``None`` for the classic shadow).
        region_name: AWS region override.

    Returns:
        A :class:`ShadowResult` with the shadow payload.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {"thingName": thing_name}
    if shadow_name is not None:
        kwargs["shadowName"] = shadow_name
    try:
        resp = client.get_thing_shadow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_thing_shadow failed for {thing_name!r}") from exc
    body = resp.get("payload")
    payload_dict: dict[str, Any] = {}
    if body is not None:
        raw = body.read() if hasattr(body, "read") else body
        if raw:
            payload_dict = json.loads(raw)
    return ShadowResult(payload=payload_dict)


def update_thing_shadow(
    thing_name: str,
    *,
    payload: dict[str, Any],
    shadow_name: str | None = None,
    region_name: str | None = None,
) -> ShadowResult:
    """Update the shadow for a thing.

    Args:
        thing_name: The IoT thing name.
        payload: Shadow document dict.
        shadow_name: Named shadow name (``None`` for the classic shadow).
        region_name: AWS region override.

    Returns:
        A :class:`ShadowResult` with the updated shadow payload.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {
        "thingName": thing_name,
        "payload": json.dumps(payload).encode("utf-8"),
    }
    if shadow_name is not None:
        kwargs["shadowName"] = shadow_name
    try:
        resp = client.update_thing_shadow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_thing_shadow failed for {thing_name!r}") from exc
    body = resp.get("payload")
    payload_dict: dict[str, Any] = {}
    if body is not None:
        raw = body.read() if hasattr(body, "read") else body
        if raw:
            payload_dict = json.loads(raw)
    return ShadowResult(payload=payload_dict)


def delete_thing_shadow(
    thing_name: str,
    *,
    shadow_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete the shadow for a thing.

    Args:
        thing_name: The IoT thing name.
        shadow_name: Named shadow name (``None`` for the classic shadow).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {"thingName": thing_name}
    if shadow_name is not None:
        kwargs["shadowName"] = shadow_name
    try:
        client.delete_thing_shadow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_thing_shadow failed for {thing_name!r}") from exc


def list_named_shadows_for_thing(
    thing_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List named shadows for a thing.

    Args:
        thing_name: The IoT thing name.
        region_name: AWS region override.

    Returns:
        A list of shadow name strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {"thingName": thing_name}
    results: list[str] = []
    try:
        while True:
            resp = client.list_named_shadows_for_thing(**kwargs)
            results.extend(resp.get("results", []))
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"list_named_shadows_for_thing failed for {thing_name!r}",
        ) from exc
    return results


# ---------------------------------------------------------------------------
# Retained messages
# ---------------------------------------------------------------------------


def get_retained_message(
    topic: str,
    *,
    region_name: str | None = None,
) -> RetainedMessageResult:
    """Get the retained message for a topic.

    Args:
        topic: The MQTT topic.
        region_name: AWS region override.

    Returns:
        A :class:`RetainedMessageResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    try:
        resp = client.get_retained_message(topic=topic)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_retained_message failed for {topic!r}") from exc
    payload_raw = resp.get("payload", b"")
    if hasattr(payload_raw, "read"):
        payload_raw = payload_raw.read()
    return RetainedMessageResult(
        topic=resp.get("topic", topic),
        payload=payload_raw if isinstance(payload_raw, bytes) else b"",
        qos=resp.get("qos", 0),
        last_modified_time=resp.get("lastModifiedTime", 0),
        extra={
            k: v
            for k, v in resp.items()
            if k not in {"topic", "payload", "qos", "lastModifiedTime", "ResponseMetadata"}
        },
    )


def list_retained_messages(
    *,
    region_name: str | None = None,
) -> list[RetainedMessageResult]:
    """List all retained messages.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`RetainedMessageResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    results: list[RetainedMessageResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_retained_messages(**kwargs)
            for item in resp.get("retainedTopics", []):
                results.append(
                    RetainedMessageResult(
                        topic=item.get("topic", ""),
                        qos=item.get("qos", 0),
                        last_modified_time=item.get("lastModifiedTime", 0),
                    )
                )
            token = resp.get("nextToken")
            if not token:
                break
            kwargs["nextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_retained_messages failed") from exc
    return results


def delete_connection(
    client_id: str,
    *,
    clean_session: bool | None = None,
    prevent_will_message: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete connection.

    Args:
        client_id: Client id.
        clean_session: Clean session.
        prevent_will_message: Prevent will message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("iot-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clientId"] = client_id
    if clean_session is not None:
        kwargs["cleanSession"] = clean_session
    if prevent_will_message is not None:
        kwargs["preventWillMessage"] = prevent_will_message
    try:
        client.delete_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return None
