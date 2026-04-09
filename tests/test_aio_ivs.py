"""Tests for aws_util.aio.ivs -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.ivs import (
    ChannelResult,
    RecordingConfigurationResult,
    StreamKeyResult,
    StreamResult,
    create_channel,
    create_recording_configuration,
    create_stream_key,
    delete_channel,
    delete_recording_configuration,
    delete_stream_key,
    get_channel,
    get_recording_configuration,
    get_stream,
    get_stream_key,
    list_channels,
    list_recording_configurations,
    list_stream_keys,
    list_streams,
    stop_stream,
    update_channel,
    batch_get_channel,
    batch_get_stream_key,
    batch_start_viewer_session_revocation,
    create_playback_restriction_policy,
    delete_playback_key_pair,
    delete_playback_restriction_policy,
    get_playback_key_pair,
    get_playback_restriction_policy,
    get_stream_session,
    import_playback_key_pair,
    list_playback_key_pairs,
    list_playback_restriction_policies,
    list_stream_sessions,
    list_tags_for_resource,
    put_metadata,
    start_viewer_session_revocation,
    tag_resource,
    untag_resource,
    update_playback_restriction_policy,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


def test_models_re_exported():
    assert ChannelResult is not None
    assert StreamKeyResult is not None
    assert StreamResult is not None
    assert RecordingConfigurationResult is not None


class TestCreateChannel:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"channel": {"arn": "arn:ch", "name": "test"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_channel("test")
        assert result.arn == "arn:ch"

    @pytest.mark.asyncio
    async def test_all_optionals(self, monkeypatch):
        mc = _mc({"channel": {"arn": "arn:ch", "name": "test"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_channel(
            "test", latency_mode="LOW", channel_type="STANDARD",
            recording_configuration_arn="arn:rc", authorized=True,
            tags={"env": "dev"}, region_name="us-west-2",
        )
        assert result.arn == "arn:ch"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await create_channel("test")


class TestGetChannel:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"channel": {"arn": "arn:ch", "name": "test"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await get_channel("arn:ch")
        assert result.arn == "arn:ch"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_channel("arn:ch")


class TestListChannels:
    @pytest.mark.asyncio
    async def test_single_page(self, monkeypatch):
        mc = _mc({"channels": [{"arn": "arn:ch"}]})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_channels()
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_with_optionals(self, monkeypatch):
        mc = _mc({"channels": []})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_channels(
            filter_by_name="test",
            filter_by_recording_configuration_arn="arn:rc",
            max_results=10,
        )
        assert result == []

    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"channels": [{"arn": "arn:ch1"}], "nextToken": "tok"},
            {"channels": [{"arn": "arn:ch2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_channels()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_channels()


class TestUpdateChannel:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"channel": {"arn": "arn:ch"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await update_channel("arn:ch")
        assert result.arn == "arn:ch"

    @pytest.mark.asyncio
    async def test_all_optionals(self, monkeypatch):
        mc = _mc({"channel": {"arn": "arn:ch"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await update_channel(
            "arn:ch", name="updated", latency_mode="NORMAL",
            channel_type="BASIC", recording_configuration_arn="arn:rc",
            authorized=False, region_name="us-west-2",
        )
        assert result.arn == "arn:ch"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await update_channel("arn:ch")


class TestDeleteChannel:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        await delete_channel("arn:ch")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await delete_channel("arn:ch")


class TestCreateStreamKey:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"streamKey": {"arn": "arn:sk", "channelArn": "arn:ch"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_stream_key("arn:ch")
        assert result.arn == "arn:sk"

    @pytest.mark.asyncio
    async def test_with_tags(self, monkeypatch):
        mc = _mc({"streamKey": {"arn": "arn:sk"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_stream_key("arn:ch", tags={"a": "b"})
        assert result.arn == "arn:sk"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await create_stream_key("arn:ch")


class TestGetStreamKey:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"streamKey": {"arn": "arn:sk"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await get_stream_key("arn:sk")
        assert result.arn == "arn:sk"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_stream_key("arn:sk")


class TestListStreamKeys:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"streamKeys": [{"arn": "arn:sk1"}], "nextToken": "tok"},
            {"streamKeys": [{"arn": "arn:sk2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_stream_keys("arn:ch", max_results=1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_stream_keys("arn:ch")


class TestDeleteStreamKey:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        await delete_stream_key("arn:sk")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await delete_stream_key("arn:sk")


class TestGetStream:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"stream": {"channelArn": "arn:ch", "state": "LIVE"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await get_stream("arn:ch")
        assert result.state == "LIVE"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_stream("arn:ch")


class TestListStreams:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"streams": [{"channelArn": "arn:ch1"}], "nextToken": "tok"},
            {"streams": [{"channelArn": "arn:ch2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_streams(filter_by_health="HEALTHY", max_results=1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_streams()


class TestStopStream:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        await stop_stream("arn:ch")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await stop_stream("arn:ch")


class TestCreateRecordingConfiguration:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"recordingConfiguration": {"arn": "arn:rc", "name": "rc"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_recording_configuration({"s3": {"bucketName": "b"}})
        assert result.arn == "arn:rc"

    @pytest.mark.asyncio
    async def test_with_optionals(self, monkeypatch):
        mc = _mc({"recordingConfiguration": {"arn": "arn:rc"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await create_recording_configuration(
            {"s3": {"bucketName": "b"}}, name="rc", tags={"a": "b"},
            region_name="us-west-2",
        )
        assert result.arn == "arn:rc"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await create_recording_configuration({"s3": {}})


class TestGetRecordingConfiguration:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"recordingConfiguration": {"arn": "arn:rc"}})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await get_recording_configuration("arn:rc")
        assert result.arn == "arn:rc"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_recording_configuration("arn:rc")


class TestListRecordingConfigurations:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"recordingConfigurations": [{"arn": "arn:rc1"}], "nextToken": "tok"},
            {"recordingConfigurations": [{"arn": "arn:rc2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        result = await list_recording_configurations(max_results=1)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_recording_configurations()


class TestDeleteRecordingConfiguration:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        await delete_recording_configuration("arn:rc")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await delete_recording_configuration("arn:rc")


async def test_batch_get_channel(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_channel([], )
    mock_client.call.assert_called_once()


async def test_batch_get_channel_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_channel([], )


async def test_batch_get_stream_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_stream_key([], )
    mock_client.call.assert_called_once()


async def test_batch_get_stream_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_stream_key([], )


async def test_batch_start_viewer_session_revocation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_start_viewer_session_revocation([], )
    mock_client.call.assert_called_once()


async def test_batch_start_viewer_session_revocation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_start_viewer_session_revocation([], )


async def test_create_playback_restriction_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_playback_restriction_policy()
    mock_client.call.assert_called_once()


async def test_create_playback_restriction_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_playback_restriction_policy()


async def test_delete_playback_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_playback_key_pair("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_playback_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_playback_key_pair("test-arn", )


async def test_delete_playback_restriction_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_playback_restriction_policy("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_playback_restriction_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_playback_restriction_policy("test-arn", )


async def test_get_playback_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_playback_key_pair("test-arn", )
    mock_client.call.assert_called_once()


async def test_get_playback_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_playback_key_pair("test-arn", )


async def test_get_playback_restriction_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_playback_restriction_policy("test-arn", )
    mock_client.call.assert_called_once()


async def test_get_playback_restriction_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_playback_restriction_policy("test-arn", )


async def test_get_stream_session(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_stream_session("test-channel_arn", )
    mock_client.call.assert_called_once()


async def test_get_stream_session_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_stream_session("test-channel_arn", )


async def test_import_playback_key_pair(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_playback_key_pair("test-public_key_material", )
    mock_client.call.assert_called_once()


async def test_import_playback_key_pair_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_playback_key_pair("test-public_key_material", )


async def test_list_playback_key_pairs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_playback_key_pairs()
    mock_client.call.assert_called_once()


async def test_list_playback_key_pairs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_playback_key_pairs()


async def test_list_playback_restriction_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_playback_restriction_policies()
    mock_client.call.assert_called_once()


async def test_list_playback_restriction_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_playback_restriction_policies()


async def test_list_stream_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_stream_sessions("test-channel_arn", )
    mock_client.call.assert_called_once()


async def test_list_stream_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_stream_sessions("test-channel_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_metadata("test-channel_arn", "test-metadata", )
    mock_client.call.assert_called_once()


async def test_put_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_metadata("test-channel_arn", "test-metadata", )


async def test_start_viewer_session_revocation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_viewer_session_revocation("test-channel_arn", "test-viewer_id", )
    mock_client.call.assert_called_once()


async def test_start_viewer_session_revocation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_viewer_session_revocation("test-channel_arn", "test-viewer_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_playback_restriction_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_playback_restriction_policy("test-arn", )
    mock_client.call.assert_called_once()


async def test_update_playback_restriction_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.ivs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_playback_restriction_policy("test-arn", )


@pytest.mark.asyncio
async def test_create_channel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import create_channel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await create_channel("test-name", latency_mode="test-latency_mode", channel_type="test-channel_type", recording_configuration_arn={}, authorized="test-authorized", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_channels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_channels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_channels(filter_by_name="test-filter_by_name", filter_by_recording_configuration_arn={}, max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_channel_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import update_channel
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await update_channel("test-arn", name="test-name", latency_mode="test-latency_mode", channel_type="test-channel_type", recording_configuration_arn={}, authorized="test-authorized", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stream_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import create_stream_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await create_stream_key("test-channel_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stream_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_stream_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_stream_keys("test-channel_arn", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_streams_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_streams
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_streams(filter_by_health="test-filter_by_health", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_recording_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import create_recording_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await create_recording_configuration({}, name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_recording_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_recording_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_recording_configurations(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_playback_restriction_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import create_playback_restriction_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await create_playback_restriction_policy(allowed_countries=True, allowed_origins=True, enable_strict_origin_enforcement=True, name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_stream_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import get_stream_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await get_stream_session("test-channel_arn", stream_id="test-stream_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_playback_key_pair_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import import_playback_key_pair
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await import_playback_key_pair("test-public_key_material", name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_playback_key_pairs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_playback_key_pairs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_playback_key_pairs(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_playback_restriction_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_playback_restriction_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_playback_restriction_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stream_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import list_stream_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await list_stream_sessions("test-channel_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_viewer_session_revocation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import start_viewer_session_revocation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await start_viewer_session_revocation("test-channel_arn", "test-viewer_id", viewer_session_versions_less_than_or_equal_to="test-viewer_session_versions_less_than_or_equal_to", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_playback_restriction_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.ivs import update_playback_restriction_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.ivs.async_client", lambda *a, **kw: mock_client)
    await update_playback_restriction_policy("test-arn", allowed_countries=True, allowed_origins=True, enable_strict_origin_enforcement=True, name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()
