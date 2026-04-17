"""aws_util.fsx --- Amazon FSx utilities.

Create, describe, update, and delete FSx file systems, backups, volumes,
data-repository associations, data-repository tasks, and file-system aliases.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "BackupResult",
    "CopySnapshotAndUpdateVolumeResult",
    "CreateAndAttachS3AccessPointResult",
    "CreateFileCacheResult",
    "CreateFileSystemFromBackupResult",
    "CreateSnapshotResult",
    "CreateStorageVirtualMachineResult",
    "CreateVolumeFromBackupResult",
    "DataRepositoryAssociationResult",
    "DataRepositoryTaskResult",
    "DeleteDataRepositoryAssociationResult",
    "DeleteFileCacheResult",
    "DeleteSnapshotResult",
    "DeleteStorageVirtualMachineResult",
    "DescribeFileCachesResult",
    "DescribeS3AccessPointAttachmentsResult",
    "DescribeSharedVpcConfigurationResult",
    "DescribeSnapshotsResult",
    "DescribeStorageVirtualMachinesResult",
    "DetachAndDeleteS3AccessPointResult",
    "FileSystemAliasResult",
    "FileSystemResult",
    "ListTagsForResourceResult",
    "ReleaseFileSystemNfsV3LocksResult",
    "RestoreVolumeFromSnapshotResult",
    "StartMisconfiguredStateRecoveryResult",
    "UpdateDataRepositoryAssociationResult",
    "UpdateFileCacheResult",
    "UpdateSharedVpcConfigurationResult",
    "UpdateSnapshotResult",
    "UpdateStorageVirtualMachineResult",
    "VolumeResult",
    "associate_file_system_aliases",
    "cancel_data_repository_task",
    "copy_backup",
    "copy_snapshot_and_update_volume",
    "create_and_attach_s3_access_point",
    "create_backup",
    "create_data_repository_association",
    "create_data_repository_task",
    "create_file_cache",
    "create_file_system",
    "create_file_system_from_backup",
    "create_snapshot",
    "create_storage_virtual_machine",
    "create_volume",
    "create_volume_from_backup",
    "delete_backup",
    "delete_data_repository_association",
    "delete_file_cache",
    "delete_file_system",
    "delete_snapshot",
    "delete_storage_virtual_machine",
    "delete_volume",
    "describe_backups",
    "describe_data_repository_associations",
    "describe_data_repository_tasks",
    "describe_file_caches",
    "describe_file_system_aliases",
    "describe_file_systems",
    "describe_s3_access_point_attachments",
    "describe_shared_vpc_configuration",
    "describe_snapshots",
    "describe_storage_virtual_machines",
    "describe_volumes",
    "detach_and_delete_s3_access_point",
    "disassociate_file_system_aliases",
    "list_tags_for_resource",
    "release_file_system_nfs_v3_locks",
    "restore_file_system_from_backup",
    "restore_volume_from_snapshot",
    "start_misconfigured_state_recovery",
    "tag_resource",
    "untag_resource",
    "update_data_repository_association",
    "update_file_cache",
    "update_file_system",
    "update_shared_vpc_configuration",
    "update_snapshot",
    "update_storage_virtual_machine",
    "update_volume",
    "wait_for_file_system",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class FileSystemResult(BaseModel):
    """Metadata for an FSx file system."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    file_system_id: str
    file_system_type: str | None = None
    lifecycle: str | None = None
    storage_capacity: int | None = None
    storage_type: str | None = None
    subnet_ids: list[str] = []
    dns_name: str | None = None
    resource_arn: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class BackupResult(BaseModel):
    """Metadata for an FSx backup."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    backup_id: str
    lifecycle: str | None = None
    backup_type: str | None = None
    file_system: dict[str, Any] | None = None
    resource_arn: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class VolumeResult(BaseModel):
    """Metadata for an FSx volume."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    volume_id: str
    name: str | None = None
    lifecycle: str | None = None
    volume_type: str | None = None
    file_system_id: str | None = None
    resource_arn: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class DataRepositoryAssociationResult(BaseModel):
    """Metadata for an FSx data-repository association."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    association_id: str
    file_system_id: str | None = None
    file_system_path: str | None = None
    data_repository_path: str | None = None
    lifecycle: str | None = None
    resource_arn: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class DataRepositoryTaskResult(BaseModel):
    """Metadata for an FSx data-repository task."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    task_id: str
    lifecycle: str | None = None
    task_type: str | None = None
    file_system_id: str | None = None
    resource_arn: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class FileSystemAliasResult(BaseModel):
    """Metadata for an FSx file-system alias."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str | None = None
    lifecycle: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _tags_to_dict(tags: list[dict[str, str]]) -> dict[str, str]:
    """Convert an AWS ``Tags`` list to a plain dict."""
    return {t["Key"]: t["Value"] for t in tags}


def _dict_to_tags(tags: dict[str, str]) -> list[dict[str, str]]:
    """Convert a plain dict to an AWS ``Tags`` list."""
    return [{"Key": k, "Value": v} for k, v in tags.items()]


def _parse_file_system(fs: dict[str, Any]) -> FileSystemResult:
    """Convert a raw FSx file-system dict to a :class:`FileSystemResult`."""
    tags = _tags_to_dict(fs.get("Tags", []))
    _known = {
        "FileSystemId",
        "FileSystemType",
        "Lifecycle",
        "StorageCapacity",
        "StorageType",
        "SubnetIds",
        "DNSName",
        "ResourceARN",
        "Tags",
    }
    return FileSystemResult(
        file_system_id=fs["FileSystemId"],
        file_system_type=fs.get("FileSystemType"),
        lifecycle=fs.get("Lifecycle"),
        storage_capacity=fs.get("StorageCapacity"),
        storage_type=fs.get("StorageType"),
        subnet_ids=fs.get("SubnetIds", []),
        dns_name=fs.get("DNSName"),
        resource_arn=fs.get("ResourceARN"),
        tags=tags,
        extra={k: v for k, v in fs.items() if k not in _known},
    )


def _parse_backup(bk: dict[str, Any]) -> BackupResult:
    """Convert a raw FSx backup dict to a :class:`BackupResult`."""
    tags = _tags_to_dict(bk.get("Tags", []))
    _known = {
        "BackupId",
        "Lifecycle",
        "Type",
        "FileSystem",
        "ResourceARN",
        "Tags",
    }
    return BackupResult(
        backup_id=bk["BackupId"],
        lifecycle=bk.get("Lifecycle"),
        backup_type=bk.get("Type"),
        file_system=bk.get("FileSystem"),
        resource_arn=bk.get("ResourceARN"),
        tags=tags,
        extra={k: v for k, v in bk.items() if k not in _known},
    )


def _parse_volume(vol: dict[str, Any]) -> VolumeResult:
    """Convert a raw FSx volume dict to a :class:`VolumeResult`."""
    tags = _tags_to_dict(vol.get("Tags", []))
    _known = {
        "VolumeId",
        "Name",
        "Lifecycle",
        "VolumeType",
        "FileSystemId",
        "ResourceARN",
        "Tags",
    }
    return VolumeResult(
        volume_id=vol["VolumeId"],
        name=vol.get("Name"),
        lifecycle=vol.get("Lifecycle"),
        volume_type=vol.get("VolumeType"),
        file_system_id=vol.get("FileSystemId"),
        resource_arn=vol.get("ResourceARN"),
        tags=tags,
        extra={k: v for k, v in vol.items() if k not in _known},
    )


def _parse_data_repository_association(
    dra: dict[str, Any],
) -> DataRepositoryAssociationResult:
    """Convert a raw data-repository association dict."""
    tags = _tags_to_dict(dra.get("Tags", []))
    _known = {
        "AssociationId",
        "FileSystemId",
        "FileSystemPath",
        "DataRepositoryPath",
        "Lifecycle",
        "ResourceARN",
        "Tags",
    }
    return DataRepositoryAssociationResult(
        association_id=dra["AssociationId"],
        file_system_id=dra.get("FileSystemId"),
        file_system_path=dra.get("FileSystemPath"),
        data_repository_path=dra.get("DataRepositoryPath"),
        lifecycle=dra.get("Lifecycle"),
        resource_arn=dra.get("ResourceARN"),
        tags=tags,
        extra={k: v for k, v in dra.items() if k not in _known},
    )


def _parse_data_repository_task(
    drt: dict[str, Any],
) -> DataRepositoryTaskResult:
    """Convert a raw data-repository task dict."""
    tags = _tags_to_dict(drt.get("Tags", []))
    _known = {
        "TaskId",
        "Lifecycle",
        "Type",
        "FileSystemId",
        "ResourceARN",
        "Tags",
    }
    return DataRepositoryTaskResult(
        task_id=drt["TaskId"],
        lifecycle=drt.get("Lifecycle"),
        task_type=drt.get("Type"),
        file_system_id=drt.get("FileSystemId"),
        resource_arn=drt.get("ResourceARN"),
        tags=tags,
        extra={k: v for k, v in drt.items() if k not in _known},
    )


def _parse_alias(alias: dict[str, Any]) -> FileSystemAliasResult:
    """Convert a raw alias dict to a :class:`FileSystemAliasResult`."""
    _known = {"Name", "Lifecycle"}
    return FileSystemAliasResult(
        name=alias.get("Name"),
        lifecycle=alias.get("Lifecycle"),
        extra={k: v for k, v in alias.items() if k not in _known},
    )


# ---------------------------------------------------------------------------
# File-system operations
# ---------------------------------------------------------------------------


def create_file_system(
    *,
    file_system_type: str,
    storage_capacity: int,
    subnet_ids: list[str],
    storage_type: str | None = None,
    security_group_ids: list[str] | None = None,
    tags: dict[str, str] | None = None,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> FileSystemResult:
    """Create an FSx file system.

    Args:
        file_system_type: File-system type (``"LUSTRE"``, ``"WINDOWS"``,
            ``"ONTAP"``, ``"OPENZFS"``).
        storage_capacity: Storage capacity in GiB.
        subnet_ids: Subnet IDs for the file system.
        storage_type: ``"SSD"`` or ``"HDD"``.
        security_group_ids: Security-group IDs to associate.
        tags: Key/value tags to apply.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        A :class:`FileSystemResult` for the newly created file system.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {
        "FileSystemType": file_system_type,
        "StorageCapacity": storage_capacity,
        "SubnetIds": subnet_ids,
    }
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.create_file_system(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_file_system failed") from exc
    return _parse_file_system(resp["FileSystem"])


def describe_file_systems(
    *,
    file_system_ids: list[str] | None = None,
    region_name: str | None = None,
) -> list[FileSystemResult]:
    """Describe one or more FSx file systems.

    Args:
        file_system_ids: Limit to specific file-system IDs.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileSystemResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_ids:
        kwargs["FileSystemIds"] = file_system_ids

    results: list[FileSystemResult] = []
    try:
        while True:
            resp = client.describe_file_systems(**kwargs)
            for fs in resp.get("FileSystems", []):
                results.append(_parse_file_system(fs))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_file_systems failed") from exc
    return results


def update_file_system(
    file_system_id: str,
    *,
    storage_capacity: int | None = None,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> FileSystemResult:
    """Update an FSx file system.

    Args:
        file_system_id: The file-system ID to update.
        storage_capacity: New storage capacity in GiB.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        The updated :class:`FileSystemResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"FileSystemId": file_system_id}
    if storage_capacity is not None:
        kwargs["StorageCapacity"] = storage_capacity
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.update_file_system(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_file_system failed") from exc
    return _parse_file_system(resp["FileSystem"])


def delete_file_system(
    file_system_id: str,
    *,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete an FSx file system.

    Args:
        file_system_id: The file-system ID to delete.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        The raw API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"FileSystemId": file_system_id}
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.delete_file_system(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_file_system failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Backup operations
# ---------------------------------------------------------------------------


def create_backup(
    *,
    file_system_id: str | None = None,
    volume_id: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> BackupResult:
    """Create an FSx backup.

    Args:
        file_system_id: File-system ID to back up.
        volume_id: Volume ID to back up (ONTAP/OpenZFS).
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`BackupResult` for the new backup.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_id is not None:
        kwargs["FileSystemId"] = file_system_id
    if volume_id is not None:
        kwargs["VolumeId"] = volume_id
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    try:
        resp = client.create_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_backup failed") from exc
    return _parse_backup(resp["Backup"])


def describe_backups(
    *,
    backup_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[BackupResult]:
    """Describe FSx backups.

    Args:
        backup_ids: Limit to specific backup IDs.
        filters: API filter dicts.
        region_name: AWS region override.

    Returns:
        A list of :class:`BackupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if backup_ids:
        kwargs["BackupIds"] = backup_ids
    if filters:
        kwargs["Filters"] = filters

    results: list[BackupResult] = []
    try:
        while True:
            resp = client.describe_backups(**kwargs)
            for bk in resp.get("Backups", []):
                results.append(_parse_backup(bk))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_backups failed") from exc
    return results


def delete_backup(
    backup_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete an FSx backup.

    Args:
        backup_id: The backup ID to delete.
        region_name: AWS region override.

    Returns:
        The raw API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    try:
        resp = client.delete_backup(BackupId=backup_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_backup failed") from exc
    return resp


def copy_backup(
    source_backup_id: str,
    *,
    source_region: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> BackupResult:
    """Copy an FSx backup.

    Args:
        source_backup_id: The source backup ID to copy.
        source_region: The region of the source backup.
        tags: Key/value tags for the new backup.
        region_name: AWS region override (destination).

    Returns:
        A :class:`BackupResult` for the copied backup.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"SourceBackupId": source_backup_id}
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    try:
        resp = client.copy_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "copy_backup failed") from exc
    return _parse_backup(resp["Backup"])


def restore_file_system_from_backup(
    backup_id: str,
    *,
    subnet_ids: list[str],
    security_group_ids: list[str] | None = None,
    tags: dict[str, str] | None = None,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> FileSystemResult:
    """Restore an FSx file system from a backup.

    Args:
        backup_id: The backup ID to restore from.
        subnet_ids: Subnet IDs for the restored file system.
        security_group_ids: Security-group IDs to associate.
        tags: Key/value tags to apply.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        A :class:`FileSystemResult` for the restored file system.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {
        "BackupId": backup_id,
        "SubnetIds": subnet_ids,
    }
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.create_file_system_from_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "restore_file_system_from_backup failed") from exc
    return _parse_file_system(resp["FileSystem"])


# ---------------------------------------------------------------------------
# Alias operations
# ---------------------------------------------------------------------------


def describe_file_system_aliases(
    file_system_id: str,
    *,
    region_name: str | None = None,
) -> list[FileSystemAliasResult]:
    """Describe aliases for an FSx file system.

    Args:
        file_system_id: The file-system ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileSystemAliasResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"FileSystemId": file_system_id}
    results: list[FileSystemAliasResult] = []
    try:
        while True:
            resp = client.describe_file_system_aliases(**kwargs)
            for alias in resp.get("Aliases", []):
                results.append(_parse_alias(alias))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_file_system_aliases failed") from exc
    return results


def associate_file_system_aliases(
    file_system_id: str,
    *,
    aliases: list[str],
    region_name: str | None = None,
) -> list[FileSystemAliasResult]:
    """Associate DNS aliases with an FSx file system.

    Args:
        file_system_id: The file-system ID.
        aliases: DNS alias names to associate.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileSystemAliasResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    try:
        resp = client.associate_file_system_aliases(
            FileSystemId=file_system_id,
            Aliases=aliases,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "associate_file_system_aliases failed") from exc
    return [_parse_alias(a) for a in resp.get("Aliases", [])]


def disassociate_file_system_aliases(
    file_system_id: str,
    *,
    aliases: list[str],
    region_name: str | None = None,
) -> list[FileSystemAliasResult]:
    """Disassociate DNS aliases from an FSx file system.

    Args:
        file_system_id: The file-system ID.
        aliases: DNS alias names to disassociate.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileSystemAliasResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    try:
        resp = client.disassociate_file_system_aliases(
            FileSystemId=file_system_id,
            Aliases=aliases,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "disassociate_file_system_aliases failed") from exc
    return [_parse_alias(a) for a in resp.get("Aliases", [])]


# ---------------------------------------------------------------------------
# Volume operations
# ---------------------------------------------------------------------------


def create_volume(
    *,
    volume_type: str,
    name: str,
    extra_params: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> VolumeResult:
    """Create an FSx volume.

    Args:
        volume_type: Volume type (``"ONTAP"`` or ``"OPENZFS"``).
        name: Name for the volume.
        extra_params: Additional API parameters forwarded verbatim
            (e.g. ``OntapConfiguration``, ``OpenZFSConfiguration``).
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`VolumeResult` for the new volume.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {
        "VolumeType": volume_type,
        "Name": name,
    }
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.create_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_volume failed") from exc
    return _parse_volume(resp["Volume"])


def describe_volumes(
    *,
    volume_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[VolumeResult]:
    """Describe FSx volumes.

    Args:
        volume_ids: Limit to specific volume IDs.
        filters: API filter dicts.
        region_name: AWS region override.

    Returns:
        A list of :class:`VolumeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if volume_ids:
        kwargs["VolumeIds"] = volume_ids
    if filters:
        kwargs["Filters"] = filters

    results: list[VolumeResult] = []
    try:
        while True:
            resp = client.describe_volumes(**kwargs)
            for vol in resp.get("Volumes", []):
                results.append(_parse_volume(vol))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_volumes failed") from exc
    return results


def update_volume(
    volume_id: str,
    *,
    name: str | None = None,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> VolumeResult:
    """Update an FSx volume.

    Args:
        volume_id: The volume ID to update.
        name: New name for the volume.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        The updated :class:`VolumeResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"VolumeId": volume_id}
    if name is not None:
        kwargs["Name"] = name
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.update_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_volume failed") from exc
    return _parse_volume(resp["Volume"])


def delete_volume(
    volume_id: str,
    *,
    extra_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete an FSx volume.

    Args:
        volume_id: The volume ID to delete.
        extra_params: Additional API parameters forwarded verbatim.
        region_name: AWS region override.

    Returns:
        The raw API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {"VolumeId": volume_id}
    if extra_params:
        kwargs.update(extra_params)
    try:
        resp = client.delete_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_volume failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Data-repository association operations
# ---------------------------------------------------------------------------


def create_data_repository_association(
    file_system_id: str,
    *,
    file_system_path: str,
    data_repository_path: str,
    batch_import_meta_data_on_create: bool | None = None,
    imported_file_chunk_size: int | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DataRepositoryAssociationResult:
    """Create a data-repository association for an FSx file system.

    Args:
        file_system_id: The file-system ID.
        file_system_path: Path on the file system.
        data_repository_path: S3 URI for the data repository.
        batch_import_meta_data_on_create: Whether to import metadata
            on creation.
        imported_file_chunk_size: Chunk size in MiB.
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`DataRepositoryAssociationResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {
        "FileSystemId": file_system_id,
        "FileSystemPath": file_system_path,
        "DataRepositoryPath": data_repository_path,
    }
    if batch_import_meta_data_on_create is not None:
        kwargs["BatchImportMetaDataOnCreate"] = batch_import_meta_data_on_create
    if imported_file_chunk_size is not None:
        kwargs["ImportedFileChunkSize"] = imported_file_chunk_size
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    try:
        resp = client.create_data_repository_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_data_repository_association failed") from exc
    return _parse_data_repository_association(resp["Association"])


def describe_data_repository_associations(
    *,
    association_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[DataRepositoryAssociationResult]:
    """Describe FSx data-repository associations.

    Args:
        association_ids: Limit to specific association IDs.
        filters: API filter dicts.
        region_name: AWS region override.

    Returns:
        A list of :class:`DataRepositoryAssociationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if association_ids:
        kwargs["AssociationIds"] = association_ids
    if filters:
        kwargs["Filters"] = filters

    results: list[DataRepositoryAssociationResult] = []
    try:
        while True:
            resp = client.describe_data_repository_associations(**kwargs)
            for dra in resp.get("Associations", []):
                results.append(_parse_data_repository_association(dra))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_data_repository_associations failed") from exc
    return results


# ---------------------------------------------------------------------------
# Data-repository task operations
# ---------------------------------------------------------------------------


def create_data_repository_task(
    file_system_id: str,
    *,
    task_type: str,
    report: dict[str, Any],
    paths: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> DataRepositoryTaskResult:
    """Create a data-repository task for an FSx file system.

    Args:
        file_system_id: The file-system ID.
        task_type: Task type (e.g. ``"EXPORT_TO_REPOSITORY"``).
        report: Report configuration dict.
        paths: Paths to include in the task.
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`DataRepositoryTaskResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {
        "FileSystemId": file_system_id,
        "Type": task_type,
        "Report": report,
    }
    if paths is not None:
        kwargs["Paths"] = paths
    if tags:
        kwargs["Tags"] = _dict_to_tags(tags)
    try:
        resp = client.create_data_repository_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_data_repository_task failed") from exc
    return _parse_data_repository_task(resp["DataRepositoryTask"])


def describe_data_repository_tasks(
    *,
    task_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[DataRepositoryTaskResult]:
    """Describe FSx data-repository tasks.

    Args:
        task_ids: Limit to specific task IDs.
        filters: API filter dicts.
        region_name: AWS region override.

    Returns:
        A list of :class:`DataRepositoryTaskResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if task_ids:
        kwargs["TaskIds"] = task_ids
    if filters:
        kwargs["Filters"] = filters

    results: list[DataRepositoryTaskResult] = []
    try:
        while True:
            resp = client.describe_data_repository_tasks(**kwargs)
            for drt in resp.get("DataRepositoryTasks", []):
                results.append(_parse_data_repository_task(drt))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_data_repository_tasks failed") from exc
    return results


def cancel_data_repository_task(
    task_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Cancel a running data-repository task.

    Args:
        task_id: The task ID to cancel.
        region_name: AWS region override.

    Returns:
        The raw API response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    try:
        resp = client.cancel_data_repository_task(TaskId=task_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, "cancel_data_repository_task failed") from exc
    return resp


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


def wait_for_file_system(
    file_system_id: str,
    *,
    target_state: str = "AVAILABLE",
    timeout: float = 300.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> FileSystemResult:
    """Poll until an FSx file system reaches the desired lifecycle state.

    Args:
        file_system_id: The file-system ID to monitor.
        target_state: Desired ``Lifecycle`` (default ``"AVAILABLE"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`FileSystemResult` once it reaches *target_state*.

    Raises:
        AwsTimeoutError: If the file system does not reach the target state
            within *timeout* seconds.
        RuntimeError: If the file system cannot be found.
    """
    deadline = time.monotonic() + timeout
    while True:
        results = describe_file_systems(file_system_ids=[file_system_id], region_name=region_name)
        if not results:
            raise RuntimeError(f"File system {file_system_id!r} not found")
        fs = results[0]
        if fs.lifecycle == target_state:
            return fs
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"File system {file_system_id!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {fs.lifecycle!r})"
            )
        time.sleep(poll_interval)


class CopySnapshotAndUpdateVolumeResult(BaseModel):
    """Result of copy_snapshot_and_update_volume."""

    model_config = ConfigDict(frozen=True)

    volume_id: str | None = None
    lifecycle: str | None = None
    administrative_actions: list[dict[str, Any]] | None = None


class CreateAndAttachS3AccessPointResult(BaseModel):
    """Result of create_and_attach_s3_access_point."""

    model_config = ConfigDict(frozen=True)

    s3_access_point_attachment: dict[str, Any] | None = None


class CreateFileCacheResult(BaseModel):
    """Result of create_file_cache."""

    model_config = ConfigDict(frozen=True)

    file_cache: dict[str, Any] | None = None


class CreateFileSystemFromBackupResult(BaseModel):
    """Result of create_file_system_from_backup."""

    model_config = ConfigDict(frozen=True)

    file_system: dict[str, Any] | None = None


class CreateSnapshotResult(BaseModel):
    """Result of create_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class CreateStorageVirtualMachineResult(BaseModel):
    """Result of create_storage_virtual_machine."""

    model_config = ConfigDict(frozen=True)

    storage_virtual_machine: dict[str, Any] | None = None


class CreateVolumeFromBackupResult(BaseModel):
    """Result of create_volume_from_backup."""

    model_config = ConfigDict(frozen=True)

    volume: dict[str, Any] | None = None


class DeleteDataRepositoryAssociationResult(BaseModel):
    """Result of delete_data_repository_association."""

    model_config = ConfigDict(frozen=True)

    association_id: str | None = None
    lifecycle: str | None = None
    delete_data_in_file_system: bool | None = None


class DeleteFileCacheResult(BaseModel):
    """Result of delete_file_cache."""

    model_config = ConfigDict(frozen=True)

    file_cache_id: str | None = None
    lifecycle: str | None = None


class DeleteSnapshotResult(BaseModel):
    """Result of delete_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str | None = None
    lifecycle: str | None = None


class DeleteStorageVirtualMachineResult(BaseModel):
    """Result of delete_storage_virtual_machine."""

    model_config = ConfigDict(frozen=True)

    storage_virtual_machine_id: str | None = None
    lifecycle: str | None = None


class DescribeFileCachesResult(BaseModel):
    """Result of describe_file_caches."""

    model_config = ConfigDict(frozen=True)

    file_caches: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeS3AccessPointAttachmentsResult(BaseModel):
    """Result of describe_s3_access_point_attachments."""

    model_config = ConfigDict(frozen=True)

    s3_access_point_attachments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeSharedVpcConfigurationResult(BaseModel):
    """Result of describe_shared_vpc_configuration."""

    model_config = ConfigDict(frozen=True)

    enable_fsx_route_table_updates_from_participant_accounts: str | None = None


class DescribeSnapshotsResult(BaseModel):
    """Result of describe_snapshots."""

    model_config = ConfigDict(frozen=True)

    snapshots: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeStorageVirtualMachinesResult(BaseModel):
    """Result of describe_storage_virtual_machines."""

    model_config = ConfigDict(frozen=True)

    storage_virtual_machines: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DetachAndDeleteS3AccessPointResult(BaseModel):
    """Result of detach_and_delete_s3_access_point."""

    model_config = ConfigDict(frozen=True)

    lifecycle: str | None = None
    name: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ReleaseFileSystemNfsV3LocksResult(BaseModel):
    """Result of release_file_system_nfs_v3_locks."""

    model_config = ConfigDict(frozen=True)

    file_system: dict[str, Any] | None = None


class RestoreVolumeFromSnapshotResult(BaseModel):
    """Result of restore_volume_from_snapshot."""

    model_config = ConfigDict(frozen=True)

    volume_id: str | None = None
    lifecycle: str | None = None
    administrative_actions: list[dict[str, Any]] | None = None


class StartMisconfiguredStateRecoveryResult(BaseModel):
    """Result of start_misconfigured_state_recovery."""

    model_config = ConfigDict(frozen=True)

    file_system: dict[str, Any] | None = None


class UpdateDataRepositoryAssociationResult(BaseModel):
    """Result of update_data_repository_association."""

    model_config = ConfigDict(frozen=True)

    association: dict[str, Any] | None = None


class UpdateFileCacheResult(BaseModel):
    """Result of update_file_cache."""

    model_config = ConfigDict(frozen=True)

    file_cache: dict[str, Any] | None = None


class UpdateSharedVpcConfigurationResult(BaseModel):
    """Result of update_shared_vpc_configuration."""

    model_config = ConfigDict(frozen=True)

    enable_fsx_route_table_updates_from_participant_accounts: str | None = None


class UpdateSnapshotResult(BaseModel):
    """Result of update_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class UpdateStorageVirtualMachineResult(BaseModel):
    """Result of update_storage_virtual_machine."""

    model_config = ConfigDict(frozen=True)

    storage_virtual_machine: dict[str, Any] | None = None


def copy_snapshot_and_update_volume(
    volume_id: str,
    source_snapshot_arn: str,
    *,
    client_request_token: str | None = None,
    copy_strategy: str | None = None,
    options: list[str] | None = None,
    region_name: str | None = None,
) -> CopySnapshotAndUpdateVolumeResult:
    """Copy snapshot and update volume.

    Args:
        volume_id: Volume id.
        source_snapshot_arn: Source snapshot arn.
        client_request_token: Client request token.
        copy_strategy: Copy strategy.
        options: Options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeId"] = volume_id
    kwargs["SourceSnapshotARN"] = source_snapshot_arn
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if copy_strategy is not None:
        kwargs["CopyStrategy"] = copy_strategy
    if options is not None:
        kwargs["Options"] = options
    try:
        resp = client.copy_snapshot_and_update_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy snapshot and update volume") from exc
    return CopySnapshotAndUpdateVolumeResult(
        volume_id=resp.get("VolumeId"),
        lifecycle=resp.get("Lifecycle"),
        administrative_actions=resp.get("AdministrativeActions"),
    )


def create_and_attach_s3_access_point(
    name: str,
    type_value: str,
    *,
    client_request_token: str | None = None,
    open_zfs_configuration: dict[str, Any] | None = None,
    s3_access_point: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAndAttachS3AccessPointResult:
    """Create and attach s3 access point.

    Args:
        name: Name.
        type_value: Type value.
        client_request_token: Client request token.
        open_zfs_configuration: Open zfs configuration.
        s3_access_point: S3 access point.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if open_zfs_configuration is not None:
        kwargs["OpenZFSConfiguration"] = open_zfs_configuration
    if s3_access_point is not None:
        kwargs["S3AccessPoint"] = s3_access_point
    try:
        resp = client.create_and_attach_s3_access_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create and attach s3 access point") from exc
    return CreateAndAttachS3AccessPointResult(
        s3_access_point_attachment=resp.get("S3AccessPointAttachment"),
    )


def create_file_cache(
    file_cache_type: str,
    file_cache_type_version: str,
    storage_capacity: int,
    subnet_ids: list[str],
    *,
    client_request_token: str | None = None,
    security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    copy_tags_to_data_repository_associations: bool | None = None,
    kms_key_id: str | None = None,
    lustre_configuration: dict[str, Any] | None = None,
    data_repository_associations: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateFileCacheResult:
    """Create file cache.

    Args:
        file_cache_type: File cache type.
        file_cache_type_version: File cache type version.
        storage_capacity: Storage capacity.
        subnet_ids: Subnet ids.
        client_request_token: Client request token.
        security_group_ids: Security group ids.
        tags: Tags.
        copy_tags_to_data_repository_associations: Copy tags to data repository associations.
        kms_key_id: Kms key id.
        lustre_configuration: Lustre configuration.
        data_repository_associations: Data repository associations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileCacheType"] = file_cache_type
    kwargs["FileCacheTypeVersion"] = file_cache_type_version
    kwargs["StorageCapacity"] = storage_capacity
    kwargs["SubnetIds"] = subnet_ids
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["Tags"] = tags
    if copy_tags_to_data_repository_associations is not None:
        kwargs["CopyTagsToDataRepositoryAssociations"] = copy_tags_to_data_repository_associations
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if lustre_configuration is not None:
        kwargs["LustreConfiguration"] = lustre_configuration
    if data_repository_associations is not None:
        kwargs["DataRepositoryAssociations"] = data_repository_associations
    try:
        resp = client.create_file_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create file cache") from exc
    return CreateFileCacheResult(
        file_cache=resp.get("FileCache"),
    )


def create_file_system_from_backup(
    backup_id: str,
    subnet_ids: list[str],
    *,
    client_request_token: str | None = None,
    security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    windows_configuration: dict[str, Any] | None = None,
    lustre_configuration: dict[str, Any] | None = None,
    storage_type: str | None = None,
    kms_key_id: str | None = None,
    file_system_type_version: str | None = None,
    open_zfs_configuration: dict[str, Any] | None = None,
    storage_capacity: int | None = None,
    network_type: str | None = None,
    region_name: str | None = None,
) -> CreateFileSystemFromBackupResult:
    """Create file system from backup.

    Args:
        backup_id: Backup id.
        subnet_ids: Subnet ids.
        client_request_token: Client request token.
        security_group_ids: Security group ids.
        tags: Tags.
        windows_configuration: Windows configuration.
        lustre_configuration: Lustre configuration.
        storage_type: Storage type.
        kms_key_id: Kms key id.
        file_system_type_version: File system type version.
        open_zfs_configuration: Open zfs configuration.
        storage_capacity: Storage capacity.
        network_type: Network type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BackupId"] = backup_id
    kwargs["SubnetIds"] = subnet_ids
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["Tags"] = tags
    if windows_configuration is not None:
        kwargs["WindowsConfiguration"] = windows_configuration
    if lustre_configuration is not None:
        kwargs["LustreConfiguration"] = lustre_configuration
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if file_system_type_version is not None:
        kwargs["FileSystemTypeVersion"] = file_system_type_version
    if open_zfs_configuration is not None:
        kwargs["OpenZFSConfiguration"] = open_zfs_configuration
    if storage_capacity is not None:
        kwargs["StorageCapacity"] = storage_capacity
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    try:
        resp = client.create_file_system_from_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create file system from backup") from exc
    return CreateFileSystemFromBackupResult(
        file_system=resp.get("FileSystem"),
    )


def create_snapshot(
    name: str,
    volume_id: str,
    *,
    client_request_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateSnapshotResult:
    """Create snapshot.

    Args:
        name: Name.
        volume_id: Volume id.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["VolumeId"] = volume_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot") from exc
    return CreateSnapshotResult(
        snapshot=resp.get("Snapshot"),
    )


def create_storage_virtual_machine(
    file_system_id: str,
    name: str,
    *,
    active_directory_configuration: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    svm_admin_password: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    root_volume_security_style: str | None = None,
    region_name: str | None = None,
) -> CreateStorageVirtualMachineResult:
    """Create storage virtual machine.

    Args:
        file_system_id: File system id.
        name: Name.
        active_directory_configuration: Active directory configuration.
        client_request_token: Client request token.
        svm_admin_password: Svm admin password.
        tags: Tags.
        root_volume_security_style: Root volume security style.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    kwargs["Name"] = name
    if active_directory_configuration is not None:
        kwargs["ActiveDirectoryConfiguration"] = active_directory_configuration
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if svm_admin_password is not None:
        kwargs["SvmAdminPassword"] = svm_admin_password
    if tags is not None:
        kwargs["Tags"] = tags
    if root_volume_security_style is not None:
        kwargs["RootVolumeSecurityStyle"] = root_volume_security_style
    try:
        resp = client.create_storage_virtual_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create storage virtual machine") from exc
    return CreateStorageVirtualMachineResult(
        storage_virtual_machine=resp.get("StorageVirtualMachine"),
    )


def create_volume_from_backup(
    backup_id: str,
    name: str,
    *,
    client_request_token: str | None = None,
    ontap_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateVolumeFromBackupResult:
    """Create volume from backup.

    Args:
        backup_id: Backup id.
        name: Name.
        client_request_token: Client request token.
        ontap_configuration: Ontap configuration.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BackupId"] = backup_id
    kwargs["Name"] = name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if ontap_configuration is not None:
        kwargs["OntapConfiguration"] = ontap_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_volume_from_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create volume from backup") from exc
    return CreateVolumeFromBackupResult(
        volume=resp.get("Volume"),
    )


def delete_data_repository_association(
    association_id: str,
    *,
    client_request_token: str | None = None,
    delete_data_in_file_system: bool | None = None,
    region_name: str | None = None,
) -> DeleteDataRepositoryAssociationResult:
    """Delete data repository association.

    Args:
        association_id: Association id.
        client_request_token: Client request token.
        delete_data_in_file_system: Delete data in file system.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if delete_data_in_file_system is not None:
        kwargs["DeleteDataInFileSystem"] = delete_data_in_file_system
    try:
        resp = client.delete_data_repository_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete data repository association") from exc
    return DeleteDataRepositoryAssociationResult(
        association_id=resp.get("AssociationId"),
        lifecycle=resp.get("Lifecycle"),
        delete_data_in_file_system=resp.get("DeleteDataInFileSystem"),
    )


def delete_file_cache(
    file_cache_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DeleteFileCacheResult:
    """Delete file cache.

    Args:
        file_cache_id: File cache id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileCacheId"] = file_cache_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.delete_file_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete file cache") from exc
    return DeleteFileCacheResult(
        file_cache_id=resp.get("FileCacheId"),
        lifecycle=resp.get("Lifecycle"),
    )


def delete_snapshot(
    snapshot_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DeleteSnapshotResult:
    """Delete snapshot.

    Args:
        snapshot_id: Snapshot id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SnapshotId"] = snapshot_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.delete_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot") from exc
    return DeleteSnapshotResult(
        snapshot_id=resp.get("SnapshotId"),
        lifecycle=resp.get("Lifecycle"),
    )


def delete_storage_virtual_machine(
    storage_virtual_machine_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DeleteStorageVirtualMachineResult:
    """Delete storage virtual machine.

    Args:
        storage_virtual_machine_id: Storage virtual machine id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StorageVirtualMachineId"] = storage_virtual_machine_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.delete_storage_virtual_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete storage virtual machine") from exc
    return DeleteStorageVirtualMachineResult(
        storage_virtual_machine_id=resp.get("StorageVirtualMachineId"),
        lifecycle=resp.get("Lifecycle"),
    )


def describe_file_caches(
    *,
    file_cache_ids: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeFileCachesResult:
    """Describe file caches.

    Args:
        file_cache_ids: File cache ids.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if file_cache_ids is not None:
        kwargs["FileCacheIds"] = file_cache_ids
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_file_caches(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe file caches") from exc
    return DescribeFileCachesResult(
        file_caches=resp.get("FileCaches"),
        next_token=resp.get("NextToken"),
    )


def describe_s3_access_point_attachments(
    *,
    names: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeS3AccessPointAttachmentsResult:
    """Describe s3 access point attachments.

    Args:
        names: Names.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if names is not None:
        kwargs["Names"] = names
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_s3_access_point_attachments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe s3 access point attachments") from exc
    return DescribeS3AccessPointAttachmentsResult(
        s3_access_point_attachments=resp.get("S3AccessPointAttachments"),
        next_token=resp.get("NextToken"),
    )


def describe_shared_vpc_configuration(
    region_name: str | None = None,
) -> DescribeSharedVpcConfigurationResult:
    """Describe shared vpc configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_shared_vpc_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe shared vpc configuration") from exc
    return DescribeSharedVpcConfigurationResult(
        enable_fsx_route_table_updates_from_participant_accounts=resp.get(
            "EnableFsxRouteTableUpdatesFromParticipantAccounts"
        ),
    )


def describe_snapshots(
    *,
    snapshot_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    include_shared: bool | None = None,
    region_name: str | None = None,
) -> DescribeSnapshotsResult:
    """Describe snapshots.

    Args:
        snapshot_ids: Snapshot ids.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        include_shared: Include shared.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if snapshot_ids is not None:
        kwargs["SnapshotIds"] = snapshot_ids
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if include_shared is not None:
        kwargs["IncludeShared"] = include_shared
    try:
        resp = client.describe_snapshots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe snapshots") from exc
    return DescribeSnapshotsResult(
        snapshots=resp.get("Snapshots"),
        next_token=resp.get("NextToken"),
    )


def describe_storage_virtual_machines(
    *,
    storage_virtual_machine_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeStorageVirtualMachinesResult:
    """Describe storage virtual machines.

    Args:
        storage_virtual_machine_ids: Storage virtual machine ids.
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if storage_virtual_machine_ids is not None:
        kwargs["StorageVirtualMachineIds"] = storage_virtual_machine_ids
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_storage_virtual_machines(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe storage virtual machines") from exc
    return DescribeStorageVirtualMachinesResult(
        storage_virtual_machines=resp.get("StorageVirtualMachines"),
        next_token=resp.get("NextToken"),
    )


def detach_and_delete_s3_access_point(
    name: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DetachAndDeleteS3AccessPointResult:
    """Detach and delete s3 access point.

    Args:
        name: Name.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.detach_and_delete_s3_access_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detach and delete s3 access point") from exc
    return DetachAndDeleteS3AccessPointResult(
        lifecycle=resp.get("Lifecycle"),
        name=resp.get("Name"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def release_file_system_nfs_v3_locks(
    file_system_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> ReleaseFileSystemNfsV3LocksResult:
    """Release file system nfs v3 locks.

    Args:
        file_system_id: File system id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.release_file_system_nfs_v3_locks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to release file system nfs v3 locks") from exc
    return ReleaseFileSystemNfsV3LocksResult(
        file_system=resp.get("FileSystem"),
    )


def restore_volume_from_snapshot(
    volume_id: str,
    snapshot_id: str,
    *,
    client_request_token: str | None = None,
    options: list[str] | None = None,
    region_name: str | None = None,
) -> RestoreVolumeFromSnapshotResult:
    """Restore volume from snapshot.

    Args:
        volume_id: Volume id.
        snapshot_id: Snapshot id.
        client_request_token: Client request token.
        options: Options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeId"] = volume_id
    kwargs["SnapshotId"] = snapshot_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if options is not None:
        kwargs["Options"] = options
    try:
        resp = client.restore_volume_from_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore volume from snapshot") from exc
    return RestoreVolumeFromSnapshotResult(
        volume_id=resp.get("VolumeId"),
        lifecycle=resp.get("Lifecycle"),
        administrative_actions=resp.get("AdministrativeActions"),
    )


def start_misconfigured_state_recovery(
    file_system_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartMisconfiguredStateRecoveryResult:
    """Start misconfigured state recovery.

    Args:
        file_system_id: File system id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.start_misconfigured_state_recovery(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start misconfigured state recovery") from exc
    return StartMisconfiguredStateRecoveryResult(
        file_system=resp.get("FileSystem"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_data_repository_association(
    association_id: str,
    *,
    client_request_token: str | None = None,
    imported_file_chunk_size: int | None = None,
    s3: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDataRepositoryAssociationResult:
    """Update data repository association.

    Args:
        association_id: Association id.
        client_request_token: Client request token.
        imported_file_chunk_size: Imported file chunk size.
        s3: S3.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AssociationId"] = association_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if imported_file_chunk_size is not None:
        kwargs["ImportedFileChunkSize"] = imported_file_chunk_size
    if s3 is not None:
        kwargs["S3"] = s3
    try:
        resp = client.update_data_repository_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update data repository association") from exc
    return UpdateDataRepositoryAssociationResult(
        association=resp.get("Association"),
    )


def update_file_cache(
    file_cache_id: str,
    *,
    client_request_token: str | None = None,
    lustre_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFileCacheResult:
    """Update file cache.

    Args:
        file_cache_id: File cache id.
        client_request_token: Client request token.
        lustre_configuration: Lustre configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileCacheId"] = file_cache_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if lustre_configuration is not None:
        kwargs["LustreConfiguration"] = lustre_configuration
    try:
        resp = client.update_file_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update file cache") from exc
    return UpdateFileCacheResult(
        file_cache=resp.get("FileCache"),
    )


def update_shared_vpc_configuration(
    *,
    enable_fsx_route_table_updates_from_participant_accounts: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateSharedVpcConfigurationResult:
    """Update shared vpc configuration.

    Args:
        enable_fsx_route_table_updates_from_participant_accounts: Enable fsx route table updates from participant accounts.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    if enable_fsx_route_table_updates_from_participant_accounts is not None:
        kwargs["EnableFsxRouteTableUpdatesFromParticipantAccounts"] = (
            enable_fsx_route_table_updates_from_participant_accounts
        )
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.update_shared_vpc_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update shared vpc configuration") from exc
    return UpdateSharedVpcConfigurationResult(
        enable_fsx_route_table_updates_from_participant_accounts=resp.get(
            "EnableFsxRouteTableUpdatesFromParticipantAccounts"
        ),
    )


def update_snapshot(
    name: str,
    snapshot_id: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateSnapshotResult:
    """Update snapshot.

    Args:
        name: Name.
        snapshot_id: Snapshot id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["SnapshotId"] = snapshot_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.update_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update snapshot") from exc
    return UpdateSnapshotResult(
        snapshot=resp.get("Snapshot"),
    )


def update_storage_virtual_machine(
    storage_virtual_machine_id: str,
    *,
    active_directory_configuration: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    svm_admin_password: str | None = None,
    region_name: str | None = None,
) -> UpdateStorageVirtualMachineResult:
    """Update storage virtual machine.

    Args:
        storage_virtual_machine_id: Storage virtual machine id.
        active_directory_configuration: Active directory configuration.
        client_request_token: Client request token.
        svm_admin_password: Svm admin password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("fsx", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StorageVirtualMachineId"] = storage_virtual_machine_id
    if active_directory_configuration is not None:
        kwargs["ActiveDirectoryConfiguration"] = active_directory_configuration
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if svm_admin_password is not None:
        kwargs["SvmAdminPassword"] = svm_admin_password
    try:
        resp = client.update_storage_virtual_machine(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update storage virtual machine") from exc
    return UpdateStorageVirtualMachineResult(
        storage_virtual_machine=resp.get("StorageVirtualMachine"),
    )
