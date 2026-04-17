"""aws_util.ivs --- Amazon Interactive Video Service (IVS) utilities.

Provides helpers for managing IVS channels, stream keys, streams, and
recording configurations.  Each function wraps a single boto3 IVS API
call with structured Pydantic result models and consistent error handling.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchGetChannelResult",
    "BatchGetStreamKeyResult",
    "BatchStartViewerSessionRevocationResult",
    "ChannelResult",
    "CreatePlaybackRestrictionPolicyResult",
    "GetPlaybackKeyPairResult",
    "GetPlaybackRestrictionPolicyResult",
    "GetStreamSessionResult",
    "ImportPlaybackKeyPairResult",
    "ListPlaybackKeyPairsResult",
    "ListPlaybackRestrictionPoliciesResult",
    "ListStreamSessionsResult",
    "ListTagsForResourceResult",
    "RecordingConfigurationResult",
    "StreamKeyResult",
    "StreamResult",
    "UpdatePlaybackRestrictionPolicyResult",
    "batch_get_channel",
    "batch_get_stream_key",
    "batch_start_viewer_session_revocation",
    "create_channel",
    "create_playback_restriction_policy",
    "create_recording_configuration",
    "create_stream_key",
    "delete_channel",
    "delete_playback_key_pair",
    "delete_playback_restriction_policy",
    "delete_recording_configuration",
    "delete_stream_key",
    "get_channel",
    "get_playback_key_pair",
    "get_playback_restriction_policy",
    "get_recording_configuration",
    "get_stream",
    "get_stream_key",
    "get_stream_session",
    "import_playback_key_pair",
    "list_channels",
    "list_playback_key_pairs",
    "list_playback_restriction_policies",
    "list_recording_configurations",
    "list_stream_keys",
    "list_stream_sessions",
    "list_streams",
    "list_tags_for_resource",
    "put_metadata",
    "start_viewer_session_revocation",
    "stop_stream",
    "tag_resource",
    "untag_resource",
    "update_channel",
    "update_playback_restriction_policy",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ChannelResult(BaseModel):
    """Metadata for an IVS channel."""

    model_config = ConfigDict(frozen=True)

    arn: str
    name: str | None = None
    latency_mode: str | None = None
    type: str | None = None
    recording_configuration_arn: str | None = None
    ingest_endpoint: str | None = None
    playback_url: str | None = None
    authorized: bool = False
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class StreamKeyResult(BaseModel):
    """Metadata for an IVS stream key."""

    model_config = ConfigDict(frozen=True)

    arn: str
    channel_arn: str | None = None
    value: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class StreamResult(BaseModel):
    """Metadata for an IVS stream."""

    model_config = ConfigDict(frozen=True)

    channel_arn: str
    stream_id: str | None = None
    state: str | None = None
    health: str | None = None
    viewer_count: int | None = None
    start_time: Any = None
    extra: dict[str, Any] = {}


class RecordingConfigurationResult(BaseModel):
    """Metadata for an IVS recording configuration."""

    model_config = ConfigDict(frozen=True)

    arn: str
    name: str | None = None
    state: str | None = None
    destination_configuration: dict[str, Any] = {}
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_channel(data: dict[str, Any]) -> ChannelResult:
    """Convert a raw API channel dict to a :class:`ChannelResult`."""
    return ChannelResult(
        arn=data.get("arn", ""),
        name=data.get("name"),
        latency_mode=data.get("latencyMode"),
        type=data.get("type"),
        recording_configuration_arn=data.get("recordingConfigurationArn"),
        ingest_endpoint=data.get("ingestEndpoint"),
        playback_url=data.get("playbackUrl"),
        authorized=data.get("authorized", False),
        tags=data.get("tags", {}),
    )


def _parse_stream_key(data: dict[str, Any]) -> StreamKeyResult:
    """Convert a raw API stream key dict to a :class:`StreamKeyResult`."""
    return StreamKeyResult(
        arn=data.get("arn", ""),
        channel_arn=data.get("channelArn"),
        value=data.get("value"),
        tags=data.get("tags", {}),
    )


def _parse_stream(data: dict[str, Any]) -> StreamResult:
    """Convert a raw API stream dict to a :class:`StreamResult`."""
    return StreamResult(
        channel_arn=data.get("channelArn", ""),
        stream_id=data.get("streamId"),
        state=data.get("state"),
        health=data.get("health"),
        viewer_count=data.get("viewerCount"),
        start_time=data.get("startTime"),
    )


def _parse_recording_configuration(
    data: dict[str, Any],
) -> RecordingConfigurationResult:
    """Convert a raw API recording config dict to a model."""
    return RecordingConfigurationResult(
        arn=data.get("arn", ""),
        name=data.get("name"),
        state=data.get("state"),
        destination_configuration=data.get("destinationConfiguration", {}),
        tags=data.get("tags", {}),
    )


# ---------------------------------------------------------------------------
# Channel functions
# ---------------------------------------------------------------------------


def create_channel(
    name: str,
    *,
    latency_mode: str | None = None,
    channel_type: str | None = None,
    recording_configuration_arn: str | None = None,
    authorized: bool | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ChannelResult:
    """Create an IVS channel.

    Args:
        name: Channel name.
        latency_mode: ``"NORMAL"`` or ``"LOW"``.
        channel_type: ``"BASIC"`` or ``"STANDARD"``.
        recording_configuration_arn: ARN of the recording configuration.
        authorized: Whether playback requires authorization.
        tags: Resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ChannelResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {"name": name}
    if latency_mode is not None:
        kwargs["latencyMode"] = latency_mode
    if channel_type is not None:
        kwargs["type"] = channel_type
    if recording_configuration_arn is not None:
        kwargs["recordingConfigurationArn"] = recording_configuration_arn
    if authorized is not None:
        kwargs["authorized"] = authorized
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_channel failed") from exc
    return _parse_channel(resp.get("channel", {}))


