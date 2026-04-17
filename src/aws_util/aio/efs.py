"""Native async EFS utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.efs import (
    AccessPointResult,
    CreateReplicationConfigurationResult,
    DescribeAccountPreferencesResult,
    DescribeBackupPolicyResult,
    DescribeReplicationConfigurationsResult,
    DescribeTagsResult,
    FileSystemResult,
    MountTargetResult,
    PutAccountPreferencesResult,
    PutBackupPolicyResult,
    UpdateFileSystemProtectionResult,
    _parse_access_point,
    _parse_file_system,
    _parse_mount_target,
)
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AccessPointResult",
    "CreateReplicationConfigurationResult",
    "DescribeAccountPreferencesResult",
    "DescribeBackupPolicyResult",
    "DescribeReplicationConfigurationsResult",
    "DescribeTagsResult",
    "FileSystemResult",
    "MountTargetResult",
    "PutAccountPreferencesResult",
    "PutBackupPolicyResult",
    "UpdateFileSystemProtectionResult",
    "create_access_point",
    "create_file_system",
    "create_mount_target",
    "create_replication_configuration",
    "create_tags",
    "delete_access_point",
    "delete_file_system",
    "delete_file_system_policy",
    "delete_mount_target",
    "delete_replication_configuration",
    "delete_tags",
    "describe_access_points",
    "describe_account_preferences",
    "describe_backup_policy",
    "describe_file_system_policy",
    "describe_file_systems",
    "describe_lifecycle_configuration",
    "describe_mount_target_security_groups",
    "describe_mount_targets",
    "describe_replication_configurations",
    "describe_tags",
    "list_tags_for_resource",
    "modify_mount_target_security_groups",
    "put_account_preferences",
    "put_backup_policy",
    "put_file_system_policy",
    "put_lifecycle_configuration",
    "tag_resource",
    "untag_resource",
    "update_file_system",
    "update_file_system_protection",
    "wait_for_file_system",
]


# ---------------------------------------------------------------------------
# File-system operations
# ---------------------------------------------------------------------------


async def create_file_system(
    *,
    creation_token: str | None = None,
    performance_mode: str = "generalPurpose",
    throughput_mode: str = "bursting",
    encrypted: bool = False,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> FileSystemResult:
    """Create an EFS file system.

    Args:
        creation_token: Idempotency token. Defaults to a new UUID.
        performance_mode: ``"generalPurpose"`` or ``"maxIO"``.
        throughput_mode: ``"bursting"`` or ``"provisioned"``.
        encrypted: Whether to encrypt the file system at rest.
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        A :class:`FileSystemResult` for the newly created file system.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    token = creation_token or str(uuid.uuid4())
    kwargs: dict[str, Any] = {
        "CreationToken": token,
        "PerformanceMode": performance_mode,
        "ThroughputMode": throughput_mode,
        "Encrypted": encrypted,
    }
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateFileSystem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_file_system failed") from exc
    return _parse_file_system(resp)


