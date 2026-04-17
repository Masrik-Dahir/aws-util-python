"""Tests for aws_util.media_processing module."""
from __future__ import annotations

import json
import time
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.media_processing as mod
from aws_util.media_processing import (
    MediaConvertResult,
    StreamArchiveResult,
    ivs_stream_recording_archiver,
    mediaconvert_job_orchestrator,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_stream_archive_result(self) -> None:
        r = StreamArchiveResult(recordings_archived=2, archive_keys=["k1", "k2"])
        assert r.recordings_archived == 2
        assert len(r.archive_keys) == 2

    def test_media_convert_result(self) -> None:
        r = MediaConvertResult(
            job_id="j1", status="COMPLETE",
            output_uri="s3://out/video", duration_seconds=123.4,
        )
        assert r.status == "COMPLETE"
        assert r.duration_seconds == 123.4

    def test_frozen(self) -> None:
        r = StreamArchiveResult(recordings_archived=0, archive_keys=[])
        with pytest.raises(Exception):
            r.recordings_archived = 1  # type: ignore[misc]


# ==================================================================
# ivs_stream_recording_archiver
# ==================================================================


class TestIvsStreamRecordingArchiver:
    def _build_clients(
        self,
        ivs: MagicMock | None = None,
        s3: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _ivs = ivs or _mock()
        _s3 = s3 or _mock()
        _ddb = ddb or _mock()

        def factory(service, region_name=None):
            if service == "ivs":
                return _ivs
            if service == "s3":
                return _s3
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _ivs, _s3, _ddb

    def test_success(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "stream-1"}]
        }
        ivs.get_stream_session.return_value = {
            "streamSession": {"streamId": "stream-1", "recordingConfiguration": {}}
        }
        s3 = _mock()
        channel_id = "ch123"
        s3.list_objects_v2.return_value = {
            "Contents": [
                {"Key": f"{channel_id}/stream-1/video.ts", "Size": 1024},
                {"Key": f"{channel_id}/stream-1/audio.ts", "Size": 512},
            ]
        }
        ddb = _mock()
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn=f"arn:aws:ivs:us-east-1:123:channel/{channel_id}",
            source_bucket="source-bucket",
            archive_bucket="archive-bucket",
            archive_prefix="archived",
            table_name="archive-meta",
            region_name=REGION,
        )
        assert result.recordings_archived == 1
        assert len(result.archive_keys) == 2
        assert s3.copy_object.call_count == 2
        ddb.put_item.assert_called_once()

    def test_no_sessions(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {"streamSessions": []}
        factory, _, _, _ = self._build_clients(ivs=ivs)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 0
        assert result.archive_keys == []

    def test_list_sessions_error(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.side_effect = _client_error("ResourceNotFoundException")
        factory, _, _, _ = self._build_clients(ivs=ivs)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            ivs_stream_recording_archiver(
                channel_arn="arn:ch", source_bucket="s", archive_bucket="d",
                archive_prefix="a", table_name="t", region_name=REGION,
            )

    def test_session_with_no_stream_id(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": ""}, {}]
        }
        factory, _, _, _ = self._build_clients(ivs=ivs)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 0

    def test_get_stream_session_error(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "s1"}]
        }
        ivs.get_stream_session.side_effect = _client_error("InternalServerError")
        s3 = _mock()
        s3.list_objects_v2.return_value = {"Contents": []}
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        # Error is warned but continues
        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 0

    def test_list_objects_error_skipped(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "s1"}]
        }
        ivs.get_stream_session.return_value = {"streamSession": {}}
        s3 = _mock()
        s3.list_objects_v2.side_effect = _client_error("AccessDenied")
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 0

    def test_no_objects_for_session(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "s1"}]
        }
        ivs.get_stream_session.return_value = {"streamSession": {}}
        s3 = _mock()
        s3.list_objects_v2.return_value = {"Contents": []}
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 0

    def test_copy_object_error_skipped(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "s1"}]
        }
        ivs.get_stream_session.return_value = {"streamSession": {}}
        s3 = _mock()
        s3.list_objects_v2.return_value = {
            "Contents": [{"Key": "ch1/s1/video.ts", "Size": 100}]
        }
        s3.copy_object.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        # All copies failed so no sessions archived
        assert result.recordings_archived == 0

    def test_ddb_metadata_error_swallowed(self, monkeypatch) -> None:
        ivs = _mock()
        ivs.list_stream_sessions.return_value = {
            "streamSessions": [{"streamId": "s1"}]
        }
        ivs.get_stream_session.return_value = {"streamSession": {}}
        s3 = _mock()
        s3.list_objects_v2.return_value = {
            "Contents": [{"Key": "ch1/s1/video.ts", "Size": 100}]
        }
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _, _ = self._build_clients(ivs=ivs, s3=s3, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        # DDB error is warned but does not fail
        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:123:channel/ch1",
            source_bucket="src", archive_bucket="dst",
            archive_prefix="arch", table_name="tbl",
            region_name=REGION,
        )
        assert result.recordings_archived == 1