def get_channel(
    arn: str,
    *,
    region_name: str | None = None,
) -> ChannelResult:
    """Fetch an IVS channel by ARN.

    Args:
        arn: The channel ARN.
        region_name: AWS region override.

    Returns:
        A :class:`ChannelResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        resp = client.get_channel(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_channel failed for {arn!r}") from exc
    return _parse_channel(resp.get("channel", {}))


def list_channels(
    *,
    filter_by_name: str | None = None,
    filter_by_recording_configuration_arn: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[ChannelResult]:
    """List IVS channels.

    Args:
        filter_by_name: Filter channels by name prefix.
        filter_by_recording_configuration_arn: Filter by recording config.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`ChannelResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if filter_by_name is not None:
        kwargs["filterByName"] = filter_by_name
    if filter_by_recording_configuration_arn is not None:
        kwargs["filterByRecordingConfigurationArn"] = filter_by_recording_configuration_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    channels: list[ChannelResult] = []
    try:
        while True:
            resp = client.list_channels(**kwargs)
            for ch in resp.get("channels", []):
                channels.append(_parse_channel(ch))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_channels failed") from exc
    return channels


def update_channel(
    arn: str,
    *,
    name: str | None = None,
    latency_mode: str | None = None,
    channel_type: str | None = None,
    recording_configuration_arn: str | None = None,
    authorized: bool | None = None,
    region_name: str | None = None,
) -> ChannelResult:
    """Update an IVS channel.

    Args:
        arn: The channel ARN.
        name: New channel name.
        latency_mode: ``"NORMAL"`` or ``"LOW"``.
        channel_type: ``"BASIC"`` or ``"STANDARD"``.
        recording_configuration_arn: ARN of the recording configuration.
        authorized: Whether playback requires authorization.
        region_name: AWS region override.

    Returns:
        A :class:`ChannelResult` with updated values.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {"arn": arn}
    if name is not None:
        kwargs["name"] = name
    if latency_mode is not None:
        kwargs["latencyMode"] = latency_mode
    if channel_type is not None:
        kwargs["type"] = channel_type
    if recording_configuration_arn is not None:
        kwargs["recordingConfigurationArn"] = recording_configuration_arn
    if authorized is not None:
        kwargs["authorized"] = authorized
    try:
        resp = client.update_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_channel failed for {arn!r}") from exc
    return _parse_channel(resp.get("channel", {}))


def delete_channel(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IVS channel.

    Args:
        arn: The channel ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        client.delete_channel(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_channel failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Stream key functions
# ---------------------------------------------------------------------------


def create_stream_key(
    channel_arn: str,
    *,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> StreamKeyResult:
    """Create an IVS stream key.

    Args:
        channel_arn: The channel ARN.
        tags: Resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`StreamKeyResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {"channelArn": channel_arn}
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_stream_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_stream_key failed") from exc
    return _parse_stream_key(resp.get("streamKey", {}))


