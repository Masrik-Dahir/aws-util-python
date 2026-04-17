"""Integration tests for aws_util.storage_ops against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. efs_to_s3_sync
# ---------------------------------------------------------------------------


class TestEfsToS3Sync:
    @pytest.mark.skip(reason="DataSync not available in LocalStack community")
    def test_creates_datasync_task_and_starts_execution(
        self, s3_bucket, dynamodb_pk_table
    ):
        from aws_util.storage_ops import efs_to_s3_sync

        result = efs_to_s3_sync(
            efs_filesystem_id="fs-12345678",
            source_subnet_arn="arn:aws:ec2:us-east-1:000000000000:subnet/subnet-abc123",
            source_security_group_arns=[
                "arn:aws:ec2:us-east-1:000000000000:security-group/sg-abc123",
            ],
            bucket=s3_bucket,
            key_prefix="efs-sync/",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert isinstance(result.task_arn, str)
        assert isinstance(result.execution_arn, str)
        assert result.status == "LAUNCHED"


# ---------------------------------------------------------------------------
# 2. fsx_backup_to_s3
# ---------------------------------------------------------------------------


class TestFsxBackupToS3:
    @pytest.mark.skip(reason="FSx not available in LocalStack community")
    def test_creates_backup_and_writes_metadata(self, s3_bucket):
        from aws_util.storage_ops import fsx_backup_to_s3

        result = fsx_backup_to_s3(
            file_system_id="fs-12345678",
            backup_name="test-backup",
            bucket=s3_bucket,
            key_prefix="fsx-backups/",
            region_name=REGION,
        )
        assert isinstance(result.backup_id, str)
        assert result.status in ("AVAILABLE", "CREATING", "FAILED")
        assert isinstance(result.s3_metadata_key, str)


# ---------------------------------------------------------------------------
# 3. transfer_family_event_processor
# ---------------------------------------------------------------------------


class TestTransferFamilyEventProcessor:
    @pytest.mark.skip(
        reason="Transfer Family not available in LocalStack community"
    )
    def test_processes_transfer_events_and_moves_files(
        self, s3_bucket, sns_topic
    ):
        from aws_util.storage_ops import transfer_family_event_processor

        result = transfer_family_event_processor(
            server_id="s-1234567890abcdef0",
            bucket=s3_bucket,
            destination_prefix="processed/",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert result.files_processed >= 0
        assert isinstance(result.files_moved, list)
        assert result.notifications_sent >= 0


# ---------------------------------------------------------------------------
# 4. storage_gateway_cache_monitor
# ---------------------------------------------------------------------------


class TestStorageGatewayCacheMonitor:
    @pytest.mark.skip(
        reason="Storage Gateway not available in LocalStack community"
    )
    def test_describes_cache_and_evaluates_threshold(self, sns_topic):
        from aws_util.storage_ops import storage_gateway_cache_monitor

        result = storage_gateway_cache_monitor(
            gateway_arn="arn:aws:storagegateway:us-east-1:000000000000:gateway/sgw-12345678",
            alarm_threshold_percent=80.0,
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.gateway_id, str)
        assert isinstance(result.cache_used_percent, float)
        assert isinstance(result.cache_allocated_bytes, int)
        assert isinstance(result.alarm_created, bool)


# ---------------------------------------------------------------------------
# 5. lightsail_snapshot_to_s3
# ---------------------------------------------------------------------------


class TestLightsailSnapshotToS3:
    @pytest.mark.skip(reason="Lightsail not available in LocalStack community")
    def test_creates_snapshot_exports_and_writes_metadata(self, s3_bucket):
        from aws_util.storage_ops import lightsail_snapshot_to_s3

        result = lightsail_snapshot_to_s3(
            instance_name="test-instance",
            snapshot_name="test-lightsail-snap",
            bucket=s3_bucket,
            key_prefix="lightsail-exports/",
            region_name=REGION,
        )
        assert result.snapshot_name == "test-lightsail-snap"
        assert result.export_arn is None or isinstance(result.export_arn, str)
        assert isinstance(result.s3_metadata_key, str)
