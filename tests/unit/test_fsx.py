"""Tests for aws_util.fsx module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.fsx as fsx_mod
from aws_util.fsx import (
    BackupResult,
    DataRepositoryAssociationResult,
    DataRepositoryTaskResult,
    FileSystemAliasResult,
    FileSystemResult,
    VolumeResult,
    _dict_to_tags,
    _parse_alias,
    _parse_backup,
    _parse_data_repository_association,
    _parse_data_repository_task,
    _parse_file_system,
    _parse_volume,
    _tags_to_dict,
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


def _client_error(code: str = "ServiceException", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


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
# Helper tests
# ---------------------------------------------------------------------------


def test_tags_to_dict():
    assert _tags_to_dict([{"Key": "a", "Value": "1"}]) == {"a": "1"}


def test_dict_to_tags():
    assert _dict_to_tags({"a": "1"}) == [{"Key": "a", "Value": "1"}]


def test_parse_file_system():
    result = _parse_file_system(_fs_dict())
    assert result.file_system_id == FS_ID
    assert result.tags == {"env": "test"}


def test_parse_backup():
    result = _parse_backup(_backup_dict())
    assert result.backup_id == BK_ID


def test_parse_volume():
    result = _parse_volume(_volume_dict())
    assert result.volume_id == VOL_ID


def test_parse_data_repository_association():
    result = _parse_data_repository_association(_dra_dict())
    assert result.association_id == DRA_ID


def test_parse_data_repository_task():
    result = _parse_data_repository_task(_drt_dict())
    assert result.task_id == DRT_ID


def test_parse_alias():
    result = _parse_alias(_alias_dict())
    assert result.name == "fsx.example.com"


# ---------------------------------------------------------------------------
# File-system operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_create_file_system_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_file_system.return_value = {"FileSystem": _fs_dict()}
    result = create_file_system(
        file_system_type="LUSTRE", storage_capacity=1200,
        subnet_ids=["subnet-1"], storage_type="SSD",
        security_group_ids=["sg-1"],
        tags={"env": "test"},
        extra_params={"LustreConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


@patch("aws_util.fsx.get_client")
def test_create_file_system_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_file_system.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_file_system(
            file_system_type="LUSTRE", storage_capacity=1200,
            subnet_ids=["subnet-1"], region_name=REGION,
        )


@patch("aws_util.fsx.get_client")
def test_describe_file_systems_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.return_value = {
        "FileSystems": [_fs_dict()],
    }
    result = describe_file_systems(
        file_system_ids=[FS_ID], region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_file_systems_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.side_effect = [
        {"FileSystems": [_fs_dict()], "NextToken": "tok"},
        {"FileSystems": [_fs_dict(FileSystemId="fs-other")]},
    ]
    result = describe_file_systems(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_file_systems_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_file_systems(region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_update_file_system_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_file_system.return_value = {"FileSystem": _fs_dict()}
    result = update_file_system(
        FS_ID, storage_capacity=2400,
        extra_params={"LustreConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


@patch("aws_util.fsx.get_client")
def test_update_file_system_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_file_system.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_file_system(FS_ID, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_delete_file_system_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_file_system.return_value = {"FileSystemId": FS_ID}
    result = delete_file_system(
        FS_ID, extra_params={"WindowsConfiguration": {}}, region_name=REGION,
    )
    assert result["FileSystemId"] == FS_ID


@patch("aws_util.fsx.get_client")
def test_delete_file_system_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_file_system.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_file_system(FS_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Backup operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_create_backup_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_backup.return_value = {"Backup": _backup_dict()}
    result = create_backup(
        file_system_id=FS_ID, volume_id=VOL_ID,
        tags={"env": "test"}, region_name=REGION,
    )
    assert result.backup_id == BK_ID


@patch("aws_util.fsx.get_client")
def test_create_backup_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_backup.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_backup(region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_describe_backups_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_backups.return_value = {"Backups": [_backup_dict()]}
    result = describe_backups(
        backup_ids=[BK_ID], filters=[{"Name": "file-system-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_backups_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_backups.side_effect = [
        {"Backups": [_backup_dict()], "NextToken": "tok"},
        {"Backups": [_backup_dict(BackupId="backup-other")]},
    ]
    result = describe_backups(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_backups_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_backups.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_backups(region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_delete_backup_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_backup.return_value = {"BackupId": BK_ID}
    result = delete_backup(BK_ID, region_name=REGION)
    assert result["BackupId"] == BK_ID


@patch("aws_util.fsx.get_client")
def test_delete_backup_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_backup.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_backup(BK_ID, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_copy_backup_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.copy_backup.return_value = {"Backup": _backup_dict()}
    result = copy_backup(
        BK_ID, source_region="us-west-2", tags={"env": "test"},
        region_name=REGION,
    )
    assert result.backup_id == BK_ID


@patch("aws_util.fsx.get_client")
def test_copy_backup_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.copy_backup.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        copy_backup(BK_ID, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_restore_file_system_from_backup_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_file_system_from_backup.return_value = {
        "FileSystem": _fs_dict(),
    }
    result = restore_file_system_from_backup(
        BK_ID, subnet_ids=["subnet-1"],
        security_group_ids=["sg-1"],
        tags={"env": "test"},
        extra_params={"WindowsConfiguration": {}},
        region_name=REGION,
    )
    assert result.file_system_id == FS_ID


@patch("aws_util.fsx.get_client")
def test_restore_file_system_from_backup_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_file_system_from_backup.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        restore_file_system_from_backup(
            BK_ID, subnet_ids=["subnet-1"], region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Alias operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_describe_file_system_aliases_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_system_aliases.return_value = {
        "Aliases": [_alias_dict()],
    }
    result = describe_file_system_aliases(FS_ID, region_name=REGION)
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_file_system_aliases_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_system_aliases.side_effect = [
        {"Aliases": [_alias_dict()], "NextToken": "tok"},
        {"Aliases": [_alias_dict(Name="fsx2.example.com")]},
    ]
    result = describe_file_system_aliases(FS_ID, region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_file_system_aliases_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_system_aliases.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_file_system_aliases(FS_ID, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_associate_file_system_aliases_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.associate_file_system_aliases.return_value = {
        "Aliases": [_alias_dict()],
    }
    result = associate_file_system_aliases(
        FS_ID, aliases=["fsx.example.com"], region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_associate_file_system_aliases_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.associate_file_system_aliases.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        associate_file_system_aliases(
            FS_ID, aliases=["fsx.example.com"], region_name=REGION,
        )


@patch("aws_util.fsx.get_client")
def test_disassociate_file_system_aliases_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.disassociate_file_system_aliases.return_value = {
        "Aliases": [_alias_dict()],
    }
    result = disassociate_file_system_aliases(
        FS_ID, aliases=["fsx.example.com"], region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_disassociate_file_system_aliases_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.disassociate_file_system_aliases.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        disassociate_file_system_aliases(
            FS_ID, aliases=["fsx.example.com"], region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Volume operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_create_volume_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_volume.return_value = {"Volume": _volume_dict()}
    result = create_volume(
        volume_type="ONTAP", name="vol1",
        extra_params={"OntapConfiguration": {}},
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.volume_id == VOL_ID


@patch("aws_util.fsx.get_client")
def test_create_volume_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_volume.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_volume(volume_type="ONTAP", name="vol1", region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_describe_volumes_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_volumes.return_value = {"Volumes": [_volume_dict()]}
    result = describe_volumes(
        volume_ids=[VOL_ID], filters=[{"Name": "file-system-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_volumes_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_volumes.side_effect = [
        {"Volumes": [_volume_dict()], "NextToken": "tok"},
        {"Volumes": [_volume_dict(VolumeId="fsvol-other")]},
    ]
    result = describe_volumes(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_volumes_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_volumes.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_volumes(region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_update_volume_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_volume.return_value = {"Volume": _volume_dict()}
    result = update_volume(
        VOL_ID, name="new-name",
        extra_params={"OntapConfiguration": {}},
        region_name=REGION,
    )
    assert result.volume_id == VOL_ID


@patch("aws_util.fsx.get_client")
def test_update_volume_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_volume.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_volume(VOL_ID, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_delete_volume_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_volume.return_value = {"VolumeId": VOL_ID}
    result = delete_volume(
        VOL_ID, extra_params={"OntapConfiguration": {}}, region_name=REGION,
    )
    assert result["VolumeId"] == VOL_ID


@patch("aws_util.fsx.get_client")
def test_delete_volume_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_volume.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_volume(VOL_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Data-repository association operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_create_data_repository_association_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_data_repository_association.return_value = {
        "Association": _dra_dict(),
    }
    result = create_data_repository_association(
        FS_ID, file_system_path="/data",
        data_repository_path="s3://bucket/path",
        batch_import_meta_data_on_create=True,
        imported_file_chunk_size=1024,
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.association_id == DRA_ID


@patch("aws_util.fsx.get_client")
def test_create_data_repository_association_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_data_repository_association.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_data_repository_association(
            FS_ID, file_system_path="/data",
            data_repository_path="s3://bucket", region_name=REGION,
        )


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_associations_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_associations.return_value = {
        "Associations": [_dra_dict()],
    }
    result = describe_data_repository_associations(
        association_ids=[DRA_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_associations_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_associations.side_effect = [
        {"Associations": [_dra_dict()], "NextToken": "tok"},
        {"Associations": [_dra_dict(AssociationId="dra-other")]},
    ]
    result = describe_data_repository_associations(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_associations_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_associations.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_data_repository_associations(region_name=REGION)


# ---------------------------------------------------------------------------
# Data-repository task operations
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_create_data_repository_task_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_data_repository_task.return_value = {
        "DataRepositoryTask": _drt_dict(),
    }
    result = create_data_repository_task(
        FS_ID, task_type="EXPORT_TO_REPOSITORY",
        report={"Enabled": True},
        paths=["/data"],
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.task_id == DRT_ID


@patch("aws_util.fsx.get_client")
def test_create_data_repository_task_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_data_repository_task.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_data_repository_task(
            FS_ID, task_type="EXPORT_TO_REPOSITORY",
            report={"Enabled": True}, region_name=REGION,
        )


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_tasks_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_tasks.return_value = {
        "DataRepositoryTasks": [_drt_dict()],
    }
    result = describe_data_repository_tasks(
        task_ids=[DRT_ID], filters=[{"Name": "fs-id"}],
        region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_tasks_pagination(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_tasks.side_effect = [
        {"DataRepositoryTasks": [_drt_dict()], "NextToken": "tok"},
        {"DataRepositoryTasks": [_drt_dict(TaskId="task-other")]},
    ]
    result = describe_data_repository_tasks(region_name=REGION)
    assert len(result) == 2


@patch("aws_util.fsx.get_client")
def test_describe_data_repository_tasks_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_data_repository_tasks.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_data_repository_tasks(region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_cancel_data_repository_task_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_data_repository_task.return_value = {"TaskId": DRT_ID}
    result = cancel_data_repository_task(DRT_ID, region_name=REGION)
    assert result["TaskId"] == DRT_ID


@patch("aws_util.fsx.get_client")
def test_cancel_data_repository_task_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_data_repository_task.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        cancel_data_repository_task(DRT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


@patch("aws_util.fsx.get_client")
def test_wait_for_file_system_immediate(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.return_value = {
        "FileSystems": [_fs_dict(Lifecycle="AVAILABLE")],
    }
    result = wait_for_file_system(FS_ID, timeout=5, region_name=REGION)
    assert result.lifecycle == "AVAILABLE"


@patch("aws_util.fsx.get_client")
def test_wait_for_file_system_not_found(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.return_value = {"FileSystems": []}
    with pytest.raises(RuntimeError, match="not found"):
        wait_for_file_system(FS_ID, timeout=5, region_name=REGION)


@patch("aws_util.fsx.get_client")
def test_wait_for_file_system_timeout(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.return_value = {
        "FileSystems": [_fs_dict(Lifecycle="CREATING")],
    }
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    with patch.object(time, "monotonic", _mono), \
         patch.object(time, "sleep"):
        with pytest.raises(AwsTimeoutError):
            wait_for_file_system(
                FS_ID, timeout=1, poll_interval=0.1, region_name=REGION,
            )


@patch("aws_util.fsx.get_client")
def test_wait_for_file_system_poll_then_ready(mock_gc):
    """Cover the sleep branch: first poll CREATING, second AVAILABLE."""
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_file_systems.side_effect = [
        {"FileSystems": [_fs_dict(Lifecycle="CREATING")]},
        {"FileSystems": [_fs_dict(Lifecycle="AVAILABLE")]},
    ]
    with patch.object(time, "sleep"):
        result = wait_for_file_system(
            FS_ID, timeout=600, poll_interval=1.0, region_name=REGION,
        )
    assert result.lifecycle == "AVAILABLE"


def test_copy_snapshot_and_update_volume(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot_and_update_volume.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", region_name=REGION)
    mock_client.copy_snapshot_and_update_volume.assert_called_once()


def test_copy_snapshot_and_update_volume_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot_and_update_volume.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_snapshot_and_update_volume",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy snapshot and update volume"):
        copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", region_name=REGION)


def test_create_and_attach_s3_access_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_and_attach_s3_access_point.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_and_attach_s3_access_point("test-name", "test-type_value", region_name=REGION)
    mock_client.create_and_attach_s3_access_point.assert_called_once()


def test_create_and_attach_s3_access_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_and_attach_s3_access_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_and_attach_s3_access_point",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create and attach s3 access point"):
        create_and_attach_s3_access_point("test-name", "test-type_value", region_name=REGION)


def test_create_file_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_file_cache.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_file_cache("test-file_cache_type", "test-file_cache_type_version", 1, [], region_name=REGION)
    mock_client.create_file_cache.assert_called_once()


def test_create_file_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_file_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_file_cache",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create file cache"):
        create_file_cache("test-file_cache_type", "test-file_cache_type_version", 1, [], region_name=REGION)


def test_create_file_system_from_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_file_system_from_backup.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_file_system_from_backup("test-backup_id", [], region_name=REGION)
    mock_client.create_file_system_from_backup.assert_called_once()


def test_create_file_system_from_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_file_system_from_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_file_system_from_backup",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create file system from backup"):
        create_file_system_from_backup("test-backup_id", [], region_name=REGION)


def test_create_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-name", "test-volume_id", region_name=REGION)
    mock_client.create_snapshot.assert_called_once()


def test_create_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        create_snapshot("test-name", "test-volume_id", region_name=REGION)


def test_create_storage_virtual_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_storage_virtual_machine.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_storage_virtual_machine("test-file_system_id", "test-name", region_name=REGION)
    mock_client.create_storage_virtual_machine.assert_called_once()


def test_create_storage_virtual_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_storage_virtual_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_storage_virtual_machine",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create storage virtual machine"):
        create_storage_virtual_machine("test-file_system_id", "test-name", region_name=REGION)


def test_create_volume_from_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_volume_from_backup.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    create_volume_from_backup("test-backup_id", "test-name", region_name=REGION)
    mock_client.create_volume_from_backup.assert_called_once()


def test_create_volume_from_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_volume_from_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_volume_from_backup",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create volume from backup"):
        create_volume_from_backup("test-backup_id", "test-name", region_name=REGION)


def test_delete_data_repository_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_repository_association.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    delete_data_repository_association("test-association_id", region_name=REGION)
    mock_client.delete_data_repository_association.assert_called_once()


def test_delete_data_repository_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_repository_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_repository_association",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data repository association"):
        delete_data_repository_association("test-association_id", region_name=REGION)


def test_delete_file_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_file_cache.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    delete_file_cache("test-file_cache_id", region_name=REGION)
    mock_client.delete_file_cache.assert_called_once()


def test_delete_file_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_file_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_file_cache",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete file cache"):
        delete_file_cache("test-file_cache_id", region_name=REGION)


def test_delete_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    delete_snapshot("test-snapshot_id", region_name=REGION)
    mock_client.delete_snapshot.assert_called_once()


def test_delete_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        delete_snapshot("test-snapshot_id", region_name=REGION)


def test_delete_storage_virtual_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_storage_virtual_machine.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    delete_storage_virtual_machine("test-storage_virtual_machine_id", region_name=REGION)
    mock_client.delete_storage_virtual_machine.assert_called_once()


def test_delete_storage_virtual_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_storage_virtual_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_storage_virtual_machine",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete storage virtual machine"):
        delete_storage_virtual_machine("test-storage_virtual_machine_id", region_name=REGION)


def test_describe_file_caches(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_file_caches.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    describe_file_caches(region_name=REGION)
    mock_client.describe_file_caches.assert_called_once()


def test_describe_file_caches_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_file_caches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_file_caches",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe file caches"):
        describe_file_caches(region_name=REGION)


def test_describe_s3_access_point_attachments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_s3_access_point_attachments.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    describe_s3_access_point_attachments(region_name=REGION)
    mock_client.describe_s3_access_point_attachments.assert_called_once()


def test_describe_s3_access_point_attachments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_s3_access_point_attachments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_s3_access_point_attachments",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe s3 access point attachments"):
        describe_s3_access_point_attachments(region_name=REGION)


def test_describe_shared_vpc_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_shared_vpc_configuration.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    describe_shared_vpc_configuration(region_name=REGION)
    mock_client.describe_shared_vpc_configuration.assert_called_once()


def test_describe_shared_vpc_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_shared_vpc_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_shared_vpc_configuration",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe shared vpc configuration"):
        describe_shared_vpc_configuration(region_name=REGION)


def test_describe_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshots.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    describe_snapshots(region_name=REGION)
    mock_client.describe_snapshots.assert_called_once()


def test_describe_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshots",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshots"):
        describe_snapshots(region_name=REGION)


def test_describe_storage_virtual_machines(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_storage_virtual_machines.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    describe_storage_virtual_machines(region_name=REGION)
    mock_client.describe_storage_virtual_machines.assert_called_once()


def test_describe_storage_virtual_machines_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_storage_virtual_machines.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_storage_virtual_machines",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe storage virtual machines"):
        describe_storage_virtual_machines(region_name=REGION)


def test_detach_and_delete_s3_access_point(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_and_delete_s3_access_point.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    detach_and_delete_s3_access_point("test-name", region_name=REGION)
    mock_client.detach_and_delete_s3_access_point.assert_called_once()


def test_detach_and_delete_s3_access_point_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_and_delete_s3_access_point.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_and_delete_s3_access_point",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach and delete s3 access point"):
        detach_and_delete_s3_access_point("test-name", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_release_file_system_nfs_v3_locks(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_file_system_nfs_v3_locks.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    release_file_system_nfs_v3_locks("test-file_system_id", region_name=REGION)
    mock_client.release_file_system_nfs_v3_locks.assert_called_once()


def test_release_file_system_nfs_v3_locks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_file_system_nfs_v3_locks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "release_file_system_nfs_v3_locks",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to release file system nfs v3 locks"):
        release_file_system_nfs_v3_locks("test-file_system_id", region_name=REGION)


def test_restore_volume_from_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_volume_from_snapshot.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", region_name=REGION)
    mock_client.restore_volume_from_snapshot.assert_called_once()


def test_restore_volume_from_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_volume_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_volume_from_snapshot",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore volume from snapshot"):
        restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", region_name=REGION)


def test_start_misconfigured_state_recovery(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_misconfigured_state_recovery.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    start_misconfigured_state_recovery("test-file_system_id", region_name=REGION)
    mock_client.start_misconfigured_state_recovery.assert_called_once()


def test_start_misconfigured_state_recovery_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_misconfigured_state_recovery.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_misconfigured_state_recovery",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start misconfigured state recovery"):
        start_misconfigured_state_recovery("test-file_system_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_data_repository_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_repository_association.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    update_data_repository_association("test-association_id", region_name=REGION)
    mock_client.update_data_repository_association.assert_called_once()


def test_update_data_repository_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_repository_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_repository_association",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data repository association"):
        update_data_repository_association("test-association_id", region_name=REGION)


def test_update_file_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_cache.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    update_file_cache("test-file_cache_id", region_name=REGION)
    mock_client.update_file_cache.assert_called_once()


def test_update_file_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_file_cache",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update file cache"):
        update_file_cache("test-file_cache_id", region_name=REGION)


def test_update_shared_vpc_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_shared_vpc_configuration.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    update_shared_vpc_configuration(region_name=REGION)
    mock_client.update_shared_vpc_configuration.assert_called_once()


def test_update_shared_vpc_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_shared_vpc_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_shared_vpc_configuration",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update shared vpc configuration"):
        update_shared_vpc_configuration(region_name=REGION)


def test_update_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    update_snapshot("test-name", "test-snapshot_id", region_name=REGION)
    mock_client.update_snapshot.assert_called_once()


def test_update_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_snapshot",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update snapshot"):
        update_snapshot("test-name", "test-snapshot_id", region_name=REGION)


def test_update_storage_virtual_machine(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_storage_virtual_machine.return_value = {}
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    update_storage_virtual_machine("test-storage_virtual_machine_id", region_name=REGION)
    mock_client.update_storage_virtual_machine.assert_called_once()


def test_update_storage_virtual_machine_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_storage_virtual_machine.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_storage_virtual_machine",
    )
    monkeypatch.setattr(fsx_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update storage virtual machine"):
        update_storage_virtual_machine("test-storage_virtual_machine_id", region_name=REGION)


def test_copy_snapshot_and_update_volume_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import copy_snapshot_and_update_volume
    mock_client = MagicMock()
    mock_client.copy_snapshot_and_update_volume.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    copy_snapshot_and_update_volume("test-volume_id", "test-source_snapshot_arn", client_request_token="test-client_request_token", copy_strategy="test-copy_strategy", options={}, region_name="us-east-1")
    mock_client.copy_snapshot_and_update_volume.assert_called_once()

def test_create_and_attach_s3_access_point_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_and_attach_s3_access_point
    mock_client = MagicMock()
    mock_client.create_and_attach_s3_access_point.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_and_attach_s3_access_point("test-name", "test-type_value", client_request_token="test-client_request_token", open_zfs_configuration={}, s3_access_point="test-s3_access_point", region_name="us-east-1")
    mock_client.create_and_attach_s3_access_point.assert_called_once()

def test_create_file_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_file_cache
    mock_client = MagicMock()
    mock_client.create_file_cache.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_file_cache("test-file_cache_type", "test-file_cache_type_version", "test-storage_capacity", "test-subnet_ids", client_request_token="test-client_request_token", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], copy_tags_to_data_repository_associations=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", lustre_configuration={}, data_repository_associations="test-data_repository_associations", region_name="us-east-1")
    mock_client.create_file_cache.assert_called_once()

def test_create_file_system_from_backup_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_file_system_from_backup
    mock_client = MagicMock()
    mock_client.create_file_system_from_backup.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_file_system_from_backup("test-backup_id", "test-subnet_ids", client_request_token="test-client_request_token", security_group_ids="test-security_group_ids", tags=[{"Key": "k", "Value": "v"}], windows_configuration={}, lustre_configuration={}, storage_type="test-storage_type", kms_key_id="test-kms_key_id", file_system_type_version="test-file_system_type_version", open_zfs_configuration={}, storage_capacity="test-storage_capacity", network_type="test-network_type", region_name="us-east-1")
    mock_client.create_file_system_from_backup.assert_called_once()

def test_create_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_snapshot
    mock_client = MagicMock()
    mock_client.create_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_snapshot("test-name", "test-volume_id", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_snapshot.assert_called_once()

def test_create_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_storage_virtual_machine
    mock_client = MagicMock()
    mock_client.create_storage_virtual_machine.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_storage_virtual_machine("test-file_system_id", "test-name", active_directory_configuration={}, client_request_token="test-client_request_token", svm_admin_password="test-svm_admin_password", tags=[{"Key": "k", "Value": "v"}], root_volume_security_style="test-root_volume_security_style", region_name="us-east-1")
    mock_client.create_storage_virtual_machine.assert_called_once()

def test_create_volume_from_backup_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import create_volume_from_backup
    mock_client = MagicMock()
    mock_client.create_volume_from_backup.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    create_volume_from_backup("test-backup_id", "test-name", client_request_token="test-client_request_token", ontap_configuration={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_volume_from_backup.assert_called_once()

def test_delete_data_repository_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import delete_data_repository_association
    mock_client = MagicMock()
    mock_client.delete_data_repository_association.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    delete_data_repository_association("test-association_id", client_request_token="test-client_request_token", delete_data_in_file_system=True, region_name="us-east-1")
    mock_client.delete_data_repository_association.assert_called_once()

def test_delete_file_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import delete_file_cache
    mock_client = MagicMock()
    mock_client.delete_file_cache.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    delete_file_cache("test-file_cache_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.delete_file_cache.assert_called_once()

def test_delete_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import delete_snapshot
    mock_client = MagicMock()
    mock_client.delete_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    delete_snapshot("test-snapshot_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.delete_snapshot.assert_called_once()

def test_delete_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import delete_storage_virtual_machine
    mock_client = MagicMock()
    mock_client.delete_storage_virtual_machine.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    delete_storage_virtual_machine("test-storage_virtual_machine_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.delete_storage_virtual_machine.assert_called_once()

def test_describe_file_caches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import describe_file_caches
    mock_client = MagicMock()
    mock_client.describe_file_caches.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    describe_file_caches(file_cache_ids="test-file_cache_ids", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_file_caches.assert_called_once()

def test_describe_s3_access_point_attachments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import describe_s3_access_point_attachments
    mock_client = MagicMock()
    mock_client.describe_s3_access_point_attachments.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    describe_s3_access_point_attachments(names="test-names", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_s3_access_point_attachments.assert_called_once()

def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import describe_snapshots
    mock_client = MagicMock()
    mock_client.describe_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    describe_snapshots(snapshot_ids="test-snapshot_ids", filters=[{}], max_results=1, next_token="test-next_token", include_shared=True, region_name="us-east-1")
    mock_client.describe_snapshots.assert_called_once()

def test_describe_storage_virtual_machines_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import describe_storage_virtual_machines
    mock_client = MagicMock()
    mock_client.describe_storage_virtual_machines.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    describe_storage_virtual_machines(storage_virtual_machine_ids="test-storage_virtual_machine_ids", filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_storage_virtual_machines.assert_called_once()

def test_detach_and_delete_s3_access_point_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import detach_and_delete_s3_access_point
    mock_client = MagicMock()
    mock_client.detach_and_delete_s3_access_point.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    detach_and_delete_s3_access_point("test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.detach_and_delete_s3_access_point.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_release_file_system_nfs_v3_locks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import release_file_system_nfs_v3_locks
    mock_client = MagicMock()
    mock_client.release_file_system_nfs_v3_locks.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    release_file_system_nfs_v3_locks("test-file_system_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.release_file_system_nfs_v3_locks.assert_called_once()

def test_restore_volume_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import restore_volume_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_volume_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    restore_volume_from_snapshot("test-volume_id", "test-snapshot_id", client_request_token="test-client_request_token", options={}, region_name="us-east-1")
    mock_client.restore_volume_from_snapshot.assert_called_once()

def test_start_misconfigured_state_recovery_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import start_misconfigured_state_recovery
    mock_client = MagicMock()
    mock_client.start_misconfigured_state_recovery.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    start_misconfigured_state_recovery("test-file_system_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_misconfigured_state_recovery.assert_called_once()

def test_update_data_repository_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import update_data_repository_association
    mock_client = MagicMock()
    mock_client.update_data_repository_association.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    update_data_repository_association("test-association_id", client_request_token="test-client_request_token", imported_file_chunk_size=1, s3="test-s3", region_name="us-east-1")
    mock_client.update_data_repository_association.assert_called_once()

def test_update_file_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import update_file_cache
    mock_client = MagicMock()
    mock_client.update_file_cache.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    update_file_cache("test-file_cache_id", client_request_token="test-client_request_token", lustre_configuration={}, region_name="us-east-1")
    mock_client.update_file_cache.assert_called_once()

def test_update_shared_vpc_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import update_shared_vpc_configuration
    mock_client = MagicMock()
    mock_client.update_shared_vpc_configuration.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    update_shared_vpc_configuration(enable_fsx_route_table_updates_from_participant_accounts=True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_shared_vpc_configuration.assert_called_once()

def test_update_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import update_snapshot
    mock_client = MagicMock()
    mock_client.update_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    update_snapshot("test-name", "test-snapshot_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_snapshot.assert_called_once()

def test_update_storage_virtual_machine_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.fsx import update_storage_virtual_machine
    mock_client = MagicMock()
    mock_client.update_storage_virtual_machine.return_value = {}
    monkeypatch.setattr("aws_util.fsx.get_client", lambda *a, **kw: mock_client)
    update_storage_virtual_machine("test-storage_virtual_machine_id", active_directory_configuration={}, client_request_token="test-client_request_token", svm_admin_password="test-svm_admin_password", region_name="us-east-1")
    mock_client.update_storage_virtual_machine.assert_called_once()