async def describe_file_systems(
    *,
    file_system_id: str | None = None,
    creation_token: str | None = None,
    region_name: str | None = None,
) -> list[FileSystemResult]:
    """Describe one or more EFS file systems.

    Args:
        file_system_id: Filter to a specific file-system ID.
        creation_token: Filter by creation token.
        region_name: AWS region override.

    Returns:
        A list of :class:`FileSystemResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_id:
        kwargs["FileSystemId"] = file_system_id
    if creation_token:
        kwargs["CreationToken"] = creation_token

    results: list[FileSystemResult] = []
    try:
        while True:
            resp = await client.call("DescribeFileSystems", **kwargs)
            for fs in resp.get("FileSystems", []):
                results.append(_parse_file_system(fs))
            marker = resp.get("NextMarker")
            if not marker:
                break
            kwargs["Marker"] = marker
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_file_systems failed") from exc
    return results


async def update_file_system(
    file_system_id: str,
    *,
    throughput_mode: str | None = None,
    provisioned_throughput_in_mibps: float | None = None,
    region_name: str | None = None,
) -> FileSystemResult:
    """Update an EFS file system's throughput configuration.

    Args:
        file_system_id: The file-system ID to update.
        throughput_mode: ``"bursting"`` or ``"provisioned"``.
        provisioned_throughput_in_mibps: Throughput in MiB/s when mode is
            ``"provisioned"``.
        region_name: AWS region override.

    Returns:
        The updated :class:`FileSystemResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {"FileSystemId": file_system_id}
    if throughput_mode is not None:
        kwargs["ThroughputMode"] = throughput_mode
    if provisioned_throughput_in_mibps is not None:
        kwargs["ProvisionedThroughputInMibps"] = provisioned_throughput_in_mibps
    try:
        resp = await client.call("UpdateFileSystem", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "update_file_system failed") from exc
    return _parse_file_system(resp)


async def delete_file_system(
    file_system_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an EFS file system.

    Args:
        file_system_id: The file-system ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call("DeleteFileSystem", FileSystemId=file_system_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_file_system failed") from exc


# ---------------------------------------------------------------------------
# Mount-target operations
# ---------------------------------------------------------------------------


async def create_mount_target(
    file_system_id: str,
    *,
    subnet_id: str,
    security_groups: list[str] | None = None,
    ip_address: str | None = None,
    region_name: str | None = None,
) -> MountTargetResult:
    """Create an EFS mount target in a subnet.

    Args:
        file_system_id: The file system to mount.
        subnet_id: The subnet in which to create the mount target.
        security_groups: Security group IDs to associate.
        ip_address: Specific IP address within the subnet.
        region_name: AWS region override.

    Returns:
        A :class:`MountTargetResult` for the new mount target.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {
        "FileSystemId": file_system_id,
        "SubnetId": subnet_id,
    }
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    if ip_address is not None:
        kwargs["IpAddress"] = ip_address
    try:
        resp = await client.call("CreateMountTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_mount_target failed") from exc
    return _parse_mount_target(resp)


async def describe_mount_targets(
    *,
    file_system_id: str | None = None,
    mount_target_id: str | None = None,
    region_name: str | None = None,
) -> list[MountTargetResult]:
    """Describe EFS mount targets.

    Args:
        file_system_id: Filter by file-system ID.
        mount_target_id: Filter by mount-target ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`MountTargetResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_id:
        kwargs["FileSystemId"] = file_system_id
    if mount_target_id:
        kwargs["MountTargetId"] = mount_target_id
    results: list[MountTargetResult] = []
    try:
        while True:
            resp = await client.call("DescribeMountTargets", **kwargs)
            for mt in resp.get("MountTargets", []):
                results.append(_parse_mount_target(mt))
            marker = resp.get("NextMarker")
            if not marker:
                break
            kwargs["Marker"] = marker
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_mount_targets failed") from exc
    return results