def get_stream_key(
    arn: str,
    *,
    region_name: str | None = None,
) -> StreamKeyResult:
    """Fetch an IVS stream key by ARN.

    Args:
        arn: The stream key ARN.
        region_name: AWS region override.

    Returns:
        A :class:`StreamKeyResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        resp = client.get_stream_key(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_stream_key failed for {arn!r}") from exc
    return _parse_stream_key(resp.get("streamKey", {}))


def list_stream_keys(
    channel_arn: str,
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[StreamKeyResult]:
    """List IVS stream keys for a channel.

    Args:
        channel_arn: The channel ARN.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`StreamKeyResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {"channelArn": channel_arn}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    keys: list[StreamKeyResult] = []
    try:
        while True:
            resp = client.list_stream_keys(**kwargs)
            for sk in resp.get("streamKeys", []):
                keys.append(_parse_stream_key(sk))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_stream_keys failed") from exc
    return keys


def delete_stream_key(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IVS stream key.

    Args:
        arn: The stream key ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        client.delete_stream_key(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_stream_key failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Stream functions
# ---------------------------------------------------------------------------


def get_stream(
    channel_arn: str,
    *,
    region_name: str | None = None,
) -> StreamResult:
    """Get the active stream for a channel.

    Args:
        channel_arn: The channel ARN.
        region_name: AWS region override.

    Returns:
        A :class:`StreamResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        resp = client.get_stream(channelArn=channel_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_stream failed for {channel_arn!r}") from exc
    return _parse_stream(resp.get("stream", {}))


def list_streams(
    *,
    filter_by_health: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[StreamResult]:
    """List IVS streams.

    Args:
        filter_by_health: Filter by stream health.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`StreamResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if filter_by_health is not None:
        kwargs["filterBy"] = {"health": filter_by_health}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    streams: list[StreamResult] = []
    try:
        while True:
            resp = client.list_streams(**kwargs)
            for s in resp.get("streams", []):
                streams.append(_parse_stream(s))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_streams failed") from exc
    return streams


def stop_stream(
    channel_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Stop an IVS stream.

    Args:
        channel_arn: The channel ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        client.stop_stream(channelArn=channel_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_stream failed for {channel_arn!r}") from exc


# ---------------------------------------------------------------------------
# Recording configuration functions
# ---------------------------------------------------------------------------


def create_recording_configuration(
    destination_configuration: dict[str, Any],
    *,
    name: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> RecordingConfigurationResult:
    """Create an IVS recording configuration.

    Args:
        destination_configuration: Destination config with S3 bucket details.
        name: Recording configuration name.
        tags: Resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`RecordingConfigurationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {
        "destinationConfiguration": destination_configuration,
    }
    if name is not None:
        kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_recording_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_recording_configuration failed") from exc
    return _parse_recording_configuration(resp.get("recordingConfiguration", {}))


def get_recording_configuration(
    arn: str,
    *,
    region_name: str | None = None,
) -> RecordingConfigurationResult:
    """Fetch an IVS recording configuration by ARN.

    Args:
        arn: The recording configuration ARN.
        region_name: AWS region override.

    Returns:
        A :class:`RecordingConfigurationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        resp = client.get_recording_configuration(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_recording_configuration failed for {arn!r}") from exc
    return _parse_recording_configuration(resp.get("recordingConfiguration", {}))


def list_recording_configurations(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[RecordingConfigurationResult]:
    """List IVS recording configurations.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`RecordingConfigurationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    configs: list[RecordingConfigurationResult] = []
    try:
        while True:
            resp = client.list_recording_configurations(**kwargs)
            for rc in resp.get("recordingConfigurations", []):
                configs.append(_parse_recording_configuration(rc))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_recording_configurations failed") from exc
    return configs


def delete_recording_configuration(
    arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IVS recording configuration.

    Args:
        arn: The recording configuration ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    try:
        client.delete_recording_configuration(arn=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_recording_configuration failed for {arn!r}") from exc


class BatchGetChannelResult(BaseModel):
    """Result of batch_get_channel."""

    model_config = ConfigDict(frozen=True)

    channels: list[dict[str, Any]] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchGetStreamKeyResult(BaseModel):
    """Result of batch_get_stream_key."""

    model_config = ConfigDict(frozen=True)

    errors: list[dict[str, Any]] | None = None
    stream_keys: list[dict[str, Any]] | None = None


class BatchStartViewerSessionRevocationResult(BaseModel):
    """Result of batch_start_viewer_session_revocation."""

    model_config = ConfigDict(frozen=True)

    errors: list[dict[str, Any]] | None = None


class CreatePlaybackRestrictionPolicyResult(BaseModel):
    """Result of create_playback_restriction_policy."""

    model_config = ConfigDict(frozen=True)

    playback_restriction_policy: dict[str, Any] | None = None


class GetPlaybackKeyPairResult(BaseModel):
    """Result of get_playback_key_pair."""

    model_config = ConfigDict(frozen=True)

    key_pair: dict[str, Any] | None = None


class GetPlaybackRestrictionPolicyResult(BaseModel):
    """Result of get_playback_restriction_policy."""

    model_config = ConfigDict(frozen=True)

    playback_restriction_policy: dict[str, Any] | None = None


class GetStreamSessionResult(BaseModel):
    """Result of get_stream_session."""

    model_config = ConfigDict(frozen=True)

    stream_session: dict[str, Any] | None = None


class ImportPlaybackKeyPairResult(BaseModel):
    """Result of import_playback_key_pair."""

    model_config = ConfigDict(frozen=True)

    key_pair: dict[str, Any] | None = None


class ListPlaybackKeyPairsResult(BaseModel):
    """Result of list_playback_key_pairs."""

    model_config = ConfigDict(frozen=True)

    key_pairs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPlaybackRestrictionPoliciesResult(BaseModel):
    """Result of list_playback_restriction_policies."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    playback_restriction_policies: list[dict[str, Any]] | None = None


class ListStreamSessionsResult(BaseModel):
    """Result of list_stream_sessions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    stream_sessions: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class UpdatePlaybackRestrictionPolicyResult(BaseModel):
    """Result of update_playback_restriction_policy."""

    model_config = ConfigDict(frozen=True)

    playback_restriction_policy: dict[str, Any] | None = None


def batch_get_channel(
    arns: list[str],
    region_name: str | None = None,
) -> BatchGetChannelResult:
    """Batch get channel.

    Args:
        arns: Arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arns"] = arns
    try:
        resp = client.batch_get_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get channel") from exc
    return BatchGetChannelResult(
        channels=resp.get("channels"),
        errors=resp.get("errors"),
    )


def batch_get_stream_key(
    arns: list[str],
    region_name: str | None = None,
) -> BatchGetStreamKeyResult:
    """Batch get stream key.

    Args:
        arns: Arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arns"] = arns
    try:
        resp = client.batch_get_stream_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get stream key") from exc
    return BatchGetStreamKeyResult(
        errors=resp.get("errors"),
        stream_keys=resp.get("streamKeys"),
    )


def batch_start_viewer_session_revocation(
    viewer_sessions: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchStartViewerSessionRevocationResult:
    """Batch start viewer session revocation.

    Args:
        viewer_sessions: Viewer sessions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["viewerSessions"] = viewer_sessions
    try:
        resp = client.batch_start_viewer_session_revocation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch start viewer session revocation") from exc
    return BatchStartViewerSessionRevocationResult(
        errors=resp.get("errors"),
    )


def create_playback_restriction_policy(
    *,
    allowed_countries: list[str] | None = None,
    allowed_origins: list[str] | None = None,
    enable_strict_origin_enforcement: bool | None = None,
    name: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePlaybackRestrictionPolicyResult:
    """Create playback restriction policy.

    Args:
        allowed_countries: Allowed countries.
        allowed_origins: Allowed origins.
        enable_strict_origin_enforcement: Enable strict origin enforcement.
        name: Name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if allowed_countries is not None:
        kwargs["allowedCountries"] = allowed_countries
    if allowed_origins is not None:
        kwargs["allowedOrigins"] = allowed_origins
    if enable_strict_origin_enforcement is not None:
        kwargs["enableStrictOriginEnforcement"] = enable_strict_origin_enforcement
    if name is not None:
        kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_playback_restriction_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create playback restriction policy") from exc
    return CreatePlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )


def delete_playback_key_pair(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete playback key pair.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        client.delete_playback_key_pair(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete playback key pair") from exc
    return None


def delete_playback_restriction_policy(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete playback restriction policy.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        client.delete_playback_restriction_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete playback restriction policy") from exc
    return None


def get_playback_key_pair(
    arn: str,
    region_name: str | None = None,
) -> GetPlaybackKeyPairResult:
    """Get playback key pair.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = client.get_playback_key_pair(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get playback key pair") from exc
    return GetPlaybackKeyPairResult(
        key_pair=resp.get("keyPair"),
    )


def get_playback_restriction_policy(
    arn: str,
    region_name: str | None = None,
) -> GetPlaybackRestrictionPolicyResult:
    """Get playback restriction policy.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = client.get_playback_restriction_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get playback restriction policy") from exc
    return GetPlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )


def get_stream_session(
    channel_arn: str,
    *,
    stream_id: str | None = None,
    region_name: str | None = None,
) -> GetStreamSessionResult:
    """Get stream session.

    Args:
        channel_arn: Channel arn.
        stream_id: Stream id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    if stream_id is not None:
        kwargs["streamId"] = stream_id
    try:
        resp = client.get_stream_session(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get stream session") from exc
    return GetStreamSessionResult(
        stream_session=resp.get("streamSession"),
    )


def import_playback_key_pair(
    public_key_material: str,
    *,
    name: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ImportPlaybackKeyPairResult:
    """Import playback key pair.

    Args:
        public_key_material: Public key material.
        name: Name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["publicKeyMaterial"] = public_key_material
    if name is not None:
        kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.import_playback_key_pair(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import playback key pair") from exc
    return ImportPlaybackKeyPairResult(
        key_pair=resp.get("keyPair"),
    )


def list_playback_key_pairs(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPlaybackKeyPairsResult:
    """List playback key pairs.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_playback_key_pairs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list playback key pairs") from exc
    return ListPlaybackKeyPairsResult(
        key_pairs=resp.get("keyPairs"),
        next_token=resp.get("nextToken"),
    )


def list_playback_restriction_policies(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPlaybackRestrictionPoliciesResult:
    """List playback restriction policies.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_playback_restriction_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list playback restriction policies") from exc
    return ListPlaybackRestrictionPoliciesResult(
        next_token=resp.get("nextToken"),
        playback_restriction_policies=resp.get("playbackRestrictionPolicies"),
    )


def list_stream_sessions(
    channel_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListStreamSessionsResult:
    """List stream sessions.

    Args:
        channel_arn: Channel arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_stream_sessions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stream sessions") from exc
    return ListStreamSessionsResult(
        next_token=resp.get("nextToken"),
        stream_sessions=resp.get("streamSessions"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def put_metadata(
    channel_arn: str,
    metadata: str,
    region_name: str | None = None,
) -> None:
    """Put metadata.

    Args:
        channel_arn: Channel arn.
        metadata: Metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    kwargs["metadata"] = metadata
    try:
        client.put_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put metadata") from exc
    return None


def start_viewer_session_revocation(
    channel_arn: str,
    viewer_id: str,
    *,
    viewer_session_versions_less_than_or_equal_to: int | None = None,
    region_name: str | None = None,
) -> None:
    """Start viewer session revocation.

    Args:
        channel_arn: Channel arn.
        viewer_id: Viewer id.
        viewer_session_versions_less_than_or_equal_to: Viewer session versions less than or equal to.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    kwargs["viewerId"] = viewer_id
    if viewer_session_versions_less_than_or_equal_to is not None:
        kwargs["viewerSessionVersionsLessThanOrEqualTo"] = (
            viewer_session_versions_less_than_or_equal_to
        )
    try:
        client.start_viewer_session_revocation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start viewer session revocation") from exc
    return None


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_playback_restriction_policy(
    arn: str,
    *,
    allowed_countries: list[str] | None = None,
    allowed_origins: list[str] | None = None,
    enable_strict_origin_enforcement: bool | None = None,
    name: str | None = None,
    region_name: str | None = None,
) -> UpdatePlaybackRestrictionPolicyResult:
    """Update playback restriction policy.

    Args:
        arn: Arn.
        allowed_countries: Allowed countries.
        allowed_origins: Allowed origins.
        enable_strict_origin_enforcement: Enable strict origin enforcement.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    if allowed_countries is not None:
        kwargs["allowedCountries"] = allowed_countries
    if allowed_origins is not None:
        kwargs["allowedOrigins"] = allowed_origins
    if enable_strict_origin_enforcement is not None:
        kwargs["enableStrictOriginEnforcement"] = enable_strict_origin_enforcement
    if name is not None:
        kwargs["name"] = name
    try:
        resp = client.update_playback_restriction_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update playback restriction policy") from exc
    return UpdatePlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )
