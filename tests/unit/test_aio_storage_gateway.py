

"""Tests for aws_util.aio.storage_gateway -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.storage_gateway as mod
from aws_util.aio.storage_gateway import (

    update_nfs_file_share,
    list_file_shares,
    list_volumes,
    assign_tape_pool,
    associate_file_system,
    attach_volume,
    create_cached_iscsi_volume,
    create_smb_file_share,
    create_snapshot_from_volume_recovery_point,
    create_stored_iscsi_volume,
    create_tape_pool,
    create_tape_with_barcode,
    create_tapes,
    delete_tape,
    delete_tape_archive,
    describe_tape_archives,
    describe_tape_recovery_points,
    describe_tapes,
    describe_vtl_devices,
    detach_volume,
    disassociate_file_system,
    evict_files_failing_upload,
    join_domain,
    list_automatic_tape_creation_policies,
    list_cache_reports,
    list_file_system_associations,
    list_tags_for_resource,
    list_tape_pools,
    list_tapes,
    refresh_cache,
    start_cache_report,
    update_bandwidth_rate_limit,
    update_chap_credentials,
    update_file_system_association,
    update_gateway_information,
    update_maintenance_start_time,
    update_smb_file_share,
    update_snapshot_schedule,
    add_cache,
    add_tags_to_resource,
    add_upload_buffer,
    add_working_storage,
    cancel_archival,
    cancel_cache_report,
    cancel_retrieval,
    delete_automatic_tape_creation_policy,
    delete_bandwidth_rate_limit,
    delete_cache_report,
    delete_chap_credentials,
    delete_snapshot_schedule,
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
    describe_upload_buffer,
    describe_working_storage,
    disable_gateway,
    list_local_disks,
    list_volume_initiators,
    list_volume_recovery_points,
    notify_when_uploaded,
    remove_tags_from_resource,
    reset_cache,
    retrieve_tape_archive,
    retrieve_tape_recovery_point,
    set_local_console_password,
    set_smb_guest_password,
    start_availability_monitor_test,
    start_gateway,
    update_automatic_tape_creation_policy,
    update_bandwidth_rate_limit_schedule,
    update_gateway_software_now,
    update_smb_file_share_visibility,
    update_smb_local_groups,
    update_smb_security_strategy,
    update_vtl_device_type,
)


REGION = "us-east-1"
_GW = {"GatewayARN": "arn:gw", "GatewayId": "gw-1", "GatewayName": "gw",
       "GatewayType": "FILE_S3", "GatewayState": "RUNNING", "GatewayTimezone": "GMT-5:00"}
_FS = {"FileShareARN": "arn:fs", "FileShareId": "fs-1", "FileShareStatus": "AVAILABLE",
       "GatewayARN": "arn:gw", "LocationARN": "arn:s3", "Role": "arn:role", "Path": "/share"}
_VOL = {"VolumeARN": "arn:vol", "VolumeId": "vol-1", "VolumeType": "STORED",
        "VolumeStatus": "AVAILABLE", "VolumeSizeInBytes": 1073741824}


@pytest.fixture()
def mc(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: client)
    return client


async def test_activate_gateway_success(mc):
    mc.call.return_value = {"GatewayARN": "arn:gw"}
    r = await mod.activate_gateway(activation_key="k", gateway_name="g",
                                    gateway_timezone="GMT", gateway_region="us-east-1")
    assert r == "arn:gw"

async def test_activate_gateway_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.activate_gateway(activation_key="k", gateway_name="g",
                                    gateway_timezone="GMT", gateway_region="us-east-1")

async def test_activate_gateway_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="activate_gateway failed"):
        await mod.activate_gateway(activation_key="k", gateway_name="g",
                                    gateway_timezone="GMT", gateway_region="us-east-1")


async def test_describe_gateway_information_success(mc):
    mc.call.return_value = _GW
    r = await mod.describe_gateway_information("arn:gw")
    assert r.gateway_arn == "arn:gw"

async def test_describe_gateway_information_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.describe_gateway_information("arn:gw")

async def test_describe_gateway_information_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_gateway_information failed"):
        await mod.describe_gateway_information("arn:gw")


async def test_list_gateways_success(mc):
    mc.call.return_value = {"Gateways": [_GW]}
    r = await mod.list_gateways()
    assert len(r) == 1

async def test_list_gateways_pagination(mc):
    mc.call.side_effect = [
        {"Gateways": [_GW], "Marker": "m1"},
        {"Gateways": [_GW]},
    ]
    r = await mod.list_gateways()
    assert len(r) == 2

async def test_list_gateways_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_gateways()

async def test_list_gateways_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_gateways failed"):
        await mod.list_gateways()


async def test_delete_gateway_success(mc):
    mc.call.return_value = {"GatewayARN": "arn:gw"}
    r = await mod.delete_gateway("arn:gw")
    assert r == "arn:gw"

async def test_delete_gateway_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_gateway("arn:gw")

async def test_delete_gateway_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_gateway failed"):
        await mod.delete_gateway("arn:gw")


async def test_shutdown_gateway_success(mc):
    mc.call.return_value = {"GatewayARN": "arn:gw"}
    r = await mod.shutdown_gateway("arn:gw")
    assert r == "arn:gw"

async def test_shutdown_gateway_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.shutdown_gateway("arn:gw")

async def test_shutdown_gateway_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="shutdown_gateway failed"):
        await mod.shutdown_gateway("arn:gw")


async def test_create_nfs_file_share_success(mc):
    mc.call.return_value = _FS
    r = await mod.create_nfs_file_share(client_token="t", gateway_arn="arn:gw",
                                         role="arn:role", location_arn="arn:s3")
    assert r.file_share_arn == "arn:fs"

async def test_create_nfs_file_share_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_nfs_file_share(client_token="t", gateway_arn="arn:gw",
                                         role="arn:role", location_arn="arn:s3")

async def test_create_nfs_file_share_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_nfs_file_share failed"):
        await mod.create_nfs_file_share(client_token="t", gateway_arn="arn:gw",
                                         role="arn:role", location_arn="arn:s3")


async def test_describe_nfs_file_shares_success(mc):
    mc.call.return_value = {"NFSFileShareInfoList": [_FS]}
    r = await mod.describe_nfs_file_shares(["arn:fs"])
    assert len(r) == 1

async def test_describe_nfs_file_shares_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.describe_nfs_file_shares(["arn:fs"])

async def test_describe_nfs_file_shares_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_nfs_file_shares failed"):
        await mod.describe_nfs_file_shares(["arn:fs"])


async def test_update_nfs_file_share_success(mc):
    mc.call.return_value = {"FileShareARN": "arn:fs"}
    r = await mod.update_nfs_file_share("arn:fs", default_storage_class="S3_IA", kms_encrypted=True)
    assert r.file_share_arn == "arn:fs"

async def test_update_nfs_file_share_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_nfs_file_share("arn:fs")

async def test_update_nfs_file_share_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_nfs_file_share failed"):
        await mod.update_nfs_file_share("arn:fs")


async def test_delete_file_share_success(mc):
    mc.call.return_value = {"FileShareARN": "arn:fs"}
    r = await mod.delete_file_share("arn:fs", force_delete=True)
    assert r == "arn:fs"

async def test_delete_file_share_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_file_share("arn:fs")

async def test_delete_file_share_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_file_share failed"):
        await mod.delete_file_share("arn:fs")


async def test_list_file_shares_success(mc):
    mc.call.return_value = {"FileShareInfoList": [_FS]}
    r = await mod.list_file_shares(gateway_arn="arn:gw")
    assert len(r) == 1

async def test_list_file_shares_pagination(mc):
    mc.call.side_effect = [
        {"FileShareInfoList": [_FS], "NextMarker": "m1"},
        {"FileShareInfoList": [_FS]},
    ]
    r = await mod.list_file_shares()
    assert len(r) == 2

async def test_list_file_shares_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_file_shares()

async def test_list_file_shares_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_file_shares failed"):
        await mod.list_file_shares()


async def test_list_volumes_success(mc):
    mc.call.return_value = {"VolumeInfos": [_VOL]}
    r = await mod.list_volumes(gateway_arn="arn:gw")
    assert len(r) == 1

async def test_list_volumes_pagination(mc):
    mc.call.side_effect = [
        {"VolumeInfos": [_VOL], "Marker": "m1"},
        {"VolumeInfos": [_VOL]},
    ]
    r = await mod.list_volumes()
    assert len(r) == 2

async def test_list_volumes_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_volumes()

async def test_list_volumes_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_volumes failed"):
        await mod.list_volumes()


async def test_describe_stored_iscsi_volumes_success(mc):
    mc.call.return_value = {"StorediSCSIVolumes": [_VOL]}
    r = await mod.describe_stored_iscsi_volumes(["arn:vol"])
    assert len(r) == 1

async def test_describe_stored_iscsi_volumes_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.describe_stored_iscsi_volumes(["arn:vol"])

async def test_describe_stored_iscsi_volumes_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_stored_iscsi_volumes failed"):
        await mod.describe_stored_iscsi_volumes(["arn:vol"])


async def test_create_snapshot_success(mc):
    mc.call.return_value = {"SnapshotId": "snap-1", "VolumeARN": "arn:vol"}
    r = await mod.create_snapshot("arn:vol", snapshot_description="desc")
    assert r.snapshot_id == "snap-1"

async def test_create_snapshot_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_snapshot("arn:vol")

async def test_create_snapshot_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_snapshot failed"):
        await mod.create_snapshot("arn:vol")


async def test_describe_snapshots_success(mc):
    mc.call.return_value = {"VolumeARN": "arn:vol", "Description": "d", "Extra": "e"}
    r = await mod.describe_snapshots("arn:vol")
    assert len(r) == 1
    assert r[0].volume_arn == "arn:vol"
    assert "Extra" in r[0].extra

async def test_describe_snapshots_runtime_error(mc):
    mc.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.describe_snapshots("arn:vol")

async def test_describe_snapshots_generic_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_snapshots failed"):
        await mod.describe_snapshots("arn:vol")


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_add_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_cache("test-gateway_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_cache("test-gateway_arn", [], )


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_arn", [], )


async def test_add_upload_buffer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_upload_buffer("test-gateway_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_upload_buffer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_upload_buffer("test-gateway_arn", [], )


async def test_add_working_storage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_working_storage("test-gateway_arn", [], )
    mock_client.call.assert_called_once()


async def test_add_working_storage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_working_storage("test-gateway_arn", [], )


async def test_assign_tape_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await assign_tape_pool("test-tape_arn", "test-pool_id", )
    mock_client.call.assert_called_once()


async def test_assign_tape_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await assign_tape_pool("test-tape_arn", "test-pool_id", )


async def test_associate_file_system(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", )
    mock_client.call.assert_called_once()


async def test_associate_file_system_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", )


async def test_attach_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_attach_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", )


async def test_cancel_archival(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_archival("test-gateway_arn", "test-tape_arn", )
    mock_client.call.assert_called_once()


async def test_cancel_archival_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_archival("test-gateway_arn", "test-tape_arn", )


async def test_cancel_cache_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_cache_report("test-cache_report_arn", )
    mock_client.call.assert_called_once()


async def test_cancel_cache_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_cache_report("test-cache_report_arn", )


async def test_cancel_retrieval(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_retrieval("test-gateway_arn", "test-tape_arn", )
    mock_client.call.assert_called_once()


async def test_cancel_retrieval_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_retrieval("test-gateway_arn", "test-tape_arn", )


async def test_create_cached_iscsi_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_create_cached_iscsi_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", )


async def test_create_smb_file_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", )
    mock_client.call.assert_called_once()


async def test_create_smb_file_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", )


async def test_create_snapshot_from_volume_recovery_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_from_volume_recovery_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", )


async def test_create_stored_iscsi_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", True, "test-target_name", "test-network_interface_id", )
    mock_client.call.assert_called_once()


async def test_create_stored_iscsi_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", True, "test-target_name", "test-network_interface_id", )


async def test_create_tape_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tape_pool("test-pool_name", "test-storage_class", )
    mock_client.call.assert_called_once()


async def test_create_tape_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tape_pool("test-pool_name", "test-storage_class", )


async def test_create_tape_with_barcode(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", )
    mock_client.call.assert_called_once()


async def test_create_tape_with_barcode_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", )


async def test_create_tapes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tapes("test-gateway_arn", 1, "test-client_token", 1, "test-tape_barcode_prefix", )
    mock_client.call.assert_called_once()


async def test_create_tapes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tapes("test-gateway_arn", 1, "test-client_token", 1, "test-tape_barcode_prefix", )


async def test_delete_automatic_tape_creation_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_automatic_tape_creation_policy("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_delete_automatic_tape_creation_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_automatic_tape_creation_policy("test-gateway_arn", )


async def test_delete_bandwidth_rate_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_bandwidth_rate_limit("test-gateway_arn", "test-bandwidth_type", )
    mock_client.call.assert_called_once()


async def test_delete_bandwidth_rate_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_bandwidth_rate_limit("test-gateway_arn", "test-bandwidth_type", )


async def test_delete_cache_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cache_report("test-cache_report_arn", )
    mock_client.call.assert_called_once()


async def test_delete_cache_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_report("test-cache_report_arn", )


async def test_delete_chap_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_chap_credentials("test-target_arn", "test-initiator_name", )
    mock_client.call.assert_called_once()


async def test_delete_chap_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_chap_credentials("test-target_arn", "test-initiator_name", )


async def test_delete_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot_schedule("test-volume_arn", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot_schedule("test-volume_arn", )


async def test_delete_tape(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tape("test-gateway_arn", "test-tape_arn", )
    mock_client.call.assert_called_once()


async def test_delete_tape_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tape("test-gateway_arn", "test-tape_arn", )


async def test_delete_tape_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tape_archive("test-tape_arn", )
    mock_client.call.assert_called_once()


async def test_delete_tape_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tape_archive("test-tape_arn", )


async def test_delete_tape_pool(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tape_pool("test-pool_arn", )
    mock_client.call.assert_called_once()


async def test_delete_tape_pool_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tape_pool("test-pool_arn", )


async def test_delete_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_volume("test-volume_arn", )
    mock_client.call.assert_called_once()


async def test_delete_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_volume("test-volume_arn", )


async def test_describe_availability_monitor_test(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_availability_monitor_test("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_availability_monitor_test_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_availability_monitor_test("test-gateway_arn", )


async def test_describe_bandwidth_rate_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bandwidth_rate_limit("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_bandwidth_rate_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bandwidth_rate_limit("test-gateway_arn", )


async def test_describe_bandwidth_rate_limit_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_bandwidth_rate_limit_schedule("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_bandwidth_rate_limit_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_bandwidth_rate_limit_schedule("test-gateway_arn", )


async def test_describe_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache("test-gateway_arn", )


async def test_describe_cache_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache_report("test-cache_report_arn", )
    mock_client.call.assert_called_once()


async def test_describe_cache_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_report("test-cache_report_arn", )


async def test_describe_cached_iscsi_volumes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cached_iscsi_volumes([], )
    mock_client.call.assert_called_once()


async def test_describe_cached_iscsi_volumes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cached_iscsi_volumes([], )


async def test_describe_chap_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_chap_credentials("test-target_arn", )
    mock_client.call.assert_called_once()


async def test_describe_chap_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_chap_credentials("test-target_arn", )


async def test_describe_file_system_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_file_system_associations([], )
    mock_client.call.assert_called_once()


async def test_describe_file_system_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_file_system_associations([], )


async def test_describe_maintenance_start_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_maintenance_start_time("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_maintenance_start_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_maintenance_start_time("test-gateway_arn", )


async def test_describe_smb_file_shares(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_smb_file_shares([], )
    mock_client.call.assert_called_once()


async def test_describe_smb_file_shares_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_smb_file_shares([], )


async def test_describe_smb_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_smb_settings("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_smb_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_smb_settings("test-gateway_arn", )


async def test_describe_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshot_schedule("test-volume_arn", )
    mock_client.call.assert_called_once()


async def test_describe_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshot_schedule("test-volume_arn", )


async def test_describe_tape_archives(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tape_archives()
    mock_client.call.assert_called_once()


async def test_describe_tape_archives_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tape_archives()


async def test_describe_tape_recovery_points(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tape_recovery_points("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_tape_recovery_points_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tape_recovery_points("test-gateway_arn", )


async def test_describe_tapes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tapes("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_tapes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tapes("test-gateway_arn", )


async def test_describe_upload_buffer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_upload_buffer("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_upload_buffer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_upload_buffer("test-gateway_arn", )


async def test_describe_vtl_devices(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vtl_devices("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_vtl_devices_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vtl_devices("test-gateway_arn", )


async def test_describe_working_storage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_working_storage("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_describe_working_storage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_working_storage("test-gateway_arn", )


async def test_detach_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_volume("test-volume_arn", )
    mock_client.call.assert_called_once()


async def test_detach_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_volume("test-volume_arn", )


async def test_disable_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_gateway("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_disable_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_gateway("test-gateway_arn", )


async def test_disassociate_file_system(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_file_system("test-file_system_association_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_file_system_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_file_system("test-file_system_association_arn", )


async def test_evict_files_failing_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await evict_files_failing_upload("test-file_share_arn", )
    mock_client.call.assert_called_once()


async def test_evict_files_failing_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await evict_files_failing_upload("test-file_share_arn", )


async def test_join_domain(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", )
    mock_client.call.assert_called_once()


async def test_join_domain_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", )


async def test_list_automatic_tape_creation_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_automatic_tape_creation_policies()
    mock_client.call.assert_called_once()


async def test_list_automatic_tape_creation_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_automatic_tape_creation_policies()


async def test_list_cache_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cache_reports()
    mock_client.call.assert_called_once()


async def test_list_cache_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cache_reports()


async def test_list_file_system_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_file_system_associations()
    mock_client.call.assert_called_once()


async def test_list_file_system_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_file_system_associations()


async def test_list_local_disks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_local_disks("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_list_local_disks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_local_disks("test-gateway_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tape_pools(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tape_pools()
    mock_client.call.assert_called_once()


async def test_list_tape_pools_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tape_pools()


async def test_list_tapes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tapes()
    mock_client.call.assert_called_once()


async def test_list_tapes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tapes()


async def test_list_volume_initiators(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_volume_initiators("test-volume_arn", )
    mock_client.call.assert_called_once()


async def test_list_volume_initiators_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_volume_initiators("test-volume_arn", )


async def test_list_volume_recovery_points(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_volume_recovery_points("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_list_volume_recovery_points_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_volume_recovery_points("test-gateway_arn", )


async def test_notify_when_uploaded(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await notify_when_uploaded("test-file_share_arn", )
    mock_client.call.assert_called_once()


async def test_notify_when_uploaded_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await notify_when_uploaded("test-file_share_arn", )


async def test_refresh_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await refresh_cache("test-file_share_arn", )
    mock_client.call.assert_called_once()


async def test_refresh_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await refresh_cache("test-file_share_arn", )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_arn", [], )


async def test_reset_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_cache("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_reset_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_cache("test-gateway_arn", )


async def test_retrieve_tape_archive(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await retrieve_tape_archive("test-tape_arn", "test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_retrieve_tape_archive_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retrieve_tape_archive("test-tape_arn", "test-gateway_arn", )


async def test_retrieve_tape_recovery_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await retrieve_tape_recovery_point("test-tape_arn", "test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_retrieve_tape_recovery_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await retrieve_tape_recovery_point("test-tape_arn", "test-gateway_arn", )


async def test_set_local_console_password(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_local_console_password("test-gateway_arn", "test-local_console_password", )
    mock_client.call.assert_called_once()


async def test_set_local_console_password_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_local_console_password("test-gateway_arn", "test-local_console_password", )


async def test_set_smb_guest_password(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_smb_guest_password("test-gateway_arn", "test-password", )
    mock_client.call.assert_called_once()


async def test_set_smb_guest_password_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_smb_guest_password("test-gateway_arn", "test-password", )


async def test_start_availability_monitor_test(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_availability_monitor_test("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_start_availability_monitor_test_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_availability_monitor_test("test-gateway_arn", )


async def test_start_cache_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", )
    mock_client.call.assert_called_once()


async def test_start_cache_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", )


async def test_start_gateway(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_gateway("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_start_gateway_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_gateway("test-gateway_arn", )


async def test_update_automatic_tape_creation_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_automatic_tape_creation_policy([], "test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_update_automatic_tape_creation_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_automatic_tape_creation_policy([], "test-gateway_arn", )


async def test_update_bandwidth_rate_limit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bandwidth_rate_limit("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_update_bandwidth_rate_limit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bandwidth_rate_limit("test-gateway_arn", )


async def test_update_bandwidth_rate_limit_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_bandwidth_rate_limit_schedule("test-gateway_arn", [], )
    mock_client.call.assert_called_once()


async def test_update_bandwidth_rate_limit_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_bandwidth_rate_limit_schedule("test-gateway_arn", [], )


async def test_update_chap_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", )
    mock_client.call.assert_called_once()


async def test_update_chap_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", )


async def test_update_file_system_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_file_system_association("test-file_system_association_arn", )
    mock_client.call.assert_called_once()


async def test_update_file_system_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_file_system_association("test-file_system_association_arn", )


async def test_update_gateway_information(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_gateway_information("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_update_gateway_information_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_gateway_information("test-gateway_arn", )


async def test_update_gateway_software_now(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_gateway_software_now("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_update_gateway_software_now_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_gateway_software_now("test-gateway_arn", )


async def test_update_maintenance_start_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_maintenance_start_time("test-gateway_arn", )
    mock_client.call.assert_called_once()


async def test_update_maintenance_start_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_maintenance_start_time("test-gateway_arn", )


async def test_update_smb_file_share(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_smb_file_share("test-file_share_arn", )
    mock_client.call.assert_called_once()


async def test_update_smb_file_share_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_smb_file_share("test-file_share_arn", )


async def test_update_smb_file_share_visibility(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_smb_file_share_visibility("test-gateway_arn", True, )
    mock_client.call.assert_called_once()


async def test_update_smb_file_share_visibility_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_smb_file_share_visibility("test-gateway_arn", True, )


async def test_update_smb_local_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_smb_local_groups("test-gateway_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_smb_local_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_smb_local_groups("test-gateway_arn", {}, )


async def test_update_smb_security_strategy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_smb_security_strategy("test-gateway_arn", "test-smb_security_strategy", )
    mock_client.call.assert_called_once()


async def test_update_smb_security_strategy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_smb_security_strategy("test-gateway_arn", "test-smb_security_strategy", )


async def test_update_snapshot_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_snapshot_schedule("test-volume_arn", 1, 1, )
    mock_client.call.assert_called_once()


async def test_update_snapshot_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_snapshot_schedule("test-volume_arn", 1, 1, )


async def test_update_vtl_device_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_vtl_device_type("test-vtl_device_arn", "test-device_type", )
    mock_client.call.assert_called_once()


async def test_update_vtl_device_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.storage_gateway.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_vtl_device_type("test-vtl_device_arn", "test-device_type", )


@pytest.mark.asyncio
async def test_list_file_shares_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_file_shares
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_file_shares(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_volumes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_volumes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_volumes(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_assign_tape_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import assign_tape_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await assign_tape_pool("test-tape_arn", "test-pool_id", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_file_system_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import associate_file_system
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await associate_file_system("test-user_name", "test-password", "test-client_token", "test-gateway_arn", "test-location_arn", tags=[{"Key": "k", "Value": "v"}], audit_destination_arn="test-audit_destination_arn", cache_attributes="test-cache_attributes", endpoint_network_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import attach_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await attach_volume("test-gateway_arn", "test-volume_arn", "test-network_interface_id", target_name="test-target_name", disk_id="test-disk_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cached_iscsi_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_cached_iscsi_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_cached_iscsi_volume("test-gateway_arn", 1, "test-target_name", "test-network_interface_id", "test-client_token", snapshot_id="test-snapshot_id", source_volume_arn="test-source_volume_arn", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_smb_file_share_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_smb_file_share
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_smb_file_share("test-client_token", "test-gateway_arn", "test-role", "test-location_arn", encryption_type="test-encryption_type", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", default_storage_class="test-default_storage_class", object_acl="test-object_acl", read_only="test-read_only", guess_mime_type_enabled="test-guess_mime_type_enabled", requester_pays="test-requester_pays", smbacl_enabled="test-smbacl_enabled", access_based_enumeration="test-access_based_enumeration", admin_user_list="test-admin_user_list", valid_user_list="test-valid_user_list", invalid_user_list="test-invalid_user_list", audit_destination_arn="test-audit_destination_arn", authentication="test-authentication", case_sensitivity="test-case_sensitivity", tags=[{"Key": "k", "Value": "v"}], file_share_name="test-file_share_name", cache_attributes="test-cache_attributes", notification_policy="{}", vpc_endpoint_dns_name="test-vpc_endpoint_dns_name", bucket_region="test-bucket_region", oplocks_enabled="test-oplocks_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_from_volume_recovery_point_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_snapshot_from_volume_recovery_point
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_snapshot_from_volume_recovery_point("test-volume_arn", "test-snapshot_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stored_iscsi_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_stored_iscsi_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_stored_iscsi_volume("test-gateway_arn", "test-disk_id", "test-preserve_existing_data", "test-target_name", "test-network_interface_id", snapshot_id="test-snapshot_id", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_tape_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_tape_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_tape_pool("test-pool_name", "test-storage_class", retention_lock_type="test-retention_lock_type", retention_lock_time_in_days="test-retention_lock_time_in_days", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_tape_with_barcode_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_tape_with_barcode
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_tape_with_barcode("test-gateway_arn", 1, "test-tape_barcode", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", pool_id="test-pool_id", worm="test-worm", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_tapes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import create_tapes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await create_tapes("test-gateway_arn", 1, "test-client_token", "test-num_tapes_to_create", "test-tape_barcode_prefix", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", pool_id="test-pool_id", worm="test-worm", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_tape_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import delete_tape
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_tape("test-gateway_arn", "test-tape_arn", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_tape_archive_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import delete_tape_archive
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await delete_tape_archive("test-tape_arn", bypass_governance_retention=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tape_archives_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import describe_tape_archives
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await describe_tape_archives(tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tape_recovery_points_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import describe_tape_recovery_points
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await describe_tape_recovery_points("test-gateway_arn", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tapes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import describe_tapes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await describe_tapes("test-gateway_arn", tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_vtl_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import describe_vtl_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await describe_vtl_devices("test-gateway_arn", vtl_device_ar_ns="test-vtl_device_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import detach_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await detach_volume("test-volume_arn", force_detach=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_file_system_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import disassociate_file_system
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await disassociate_file_system("test-file_system_association_arn", force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_evict_files_failing_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import evict_files_failing_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await evict_files_failing_upload("test-file_share_arn", force_remove=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_join_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import join_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await join_domain("test-gateway_arn", "test-domain_name", "test-user_name", "test-password", organizational_unit="test-organizational_unit", domain_controllers="test-domain_controllers", timeout_in_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_automatic_tape_creation_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_automatic_tape_creation_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_automatic_tape_creation_policies(gateway_arn="test-gateway_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cache_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_cache_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_cache_reports(marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_file_system_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_file_system_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_file_system_associations(gateway_arn="test-gateway_arn", limit=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tape_pools_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_tape_pools
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_tape_pools(pool_ar_ns="test-pool_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tapes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import list_tapes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await list_tapes(tape_ar_ns="test-tape_ar_ns", marker="test-marker", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_refresh_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import refresh_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await refresh_cache("test-file_share_arn", folder_list="test-folder_list", recursive=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_cache_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import start_cache_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await start_cache_report("test-file_share_arn", "test-role", "test-location_arn", "test-bucket_region", "test-client_token", vpc_endpoint_dns_name="test-vpc_endpoint_dns_name", inclusion_filters="test-inclusion_filters", exclusion_filters="test-exclusion_filters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_bandwidth_rate_limit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_bandwidth_rate_limit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_bandwidth_rate_limit("test-gateway_arn", average_upload_rate_limit_in_bits_per_sec=1, average_download_rate_limit_in_bits_per_sec=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_chap_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_chap_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_chap_credentials("test-target_arn", "test-secret_to_authenticate_initiator", "test-initiator_name", secret_to_authenticate_target="test-secret_to_authenticate_target", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_file_system_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_file_system_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_file_system_association("test-file_system_association_arn", user_name="test-user_name", password="test-password", audit_destination_arn="test-audit_destination_arn", cache_attributes="test-cache_attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_gateway_information_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_gateway_information
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_gateway_information("test-gateway_arn", gateway_name="test-gateway_name", gateway_timezone="test-gateway_timezone", cloud_watch_log_group_arn="test-cloud_watch_log_group_arn", gateway_capacity="test-gateway_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_maintenance_start_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_maintenance_start_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_maintenance_start_time("test-gateway_arn", hour_of_day="test-hour_of_day", minute_of_hour="test-minute_of_hour", day_of_week="test-day_of_week", day_of_month="test-day_of_month", software_update_preferences="test-software_update_preferences", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_smb_file_share_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_smb_file_share
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_smb_file_share("test-file_share_arn", encryption_type="test-encryption_type", kms_encrypted="test-kms_encrypted", kms_key="test-kms_key", default_storage_class="test-default_storage_class", object_acl="test-object_acl", read_only="test-read_only", guess_mime_type_enabled="test-guess_mime_type_enabled", requester_pays="test-requester_pays", smbacl_enabled="test-smbacl_enabled", access_based_enumeration="test-access_based_enumeration", admin_user_list="test-admin_user_list", valid_user_list="test-valid_user_list", invalid_user_list="test-invalid_user_list", audit_destination_arn="test-audit_destination_arn", case_sensitivity="test-case_sensitivity", file_share_name="test-file_share_name", cache_attributes="test-cache_attributes", notification_policy="{}", oplocks_enabled="test-oplocks_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.storage_gateway import update_snapshot_schedule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.storage_gateway.async_client", lambda *a, **kw: mock_client)
    await update_snapshot_schedule("test-volume_arn", "test-start_at", "test-recurrence_in_hours", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()
