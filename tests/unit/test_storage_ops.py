"""Tests for aws_util.storage_ops module."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.storage_ops as mod
from aws_util.storage_ops import (
    CacheMonitorResult,
    EfsS3SyncResult,
    FsxBackupResult,
    LightsailExportResult,
    TransferEventResult,
    efs_to_s3_sync,
    fsx_backup_to_s3,
    lightsail_snapshot_to_s3,
    storage_gateway_cache_monitor,
    transfer_family_event_processor,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str = "AccessDenied", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestEfsS3SyncResult:
    def test_create(self) -> None:
        r = EfsS3SyncResult(task_arn="arn:task", execution_arn="arn:exec", status="LAUNCHED")
        assert r.status == "LAUNCHED"

    def test_frozen(self) -> None:
        r = EfsS3SyncResult(task_arn="a", execution_arn="e", status="s")
        with pytest.raises(Exception):
            r.status = "x"  # type: ignore[misc]


class TestFsxBackupResult:
    def test_create(self) -> None:
        r = FsxBackupResult(backup_id="b-1", status="AVAILABLE", s3_metadata_key="k")
        assert r.backup_id == "b-1"


class TestTransferEventResult:
    def test_create(self) -> None:
        r = TransferEventResult(files_processed=3, files_moved=["a", "b", "c"], notifications_sent=3)
        assert r.files_processed == 3


class TestCacheMonitorResult:
    def test_create(self) -> None:
        r = CacheMonitorResult(
            gateway_id="gw-1", cache_used_percent=55.0,
            cache_allocated_bytes=1000000, alarm_created=False,
        )
        assert r.cache_used_percent == 55.0


class TestLightsailExportResult:
    def test_create(self) -> None:
        r = LightsailExportResult(snapshot_name="snap", export_arn="arn:exp", s3_metadata_key="k")
        assert r.export_arn == "arn:exp"


# ---------------------------------------------------------------------------
# efs_to_s3_sync
# ---------------------------------------------------------------------------


class TestEfsToS3Sync:
    def _factory(self, datasync: MagicMock, ddb: MagicMock):
        def get_client(service: str, region=None):
            return {"datasync": datasync, "dynamodb": ddb}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs-loc"}
        ds.create_location_s3.return_value = {"LocationArn": "arn:s3-loc"}
        ds.create_task.return_value = {"TaskArn": "arn:task-1"}
        ds.start_task_execution.return_value = {"TaskExecutionArn": "arn:exec-1"}
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        result = efs_to_s3_sync(
            efs_filesystem_id="fs-123",
            source_subnet_arn="arn:subnet",
            source_security_group_arns=["arn:sg"],
            bucket="my-bucket",
            key_prefix="prefix/",
            table_name="sync-table",
            region_name=REGION,
        )
        assert isinstance(result, EfsS3SyncResult)
        assert result.task_arn == "arn:task-1"
        assert result.execution_arn == "arn:exec-1"
        assert result.status == "LAUNCHED"
        ddb.put_item.assert_called_once()

    def test_create_location_efs_error(self, monkeypatch) -> None:
        ds = _mock()
        ds.create_location_efs.side_effect = _client_error("InvalidRequestException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        with pytest.raises(RuntimeError, match="Failed to create DataSync EFS"):
            efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")

    def test_create_location_s3_error(self, monkeypatch) -> None:
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs"}
        ds.create_location_s3.side_effect = _client_error("InvalidRequestException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        with pytest.raises(RuntimeError, match="Failed to create DataSync S3"):
            efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")

    def test_create_task_error(self, monkeypatch) -> None:
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs"}
        ds.create_location_s3.return_value = {"LocationArn": "arn:s3"}
        ds.create_task.side_effect = _client_error("InternalException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        with pytest.raises(RuntimeError, match="Failed to create DataSync task"):
            efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")

    def test_start_execution_error(self, monkeypatch) -> None:
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs"}
        ds.create_location_s3.return_value = {"LocationArn": "arn:s3"}
        ds.create_task.return_value = {"TaskArn": "arn:task"}
        ds.start_task_execution.side_effect = _client_error("InvalidRequestException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        with pytest.raises(RuntimeError, match="Failed to start DataSync task"):
            efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")

    def test_dynamodb_put_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs"}
        ds.create_location_s3.return_value = {"LocationArn": "arn:s3"}
        ds.create_task.return_value = {"TaskArn": "arn:task"}
        ds.start_task_execution.return_value = {"TaskExecutionArn": "arn:exec"}
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        with pytest.raises(RuntimeError, match="Failed to record sync metadata"):
            efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")

    def test_default_region(self, monkeypatch) -> None:
        """When region_name is None, default to us-east-1 in EFS ARN."""
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ds = _mock()
        ds.create_location_efs.return_value = {"LocationArn": "arn:efs"}
        ds.create_location_s3.return_value = {"LocationArn": "arn:s3"}
        ds.create_task.return_value = {"TaskArn": "arn:task"}
        ds.start_task_execution.return_value = {"TaskExecutionArn": "arn:exec"}
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ds, ddb))

        result = efs_to_s3_sync("fs-1", "arn:sub", ["arn:sg"], "bkt", "pfx", "tbl")
        call_kwargs = ds.create_location_efs.call_args
        efs_arn = call_kwargs.kwargs.get("EfsFilesystemArn") or call_kwargs[1].get("EfsFilesystemArn")
        assert "us-east-1" in efs_arn


# ---------------------------------------------------------------------------
# fsx_backup_to_s3
# ---------------------------------------------------------------------------


class TestFsxBackupToS3:
    def _factory(self, fsx: MagicMock, s3: MagicMock):
        def get_client(service: str, region=None):
            return {"fsx": fsx, "s3": s3}.get(service, MagicMock())

        return get_client

    def test_success_available(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        fsx = _mock()
        fsx.create_backup.return_value = {
            "Backup": {"BackupId": "bkp-1", "Lifecycle": "CREATING"}
        }
        fsx.describe_backups.return_value = {
            "Backups": [{"Lifecycle": "AVAILABLE"}]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        result = fsx_backup_to_s3(
            file_system_id="fs-abc",
            backup_name="daily-backup",
            bucket="bkt",
            key_prefix="backups",
            region_name=REGION,
        )
        assert isinstance(result, FsxBackupResult)
        assert result.backup_id == "bkp-1"
        assert result.status == "AVAILABLE"
        assert result.s3_metadata_key == "backups/bkp-1.json"
        s3.put_object.assert_called_once()

    def test_backup_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        fsx = _mock()
        fsx.create_backup.return_value = {
            "Backup": {"BackupId": "bkp-2", "Lifecycle": "CREATING"}
        }
        fsx.describe_backups.return_value = {
            "Backups": [{"Lifecycle": "FAILED"}]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        result = fsx_backup_to_s3("fs-abc", "bkp", "bkt", "pfx")
        assert result.status == "FAILED"

    def test_create_backup_error(self, monkeypatch) -> None:
        fsx = _mock()
        fsx.create_backup.side_effect = _client_error("FileSystemNotFound")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        with pytest.raises(RuntimeError, match="Failed to create FSx backup"):
            fsx_backup_to_s3("fs-bad", "bkp", "bkt", "pfx")

    def test_describe_backups_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        fsx = _mock()
        fsx.create_backup.return_value = {
            "Backup": {"BackupId": "bkp-3", "Lifecycle": "CREATING"}
        }
        fsx.describe_backups.side_effect = _client_error("BackupNotFound")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        with pytest.raises(RuntimeError, match="Failed to describe FSx backup"):
            fsx_backup_to_s3("fs-abc", "bkp", "bkt", "pfx")

    def test_s3_put_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        fsx = _mock()
        fsx.create_backup.return_value = {
            "Backup": {"BackupId": "bkp-4", "Lifecycle": "AVAILABLE"}
        }
        s3 = _mock()
        s3.put_object.side_effect = _client_error("NoSuchBucket")
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        with pytest.raises(RuntimeError, match="Failed to write FSx backup metadata"):
            fsx_backup_to_s3("fs-abc", "bkp", "bad-bkt", "pfx")

    def test_key_prefix_trailing_slash_stripped(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        fsx = _mock()
        fsx.create_backup.return_value = {
            "Backup": {"BackupId": "bkp-5", "Lifecycle": "AVAILABLE"}
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(fsx, s3))

        result = fsx_backup_to_s3("fs-abc", "bkp", "bkt", "pfx/")
        assert result.s3_metadata_key == "pfx/bkp-5.json"


# ---------------------------------------------------------------------------
# transfer_family_event_processor
# ---------------------------------------------------------------------------


class TestTransferFamilyEventProcessor:
    def _factory(self, transfer: MagicMock, s3: MagicMock, sns: MagicMock | None = None):
        def get_client(service: str, region=None):
            clients: dict[str, Any] = {"transfer": transfer, "s3": s3}
            if sns is not None:
                clients["sns"] = sns
            return clients.get(service, MagicMock())

        return get_client

    def test_success_with_sns(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {
                    "Status": "COMPLETED",
                    "InitialFile": {"Path": "uploads/file.csv"},
                }
            ]
        }
        s3 = _mock()
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3, sns))

        result = transfer_family_event_processor(
            server_id="s-123",
            bucket="bkt",
            destination_prefix="processed",
            sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
            region_name=REGION,
        )
        assert isinstance(result, TransferEventResult)
        assert result.files_processed == 1
        assert len(result.files_moved) == 1
        assert result.notifications_sent == 1
        s3.head_object.assert_called_once()
        s3.copy_object.assert_called_once()
        s3.delete_object.assert_called_once()
        sns.publish.assert_called_once()

    def test_success_without_sns(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {
                    "Status": "COMPLETED",
                    "InitialFile": {"Path": "uploads/data.json"},
                }
            ]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        result = transfer_family_event_processor(
            server_id="s-123",
            bucket="bkt",
            destination_prefix="out",
        )
        assert result.files_processed == 1
        assert result.notifications_sent == 0

    def test_list_executions_fallback(self, monkeypatch) -> None:
        """list_executions failure should fall back to empty list."""
        transfer = _mock()
        transfer.list_executions.side_effect = _client_error("ResourceNotFoundException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        result = transfer_family_event_processor("s-1", "bkt", "out")
        assert result.files_processed == 0
        assert result.files_moved == []

    def test_file_not_found_skipped(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": "missing.txt"}},
            ]
        }
        s3 = _mock()
        s3.head_object.side_effect = _client_error("404")
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        result = transfer_family_event_processor("s-1", "bkt", "out")
        assert result.files_processed == 0
        s3.copy_object.assert_not_called()

    def test_head_object_other_error(self, monkeypatch) -> None:
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": "f.txt"}},
            ]
        }
        s3 = _mock()
        s3.head_object.side_effect = _client_error("InternalError")
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        with pytest.raises(RuntimeError, match="Failed to check existence"):
            transfer_family_event_processor("s-1", "bkt", "out")

    def test_copy_object_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": "f.txt"}},
            ]
        }
        s3 = _mock()
        s3.head_object.return_value = {}
        s3.copy_object.side_effect = _client_error("InternalError")
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        with pytest.raises(RuntimeError, match="Failed to copy"):
            transfer_family_event_processor("s-1", "bkt", "out")

    def test_delete_object_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": "f.txt"}},
            ]
        }
        s3 = _mock()
        s3.head_object.return_value = {}
        s3.copy_object.return_value = {}
        s3.delete_object.side_effect = _client_error("InternalError")
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        with pytest.raises(RuntimeError, match="Failed to delete original"):
            transfer_family_event_processor("s-1", "bkt", "out")

    def test_sns_publish_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "20250101T000000Z",
            gmtime=lambda: None,
        ))
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": "f.txt"}},
            ]
        }
        s3 = _mock()
        s3.head_object.return_value = {}
        s3.copy_object.return_value = {}
        s3.delete_object.return_value = {}
        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3, sns))

        with pytest.raises(RuntimeError, match="Failed to publish SNS"):
            transfer_family_event_processor("s-1", "bkt", "out", sns_topic_arn="arn:topic")

    def test_non_completed_executions_skipped(self, monkeypatch) -> None:
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "RUNNING", "InitialFile": {"Path": "a.txt"}},
                {"Status": "FAILED", "InitialFile": {"Path": "b.txt"}},
            ]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        result = transfer_family_event_processor("s-1", "bkt", "out")
        assert result.files_processed == 0
        s3.head_object.assert_not_called()

    def test_empty_path_skipped(self, monkeypatch) -> None:
        transfer = _mock()
        transfer.list_executions.return_value = {
            "Executions": [
                {"Status": "COMPLETED", "InitialFile": {"Path": ""}},
                {"Status": "COMPLETED", "InitialFile": {}},
            ]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(transfer, s3))

        result = transfer_family_event_processor("s-1", "bkt", "out")
        assert result.files_processed == 0


# ---------------------------------------------------------------------------
# storage_gateway_cache_monitor
# ---------------------------------------------------------------------------


class TestStorageGatewayCacheMonitor:
    def _factory(self, sgw: MagicMock, cw: MagicMock):
        def get_client(service: str, region=None):
            return {"storagegateway": sgw, "cloudwatch": cw}.get(service, MagicMock())

        return get_client

    def test_below_threshold_no_alarm(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.return_value = {
            "GatewayARN": "arn:aws:storagegateway:us-east-1:123:gateway/gw-abc",
            "CacheAllocatedInBytes": 1073741824,
            "CacheUsedPercentage": 50.0,
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        result = storage_gateway_cache_monitor(
            gateway_arn="arn:aws:storagegateway:us-east-1:123:gateway/gw-abc",
            alarm_threshold_percent=80.0,
            region_name=REGION,
        )
        assert isinstance(result, CacheMonitorResult)
        assert result.gateway_id == "gw-abc"
        assert result.cache_used_percent == 50.0
        assert result.cache_allocated_bytes == 1073741824
        assert result.alarm_created is False
        cw.put_metric_alarm.assert_not_called()

    def test_above_threshold_alarm_created(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.return_value = {
            "GatewayARN": "arn:aws:storagegateway:us-east-1:123:gateway/gw-xyz",
            "CacheAllocatedInBytes": 500000,
            "CacheUsedPercentage": 92.5,
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        result = storage_gateway_cache_monitor(
            gateway_arn="arn:aws:storagegateway:us-east-1:123:gateway/gw-xyz",
            alarm_threshold_percent=80.0,
            sns_topic_arn="arn:sns:topic",
        )
        assert result.alarm_created is True
        assert result.cache_used_percent == 92.5
        cw.put_metric_alarm.assert_called_once()
        call_kwargs = cw.put_metric_alarm.call_args
        assert call_kwargs.kwargs.get("AlarmActions") or call_kwargs[1].get("AlarmActions") == ["arn:sns:topic"]

    def test_exactly_at_threshold(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.return_value = {
            "GatewayARN": "arn:gw/gw-eq",
            "CacheAllocatedInBytes": 100,
            "CacheUsedPercentage": 80.0,
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        result = storage_gateway_cache_monitor("arn:gw/gw-eq", alarm_threshold_percent=80.0)
        assert result.alarm_created is True

    def test_describe_cache_error(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.side_effect = _client_error("InvalidGatewayRequestException")
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        with pytest.raises(RuntimeError, match="Failed to describe cache"):
            storage_gateway_cache_monitor("arn:gw/gw-bad")

    def test_put_metric_alarm_error(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.return_value = {
            "GatewayARN": "arn:gw/gw-err",
            "CacheAllocatedInBytes": 100,
            "CacheUsedPercentage": 99.0,
        }
        cw = _mock()
        cw.put_metric_alarm.side_effect = _client_error("LimitExceededException")
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        with pytest.raises(RuntimeError, match="Failed to create CloudWatch alarm"):
            storage_gateway_cache_monitor("arn:gw/gw-err")

    def test_no_sns_topic_empty_actions(self, monkeypatch) -> None:
        sgw = _mock()
        sgw.describe_cache.return_value = {
            "GatewayARN": "arn:gw/gw-ns",
            "CacheAllocatedInBytes": 100,
            "CacheUsedPercentage": 90.0,
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(sgw, cw))

        result = storage_gateway_cache_monitor("arn:gw/gw-ns", sns_topic_arn=None)
        assert result.alarm_created is True
        call_kwargs = cw.put_metric_alarm.call_args
        alarm_actions = call_kwargs.kwargs.get("AlarmActions") or call_kwargs[1].get("AlarmActions")
        assert alarm_actions == []


# ---------------------------------------------------------------------------
# lightsail_snapshot_to_s3
# ---------------------------------------------------------------------------


class TestLightsailSnapshotToS3:
    def _factory(self, ls: MagicMock, s3: MagicMock):
        def get_client(service: str, region=None):
            return {"lightsail": ls, "s3": s3}.get(service, MagicMock())

        return get_client

    def test_success_available_export(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "available"}
        }
        ls.export_snapshot.return_value = {
            "operations": [{"resourceArn": "arn:export-1"}]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        result = lightsail_snapshot_to_s3(
            instance_name="web-1",
            snapshot_name="snap-daily",
            bucket="bkt",
            key_prefix="exports",
            region_name=REGION,
        )
        assert isinstance(result, LightsailExportResult)
        assert result.snapshot_name == "snap-daily"
        assert result.export_arn == "arn:export-1"
        assert result.s3_metadata_key == "exports/snap-daily.json"
        s3.put_object.assert_called_once()

    def test_snapshot_not_available_skips_export(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        # Never return "available"
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "pending"}
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        result = lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")
        assert result.export_arn is None
        ls.export_snapshot.assert_not_called()

    def test_create_snapshot_error(self, monkeypatch) -> None:
        ls = _mock()
        ls.create_instance_snapshot.side_effect = _client_error("NotFoundException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        with pytest.raises(RuntimeError, match="Failed to create Lightsail snapshot"):
            lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")

    def test_get_snapshot_poll_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        ls = _mock()
        ls.get_instance_snapshot.side_effect = _client_error("NotFoundException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        with pytest.raises(RuntimeError, match="Failed to get Lightsail snapshot"):
            lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")

    def test_export_snapshot_error_logged(self, monkeypatch) -> None:
        """export_snapshot failure is logged as warning, not raised."""
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "available"}
        }
        ls.export_snapshot.side_effect = _client_error("InvalidInputException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        result = lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")
        assert result.export_arn is None  # export failed gracefully
        s3.put_object.assert_called_once()  # metadata still written

    def test_s3_put_metadata_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "available"}
        }
        ls.export_snapshot.return_value = {"operations": [{"resourceArn": "arn:x"}]}
        s3 = _mock()
        s3.put_object.side_effect = _client_error("NoSuchBucket")
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        with pytest.raises(RuntimeError, match="Failed to write Lightsail export metadata"):
            lightsail_snapshot_to_s3("inst", "snap", "bad-bkt", "pfx")

    def test_export_with_id_fallback(self, monkeypatch) -> None:
        """When resourceArn is missing, fall back to 'id'."""
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "available"}
        }
        ls.export_snapshot.return_value = {
            "operations": [{"id": "op-123"}]
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        result = lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")
        assert result.export_arn == "op-123"

    def test_export_empty_operations(self, monkeypatch) -> None:
        """Empty operations list should set export_arn to None."""
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            strftime=lambda *a, **kw: "2025-01-01T00:00:00Z",
            gmtime=lambda: None,
        ))
        ls = _mock()
        ls.get_instance_snapshot.return_value = {
            "instanceSnapshot": {"state": "available"}
        }
        ls.export_snapshot.return_value = {"operations": []}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ls, s3))

        result = lightsail_snapshot_to_s3("inst", "snap", "bkt", "pfx")
        assert result.export_arn is None
