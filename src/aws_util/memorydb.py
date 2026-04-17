"""aws_util.memorydb — Amazon MemoryDB utilities.

Create, describe, update, and delete MemoryDB clusters, snapshots,
users, ACLs, and subnet groups.  Includes a polling helper
(``wait_for_cluster``).
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import (
    AwsServiceError,
    AwsTimeoutError,
    wrap_aws_error,
)

__all__ = [
    "AclResult",
    "BatchUpdateClusterResult",
    "ClusterResult",
    "CreateMultiRegionClusterResult",
    "CreateParameterGroupResult",
    "DeleteMultiRegionClusterResult",
    "DeleteParameterGroupResult",
    "DeleteSubnetGroupResult",
    "DescribeEngineVersionsResult",
    "DescribeEventsResult",
    "DescribeMultiRegionClustersResult",
    "DescribeMultiRegionParameterGroupsResult",
    "DescribeMultiRegionParametersResult",
    "DescribeParameterGroupsResult",
    "DescribeParametersResult",
    "DescribeReservedNodesOfferingsResult",
    "DescribeReservedNodesResult",
    "DescribeServiceUpdatesResult",
    "FailoverShardResult",
    "ListAllowedMultiRegionClusterUpdatesResult",
    "ListAllowedNodeTypeUpdatesResult",
    "ListTagsResult",
    "PurchaseReservedNodesOfferingResult",
    "ResetParameterGroupResult",
    "SnapshotResult",
    "SubnetGroupResult",
    "TagResourceResult",
    "UntagResourceResult",
    "UpdateMultiRegionClusterResult",
    "UpdateParameterGroupResult",
    "UpdateSubnetGroupResult",
    "UserResult",
    "batch_update_cluster",
    "copy_snapshot",
    "create_acl",
    "create_cluster",
    "create_multi_region_cluster",
    "create_parameter_group",
    "create_snapshot",
    "create_subnet_group",
    "create_user",
    "delete_acl",
    "delete_cluster",
    "delete_multi_region_cluster",
    "delete_parameter_group",
    "delete_snapshot",
    "delete_subnet_group",
    "delete_user",
    "describe_acls",
    "describe_clusters",
    "describe_engine_versions",
    "describe_events",
    "describe_multi_region_clusters",
    "describe_multi_region_parameter_groups",
    "describe_multi_region_parameters",
    "describe_parameter_groups",
    "describe_parameters",
    "describe_reserved_nodes",
    "describe_reserved_nodes_offerings",
    "describe_service_updates",
    "describe_snapshots",
    "describe_subnet_groups",
    "describe_users",
    "failover_shard",
    "list_allowed_multi_region_cluster_updates",
    "list_allowed_node_type_updates",
    "list_tags",
    "purchase_reserved_nodes_offering",
    "reset_parameter_group",
    "tag_resource",
    "untag_resource",
    "update_acl",
    "update_cluster",
    "update_multi_region_cluster",
    "update_parameter_group",
    "update_subnet_group",
    "update_user",
    "wait_for_cluster",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ClusterResult(BaseModel):
    """Metadata for a MemoryDB cluster."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    status: str
    node_type: str
    engine: str | None = None
    engine_version: str | None = None
    num_shards: int | None = None
    acl_name: str | None = None
    subnet_group_name: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class SnapshotResult(BaseModel):
    """Metadata for a MemoryDB snapshot."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    status: str
    cluster_name: str | None = None
    source: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class UserResult(BaseModel):
    """Metadata for a MemoryDB user."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    status: str
    access_string: str | None = None
    acl_names: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class AclResult(BaseModel):
    """Metadata for a MemoryDB ACL."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    status: str
    user_names: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class SubnetGroupResult(BaseModel):
    """Metadata for a MemoryDB subnet group."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    description: str | None = None
    vpc_id: str | None = None
    subnet_ids: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal parsers
# ---------------------------------------------------------------------------

_CLUSTER_KEYS = {
    "Name",
    "Status",
    "NodeType",
    "Engine",
    "EngineVersion",
    "NumberOfShards",
    "ACLName",
    "SubnetGroupName",
}


def _parse_cluster(data: dict[str, Any]) -> ClusterResult:
    """Build a :class:`ClusterResult` from a raw API dict."""
    return ClusterResult(
        name=data["Name"],
        status=data.get("Status", "unknown"),
        node_type=data.get("NodeType", "unknown"),
        engine=data.get("Engine"),
        engine_version=data.get("EngineVersion"),
        num_shards=data.get("NumberOfShards"),
        acl_name=data.get("ACLName"),
        subnet_group_name=data.get("SubnetGroupName"),
        extra={k: v for k, v in data.items() if k not in _CLUSTER_KEYS},
    )


_SNAPSHOT_KEYS = {"Name", "Status", "ClusterConfiguration", "Source"}