async def delete_mount_target(
    mount_target_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an EFS mount target.

    Args:
        mount_target_id: The mount-target ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call("DeleteMountTarget", MountTargetId=mount_target_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_mount_target failed") from exc


async def describe_mount_target_security_groups(
    mount_target_id: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List security groups for a mount target.

    Args:
        mount_target_id: The mount-target ID.
        region_name: AWS region override.

    Returns:
        A list of security-group IDs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        resp = await client.call(
            "DescribeMountTargetSecurityGroups",
            MountTargetId=mount_target_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_mount_target_security_groups failed") from exc
    return resp.get("SecurityGroups", [])


async def modify_mount_target_security_groups(
    mount_target_id: str,
    *,
    security_groups: list[str],
    region_name: str | None = None,
) -> None:
    """Replace security groups on a mount target.

    Args:
        mount_target_id: The mount-target ID.
        security_groups: The new security-group IDs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call(
            "ModifyMountTargetSecurityGroups",
            MountTargetId=mount_target_id,
            SecurityGroups=security_groups,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_mount_target_security_groups failed") from exc


# ---------------------------------------------------------------------------
# Access-point operations
# ---------------------------------------------------------------------------


async def create_access_point(
    file_system_id: str,
    *,
    posix_user: dict[str, Any] | None = None,
    root_directory: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AccessPointResult:
    """Create an EFS access point.

    Args:
        file_system_id: The file system for the access point.
        posix_user: POSIX user identity (``Uid``, ``Gid``, optional
            ``SecondaryGids``).
        root_directory: Root directory configuration (``Path``,
            ``CreationInfo``).
        tags: Key/value tags to apply.
        region_name: AWS region override.

    Returns:
        An :class:`AccessPointResult` for the new access point.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {"FileSystemId": file_system_id}
    if posix_user is not None:
        kwargs["PosixUser"] = posix_user
    if root_directory is not None:
        kwargs["RootDirectory"] = root_directory
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateAccessPoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_access_point failed") from exc
    return _parse_access_point(resp)


async def describe_access_points(
    *,
    file_system_id: str | None = None,
    access_point_id: str | None = None,
    region_name: str | None = None,
) -> list[AccessPointResult]:
    """Describe EFS access points.

    Args:
        file_system_id: Filter by file-system ID.
        access_point_id: Filter by access-point ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`AccessPointResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_id:
        kwargs["FileSystemId"] = file_system_id
    if access_point_id:
        kwargs["AccessPointId"] = access_point_id
    results: list[AccessPointResult] = []
    try:
        while True:
            resp = await client.call("DescribeAccessPoints", **kwargs)
            for ap in resp.get("AccessPoints", []):
                results.append(_parse_access_point(ap))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_access_points failed") from exc
    return results


async def delete_access_point(
    access_point_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an EFS access point.

    Args:
        access_point_id: The access-point ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call("DeleteAccessPoint", AccessPointId=access_point_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_access_point failed") from exc


# ---------------------------------------------------------------------------
# Lifecycle configuration
# ---------------------------------------------------------------------------


async def put_lifecycle_configuration(
    file_system_id: str,
    *,
    lifecycle_policies: list[dict[str, str]],
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """Set lifecycle policies on an EFS file system.

    Args:
        file_system_id: The file-system ID.
        lifecycle_policies: A list of lifecycle-policy dicts, e.g.
            ``[{"TransitionToIA": "AFTER_30_DAYS"}]``.
        region_name: AWS region override.

    Returns:
        The list of lifecycle policies now in effect.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        resp = await client.call(
            "PutLifecycleConfiguration",
            FileSystemId=file_system_id,
            LifecyclePolicies=lifecycle_policies,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "put_lifecycle_configuration failed") from exc
    return resp.get("LifecyclePolicies", [])


async def describe_lifecycle_configuration(
    file_system_id: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """Retrieve lifecycle policies for an EFS file system.

    Args:
        file_system_id: The file-system ID.
        region_name: AWS region override.

    Returns:
        The list of lifecycle-policy dicts currently configured.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        resp = await client.call(
            "DescribeLifecycleConfiguration",
            FileSystemId=file_system_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_lifecycle_configuration failed") from exc
    return resp.get("LifecyclePolicies", [])


# ---------------------------------------------------------------------------
# File-system policy
# ---------------------------------------------------------------------------


async def put_file_system_policy(
    file_system_id: str,
    *,
    policy: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Set a resource policy on an EFS file system.

    Args:
        file_system_id: The file-system ID.
        policy: A JSON policy document string.
        region_name: AWS region override.

    Returns:
        The response dict containing the policy details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        resp = await client.call(
            "PutFileSystemPolicy",
            FileSystemId=file_system_id,
            Policy=policy,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "put_file_system_policy failed") from exc
    return resp


async def describe_file_system_policy(
    file_system_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any] | None:
    """Retrieve the resource policy for an EFS file system.

    Args:
        file_system_id: The file-system ID.
        region_name: AWS region override.

    Returns:
        The policy response dict, or ``None`` if no policy is set.

    Raises:
        RuntimeError: If the API call fails for reasons other than a
            missing policy.
    """
    client = async_client("efs", region_name)
    try:
        resp = await client.call(
            "DescribeFileSystemPolicy",
            FileSystemId=file_system_id,
        )
    except Exception as exc:
        err_msg = str(exc)
        if "PolicyNotFound" in err_msg or "FileSystemNotFound" in err_msg:
            return None
        raise wrap_aws_error(exc, "describe_file_system_policy failed") from exc
    return resp


async def delete_file_system_policy(
    file_system_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete the resource policy from an EFS file system.

    Args:
        file_system_id: The file-system ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call("DeleteFileSystemPolicy", FileSystemId=file_system_id)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_file_system_policy failed") from exc


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


async def tag_resource(
    resource_id: str,
    *,
    tags: dict[str, str],
    region_name: str | None = None,
) -> None:
    """Add or overwrite tags on an EFS resource.

    Args:
        resource_id: The EFS resource ARN or file-system ID.
        tags: Key/value tags to set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    try:
        await client.call(
            "TagResource",
            ResourceId=resource_id,
            Tags=[{"Key": k, "Value": v} for k, v in tags.items()],
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


async def list_tags_for_resource(
    resource_id: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """List tags on an EFS resource.

    Args:
        resource_id: The EFS resource ARN or file-system ID.
        region_name: AWS region override.

    Returns:
        A dict of tag key/value pairs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    tags: dict[str, str] = {}
    try:
        kwargs: dict[str, Any] = {"ResourceId": resource_id}
        while True:
            resp = await client.call("ListTagsForResource", **kwargs)
            for tag in resp.get("Tags", []):
                tags[tag["Key"]] = tag["Value"]
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return tags


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


async def wait_for_file_system(
    file_system_id: str,
    *,
    target_state: str = "available",
    timeout: float = 300.0,
    poll_interval: float = 5.0,
    region_name: str | None = None,
) -> FileSystemResult:
    """Poll until an EFS file system reaches the desired lifecycle state.

    Args:
        file_system_id: The file-system ID to monitor.
        target_state: Desired ``LifeCycleState`` (default ``"available"``).
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
        results = await describe_file_systems(
            file_system_id=file_system_id, region_name=region_name
        )
        if not results:
            raise RuntimeError(f"File system {file_system_id!r} not found")
        fs = results[0]
        if fs.life_cycle_state == target_state:
            return fs
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"File system {file_system_id!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {fs.life_cycle_state!r})"
            )
        await asyncio.sleep(poll_interval)


async def create_replication_configuration(
    source_file_system_id: str,
    destinations: list[dict[str, Any]],
    region_name: str | None = None,
) -> CreateReplicationConfigurationResult:
    """Create replication configuration.

    Args:
        source_file_system_id: Source file system id.
        destinations: Destinations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceFileSystemId"] = source_file_system_id
    kwargs["Destinations"] = destinations
    try:
        resp = await client.call("CreateReplicationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create replication configuration") from exc
    return CreateReplicationConfigurationResult(
        source_file_system_id=resp.get("SourceFileSystemId"),
        source_file_system_region=resp.get("SourceFileSystemRegion"),
        source_file_system_arn=resp.get("SourceFileSystemArn"),
        original_source_file_system_arn=resp.get("OriginalSourceFileSystemArn"),
        creation_time=resp.get("CreationTime"),
        destinations=resp.get("Destinations"),
        source_file_system_owner_id=resp.get("SourceFileSystemOwnerId"),
    )


async def create_tags(
    file_system_id: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Create tags.

    Args:
        file_system_id: File system id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    kwargs["Tags"] = tags
    try:
        await client.call("CreateTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create tags") from exc
    return None


async def delete_replication_configuration(
    source_file_system_id: str,
    *,
    deletion_mode: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete replication configuration.

    Args:
        source_file_system_id: Source file system id.
        deletion_mode: Deletion mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceFileSystemId"] = source_file_system_id
    if deletion_mode is not None:
        kwargs["DeletionMode"] = deletion_mode
    try:
        await client.call("DeleteReplicationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete replication configuration") from exc
    return None


async def delete_tags(
    file_system_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Delete tags.

    Args:
        file_system_id: File system id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("DeleteTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete tags") from exc
    return None


async def describe_account_preferences(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeAccountPreferencesResult:
    """Describe account preferences.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeAccountPreferences", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account preferences") from exc
    return DescribeAccountPreferencesResult(
        resource_id_preference=resp.get("ResourceIdPreference"),
        next_token=resp.get("NextToken"),
    )


async def describe_backup_policy(
    file_system_id: str,
    region_name: str | None = None,
) -> DescribeBackupPolicyResult:
    """Describe backup policy.

    Args:
        file_system_id: File system id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    try:
        resp = await client.call("DescribeBackupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe backup policy") from exc
    return DescribeBackupPolicyResult(
        backup_policy=resp.get("BackupPolicy"),
    )


async def describe_replication_configurations(
    *,
    file_system_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeReplicationConfigurationsResult:
    """Describe replication configurations.

    Args:
        file_system_id: File system id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    if file_system_id is not None:
        kwargs["FileSystemId"] = file_system_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeReplicationConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replication configurations") from exc
    return DescribeReplicationConfigurationsResult(
        replications=resp.get("Replications"),
        next_token=resp.get("NextToken"),
    )


async def describe_tags(
    file_system_id: str,
    *,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeTagsResult:
    """Describe tags.

    Args:
        file_system_id: File system id.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe tags") from exc
    return DescribeTagsResult(
        marker=resp.get("Marker"),
        tags=resp.get("Tags"),
        next_marker=resp.get("NextMarker"),
    )


async def put_account_preferences(
    resource_id_type: str,
    region_name: str | None = None,
) -> PutAccountPreferencesResult:
    """Put account preferences.

    Args:
        resource_id_type: Resource id type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceIdType"] = resource_id_type
    try:
        resp = await client.call("PutAccountPreferences", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account preferences") from exc
    return PutAccountPreferencesResult(
        resource_id_preference=resp.get("ResourceIdPreference"),
    )


async def put_backup_policy(
    file_system_id: str,
    backup_policy: dict[str, Any],
    region_name: str | None = None,
) -> PutBackupPolicyResult:
    """Put backup policy.

    Args:
        file_system_id: File system id.
        backup_policy: Backup policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    kwargs["BackupPolicy"] = backup_policy
    try:
        resp = await client.call("PutBackupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put backup policy") from exc
    return PutBackupPolicyResult(
        backup_policy=resp.get("BackupPolicy"),
    )


async def untag_resource(
    resource_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_id: Resource id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_file_system_protection(
    file_system_id: str,
    *,
    replication_overwrite_protection: str | None = None,
    region_name: str | None = None,
) -> UpdateFileSystemProtectionResult:
    """Update file system protection.

    Args:
        file_system_id: File system id.
        replication_overwrite_protection: Replication overwrite protection.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("efs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileSystemId"] = file_system_id
    if replication_overwrite_protection is not None:
        kwargs["ReplicationOverwriteProtection"] = replication_overwrite_protection
    try:
        resp = await client.call("UpdateFileSystemProtection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update file system protection") from exc
    return UpdateFileSystemProtectionResult(
        replication_overwrite_protection=resp.get("ReplicationOverwriteProtection"),
    )
