"""aws_util.storage_gateway — AWS Storage Gateway utilities.

Activate, describe, list, delete, and shut down gateways.  Manage NFS file
shares, volumes, and snapshots via the ``storagegateway`` API.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AddCacheResult",
    "AddTagsToResourceResult",
    "AddUploadBufferResult",
    "AddWorkingStorageResult",
    "AssignTapePoolResult",
    "AssociateFileSystemResult",
    "AttachVolumeResult",
    "CancelArchivalResult",
    "CancelCacheReportResult",
    "CancelRetrievalResult",
    "CreateCachedIscsiVolumeResult",
    "CreateSmbFileShareResult",
    "CreateSnapshotFromVolumeRecoveryPointResult",
    "CreateStoredIscsiVolumeResult",
    "CreateTapePoolResult",
    "CreateTapeWithBarcodeResult",
    "CreateTapesResult",
    "DeleteAutomaticTapeCreationPolicyResult",
    "DeleteBandwidthRateLimitResult",
    "DeleteCacheReportResult",
    "DeleteChapCredentialsResult",
    "DeleteSnapshotScheduleResult",
    "DeleteTapeArchiveResult",
    "DeleteTapePoolResult",
    "DeleteTapeResult",
    "DeleteVolumeResult",
    "DescribeAvailabilityMonitorTestResult",
    "DescribeBandwidthRateLimitResult",
    "DescribeBandwidthRateLimitScheduleResult",
    "DescribeCacheReportResult",
    "DescribeCacheResult",
    "DescribeCachedIscsiVolumesResult",
    "DescribeChapCredentialsResult",
    "DescribeFileSystemAssociationsResult",
    "DescribeMaintenanceStartTimeResult",
    "DescribeSmbFileSharesResult",
    "DescribeSmbSettingsResult",
    "DescribeSnapshotScheduleResult",
    "DescribeTapeArchivesResult",
    "DescribeTapeRecoveryPointsResult",
    "DescribeTapesResult",
    "DescribeUploadBufferResult",
    "DescribeVtlDevicesResult",
    "DescribeWorkingStorageResult",
    "DetachVolumeResult",
    "DisableGatewayResult",
    "DisassociateFileSystemResult",
    "EvictFilesFailingUploadResult",
    "FileShareResult",
    "GatewayResult",
    "JoinDomainResult",
    "ListAutomaticTapeCreationPoliciesResult",
    "ListCacheReportsResult",
    "ListFileSystemAssociationsResult",
    "ListLocalDisksResult",
    "ListTagsForResourceResult",
    "ListTapePoolsResult",
    "ListTapesResult",
    "ListVolumeInitiatorsResult",
    "ListVolumeRecoveryPointsResult",
    "NotifyWhenUploadedResult",
    "RefreshCacheResult",
    "RemoveTagsFromResourceResult",
    "ResetCacheResult",
    "RetrieveTapeArchiveResult",
    "RetrieveTapeRecoveryPointResult",
    "SetLocalConsolePasswordResult",
    "SetSmbGuestPasswordResult",
    "SnapshotResult",
    "StartAvailabilityMonitorTestResult",
    "StartCacheReportResult",
    "StartGatewayResult",
    "UpdateAutomaticTapeCreationPolicyResult",
    "UpdateBandwidthRateLimitResult",
    "UpdateBandwidthRateLimitScheduleResult",
    "UpdateChapCredentialsResult",
    "UpdateFileSystemAssociationResult",
    "UpdateGatewayInformationResult",
    "UpdateGatewaySoftwareNowResult",
    "UpdateMaintenanceStartTimeResult",
    "UpdateSmbFileShareResult",
    "UpdateSmbFileShareVisibilityResult",
    "UpdateSmbLocalGroupsResult",
    "UpdateSmbSecurityStrategyResult",
    "UpdateSnapshotScheduleResult",
    "UpdateVtlDeviceTypeResult",
    "VolumeResult",
    "activate_gateway",
    "add_cache",
    "add_tags_to_resource",
    "add_upload_buffer",
    "add_working_storage",
    "assign_tape_pool",
    "associate_file_system",
    "attach_volume",
    "cancel_archival",
    "cancel_cache_report",
    "cancel_retrieval",
    "create_cached_iscsi_volume",
    "create_nfs_file_share",
    "create_smb_file_share",
    "create_snapshot",
    "create_snapshot_from_volume_recovery_point",
    "create_stored_iscsi_volume",
    "create_tape_pool",
    "create_tape_with_barcode",
    "create_tapes",
    "delete_automatic_tape_creation_policy",
    "delete_bandwidth_rate_limit",
    "delete_cache_report",
    "delete_chap_credentials",
    "delete_file_share",
    "delete_gateway",
    "delete_snapshot_schedule",
    "delete_tape",
    "delete_tape_archive",
    "delete_tape_pool",
    "delete_volume",
    "describe_availability_monitor_test",
    "describe_bandwidth_rate_limit",
    "describe_bandwidth_rate_limit_schedule",
    "describe_cache",
    "describe_cache_report",
    "describe_cached_iscsi_volumes",
    "describe_chap_credentials",
    "describe_file_system_associations",
    "describe_gateway_information",
    "describe_maintenance_start_time",
    "describe_nfs_file_shares",
    "describe_smb_file_shares",
    "describe_smb_settings",
    "describe_snapshot_schedule",
    "describe_snapshots",
    "describe_stored_iscsi_volumes",
    "describe_tape_archives",
    "describe_tape_recovery_points",
    "describe_tapes",
    "describe_upload_buffer",
    "describe_vtl_devices",
    "describe_working_storage",
    "detach_volume",
    "disable_gateway",
    "disassociate_file_system",
    "evict_files_failing_upload",
    "join_domain",
    "list_automatic_tape_creation_policies",
    "list_cache_reports",
    "list_file_shares",
    "list_file_system_associations",
    "list_gateways",
    "list_local_disks",
    "list_tags_for_resource",
    "list_tape_pools",
    "list_tapes",
    "list_volume_initiators",
    "list_volume_recovery_points",
    "list_volumes",
    "notify_when_uploaded",
    "refresh_cache",
    "remove_tags_from_resource",
    "reset_cache",
    "retrieve_tape_archive",
    "retrieve_tape_recovery_point",
    "set_local_console_password",
    "set_smb_guest_password",
    "shutdown_gateway",
    "start_availability_monitor_test",
    "start_cache_report",
    "start_gateway",
    "update_automatic_tape_creation_policy",
    "update_bandwidth_rate_limit",
    "update_bandwidth_rate_limit_schedule",
    "update_chap_credentials",
    "update_file_system_association",
    "update_gateway_information",
    "update_gateway_software_now",
    "update_maintenance_start_time",
    "update_nfs_file_share",
    "update_smb_file_share",
    "update_smb_file_share_visibility",
    "update_smb_local_groups",
    "update_smb_security_strategy",
    "update_snapshot_schedule",
    "update_vtl_device_type",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class GatewayResult(BaseModel):
    """Metadata for a Storage Gateway."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str
    gateway_id: str | None = None
    gateway_name: str | None = None
    gateway_type: str | None = None
    gateway_state: str | None = None
    gateway_timezone: str | None = None
    extra: dict[str, Any] = {}


class FileShareResult(BaseModel):
    """Metadata for an NFS file share."""

    model_config = ConfigDict(frozen=True)

    file_share_arn: str
    file_share_id: str | None = None
    file_share_status: str | None = None
    gateway_arn: str | None = None
    location_arn: str | None = None
    role: str | None = None
    path: str | None = None
    extra: dict[str, Any] = {}


class VolumeResult(BaseModel):
    """Metadata for a stored iSCSI volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str
    volume_id: str | None = None
    volume_type: str | None = None
    volume_status: str | None = None
    volume_size_in_bytes: int | None = None
    extra: dict[str, Any] = {}


class SnapshotResult(BaseModel):
    """Metadata for a volume snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    volume_arn: str | None = None
    snapshot_description: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal parsers
# ---------------------------------------------------------------------------


def _parse_gateway(gw: dict[str, Any]) -> GatewayResult:
    """Convert a raw gateway dict to a :class:`GatewayResult`."""
    known = {
        "GatewayARN",
        "GatewayId",
        "GatewayName",
        "GatewayType",
        "GatewayState",
        "GatewayTimezone",
    }
    return GatewayResult(
        gateway_arn=gw["GatewayARN"],
        gateway_id=gw.get("GatewayId"),
        gateway_name=gw.get("GatewayName"),
        gateway_type=gw.get("GatewayType"),
        gateway_state=gw.get("GatewayState"),
        gateway_timezone=gw.get("GatewayTimezone"),
        extra={k: v for k, v in gw.items() if k not in known},
    )


def _parse_file_share(fs: dict[str, Any]) -> FileShareResult:
    """Convert a raw NFS file-share dict to a :class:`FileShareResult`."""
    known = {
        "FileShareARN",
        "FileShareId",
        "FileShareStatus",
        "GatewayARN",
        "LocationARN",
        "Role",
        "Path",
    }
    return FileShareResult(
        file_share_arn=fs["FileShareARN"],
        file_share_id=fs.get("FileShareId"),
        file_share_status=fs.get("FileShareStatus"),
        gateway_arn=fs.get("GatewayARN"),
        location_arn=fs.get("LocationARN"),
        role=fs.get("Role"),
        path=fs.get("Path"),
        extra={k: v for k, v in fs.items() if k not in known},
    )


def _parse_volume(vol: dict[str, Any]) -> VolumeResult:
    """Convert a raw volume dict to a :class:`VolumeResult`."""
    known = {
        "VolumeARN",
        "VolumeId",
        "VolumeType",
        "VolumeStatus",
        "VolumeSizeInBytes",
    }
    return VolumeResult(
        volume_arn=vol["VolumeARN"],
        volume_id=vol.get("VolumeId"),
        volume_type=vol.get("VolumeType"),
        volume_status=vol.get("VolumeStatus"),
        volume_size_in_bytes=vol.get("VolumeSizeInBytes"),
        extra={k: v for k, v in vol.items() if k not in known},
    )


def _parse_snapshot(snap: dict[str, Any]) -> SnapshotResult:
    """Convert a raw snapshot dict to a :class:`SnapshotResult`."""
    known = {"SnapshotId", "VolumeARN", "SnapshotDescription"}
    return SnapshotResult(
        snapshot_id=snap["SnapshotId"],
        volume_arn=snap.get("VolumeARN"),
        snapshot_description=snap.get("SnapshotDescription"),
        extra={k: v for k, v in snap.items() if k not in known},
    )


# ---------------------------------------------------------------------------
# Gateway operations
# ---------------------------------------------------------------------------


