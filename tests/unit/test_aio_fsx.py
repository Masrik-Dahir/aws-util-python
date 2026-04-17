"""Tests for aws_util.aio.fsx module."""
from __future__ import annotations

import time as _time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.fsx import (
    BackupResult,
    DataRepositoryAssociationResult,
    DataRepositoryTaskResult,
    FileSystemAliasResult,
    FileSystemResult,
    VolumeResult,
    associate_file_system_aliases,
    cancel_data_repository_task,
    copy_backup,
    create_backup,
    create_data_repository_association,
    create_data_repository_task,
    create_file_system,
    create_volume,
    delete_backup,
    delete_file_system,
    delete_volume,
    describe_backups,
    describe_data_repository_associations,
    describe_data_repository_tasks,
    describe_file_system_aliases,
    describe_file_systems,
    describe_volumes,
    disassociate_file_system_aliases,
    restore_file_system_from_backup,
    update_file_system,
    update_volume,
    wait_for_file_system,
    copy_snapshot_and_update_volume,
    create_and_attach_s3_access_point,
    create_file_cache,
    create_file_system_from_backup,
    create_snapshot,
    create_storage_virtual_machine,
    create_volume_from_backup,
    delete_data_repository_association,
    delete_file_cache,
    delete_snapshot,
    delete_storage_virtual_machine,
    describe_file_caches,
    describe_s3_access_point_attachments,
    describe_shared_vpc_configuration,
    describe_snapshots,
    describe_storage_virtual_machines,
    detach_and_delete_s3_access_point,
    list_tags_for_resource,
    release_file_system_nfs_v3_locks,
    restore_volume_from_snapshot,
    start_misconfigured_state_recovery,
    tag_resource,
    untag_resource,
    update_data_repository_association,
    update_file_cache,
    update_shared_vpc_configuration,
    update_snapshot,
    update_storage_virtual_machine,
)
from aws_util.exceptions import AwsTimeoutError


REGION = "us-east-1"
FS_ID = "fs-012345678"
BK_ID = "backup-012345678"
VOL_ID = "fsvol-012345678"
DRA_ID = "dra-012345678"
DRT_ID = "task-012345678"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _fs_dict(**overrides):
    d = {
        "FileSystemId": FS_ID,
        "FileSystemType": "LUSTRE",
        "Lifecycle": "AVAILABLE",
        "StorageCapacity": 1200,
        "StorageType": "SSD",
        "SubnetIds": ["subnet-1"],
        "DNSName": "fs.example.com",
        "ResourceARN": "arn:...",
        "Tags": [{"Key": "env", "Value": "test"}],
    }
    d.update(overrides)
    return d


def _backup_dict(**overrides):
    d = {
        "BackupId": BK_ID,
        "Lifecycle": "AVAILABLE",
        "Type": "USER_INITIATED",
        "FileSystem": {"FileSystemId": FS_ID},
        "ResourceARN": "arn:...",
        "Tags": [],
    }
    d.update(overrides)
    return d


def _volume_dict(**overrides):
    d = {
        "VolumeId": VOL_ID,
        "Name": "vol1",
        "Lifecycle": "AVAILABLE",
        "VolumeType": "ONTAP",
        "FileSystemId": FS_ID,
        "ResourceARN": "arn:...",
        "Tags": [],
    }
    d.update(overrides)
    return d


def _dra_dict(**overrides):
    d = {
        "AssociationId": DRA_ID,
        "FileSystemId": FS_ID,
        "FileSystemPath": "/data",
        "DataRepositoryPath": "s3://bucket/path",
        "Lifecycle": "AVAILABLE",
        "ResourceARN": "arn:...",
        "Tags": [],
    }
    d.update(overrides)
    return d


def _drt_dict(**overrides):
    d = {
        "TaskId": DRT_ID,
        "Lifecycle": "SUCCEEDED",
        "Type": "EXPORT_TO_REPOSITORY",
        "FileSystemId": FS_ID,
        "ResourceARN": "arn:...",
        "Tags": [],
    }
    d.update(overrides)
    return d


def _alias_dict(**overrides):
    d = {"Name": "fsx.example.com", "Lifecycle": "AVAILABLE"}
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# File-system operations
# ---------------------------------------------------------------------------


