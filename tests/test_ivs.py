"""Tests for aws_util.ivs -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.ivs import (
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

_ERR = ClientError(
    {"Error": {"Code": "ServiceException", "Message": "boom"}},
    "op",
)


def _client():
    return MagicMock()


# -------------------------------------------------------------------
# create_channel
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_create_channel_minimal(gc):
    c = _client()
    gc.return_value = c
    c.create_channel.return_value = {
        "channel": {"arn": "arn:ch", "name": "ch1"},
    }
    r = create_channel("ch1")
    assert isinstance(r, ChannelResult)
    assert r.arn == "arn:ch"


@patch("aws_util.ivs.get_client")
def test_create_channel_all_opts(gc):
    c = _client()
    gc.return_value = c
    c.create_channel.return_value = {
        "channel": {
            "arn": "arn:ch",
            "name": "ch1",
            "latencyMode": "LOW",
            "type": "STANDARD",
            "recordingConfigurationArn": "arn:rc",
            "ingestEndpoint": "ep",
            "playbackUrl": "url",
            "authorized": True,
            "tags": {"k": "v"},
        },
    }
    r = create_channel(
        "ch1",
        latency_mode="LOW",
        channel_type="STANDARD",
        recording_configuration_arn="arn:rc",
        authorized=True,
        tags={"k": "v"},
    )
    assert r.latency_mode == "LOW"
    assert r.authorized is True


@patch("aws_util.ivs.get_client")
def test_create_channel_error(gc):
    c = _client()
    gc.return_value = c
    c.create_channel.side_effect = _ERR
    with pytest.raises(RuntimeError):
        create_channel("ch1")


# -------------------------------------------------------------------
# get_channel
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_get_channel_ok(gc):
    c = _client()
    gc.return_value = c
    c.get_channel.return_value = {"channel": {"arn": "arn:ch"}}
    r = get_channel("arn:ch")
    assert r.arn == "arn:ch"


@patch("aws_util.ivs.get_client")
def test_get_channel_error(gc):
    c = _client()
    gc.return_value = c
    c.get_channel.side_effect = _ERR
    with pytest.raises(RuntimeError):
        get_channel("arn:ch")


# -------------------------------------------------------------------
# list_channels
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_list_channels_no_filter(gc):
    c = _client()
    gc.return_value = c
    c.list_channels.return_value = {
        "channels": [{"arn": "arn:ch1"}],
    }
    r = list_channels()
    assert len(r) == 1


@patch("aws_util.ivs.get_client")
def test_list_channels_pagination(gc):
    c = _client()
    gc.return_value = c
    c.list_channels.side_effect = [
        {"channels": [{"arn": "a1"}], "nextToken": "t"},
        {"channels": [{"arn": "a2"}]},
    ]
    r = list_channels(
        filter_by_name="x",
        filter_by_recording_configuration_arn="arn:rc",
        max_results=10,
    )
    assert len(r) == 2


@patch("aws_util.ivs.get_client")
def test_list_channels_error(gc):
    c = _client()
    gc.return_value = c
    c.list_channels.side_effect = _ERR
    with pytest.raises(RuntimeError):
        list_channels()


# -------------------------------------------------------------------
# update_channel
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_update_channel_all_opts(gc):
    c = _client()
    gc.return_value = c
    c.update_channel.return_value = {"channel": {"arn": "arn:ch"}}
    r = update_channel(
        "arn:ch",
        name="n",
        latency_mode="LOW",
        channel_type="BASIC",
        recording_configuration_arn="arn:rc",
        authorized=False,
    )
    assert r.arn == "arn:ch"


@patch("aws_util.ivs.get_client")
def test_update_channel_error(gc):
    c = _client()
    gc.return_value = c
    c.update_channel.side_effect = _ERR
    with pytest.raises(RuntimeError):
        update_channel("arn:ch")


# -------------------------------------------------------------------
# delete_channel
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_delete_channel_ok(gc):
    c = _client()
    gc.return_value = c
    delete_channel("arn:ch")
    c.delete_channel.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_delete_channel_error(gc):
    c = _client()
    gc.return_value = c
    c.delete_channel.side_effect = _ERR
    with pytest.raises(RuntimeError):
        delete_channel("arn:ch")


# -------------------------------------------------------------------
# create_stream_key
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_create_stream_key_ok(gc):
    c = _client()
    gc.return_value = c
    c.create_stream_key.return_value = {
        "streamKey": {"arn": "arn:sk", "channelArn": "arn:ch", "value": "v"},
    }
    r = create_stream_key("arn:ch", tags={"k": "v"})
    assert r.arn == "arn:sk"


@patch("aws_util.ivs.get_client")
def test_create_stream_key_error(gc):
    c = _client()
    gc.return_value = c
    c.create_stream_key.side_effect = _ERR
    with pytest.raises(RuntimeError):
        create_stream_key("arn:ch")


# -------------------------------------------------------------------
# get_stream_key
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_get_stream_key_ok(gc):
    c = _client()
    gc.return_value = c
    c.get_stream_key.return_value = {"streamKey": {"arn": "arn:sk"}}
    r = get_stream_key("arn:sk")
    assert r.arn == "arn:sk"


@patch("aws_util.ivs.get_client")
def test_get_stream_key_error(gc):
    c = _client()
    gc.return_value = c
    c.get_stream_key.side_effect = _ERR
    with pytest.raises(RuntimeError):
        get_stream_key("arn:sk")


# -------------------------------------------------------------------
# list_stream_keys
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_list_stream_keys_pagination(gc):
    c = _client()
    gc.return_value = c
    c.list_stream_keys.side_effect = [
        {"streamKeys": [{"arn": "a1"}], "nextToken": "t"},
        {"streamKeys": [{"arn": "a2"}]},
    ]
    r = list_stream_keys("arn:ch", max_results=1)
    assert len(r) == 2


@patch("aws_util.ivs.get_client")
def test_list_stream_keys_error(gc):
    c = _client()
    gc.return_value = c
    c.list_stream_keys.side_effect = _ERR
    with pytest.raises(RuntimeError):
        list_stream_keys("arn:ch")


# -------------------------------------------------------------------
# delete_stream_key
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_delete_stream_key_ok(gc):
    c = _client()
    gc.return_value = c
    delete_stream_key("arn:sk")


@patch("aws_util.ivs.get_client")
def test_delete_stream_key_error(gc):
    c = _client()
    gc.return_value = c
    c.delete_stream_key.side_effect = _ERR
    with pytest.raises(RuntimeError):
        delete_stream_key("arn:sk")


# -------------------------------------------------------------------
# get_stream
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_get_stream_ok(gc):
    c = _client()
    gc.return_value = c
    c.get_stream.return_value = {
        "stream": {
            "channelArn": "arn:ch",
            "streamId": "sid",
            "state": "LIVE",
            "health": "HEALTHY",
            "viewerCount": 42,
            "startTime": "2024-01-01",
        },
    }
    r = get_stream("arn:ch")
    assert r.state == "LIVE"
    assert r.viewer_count == 42


@patch("aws_util.ivs.get_client")
def test_get_stream_error(gc):
    c = _client()
    gc.return_value = c
    c.get_stream.side_effect = _ERR
    with pytest.raises(RuntimeError):
        get_stream("arn:ch")


# -------------------------------------------------------------------
# list_streams
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_list_streams_pagination(gc):
    c = _client()
    gc.return_value = c
    c.list_streams.side_effect = [
        {"streams": [{"channelArn": "a1"}], "nextToken": "t"},
        {"streams": [{"channelArn": "a2"}]},
    ]
    r = list_streams(filter_by_health="HEALTHY", max_results=1)
    assert len(r) == 2


@patch("aws_util.ivs.get_client")
def test_list_streams_error(gc):
    c = _client()
    gc.return_value = c
    c.list_streams.side_effect = _ERR
    with pytest.raises(RuntimeError):
        list_streams()


# -------------------------------------------------------------------
# stop_stream
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_stop_stream_ok(gc):
    c = _client()
    gc.return_value = c
    stop_stream("arn:ch")


@patch("aws_util.ivs.get_client")
def test_stop_stream_error(gc):
    c = _client()
    gc.return_value = c
    c.stop_stream.side_effect = _ERR
    with pytest.raises(RuntimeError):
        stop_stream("arn:ch")


# -------------------------------------------------------------------
# create_recording_configuration
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_create_recording_configuration_ok(gc):
    c = _client()
    gc.return_value = c
    c.create_recording_configuration.return_value = {
        "recordingConfiguration": {
            "arn": "arn:rc",
            "name": "rc1",
            "state": "ACTIVE",
            "destinationConfiguration": {"s3": {}},
            "tags": {},
        },
    }
    r = create_recording_configuration(
        {"s3": {}}, name="rc1", tags={"k": "v"}
    )
    assert r.arn == "arn:rc"


@patch("aws_util.ivs.get_client")
def test_create_recording_configuration_error(gc):
    c = _client()
    gc.return_value = c
    c.create_recording_configuration.side_effect = _ERR
    with pytest.raises(RuntimeError):
        create_recording_configuration({"s3": {}})


# -------------------------------------------------------------------
# get_recording_configuration
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_get_recording_configuration_ok(gc):
    c = _client()
    gc.return_value = c
    c.get_recording_configuration.return_value = {
        "recordingConfiguration": {"arn": "arn:rc"},
    }
    r = get_recording_configuration("arn:rc")
    assert r.arn == "arn:rc"


@patch("aws_util.ivs.get_client")
def test_get_recording_configuration_error(gc):
    c = _client()
    gc.return_value = c
    c.get_recording_configuration.side_effect = _ERR
    with pytest.raises(RuntimeError):
        get_recording_configuration("arn:rc")


# -------------------------------------------------------------------
# list_recording_configurations
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_list_recording_configurations_pagination(gc):
    c = _client()
    gc.return_value = c
    c.list_recording_configurations.side_effect = [
        {"recordingConfigurations": [{"arn": "a1"}], "nextToken": "t"},
        {"recordingConfigurations": [{"arn": "a2"}]},
    ]
    r = list_recording_configurations(max_results=1)
    assert len(r) == 2


@patch("aws_util.ivs.get_client")
def test_list_recording_configurations_error(gc):
    c = _client()
    gc.return_value = c
    c.list_recording_configurations.side_effect = _ERR
    with pytest.raises(RuntimeError):
        list_recording_configurations()


# -------------------------------------------------------------------
# delete_recording_configuration
# -------------------------------------------------------------------


@patch("aws_util.ivs.get_client")
def test_delete_recording_configuration_ok(gc):
    c = _client()
    gc.return_value = c
    delete_recording_configuration("arn:rc")


@patch("aws_util.ivs.get_client")
def test_delete_recording_configuration_error(gc):
    c = _client()
    gc.return_value = c
    c.delete_recording_configuration.side_effect = _ERR
    with pytest.raises(RuntimeError):
        delete_recording_configuration("arn:rc")


REGION = "us-east-1"


@patch("aws_util.ivs.get_client")
def test_batch_get_channel(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_channel.return_value = {}
    batch_get_channel([], region_name=REGION)
    mock_client.batch_get_channel.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_batch_get_channel_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_channel",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get channel"):
        batch_get_channel([], region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_batch_get_stream_key(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_stream_key.return_value = {}
    batch_get_stream_key([], region_name=REGION)
    mock_client.batch_get_stream_key.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_batch_get_stream_key_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_stream_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_stream_key",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get stream key"):
        batch_get_stream_key([], region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_batch_start_viewer_session_revocation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_start_viewer_session_revocation.return_value = {}
    batch_start_viewer_session_revocation([], region_name=REGION)
    mock_client.batch_start_viewer_session_revocation.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_batch_start_viewer_session_revocation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_start_viewer_session_revocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_start_viewer_session_revocation",
    )
    with pytest.raises(RuntimeError, match="Failed to batch start viewer session revocation"):
        batch_start_viewer_session_revocation([], region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_create_playback_restriction_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_playback_restriction_policy.return_value = {}
    create_playback_restriction_policy(region_name=REGION)
    mock_client.create_playback_restriction_policy.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_create_playback_restriction_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_playback_restriction_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_playback_restriction_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to create playback restriction policy"):
        create_playback_restriction_policy(region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_delete_playback_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_playback_key_pair.return_value = {}
    delete_playback_key_pair("test-arn", region_name=REGION)
    mock_client.delete_playback_key_pair.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_delete_playback_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_playback_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_playback_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to delete playback key pair"):
        delete_playback_key_pair("test-arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_delete_playback_restriction_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_playback_restriction_policy.return_value = {}
    delete_playback_restriction_policy("test-arn", region_name=REGION)
    mock_client.delete_playback_restriction_policy.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_delete_playback_restriction_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_playback_restriction_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_playback_restriction_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to delete playback restriction policy"):
        delete_playback_restriction_policy("test-arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_get_playback_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_playback_key_pair.return_value = {}
    get_playback_key_pair("test-arn", region_name=REGION)
    mock_client.get_playback_key_pair.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_get_playback_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_playback_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_playback_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to get playback key pair"):
        get_playback_key_pair("test-arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_get_playback_restriction_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_playback_restriction_policy.return_value = {}
    get_playback_restriction_policy("test-arn", region_name=REGION)
    mock_client.get_playback_restriction_policy.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_get_playback_restriction_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_playback_restriction_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_playback_restriction_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to get playback restriction policy"):
        get_playback_restriction_policy("test-arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_get_stream_session(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_stream_session.return_value = {}
    get_stream_session("test-channel_arn", region_name=REGION)
    mock_client.get_stream_session.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_get_stream_session_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_stream_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_stream_session",
    )
    with pytest.raises(RuntimeError, match="Failed to get stream session"):
        get_stream_session("test-channel_arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_import_playback_key_pair(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_playback_key_pair.return_value = {}
    import_playback_key_pair("test-public_key_material", region_name=REGION)
    mock_client.import_playback_key_pair.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_import_playback_key_pair_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.import_playback_key_pair.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_playback_key_pair",
    )
    with pytest.raises(RuntimeError, match="Failed to import playback key pair"):
        import_playback_key_pair("test-public_key_material", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_list_playback_key_pairs(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_playback_key_pairs.return_value = {}
    list_playback_key_pairs(region_name=REGION)
    mock_client.list_playback_key_pairs.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_list_playback_key_pairs_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_playback_key_pairs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_playback_key_pairs",
    )
    with pytest.raises(RuntimeError, match="Failed to list playback key pairs"):
        list_playback_key_pairs(region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_list_playback_restriction_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_playback_restriction_policies.return_value = {}
    list_playback_restriction_policies(region_name=REGION)
    mock_client.list_playback_restriction_policies.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_list_playback_restriction_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_playback_restriction_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_playback_restriction_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to list playback restriction policies"):
        list_playback_restriction_policies(region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_list_stream_sessions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_stream_sessions.return_value = {}
    list_stream_sessions("test-channel_arn", region_name=REGION)
    mock_client.list_stream_sessions.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_list_stream_sessions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_stream_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stream_sessions",
    )
    with pytest.raises(RuntimeError, match="Failed to list stream sessions"):
        list_stream_sessions("test-channel_arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_put_metadata(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_metadata.return_value = {}
    put_metadata("test-channel_arn", "test-metadata", region_name=REGION)
    mock_client.put_metadata.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_put_metadata_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_metadata",
    )
    with pytest.raises(RuntimeError, match="Failed to put metadata"):
        put_metadata("test-channel_arn", "test-metadata", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_start_viewer_session_revocation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_viewer_session_revocation.return_value = {}
    start_viewer_session_revocation("test-channel_arn", "test-viewer_id", region_name=REGION)
    mock_client.start_viewer_session_revocation.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_start_viewer_session_revocation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_viewer_session_revocation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_viewer_session_revocation",
    )
    with pytest.raises(RuntimeError, match="Failed to start viewer session revocation"):
        start_viewer_session_revocation("test-channel_arn", "test-viewer_id", region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.ivs.get_client")
def test_update_playback_restriction_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_playback_restriction_policy.return_value = {}
    update_playback_restriction_policy("test-arn", region_name=REGION)
    mock_client.update_playback_restriction_policy.assert_called_once()


@patch("aws_util.ivs.get_client")
def test_update_playback_restriction_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_playback_restriction_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_playback_restriction_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to update playback restriction policy"):
        update_playback_restriction_policy("test-arn", region_name=REGION)


def test_create_channel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import create_channel
    mock_client = MagicMock()
    mock_client.create_channel.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    create_channel("test-name", latency_mode="test-latency_mode", channel_type="test-channel_type", recording_configuration_arn={}, authorized="test-authorized", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_channel.assert_called_once()

def test_list_channels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_channels
    mock_client = MagicMock()
    mock_client.list_channels.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_channels(filter_by_name="test-filter_by_name", filter_by_recording_configuration_arn={}, max_results=1, region_name="us-east-1")
    mock_client.list_channels.assert_called_once()

def test_update_channel_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import update_channel
    mock_client = MagicMock()
    mock_client.update_channel.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    update_channel("test-arn", name="test-name", latency_mode="test-latency_mode", channel_type="test-channel_type", recording_configuration_arn={}, authorized="test-authorized", region_name="us-east-1")
    mock_client.update_channel.assert_called_once()

def test_create_stream_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import create_stream_key
    mock_client = MagicMock()
    mock_client.create_stream_key.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    create_stream_key("test-channel_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_stream_key.assert_called_once()

def test_list_stream_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_stream_keys
    mock_client = MagicMock()
    mock_client.list_stream_keys.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_stream_keys("test-channel_arn", max_results=1, region_name="us-east-1")
    mock_client.list_stream_keys.assert_called_once()

def test_list_streams_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_streams
    mock_client = MagicMock()
    mock_client.list_streams.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_streams(filter_by_health="test-filter_by_health", max_results=1, region_name="us-east-1")
    mock_client.list_streams.assert_called_once()

def test_create_recording_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import create_recording_configuration
    mock_client = MagicMock()
    mock_client.create_recording_configuration.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    create_recording_configuration({}, name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_recording_configuration.assert_called_once()

def test_list_recording_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_recording_configurations
    mock_client = MagicMock()
    mock_client.list_recording_configurations.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_recording_configurations(max_results=1, region_name="us-east-1")
    mock_client.list_recording_configurations.assert_called_once()

def test_create_playback_restriction_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import create_playback_restriction_policy
    mock_client = MagicMock()
    mock_client.create_playback_restriction_policy.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    create_playback_restriction_policy(allowed_countries=True, allowed_origins=True, enable_strict_origin_enforcement=True, name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_playback_restriction_policy.assert_called_once()

def test_get_stream_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import get_stream_session
    mock_client = MagicMock()
    mock_client.get_stream_session.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    get_stream_session("test-channel_arn", stream_id="test-stream_id", region_name="us-east-1")
    mock_client.get_stream_session.assert_called_once()

def test_import_playback_key_pair_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import import_playback_key_pair
    mock_client = MagicMock()
    mock_client.import_playback_key_pair.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    import_playback_key_pair("test-public_key_material", name="test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.import_playback_key_pair.assert_called_once()

def test_list_playback_key_pairs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_playback_key_pairs
    mock_client = MagicMock()
    mock_client.list_playback_key_pairs.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_playback_key_pairs(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_playback_key_pairs.assert_called_once()

def test_list_playback_restriction_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_playback_restriction_policies
    mock_client = MagicMock()
    mock_client.list_playback_restriction_policies.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_playback_restriction_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_playback_restriction_policies.assert_called_once()

def test_list_stream_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import list_stream_sessions
    mock_client = MagicMock()
    mock_client.list_stream_sessions.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    list_stream_sessions("test-channel_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_stream_sessions.assert_called_once()

def test_start_viewer_session_revocation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import start_viewer_session_revocation
    mock_client = MagicMock()
    mock_client.start_viewer_session_revocation.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    start_viewer_session_revocation("test-channel_arn", "test-viewer_id", viewer_session_versions_less_than_or_equal_to="test-viewer_session_versions_less_than_or_equal_to", region_name="us-east-1")
    mock_client.start_viewer_session_revocation.assert_called_once()

def test_update_playback_restriction_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.ivs import update_playback_restriction_policy
    mock_client = MagicMock()
    mock_client.update_playback_restriction_policy.return_value = {}
    monkeypatch.setattr("aws_util.ivs.get_client", lambda *a, **kw: mock_client)
    update_playback_restriction_policy("test-arn", allowed_countries=True, allowed_origins=True, enable_strict_origin_enforcement=True, name="test-name", region_name="us-east-1")
    mock_client.update_playback_restriction_policy.assert_called_once()
