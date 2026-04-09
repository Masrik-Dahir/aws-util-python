"""Native async Amazon IVS utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.ivs import (
    BatchGetChannelResult,
    BatchGetStreamKeyResult,
    BatchStartViewerSessionRevocationResult,
    ChannelResult,
    CreatePlaybackRestrictionPolicyResult,
    GetPlaybackKeyPairResult,
    GetPlaybackRestrictionPolicyResult,
    GetStreamSessionResult,
    ImportPlaybackKeyPairResult,
    ListPlaybackKeyPairsResult,
    ListPlaybackRestrictionPoliciesResult,
    ListStreamSessionsResult,
    ListTagsForResourceResult,
    RecordingConfigurationResult,
    StreamKeyResult,
    StreamResult,
    UpdatePlaybackRestrictionPolicyResult,
    _parse_channel,
    _parse_recording_configuration,
    _parse_stream,
    _parse_stream_key,
)

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
# Channel functions
# ---------------------------------------------------------------------------


async def create_channel(
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
    client = async_client("ivs", region_name)
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
        resp = await client.call("CreateChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_channel failed") from exc
    return _parse_channel(resp.get("channel", {}))


async def get_channel(
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
    client = async_client("ivs", region_name)
    try:
        resp = await client.call("GetChannel", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_channel failed for {arn!r}") from exc
    return _parse_channel(resp.get("channel", {}))


async def list_channels(
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
    client = async_client("ivs", region_name)
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
            resp = await client.call("ListChannels", **kwargs)
            for ch in resp.get("channels", []):
                channels.append(_parse_channel(ch))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_channels failed") from exc
    return channels


async def update_channel(
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
    client = async_client("ivs", region_name)
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
        resp = await client.call("UpdateChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_channel failed for {arn!r}") from exc
    return _parse_channel(resp.get("channel", {}))


async def delete_channel(
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
    client = async_client("ivs", region_name)
    try:
        await client.call("DeleteChannel", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_channel failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Stream key functions
# ---------------------------------------------------------------------------


async def create_stream_key(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {"channelArn": channel_arn}
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateStreamKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_stream_key failed") from exc
    return _parse_stream_key(resp.get("streamKey", {}))


async def get_stream_key(
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
    client = async_client("ivs", region_name)
    try:
        resp = await client.call("GetStreamKey", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_stream_key failed for {arn!r}") from exc
    return _parse_stream_key(resp.get("streamKey", {}))


async def list_stream_keys(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {"channelArn": channel_arn}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    keys: list[StreamKeyResult] = []
    try:
        while True:
            resp = await client.call("ListStreamKeys", **kwargs)
            for sk in resp.get("streamKeys", []):
                keys.append(_parse_stream_key(sk))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_stream_keys failed") from exc
    return keys


async def delete_stream_key(
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
    client = async_client("ivs", region_name)
    try:
        await client.call("DeleteStreamKey", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_stream_key failed for {arn!r}") from exc


# ---------------------------------------------------------------------------
# Stream functions
# ---------------------------------------------------------------------------


async def get_stream(
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
    client = async_client("ivs", region_name)
    try:
        resp = await client.call("GetStream", channelArn=channel_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_stream failed for {channel_arn!r}") from exc
    return _parse_stream(resp.get("stream", {}))


async def list_streams(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if filter_by_health is not None:
        kwargs["filterBy"] = {"health": filter_by_health}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    streams: list[StreamResult] = []
    try:
        while True:
            resp = await client.call("ListStreams", **kwargs)
            for s in resp.get("streams", []):
                streams.append(_parse_stream(s))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_streams failed") from exc
    return streams


async def stop_stream(
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
    client = async_client("ivs", region_name)
    try:
        await client.call("StopStream", channelArn=channel_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"stop_stream failed for {channel_arn!r}") from exc


# ---------------------------------------------------------------------------
# Recording configuration functions
# ---------------------------------------------------------------------------


async def create_recording_configuration(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {
        "destinationConfiguration": destination_configuration,
    }
    if name is not None:
        kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRecordingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_recording_configuration failed") from exc
    return _parse_recording_configuration(resp.get("recordingConfiguration", {}))


async def get_recording_configuration(
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
    client = async_client("ivs", region_name)
    try:
        resp = await client.call("GetRecordingConfiguration", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_recording_configuration failed for {arn!r}") from exc
    return _parse_recording_configuration(resp.get("recordingConfiguration", {}))


async def list_recording_configurations(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    configs: list[RecordingConfigurationResult] = []
    try:
        while True:
            resp = await client.call("ListRecordingConfigurations", **kwargs)
            for rc in resp.get("recordingConfigurations", []):
                configs.append(_parse_recording_configuration(rc))
            next_token = resp.get("nextToken")
            if not next_token:
                break
            kwargs["nextToken"] = next_token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_recording_configurations failed") from exc
    return configs


async def delete_recording_configuration(
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
    client = async_client("ivs", region_name)
    try:
        await client.call("DeleteRecordingConfiguration", arn=arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_recording_configuration failed for {arn!r}") from exc


async def batch_get_channel(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arns"] = arns
    try:
        resp = await client.call("BatchGetChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get channel") from exc
    return BatchGetChannelResult(
        channels=resp.get("channels"),
        errors=resp.get("errors"),
    )


async def batch_get_stream_key(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arns"] = arns
    try:
        resp = await client.call("BatchGetStreamKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get stream key") from exc
    return BatchGetStreamKeyResult(
        errors=resp.get("errors"),
        stream_keys=resp.get("streamKeys"),
    )


async def batch_start_viewer_session_revocation(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["viewerSessions"] = viewer_sessions
    try:
        resp = await client.call("BatchStartViewerSessionRevocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch start viewer session revocation") from exc
    return BatchStartViewerSessionRevocationResult(
        errors=resp.get("errors"),
    )


async def create_playback_restriction_policy(
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
    client = async_client("ivs", region_name)
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
        resp = await client.call("CreatePlaybackRestrictionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create playback restriction policy") from exc
    return CreatePlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )


async def delete_playback_key_pair(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        await client.call("DeletePlaybackKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete playback key pair") from exc
    return None


async def delete_playback_restriction_policy(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        await client.call("DeletePlaybackRestrictionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete playback restriction policy") from exc
    return None


async def get_playback_key_pair(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = await client.call("GetPlaybackKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get playback key pair") from exc
    return GetPlaybackKeyPairResult(
        key_pair=resp.get("keyPair"),
    )


async def get_playback_restriction_policy(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = await client.call("GetPlaybackRestrictionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get playback restriction policy") from exc
    return GetPlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )


async def get_stream_session(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    if stream_id is not None:
        kwargs["streamId"] = stream_id
    try:
        resp = await client.call("GetStreamSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get stream session") from exc
    return GetStreamSessionResult(
        stream_session=resp.get("streamSession"),
    )


async def import_playback_key_pair(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["publicKeyMaterial"] = public_key_material
    if name is not None:
        kwargs["name"] = name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("ImportPlaybackKeyPair", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import playback key pair") from exc
    return ImportPlaybackKeyPairResult(
        key_pair=resp.get("keyPair"),
    )


async def list_playback_key_pairs(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPlaybackKeyPairs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list playback key pairs") from exc
    return ListPlaybackKeyPairsResult(
        key_pairs=resp.get("keyPairs"),
        next_token=resp.get("nextToken"),
    )


async def list_playback_restriction_policies(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPlaybackRestrictionPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list playback restriction policies") from exc
    return ListPlaybackRestrictionPoliciesResult(
        next_token=resp.get("nextToken"),
        playback_restriction_policies=resp.get("playbackRestrictionPolicies"),
    )


async def list_stream_sessions(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListStreamSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list stream sessions") from exc
    return ListStreamSessionsResult(
        next_token=resp.get("nextToken"),
        stream_sessions=resp.get("streamSessions"),
    )


async def list_tags_for_resource(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def put_metadata(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    kwargs["metadata"] = metadata
    try:
        await client.call("PutMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put metadata") from exc
    return None


async def start_viewer_session_revocation(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["channelArn"] = channel_arn
    kwargs["viewerId"] = viewer_id
    if viewer_session_versions_less_than_or_equal_to is not None:
        kwargs["viewerSessionVersionsLessThanOrEqualTo"] = (
            viewer_session_versions_less_than_or_equal_to
        )
    try:
        await client.call("StartViewerSessionRevocation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start viewer session revocation") from exc
    return None


async def tag_resource(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("ivs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_playback_restriction_policy(
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
    client = async_client("ivs", region_name)
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
        resp = await client.call("UpdatePlaybackRestrictionPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update playback restriction policy") from exc
    return UpdatePlaybackRestrictionPolicyResult(
        playback_restriction_policy=resp.get("playbackRestrictionPolicy"),
    )