async def test_create_file_system_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystem": _fs_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await create_file_system(
        file_system_type="LUSTRE", storage_capacity=1200,
        subnet_ids=["subnet-1"], storage_type="SSD",
        security_group_ids=["sg-1"],
        tags={"env": "test"},
        extra_params={"LustreConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


async def test_create_file_system_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_file_system(
            file_system_type="LUSTRE", storage_capacity=1200,
            subnet_ids=["subnet-1"], region_name=REGION,
        )


async def test_describe_file_systems_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystems": [_fs_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_file_systems(
        file_system_ids=[FS_ID], region_name=REGION,
    )
    assert len(result) == 1


async def test_describe_file_systems_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"FileSystems": [_fs_dict()], "NextToken": "tok"},
        {"FileSystems": [_fs_dict(FileSystemId="fs-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_file_systems(region_name=REGION)
    assert len(result) == 2


async def test_describe_file_systems_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_file_systems(region_name=REGION)


async def test_update_file_system_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystem": _fs_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await update_file_system(
        FS_ID, storage_capacity=2400,
        extra_params={"LustreConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


async def test_update_file_system_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await update_file_system(FS_ID, region_name=REGION)


async def test_delete_file_system_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystemId": FS_ID}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await delete_file_system(
        FS_ID, extra_params={"WindowsConfiguration": {}}, region_name=REGION,
    )
    assert result["FileSystemId"] == FS_ID


async def test_delete_file_system_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_file_system(FS_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Backup operations
# ---------------------------------------------------------------------------


async def test_create_backup_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Backup": _backup_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await create_backup(
        file_system_id=FS_ID, volume_id=VOL_ID,
        tags={"env": "test"}, region_name=REGION,
    )
    assert result.backup_id == BK_ID


async def test_create_backup_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_backup(region_name=REGION)


async def test_describe_backups_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Backups": [_backup_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_backups(
        backup_ids=[BK_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


async def test_describe_backups_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Backups": [_backup_dict()], "NextToken": "tok"},
        {"Backups": [_backup_dict(BackupId="bk-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_backups(region_name=REGION)
    assert len(result) == 2


async def test_describe_backups_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_backups(region_name=REGION)


async def test_delete_backup_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"BackupId": BK_ID}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await delete_backup(BK_ID, region_name=REGION)
    assert result["BackupId"] == BK_ID


async def test_delete_backup_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_backup(BK_ID, region_name=REGION)


async def test_copy_backup_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Backup": _backup_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await copy_backup(
        BK_ID, source_region="us-west-2", tags={"env": "test"},
        region_name=REGION,
    )
    assert result.backup_id == BK_ID


async def test_copy_backup_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await copy_backup(BK_ID, region_name=REGION)


async def test_restore_file_system_from_backup_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystem": _fs_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await restore_file_system_from_backup(
        BK_ID, subnet_ids=["subnet-1"],
        security_group_ids=["sg-1"],
        tags={"env": "test"},
        extra_params={"WindowsConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


async def test_restore_file_system_from_backup_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await restore_file_system_from_backup(
            BK_ID, subnet_ids=["subnet-1"], region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Alias operations
# ---------------------------------------------------------------------------


async def test_describe_file_system_aliases_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Aliases": [_alias_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_file_system_aliases(FS_ID, region_name=REGION)
    assert len(result) == 1


async def test_describe_file_system_aliases_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Aliases": [_alias_dict()], "NextToken": "tok"},
        {"Aliases": [_alias_dict(Name="fsx2.example.com")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_file_system_aliases(FS_ID, region_name=REGION)
    assert len(result) == 2


async def test_describe_file_system_aliases_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_file_system_aliases(FS_ID, region_name=REGION)


async def test_associate_file_system_aliases_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Aliases": [_alias_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await associate_file_system_aliases(
        FS_ID, aliases=["fsx.example.com"], region_name=REGION,
    )
    assert len(result) == 1


async def test_associate_file_system_aliases_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await associate_file_system_aliases(
            FS_ID, aliases=["fsx.example.com"], region_name=REGION,
        )


async def test_disassociate_file_system_aliases_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Aliases": [_alias_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await disassociate_file_system_aliases(
        FS_ID, aliases=["fsx.example.com"], region_name=REGION,
    )
    assert len(result) == 1


async def test_disassociate_file_system_aliases_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await disassociate_file_system_aliases(
            FS_ID, aliases=["fsx.example.com"], region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Volume operations
# ---------------------------------------------------------------------------


async def test_create_volume_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Volume": _volume_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await create_volume(
        volume_type="ONTAP", name="vol1",
        extra_params={"OntapConfiguration": {}},
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.volume_id == VOL_ID


async def test_create_volume_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_volume(volume_type="ONTAP", name="vol1", region_name=REGION)


async def test_describe_volumes_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Volumes": [_volume_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_volumes(
        volume_ids=[VOL_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


async def test_describe_volumes_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Volumes": [_volume_dict()], "NextToken": "tok"},
        {"Volumes": [_volume_dict(VolumeId="fsvol-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_volumes(region_name=REGION)
    assert len(result) == 2


async def test_describe_volumes_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_volumes(region_name=REGION)


async def test_update_volume_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Volume": _volume_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await update_volume(
        VOL_ID, name="new-name",
        extra_params={"OntapConfiguration": {}},
        region_name=REGION,
    )
    assert result.volume_id == VOL_ID


async def test_update_volume_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await update_volume(VOL_ID, region_name=REGION)


async def test_delete_volume_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"VolumeId": VOL_ID}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await delete_volume(
        VOL_ID, extra_params={"OntapConfiguration": {}}, region_name=REGION,
    )
    assert result["VolumeId"] == VOL_ID


async def test_delete_volume_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_volume(VOL_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Data-repository association operations
# ---------------------------------------------------------------------------


async def test_create_data_repository_association_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Association": _dra_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await create_data_repository_association(
        FS_ID, file_system_path="/data",
        data_repository_path="s3://bucket/path",
        batch_import_meta_data_on_create=True,
        imported_file_chunk_size=1024,
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.association_id == DRA_ID


async def test_create_data_repository_association_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_data_repository_association(
            FS_ID, file_system_path="/data",
            data_repository_path="s3://bucket", region_name=REGION,
        )


async def test_describe_data_repository_associations_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Associations": [_dra_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_data_repository_associations(
        association_ids=[DRA_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


async def test_describe_data_repository_associations_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"Associations": [_dra_dict()], "NextToken": "tok"},
        {"Associations": [_dra_dict(AssociationId="dra-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_data_repository_associations(region_name=REGION)
    assert len(result) == 2


async def test_describe_data_repository_associations_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_data_repository_associations(region_name=REGION)


# ---------------------------------------------------------------------------
# Data-repository task operations
# ---------------------------------------------------------------------------


async def test_create_data_repository_task_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DataRepositoryTask": _drt_dict()}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await create_data_repository_task(
        FS_ID, task_type="EXPORT_TO_REPOSITORY",
        report={"Enabled": True},
        paths=["/data"],
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.task_id == DRT_ID


async def test_create_data_repository_task_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_data_repository_task(
            FS_ID, task_type="EXPORT_TO_REPOSITORY",
            report={"Enabled": True}, region_name=REGION,
        )


async def test_describe_data_repository_tasks_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DataRepositoryTasks": [_drt_dict()]}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_data_repository_tasks(
        task_ids=[DRT_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


async def test_describe_data_repository_tasks_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"DataRepositoryTasks": [_drt_dict()], "NextToken": "tok"},
        {"DataRepositoryTasks": [_drt_dict(TaskId="task-other")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await describe_data_repository_tasks(region_name=REGION)
    assert len(result) == 2


async def test_describe_data_repository_tasks_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_data_repository_tasks(region_name=REGION)


async def test_cancel_data_repository_task_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"TaskId": DRT_ID}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await cancel_data_repository_task(DRT_ID, region_name=REGION)
    assert result["TaskId"] == DRT_ID


async def test_cancel_data_repository_task_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await cancel_data_repository_task(DRT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


async def test_wait_for_file_system_immediate(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "FileSystems": [_fs_dict(Lifecycle="AVAILABLE")],
    }
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    result = await wait_for_file_system(FS_ID, timeout=5, region_name=REGION)
    assert result.lifecycle == "AVAILABLE"


async def test_wait_for_file_system_not_found(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"FileSystems": []}
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_file_system(FS_ID, timeout=5, region_name=REGION)


async def test_wait_for_file_system_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "FileSystems": [_fs_dict(Lifecycle="CREATING")],
    }
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(_time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_file_system(
            FS_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_file_system_poll_then_ready(monkeypatch):
    """Cover the sleep branch: first poll CREATING, second AVAILABLE."""
    client = AsyncMock()
    client.call.side_effect = [
        {"FileSystems": [_fs_dict(Lifecycle="CREATING")]},
        {"FileSystems": [_fs_dict(Lifecycle="AVAILABLE")]},
    ]
    monkeypatch.setattr("aws_util.aio.fsx.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    result = await wait_for_file_system(
        FS_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert result.lifecycle == "AVAILABLE"


async def test_copy_snapshot_and_update_volume(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", )
    mock_client.call.assert_called_once()


async def test_copy_snapshot_and_update_volume_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", )


async def test_create_and_attach_s3_access_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_and_attach_s3_access_point("test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_and_attach_s3_access_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_and_attach_s3_access_point("test-name", "test-type_value", )


async def test_create_file_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_file_cache("test-file_cache_type", "test-file_cache_type_version", 1, [], )
    mock_client.call.assert_called_once()


async def test_create_file_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_file_cache("test-file_cache_type", "test-file_cache_type_version", 1, [], )


async def test_create_file_system_from_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_file_system_from_backup("test-backup_id", [], )
    mock_client.call.assert_called_once()


async def test_create_file_system_from_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_file_system_from_backup("test-backup_id", [], )


async def test_create_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_snapshot("test-name", "test-volume_id", )
    mock_client.call.assert_called_once()


async def test_create_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot("test-name", "test-volume_id", )


async def test_create_storage_virtual_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_storage_virtual_machine("test-file_system_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_storage_virtual_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_storage_virtual_machine("test-file_system_id", "test-name", )


async def test_create_volume_from_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_volume_from_backup("test-backup_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_volume_from_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_volume_from_backup("test-backup_id", "test-name", )


async def test_delete_data_repository_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_data_repository_association("test-association_id", )
    mock_client.call.assert_called_once()


async def test_delete_data_repository_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_repository_association("test-association_id", )


async def test_delete_file_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_file_cache("test-file_cache_id", )
    mock_client.call.assert_called_once()


async def test_delete_file_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_file_cache("test-file_cache_id", )


async def test_delete_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_snapshot("test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_delete_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot("test-snapshot_id", )


async def test_delete_storage_virtual_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_storage_virtual_machine("test-storage_virtual_machine_id", )
    mock_client.call.assert_called_once()


async def test_delete_storage_virtual_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_storage_virtual_machine("test-storage_virtual_machine_id", )


async def test_describe_file_caches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_file_caches()
    mock_client.call.assert_called_once()


async def test_describe_file_caches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_file_caches()


async def test_describe_s3_access_point_attachments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_s3_access_point_attachments()
    mock_client.call.assert_called_once()


async def test_describe_s3_access_point_attachments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_s3_access_point_attachments()


async def test_describe_shared_vpc_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_shared_vpc_configuration()
    mock_client.call.assert_called_once()


async def test_describe_shared_vpc_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_shared_vpc_configuration()


async def test_describe_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_snapshots()
    mock_client.call.assert_called_once()


async def test_describe_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshots()


async def test_describe_storage_virtual_machines(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_storage_virtual_machines()
    mock_client.call.assert_called_once()


async def test_describe_storage_virtual_machines_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_storage_virtual_machines()


async def test_detach_and_delete_s3_access_point(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_and_delete_s3_access_point("test-name", )
    mock_client.call.assert_called_once()


async def test_detach_and_delete_s3_access_point_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_and_delete_s3_access_point("test-name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_release_file_system_nfs_v3_locks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await release_file_system_nfs_v3_locks("test-file_system_id", )
    mock_client.call.assert_called_once()


async def test_release_file_system_nfs_v3_locks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await release_file_system_nfs_v3_locks("test-file_system_id", )


async def test_restore_volume_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_restore_volume_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", )


async def test_start_misconfigured_state_recovery(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_misconfigured_state_recovery("test-file_system_id", )
    mock_client.call.assert_called_once()


async def test_start_misconfigured_state_recovery_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_misconfigured_state_recovery("test-file_system_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_data_repository_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_data_repository_association("test-association_id", )
    mock_client.call.assert_called_once()


async def test_update_data_repository_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_repository_association("test-association_id", )


async def test_update_file_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_file_cache("test-file_cache_id", )
    mock_client.call.assert_called_once()


async def test_update_file_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_file_cache("test-file_cache_id", )


async def test_update_shared_vpc_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_shared_vpc_configuration()
    mock_client.call.assert_called_once()


async def test_update_shared_vpc_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_shared_vpc_configuration()


async def test_update_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_snapshot("test-name", "test-snapshot_id", )
    mock_client.call.assert_called_once()


async def test_update_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_snapshot("test-name", "test-snapshot_id", )


async def test_update_storage_virtual_machine(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_storage_virtual_machine("test-storage_virtual_machine_id", )
    mock_client.call.assert_called_once()


async def test_update_storage_virtual_machine_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.fsx.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_storage_virtual_machine("test-storage_virtual_machine_id", )


@pytest.mark.asyncio
async def test_copy_snapshot_and_update_volume_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import copy_snapshot_and_update_volume
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", client_request_token="test-client_request_token", copy_strategy="test-copy_strategy", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_and_attach_s3_access_point_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_and_attach_s3_access_point
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_and_attach_s3_access_point("test-name", "test-type_value", client_request_token="test-client_request_token", open_zfs_configuration={}, s3_access_point="test-s3_access_point", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_file_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_file_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_file_cache("test-file_cache_type", "test-file_cache_type_version", "test-storage_capacity", "test-subnet_ids", client_request_token="test-client_request_token", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], copy_tags_to_data_repository_associations=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", lustre_configuration={}, data_repository_associations="test-data_repository_associations", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_file_system_from_backup_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_file_system_from_backup
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_file_system_from_backup("test-backup_id", "test-subnet_ids", client_request_token="test-client_request_token", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], windows_configuration={}, lustre_configuration={}, storage_type="test-storage_type", kms_key_id="test-kms_key_id", file_system_type_version="test-file_system_type_version", open_zfs_configuration={}, storage_capacity="test-storage_capacity", network_type="test-network_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_snapshot("test-name", "test-volume_id", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_storage_virtual_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_storage_virtual_machine("test-file_system_id", "test-name", active_directory_configuration={}, client_request_token="test-client_request_token", svm_admin_password="test-svm_admin_password", tags=[{"Key": "k", "Value": "v"}], root_volume_security_style="test-root_volume_security_style", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_volume_from_backup_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import create_volume_from_backup
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await create_volume_from_backup("test-backup_id", "test-name", client_request_token="test-client_request_token", ontap_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_data_repository_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import delete_data_repository_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await delete_data_repository_association("test-association_id", client_request_token="test-client_request_token", delete_data_in_file_system=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_file_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import delete_file_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await delete_file_cache("test-file_cache_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import delete_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await delete_snapshot("test-snapshot_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import delete_storage_virtual_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await delete_storage_virtual_machine("test-storage_virtual_machine_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_file_caches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import describe_file_caches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await describe_file_caches(file_cache_ids="test-file_cache_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_s3_access_point_attachments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import describe_s3_access_point_attachments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await describe_s3_access_point_attachments(names="test-names", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import describe_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await describe_snapshots(snapshot_ids="test-snapshot_ids", filters=[{}], max_results=1, next_token="test-next_token", include_shared=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_storage_virtual_machines_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import describe_storage_virtual_machines
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await describe_storage_virtual_machines(storage_virtual_machine_ids="test-storage_virtual_machine_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_detach_and_delete_s3_access_point_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import detach_and_delete_s3_access_point
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await detach_and_delete_s3_access_point("test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_release_file_system_nfs_v3_locks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import release_file_system_nfs_v3_locks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await release_file_system_nfs_v3_locks("test-file_system_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_volume_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import restore_volume_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", client_request_token="test-client_request_token", options={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_misconfigured_state_recovery_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import start_misconfigured_state_recovery
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await start_misconfigured_state_recovery("test-file_system_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_repository_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import update_data_repository_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await update_data_repository_association("test-association_id", client_request_token="test-client_request_token", imported_file_chunk_size=1, s3="test-s3", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_file_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import update_file_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await update_file_cache("test-file_cache_id", client_request_token="test-client_request_token", lustre_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_shared_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import update_shared_vpc_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await update_shared_vpc_configuration(enable_fsx_route_table_updates_from_participant_accounts=True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import update_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await update_snapshot("test-name", "test-snapshot_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.fsx import update_storage_virtual_machine
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.fsx.async_client", lambda *a, **kw: mock_client)
    await update_storage_virtual_machine("test-storage_virtual_machine_id", active_directory_configuration={}, client_request_token="test-client_request_token", svm_admin_password="test-svm_admin_password", region_name="us-east-1")
    mock_client.call.assert_called_once()
