"""Tests for aws_util.storage_gateway module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.storage_gateway as mod
from aws_util.storage_gateway import (
    FileShareResult, GatewayResult, SnapshotResult, VolumeResult,
    _parse_file_share, _parse_gateway, _parse_snapshot, _parse_volume,
    activate_gateway, create_nfs_file_share, create_snapshot,
    delete_file_share, delete_gateway, describe_gateway_information,
    describe_nfs_file_shares, describe_snapshots,
    describe_stored_iscsi_volumes, list_file_shares, list_gateways,
    list_volumes, shutdown_gateway, update_nfs_file_share,
    add_cache,
    add_tags_to_resource,
    add_upload_buffer,
    add_working_storage,
    assign_tape_pool,
    associate_file_system,
    attach_volume,
    cancel_archival,
    cancel_cache_report,
    cancel_retrieval,
    create_cached_iscsi_volume,
    create_smb_file_share,
    create_snapshot_from_volume_recovery_point,
    create_stored_iscsi_volume,
    create_tape_pool,
    create_tape_with_barcode,
    create_tapes,
    delete_automatic_tape_creation_policy,
    delete_bandwidth_rate_limit,
    delete_cache_report,
    delete_chap_credentials,
    delete_snapshot_schedule,
    delete_tape,
    delete_tape_archive,
    delete_tape_pool,
    delete_volume,
    describe_availability_monitor_test,
    describe_bandwidth_rate_limit,
    describe_bandwidth_rate_limit_schedule,
    describe_cache,
    describe_cache_report,
    describe_cached_iscsi_volumes,
    describe_chap_credentials,
    describe_file_system_associations,
    describe_maintenance_start_time,
    describe_smb_file_shares,
    describe_smb_settings,
    describe_snapshot_schedule,
    describe_tape_archives,
    describe_tape_recovery_points,
    describe_tapes,
    describe_upload_buffer,
    describe_vtl_devices,
    describe_working_storage,
    detach_volume,
    disable_gateway,
    disassociate_file_system,
    evict_files_failing_upload,
    join_domain,
    list_automatic_tape_creation_policies,
    list_cache_reports,
    list_file_system_associations,
    list_local_disks,
    list_tags_for_resource,
    list_tape_pools,
    list_tapes,
    list_volume_initiators,
    list_volume_recovery_points,
    notify_when_uploaded,
    refresh_cache,
    remove_tags_from_resource,
    reset_cache,
    retrieve_tape_archive,
    retrieve_tape_recovery_point,
    set_local_console_password,
    set_smb_guest_password,
    start_availability_monitor_test,
    start_cache_report,
    start_gateway,
    update_automatic_tape_creation_policy,
    update_bandwidth_rate_limit,
    update_bandwidth_rate_limit_schedule,
    update_chap_credentials,
    update_file_system_association,
    update_gateway_information,
    update_gateway_software_now,
    update_maintenance_start_time,
    update_smb_file_share,
    update_smb_file_share_visibility,
    update_smb_local_groups,
    update_smb_security_strategy,
    update_snapshot_schedule,
    update_vtl_device_type,
)

REGION = "us-east-1"
_GW = {"GatewayARN": "arn:gw", "GatewayId": "gw-1", "GatewayName": "gw",
       "GatewayType": "FILE_S3", "GatewayState": "RUNNING",
       "GatewayTimezone": "GMT-5:00", "extraG": "x"}
_FS = {"FileShareARN": "arn:fs", "FileShareId": "fs-1", "FileShareStatus": "AVAILABLE",
       "GatewayARN": "arn:gw", "LocationARN": "arn:s3", "Role": "arn:role",
       "Path": "/share", "extraF": "y"}
_VOL = {"VolumeARN": "arn:vol", "VolumeId": "vol-1", "VolumeType": "STORED",
        "VolumeStatus": "AVAILABLE", "VolumeSizeInBytes": 1073741824, "extraV": "z"}
_SNAP_DATA = {"SnapshotId": "snap-1", "VolumeARN": "arn:vol",
              "SnapshotDescription": "desc", "extraS": "s"}


def _ce(code="ServiceException", msg="fail"):
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# Models
def test_gateway_result():
    r = GatewayResult(gateway_arn="arn:gw")
    assert r.gateway_arn == "arn:gw"

def test_file_share_result():
    r = FileShareResult(file_share_arn="arn:fs")
    assert r.file_share_arn == "arn:fs"

def test_volume_result():
    r = VolumeResult(volume_arn="arn:vol")
    assert r.volume_arn == "arn:vol"

def test_snapshot_result():
    r = SnapshotResult(snapshot_id="snap-1")
    assert r.snapshot_id == "snap-1"


# Parsers
def test_parse_gateway():
    r = _parse_gateway(_GW)
    assert r.gateway_arn == "arn:gw"
    assert "extraG" in r.extra

def test_parse_file_share():
    r = _parse_file_share(_FS)
    assert r.file_share_arn == "arn:fs"
    assert "extraF" in r.extra

def test_parse_volume():
    r = _parse_volume(_VOL)
    assert r.volume_arn == "arn:vol"
    assert "extraV" in r.extra

def test_parse_snapshot():
    r = _parse_snapshot(_SNAP_DATA)
    assert r.snapshot_id == "snap-1"
    assert "extraS" in r.extra


# activate_gateway
def test_activate_gateway_success(monkeypatch):
    client = MagicMock()
    client.activate_gateway.return_value = {"GatewayARN": "arn:gw"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = activate_gateway(activation_key="key", gateway_name="gw",
                         gateway_timezone="GMT", gateway_region="us-east-1", region_name=REGION)
    assert r == "arn:gw"

def test_activate_gateway_error(monkeypatch):
    client = MagicMock()
    client.activate_gateway.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="activate_gateway failed"):
        activate_gateway(activation_key="k", gateway_name="g",
                         gateway_timezone="GMT", gateway_region="us-east-1", region_name=REGION)


# describe_gateway_information
def test_describe_gateway_info_success(monkeypatch):
    client = MagicMock()
    client.describe_gateway_information.return_value = _GW
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_gateway_information("arn:gw", region_name=REGION)
    assert r.gateway_arn == "arn:gw"

def test_describe_gateway_info_error(monkeypatch):
    client = MagicMock()
    client.describe_gateway_information.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_gateway_information failed"):
        describe_gateway_information("arn:gw", region_name=REGION)


# list_gateways
def test_list_gateways_success(monkeypatch):
    client = MagicMock()
    client.list_gateways.return_value = {"Gateways": [_GW]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_gateways(region_name=REGION)
    assert len(r) == 1

def test_list_gateways_pagination(monkeypatch):
    client = MagicMock()
    client.list_gateways.side_effect = [
        {"Gateways": [_GW], "Marker": "m1"},
        {"Gateways": [_GW]},
    ]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_gateways(region_name=REGION)
    assert len(r) == 2

def test_list_gateways_error(monkeypatch):
    client = MagicMock()
    client.list_gateways.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_gateways failed"):
        list_gateways(region_name=REGION)


# delete_gateway
def test_delete_gateway_success(monkeypatch):
    client = MagicMock()
    client.delete_gateway.return_value = {"GatewayARN": "arn:gw"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = delete_gateway("arn:gw", region_name=REGION)
    assert r == "arn:gw"

def test_delete_gateway_error(monkeypatch):
    client = MagicMock()
    client.delete_gateway.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_gateway failed"):
        delete_gateway("arn:gw", region_name=REGION)


# shutdown_gateway
def test_shutdown_gateway_success(monkeypatch):
    client = MagicMock()
    client.shutdown_gateway.return_value = {"GatewayARN": "arn:gw"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = shutdown_gateway("arn:gw", region_name=REGION)
    assert r == "arn:gw"

def test_shutdown_gateway_error(monkeypatch):
    client = MagicMock()
    client.shutdown_gateway.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="shutdown_gateway failed"):
        shutdown_gateway("arn:gw", region_name=REGION)


# create_nfs_file_share
def test_create_nfs_file_share_success(monkeypatch):
    client = MagicMock()
    client.create_nfs_file_share.return_value = _FS
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_nfs_file_share(client_token="t", gateway_arn="arn:gw",
                              role="arn:role", location_arn="arn:s3", region_name=REGION)
    assert r.file_share_arn == "arn:fs"

def test_create_nfs_file_share_error(monkeypatch):
    client = MagicMock()
    client.create_nfs_file_share.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_nfs_file_share failed"):
        create_nfs_file_share(client_token="t", gateway_arn="arn:gw",
                              role="arn:role", location_arn="arn:s3", region_name=REGION)


# describe_nfs_file_shares
def test_describe_nfs_file_shares_success(monkeypatch):
    client = MagicMock()
    client.describe_nfs_file_shares.return_value = {"NFSFileShareInfoList": [_FS]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_nfs_file_shares(["arn:fs"], region_name=REGION)
    assert len(r) == 1

def test_describe_nfs_file_shares_error(monkeypatch):
    client = MagicMock()
    client.describe_nfs_file_shares.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_nfs_file_shares failed"):
        describe_nfs_file_shares(["arn:fs"], region_name=REGION)


# update_nfs_file_share
def test_update_nfs_file_share_success(monkeypatch):
    client = MagicMock()
    client.update_nfs_file_share.return_value = {"FileShareARN": "arn:fs"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_nfs_file_share("arn:fs", default_storage_class="S3_IA",
                              kms_encrypted=True, region_name=REGION)
    assert r.file_share_arn == "arn:fs"

def test_update_nfs_file_share_error(monkeypatch):
    client = MagicMock()
    client.update_nfs_file_share.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_nfs_file_share failed"):
        update_nfs_file_share("arn:fs", region_name=REGION)


# delete_file_share
def test_delete_file_share_success(monkeypatch):
    client = MagicMock()
    client.delete_file_share.return_value = {"FileShareARN": "arn:fs"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = delete_file_share("arn:fs", force_delete=True, region_name=REGION)
    assert r == "arn:fs"

def test_delete_file_share_error(monkeypatch):
    client = MagicMock()
    client.delete_file_share.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_file_share failed"):
        delete_file_share("arn:fs", region_name=REGION)


# list_file_shares
def test_list_file_shares_success(monkeypatch):
    client = MagicMock()
    client.list_file_shares.return_value = {"FileShareInfoList": [_FS]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_file_shares(gateway_arn="arn:gw", region_name=REGION)
    assert len(r) == 1

def test_list_file_shares_pagination(monkeypatch):
    client = MagicMock()
    client.list_file_shares.side_effect = [
        {"FileShareInfoList": [_FS], "NextMarker": "m1"},
        {"FileShareInfoList": [_FS]},
    ]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_file_shares(region_name=REGION)
    assert len(r) == 2

def test_list_file_shares_error(monkeypatch):
    client = MagicMock()
    client.list_file_shares.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_file_shares failed"):
        list_file_shares(region_name=REGION)


# list_volumes
def test_list_volumes_success(monkeypatch):
    client = MagicMock()
    client.list_volumes.return_value = {"VolumeInfos": [_VOL]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_volumes(gateway_arn="arn:gw", region_name=REGION)
    assert len(r) == 1

def test_list_volumes_pagination(monkeypatch):
    client = MagicMock()
    client.list_volumes.side_effect = [
        {"VolumeInfos": [_VOL], "Marker": "m1"},
        {"VolumeInfos": [_VOL]},
    ]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_volumes(region_name=REGION)
    assert len(r) == 2

def test_list_volumes_error(monkeypatch):
    client = MagicMock()
    client.list_volumes.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_volumes failed"):
        list_volumes(region_name=REGION)


# describe_stored_iscsi_volumes
def test_describe_stored_iscsi_volumes_success(monkeypatch):
    client = MagicMock()
    client.describe_stored_iscsi_volumes.return_value = {"StorediSCSIVolumes": [_VOL]}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_stored_iscsi_volumes(["arn:vol"], region_name=REGION)
    assert len(r) == 1

def test_describe_stored_iscsi_volumes_error(monkeypatch):
    client = MagicMock()
    client.describe_stored_iscsi_volumes.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_stored_iscsi_volumes failed"):
        describe_stored_iscsi_volumes(["arn:vol"], region_name=REGION)


# create_snapshot
def test_create_snapshot_success(monkeypatch):
    client = MagicMock()
    client.create_snapshot.return_value = {"SnapshotId": "snap-1", "VolumeARN": "arn:vol"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_snapshot("arn:vol", snapshot_description="desc", region_name=REGION)
    assert r.snapshot_id == "snap-1"

def test_create_snapshot_error(monkeypatch):
    client = MagicMock()
    client.create_snapshot.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_snapshot failed"):
        create_snapshot("arn:vol", region_name=REGION)


# describe_snapshots
def test_describe_snapshots_success(monkeypatch):
    client = MagicMock()
    client.describe_snapshot_schedule.return_value = {
        "VolumeARN": "arn:vol", "Description": "d", "StartAt": "12:00"
    }
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_snapshots("arn:vol", region_name=REGION)
    assert len(r) == 1
    assert r[0].volume_arn == "arn:vol"
    assert "StartAt" in r[0].extra

def test_describe_snapshots_error(monkeypatch):
    client = MagicMock()
    client.describe_snapshot_schedule.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_snapshots failed"):
        describe_snapshots("arn:vol", region_name=REGION)


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_add_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_cache.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    add_cache("test-gateway_arn", [], region_name=REGION)
    mock_client.add_cache.assert_called_once()


def test_add_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_cache",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add cache"):
        add_cache("test-gateway_arn", [], region_name=REGION)


def test_add_tags_to_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    add_tags_to_resource("test-resource_arn", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


def test_add_tags_to_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_arn", [], region_name=REGION)


def test_add_upload_buffer(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_upload_buffer.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    add_upload_buffer("test-gateway_arn", [], region_name=REGION)
    mock_client.add_upload_buffer.assert_called_once()


def test_add_upload_buffer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_upload_buffer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_upload_buffer",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add upload buffer"):
        add_upload_buffer("test-gateway_arn", [], region_name=REGION)


def test_add_working_storage(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_working_storage.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    add_working_storage("test-gateway_arn", [], region_name=REGION)
    mock_client.add_working_storage.assert_called_once()


def test_add_working_storage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_working_storage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_working_storage",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add working storage"):
        add_working_storage("test-gateway_arn", [], region_name=REGION)


def test_assign_tape_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_tape_pool.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    assign_tape_pool("test-tape_arn", "test-pool_id", region_name=REGION)
    mock_client.assign_tape_pool.assert_called_once()


def test_assign_tape_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.assign_tape_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "assign_tape_pool",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to assign tape pool"):
        assign_tape_pool("test-tape_arn", "test-pool_id", region_name=REGION)


def test_associate_file_system(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_file_system.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", region_name=REGION)
    mock_client.associate_file_system.assert_called_once()


def test_associate_file_system_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_file_system.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_file_system",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate file system"):
        associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", region_name=REGION)


def test_attach_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", region_name=REGION)
    mock_client.attach_volume.assert_called_once()


def test_attach_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_volume",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach volume"):
        attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", region_name=REGION)


def test_cancel_archival(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_archival.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    cancel_archival("test-gateway_arn", "test-tape_arn", region_name=REGION)
    mock_client.cancel_archival.assert_called_once()


def test_cancel_archival_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_archival.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_archival",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel archival"):
        cancel_archival("test-gateway_arn", "test-tape_arn", region_name=REGION)


def test_cancel_cache_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_cache_report.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    cancel_cache_report("test-cache_report_arn", region_name=REGION)
    mock_client.cancel_cache_report.assert_called_once()


def test_cancel_cache_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_cache_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_cache_report",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel cache report"):
        cancel_cache_report("test-cache_report_arn", region_name=REGION)


def test_cancel_retrieval(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_retrieval.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    cancel_retrieval("test-gateway_arn", "test-tape_arn", region_name=REGION)
    mock_client.cancel_retrieval.assert_called_once()


def test_cancel_retrieval_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_retrieval.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_retrieval",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel retrieval"):
        cancel_retrieval("test-gateway_arn", "test-tape_arn", region_name=REGION)


def test_create_cached_iscsi_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cached_iscsi_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", region_name=REGION)
    mock_client.create_cached_iscsi_volume.assert_called_once()


def test_create_cached_iscsi_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cached_iscsi_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cached_iscsi_volume",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cached iscsi volume"):
        create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", region_name=REGION)


def test_create_smb_file_share(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_smb_file_share.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", region_name=REGION)
    mock_client.create_smb_file_share.assert_called_once()


def test_create_smb_file_share_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_smb_file_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_smb_file_share",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create smb file share"):
        create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", region_name=REGION)


def test_create_snapshot_from_volume_recovery_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_from_volume_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", region_name=REGION)
    mock_client.create_snapshot_from_volume_recovery_point.assert_called_once()


def test_create_snapshot_from_volume_recovery_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_from_volume_recovery_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot_from_volume_recovery_point",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot from volume recovery point"):
        create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", region_name=REGION)


def test_create_stored_iscsi_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stored_iscsi_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", True, "test-target_name", "test-network_interface_id", region_name=REGION)
    mock_client.create_stored_iscsi_volume.assert_called_once()


def test_create_stored_iscsi_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_stored_iscsi_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stored_iscsi_volume",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create stored iscsi volume"):
        create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", True, "test-target_name", "test-network_interface_id", region_name=REGION)


def test_create_tape_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tape_pool.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tape_pool("test-pool_name", "test-storage_class", region_name=REGION)
    mock_client.create_tape_pool.assert_called_once()


def test_create_tape_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tape_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tape_pool",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tape pool"):
        create_tape_pool("test-pool_name", "test-storage_class", region_name=REGION)


def test_create_tape_with_barcode(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tape_with_barcode.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", region_name=REGION)
    mock_client.create_tape_with_barcode.assert_called_once()


def test_create_tape_with_barcode_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tape_with_barcode.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tape_with_barcode",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tape with barcode"):
        create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", region_name=REGION)


def test_create_tapes(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tapes("test-gateway_arn", 1, "test-client_token", 1, "test-tape_barcode_prefix", region_name=REGION)
    mock_client.create_tapes.assert_called_once()


def test_create_tapes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tapes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tapes",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tapes"):
        create_tapes("test-gateway_arn", 1, "test-client_token", 1, "test-tape_barcode_prefix", region_name=REGION)


def test_delete_automatic_tape_creation_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automatic_tape_creation_policy.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_automatic_tape_creation_policy("test-gateway_arn", region_name=REGION)
    mock_client.delete_automatic_tape_creation_policy.assert_called_once()


def test_delete_automatic_tape_creation_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automatic_tape_creation_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_automatic_tape_creation_policy",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete automatic tape creation policy"):
        delete_automatic_tape_creation_policy("test-gateway_arn", region_name=REGION)


def test_delete_bandwidth_rate_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bandwidth_rate_limit.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_bandwidth_rate_limit("test-gateway_arn", "test-bandwidth_type", region_name=REGION)
    mock_client.delete_bandwidth_rate_limit.assert_called_once()


def test_delete_bandwidth_rate_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_bandwidth_rate_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_bandwidth_rate_limit",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete bandwidth rate limit"):
        delete_bandwidth_rate_limit("test-gateway_arn", "test-bandwidth_type", region_name=REGION)


def test_delete_cache_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_report.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_cache_report("test-cache_report_arn", region_name=REGION)
    mock_client.delete_cache_report.assert_called_once()


def test_delete_cache_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cache_report",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cache report"):
        delete_cache_report("test-cache_report_arn", region_name=REGION)


def test_delete_chap_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_chap_credentials.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_chap_credentials("test-target_arn", "test-initiator_name", region_name=REGION)
    mock_client.delete_chap_credentials.assert_called_once()


def test_delete_chap_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_chap_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_chap_credentials",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete chap credentials"):
        delete_chap_credentials("test-target_arn", "test-initiator_name", region_name=REGION)


def test_delete_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_snapshot_schedule("test-volume_arn", region_name=REGION)
    mock_client.delete_snapshot_schedule.assert_called_once()


def test_delete_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot schedule"):
        delete_snapshot_schedule("test-volume_arn", region_name=REGION)


def test_delete_tape(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_tape("test-gateway_arn", "test-tape_arn", region_name=REGION)
    mock_client.delete_tape.assert_called_once()


def test_delete_tape_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tape",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tape"):
        delete_tape("test-gateway_arn", "test-tape_arn", region_name=REGION)


def test_delete_tape_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape_archive.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_tape_archive("test-tape_arn", region_name=REGION)
    mock_client.delete_tape_archive.assert_called_once()


def test_delete_tape_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tape_archive",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tape archive"):
        delete_tape_archive("test-tape_arn", region_name=REGION)


def test_delete_tape_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape_pool.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_tape_pool("test-pool_arn", region_name=REGION)
    mock_client.delete_tape_pool.assert_called_once()


def test_delete_tape_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tape_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tape_pool",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tape pool"):
        delete_tape_pool("test-pool_arn", region_name=REGION)


def test_delete_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_volume("test-volume_arn", region_name=REGION)
    mock_client.delete_volume.assert_called_once()


def test_delete_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_volume",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete volume"):
        delete_volume("test-volume_arn", region_name=REGION)


def test_describe_availability_monitor_test(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_availability_monitor_test.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_availability_monitor_test("test-gateway_arn", region_name=REGION)
    mock_client.describe_availability_monitor_test.assert_called_once()


def test_describe_availability_monitor_test_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_availability_monitor_test.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_availability_monitor_test",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe availability monitor test"):
        describe_availability_monitor_test("test-gateway_arn", region_name=REGION)


def test_describe_bandwidth_rate_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bandwidth_rate_limit.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_bandwidth_rate_limit("test-gateway_arn", region_name=REGION)
    mock_client.describe_bandwidth_rate_limit.assert_called_once()


def test_describe_bandwidth_rate_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bandwidth_rate_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bandwidth_rate_limit",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe bandwidth rate limit"):
        describe_bandwidth_rate_limit("test-gateway_arn", region_name=REGION)


def test_describe_bandwidth_rate_limit_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bandwidth_rate_limit_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_bandwidth_rate_limit_schedule("test-gateway_arn", region_name=REGION)
    mock_client.describe_bandwidth_rate_limit_schedule.assert_called_once()


def test_describe_bandwidth_rate_limit_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_bandwidth_rate_limit_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_bandwidth_rate_limit_schedule",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe bandwidth rate limit schedule"):
        describe_bandwidth_rate_limit_schedule("test-gateway_arn", region_name=REGION)


def test_describe_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_cache("test-gateway_arn", region_name=REGION)
    mock_client.describe_cache.assert_called_once()


def test_describe_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache"):
        describe_cache("test-gateway_arn", region_name=REGION)


def test_describe_cache_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_report.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_cache_report("test-cache_report_arn", region_name=REGION)
    mock_client.describe_cache_report.assert_called_once()


def test_describe_cache_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache_report",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache report"):
        describe_cache_report("test-cache_report_arn", region_name=REGION)


def test_describe_cached_iscsi_volumes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cached_iscsi_volumes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_cached_iscsi_volumes([], region_name=REGION)
    mock_client.describe_cached_iscsi_volumes.assert_called_once()


def test_describe_cached_iscsi_volumes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cached_iscsi_volumes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cached_iscsi_volumes",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cached iscsi volumes"):
        describe_cached_iscsi_volumes([], region_name=REGION)


def test_describe_chap_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_chap_credentials.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_chap_credentials("test-target_arn", region_name=REGION)
    mock_client.describe_chap_credentials.assert_called_once()


def test_describe_chap_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_chap_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_chap_credentials",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe chap credentials"):
        describe_chap_credentials("test-target_arn", region_name=REGION)


def test_describe_file_system_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_file_system_associations.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_file_system_associations([], region_name=REGION)
    mock_client.describe_file_system_associations.assert_called_once()


def test_describe_file_system_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_file_system_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_file_system_associations",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe file system associations"):
        describe_file_system_associations([], region_name=REGION)


def test_describe_maintenance_start_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_start_time.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_maintenance_start_time("test-gateway_arn", region_name=REGION)
    mock_client.describe_maintenance_start_time.assert_called_once()


def test_describe_maintenance_start_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_maintenance_start_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_maintenance_start_time",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe maintenance start time"):
        describe_maintenance_start_time("test-gateway_arn", region_name=REGION)


def test_describe_smb_file_shares(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_smb_file_shares.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_smb_file_shares([], region_name=REGION)
    mock_client.describe_smb_file_shares.assert_called_once()


def test_describe_smb_file_shares_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_smb_file_shares.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_smb_file_shares",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe smb file shares"):
        describe_smb_file_shares([], region_name=REGION)


def test_describe_smb_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_smb_settings.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_smb_settings("test-gateway_arn", region_name=REGION)
    mock_client.describe_smb_settings.assert_called_once()


def test_describe_smb_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_smb_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_smb_settings",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe smb settings"):
        describe_smb_settings("test-gateway_arn", region_name=REGION)


def test_describe_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_schedule("test-volume_arn", region_name=REGION)
    mock_client.describe_snapshot_schedule.assert_called_once()


def test_describe_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshot schedule"):
        describe_snapshot_schedule("test-volume_arn", region_name=REGION)


def test_describe_tape_archives(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tape_archives.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tape_archives(region_name=REGION)
    mock_client.describe_tape_archives.assert_called_once()


def test_describe_tape_archives_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tape_archives.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tape_archives",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tape archives"):
        describe_tape_archives(region_name=REGION)


def test_describe_tape_recovery_points(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tape_recovery_points.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tape_recovery_points("test-gateway_arn", region_name=REGION)
    mock_client.describe_tape_recovery_points.assert_called_once()


def test_describe_tape_recovery_points_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tape_recovery_points.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tape_recovery_points",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tape recovery points"):
        describe_tape_recovery_points("test-gateway_arn", region_name=REGION)


def test_describe_tapes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tapes("test-gateway_arn", region_name=REGION)
    mock_client.describe_tapes.assert_called_once()


def test_describe_tapes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tapes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tapes",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tapes"):
        describe_tapes("test-gateway_arn", region_name=REGION)


def test_describe_upload_buffer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_upload_buffer.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_upload_buffer("test-gateway_arn", region_name=REGION)
    mock_client.describe_upload_buffer.assert_called_once()


def test_describe_upload_buffer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_upload_buffer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_upload_buffer",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe upload buffer"):
        describe_upload_buffer("test-gateway_arn", region_name=REGION)


def test_describe_vtl_devices(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vtl_devices.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_vtl_devices("test-gateway_arn", region_name=REGION)
    mock_client.describe_vtl_devices.assert_called_once()


def test_describe_vtl_devices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vtl_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vtl_devices",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vtl devices"):
        describe_vtl_devices("test-gateway_arn", region_name=REGION)


def test_describe_working_storage(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_working_storage.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_working_storage("test-gateway_arn", region_name=REGION)
    mock_client.describe_working_storage.assert_called_once()


def test_describe_working_storage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_working_storage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_working_storage",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe working storage"):
        describe_working_storage("test-gateway_arn", region_name=REGION)


def test_detach_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    detach_volume("test-volume_arn", region_name=REGION)
    mock_client.detach_volume.assert_called_once()


def test_detach_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_volume",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach volume"):
        detach_volume("test-volume_arn", region_name=REGION)


def test_disable_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_gateway.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    disable_gateway("test-gateway_arn", region_name=REGION)
    mock_client.disable_gateway.assert_called_once()


def test_disable_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_gateway",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable gateway"):
        disable_gateway("test-gateway_arn", region_name=REGION)


def test_disassociate_file_system(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_file_system.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    disassociate_file_system("test-file_system_association_arn", region_name=REGION)
    mock_client.disassociate_file_system.assert_called_once()


def test_disassociate_file_system_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_file_system.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_file_system",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate file system"):
        disassociate_file_system("test-file_system_association_arn", region_name=REGION)


def test_evict_files_failing_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.evict_files_failing_upload.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    evict_files_failing_upload("test-file_share_arn", region_name=REGION)
    mock_client.evict_files_failing_upload.assert_called_once()


def test_evict_files_failing_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.evict_files_failing_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "evict_files_failing_upload",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to evict files failing upload"):
        evict_files_failing_upload("test-file_share_arn", region_name=REGION)


def test_join_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.join_domain.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", region_name=REGION)
    mock_client.join_domain.assert_called_once()


def test_join_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.join_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "join_domain",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to join domain"):
        join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", region_name=REGION)


def test_list_automatic_tape_creation_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automatic_tape_creation_policies.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_automatic_tape_creation_policies(region_name=REGION)
    mock_client.list_automatic_tape_creation_policies.assert_called_once()


def test_list_automatic_tape_creation_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automatic_tape_creation_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automatic_tape_creation_policies",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list automatic tape creation policies"):
        list_automatic_tape_creation_policies(region_name=REGION)


def test_list_cache_reports(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cache_reports.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_cache_reports(region_name=REGION)
    mock_client.list_cache_reports.assert_called_once()


def test_list_cache_reports_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cache_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cache_reports",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cache reports"):
        list_cache_reports(region_name=REGION)


def test_list_file_system_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_file_system_associations.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_file_system_associations(region_name=REGION)
    mock_client.list_file_system_associations.assert_called_once()


def test_list_file_system_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_file_system_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_file_system_associations",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list file system associations"):
        list_file_system_associations(region_name=REGION)


def test_list_local_disks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_local_disks.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_local_disks("test-gateway_arn", region_name=REGION)
    mock_client.list_local_disks.assert_called_once()


def test_list_local_disks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_local_disks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_local_disks",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list local disks"):
        list_local_disks("test-gateway_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_tape_pools(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tape_pools.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tape_pools(region_name=REGION)
    mock_client.list_tape_pools.assert_called_once()


def test_list_tape_pools_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tape_pools.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tape_pools",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tape pools"):
        list_tape_pools(region_name=REGION)


def test_list_tapes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tapes(region_name=REGION)
    mock_client.list_tapes.assert_called_once()


def test_list_tapes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tapes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tapes",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tapes"):
        list_tapes(region_name=REGION)


def test_list_volume_initiators(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_volume_initiators.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_volume_initiators("test-volume_arn", region_name=REGION)
    mock_client.list_volume_initiators.assert_called_once()


def test_list_volume_initiators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_volume_initiators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_volume_initiators",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list volume initiators"):
        list_volume_initiators("test-volume_arn", region_name=REGION)


def test_list_volume_recovery_points(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_volume_recovery_points.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_volume_recovery_points("test-gateway_arn", region_name=REGION)
    mock_client.list_volume_recovery_points.assert_called_once()


def test_list_volume_recovery_points_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_volume_recovery_points.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_volume_recovery_points",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list volume recovery points"):
        list_volume_recovery_points("test-gateway_arn", region_name=REGION)


def test_notify_when_uploaded(monkeypatch):
    mock_client = MagicMock()
    mock_client.notify_when_uploaded.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    notify_when_uploaded("test-file_share_arn", region_name=REGION)
    mock_client.notify_when_uploaded.assert_called_once()


def test_notify_when_uploaded_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.notify_when_uploaded.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "notify_when_uploaded",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to notify when uploaded"):
        notify_when_uploaded("test-file_share_arn", region_name=REGION)


def test_refresh_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.refresh_cache.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    refresh_cache("test-file_share_arn", region_name=REGION)
    mock_client.refresh_cache.assert_called_once()


def test_refresh_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.refresh_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "refresh_cache",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to refresh cache"):
        refresh_cache("test-file_share_arn", region_name=REGION)


def test_remove_tags_from_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    remove_tags_from_resource("test-resource_arn", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_arn", [], region_name=REGION)


def test_reset_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cache.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    reset_cache("test-gateway_arn", region_name=REGION)
    mock_client.reset_cache.assert_called_once()


def test_reset_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_cache",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset cache"):
        reset_cache("test-gateway_arn", region_name=REGION)


def test_retrieve_tape_archive(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_tape_archive.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    retrieve_tape_archive("test-tape_arn", "test-gateway_arn", region_name=REGION)
    mock_client.retrieve_tape_archive.assert_called_once()


def test_retrieve_tape_archive_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_tape_archive.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retrieve_tape_archive",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to retrieve tape archive"):
        retrieve_tape_archive("test-tape_arn", "test-gateway_arn", region_name=REGION)


def test_retrieve_tape_recovery_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_tape_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    retrieve_tape_recovery_point("test-tape_arn", "test-gateway_arn", region_name=REGION)
    mock_client.retrieve_tape_recovery_point.assert_called_once()


def test_retrieve_tape_recovery_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.retrieve_tape_recovery_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "retrieve_tape_recovery_point",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to retrieve tape recovery point"):
        retrieve_tape_recovery_point("test-tape_arn", "test-gateway_arn", region_name=REGION)


def test_set_local_console_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_local_console_password.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    set_local_console_password("test-gateway_arn", "test-local_console_password", region_name=REGION)
    mock_client.set_local_console_password.assert_called_once()


def test_set_local_console_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_local_console_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_local_console_password",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set local console password"):
        set_local_console_password("test-gateway_arn", "test-local_console_password", region_name=REGION)


def test_set_smb_guest_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_smb_guest_password.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    set_smb_guest_password("test-gateway_arn", "test-password", region_name=REGION)
    mock_client.set_smb_guest_password.assert_called_once()


def test_set_smb_guest_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_smb_guest_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_smb_guest_password",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set smb guest password"):
        set_smb_guest_password("test-gateway_arn", "test-password", region_name=REGION)


def test_start_availability_monitor_test(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_availability_monitor_test.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    start_availability_monitor_test("test-gateway_arn", region_name=REGION)
    mock_client.start_availability_monitor_test.assert_called_once()


def test_start_availability_monitor_test_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_availability_monitor_test.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_availability_monitor_test",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start availability monitor test"):
        start_availability_monitor_test("test-gateway_arn", region_name=REGION)


def test_start_cache_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_cache_report.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", region_name=REGION)
    mock_client.start_cache_report.assert_called_once()


def test_start_cache_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_cache_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_cache_report",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start cache report"):
        start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", region_name=REGION)


def test_start_gateway(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_gateway.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    start_gateway("test-gateway_arn", region_name=REGION)
    mock_client.start_gateway.assert_called_once()


def test_start_gateway_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_gateway.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_gateway",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start gateway"):
        start_gateway("test-gateway_arn", region_name=REGION)


def test_update_automatic_tape_creation_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automatic_tape_creation_policy.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_automatic_tape_creation_policy([], "test-gateway_arn", region_name=REGION)
    mock_client.update_automatic_tape_creation_policy.assert_called_once()


def test_update_automatic_tape_creation_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automatic_tape_creation_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automatic_tape_creation_policy",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update automatic tape creation policy"):
        update_automatic_tape_creation_policy([], "test-gateway_arn", region_name=REGION)


def test_update_bandwidth_rate_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bandwidth_rate_limit.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_bandwidth_rate_limit("test-gateway_arn", region_name=REGION)
    mock_client.update_bandwidth_rate_limit.assert_called_once()


def test_update_bandwidth_rate_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bandwidth_rate_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bandwidth_rate_limit",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update bandwidth rate limit"):
        update_bandwidth_rate_limit("test-gateway_arn", region_name=REGION)


def test_update_bandwidth_rate_limit_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bandwidth_rate_limit_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_bandwidth_rate_limit_schedule("test-gateway_arn", [], region_name=REGION)
    mock_client.update_bandwidth_rate_limit_schedule.assert_called_once()


def test_update_bandwidth_rate_limit_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_bandwidth_rate_limit_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_bandwidth_rate_limit_schedule",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update bandwidth rate limit schedule"):
        update_bandwidth_rate_limit_schedule("test-gateway_arn", [], region_name=REGION)


def test_update_chap_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_chap_credentials.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", region_name=REGION)
    mock_client.update_chap_credentials.assert_called_once()


def test_update_chap_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_chap_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_chap_credentials",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update chap credentials"):
        update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", region_name=REGION)


def test_update_file_system_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_system_association.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_file_system_association("test-file_system_association_arn", region_name=REGION)
    mock_client.update_file_system_association.assert_called_once()


def test_update_file_system_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_system_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_file_system_association",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update file system association"):
        update_file_system_association("test-file_system_association_arn", region_name=REGION)


def test_update_gateway_information(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_information.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_gateway_information("test-gateway_arn", region_name=REGION)
    mock_client.update_gateway_information.assert_called_once()


def test_update_gateway_information_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_information.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_gateway_information",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update gateway information"):
        update_gateway_information("test-gateway_arn", region_name=REGION)


def test_update_gateway_software_now(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_software_now.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_gateway_software_now("test-gateway_arn", region_name=REGION)
    mock_client.update_gateway_software_now.assert_called_once()


def test_update_gateway_software_now_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_gateway_software_now.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_gateway_software_now",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update gateway software now"):
        update_gateway_software_now("test-gateway_arn", region_name=REGION)


def test_update_maintenance_start_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_start_time.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_maintenance_start_time("test-gateway_arn", region_name=REGION)
    mock_client.update_maintenance_start_time.assert_called_once()


def test_update_maintenance_start_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_maintenance_start_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_maintenance_start_time",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update maintenance start time"):
        update_maintenance_start_time("test-gateway_arn", region_name=REGION)


def test_update_smb_file_share(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_file_share.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_smb_file_share("test-file_share_arn", region_name=REGION)
    mock_client.update_smb_file_share.assert_called_once()


def test_update_smb_file_share_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_file_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_smb_file_share",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update smb file share"):
        update_smb_file_share("test-file_share_arn", region_name=REGION)


def test_update_smb_file_share_visibility(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_file_share_visibility.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_smb_file_share_visibility("test-gateway_arn", True, region_name=REGION)
    mock_client.update_smb_file_share_visibility.assert_called_once()


def test_update_smb_file_share_visibility_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_file_share_visibility.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_smb_file_share_visibility",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update smb file share visibility"):
        update_smb_file_share_visibility("test-gateway_arn", True, region_name=REGION)


def test_update_smb_local_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_local_groups.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_smb_local_groups("test-gateway_arn", {}, region_name=REGION)
    mock_client.update_smb_local_groups.assert_called_once()


def test_update_smb_local_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_local_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_smb_local_groups",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update smb local groups"):
        update_smb_local_groups("test-gateway_arn", {}, region_name=REGION)


def test_update_smb_security_strategy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_security_strategy.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_smb_security_strategy("test-gateway_arn", "test-smb_security_strategy", region_name=REGION)
    mock_client.update_smb_security_strategy.assert_called_once()


def test_update_smb_security_strategy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_smb_security_strategy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_smb_security_strategy",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update smb security strategy"):
        update_smb_security_strategy("test-gateway_arn", "test-smb_security_strategy", region_name=REGION)


def test_update_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_snapshot_schedule("test-volume_arn", 1, 1, region_name=REGION)
    mock_client.update_snapshot_schedule.assert_called_once()


def test_update_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update snapshot schedule"):
        update_snapshot_schedule("test-volume_arn", 1, 1, region_name=REGION)


def test_update_vtl_device_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vtl_device_type.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_vtl_device_type("test-vtl_device_arn", "test-device_type", region_name=REGION)
    mock_client.update_vtl_device_type.assert_called_once()


def test_update_vtl_device_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_vtl_device_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_vtl_device_type",
    )
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update vtl device type"):
        update_vtl_device_type("test-vtl_device_arn", "test-device_type", region_name=REGION)


def test_list_file_shares_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_file_shares
    mock_client = MagicMock()
    mock_client.list_file_shares.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_file_shares(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.list_file_shares.assert_called_once()

def test_list_volumes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_volumes
    mock_client = MagicMock()
    mock_client.list_volumes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_volumes(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.list_volumes.assert_called_once()

def test_assign_tape_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import assign_tape_pool
    mock_client = MagicMock()
    mock_client.assign_tape_pool.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    assign_tape_pool("test-tape_arn", "test-pool_id", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.assign_tape_pool.assert_called_once()

def test_associate_file_system_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import associate_file_system
    mock_client = MagicMock()
    mock_client.associate_file_system.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", tags=[{"Key": "k", "Value": "v"}], audit_destination_arn="test-audit_destination_arn", cache_attributes="test-cache_attributes", endpoint_network_configuration={}, region_name="us-east-1")
    mock_client.associate_file_system.assert_called_once()

def test_attach_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import attach_volume
    mock_client = MagicMock()
    mock_client.attach_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", target_name="test-target_name", disk_id="test-disk_id", region_name="us-east-1")
    mock_client.attach_volume.assert_called_once()

def test_create_cached_iscsi_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_cached_iscsi_volume
    mock_client = MagicMock()
    mock_client.create_cached_iscsi_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", snapshot_id="test-snapshot_id", source_volume_arn="test-source_volume_arn", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_cached_iscsi_volume.assert_called_once()

def test_create_smb_file_share_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_smb_file_share
    mock_client = MagicMock()
    mock_client.create_smb_file_share.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", encryption_type="test-encryption_type", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", default_storage_class="test-default_storage_class", object_acl="test-object_acl", read_only="test-read_only", guess_mime_type_enabled="test-guess_mime_type_enabled", requester_pays="test-requester_pays", smbacl_enabled="test-smbacl_enabled", access_based_enumeration="test-access_based_enumeration", admin_user_list="test-admin_user_list", valid_user_list="test-valid_user_list", invalid_user_list="test-invalid_user_list", audit_destination_arn="test-audit_destination_arn", authentication="test-authentication", case_sensitivity="test-case_sensitivity", tags=[{"Key": "k", "Value": "v"}], file_share_name="test-file_share_name", cache_attributes="test-cache_attributes", notification_policy="{}", vpc_endpoint_dns_name="test-vpc_endpoint_dns_name", bucket_region="test-bucket_region", oplocks_enabled="test-oplocks_enabled", region_name="us-east-1")
    mock_client.create_smb_file_share.assert_called_once()

def test_create_snapshot_from_volume_recovery_point_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_snapshot_from_volume_recovery_point
    mock_client = MagicMock()
    mock_client.create_snapshot_from_volume_recovery_point.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_snapshot_from_volume_recovery_point.assert_called_once()

def test_create_stored_iscsi_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_stored_iscsi_volume
    mock_client = MagicMock()
    mock_client.create_stored_iscsi_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", "test-preserve_existing_data", "test-target_name", "test-network_interface_id", snapshot_id="test-snapshot_id", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_stored_iscsi_volume.assert_called_once()

def test_create_tape_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_tape_pool
    mock_client = MagicMock()
    mock_client.create_tape_pool.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tape_pool("test-pool_name", "test-storage_class", retention_lock_type="test-retention_lock_type", retention_lock_time_in_days="test-retention_lock_time_in_days", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_tape_pool.assert_called_once()

def test_create_tape_with_barcode_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_tape_with_barcode
    mock_client = MagicMock()
    mock_client.create_tape_with_barcode.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", pool_id="test-pool_id", worm="test-worm", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_tape_with_barcode.assert_called_once()

def test_create_tapes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import create_tapes
    mock_client = MagicMock()
    mock_client.create_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    create_tapes("test-gateway_arn", 1, "test-client_token", "test-num_tapes_to_create", "test-tape_barcode_prefix", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", pool_id="test-pool_id", worm="test-worm", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_tapes.assert_called_once()

def test_delete_tape_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import delete_tape
    mock_client = MagicMock()
    mock_client.delete_tape.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_tape("test-gateway_arn", "test-tape_arn", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.delete_tape.assert_called_once()

def test_delete_tape_archive_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import delete_tape_archive
    mock_client = MagicMock()
    mock_client.delete_tape_archive.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    delete_tape_archive("test-tape_arn", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.delete_tape_archive.assert_called_once()

def test_describe_tape_archives_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import describe_tape_archives
    mock_client = MagicMock()
    mock_client.describe_tape_archives.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tape_archives(tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.describe_tape_archives.assert_called_once()

def test_describe_tape_recovery_points_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import describe_tape_recovery_points
    mock_client = MagicMock()
    mock_client.describe_tape_recovery_points.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tape_recovery_points("test-gateway_arn", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.describe_tape_recovery_points.assert_called_once()

def test_describe_tapes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import describe_tapes
    mock_client = MagicMock()
    mock_client.describe_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_tapes("test-gateway_arn", tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.describe_tapes.assert_called_once()

def test_describe_vtl_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import describe_vtl_devices
    mock_client = MagicMock()
    mock_client.describe_vtl_devices.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    describe_vtl_devices("test-gateway_arn", vtl_device_ar_ns="test-vtl_device_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.describe_vtl_devices.assert_called_once()

def test_detach_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import detach_volume
    mock_client = MagicMock()
    mock_client.detach_volume.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    detach_volume("test-volume_arn", force_detach=True, region_name="us-east-1")
    mock_client.detach_volume.assert_called_once()

def test_disassociate_file_system_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import disassociate_file_system
    mock_client = MagicMock()
    mock_client.disassociate_file_system.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    disassociate_file_system("test-file_system_association_arn", force_delete=True, region_name="us-east-1")
    mock_client.disassociate_file_system.assert_called_once()

def test_evict_files_failing_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import evict_files_failing_upload
    mock_client = MagicMock()
    mock_client.evict_files_failing_upload.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    evict_files_failing_upload("test-file_share_arn", force_remove=True, region_name="us-east-1")
    mock_client.evict_files_failing_upload.assert_called_once()

def test_join_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import join_domain
    mock_client = MagicMock()
    mock_client.join_domain.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", organizational_unit="test-organizational_unit", domain_controllers="test-domain_controllers", timeout_in_seconds=1, region_name="us-east-1")
    mock_client.join_domain.assert_called_once()

def test_list_automatic_tape_creation_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_automatic_tape_creation_policies
    mock_client = MagicMock()
    mock_client.list_automatic_tape_creation_policies.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_automatic_tape_creation_policies(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.list_automatic_tape_creation_policies.assert_called_once()

def test_list_cache_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_cache_reports
    mock_client = MagicMock()
    mock_client.list_cache_reports.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_cache_reports(marker="test-marker", region_name="us-east-1")
    mock_client.list_cache_reports.assert_called_once()

def test_list_file_system_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_file_system_associations
    mock_client = MagicMock()
    mock_client.list_file_system_associations.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_file_system_associations(gateway_arn="test-gateway_arn", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_file_system_associations.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_tape_pools_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_tape_pools
    mock_client = MagicMock()
    mock_client.list_tape_pools.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tape_pools(pool_ar_ns="test-pool_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.list_tape_pools.assert_called_once()

def test_list_tapes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import list_tapes
    mock_client = MagicMock()
    mock_client.list_tapes.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    list_tapes(tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.list_tapes.assert_called_once()

def test_refresh_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import refresh_cache
    mock_client = MagicMock()
    mock_client.refresh_cache.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    refresh_cache("test-file_share_arn", folder_list="test-folder_list", recursive=True, region_name="us-east-1")
    mock_client.refresh_cache.assert_called_once()

def test_start_cache_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import start_cache_report
    mock_client = MagicMock()
    mock_client.start_cache_report.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", vpc_endpoint_dns_name="test-vpc_endpoint_dns_name", inclusion_filters="test-inclusion_filters", exclusion_filters="test-exclusion_filters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_cache_report.assert_called_once()

def test_update_bandwidth_rate_limit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_bandwidth_rate_limit
    mock_client = MagicMock()
    mock_client.update_bandwidth_rate_limit.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_bandwidth_rate_limit("test-gateway_arn", average_upload_rate_limit_in_bits_per_sec=1, average_download_rate_limit_in_bits_per_sec=1, region_name="us-east-1")
    mock_client.update_bandwidth_rate_limit.assert_called_once()

def test_update_chap_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_chap_credentials
    mock_client = MagicMock()
    mock_client.update_chap_credentials.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", secret_to_authenticate_target="test-secret_to_authenticate_target", region_name="us-east-1")
    mock_client.update_chap_credentials.assert_called_once()

def test_update_file_system_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_file_system_association
    mock_client = MagicMock()
    mock_client.update_file_system_association.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_file_system_association("test-file_system_association_arn", user_name="test-user_name", password="test-password", audit_destination_arn="test-audit_destination_arn", cache_attributes="test-cache_attributes", region_name="us-east-1")
    mock_client.update_file_system_association.assert_called_once()

def test_update_gateway_information_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_gateway_information
    mock_client = MagicMock()
    mock_client.update_gateway_information.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_gateway_information("test-gateway_arn", gateway_name="test-gateway_name", gateway_timezone="test-gateway_timezone", cloud_watch_log_group_arn="test-cloud_watch_log_group_arn", gateway_capacity="test-gateway_capacity", region_name="us-east-1")
    mock_client.update_gateway_information.assert_called_once()

def test_update_maintenance_start_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_maintenance_start_time
    mock_client = MagicMock()
    mock_client.update_maintenance_start_time.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_maintenance_start_time("test-gateway_arn", hour_of_day="test-hour_of_day", minute_of_hour="test-minute_of_hour", day_of_week="test-day_of_week", day_of_month="test-day_of_month", software_update_preferences="test-software_update_preferences", region_name="us-east-1")
    mock_client.update_maintenance_start_time.assert_called_once()

def test_update_smb_file_share_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_smb_file_share
    mock_client = MagicMock()
    mock_client.update_smb_file_share.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_smb_file_share("test-file_share_arn", encryption_type="test-encryption_type", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", default_storage_class="test-default_storage_class", object_acl="test-object_acl", read_only="test-read_only", guess_mime_type_enabled="test-guess_mime_type_enabled", requester_pays="test-requester_pays", smbacl_enabled="test-smbacl_enabled", access_based_enumeration="test-access_based_enumeration", admin_user_list="test-admin_user_list", valid_user_list="test-valid_user_list", invalid_user_list="test-invalid_user_list", audit_destination_arn="test-audit_destination_arn", case_sensitivity="test-case_sensitivity", file_share_name="test-file_share_name", cache_attributes="test-cache_attributes", notification_policy="{}", oplocks_enabled="test-oplocks_enabled", region_name="us-east-1")
    mock_client.update_smb_file_share.assert_called_once()

def test_update_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.storage_gateway import update_snapshot_schedule
    mock_client = MagicMock()
    mock_client.update_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.storage_gateway.get_client", lambda *a, **kw: mock_client)
    update_snapshot_schedule("test-volume_arn", "test-start_at", "test-recurrence_in_hours", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.update_snapshot_schedule.assert_called_once()