def _parse_snapshot(data: dict[str, Any]) -> SnapshotResult:
    """Build a :class:`SnapshotResult` from a raw API dict."""
    cluster_name = None
    cc = data.get("ClusterConfiguration")
    if isinstance(cc, dict):
        cluster_name = cc.get("Name")
    return SnapshotResult(
        name=data["Name"],
        status=data.get("Status", "unknown"),
        cluster_name=cluster_name,
        source=data.get("Source"),
        extra={k: v for k, v in data.items() if k not in _SNAPSHOT_KEYS},
    )


_USER_KEYS = {"Name", "Status", "AccessString", "ACLNames"}


def _parse_user(data: dict[str, Any]) -> UserResult:
    """Build a :class:`UserResult` from a raw API dict."""
    return UserResult(
        name=data["Name"],
        status=data.get("Status", "unknown"),
        access_string=data.get("AccessString"),
        acl_names=data.get("ACLNames", []),
        extra={k: v for k, v in data.items() if k not in _USER_KEYS},
    )


_ACL_KEYS = {"Name", "Status", "UserNames"}


def _parse_acl(data: dict[str, Any]) -> AclResult:
    """Build an :class:`AclResult` from a raw API dict."""
    return AclResult(
        name=data["Name"],
        status=data.get("Status", "unknown"),
        user_names=data.get("UserNames", []),
        extra={k: v for k, v in data.items() if k not in _ACL_KEYS},
    )


_SUBNET_GROUP_KEYS = {"Name", "Description", "VpcId", "Subnets"}


def _parse_subnet_group(data: dict[str, Any]) -> SubnetGroupResult:
    """Build a :class:`SubnetGroupResult` from a raw API dict."""
    subnets = data.get("Subnets", [])
    subnet_ids = [s.get("Identifier", "") for s in subnets if isinstance(s, dict)]
    return SubnetGroupResult(
        name=data["Name"],
        description=data.get("Description"),
        vpc_id=data.get("VpcId"),
        subnet_ids=subnet_ids,
        extra={k: v for k, v in data.items() if k not in _SUBNET_GROUP_KEYS},
    )


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