# ==================================================================
# mediaconvert_job_orchestrator
# ==================================================================


class TestMediaconvertJobOrchestrator:
    def _build_clients(
        self,
        mc_base: MagicMock | None = None,
        mc: MagicMock | None = None,
        ddb: MagicMock | None = None,
        sns: MagicMock | None = None,
    ) -> Any:
        _mc_base = mc_base or _mock()
        _mc = mc or _mock()
        _ddb = ddb or _mock()
        _sns = sns or _mock()

        # Default: endpoint discovered OK
        if not mc_base:
            _mc_base.describe_endpoints.return_value = {
                "Endpoints": [{"Url": "https://mc.example.com"}]
            }

        def factory(service, region_name=None):
            if service == "mediaconvert":
                return _mc_base
            if service == "dynamodb":
                return _ddb
            if service == "sns":
                return _sns
            return _mock()
        return factory, _mc_base, _mc, _ddb, _sns

    def test_success(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "job-123"}}
        mc.describe_job.return_value = {"Job": {"Id": "job-123", "Status": "COMPLETE"}}
        ddb = _mock()
        sns = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/video.mp4",
                output_s3_uri="s3://out/",
                role_arn="arn:aws:iam::123:role/mc",
                table_name="mc-table",
                sns_topic_arn="arn:aws:sns:us-east-1:123:mc-topic",
                region_name=REGION,
            )
        assert result.job_id == "job-123"
        assert result.status == "COMPLETE"
        ddb.put_item.assert_called_once()
        sns.publish.assert_called_once()

    def test_endpoint_discovery_error(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )

    def test_no_endpoint_found(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {"Endpoints": []}
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )

    def test_create_job_error(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base)
        monkeypatch.setattr(mod, "get_client", factory)
        with patch("boto3.client", return_value=mc):
            with pytest.raises(RuntimeError):
                mediaconvert_job_orchestrator(
                    input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                    role_arn="arn:role", table_name="t",
                    region_name=REGION,
                )

    def test_job_status_error(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "ERROR"}}
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )
        assert result.status == "ERROR"

    def test_job_status_canceled(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "CANCELED"}}
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )
        assert result.status == "CANCELED"

    def test_describe_job_error(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            with pytest.raises(RuntimeError):
                mediaconvert_job_orchestrator(
                    input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                    role_arn="arn:role", table_name="t",
                    region_name=REGION,
                )

    def test_polling_timeout(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "PROGRESSING"}}
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        # Force the loop to exhaust all iterations
        monkeypatch.setattr(mod, "_MEDIACONVERT_MAX_ITERATIONS", 2)
        with patch("boto3.client", return_value=mc):
            with pytest.raises(RuntimeError):
                mediaconvert_job_orchestrator(
                    input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                    role_arn="arn:role", table_name="t",
                    region_name=REGION,
                )

    def test_ddb_write_error_swallowed(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "COMPLETE"}}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            # DDB error should not raise
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )
        assert result.status == "COMPLETE"

    def test_sns_notification_error_swallowed(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "COMPLETE"}}
        ddb = _mock()
        sns = _mock()
        sns.publish.side_effect = _client_error("InternalServerError")
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb, sns=sns)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
                region_name=REGION,
            )
        assert result.status == "COMPLETE"

    def test_no_sns_topic(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "COMPLETE"}}
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )
        assert result.status == "COMPLETE"

    def test_custom_settings(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.return_value = {"Job": {"Id": "j1", "Status": "COMPLETE"}}
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        custom = {
            "VideoCodecSettings": {"Codec": "H_265"},
            "AudioCodecSettings": {"Codec": "OPUS"},
            "Container": "MKV",
        }
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                settings=custom,
                region_name=REGION,
            )
        assert result.status == "COMPLETE"
        # Verify the job was created (settings are embedded in call)
        mc.create_job.assert_called_once()

    def test_polling_transitions_to_complete(self, monkeypatch) -> None:
        mc_base = _mock()
        mc_base.describe_endpoints.return_value = {
            "Endpoints": [{"Url": "https://mc.example.com"}]
        }
        mc = _mock()
        mc.create_job.return_value = {"Job": {"Id": "j1"}}
        mc.describe_job.side_effect = [
            {"Job": {"Id": "j1", "Status": "PROGRESSING"}},
            {"Job": {"Id": "j1", "Status": "PROGRESSING"}},
            {"Job": {"Id": "j1", "Status": "COMPLETE"}},
        ]
        ddb = _mock()
        factory, _, _, _, _ = self._build_clients(mc_base=mc_base, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        with patch("boto3.client", return_value=mc):
            result = mediaconvert_job_orchestrator(
                input_s3_uri="s3://in/v.mp4", output_s3_uri="s3://out/",
                role_arn="arn:role", table_name="t",
                region_name=REGION,
            )
        assert result.status == "COMPLETE"
        assert mc.describe_job.call_count == 3