def activate_gateway(
    *,
    activation_key: str,
    gateway_name: str,
    gateway_timezone: str,
    gateway_region: str,
    gateway_type: str = "FILE_S3",
    region_name: str | None = None,
) -> str:
    """Activate a Storage Gateway and return the gateway ARN.

    Args:
        activation_key: The activation key obtained from the gateway VM.
        gateway_name: A human-readable name for the gateway.
        gateway_timezone: Timezone, e.g. ``"GMT-5:00"``.
        gateway_region: AWS region for the gateway.
        gateway_type: Gateway type (``"FILE_S3"``, ``"STORED"``, etc.).
        region_name: AWS region override for the API call.

    Returns:
        The ARN of the activated gateway.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.activate_gateway(
            ActivationKey=activation_key,
            GatewayName=gateway_name,
            GatewayTimezone=gateway_timezone,
            GatewayRegion=gateway_region,
            GatewayType=gateway_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "activate_gateway failed") from exc
    return resp["GatewayARN"]


def describe_gateway_information(
    gateway_arn: str,
    *,
    region_name: str | None = None,
) -> GatewayResult:
    """Describe a single Storage Gateway.

    Args:
        gateway_arn: The ARN of the gateway to describe.
        region_name: AWS region override.

    Returns:
        A :class:`GatewayResult` with gateway metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.describe_gateway_information(GatewayARN=gateway_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_gateway_information failed") from exc
    return _parse_gateway(resp)


def list_gateways(
    *,
    region_name: str | None = None,
) -> list[GatewayResult]:
    """List all Storage Gateways in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`GatewayResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    results: list[GatewayResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_gateways(**kwargs)
            for gw in resp.get("Gateways", []):
                results.append(_parse_gateway(gw))
            marker = resp.get("Marker")
            if not marker:
                break
            kwargs["Marker"] = marker
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_gateways failed") from exc
    return results


def delete_gateway(
    gateway_arn: str,
    *,
    region_name: str | None = None,
) -> str:
    """Delete a Storage Gateway.

    Args:
        gateway_arn: The ARN of the gateway to delete.
        region_name: AWS region override.

    Returns:
        The ARN of the deleted gateway.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.delete_gateway(GatewayARN=gateway_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_gateway failed") from exc
    return resp["GatewayARN"]


def shutdown_gateway(
    gateway_arn: str,
    *,
    region_name: str | None = None,
) -> str:
    """Shut down a Storage Gateway.

    Args:
        gateway_arn: The ARN of the gateway to shut down.
        region_name: AWS region override.

    Returns:
        The ARN of the shut-down gateway.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.shutdown_gateway(GatewayARN=gateway_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "shutdown_gateway failed") from exc
    return resp["GatewayARN"]


# ---------------------------------------------------------------------------
# NFS file-share operations
# ---------------------------------------------------------------------------


def create_nfs_file_share(
    *,
    client_token: str,
    gateway_arn: str,
    role: str,
    location_arn: str,
    default_storage_class: str = "S3_STANDARD",
    region_name: str | None = None,
) -> FileShareResult:
    """Create an NFS file share on a file gateway.

    Args:
        client_token: Idempotency token.
        gateway_arn: The gateway ARN hosting the share.
        role: IAM role ARN granting access to S3.
        location_arn: S3 bucket ARN for the share.
        default_storage_class: S3 storage class for new objects.
        region_name: AWS region override.

    Returns:
        A :class:`FileShareResult` for the new file share.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.create_nfs_file_share(
            ClientToken=client_token,
            GatewayARN=gateway_arn,
            Role=role,
            LocationARN=location_arn,
            DefaultStorageClass=default_storage_class,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_nfs_file_share failed") from exc
    return _parse_file_share(resp.get("NFSFileShareDefaults", resp))


def describe_nfs_file_shares(
    file_share_arns: list[str],
    *,
    region_name: str | None = None,
) -> list[FileShareResult]:
    """Describe one or more NFS file shares.

    Args:
        file_share_arns: List of file-share ARNs to describe.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileShareResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.describe_nfs_file_shares(
            FileShareARNList=file_share_arns,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_nfs_file_shares failed") from exc
    return [_parse_file_share(fs) for fs in resp.get("NFSFileShareInfoList", [])]


def update_nfs_file_share(
    file_share_arn: str,
    *,
    default_storage_class: str | None = None,
    kms_encrypted: bool | None = None,
    region_name: str | None = None,
) -> FileShareResult:
    """Update an NFS file share.

    Args:
        file_share_arn: The ARN of the file share to update.
        default_storage_class: New S3 storage class.
        kms_encrypted: Whether to enable KMS encryption.
        region_name: AWS region override.

    Returns:
        A :class:`FileShareResult` with the updated file share ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {"FileShareARN": file_share_arn}
    if default_storage_class is not None:
        kwargs["DefaultStorageClass"] = default_storage_class
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    try:
        resp = client.update_nfs_file_share(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_nfs_file_share failed") from exc
    return FileShareResult(file_share_arn=resp["FileShareARN"])


def delete_file_share(
    file_share_arn: str,
    *,
    force_delete: bool = False,
    region_name: str | None = None,
) -> str:
    """Delete a file share.

    Args:
        file_share_arn: The ARN of the file share to delete.
        force_delete: Whether to force-delete the share.
        region_name: AWS region override.

    Returns:
        The ARN of the deleted file share.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.delete_file_share(
            FileShareARN=file_share_arn,
            ForceDelete=force_delete,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_file_share failed") from exc
    return resp["FileShareARN"]


def list_file_shares(
    *,
    gateway_arn: str | None = None,
    region_name: str | None = None,
) -> list[FileShareResult]:
    """List file shares, optionally filtered by gateway.

    Args:
        gateway_arn: Filter by gateway ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileShareResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if gateway_arn is not None:
        kwargs["GatewayARN"] = gateway_arn
    results: list[FileShareResult] = []
    try:
        while True:
            resp = client.list_file_shares(**kwargs)
            for fs in resp.get("FileShareInfoList", []):
                results.append(_parse_file_share(fs))
            marker = resp.get("NextMarker")
            if not marker:
                break
            kwargs["Marker"] = marker
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_file_shares failed") from exc
    return results


# ---------------------------------------------------------------------------
# Volume operations
# ---------------------------------------------------------------------------


def list_volumes(
    *,
    gateway_arn: str | None = None,
    region_name: str | None = None,
) -> list[VolumeResult]:
    """List gateway volumes.

    Args:
        gateway_arn: Filter by gateway ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`VolumeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if gateway_arn is not None:
        kwargs["GatewayARN"] = gateway_arn
    results: list[VolumeResult] = []
    try:
        while True:
            resp = client.list_volumes(**kwargs)
            for vol in resp.get("VolumeInfos", []):
                results.append(_parse_volume(vol))
            marker = resp.get("Marker")
            if not marker:
                break
            kwargs["Marker"] = marker
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_volumes failed") from exc
    return results


def describe_stored_iscsi_volumes(
    volume_arns: list[str],
    *,
    region_name: str | None = None,
) -> list[VolumeResult]:
    """Describe stored iSCSI volumes.

    Args:
        volume_arns: List of volume ARNs to describe.
        region_name: AWS region override.

    Returns:
        A list of :class:`VolumeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.describe_stored_iscsi_volumes(VolumeARNs=volume_arns)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_stored_iscsi_volumes failed") from exc
    return [_parse_volume(vol) for vol in resp.get("StorediSCSIVolumes", [])]


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


def create_snapshot(
    volume_arn: str,
    *,
    snapshot_description: str = "",
    region_name: str | None = None,
) -> SnapshotResult:
    """Create a snapshot of a gateway volume.

    Args:
        volume_arn: The ARN of the volume to snapshot.
        snapshot_description: Optional description.
        region_name: AWS region override.

    Returns:
        A :class:`SnapshotResult` for the new snapshot.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.create_snapshot(
            VolumeARN=volume_arn,
            SnapshotDescription=snapshot_description,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_snapshot failed") from exc
    return SnapshotResult(
        snapshot_id=resp["SnapshotId"],
        volume_arn=resp.get("VolumeARN"),
        snapshot_description=snapshot_description,
    )


def describe_snapshots(
    volume_arn: str,
    *,
    region_name: str | None = None,
) -> list[SnapshotResult]:
    """Describe snapshots for a volume.

    Args:
        volume_arn: The volume ARN whose snapshots to list.
        region_name: AWS region override.

    Returns:
        A list of :class:`SnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    try:
        resp = client.describe_snapshot_schedule(VolumeARN=volume_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_snapshots failed") from exc
    result = SnapshotResult(
        snapshot_id=resp.get("VolumeARN", volume_arn),
        volume_arn=resp.get("VolumeARN"),
        snapshot_description=resp.get("Description"),
        extra={k: v for k, v in resp.items() if k not in {"VolumeARN", "Description"}},
    )
    return [result]


class AddCacheResult(BaseModel):
    """Result of add_cache."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class AddTagsToResourceResult(BaseModel):
    """Result of add_tags_to_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None


class AddUploadBufferResult(BaseModel):
    """Result of add_upload_buffer."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class AddWorkingStorageResult(BaseModel):
    """Result of add_working_storage."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class AssignTapePoolResult(BaseModel):
    """Result of assign_tape_pool."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class AssociateFileSystemResult(BaseModel):
    """Result of associate_file_system."""

    model_config = ConfigDict(frozen=True)

    file_system_association_arn: str | None = None


class AttachVolumeResult(BaseModel):
    """Result of attach_volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None
    target_arn: str | None = None


class CancelArchivalResult(BaseModel):
    """Result of cancel_archival."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class CancelCacheReportResult(BaseModel):
    """Result of cancel_cache_report."""

    model_config = ConfigDict(frozen=True)

    cache_report_arn: str | None = None


class CancelRetrievalResult(BaseModel):
    """Result of cancel_retrieval."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class CreateCachedIscsiVolumeResult(BaseModel):
    """Result of create_cached_iscsi_volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None
    target_arn: str | None = None


class CreateSmbFileShareResult(BaseModel):
    """Result of create_smb_file_share."""

    model_config = ConfigDict(frozen=True)

    file_share_arn: str | None = None


class CreateSnapshotFromVolumeRecoveryPointResult(BaseModel):
    """Result of create_snapshot_from_volume_recovery_point."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str | None = None
    volume_arn: str | None = None
    volume_recovery_point_time: str | None = None


class CreateStoredIscsiVolumeResult(BaseModel):
    """Result of create_stored_iscsi_volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None
    volume_size_in_bytes: int | None = None
    target_arn: str | None = None


class CreateTapePoolResult(BaseModel):
    """Result of create_tape_pool."""

    model_config = ConfigDict(frozen=True)

    pool_arn: str | None = None


class CreateTapeWithBarcodeResult(BaseModel):
    """Result of create_tape_with_barcode."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class CreateTapesResult(BaseModel):
    """Result of create_tapes."""

    model_config = ConfigDict(frozen=True)

    tape_ar_ns: list[str] | None = None


class DeleteAutomaticTapeCreationPolicyResult(BaseModel):
    """Result of delete_automatic_tape_creation_policy."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class DeleteBandwidthRateLimitResult(BaseModel):
    """Result of delete_bandwidth_rate_limit."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class DeleteCacheReportResult(BaseModel):
    """Result of delete_cache_report."""

    model_config = ConfigDict(frozen=True)

    cache_report_arn: str | None = None


class DeleteChapCredentialsResult(BaseModel):
    """Result of delete_chap_credentials."""

    model_config = ConfigDict(frozen=True)

    target_arn: str | None = None
    initiator_name: str | None = None


class DeleteSnapshotScheduleResult(BaseModel):
    """Result of delete_snapshot_schedule."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None


class DeleteTapeResult(BaseModel):
    """Result of delete_tape."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class DeleteTapeArchiveResult(BaseModel):
    """Result of delete_tape_archive."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class DeleteTapePoolResult(BaseModel):
    """Result of delete_tape_pool."""

    model_config = ConfigDict(frozen=True)

    pool_arn: str | None = None


class DeleteVolumeResult(BaseModel):
    """Result of delete_volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None


class DescribeAvailabilityMonitorTestResult(BaseModel):
    """Result of describe_availability_monitor_test."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    status: str | None = None
    start_time: str | None = None


class DescribeBandwidthRateLimitResult(BaseModel):
    """Result of describe_bandwidth_rate_limit."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    average_upload_rate_limit_in_bits_per_sec: int | None = None
    average_download_rate_limit_in_bits_per_sec: int | None = None


class DescribeBandwidthRateLimitScheduleResult(BaseModel):
    """Result of describe_bandwidth_rate_limit_schedule."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    bandwidth_rate_limit_intervals: list[dict[str, Any]] | None = None


class DescribeCacheResult(BaseModel):
    """Result of describe_cache."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    disk_ids: list[str] | None = None
    cache_allocated_in_bytes: int | None = None
    cache_used_percentage: float | None = None
    cache_dirty_percentage: float | None = None
    cache_hit_percentage: float | None = None
    cache_miss_percentage: float | None = None


class DescribeCacheReportResult(BaseModel):
    """Result of describe_cache_report."""

    model_config = ConfigDict(frozen=True)

    cache_report_info: dict[str, Any] | None = None


class DescribeCachedIscsiVolumesResult(BaseModel):
    """Result of describe_cached_iscsi_volumes."""

    model_config = ConfigDict(frozen=True)

    cachedi_scsi_volumes: list[dict[str, Any]] | None = None


class DescribeChapCredentialsResult(BaseModel):
    """Result of describe_chap_credentials."""

    model_config = ConfigDict(frozen=True)

    chap_credentials: list[dict[str, Any]] | None = None


class DescribeFileSystemAssociationsResult(BaseModel):
    """Result of describe_file_system_associations."""

    model_config = ConfigDict(frozen=True)

    file_system_association_info_list: list[dict[str, Any]] | None = None


class DescribeMaintenanceStartTimeResult(BaseModel):
    """Result of describe_maintenance_start_time."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    hour_of_day: int | None = None
    minute_of_hour: int | None = None
    day_of_week: int | None = None
    day_of_month: int | None = None
    timezone: str | None = None
    software_update_preferences: dict[str, Any] | None = None


class DescribeSmbFileSharesResult(BaseModel):
    """Result of describe_smb_file_shares."""

    model_config = ConfigDict(frozen=True)

    smb_file_share_info_list: list[dict[str, Any]] | None = None


class DescribeSmbSettingsResult(BaseModel):
    """Result of describe_smb_settings."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    domain_name: str | None = None
    active_directory_status: str | None = None
    smb_guest_password_set: bool | None = None
    smb_security_strategy: str | None = None
    file_shares_visible: bool | None = None
    smb_local_groups: dict[str, Any] | None = None


class DescribeSnapshotScheduleResult(BaseModel):
    """Result of describe_snapshot_schedule."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None
    start_at: int | None = None
    recurrence_in_hours: int | None = None
    description: str | None = None
    timezone: str | None = None
    tags: list[dict[str, Any]] | None = None


class DescribeTapeArchivesResult(BaseModel):
    """Result of describe_tape_archives."""

    model_config = ConfigDict(frozen=True)

    tape_archives: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeTapeRecoveryPointsResult(BaseModel):
    """Result of describe_tape_recovery_points."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    tape_recovery_point_infos: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeTapesResult(BaseModel):
    """Result of describe_tapes."""

    model_config = ConfigDict(frozen=True)

    tapes: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeUploadBufferResult(BaseModel):
    """Result of describe_upload_buffer."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    disk_ids: list[str] | None = None
    upload_buffer_used_in_bytes: int | None = None
    upload_buffer_allocated_in_bytes: int | None = None


class DescribeVtlDevicesResult(BaseModel):
    """Result of describe_vtl_devices."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    vtl_devices: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeWorkingStorageResult(BaseModel):
    """Result of describe_working_storage."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    disk_ids: list[str] | None = None
    working_storage_used_in_bytes: int | None = None
    working_storage_allocated_in_bytes: int | None = None


class DetachVolumeResult(BaseModel):
    """Result of detach_volume."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None


class DisableGatewayResult(BaseModel):
    """Result of disable_gateway."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class DisassociateFileSystemResult(BaseModel):
    """Result of disassociate_file_system."""

    model_config = ConfigDict(frozen=True)

    file_system_association_arn: str | None = None


class EvictFilesFailingUploadResult(BaseModel):
    """Result of evict_files_failing_upload."""

    model_config = ConfigDict(frozen=True)

    notification_id: str | None = None


class JoinDomainResult(BaseModel):
    """Result of join_domain."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    active_directory_status: str | None = None


class ListAutomaticTapeCreationPoliciesResult(BaseModel):
    """Result of list_automatic_tape_creation_policies."""

    model_config = ConfigDict(frozen=True)

    automatic_tape_creation_policy_infos: list[dict[str, Any]] | None = None


class ListCacheReportsResult(BaseModel):
    """Result of list_cache_reports."""

    model_config = ConfigDict(frozen=True)

    cache_report_list: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListFileSystemAssociationsResult(BaseModel):
    """Result of list_file_system_associations."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    next_marker: str | None = None
    file_system_association_summary_list: list[dict[str, Any]] | None = None


class ListLocalDisksResult(BaseModel):
    """Result of list_local_disks."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    disks: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    marker: str | None = None
    tags: list[dict[str, Any]] | None = None


class ListTapePoolsResult(BaseModel):
    """Result of list_tape_pools."""

    model_config = ConfigDict(frozen=True)

    pool_infos: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListTapesResult(BaseModel):
    """Result of list_tapes."""

    model_config = ConfigDict(frozen=True)

    tape_infos: list[dict[str, Any]] | None = None
    marker: str | None = None


class ListVolumeInitiatorsResult(BaseModel):
    """Result of list_volume_initiators."""

    model_config = ConfigDict(frozen=True)

    initiators: list[str] | None = None


class ListVolumeRecoveryPointsResult(BaseModel):
    """Result of list_volume_recovery_points."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    volume_recovery_point_infos: list[dict[str, Any]] | None = None


class NotifyWhenUploadedResult(BaseModel):
    """Result of notify_when_uploaded."""

    model_config = ConfigDict(frozen=True)

    file_share_arn: str | None = None
    notification_id: str | None = None


class RefreshCacheResult(BaseModel):
    """Result of refresh_cache."""

    model_config = ConfigDict(frozen=True)

    file_share_arn: str | None = None
    notification_id: str | None = None


class RemoveTagsFromResourceResult(BaseModel):
    """Result of remove_tags_from_resource."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None


class ResetCacheResult(BaseModel):
    """Result of reset_cache."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class RetrieveTapeArchiveResult(BaseModel):
    """Result of retrieve_tape_archive."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class RetrieveTapeRecoveryPointResult(BaseModel):
    """Result of retrieve_tape_recovery_point."""

    model_config = ConfigDict(frozen=True)

    tape_arn: str | None = None


class SetLocalConsolePasswordResult(BaseModel):
    """Result of set_local_console_password."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class SetSmbGuestPasswordResult(BaseModel):
    """Result of set_smb_guest_password."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class StartAvailabilityMonitorTestResult(BaseModel):
    """Result of start_availability_monitor_test."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class StartCacheReportResult(BaseModel):
    """Result of start_cache_report."""

    model_config = ConfigDict(frozen=True)

    cache_report_arn: str | None = None


class StartGatewayResult(BaseModel):
    """Result of start_gateway."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateAutomaticTapeCreationPolicyResult(BaseModel):
    """Result of update_automatic_tape_creation_policy."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateBandwidthRateLimitResult(BaseModel):
    """Result of update_bandwidth_rate_limit."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateBandwidthRateLimitScheduleResult(BaseModel):
    """Result of update_bandwidth_rate_limit_schedule."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateChapCredentialsResult(BaseModel):
    """Result of update_chap_credentials."""

    model_config = ConfigDict(frozen=True)

    target_arn: str | None = None
    initiator_name: str | None = None


class UpdateFileSystemAssociationResult(BaseModel):
    """Result of update_file_system_association."""

    model_config = ConfigDict(frozen=True)

    file_system_association_arn: str | None = None


class UpdateGatewayInformationResult(BaseModel):
    """Result of update_gateway_information."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None
    gateway_name: str | None = None


class UpdateGatewaySoftwareNowResult(BaseModel):
    """Result of update_gateway_software_now."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateMaintenanceStartTimeResult(BaseModel):
    """Result of update_maintenance_start_time."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateSmbFileShareResult(BaseModel):
    """Result of update_smb_file_share."""

    model_config = ConfigDict(frozen=True)

    file_share_arn: str | None = None


class UpdateSmbFileShareVisibilityResult(BaseModel):
    """Result of update_smb_file_share_visibility."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateSmbLocalGroupsResult(BaseModel):
    """Result of update_smb_local_groups."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateSmbSecurityStrategyResult(BaseModel):
    """Result of update_smb_security_strategy."""

    model_config = ConfigDict(frozen=True)

    gateway_arn: str | None = None


class UpdateSnapshotScheduleResult(BaseModel):
    """Result of update_snapshot_schedule."""

    model_config = ConfigDict(frozen=True)

    volume_arn: str | None = None


class UpdateVtlDeviceTypeResult(BaseModel):
    """Result of update_vtl_device_type."""

    model_config = ConfigDict(frozen=True)

    vtl_device_arn: str | None = None


def add_cache(
    gateway_arn: str,
    disk_ids: list[str],
    region_name: str | None = None,
) -> AddCacheResult:
    """Add cache.

    Args:
        gateway_arn: Gateway arn.
        disk_ids: Disk ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["DiskIds"] = disk_ids
    try:
        resp = client.add_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add cache") from exc
    return AddCacheResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def add_tags_to_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> AddTagsToResourceResult:
    """Add tags to resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        resp = client.add_tags_to_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add tags to resource") from exc
    return AddTagsToResourceResult(
        resource_arn=resp.get("ResourceARN"),
    )


def add_upload_buffer(
    gateway_arn: str,
    disk_ids: list[str],
    region_name: str | None = None,
) -> AddUploadBufferResult:
    """Add upload buffer.

    Args:
        gateway_arn: Gateway arn.
        disk_ids: Disk ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["DiskIds"] = disk_ids
    try:
        resp = client.add_upload_buffer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add upload buffer") from exc
    return AddUploadBufferResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def add_working_storage(
    gateway_arn: str,
    disk_ids: list[str],
    region_name: str | None = None,
) -> AddWorkingStorageResult:
    """Add working storage.

    Args:
        gateway_arn: Gateway arn.
        disk_ids: Disk ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["DiskIds"] = disk_ids
    try:
        resp = client.add_working_storage(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add working storage") from exc
    return AddWorkingStorageResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def assign_tape_pool(
    tape_arn: str,
    pool_id: str,
    *,
    bypass_governance_retention: bool | None = None,
    region_name: str | None = None,
) -> AssignTapePoolResult:
    """Assign tape pool.

    Args:
        tape_arn: Tape arn.
        pool_id: Pool id.
        bypass_governance_retention: Bypass governance retention.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TapeARN"] = tape_arn
    kwargs["PoolId"] = pool_id
    if bypass_governance_retention is not None:
        kwargs["BypassGovernanceRetention"] = bypass_governance_retention
    try:
        resp = client.assign_tape_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to assign tape pool") from exc
    return AssignTapePoolResult(
        tape_arn=resp.get("TapeARN"),
    )


def associate_file_system(
    user_name: str,
    password: str,
    client_token: str,
    gateway_arn: str,
    location_arn: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    audit_destination_arn: str | None = None,
    cache_attributes: dict[str, Any] | None = None,
    endpoint_network_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> AssociateFileSystemResult:
    """Associate file system.

    Args:
        user_name: User name.
        password: Password.
        client_token: Client token.
        gateway_arn: Gateway arn.
        location_arn: Location arn.
        tags: Tags.
        audit_destination_arn: Audit destination arn.
        cache_attributes: Cache attributes.
        endpoint_network_configuration: Endpoint network configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["Password"] = password
    kwargs["ClientToken"] = client_token
    kwargs["GatewayARN"] = gateway_arn
    kwargs["LocationARN"] = location_arn
    if tags is not None:
        kwargs["Tags"] = tags
    if audit_destination_arn is not None:
        kwargs["AuditDestinationARN"] = audit_destination_arn
    if cache_attributes is not None:
        kwargs["CacheAttributes"] = cache_attributes
    if endpoint_network_configuration is not None:
        kwargs["EndpointNetworkConfiguration"] = endpoint_network_configuration
    try:
        resp = client.associate_file_system(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate file system") from exc
    return AssociateFileSystemResult(
        file_system_association_arn=resp.get("FileSystemAssociationARN"),
    )


def attach_volume(
    gateway_arn: str,
    volume_arn: str,
    network_interface_id: str,
    *,
    target_name: str | None = None,
    disk_id: str | None = None,
    region_name: str | None = None,
) -> AttachVolumeResult:
    """Attach volume.

    Args:
        gateway_arn: Gateway arn.
        volume_arn: Volume arn.
        network_interface_id: Network interface id.
        target_name: Target name.
        disk_id: Disk id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["VolumeARN"] = volume_arn
    kwargs["NetworkInterfaceId"] = network_interface_id
    if target_name is not None:
        kwargs["TargetName"] = target_name
    if disk_id is not None:
        kwargs["DiskId"] = disk_id
    try:
        resp = client.attach_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to attach volume") from exc
    return AttachVolumeResult(
        volume_arn=resp.get("VolumeARN"),
        target_arn=resp.get("TargetARN"),
    )


def cancel_archival(
    gateway_arn: str,
    tape_arn: str,
    region_name: str | None = None,
) -> CancelArchivalResult:
    """Cancel archival.

    Args:
        gateway_arn: Gateway arn.
        tape_arn: Tape arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["TapeARN"] = tape_arn
    try:
        resp = client.cancel_archival(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel archival") from exc
    return CancelArchivalResult(
        tape_arn=resp.get("TapeARN"),
    )


def cancel_cache_report(
    cache_report_arn: str,
    region_name: str | None = None,
) -> CancelCacheReportResult:
    """Cancel cache report.

    Args:
        cache_report_arn: Cache report arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheReportARN"] = cache_report_arn
    try:
        resp = client.cancel_cache_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel cache report") from exc
    return CancelCacheReportResult(
        cache_report_arn=resp.get("CacheReportARN"),
    )


def cancel_retrieval(
    gateway_arn: str,
    tape_arn: str,
    region_name: str | None = None,
) -> CancelRetrievalResult:
    """Cancel retrieval.

    Args:
        gateway_arn: Gateway arn.
        tape_arn: Tape arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["TapeARN"] = tape_arn
    try:
        resp = client.cancel_retrieval(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel retrieval") from exc
    return CancelRetrievalResult(
        tape_arn=resp.get("TapeARN"),
    )


def create_cached_iscsi_volume(
    gateway_arn: str,
    volume_size_in_bytes: int,
    target_name: str,
    network_interface_id: str,
    client_token: str,
    *,
    snapshot_id: str | None = None,
    source_volume_arn: str | None = None,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCachedIscsiVolumeResult:
    """Create cached iscsi volume.

    Args:
        gateway_arn: Gateway arn.
        volume_size_in_bytes: Volume size in bytes.
        target_name: Target name.
        network_interface_id: Network interface id.
        client_token: Client token.
        snapshot_id: Snapshot id.
        source_volume_arn: Source volume arn.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["VolumeSizeInBytes"] = volume_size_in_bytes
    kwargs["TargetName"] = target_name
    kwargs["NetworkInterfaceId"] = network_interface_id
    kwargs["ClientToken"] = client_token
    if snapshot_id is not None:
        kwargs["SnapshotId"] = snapshot_id
    if source_volume_arn is not None:
        kwargs["SourceVolumeARN"] = source_volume_arn
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_cached_iscsi_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cached iscsi volume") from exc
    return CreateCachedIscsiVolumeResult(
        volume_arn=resp.get("VolumeARN"),
        target_arn=resp.get("TargetARN"),
    )


def create_smb_file_share(
    client_token: str,
    gateway_arn: str,
    role: str,
    location_arn: str,
    *,
    encryption_type: str | None = None,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    default_storage_class: str | None = None,
    object_acl: str | None = None,
    read_only: bool | None = None,
    guess_mime_type_enabled: bool | None = None,
    requester_pays: bool | None = None,
    smbacl_enabled: bool | None = None,
    access_based_enumeration: bool | None = None,
    admin_user_list: list[str] | None = None,
    valid_user_list: list[str] | None = None,
    invalid_user_list: list[str] | None = None,
    audit_destination_arn: str | None = None,
    authentication: str | None = None,
    case_sensitivity: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    file_share_name: str | None = None,
    cache_attributes: dict[str, Any] | None = None,
    notification_policy: str | None = None,
    vpc_endpoint_dns_name: str | None = None,
    bucket_region: str | None = None,
    oplocks_enabled: bool | None = None,
    region_name: str | None = None,
) -> CreateSmbFileShareResult:
    """Create smb file share.

    Args:
        client_token: Client token.
        gateway_arn: Gateway arn.
        role: Role.
        location_arn: Location arn.
        encryption_type: Encryption type.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        default_storage_class: Default storage class.
        object_acl: Object acl.
        read_only: Read only.
        guess_mime_type_enabled: Guess mime type enabled.
        requester_pays: Requester pays.
        smbacl_enabled: Smbacl enabled.
        access_based_enumeration: Access based enumeration.
        admin_user_list: Admin user list.
        valid_user_list: Valid user list.
        invalid_user_list: Invalid user list.
        audit_destination_arn: Audit destination arn.
        authentication: Authentication.
        case_sensitivity: Case sensitivity.
        tags: Tags.
        file_share_name: File share name.
        cache_attributes: Cache attributes.
        notification_policy: Notification policy.
        vpc_endpoint_dns_name: Vpc endpoint dns name.
        bucket_region: Bucket region.
        oplocks_enabled: Oplocks enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientToken"] = client_token
    kwargs["GatewayARN"] = gateway_arn
    kwargs["Role"] = role
    kwargs["LocationARN"] = location_arn
    if encryption_type is not None:
        kwargs["EncryptionType"] = encryption_type
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if default_storage_class is not None:
        kwargs["DefaultStorageClass"] = default_storage_class
    if object_acl is not None:
        kwargs["ObjectACL"] = object_acl
    if read_only is not None:
        kwargs["ReadOnly"] = read_only
    if guess_mime_type_enabled is not None:
        kwargs["GuessMIMETypeEnabled"] = guess_mime_type_enabled
    if requester_pays is not None:
        kwargs["RequesterPays"] = requester_pays
    if smbacl_enabled is not None:
        kwargs["SMBACLEnabled"] = smbacl_enabled
    if access_based_enumeration is not None:
        kwargs["AccessBasedEnumeration"] = access_based_enumeration
    if admin_user_list is not None:
        kwargs["AdminUserList"] = admin_user_list
    if valid_user_list is not None:
        kwargs["ValidUserList"] = valid_user_list
    if invalid_user_list is not None:
        kwargs["InvalidUserList"] = invalid_user_list
    if audit_destination_arn is not None:
        kwargs["AuditDestinationARN"] = audit_destination_arn
    if authentication is not None:
        kwargs["Authentication"] = authentication
    if case_sensitivity is not None:
        kwargs["CaseSensitivity"] = case_sensitivity
    if tags is not None:
        kwargs["Tags"] = tags
    if file_share_name is not None:
        kwargs["FileShareName"] = file_share_name
    if cache_attributes is not None:
        kwargs["CacheAttributes"] = cache_attributes
    if notification_policy is not None:
        kwargs["NotificationPolicy"] = notification_policy
    if vpc_endpoint_dns_name is not None:
        kwargs["VPCEndpointDNSName"] = vpc_endpoint_dns_name
    if bucket_region is not None:
        kwargs["BucketRegion"] = bucket_region
    if oplocks_enabled is not None:
        kwargs["OplocksEnabled"] = oplocks_enabled
    try:
        resp = client.create_smb_file_share(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create smb file share") from exc
    return CreateSmbFileShareResult(
        file_share_arn=resp.get("FileShareARN"),
    )


def create_snapshot_from_volume_recovery_point(
    volume_arn: str,
    snapshot_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateSnapshotFromVolumeRecoveryPointResult:
    """Create snapshot from volume recovery point.

    Args:
        volume_arn: Volume arn.
        snapshot_description: Snapshot description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    kwargs["SnapshotDescription"] = snapshot_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_snapshot_from_volume_recovery_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot from volume recovery point") from exc
    return CreateSnapshotFromVolumeRecoveryPointResult(
        snapshot_id=resp.get("SnapshotId"),
        volume_arn=resp.get("VolumeARN"),
        volume_recovery_point_time=resp.get("VolumeRecoveryPointTime"),
    )


def create_stored_iscsi_volume(
    gateway_arn: str,
    disk_id: str,
    preserve_existing_data: bool,
    target_name: str,
    network_interface_id: str,
    *,
    snapshot_id: str | None = None,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateStoredIscsiVolumeResult:
    """Create stored iscsi volume.

    Args:
        gateway_arn: Gateway arn.
        disk_id: Disk id.
        preserve_existing_data: Preserve existing data.
        target_name: Target name.
        network_interface_id: Network interface id.
        snapshot_id: Snapshot id.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["DiskId"] = disk_id
    kwargs["PreserveExistingData"] = preserve_existing_data
    kwargs["TargetName"] = target_name
    kwargs["NetworkInterfaceId"] = network_interface_id
    if snapshot_id is not None:
        kwargs["SnapshotId"] = snapshot_id
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_stored_iscsi_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create stored iscsi volume") from exc
    return CreateStoredIscsiVolumeResult(
        volume_arn=resp.get("VolumeARN"),
        volume_size_in_bytes=resp.get("VolumeSizeInBytes"),
        target_arn=resp.get("TargetARN"),
    )


def create_tape_pool(
    pool_name: str,
    storage_class: str,
    *,
    retention_lock_type: str | None = None,
    retention_lock_time_in_days: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTapePoolResult:
    """Create tape pool.

    Args:
        pool_name: Pool name.
        storage_class: Storage class.
        retention_lock_type: Retention lock type.
        retention_lock_time_in_days: Retention lock time in days.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    kwargs["StorageClass"] = storage_class
    if retention_lock_type is not None:
        kwargs["RetentionLockType"] = retention_lock_type
    if retention_lock_time_in_days is not None:
        kwargs["RetentionLockTimeInDays"] = retention_lock_time_in_days
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_tape_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create tape pool") from exc
    return CreateTapePoolResult(
        pool_arn=resp.get("PoolARN"),
    )


def create_tape_with_barcode(
    gateway_arn: str,
    tape_size_in_bytes: int,
    tape_barcode: str,
    *,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    pool_id: str | None = None,
    worm: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTapeWithBarcodeResult:
    """Create tape with barcode.

    Args:
        gateway_arn: Gateway arn.
        tape_size_in_bytes: Tape size in bytes.
        tape_barcode: Tape barcode.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        pool_id: Pool id.
        worm: Worm.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["TapeSizeInBytes"] = tape_size_in_bytes
    kwargs["TapeBarcode"] = tape_barcode
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if pool_id is not None:
        kwargs["PoolId"] = pool_id
    if worm is not None:
        kwargs["Worm"] = worm
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_tape_with_barcode(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create tape with barcode") from exc
    return CreateTapeWithBarcodeResult(
        tape_arn=resp.get("TapeARN"),
    )


def create_tapes(
    gateway_arn: str,
    tape_size_in_bytes: int,
    client_token: str,
    num_tapes_to_create: int,
    tape_barcode_prefix: str,
    *,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    pool_id: str | None = None,
    worm: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTapesResult:
    """Create tapes.

    Args:
        gateway_arn: Gateway arn.
        tape_size_in_bytes: Tape size in bytes.
        client_token: Client token.
        num_tapes_to_create: Num tapes to create.
        tape_barcode_prefix: Tape barcode prefix.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        pool_id: Pool id.
        worm: Worm.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["TapeSizeInBytes"] = tape_size_in_bytes
    kwargs["ClientToken"] = client_token
    kwargs["NumTapesToCreate"] = num_tapes_to_create
    kwargs["TapeBarcodePrefix"] = tape_barcode_prefix
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if pool_id is not None:
        kwargs["PoolId"] = pool_id
    if worm is not None:
        kwargs["Worm"] = worm
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_tapes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create tapes") from exc
    return CreateTapesResult(
        tape_ar_ns=resp.get("TapeARNs"),
    )


def delete_automatic_tape_creation_policy(
    gateway_arn: str,
    region_name: str | None = None,
) -> DeleteAutomaticTapeCreationPolicyResult:
    """Delete automatic tape creation policy.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.delete_automatic_tape_creation_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete automatic tape creation policy") from exc
    return DeleteAutomaticTapeCreationPolicyResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def delete_bandwidth_rate_limit(
    gateway_arn: str,
    bandwidth_type: str,
    region_name: str | None = None,
) -> DeleteBandwidthRateLimitResult:
    """Delete bandwidth rate limit.

    Args:
        gateway_arn: Gateway arn.
        bandwidth_type: Bandwidth type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["BandwidthType"] = bandwidth_type
    try:
        resp = client.delete_bandwidth_rate_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete bandwidth rate limit") from exc
    return DeleteBandwidthRateLimitResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def delete_cache_report(
    cache_report_arn: str,
    region_name: str | None = None,
) -> DeleteCacheReportResult:
    """Delete cache report.

    Args:
        cache_report_arn: Cache report arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheReportARN"] = cache_report_arn
    try:
        resp = client.delete_cache_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cache report") from exc
    return DeleteCacheReportResult(
        cache_report_arn=resp.get("CacheReportARN"),
    )


def delete_chap_credentials(
    target_arn: str,
    initiator_name: str,
    region_name: str | None = None,
) -> DeleteChapCredentialsResult:
    """Delete chap credentials.

    Args:
        target_arn: Target arn.
        initiator_name: Initiator name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetARN"] = target_arn
    kwargs["InitiatorName"] = initiator_name
    try:
        resp = client.delete_chap_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete chap credentials") from exc
    return DeleteChapCredentialsResult(
        target_arn=resp.get("TargetARN"),
        initiator_name=resp.get("InitiatorName"),
    )


def delete_snapshot_schedule(
    volume_arn: str,
    region_name: str | None = None,
) -> DeleteSnapshotScheduleResult:
    """Delete snapshot schedule.

    Args:
        volume_arn: Volume arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    try:
        resp = client.delete_snapshot_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot schedule") from exc
    return DeleteSnapshotScheduleResult(
        volume_arn=resp.get("VolumeARN"),
    )


def delete_tape(
    gateway_arn: str,
    tape_arn: str,
    *,
    bypass_governance_retention: bool | None = None,
    region_name: str | None = None,
) -> DeleteTapeResult:
    """Delete tape.

    Args:
        gateway_arn: Gateway arn.
        tape_arn: Tape arn.
        bypass_governance_retention: Bypass governance retention.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["TapeARN"] = tape_arn
    if bypass_governance_retention is not None:
        kwargs["BypassGovernanceRetention"] = bypass_governance_retention
    try:
        resp = client.delete_tape(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete tape") from exc
    return DeleteTapeResult(
        tape_arn=resp.get("TapeARN"),
    )


def delete_tape_archive(
    tape_arn: str,
    *,
    bypass_governance_retention: bool | None = None,
    region_name: str | None = None,
) -> DeleteTapeArchiveResult:
    """Delete tape archive.

    Args:
        tape_arn: Tape arn.
        bypass_governance_retention: Bypass governance retention.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TapeARN"] = tape_arn
    if bypass_governance_retention is not None:
        kwargs["BypassGovernanceRetention"] = bypass_governance_retention
    try:
        resp = client.delete_tape_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete tape archive") from exc
    return DeleteTapeArchiveResult(
        tape_arn=resp.get("TapeARN"),
    )


def delete_tape_pool(
    pool_arn: str,
    region_name: str | None = None,
) -> DeleteTapePoolResult:
    """Delete tape pool.

    Args:
        pool_arn: Pool arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolARN"] = pool_arn
    try:
        resp = client.delete_tape_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete tape pool") from exc
    return DeleteTapePoolResult(
        pool_arn=resp.get("PoolARN"),
    )


def delete_volume(
    volume_arn: str,
    region_name: str | None = None,
) -> DeleteVolumeResult:
    """Delete volume.

    Args:
        volume_arn: Volume arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    try:
        resp = client.delete_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete volume") from exc
    return DeleteVolumeResult(
        volume_arn=resp.get("VolumeARN"),
    )


def describe_availability_monitor_test(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeAvailabilityMonitorTestResult:
    """Describe availability monitor test.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_availability_monitor_test(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe availability monitor test") from exc
    return DescribeAvailabilityMonitorTestResult(
        gateway_arn=resp.get("GatewayARN"),
        status=resp.get("Status"),
        start_time=resp.get("StartTime"),
    )


def describe_bandwidth_rate_limit(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeBandwidthRateLimitResult:
    """Describe bandwidth rate limit.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_bandwidth_rate_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe bandwidth rate limit") from exc
    return DescribeBandwidthRateLimitResult(
        gateway_arn=resp.get("GatewayARN"),
        average_upload_rate_limit_in_bits_per_sec=resp.get("AverageUploadRateLimitInBitsPerSec"),
        average_download_rate_limit_in_bits_per_sec=resp.get(
            "AverageDownloadRateLimitInBitsPerSec"
        ),
    )


def describe_bandwidth_rate_limit_schedule(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeBandwidthRateLimitScheduleResult:
    """Describe bandwidth rate limit schedule.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_bandwidth_rate_limit_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe bandwidth rate limit schedule") from exc
    return DescribeBandwidthRateLimitScheduleResult(
        gateway_arn=resp.get("GatewayARN"),
        bandwidth_rate_limit_intervals=resp.get("BandwidthRateLimitIntervals"),
    )


def describe_cache(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeCacheResult:
    """Describe cache.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache") from exc
    return DescribeCacheResult(
        gateway_arn=resp.get("GatewayARN"),
        disk_ids=resp.get("DiskIds"),
        cache_allocated_in_bytes=resp.get("CacheAllocatedInBytes"),
        cache_used_percentage=resp.get("CacheUsedPercentage"),
        cache_dirty_percentage=resp.get("CacheDirtyPercentage"),
        cache_hit_percentage=resp.get("CacheHitPercentage"),
        cache_miss_percentage=resp.get("CacheMissPercentage"),
    )


def describe_cache_report(
    cache_report_arn: str,
    region_name: str | None = None,
) -> DescribeCacheReportResult:
    """Describe cache report.

    Args:
        cache_report_arn: Cache report arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheReportARN"] = cache_report_arn
    try:
        resp = client.describe_cache_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache report") from exc
    return DescribeCacheReportResult(
        cache_report_info=resp.get("CacheReportInfo"),
    )


def describe_cached_iscsi_volumes(
    volume_ar_ns: list[str],
    region_name: str | None = None,
) -> DescribeCachedIscsiVolumesResult:
    """Describe cached iscsi volumes.

    Args:
        volume_ar_ns: Volume ar ns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARNs"] = volume_ar_ns
    try:
        resp = client.describe_cached_iscsi_volumes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cached iscsi volumes") from exc
    return DescribeCachedIscsiVolumesResult(
        cachedi_scsi_volumes=resp.get("CachediSCSIVolumes"),
    )


def describe_chap_credentials(
    target_arn: str,
    region_name: str | None = None,
) -> DescribeChapCredentialsResult:
    """Describe chap credentials.

    Args:
        target_arn: Target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetARN"] = target_arn
    try:
        resp = client.describe_chap_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe chap credentials") from exc
    return DescribeChapCredentialsResult(
        chap_credentials=resp.get("ChapCredentials"),
    )


def describe_file_system_associations(
    file_system_association_arn_list: list[str],
    region_name: str | None = None,
) -> DescribeFileSystemAssociationsResult:
    """Describe file system associations.

    Args:
        file_system_association_arn_list: File system association arn list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemAssociationARNList"] = file_system_association_arn_list
    try:
        resp = client.describe_file_system_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe file system associations") from exc
    return DescribeFileSystemAssociationsResult(
        file_system_association_info_list=resp.get("FileSystemAssociationInfoList"),
    )


def describe_maintenance_start_time(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeMaintenanceStartTimeResult:
    """Describe maintenance start time.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_maintenance_start_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe maintenance start time") from exc
    return DescribeMaintenanceStartTimeResult(
        gateway_arn=resp.get("GatewayARN"),
        hour_of_day=resp.get("HourOfDay"),
        minute_of_hour=resp.get("MinuteOfHour"),
        day_of_week=resp.get("DayOfWeek"),
        day_of_month=resp.get("DayOfMonth"),
        timezone=resp.get("Timezone"),
        software_update_preferences=resp.get("SoftwareUpdatePreferences"),
    )


def describe_smb_file_shares(
    file_share_arn_list: list[str],
    region_name: str | None = None,
) -> DescribeSmbFileSharesResult:
    """Describe smb file shares.

    Args:
        file_share_arn_list: File share arn list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARNList"] = file_share_arn_list
    try:
        resp = client.describe_smb_file_shares(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe smb file shares") from exc
    return DescribeSmbFileSharesResult(
        smb_file_share_info_list=resp.get("SMBFileShareInfoList"),
    )


def describe_smb_settings(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeSmbSettingsResult:
    """Describe smb settings.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_smb_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe smb settings") from exc
    return DescribeSmbSettingsResult(
        gateway_arn=resp.get("GatewayARN"),
        domain_name=resp.get("DomainName"),
        active_directory_status=resp.get("ActiveDirectoryStatus"),
        smb_guest_password_set=resp.get("SMBGuestPasswordSet"),
        smb_security_strategy=resp.get("SMBSecurityStrategy"),
        file_shares_visible=resp.get("FileSharesVisible"),
        smb_local_groups=resp.get("SMBLocalGroups"),
    )


def describe_snapshot_schedule(
    volume_arn: str,
    region_name: str | None = None,
) -> DescribeSnapshotScheduleResult:
    """Describe snapshot schedule.

    Args:
        volume_arn: Volume arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    try:
        resp = client.describe_snapshot_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe snapshot schedule") from exc
    return DescribeSnapshotScheduleResult(
        volume_arn=resp.get("VolumeARN"),
        start_at=resp.get("StartAt"),
        recurrence_in_hours=resp.get("RecurrenceInHours"),
        description=resp.get("Description"),
        timezone=resp.get("Timezone"),
        tags=resp.get("Tags"),
    )


def describe_tape_archives(
    *,
    tape_ar_ns: list[str] | None = None,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeTapeArchivesResult:
    """Describe tape archives.

    Args:
        tape_ar_ns: Tape ar ns.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if tape_ar_ns is not None:
        kwargs["TapeARNs"] = tape_ar_ns
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_tape_archives(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe tape archives") from exc
    return DescribeTapeArchivesResult(
        tape_archives=resp.get("TapeArchives"),
        marker=resp.get("Marker"),
    )


def describe_tape_recovery_points(
    gateway_arn: str,
    *,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeTapeRecoveryPointsResult:
    """Describe tape recovery points.

    Args:
        gateway_arn: Gateway arn.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_tape_recovery_points(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe tape recovery points") from exc
    return DescribeTapeRecoveryPointsResult(
        gateway_arn=resp.get("GatewayARN"),
        tape_recovery_point_infos=resp.get("TapeRecoveryPointInfos"),
        marker=resp.get("Marker"),
    )


def describe_tapes(
    gateway_arn: str,
    *,
    tape_ar_ns: list[str] | None = None,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeTapesResult:
    """Describe tapes.

    Args:
        gateway_arn: Gateway arn.
        tape_ar_ns: Tape ar ns.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if tape_ar_ns is not None:
        kwargs["TapeARNs"] = tape_ar_ns
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_tapes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe tapes") from exc
    return DescribeTapesResult(
        tapes=resp.get("Tapes"),
        marker=resp.get("Marker"),
    )


def describe_upload_buffer(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeUploadBufferResult:
    """Describe upload buffer.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_upload_buffer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe upload buffer") from exc
    return DescribeUploadBufferResult(
        gateway_arn=resp.get("GatewayARN"),
        disk_ids=resp.get("DiskIds"),
        upload_buffer_used_in_bytes=resp.get("UploadBufferUsedInBytes"),
        upload_buffer_allocated_in_bytes=resp.get("UploadBufferAllocatedInBytes"),
    )


def describe_vtl_devices(
    gateway_arn: str,
    *,
    vtl_device_ar_ns: list[str] | None = None,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeVtlDevicesResult:
    """Describe vtl devices.

    Args:
        gateway_arn: Gateway arn.
        vtl_device_ar_ns: Vtl device ar ns.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if vtl_device_ar_ns is not None:
        kwargs["VTLDeviceARNs"] = vtl_device_ar_ns
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_vtl_devices(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe vtl devices") from exc
    return DescribeVtlDevicesResult(
        gateway_arn=resp.get("GatewayARN"),
        vtl_devices=resp.get("VTLDevices"),
        marker=resp.get("Marker"),
    )


def describe_working_storage(
    gateway_arn: str,
    region_name: str | None = None,
) -> DescribeWorkingStorageResult:
    """Describe working storage.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.describe_working_storage(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe working storage") from exc
    return DescribeWorkingStorageResult(
        gateway_arn=resp.get("GatewayARN"),
        disk_ids=resp.get("DiskIds"),
        working_storage_used_in_bytes=resp.get("WorkingStorageUsedInBytes"),
        working_storage_allocated_in_bytes=resp.get("WorkingStorageAllocatedInBytes"),
    )


def detach_volume(
    volume_arn: str,
    *,
    force_detach: bool | None = None,
    region_name: str | None = None,
) -> DetachVolumeResult:
    """Detach volume.

    Args:
        volume_arn: Volume arn.
        force_detach: Force detach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    if force_detach is not None:
        kwargs["ForceDetach"] = force_detach
    try:
        resp = client.detach_volume(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to detach volume") from exc
    return DetachVolumeResult(
        volume_arn=resp.get("VolumeARN"),
    )


def disable_gateway(
    gateway_arn: str,
    region_name: str | None = None,
) -> DisableGatewayResult:
    """Disable gateway.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.disable_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable gateway") from exc
    return DisableGatewayResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def disassociate_file_system(
    file_system_association_arn: str,
    *,
    force_delete: bool | None = None,
    region_name: str | None = None,
) -> DisassociateFileSystemResult:
    """Disassociate file system.

    Args:
        file_system_association_arn: File system association arn.
        force_delete: Force delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemAssociationARN"] = file_system_association_arn
    if force_delete is not None:
        kwargs["ForceDelete"] = force_delete
    try:
        resp = client.disassociate_file_system(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate file system") from exc
    return DisassociateFileSystemResult(
        file_system_association_arn=resp.get("FileSystemAssociationARN"),
    )


def evict_files_failing_upload(
    file_share_arn: str,
    *,
    force_remove: bool | None = None,
    region_name: str | None = None,
) -> EvictFilesFailingUploadResult:
    """Evict files failing upload.

    Args:
        file_share_arn: File share arn.
        force_remove: Force remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARN"] = file_share_arn
    if force_remove is not None:
        kwargs["ForceRemove"] = force_remove
    try:
        resp = client.evict_files_failing_upload(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to evict files failing upload") from exc
    return EvictFilesFailingUploadResult(
        notification_id=resp.get("NotificationId"),
    )


def join_domain(
    gateway_arn: str,
    domain_name: str,
    user_name: str,
    password: str,
    *,
    organizational_unit: str | None = None,
    domain_controllers: list[str] | None = None,
    timeout_in_seconds: int | None = None,
    region_name: str | None = None,
) -> JoinDomainResult:
    """Join domain.

    Args:
        gateway_arn: Gateway arn.
        domain_name: Domain name.
        user_name: User name.
        password: Password.
        organizational_unit: Organizational unit.
        domain_controllers: Domain controllers.
        timeout_in_seconds: Timeout in seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["DomainName"] = domain_name
    kwargs["UserName"] = user_name
    kwargs["Password"] = password
    if organizational_unit is not None:
        kwargs["OrganizationalUnit"] = organizational_unit
    if domain_controllers is not None:
        kwargs["DomainControllers"] = domain_controllers
    if timeout_in_seconds is not None:
        kwargs["TimeoutInSeconds"] = timeout_in_seconds
    try:
        resp = client.join_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to join domain") from exc
    return JoinDomainResult(
        gateway_arn=resp.get("GatewayARN"),
        active_directory_status=resp.get("ActiveDirectoryStatus"),
    )


def list_automatic_tape_creation_policies(
    *,
    gateway_arn: str | None = None,
    region_name: str | None = None,
) -> ListAutomaticTapeCreationPoliciesResult:
    """List automatic tape creation policies.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if gateway_arn is not None:
        kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.list_automatic_tape_creation_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automatic tape creation policies") from exc
    return ListAutomaticTapeCreationPoliciesResult(
        automatic_tape_creation_policy_infos=resp.get("AutomaticTapeCreationPolicyInfos"),
    )


def list_cache_reports(
    *,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListCacheReportsResult:
    """List cache reports.

    Args:
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_cache_reports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list cache reports") from exc
    return ListCacheReportsResult(
        cache_report_list=resp.get("CacheReportList"),
        marker=resp.get("Marker"),
    )


def list_file_system_associations(
    *,
    gateway_arn: str | None = None,
    limit: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListFileSystemAssociationsResult:
    """List file system associations.

    Args:
        gateway_arn: Gateway arn.
        limit: Limit.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if gateway_arn is not None:
        kwargs["GatewayARN"] = gateway_arn
    if limit is not None:
        kwargs["Limit"] = limit
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.list_file_system_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list file system associations") from exc
    return ListFileSystemAssociationsResult(
        marker=resp.get("Marker"),
        next_marker=resp.get("NextMarker"),
        file_system_association_summary_list=resp.get("FileSystemAssociationSummaryList"),
    )


def list_local_disks(
    gateway_arn: str,
    region_name: str | None = None,
) -> ListLocalDisksResult:
    """List local disks.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.list_local_disks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list local disks") from exc
    return ListLocalDisksResult(
        gateway_arn=resp.get("GatewayARN"),
        disks=resp.get("Disks"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        resource_arn=resp.get("ResourceARN"),
        marker=resp.get("Marker"),
        tags=resp.get("Tags"),
    )


def list_tape_pools(
    *,
    pool_ar_ns: list[str] | None = None,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTapePoolsResult:
    """List tape pools.

    Args:
        pool_ar_ns: Pool ar ns.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if pool_ar_ns is not None:
        kwargs["PoolARNs"] = pool_ar_ns
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_tape_pools(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tape pools") from exc
    return ListTapePoolsResult(
        pool_infos=resp.get("PoolInfos"),
        marker=resp.get("Marker"),
    )


def list_tapes(
    *,
    tape_ar_ns: list[str] | None = None,
    marker: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTapesResult:
    """List tapes.

    Args:
        tape_ar_ns: Tape ar ns.
        marker: Marker.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    if tape_ar_ns is not None:
        kwargs["TapeARNs"] = tape_ar_ns
    if marker is not None:
        kwargs["Marker"] = marker
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_tapes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tapes") from exc
    return ListTapesResult(
        tape_infos=resp.get("TapeInfos"),
        marker=resp.get("Marker"),
    )


def list_volume_initiators(
    volume_arn: str,
    region_name: str | None = None,
) -> ListVolumeInitiatorsResult:
    """List volume initiators.

    Args:
        volume_arn: Volume arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    try:
        resp = client.list_volume_initiators(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list volume initiators") from exc
    return ListVolumeInitiatorsResult(
        initiators=resp.get("Initiators"),
    )


def list_volume_recovery_points(
    gateway_arn: str,
    region_name: str | None = None,
) -> ListVolumeRecoveryPointsResult:
    """List volume recovery points.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.list_volume_recovery_points(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list volume recovery points") from exc
    return ListVolumeRecoveryPointsResult(
        gateway_arn=resp.get("GatewayARN"),
        volume_recovery_point_infos=resp.get("VolumeRecoveryPointInfos"),
    )


def notify_when_uploaded(
    file_share_arn: str,
    region_name: str | None = None,
) -> NotifyWhenUploadedResult:
    """Notify when uploaded.

    Args:
        file_share_arn: File share arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARN"] = file_share_arn
    try:
        resp = client.notify_when_uploaded(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to notify when uploaded") from exc
    return NotifyWhenUploadedResult(
        file_share_arn=resp.get("FileShareARN"),
        notification_id=resp.get("NotificationId"),
    )


def refresh_cache(
    file_share_arn: str,
    *,
    folder_list: list[str] | None = None,
    recursive: bool | None = None,
    region_name: str | None = None,
) -> RefreshCacheResult:
    """Refresh cache.

    Args:
        file_share_arn: File share arn.
        folder_list: Folder list.
        recursive: Recursive.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARN"] = file_share_arn
    if folder_list is not None:
        kwargs["FolderList"] = folder_list
    if recursive is not None:
        kwargs["Recursive"] = recursive
    try:
        resp = client.refresh_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to refresh cache") from exc
    return RefreshCacheResult(
        file_share_arn=resp.get("FileShareARN"),
        notification_id=resp.get("NotificationId"),
    )


def remove_tags_from_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> RemoveTagsFromResourceResult:
    """Remove tags from resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        resp = client.remove_tags_from_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return RemoveTagsFromResourceResult(
        resource_arn=resp.get("ResourceARN"),
    )


def reset_cache(
    gateway_arn: str,
    region_name: str | None = None,
) -> ResetCacheResult:
    """Reset cache.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.reset_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reset cache") from exc
    return ResetCacheResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def retrieve_tape_archive(
    tape_arn: str,
    gateway_arn: str,
    region_name: str | None = None,
) -> RetrieveTapeArchiveResult:
    """Retrieve tape archive.

    Args:
        tape_arn: Tape arn.
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TapeARN"] = tape_arn
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.retrieve_tape_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to retrieve tape archive") from exc
    return RetrieveTapeArchiveResult(
        tape_arn=resp.get("TapeARN"),
    )


def retrieve_tape_recovery_point(
    tape_arn: str,
    gateway_arn: str,
    region_name: str | None = None,
) -> RetrieveTapeRecoveryPointResult:
    """Retrieve tape recovery point.

    Args:
        tape_arn: Tape arn.
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TapeARN"] = tape_arn
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.retrieve_tape_recovery_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to retrieve tape recovery point") from exc
    return RetrieveTapeRecoveryPointResult(
        tape_arn=resp.get("TapeARN"),
    )


def set_local_console_password(
    gateway_arn: str,
    local_console_password: str,
    region_name: str | None = None,
) -> SetLocalConsolePasswordResult:
    """Set local console password.

    Args:
        gateway_arn: Gateway arn.
        local_console_password: Local console password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["LocalConsolePassword"] = local_console_password
    try:
        resp = client.set_local_console_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set local console password") from exc
    return SetLocalConsolePasswordResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def set_smb_guest_password(
    gateway_arn: str,
    password: str,
    region_name: str | None = None,
) -> SetSmbGuestPasswordResult:
    """Set smb guest password.

    Args:
        gateway_arn: Gateway arn.
        password: Password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["Password"] = password
    try:
        resp = client.set_smb_guest_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set smb guest password") from exc
    return SetSmbGuestPasswordResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def start_availability_monitor_test(
    gateway_arn: str,
    region_name: str | None = None,
) -> StartAvailabilityMonitorTestResult:
    """Start availability monitor test.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.start_availability_monitor_test(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start availability monitor test") from exc
    return StartAvailabilityMonitorTestResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def start_cache_report(
    file_share_arn: str,
    role: str,
    location_arn: str,
    bucket_region: str,
    client_token: str,
    *,
    vpc_endpoint_dns_name: str | None = None,
    inclusion_filters: list[dict[str, Any]] | None = None,
    exclusion_filters: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartCacheReportResult:
    """Start cache report.

    Args:
        file_share_arn: File share arn.
        role: Role.
        location_arn: Location arn.
        bucket_region: Bucket region.
        client_token: Client token.
        vpc_endpoint_dns_name: Vpc endpoint dns name.
        inclusion_filters: Inclusion filters.
        exclusion_filters: Exclusion filters.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARN"] = file_share_arn
    kwargs["Role"] = role
    kwargs["LocationARN"] = location_arn
    kwargs["BucketRegion"] = bucket_region
    kwargs["ClientToken"] = client_token
    if vpc_endpoint_dns_name is not None:
        kwargs["VPCEndpointDNSName"] = vpc_endpoint_dns_name
    if inclusion_filters is not None:
        kwargs["InclusionFilters"] = inclusion_filters
    if exclusion_filters is not None:
        kwargs["ExclusionFilters"] = exclusion_filters
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_cache_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start cache report") from exc
    return StartCacheReportResult(
        cache_report_arn=resp.get("CacheReportARN"),
    )


def start_gateway(
    gateway_arn: str,
    region_name: str | None = None,
) -> StartGatewayResult:
    """Start gateway.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.start_gateway(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start gateway") from exc
    return StartGatewayResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_automatic_tape_creation_policy(
    automatic_tape_creation_rules: list[dict[str, Any]],
    gateway_arn: str,
    region_name: str | None = None,
) -> UpdateAutomaticTapeCreationPolicyResult:
    """Update automatic tape creation policy.

    Args:
        automatic_tape_creation_rules: Automatic tape creation rules.
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomaticTapeCreationRules"] = automatic_tape_creation_rules
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.update_automatic_tape_creation_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update automatic tape creation policy") from exc
    return UpdateAutomaticTapeCreationPolicyResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_bandwidth_rate_limit(
    gateway_arn: str,
    *,
    average_upload_rate_limit_in_bits_per_sec: int | None = None,
    average_download_rate_limit_in_bits_per_sec: int | None = None,
    region_name: str | None = None,
) -> UpdateBandwidthRateLimitResult:
    """Update bandwidth rate limit.

    Args:
        gateway_arn: Gateway arn.
        average_upload_rate_limit_in_bits_per_sec: Average upload rate limit in bits per sec.
        average_download_rate_limit_in_bits_per_sec: Average download rate limit in bits per sec.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if average_upload_rate_limit_in_bits_per_sec is not None:
        kwargs["AverageUploadRateLimitInBitsPerSec"] = average_upload_rate_limit_in_bits_per_sec
    if average_download_rate_limit_in_bits_per_sec is not None:
        kwargs["AverageDownloadRateLimitInBitsPerSec"] = average_download_rate_limit_in_bits_per_sec
    try:
        resp = client.update_bandwidth_rate_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update bandwidth rate limit") from exc
    return UpdateBandwidthRateLimitResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_bandwidth_rate_limit_schedule(
    gateway_arn: str,
    bandwidth_rate_limit_intervals: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateBandwidthRateLimitScheduleResult:
    """Update bandwidth rate limit schedule.

    Args:
        gateway_arn: Gateway arn.
        bandwidth_rate_limit_intervals: Bandwidth rate limit intervals.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["BandwidthRateLimitIntervals"] = bandwidth_rate_limit_intervals
    try:
        resp = client.update_bandwidth_rate_limit_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update bandwidth rate limit schedule") from exc
    return UpdateBandwidthRateLimitScheduleResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_chap_credentials(
    target_arn: str,
    secret_to_authenticate_initiator: str,
    initiator_name: str,
    *,
    secret_to_authenticate_target: str | None = None,
    region_name: str | None = None,
) -> UpdateChapCredentialsResult:
    """Update chap credentials.

    Args:
        target_arn: Target arn.
        secret_to_authenticate_initiator: Secret to authenticate initiator.
        initiator_name: Initiator name.
        secret_to_authenticate_target: Secret to authenticate target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetARN"] = target_arn
    kwargs["SecretToAuthenticateInitiator"] = secret_to_authenticate_initiator
    kwargs["InitiatorName"] = initiator_name
    if secret_to_authenticate_target is not None:
        kwargs["SecretToAuthenticateTarget"] = secret_to_authenticate_target
    try:
        resp = client.update_chap_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update chap credentials") from exc
    return UpdateChapCredentialsResult(
        target_arn=resp.get("TargetARN"),
        initiator_name=resp.get("InitiatorName"),
    )


def update_file_system_association(
    file_system_association_arn: str,
    *,
    user_name: str | None = None,
    password: str | None = None,
    audit_destination_arn: str | None = None,
    cache_attributes: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateFileSystemAssociationResult:
    """Update file system association.

    Args:
        file_system_association_arn: File system association arn.
        user_name: User name.
        password: Password.
        audit_destination_arn: Audit destination arn.
        cache_attributes: Cache attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemAssociationARN"] = file_system_association_arn
    if user_name is not None:
        kwargs["UserName"] = user_name
    if password is not None:
        kwargs["Password"] = password
    if audit_destination_arn is not None:
        kwargs["AuditDestinationARN"] = audit_destination_arn
    if cache_attributes is not None:
        kwargs["CacheAttributes"] = cache_attributes
    try:
        resp = client.update_file_system_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update file system association") from exc
    return UpdateFileSystemAssociationResult(
        file_system_association_arn=resp.get("FileSystemAssociationARN"),
    )


def update_gateway_information(
    gateway_arn: str,
    *,
    gateway_name: str | None = None,
    gateway_timezone: str | None = None,
    cloud_watch_log_group_arn: str | None = None,
    gateway_capacity: str | None = None,
    region_name: str | None = None,
) -> UpdateGatewayInformationResult:
    """Update gateway information.

    Args:
        gateway_arn: Gateway arn.
        gateway_name: Gateway name.
        gateway_timezone: Gateway timezone.
        cloud_watch_log_group_arn: Cloud watch log group arn.
        gateway_capacity: Gateway capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if gateway_name is not None:
        kwargs["GatewayName"] = gateway_name
    if gateway_timezone is not None:
        kwargs["GatewayTimezone"] = gateway_timezone
    if cloud_watch_log_group_arn is not None:
        kwargs["CloudWatchLogGroupARN"] = cloud_watch_log_group_arn
    if gateway_capacity is not None:
        kwargs["GatewayCapacity"] = gateway_capacity
    try:
        resp = client.update_gateway_information(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update gateway information") from exc
    return UpdateGatewayInformationResult(
        gateway_arn=resp.get("GatewayARN"),
        gateway_name=resp.get("GatewayName"),
    )


def update_gateway_software_now(
    gateway_arn: str,
    region_name: str | None = None,
) -> UpdateGatewaySoftwareNowResult:
    """Update gateway software now.

    Args:
        gateway_arn: Gateway arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    try:
        resp = client.update_gateway_software_now(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update gateway software now") from exc
    return UpdateGatewaySoftwareNowResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_maintenance_start_time(
    gateway_arn: str,
    *,
    hour_of_day: int | None = None,
    minute_of_hour: int | None = None,
    day_of_week: int | None = None,
    day_of_month: int | None = None,
    software_update_preferences: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateMaintenanceStartTimeResult:
    """Update maintenance start time.

    Args:
        gateway_arn: Gateway arn.
        hour_of_day: Hour of day.
        minute_of_hour: Minute of hour.
        day_of_week: Day of week.
        day_of_month: Day of month.
        software_update_preferences: Software update preferences.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    if hour_of_day is not None:
        kwargs["HourOfDay"] = hour_of_day
    if minute_of_hour is not None:
        kwargs["MinuteOfHour"] = minute_of_hour
    if day_of_week is not None:
        kwargs["DayOfWeek"] = day_of_week
    if day_of_month is not None:
        kwargs["DayOfMonth"] = day_of_month
    if software_update_preferences is not None:
        kwargs["SoftwareUpdatePreferences"] = software_update_preferences
    try:
        resp = client.update_maintenance_start_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update maintenance start time") from exc
    return UpdateMaintenanceStartTimeResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_smb_file_share(
    file_share_arn: str,
    *,
    encryption_type: str | None = None,
    kms_encrypted: bool | None = None,
    kms_key: str | None = None,
    default_storage_class: str | None = None,
    object_acl: str | None = None,
    read_only: bool | None = None,
    guess_mime_type_enabled: bool | None = None,
    requester_pays: bool | None = None,
    smbacl_enabled: bool | None = None,
    access_based_enumeration: bool | None = None,
    admin_user_list: list[str] | None = None,
    valid_user_list: list[str] | None = None,
    invalid_user_list: list[str] | None = None,
    audit_destination_arn: str | None = None,
    case_sensitivity: str | None = None,
    file_share_name: str | None = None,
    cache_attributes: dict[str, Any] | None = None,
    notification_policy: str | None = None,
    oplocks_enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateSmbFileShareResult:
    """Update smb file share.

    Args:
        file_share_arn: File share arn.
        encryption_type: Encryption type.
        kms_encrypted: Kms encrypted.
        kms_key: Kms key.
        default_storage_class: Default storage class.
        object_acl: Object acl.
        read_only: Read only.
        guess_mime_type_enabled: Guess mime type enabled.
        requester_pays: Requester pays.
        smbacl_enabled: Smbacl enabled.
        access_based_enumeration: Access based enumeration.
        admin_user_list: Admin user list.
        valid_user_list: Valid user list.
        invalid_user_list: Invalid user list.
        audit_destination_arn: Audit destination arn.
        case_sensitivity: Case sensitivity.
        file_share_name: File share name.
        cache_attributes: Cache attributes.
        notification_policy: Notification policy.
        oplocks_enabled: Oplocks enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileShareARN"] = file_share_arn
    if encryption_type is not None:
        kwargs["EncryptionType"] = encryption_type
    if kms_encrypted is not None:
        kwargs["KMSEncrypted"] = kms_encrypted
    if kms_key is not None:
        kwargs["KMSKey"] = kms_key
    if default_storage_class is not None:
        kwargs["DefaultStorageClass"] = default_storage_class
    if object_acl is not None:
        kwargs["ObjectACL"] = object_acl
    if read_only is not None:
        kwargs["ReadOnly"] = read_only
    if guess_mime_type_enabled is not None:
        kwargs["GuessMIMETypeEnabled"] = guess_mime_type_enabled
    if requester_pays is not None:
        kwargs["RequesterPays"] = requester_pays
    if smbacl_enabled is not None:
        kwargs["SMBACLEnabled"] = smbacl_enabled
    if access_based_enumeration is not None:
        kwargs["AccessBasedEnumeration"] = access_based_enumeration
    if admin_user_list is not None:
        kwargs["AdminUserList"] = admin_user_list
    if valid_user_list is not None:
        kwargs["ValidUserList"] = valid_user_list
    if invalid_user_list is not None:
        kwargs["InvalidUserList"] = invalid_user_list
    if audit_destination_arn is not None:
        kwargs["AuditDestinationARN"] = audit_destination_arn
    if case_sensitivity is not None:
        kwargs["CaseSensitivity"] = case_sensitivity
    if file_share_name is not None:
        kwargs["FileShareName"] = file_share_name
    if cache_attributes is not None:
        kwargs["CacheAttributes"] = cache_attributes
    if notification_policy is not None:
        kwargs["NotificationPolicy"] = notification_policy
    if oplocks_enabled is not None:
        kwargs["OplocksEnabled"] = oplocks_enabled
    try:
        resp = client.update_smb_file_share(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update smb file share") from exc
    return UpdateSmbFileShareResult(
        file_share_arn=resp.get("FileShareARN"),
    )


def update_smb_file_share_visibility(
    gateway_arn: str,
    file_shares_visible: bool,
    region_name: str | None = None,
) -> UpdateSmbFileShareVisibilityResult:
    """Update smb file share visibility.

    Args:
        gateway_arn: Gateway arn.
        file_shares_visible: File shares visible.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["FileSharesVisible"] = file_shares_visible
    try:
        resp = client.update_smb_file_share_visibility(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update smb file share visibility") from exc
    return UpdateSmbFileShareVisibilityResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_smb_local_groups(
    gateway_arn: str,
    smb_local_groups: dict[str, Any],
    region_name: str | None = None,
) -> UpdateSmbLocalGroupsResult:
    """Update smb local groups.

    Args:
        gateway_arn: Gateway arn.
        smb_local_groups: Smb local groups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["SMBLocalGroups"] = smb_local_groups
    try:
        resp = client.update_smb_local_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update smb local groups") from exc
    return UpdateSmbLocalGroupsResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_smb_security_strategy(
    gateway_arn: str,
    smb_security_strategy: str,
    region_name: str | None = None,
) -> UpdateSmbSecurityStrategyResult:
    """Update smb security strategy.

    Args:
        gateway_arn: Gateway arn.
        smb_security_strategy: Smb security strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GatewayARN"] = gateway_arn
    kwargs["SMBSecurityStrategy"] = smb_security_strategy
    try:
        resp = client.update_smb_security_strategy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update smb security strategy") from exc
    return UpdateSmbSecurityStrategyResult(
        gateway_arn=resp.get("GatewayARN"),
    )


def update_snapshot_schedule(
    volume_arn: str,
    start_at: int,
    recurrence_in_hours: int,
    *,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateSnapshotScheduleResult:
    """Update snapshot schedule.

    Args:
        volume_arn: Volume arn.
        start_at: Start at.
        recurrence_in_hours: Recurrence in hours.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VolumeARN"] = volume_arn
    kwargs["StartAt"] = start_at
    kwargs["RecurrenceInHours"] = recurrence_in_hours
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.update_snapshot_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update snapshot schedule") from exc
    return UpdateSnapshotScheduleResult(
        volume_arn=resp.get("VolumeARN"),
    )


def update_vtl_device_type(
    vtl_device_arn: str,
    device_type: str,
    region_name: str | None = None,
) -> UpdateVtlDeviceTypeResult:
    """Update vtl device type.

    Args:
        vtl_device_arn: Vtl device arn.
        device_type: Device type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("storagegateway", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VTLDeviceARN"] = vtl_device_arn
    kwargs["DeviceType"] = device_type
    try:
        resp = client.update_vtl_device_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update vtl device type") from exc
    return UpdateVtlDeviceTypeResult(
        vtl_device_arn=resp.get("VTLDeviceARN"),
    )