def create_cluster(
    cluster_name: str,
    *,
    node_type: str = "db.r6g.large",
    acl_name: str = "open-access",
    num_shards: int | None = None,
    num_replicas_per_shard: int | None = None,
    subnet_group_name: str | None = None,
    security_group_ids: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Create a new MemoryDB cluster.

    Args:
        cluster_name: Unique cluster name.
        node_type: Node type for the cluster.
        acl_name: ACL name to associate with the cluster.
        num_shards: Number of shards.
        num_replicas_per_shard: Replicas per shard.
        subnet_group_name: Subnet group name.
        security_group_ids: VPC security group IDs.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {
        "ClusterName": cluster_name,
        "NodeType": node_type,
        "ACLName": acl_name,
    }
    if num_shards is not None:
        kwargs["NumShards"] = num_shards
    if num_replicas_per_shard is not None:
        kwargs["NumReplicasPerShard"] = num_replicas_per_shard
    if subnet_group_name is not None:
        kwargs["SubnetGroupName"] = subnet_group_name
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create cluster {cluster_name!r}") from exc
    return _parse_cluster(resp["Cluster"])


def describe_clusters(
    *,
    cluster_name: str | None = None,
    region_name: str | None = None,
) -> list[ClusterResult]:
    """Describe one or more MemoryDB clusters.

    Args:
        cluster_name: Specific cluster name. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_name is not None:
        kwargs["ClusterName"] = cluster_name
    clusters: list[ClusterResult] = []
    try:
        while True:
            resp = client.describe_clusters(**kwargs)
            for item in resp.get("Clusters", []):
                clusters.append(_parse_cluster(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_clusters failed") from exc
    return clusters


def update_cluster(
    cluster_name: str,
    *,
    node_type: str | None = None,
    acl_name: str | None = None,
    security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Update an existing MemoryDB cluster.

    Args:
        cluster_name: Cluster name.
        node_type: New node type.
        acl_name: New ACL name.
        security_group_ids: Updated security group IDs.
        region_name: AWS region override.

    Returns:
        The updated :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {"ClusterName": cluster_name}
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if acl_name is not None:
        kwargs["ACLName"] = acl_name
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    try:
        resp = client.update_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update cluster {cluster_name!r}") from exc
    return _parse_cluster(resp["Cluster"])


def delete_cluster(
    cluster_name: str,
    *,
    final_snapshot_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete a MemoryDB cluster.

    Args:
        cluster_name: Cluster name.
        final_snapshot_name: Create a final snapshot before deletion.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {"ClusterName": cluster_name}
    if final_snapshot_name is not None:
        kwargs["FinalSnapshotName"] = final_snapshot_name
    try:
        client.delete_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete cluster {cluster_name!r}") from exc


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


def create_snapshot(
    snapshot_name: str,
    *,
    cluster_name: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> SnapshotResult:
    """Create a MemoryDB snapshot.

    Args:
        snapshot_name: Unique snapshot name.
        cluster_name: Source cluster name.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`SnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {
        "SnapshotName": snapshot_name,
        "ClusterName": cluster_name,
    }
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create snapshot {snapshot_name!r}") from exc
    return _parse_snapshot(resp["Snapshot"])


def describe_snapshots(
    *,
    snapshot_name: str | None = None,
    cluster_name: str | None = None,
    region_name: str | None = None,
) -> list[SnapshotResult]:
    """Describe one or more MemoryDB snapshots.

    Args:
        snapshot_name: Specific snapshot name.
        cluster_name: Filter by source cluster.
        region_name: AWS region override.

    Returns:
        A list of :class:`SnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if snapshot_name is not None:
        kwargs["SnapshotName"] = snapshot_name
    if cluster_name is not None:
        kwargs["ClusterName"] = cluster_name
    snapshots: list[SnapshotResult] = []
    try:
        while True:
            resp = client.describe_snapshots(**kwargs)
            for item in resp.get("Snapshots", []):
                snapshots.append(_parse_snapshot(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_snapshots failed") from exc
    return snapshots


def copy_snapshot(
    source_snapshot_name: str,
    target_snapshot_name: str,
    *,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> SnapshotResult:
    """Copy a MemoryDB snapshot.

    Args:
        source_snapshot_name: Source snapshot name.
        target_snapshot_name: Target snapshot name.
        tags: Key/value tags for the copy.
        region_name: AWS region override.

    Returns:
        The copied :class:`SnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {
        "SourceSnapshotName": source_snapshot_name,
        "TargetSnapshotName": target_snapshot_name,
    }
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.copy_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to copy snapshot {source_snapshot_name!r}",
        ) from exc
    return _parse_snapshot(resp["Snapshot"])


def delete_snapshot(
    snapshot_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a MemoryDB snapshot.

    Args:
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    try:
        client.delete_snapshot(SnapshotName=snapshot_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete snapshot {snapshot_name!r}") from exc


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


def create_user(
    user_name: str,
    *,
    access_string: str = "on ~* +@all",
    authentication_mode: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> UserResult:
    """Create a MemoryDB user.

    Args:
        user_name: Unique user name.
        access_string: Redis ACL access string.
        authentication_mode: Authentication configuration.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`UserResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {
        "UserName": user_name,
        "AccessString": access_string,
    }
    if authentication_mode is not None:
        kwargs["AuthenticationMode"] = authentication_mode
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create user {user_name!r}") from exc
    return _parse_user(resp["User"])


def describe_users(
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> list[UserResult]:
    """Describe one or more MemoryDB users.

    Args:
        user_name: Specific user name. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`UserResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    users: list[UserResult] = []
    try:
        while True:
            resp = client.describe_users(**kwargs)
            for item in resp.get("Users", []):
                users.append(_parse_user(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_users failed") from exc
    return users


def update_user(
    user_name: str,
    *,
    access_string: str | None = None,
    authentication_mode: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UserResult:
    """Update a MemoryDB user.

    Args:
        user_name: User name.
        access_string: New access string.
        authentication_mode: New authentication configuration.
        region_name: AWS region override.

    Returns:
        The updated :class:`UserResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {"UserName": user_name}
    if access_string is not None:
        kwargs["AccessString"] = access_string
    if authentication_mode is not None:
        kwargs["AuthenticationMode"] = authentication_mode
    try:
        resp = client.update_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update user {user_name!r}") from exc
    return _parse_user(resp["User"])


def delete_user(
    user_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a MemoryDB user.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    try:
        client.delete_user(UserName=user_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete user {user_name!r}") from exc


# ---------------------------------------------------------------------------
# ACL operations
# ---------------------------------------------------------------------------


def create_acl(
    acl_name: str,
    *,
    user_names: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AclResult:
    """Create a MemoryDB ACL.

    Args:
        acl_name: Unique ACL name.
        user_names: Users to add to the ACL.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`AclResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {"ACLName": acl_name}
    if user_names is not None:
        kwargs["UserNames"] = user_names
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create ACL {acl_name!r}") from exc
    return _parse_acl(resp["ACL"])


def describe_acls(
    *,
    acl_name: str | None = None,
    region_name: str | None = None,
) -> list[AclResult]:
    """Describe one or more MemoryDB ACLs.

    Args:
        acl_name: Specific ACL name. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`AclResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if acl_name is not None:
        kwargs["ACLName"] = acl_name
    acls: list[AclResult] = []
    try:
        while True:
            resp = client.describe_acls(**kwargs)
            for item in resp.get("ACLs", []):
                acls.append(_parse_acl(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_acls failed") from exc
    return acls


def update_acl(
    acl_name: str,
    *,
    user_names_to_add: list[str] | None = None,
    user_names_to_remove: list[str] | None = None,
    region_name: str | None = None,
) -> AclResult:
    """Update a MemoryDB ACL.

    Args:
        acl_name: ACL name.
        user_names_to_add: Users to add.
        user_names_to_remove: Users to remove.
        region_name: AWS region override.

    Returns:
        The updated :class:`AclResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {"ACLName": acl_name}
    if user_names_to_add is not None:
        kwargs["UserNamesToAdd"] = user_names_to_add
    if user_names_to_remove is not None:
        kwargs["UserNamesToRemove"] = user_names_to_remove
    try:
        resp = client.update_acl(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to update ACL {acl_name!r}") from exc
    return _parse_acl(resp["ACL"])


def delete_acl(
    acl_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a MemoryDB ACL.

    Args:
        acl_name: ACL name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    try:
        client.delete_acl(ACLName=acl_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete ACL {acl_name!r}") from exc


# ---------------------------------------------------------------------------
# Subnet group operations
# ---------------------------------------------------------------------------


def create_subnet_group(
    subnet_group_name: str,
    *,
    subnet_ids: list[str],
    description: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> SubnetGroupResult:
    """Create a MemoryDB subnet group.

    Args:
        subnet_group_name: Unique subnet group name.
        subnet_ids: List of VPC subnet IDs.
        description: Description.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`SubnetGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {
        "SubnetGroupName": subnet_group_name,
        "SubnetIds": subnet_ids,
    }
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create subnet group {subnet_group_name!r}",
        ) from exc
    return _parse_subnet_group(resp["SubnetGroup"])


def describe_subnet_groups(
    *,
    subnet_group_name: str | None = None,
    region_name: str | None = None,
) -> list[SubnetGroupResult]:
    """Describe one or more MemoryDB subnet groups.

    Args:
        subnet_group_name: Specific subnet group name. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`SubnetGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if subnet_group_name is not None:
        kwargs["SubnetGroupName"] = subnet_group_name
    groups: list[SubnetGroupResult] = []
    try:
        while True:
            resp = client.describe_subnet_groups(**kwargs)
            for item in resp.get("SubnetGroups", []):
                groups.append(_parse_subnet_group(item))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_subnet_groups failed") from exc
    return groups


# ---------------------------------------------------------------------------
# Wait / polling helpers
# ---------------------------------------------------------------------------


def wait_for_cluster(
    cluster_name: str,
    *,
    target_status: str = "available",
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until a MemoryDB cluster reaches the target status.

    Args:
        cluster_name: Cluster name.
        target_status: Desired status (default ``"available"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` in the target status.

    Raises:
        TimeoutError: If the cluster does not reach *target_status* in time.
        RuntimeError: If the cluster is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        clusters = describe_clusters(cluster_name=cluster_name, region_name=region_name)
        if not clusters:
            raise AwsServiceError(f"Cluster {cluster_name!r} not found")
        cluster = clusters[0]
        if cluster.status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {cluster_name!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {cluster.status!r})"
            )
        time.sleep(poll_interval)


class BatchUpdateClusterResult(BaseModel):
    """Result of batch_update_cluster."""

    model_config = ConfigDict(frozen=True)

    processed_clusters: list[dict[str, Any]] | None = None
    unprocessed_clusters: list[dict[str, Any]] | None = None


class CreateMultiRegionClusterResult(BaseModel):
    """Result of create_multi_region_cluster."""

    model_config = ConfigDict(frozen=True)

    multi_region_cluster: dict[str, Any] | None = None


class CreateParameterGroupResult(BaseModel):
    """Result of create_parameter_group."""

    model_config = ConfigDict(frozen=True)

    parameter_group: dict[str, Any] | None = None


class DeleteMultiRegionClusterResult(BaseModel):
    """Result of delete_multi_region_cluster."""

    model_config = ConfigDict(frozen=True)

    multi_region_cluster: dict[str, Any] | None = None


class DeleteParameterGroupResult(BaseModel):
    """Result of delete_parameter_group."""

    model_config = ConfigDict(frozen=True)

    parameter_group: dict[str, Any] | None = None


class DeleteSubnetGroupResult(BaseModel):
    """Result of delete_subnet_group."""

    model_config = ConfigDict(frozen=True)

    subnet_group: dict[str, Any] | None = None


class DescribeEngineVersionsResult(BaseModel):
    """Result of describe_engine_versions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    engine_versions: list[dict[str, Any]] | None = None


class DescribeEventsResult(BaseModel):
    """Result of describe_events."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    events: list[dict[str, Any]] | None = None


class DescribeMultiRegionClustersResult(BaseModel):
    """Result of describe_multi_region_clusters."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    multi_region_clusters: list[dict[str, Any]] | None = None


class DescribeMultiRegionParameterGroupsResult(BaseModel):
    """Result of describe_multi_region_parameter_groups."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    multi_region_parameter_groups: list[dict[str, Any]] | None = None


class DescribeMultiRegionParametersResult(BaseModel):
    """Result of describe_multi_region_parameters."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    multi_region_parameters: list[dict[str, Any]] | None = None


class DescribeParameterGroupsResult(BaseModel):
    """Result of describe_parameter_groups."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    parameter_groups: list[dict[str, Any]] | None = None


class DescribeParametersResult(BaseModel):
    """Result of describe_parameters."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    parameters: list[dict[str, Any]] | None = None


class DescribeReservedNodesResult(BaseModel):
    """Result of describe_reserved_nodes."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reserved_nodes: list[dict[str, Any]] | None = None


class DescribeReservedNodesOfferingsResult(BaseModel):
    """Result of describe_reserved_nodes_offerings."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reserved_nodes_offerings: list[dict[str, Any]] | None = None


class DescribeServiceUpdatesResult(BaseModel):
    """Result of describe_service_updates."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    service_updates: list[dict[str, Any]] | None = None


class FailoverShardResult(BaseModel):
    """Result of failover_shard."""

    model_config = ConfigDict(frozen=True)

    cluster: dict[str, Any] | None = None


class ListAllowedMultiRegionClusterUpdatesResult(BaseModel):
    """Result of list_allowed_multi_region_cluster_updates."""

    model_config = ConfigDict(frozen=True)

    scale_up_node_types: list[str] | None = None
    scale_down_node_types: list[str] | None = None


class ListAllowedNodeTypeUpdatesResult(BaseModel):
    """Result of list_allowed_node_type_updates."""

    model_config = ConfigDict(frozen=True)

    scale_up_node_types: list[str] | None = None
    scale_down_node_types: list[str] | None = None


class ListTagsResult(BaseModel):
    """Result of list_tags."""

    model_config = ConfigDict(frozen=True)

    tag_list: list[dict[str, Any]] | None = None


class PurchaseReservedNodesOfferingResult(BaseModel):
    """Result of purchase_reserved_nodes_offering."""

    model_config = ConfigDict(frozen=True)

    reserved_node: dict[str, Any] | None = None


class ResetParameterGroupResult(BaseModel):
    """Result of reset_parameter_group."""

    model_config = ConfigDict(frozen=True)

    parameter_group: dict[str, Any] | None = None


class TagResourceResult(BaseModel):
    """Result of tag_resource."""

    model_config = ConfigDict(frozen=True)

    tag_list: list[dict[str, Any]] | None = None


class UntagResourceResult(BaseModel):
    """Result of untag_resource."""

    model_config = ConfigDict(frozen=True)

    tag_list: list[dict[str, Any]] | None = None


class UpdateMultiRegionClusterResult(BaseModel):
    """Result of update_multi_region_cluster."""

    model_config = ConfigDict(frozen=True)

    multi_region_cluster: dict[str, Any] | None = None


class UpdateParameterGroupResult(BaseModel):
    """Result of update_parameter_group."""

    model_config = ConfigDict(frozen=True)

    parameter_group: dict[str, Any] | None = None


class UpdateSubnetGroupResult(BaseModel):
    """Result of update_subnet_group."""

    model_config = ConfigDict(frozen=True)

    subnet_group: dict[str, Any] | None = None


def batch_update_cluster(
    cluster_names: list[str],
    *,
    service_update: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> BatchUpdateClusterResult:
    """Batch update cluster.

    Args:
        cluster_names: Cluster names.
        service_update: Service update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterNames"] = cluster_names
    if service_update is not None:
        kwargs["ServiceUpdate"] = service_update
    try:
        resp = client.batch_update_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update cluster") from exc
    return BatchUpdateClusterResult(
        processed_clusters=resp.get("ProcessedClusters"),
        unprocessed_clusters=resp.get("UnprocessedClusters"),
    )


def create_multi_region_cluster(
    multi_region_cluster_name_suffix: str,
    node_type: str,
    *,
    description: str | None = None,
    engine: str | None = None,
    engine_version: str | None = None,
    multi_region_parameter_group_name: str | None = None,
    num_shards: int | None = None,
    tls_enabled: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMultiRegionClusterResult:
    """Create multi region cluster.

    Args:
        multi_region_cluster_name_suffix: Multi region cluster name suffix.
        node_type: Node type.
        description: Description.
        engine: Engine.
        engine_version: Engine version.
        multi_region_parameter_group_name: Multi region parameter group name.
        num_shards: Num shards.
        tls_enabled: Tls enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MultiRegionClusterNameSuffix"] = multi_region_cluster_name_suffix
    kwargs["NodeType"] = node_type
    if description is not None:
        kwargs["Description"] = description
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if multi_region_parameter_group_name is not None:
        kwargs["MultiRegionParameterGroupName"] = multi_region_parameter_group_name
    if num_shards is not None:
        kwargs["NumShards"] = num_shards
    if tls_enabled is not None:
        kwargs["TLSEnabled"] = tls_enabled
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_multi_region_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create multi region cluster") from exc
    return CreateMultiRegionClusterResult(
        multi_region_cluster=resp.get("MultiRegionCluster"),
    )


def create_parameter_group(
    parameter_group_name: str,
    family: str,
    *,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateParameterGroupResult:
    """Create parameter group.

    Args:
        parameter_group_name: Parameter group name.
        family: Family.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    kwargs["Family"] = family
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create parameter group") from exc
    return CreateParameterGroupResult(
        parameter_group=resp.get("ParameterGroup"),
    )


def delete_multi_region_cluster(
    multi_region_cluster_name: str,
    region_name: str | None = None,
) -> DeleteMultiRegionClusterResult:
    """Delete multi region cluster.

    Args:
        multi_region_cluster_name: Multi region cluster name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MultiRegionClusterName"] = multi_region_cluster_name
    try:
        resp = client.delete_multi_region_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete multi region cluster") from exc
    return DeleteMultiRegionClusterResult(
        multi_region_cluster=resp.get("MultiRegionCluster"),
    )


def delete_parameter_group(
    parameter_group_name: str,
    region_name: str | None = None,
) -> DeleteParameterGroupResult:
    """Delete parameter group.

    Args:
        parameter_group_name: Parameter group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    try:
        resp = client.delete_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete parameter group") from exc
    return DeleteParameterGroupResult(
        parameter_group=resp.get("ParameterGroup"),
    )


def delete_subnet_group(
    subnet_group_name: str,
    region_name: str | None = None,
) -> DeleteSubnetGroupResult:
    """Delete subnet group.

    Args:
        subnet_group_name: Subnet group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubnetGroupName"] = subnet_group_name
    try:
        resp = client.delete_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete subnet group") from exc
    return DeleteSubnetGroupResult(
        subnet_group=resp.get("SubnetGroup"),
    )


def describe_engine_versions(
    *,
    engine: str | None = None,
    engine_version: str | None = None,
    parameter_group_family: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    default_only: bool | None = None,
    region_name: str | None = None,
) -> DescribeEngineVersionsResult:
    """Describe engine versions.

    Args:
        engine: Engine.
        engine_version: Engine version.
        parameter_group_family: Parameter group family.
        max_results: Max results.
        next_token: Next token.
        default_only: Default only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if parameter_group_family is not None:
        kwargs["ParameterGroupFamily"] = parameter_group_family
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if default_only is not None:
        kwargs["DefaultOnly"] = default_only
    try:
        resp = client.describe_engine_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe engine versions") from exc
    return DescribeEngineVersionsResult(
        next_token=resp.get("NextToken"),
        engine_versions=resp.get("EngineVersions"),
    )


def describe_events(
    *,
    source_name: str | None = None,
    source_type: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    duration: int | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeEventsResult:
    """Describe events.

    Args:
        source_name: Source name.
        source_type: Source type.
        start_time: Start time.
        end_time: End time.
        duration: Duration.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if source_name is not None:
        kwargs["SourceName"] = source_name
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if duration is not None:
        kwargs["Duration"] = duration
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        next_token=resp.get("NextToken"),
        events=resp.get("Events"),
    )


def describe_multi_region_clusters(
    *,
    multi_region_cluster_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    show_cluster_details: bool | None = None,
    region_name: str | None = None,
) -> DescribeMultiRegionClustersResult:
    """Describe multi region clusters.

    Args:
        multi_region_cluster_name: Multi region cluster name.
        max_results: Max results.
        next_token: Next token.
        show_cluster_details: Show cluster details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if multi_region_cluster_name is not None:
        kwargs["MultiRegionClusterName"] = multi_region_cluster_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if show_cluster_details is not None:
        kwargs["ShowClusterDetails"] = show_cluster_details
    try:
        resp = client.describe_multi_region_clusters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe multi region clusters") from exc
    return DescribeMultiRegionClustersResult(
        next_token=resp.get("NextToken"),
        multi_region_clusters=resp.get("MultiRegionClusters"),
    )


def describe_multi_region_parameter_groups(
    *,
    multi_region_parameter_group_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMultiRegionParameterGroupsResult:
    """Describe multi region parameter groups.

    Args:
        multi_region_parameter_group_name: Multi region parameter group name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if multi_region_parameter_group_name is not None:
        kwargs["MultiRegionParameterGroupName"] = multi_region_parameter_group_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_multi_region_parameter_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe multi region parameter groups") from exc
    return DescribeMultiRegionParameterGroupsResult(
        next_token=resp.get("NextToken"),
        multi_region_parameter_groups=resp.get("MultiRegionParameterGroups"),
    )


def describe_multi_region_parameters(
    multi_region_parameter_group_name: str,
    *,
    source: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeMultiRegionParametersResult:
    """Describe multi region parameters.

    Args:
        multi_region_parameter_group_name: Multi region parameter group name.
        source: Source.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MultiRegionParameterGroupName"] = multi_region_parameter_group_name
    if source is not None:
        kwargs["Source"] = source
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_multi_region_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe multi region parameters") from exc
    return DescribeMultiRegionParametersResult(
        next_token=resp.get("NextToken"),
        multi_region_parameters=resp.get("MultiRegionParameters"),
    )


def describe_parameter_groups(
    *,
    parameter_group_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeParameterGroupsResult:
    """Describe parameter groups.

    Args:
        parameter_group_name: Parameter group name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if parameter_group_name is not None:
        kwargs["ParameterGroupName"] = parameter_group_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_parameter_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe parameter groups") from exc
    return DescribeParameterGroupsResult(
        next_token=resp.get("NextToken"),
        parameter_groups=resp.get("ParameterGroups"),
    )


def describe_parameters(
    parameter_group_name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeParametersResult:
    """Describe parameters.

    Args:
        parameter_group_name: Parameter group name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe parameters") from exc
    return DescribeParametersResult(
        next_token=resp.get("NextToken"),
        parameters=resp.get("Parameters"),
    )


def describe_reserved_nodes(
    *,
    reservation_id: str | None = None,
    reserved_nodes_offering_id: str | None = None,
    node_type: str | None = None,
    duration: str | None = None,
    offering_type: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedNodesResult:
    """Describe reserved nodes.

    Args:
        reservation_id: Reservation id.
        reserved_nodes_offering_id: Reserved nodes offering id.
        node_type: Node type.
        duration: Duration.
        offering_type: Offering type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if reservation_id is not None:
        kwargs["ReservationId"] = reservation_id
    if reserved_nodes_offering_id is not None:
        kwargs["ReservedNodesOfferingId"] = reserved_nodes_offering_id
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if duration is not None:
        kwargs["Duration"] = duration
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_reserved_nodes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved nodes") from exc
    return DescribeReservedNodesResult(
        next_token=resp.get("NextToken"),
        reserved_nodes=resp.get("ReservedNodes"),
    )


def describe_reserved_nodes_offerings(
    *,
    reserved_nodes_offering_id: str | None = None,
    node_type: str | None = None,
    duration: str | None = None,
    offering_type: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedNodesOfferingsResult:
    """Describe reserved nodes offerings.

    Args:
        reserved_nodes_offering_id: Reserved nodes offering id.
        node_type: Node type.
        duration: Duration.
        offering_type: Offering type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_nodes_offering_id is not None:
        kwargs["ReservedNodesOfferingId"] = reserved_nodes_offering_id
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if duration is not None:
        kwargs["Duration"] = duration
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_reserved_nodes_offerings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved nodes offerings") from exc
    return DescribeReservedNodesOfferingsResult(
        next_token=resp.get("NextToken"),
        reserved_nodes_offerings=resp.get("ReservedNodesOfferings"),
    )


def describe_service_updates(
    *,
    service_update_name: str | None = None,
    cluster_names: list[str] | None = None,
    status: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeServiceUpdatesResult:
    """Describe service updates.

    Args:
        service_update_name: Service update name.
        cluster_names: Cluster names.
        status: Status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    if service_update_name is not None:
        kwargs["ServiceUpdateName"] = service_update_name
    if cluster_names is not None:
        kwargs["ClusterNames"] = cluster_names
    if status is not None:
        kwargs["Status"] = status
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_service_updates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe service updates") from exc
    return DescribeServiceUpdatesResult(
        next_token=resp.get("NextToken"),
        service_updates=resp.get("ServiceUpdates"),
    )


def failover_shard(
    cluster_name: str,
    shard_name: str,
    region_name: str | None = None,
) -> FailoverShardResult:
    """Failover shard.

    Args:
        cluster_name: Cluster name.
        shard_name: Shard name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterName"] = cluster_name
    kwargs["ShardName"] = shard_name
    try:
        resp = client.failover_shard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to failover shard") from exc
    return FailoverShardResult(
        cluster=resp.get("Cluster"),
    )


def list_allowed_multi_region_cluster_updates(
    multi_region_cluster_name: str,
    region_name: str | None = None,
) -> ListAllowedMultiRegionClusterUpdatesResult:
    """List allowed multi region cluster updates.

    Args:
        multi_region_cluster_name: Multi region cluster name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MultiRegionClusterName"] = multi_region_cluster_name
    try:
        resp = client.list_allowed_multi_region_cluster_updates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list allowed multi region cluster updates") from exc
    return ListAllowedMultiRegionClusterUpdatesResult(
        scale_up_node_types=resp.get("ScaleUpNodeTypes"),
        scale_down_node_types=resp.get("ScaleDownNodeTypes"),
    )


def list_allowed_node_type_updates(
    cluster_name: str,
    region_name: str | None = None,
) -> ListAllowedNodeTypeUpdatesResult:
    """List allowed node type updates.

    Args:
        cluster_name: Cluster name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterName"] = cluster_name
    try:
        resp = client.list_allowed_node_type_updates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list allowed node type updates") from exc
    return ListAllowedNodeTypeUpdatesResult(
        scale_up_node_types=resp.get("ScaleUpNodeTypes"),
        scale_down_node_types=resp.get("ScaleDownNodeTypes"),
    )


def list_tags(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsResult:
    """List tags.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags") from exc
    return ListTagsResult(
        tag_list=resp.get("TagList"),
    )


def purchase_reserved_nodes_offering(
    reserved_nodes_offering_id: str,
    *,
    reservation_id: str | None = None,
    node_count: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PurchaseReservedNodesOfferingResult:
    """Purchase reserved nodes offering.

    Args:
        reserved_nodes_offering_id: Reserved nodes offering id.
        reservation_id: Reservation id.
        node_count: Node count.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedNodesOfferingId"] = reserved_nodes_offering_id
    if reservation_id is not None:
        kwargs["ReservationId"] = reservation_id
    if node_count is not None:
        kwargs["NodeCount"] = node_count
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.purchase_reserved_nodes_offering(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to purchase reserved nodes offering") from exc
    return PurchaseReservedNodesOfferingResult(
        reserved_node=resp.get("ReservedNode"),
    )


def reset_parameter_group(
    parameter_group_name: str,
    *,
    all_parameters: bool | None = None,
    parameter_names: list[str] | None = None,
    region_name: str | None = None,
) -> ResetParameterGroupResult:
    """Reset parameter group.

    Args:
        parameter_group_name: Parameter group name.
        all_parameters: All parameters.
        parameter_names: Parameter names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    if all_parameters is not None:
        kwargs["AllParameters"] = all_parameters
    if parameter_names is not None:
        kwargs["ParameterNames"] = parameter_names
    try:
        resp = client.reset_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reset parameter group") from exc
    return ResetParameterGroupResult(
        parameter_group=resp.get("ParameterGroup"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> TagResourceResult:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        resp = client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return TagResourceResult(
        tag_list=resp.get("TagList"),
    )


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> UntagResourceResult:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        resp = client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return UntagResourceResult(
        tag_list=resp.get("TagList"),
    )


def update_multi_region_cluster(
    multi_region_cluster_name: str,
    *,
    node_type: str | None = None,
    description: str | None = None,
    engine_version: str | None = None,
    shard_configuration: dict[str, Any] | None = None,
    multi_region_parameter_group_name: str | None = None,
    update_strategy: str | None = None,
    region_name: str | None = None,
) -> UpdateMultiRegionClusterResult:
    """Update multi region cluster.

    Args:
        multi_region_cluster_name: Multi region cluster name.
        node_type: Node type.
        description: Description.
        engine_version: Engine version.
        shard_configuration: Shard configuration.
        multi_region_parameter_group_name: Multi region parameter group name.
        update_strategy: Update strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MultiRegionClusterName"] = multi_region_cluster_name
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if description is not None:
        kwargs["Description"] = description
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if shard_configuration is not None:
        kwargs["ShardConfiguration"] = shard_configuration
    if multi_region_parameter_group_name is not None:
        kwargs["MultiRegionParameterGroupName"] = multi_region_parameter_group_name
    if update_strategy is not None:
        kwargs["UpdateStrategy"] = update_strategy
    try:
        resp = client.update_multi_region_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update multi region cluster") from exc
    return UpdateMultiRegionClusterResult(
        multi_region_cluster=resp.get("MultiRegionCluster"),
    )


def update_parameter_group(
    parameter_group_name: str,
    parameter_name_values: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateParameterGroupResult:
    """Update parameter group.

    Args:
        parameter_group_name: Parameter group name.
        parameter_name_values: Parameter name values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    kwargs["ParameterNameValues"] = parameter_name_values
    try:
        resp = client.update_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update parameter group") from exc
    return UpdateParameterGroupResult(
        parameter_group=resp.get("ParameterGroup"),
    )


def update_subnet_group(
    subnet_group_name: str,
    *,
    description: str | None = None,
    subnet_ids: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateSubnetGroupResult:
    """Update subnet group.

    Args:
        subnet_group_name: Subnet group name.
        description: Description.
        subnet_ids: Subnet ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("memorydb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubnetGroupName"] = subnet_group_name
    if description is not None:
        kwargs["Description"] = description
    if subnet_ids is not None:
        kwargs["SubnetIds"] = subnet_ids
    try:
        resp = client.update_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update subnet group") from exc
    return UpdateSubnetGroupResult(
        subnet_group=resp.get("SubnetGroup"),
    )
