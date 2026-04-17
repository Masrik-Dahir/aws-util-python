"""Integration tests for aws_util.media_processing against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. ivs_stream_recording_archiver
# ---------------------------------------------------------------------------


class TestIvsStreamRecordingArchiver:
    @pytest.mark.skip(reason="IVS not available in LocalStack community")
    def test_archives_stream_recordings_to_s3(
        self, s3_bucket, dynamodb_pk_table
    ):
        from aws_util.media_processing import ivs_stream_recording_archiver

        # Create an archive bucket
        archive_bucket_name = f"{s3_bucket}-archive"
        s3 = ls_client("s3")
        try:
            s3.create_bucket(Bucket=archive_bucket_name)
        except Exception:
            pass  # bucket may already exist

        result = ivs_stream_recording_archiver(
            channel_arn="arn:aws:ivs:us-east-1:000000000000:channel/test-channel",
            source_bucket=s3_bucket,
            archive_bucket=archive_bucket_name,
            archive_prefix="archived-streams",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert result.recordings_archived >= 0
        assert isinstance(result.archive_keys, list)

        # Cleanup archive bucket
        try:
            s3.delete_bucket(Bucket=archive_bucket_name)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# 2. mediaconvert_job_orchestrator
# ---------------------------------------------------------------------------


class TestMediaconvertJobOrchestrator:
    @pytest.mark.skip(reason="MediaConvert not available in LocalStack community")
    def test_submits_job_and_polls_for_completion(
        self, s3_bucket, dynamodb_pk_table, sns_topic, iam_role
    ):
        from aws_util.media_processing import mediaconvert_job_orchestrator

        # Upload a dummy media file
        s3 = ls_client("s3")
        s3.put_object(
            Bucket=s3_bucket,
            Key="input/test-video.mp4",
            Body=b"\x00" * 2048,
        )

        result = mediaconvert_job_orchestrator(
            input_s3_uri=f"s3://{s3_bucket}/input/test-video.mp4",
            output_s3_uri=f"s3://{s3_bucket}/output/",
            role_arn=iam_role,
            table_name=dynamodb_pk_table,
            sns_topic_arn=sns_topic,
            settings=None,
            region_name=REGION,
        )
        assert isinstance(result.job_id, str)
        assert result.status in ("COMPLETE", "ERROR", "CANCELED", "SUBMITTED")
        assert isinstance(result.output_uri, str)
        assert isinstance(result.duration_seconds, float)
