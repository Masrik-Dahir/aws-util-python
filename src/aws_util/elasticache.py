"""aws_util.elasticache — ElastiCache utilities.

Create, describe, modify, and delete ElastiCache cache clusters,
replication groups, subnet groups, and snapshots.  Includes polling
helpers (``wait_for_*``) and idempotent ``ensure_*`` wrappers.
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
    "AuthorizeCacheSecurityGroupIngressResult",
    "BatchApplyUpdateActionResult",
    "BatchStopUpdateActionResult",
    "CacheClusterResult",
    "CacheSubnetGroupResult",
    "CompleteMigrationResult",
    "CopyServerlessCacheSnapshotResult",
    "CopySnapshotResult",
    "CreateCacheParameterGroupResult",
    "CreateCacheSecurityGroupResult",
    "CreateGlobalReplicationGroupResult",
    "CreateServerlessCacheResult",
    "CreateServerlessCacheSnapshotResult",
    "CreateUserGroupResult",
    "CreateUserResult",
    "DecreaseNodeGroupsInGlobalReplicationGroupResult",
    "DecreaseReplicaCountResult",
    "DeleteGlobalReplicationGroupResult",
    "DeleteServerlessCacheResult",
    "DeleteServerlessCacheSnapshotResult",
    "DeleteUserGroupResult",
    "DeleteUserResult",
    "DescribeCacheEngineVersionsResult",
    "DescribeCacheParameterGroupsResult",
    "DescribeCacheParametersResult",
    "DescribeCacheSecurityGroupsResult",
    "DescribeEngineDefaultParametersResult",
    "DescribeEventsResult",
    "DescribeGlobalReplicationGroupsResult",
    "DescribeReservedCacheNodesOfferingsResult",
    "DescribeReservedCacheNodesResult",
    "DescribeServerlessCacheSnapshotsResult",
    "DescribeServerlessCachesResult",
    "DescribeServiceUpdatesResult",
    "DescribeUpdateActionsResult",
    "DescribeUserGroupsResult",
    "DescribeUsersResult",
    "DisassociateGlobalReplicationGroupResult",
    "ExportServerlessCacheSnapshotResult",
    "FailoverGlobalReplicationGroupResult",
    "IncreaseNodeGroupsInGlobalReplicationGroupResult",
    "IncreaseReplicaCountResult",
    "ListAllowedNodeTypeModificationsResult",
    "ModifyCacheParameterGroupResult",
    "ModifyCacheSubnetGroupResult",
    "ModifyGlobalReplicationGroupResult",
    "ModifyReplicationGroupShardConfigurationResult",
    "ModifyServerlessCacheResult",
    "ModifyUserGroupResult",
    "ModifyUserResult",
    "PurchaseReservedCacheNodesOfferingResult",
    "RebalanceSlotsInGlobalReplicationGroupResult",
    "RemoveTagsFromResourceResult",
    "ReplicationGroupResult",
    "ResetCacheParameterGroupResult",
    "RevokeCacheSecurityGroupIngressResult",
    "RunFailoverResult",
    "RunMigrationResult",
    "SnapshotResult",
    "StartMigrationResult",
    "add_tags_to_resource",
    "authorize_cache_security_group_ingress",
    "batch_apply_update_action",
    "batch_stop_update_action",
    "complete_migration",
    "copy_serverless_cache_snapshot",
    "copy_snapshot",
    "create_cache_cluster",
    "create_cache_parameter_group",
    "create_cache_security_group",
    "create_cache_subnet_group",
    "create_global_replication_group",
    "create_replication_group",
    "create_serverless_cache",
    "create_serverless_cache_snapshot",
    "create_snapshot",
    "create_user",
    "create_user_group",
    "decrease_node_groups_in_global_replication_group",
    "decrease_replica_count",
    "delete_cache_cluster",
    "delete_cache_parameter_group",
    "delete_cache_security_group",
    "delete_cache_subnet_group",
    "delete_global_replication_group",
    "delete_replication_group",
    "delete_serverless_cache",
    "delete_serverless_cache_snapshot",
    "delete_snapshot",
    "delete_user",
    "delete_user_group",
    "describe_cache_clusters",
    "describe_cache_engine_versions",
    "describe_cache_parameter_groups",
    "describe_cache_parameters",
    "describe_cache_security_groups",
    "describe_cache_subnet_groups",
    "describe_engine_default_parameters",
    "describe_events",
    "describe_global_replication_groups",
    "describe_replication_groups",
    "describe_reserved_cache_nodes",
    "describe_reserved_cache_nodes_offerings",
    "describe_serverless_cache_snapshots",
    "describe_serverless_caches",
    "describe_service_updates",
    "describe_snapshots",
    "describe_update_actions",
    "describe_user_groups",
    "describe_users",
    "disassociate_global_replication_group",
    "ensure_cache_cluster",
    "ensure_replication_group",
    "export_serverless_cache_snapshot",
    "failover_global_replication_group",
    "increase_node_groups_in_global_replication_group",
    "increase_replica_count",
    "list_allowed_node_type_modifications",
    "list_tags_for_resource",
    "modify_cache_cluster",
    "modify_cache_parameter_group",
    "modify_cache_subnet_group",
    "modify_global_replication_group",
    "modify_replication_group",
    "modify_replication_group_shard_configuration",
    "modify_serverless_cache",
    "modify_user",
    "modify_user_group",
    "purchase_reserved_cache_nodes_offering",
    "rebalance_slots_in_global_replication_group",
    "reboot_cache_cluster",
    "remove_tags_from_resource",
    "reset_cache_parameter_group",
    "revoke_cache_security_group_ingress",
    "run_failover",
    "run_migration",
    "start_migration",
    "wait_for_cache_cluster",
    "wait_for_replication_group",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CacheClusterResult(BaseModel):
    """Metadata for an ElastiCache cache cluster."""

    model_config = ConfigDict(frozen=True)

    cache_cluster_id: str
    cache_cluster_status: str
    cache_node_type: str
    engine: str
    engine_version: str
    num_cache_nodes: int
    preferred_availability_zone: str | None = None
    cache_subnet_group_name: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class ReplicationGroupResult(BaseModel):
    """Metadata for an ElastiCache replication group."""

    model_config = ConfigDict(frozen=True)

    replication_group_id: str
    description: str
    status: str
    member_clusters: list[str] = Field(default_factory=list)
    node_groups: list[dict[str, Any]] = Field(default_factory=list)
    automatic_failover: str = "disabled"
    extra: dict[str, Any] = Field(default_factory=dict)


class CacheSubnetGroupResult(BaseModel):
    """Metadata for an ElastiCache cache subnet group."""

    model_config = ConfigDict(frozen=True)

    name: str
    description: str
    vpc_id: str
    subnets: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class SnapshotResult(BaseModel):
    """Metadata for an ElastiCache snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_name: str
    cache_cluster_id: str | None = None
    replication_group_id: str | None = None
    snapshot_status: str
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_cluster(data: dict[str, Any]) -> CacheClusterResult:
    """Build a :class:`CacheClusterResult` from a raw API dict."""
    return CacheClusterResult(
        cache_cluster_id=data["CacheClusterId"],
        cache_cluster_status=data.get("CacheClusterStatus", "unknown"),
        cache_node_type=data.get("CacheNodeType", "unknown"),
        engine=data.get("Engine", "unknown"),
        engine_version=data.get("EngineVersion", "unknown"),
        num_cache_nodes=data.get("NumCacheNodes", 0),
        preferred_availability_zone=data.get("PreferredAvailabilityZone"),
        cache_subnet_group_name=data.get("CacheSubnetGroupName"),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "CacheClusterId",
                "CacheClusterStatus",
                "CacheNodeType",
                "Engine",
                "EngineVersion",
                "NumCacheNodes",
                "PreferredAvailabilityZone",
                "CacheSubnetGroupName",
            }
        },
    )


def _parse_replication_group(data: dict[str, Any]) -> ReplicationGroupResult:
    """Build a :class:`ReplicationGroupResult` from a raw API dict."""
    return ReplicationGroupResult(
        replication_group_id=data["ReplicationGroupId"],
        description=data.get("Description", ""),
        status=data.get("Status", "unknown"),
        member_clusters=data.get("MemberClusters", []),
        node_groups=data.get("NodeGroups", []),
        automatic_failover=data.get("AutomaticFailover", "disabled"),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "ReplicationGroupId",
                "Description",
                "Status",
                "MemberClusters",
                "NodeGroups",
                "AutomaticFailover",
            }
        },
    )


def _parse_subnet_group(data: dict[str, Any]) -> CacheSubnetGroupResult:
    """Build a :class:`CacheSubnetGroupResult` from a raw API dict."""
    return CacheSubnetGroupResult(
        name=data["CacheSubnetGroupName"],
        description=data.get("CacheSubnetGroupDescription", ""),
        vpc_id=data.get("VpcId", ""),
        subnets=[s.get("SubnetIdentifier", "") for s in data.get("Subnets", [])],
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "CacheSubnetGroupName",
                "CacheSubnetGroupDescription",
                "VpcId",
                "Subnets",
            }
        },
    )


def _parse_snapshot(data: dict[str, Any]) -> SnapshotResult:
    """Build a :class:`SnapshotResult` from a raw API dict."""
    return SnapshotResult(
        snapshot_name=data["SnapshotName"],
        cache_cluster_id=data.get("CacheClusterId"),
        replication_group_id=data.get("ReplicationGroupId"),
        snapshot_status=data.get("SnapshotStatus", "unknown"),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "SnapshotName",
                "CacheClusterId",
                "ReplicationGroupId",
                "SnapshotStatus",
            }
        },
    )


# ---------------------------------------------------------------------------
# Cache cluster operations
# ---------------------------------------------------------------------------


def create_cache_cluster(
    cache_cluster_id: str,
    *,
    cache_node_type: str = "cache.t3.micro",
    engine: str = "redis",
    num_cache_nodes: int = 1,
    cache_subnet_group_name: str | None = None,
    security_group_ids: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> CacheClusterResult:
    """Create a new ElastiCache cache cluster.

    Args:
        cache_cluster_id: Unique identifier for the cluster.
        cache_node_type: Compute/memory capacity node type.
        engine: Cache engine (``"redis"`` or ``"memcached"``).
        num_cache_nodes: Number of cache nodes in the cluster.
        cache_subnet_group_name: Subnet group to launch into.
        security_group_ids: VPC security group IDs.
        tags: Key/value tags for the cluster.
        region_name: AWS region override.

    Returns:
        The newly created :class:`CacheClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {
        "CacheClusterId": cache_cluster_id,
        "CacheNodeType": cache_node_type,
        "Engine": engine,
        "NumCacheNodes": num_cache_nodes,
    }
    if cache_subnet_group_name is not None:
        kwargs["CacheSubnetGroupName"] = cache_subnet_group_name
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = client.create_cache_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create cache cluster {cache_cluster_id!r}") from exc
    return _parse_cluster(resp["CacheCluster"])


def describe_cache_clusters(
    *,
    cache_cluster_id: str | None = None,
    show_node_info: bool = False,
    region_name: str | None = None,
) -> list[CacheClusterResult]:
    """Describe one or more cache clusters.

    Args:
        cache_cluster_id: Specific cluster ID. ``None`` returns all.
        show_node_info: Include individual cache node information.
        region_name: AWS region override.

    Returns:
        A list of :class:`CacheClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {
        "ShowCacheNodeInfo": show_node_info,
    }
    if cache_cluster_id is not None:
        kwargs["CacheClusterId"] = cache_cluster_id
    clusters: list[CacheClusterResult] = []
    try:
        paginator = client.get_paginator("describe_cache_clusters")
        for page in paginator.paginate(**kwargs):
            for item in page.get("CacheClusters", []):
                clusters.append(_parse_cluster(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_cache_clusters failed") from exc
    return clusters


def modify_cache_cluster(
    cache_cluster_id: str,
    *,
    num_cache_nodes: int | None = None,
    cache_node_type: str | None = None,
    region_name: str | None = None,
) -> CacheClusterResult:
    """Modify an existing cache cluster.

    Args:
        cache_cluster_id: Cluster identifier.
        num_cache_nodes: New number of cache nodes.
        cache_node_type: New node type.
        region_name: AWS region override.

    Returns:
        The modified :class:`CacheClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {"CacheClusterId": cache_cluster_id}
    if num_cache_nodes is not None:
        kwargs["NumCacheNodes"] = num_cache_nodes
    if cache_node_type is not None:
        kwargs["CacheNodeType"] = cache_node_type
    try:
        resp = client.modify_cache_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to modify cache cluster {cache_cluster_id!r}") from exc
    return _parse_cluster(resp["CacheCluster"])


def delete_cache_cluster(
    cache_cluster_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a cache cluster.

    Args:
        cache_cluster_id: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        client.delete_cache_cluster(CacheClusterId=cache_cluster_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete cache cluster {cache_cluster_id!r}") from exc


def reboot_cache_cluster(
    cache_cluster_id: str,
    *,
    node_ids_to_reboot: list[str],
    region_name: str | None = None,
) -> CacheClusterResult:
    """Reboot specific nodes in a cache cluster.

    Args:
        cache_cluster_id: Cluster identifier.
        node_ids_to_reboot: List of node IDs to reboot.
        region_name: AWS region override.

    Returns:
        The :class:`CacheClusterResult` after reboot initiation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        resp = client.reboot_cache_cluster(
            CacheClusterId=cache_cluster_id,
            CacheNodeIdsToReboot=node_ids_to_reboot,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to reboot cache cluster {cache_cluster_id!r}") from exc
    return _parse_cluster(resp["CacheCluster"])


# ---------------------------------------------------------------------------
# Replication group operations
# ---------------------------------------------------------------------------


def create_replication_group(
    replication_group_id: str,
    *,
    description: str,
    primary_cluster_id: str | None = None,
    num_cache_clusters: int | None = None,
    cache_node_type: str | None = None,
    automatic_failover_enabled: bool = False,
    region_name: str | None = None,
) -> ReplicationGroupResult:
    """Create a new replication group.

    Args:
        replication_group_id: Unique identifier.
        description: User-supplied description.
        primary_cluster_id: Existing cluster to promote as primary.
        num_cache_clusters: Number of clusters in the group.
        cache_node_type: Node type for all clusters.
        automatic_failover_enabled: Enable automatic failover.
        region_name: AWS region override.

    Returns:
        The newly created :class:`ReplicationGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationGroupId": replication_group_id,
        "ReplicationGroupDescription": description,
        "AutomaticFailoverEnabled": automatic_failover_enabled,
    }
    if primary_cluster_id is not None:
        kwargs["PrimaryClusterId"] = primary_cluster_id
    if num_cache_clusters is not None:
        kwargs["NumCacheClusters"] = num_cache_clusters
    if cache_node_type is not None:
        kwargs["CacheNodeType"] = cache_node_type
    try:
        resp = client.create_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create replication group {replication_group_id!r}",
        ) from exc
    return _parse_replication_group(resp["ReplicationGroup"])


def describe_replication_groups(
    *,
    replication_group_id: str | None = None,
    region_name: str | None = None,
) -> list[ReplicationGroupResult]:
    """Describe one or more replication groups.

    Args:
        replication_group_id: Specific group ID. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ReplicationGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if replication_group_id is not None:
        kwargs["ReplicationGroupId"] = replication_group_id
    groups: list[ReplicationGroupResult] = []
    try:
        paginator = client.get_paginator("describe_replication_groups")
        for page in paginator.paginate(**kwargs):
            for item in page.get("ReplicationGroups", []):
                groups.append(_parse_replication_group(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_replication_groups failed") from exc
    return groups


def modify_replication_group(
    replication_group_id: str,
    *,
    description: str | None = None,
    automatic_failover_enabled: bool | None = None,
    region_name: str | None = None,
) -> ReplicationGroupResult:
    """Modify an existing replication group.

    Args:
        replication_group_id: Replication group identifier.
        description: Updated description.
        automatic_failover_enabled: Enable/disable automatic failover.
        region_name: AWS region override.

    Returns:
        The modified :class:`ReplicationGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {
        "ReplicationGroupId": replication_group_id,
    }
    if description is not None:
        kwargs["ReplicationGroupDescription"] = description
    if automatic_failover_enabled is not None:
        kwargs["AutomaticFailoverEnabled"] = automatic_failover_enabled
    try:
        resp = client.modify_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to modify replication group {replication_group_id!r}",
        ) from exc
    return _parse_replication_group(resp["ReplicationGroup"])


def delete_replication_group(
    replication_group_id: str,
    *,
    retain_primary_cluster: bool = False,
    region_name: str | None = None,
) -> None:
    """Delete a replication group.

    Args:
        replication_group_id: Replication group identifier.
        retain_primary_cluster: If ``True``, keep the primary cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        client.delete_replication_group(
            ReplicationGroupId=replication_group_id,
            RetainPrimaryCluster=retain_primary_cluster,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete replication group {replication_group_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Subnet group operations
# ---------------------------------------------------------------------------


def create_cache_subnet_group(
    name: str,
    *,
    description: str,
    subnet_ids: list[str],
    region_name: str | None = None,
) -> CacheSubnetGroupResult:
    """Create a cache subnet group.

    Args:
        name: Subnet group name.
        description: Description.
        subnet_ids: List of VPC subnet IDs.
        region_name: AWS region override.

    Returns:
        The newly created :class:`CacheSubnetGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        resp = client.create_cache_subnet_group(
            CacheSubnetGroupName=name,
            CacheSubnetGroupDescription=description,
            SubnetIds=subnet_ids,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create cache subnet group {name!r}") from exc
    return _parse_subnet_group(resp["CacheSubnetGroup"])


def describe_cache_subnet_groups(
    *,
    name: str | None = None,
    region_name: str | None = None,
) -> list[CacheSubnetGroupResult]:
    """Describe one or more cache subnet groups.

    Args:
        name: Specific subnet group name. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`CacheSubnetGroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["CacheSubnetGroupName"] = name
    groups: list[CacheSubnetGroupResult] = []
    try:
        paginator = client.get_paginator("describe_cache_subnet_groups")
        for page in paginator.paginate(**kwargs):
            for item in page.get("CacheSubnetGroups", []):
                groups.append(_parse_subnet_group(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_cache_subnet_groups failed") from exc
    return groups


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


def create_snapshot(
    snapshot_name: str,
    *,
    cache_cluster_id: str | None = None,
    replication_group_id: str | None = None,
    region_name: str | None = None,
) -> SnapshotResult:
    """Create a snapshot of a cache cluster or replication group.

    Args:
        snapshot_name: Unique snapshot name.
        cache_cluster_id: Source cache cluster.
        replication_group_id: Source replication group.
        region_name: AWS region override.

    Returns:
        The newly created :class:`SnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {"SnapshotName": snapshot_name}
    if cache_cluster_id is not None:
        kwargs["CacheClusterId"] = cache_cluster_id
    if replication_group_id is not None:
        kwargs["ReplicationGroupId"] = replication_group_id
    try:
        resp = client.create_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create snapshot {snapshot_name!r}") from exc
    return _parse_snapshot(resp["Snapshot"])


def describe_snapshots(
    *,
    snapshot_name: str | None = None,
    cache_cluster_id: str | None = None,
    region_name: str | None = None,
) -> list[SnapshotResult]:
    """Describe one or more snapshots.

    Args:
        snapshot_name: Specific snapshot name.
        cache_cluster_id: Filter by cache cluster.
        region_name: AWS region override.

    Returns:
        A list of :class:`SnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if snapshot_name is not None:
        kwargs["SnapshotName"] = snapshot_name
    if cache_cluster_id is not None:
        kwargs["CacheClusterId"] = cache_cluster_id
    snapshots: list[SnapshotResult] = []
    try:
        paginator = client.get_paginator("describe_snapshots")
        for page in paginator.paginate(**kwargs):
            for item in page.get("Snapshots", []):
                snapshots.append(_parse_snapshot(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_snapshots failed") from exc
    return snapshots


def delete_snapshot(
    snapshot_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a snapshot.

    Args:
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        client.delete_snapshot(SnapshotName=snapshot_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete snapshot {snapshot_name!r}") from exc


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


def list_tags_for_resource(
    arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, str]:
    """List tags for an ElastiCache resource.

    Args:
        arn: The ARN of the resource.
        region_name: AWS region override.

    Returns:
        A ``{key: value}`` dict of tags.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    try:
        resp = client.list_tags_for_resource(ResourceName=arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to list tags for {arn!r}") from exc
    return {t["Key"]: t["Value"] for t in resp.get("TagList", [])}


def add_tags_to_resource(
    arn: str,
    *,
    tags: dict[str, str],
    region_name: str | None = None,
) -> None:
    """Add tags to an ElastiCache resource.

    Args:
        arn: The ARN of the resource.
        tags: ``{key: value}`` tags to add.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        client.add_tags_to_resource(ResourceName=arn, Tags=tag_list)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to add tags to {arn!r}") from exc


# ---------------------------------------------------------------------------
# Wait / polling helpers
# ---------------------------------------------------------------------------


def wait_for_cache_cluster(
    cache_cluster_id: str,
    *,
    target_status: str = "available",
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> CacheClusterResult:
    """Poll until a cache cluster reaches the target status.

    Args:
        cache_cluster_id: Cluster identifier.
        target_status: Desired status (default ``"available"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`CacheClusterResult` in the target status.

    Raises:
        TimeoutError: If the cluster does not reach *target_status* in time.
        RuntimeError: If the cluster is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        clusters = describe_cache_clusters(
            cache_cluster_id=cache_cluster_id, region_name=region_name
        )
        if not clusters:
            raise AwsServiceError(f"Cache cluster {cache_cluster_id!r} not found")
        cluster = clusters[0]
        if cluster.cache_cluster_status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cache cluster {cache_cluster_id!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {cluster.cache_cluster_status!r})"
            )
        time.sleep(poll_interval)


def wait_for_replication_group(
    replication_group_id: str,
    *,
    target_status: str = "available",
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> ReplicationGroupResult:
    """Poll until a replication group reaches the target status.

    Args:
        replication_group_id: Replication group identifier.
        target_status: Desired status (default ``"available"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`ReplicationGroupResult` in the target status.

    Raises:
        TimeoutError: If the group does not reach *target_status* in time.
        RuntimeError: If the group is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        groups = describe_replication_groups(
            replication_group_id=replication_group_id,
            region_name=region_name,
        )
        if not groups:
            raise AwsServiceError(f"Replication group {replication_group_id!r} not found")
        group = groups[0]
        if group.status == target_status:
            return group
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Replication group {replication_group_id!r} did not reach "
                f"status {target_status!r} within {timeout}s "
                f"(current: {group.status!r})"
            )
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Idempotent ensure helpers
# ---------------------------------------------------------------------------


def ensure_cache_cluster(
    cache_cluster_id: str,
    *,
    cache_node_type: str = "cache.t3.micro",
    engine: str = "redis",
    region_name: str | None = None,
) -> tuple[CacheClusterResult, bool]:
    """Get or create a cache cluster (idempotent).

    Args:
        cache_cluster_id: Cluster identifier.
        cache_node_type: Node type (used only on creation).
        engine: Engine (used only on creation).
        region_name: AWS region override.

    Returns:
        A tuple of ``(cluster, created)`` where *created* is ``True``
        when a new cluster was provisioned.

    Raises:
        RuntimeError: If the API calls fail.
    """
    existing = describe_cache_clusters(cache_cluster_id=cache_cluster_id, region_name=region_name)
    if existing:
        return existing[0], False
    cluster = create_cache_cluster(
        cache_cluster_id,
        cache_node_type=cache_node_type,
        engine=engine,
        region_name=region_name,
    )
    return cluster, True


def ensure_replication_group(
    replication_group_id: str,
    *,
    description: str,
    region_name: str | None = None,
) -> tuple[ReplicationGroupResult, bool]:
    """Get or create a replication group (idempotent).

    Args:
        replication_group_id: Replication group identifier.
        description: Description (used only on creation).
        region_name: AWS region override.

    Returns:
        A tuple of ``(group, created)`` where *created* is ``True``
        when a new group was provisioned.

    Raises:
        RuntimeError: If the API calls fail.
    """
    existing = describe_replication_groups(
        replication_group_id=replication_group_id,
        region_name=region_name,
    )
    if existing:
        return existing[0], False
    group = create_replication_group(
        replication_group_id,
        description=description,
        region_name=region_name,
    )
    return group, True


class AuthorizeCacheSecurityGroupIngressResult(BaseModel):
    """Result of authorize_cache_security_group_ingress."""

    model_config = ConfigDict(frozen=True)

    cache_security_group: dict[str, Any] | None = None


class BatchApplyUpdateActionResult(BaseModel):
    """Result of batch_apply_update_action."""

    model_config = ConfigDict(frozen=True)

    processed_update_actions: list[dict[str, Any]] | None = None
    unprocessed_update_actions: list[dict[str, Any]] | None = None


class BatchStopUpdateActionResult(BaseModel):
    """Result of batch_stop_update_action."""

    model_config = ConfigDict(frozen=True)

    processed_update_actions: list[dict[str, Any]] | None = None
    unprocessed_update_actions: list[dict[str, Any]] | None = None


class CompleteMigrationResult(BaseModel):
    """Result of complete_migration."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class CopyServerlessCacheSnapshotResult(BaseModel):
    """Result of copy_serverless_cache_snapshot."""

    model_config = ConfigDict(frozen=True)

    serverless_cache_snapshot: dict[str, Any] | None = None


class CopySnapshotResult(BaseModel):
    """Result of copy_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class CreateCacheParameterGroupResult(BaseModel):
    """Result of create_cache_parameter_group."""

    model_config = ConfigDict(frozen=True)

    cache_parameter_group: dict[str, Any] | None = None


class CreateCacheSecurityGroupResult(BaseModel):
    """Result of create_cache_security_group."""

    model_config = ConfigDict(frozen=True)

    cache_security_group: dict[str, Any] | None = None


class CreateGlobalReplicationGroupResult(BaseModel):
    """Result of create_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class CreateServerlessCacheResult(BaseModel):
    """Result of create_serverless_cache."""

    model_config = ConfigDict(frozen=True)

    serverless_cache: dict[str, Any] | None = None


class CreateServerlessCacheSnapshotResult(BaseModel):
    """Result of create_serverless_cache_snapshot."""

    model_config = ConfigDict(frozen=True)

    serverless_cache_snapshot: dict[str, Any] | None = None


class CreateUserResult(BaseModel):
    """Result of create_user."""

    model_config = ConfigDict(frozen=True)

    user_id: str | None = None
    user_name: str | None = None
    status: str | None = None
    engine: str | None = None
    minimum_engine_version: str | None = None
    access_string: str | None = None
    user_group_ids: list[str] | None = None
    authentication: dict[str, Any] | None = None
    arn: str | None = None


class CreateUserGroupResult(BaseModel):
    """Result of create_user_group."""

    model_config = ConfigDict(frozen=True)

    user_group_id: str | None = None
    status: str | None = None
    engine: str | None = None
    user_ids: list[str] | None = None
    minimum_engine_version: str | None = None
    pending_changes: dict[str, Any] | None = None
    replication_groups: list[str] | None = None
    serverless_caches: list[str] | None = None
    arn: str | None = None


class DecreaseNodeGroupsInGlobalReplicationGroupResult(BaseModel):
    """Result of decrease_node_groups_in_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class DecreaseReplicaCountResult(BaseModel):
    """Result of decrease_replica_count."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class DeleteGlobalReplicationGroupResult(BaseModel):
    """Result of delete_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class DeleteServerlessCacheResult(BaseModel):
    """Result of delete_serverless_cache."""

    model_config = ConfigDict(frozen=True)

    serverless_cache: dict[str, Any] | None = None


class DeleteServerlessCacheSnapshotResult(BaseModel):
    """Result of delete_serverless_cache_snapshot."""

    model_config = ConfigDict(frozen=True)

    serverless_cache_snapshot: dict[str, Any] | None = None


class DeleteUserResult(BaseModel):
    """Result of delete_user."""

    model_config = ConfigDict(frozen=True)

    user_id: str | None = None
    user_name: str | None = None
    status: str | None = None
    engine: str | None = None
    minimum_engine_version: str | None = None
    access_string: str | None = None
    user_group_ids: list[str] | None = None
    authentication: dict[str, Any] | None = None
    arn: str | None = None


class DeleteUserGroupResult(BaseModel):
    """Result of delete_user_group."""

    model_config = ConfigDict(frozen=True)

    user_group_id: str | None = None
    status: str | None = None
    engine: str | None = None
    user_ids: list[str] | None = None
    minimum_engine_version: str | None = None
    pending_changes: dict[str, Any] | None = None
    replication_groups: list[str] | None = None
    serverless_caches: list[str] | None = None
    arn: str | None = None


class DescribeCacheEngineVersionsResult(BaseModel):
    """Result of describe_cache_engine_versions."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    cache_engine_versions: list[dict[str, Any]] | None = None


class DescribeCacheParameterGroupsResult(BaseModel):
    """Result of describe_cache_parameter_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    cache_parameter_groups: list[dict[str, Any]] | None = None


class DescribeCacheParametersResult(BaseModel):
    """Result of describe_cache_parameters."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    parameters: list[dict[str, Any]] | None = None
    cache_node_type_specific_parameters: list[dict[str, Any]] | None = None


class DescribeCacheSecurityGroupsResult(BaseModel):
    """Result of describe_cache_security_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    cache_security_groups: list[dict[str, Any]] | None = None


class DescribeEngineDefaultParametersResult(BaseModel):
    """Result of describe_engine_default_parameters."""

    model_config = ConfigDict(frozen=True)

    engine_defaults: dict[str, Any] | None = None


class DescribeEventsResult(BaseModel):
    """Result of describe_events."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    events: list[dict[str, Any]] | None = None


class DescribeGlobalReplicationGroupsResult(BaseModel):
    """Result of describe_global_replication_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    global_replication_groups: list[dict[str, Any]] | None = None


class DescribeReservedCacheNodesResult(BaseModel):
    """Result of describe_reserved_cache_nodes."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    reserved_cache_nodes: list[dict[str, Any]] | None = None


class DescribeReservedCacheNodesOfferingsResult(BaseModel):
    """Result of describe_reserved_cache_nodes_offerings."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    reserved_cache_nodes_offerings: list[dict[str, Any]] | None = None


class DescribeServerlessCacheSnapshotsResult(BaseModel):
    """Result of describe_serverless_cache_snapshots."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    serverless_cache_snapshots: list[dict[str, Any]] | None = None


class DescribeServerlessCachesResult(BaseModel):
    """Result of describe_serverless_caches."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    serverless_caches: list[dict[str, Any]] | None = None


class DescribeServiceUpdatesResult(BaseModel):
    """Result of describe_service_updates."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    service_updates: list[dict[str, Any]] | None = None


class DescribeUpdateActionsResult(BaseModel):
    """Result of describe_update_actions."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    update_actions: list[dict[str, Any]] | None = None


class DescribeUserGroupsResult(BaseModel):
    """Result of describe_user_groups."""

    model_config = ConfigDict(frozen=True)

    user_groups: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeUsersResult(BaseModel):
    """Result of describe_users."""

    model_config = ConfigDict(frozen=True)

    users: list[dict[str, Any]] | None = None
    marker: str | None = None


class DisassociateGlobalReplicationGroupResult(BaseModel):
    """Result of disassociate_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class ExportServerlessCacheSnapshotResult(BaseModel):
    """Result of export_serverless_cache_snapshot."""

    model_config = ConfigDict(frozen=True)

    serverless_cache_snapshot: dict[str, Any] | None = None


class FailoverGlobalReplicationGroupResult(BaseModel):
    """Result of failover_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class IncreaseNodeGroupsInGlobalReplicationGroupResult(BaseModel):
    """Result of increase_node_groups_in_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class IncreaseReplicaCountResult(BaseModel):
    """Result of increase_replica_count."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class ListAllowedNodeTypeModificationsResult(BaseModel):
    """Result of list_allowed_node_type_modifications."""

    model_config = ConfigDict(frozen=True)

    scale_up_modifications: list[str] | None = None
    scale_down_modifications: list[str] | None = None


class ModifyCacheParameterGroupResult(BaseModel):
    """Result of modify_cache_parameter_group."""

    model_config = ConfigDict(frozen=True)

    cache_parameter_group_name: str | None = None


class ModifyCacheSubnetGroupResult(BaseModel):
    """Result of modify_cache_subnet_group."""

    model_config = ConfigDict(frozen=True)

    cache_subnet_group: dict[str, Any] | None = None


class ModifyGlobalReplicationGroupResult(BaseModel):
    """Result of modify_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class ModifyReplicationGroupShardConfigurationResult(BaseModel):
    """Result of modify_replication_group_shard_configuration."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class ModifyServerlessCacheResult(BaseModel):
    """Result of modify_serverless_cache."""

    model_config = ConfigDict(frozen=True)

    serverless_cache: dict[str, Any] | None = None


class ModifyUserResult(BaseModel):
    """Result of modify_user."""

    model_config = ConfigDict(frozen=True)

    user_id: str | None = None
    user_name: str | None = None
    status: str | None = None
    engine: str | None = None
    minimum_engine_version: str | None = None
    access_string: str | None = None
    user_group_ids: list[str] | None = None
    authentication: dict[str, Any] | None = None
    arn: str | None = None


class ModifyUserGroupResult(BaseModel):
    """Result of modify_user_group."""

    model_config = ConfigDict(frozen=True)

    user_group_id: str | None = None
    status: str | None = None
    engine: str | None = None
    user_ids: list[str] | None = None
    minimum_engine_version: str | None = None
    pending_changes: dict[str, Any] | None = None
    replication_groups: list[str] | None = None
    serverless_caches: list[str] | None = None
    arn: str | None = None


class PurchaseReservedCacheNodesOfferingResult(BaseModel):
    """Result of purchase_reserved_cache_nodes_offering."""

    model_config = ConfigDict(frozen=True)

    reserved_cache_node: dict[str, Any] | None = None


class RebalanceSlotsInGlobalReplicationGroupResult(BaseModel):
    """Result of rebalance_slots_in_global_replication_group."""

    model_config = ConfigDict(frozen=True)

    global_replication_group: dict[str, Any] | None = None


class RemoveTagsFromResourceResult(BaseModel):
    """Result of remove_tags_from_resource."""

    model_config = ConfigDict(frozen=True)

    tag_list: list[dict[str, Any]] | None = None


class ResetCacheParameterGroupResult(BaseModel):
    """Result of reset_cache_parameter_group."""

    model_config = ConfigDict(frozen=True)

    cache_parameter_group_name: str | None = None


class RevokeCacheSecurityGroupIngressResult(BaseModel):
    """Result of revoke_cache_security_group_ingress."""

    model_config = ConfigDict(frozen=True)

    cache_security_group: dict[str, Any] | None = None


class RunFailoverResult(BaseModel):
    """Result of run_failover."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class RunMigrationResult(BaseModel):
    """Result of run_migration."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


class StartMigrationResult(BaseModel):
    """Result of start_migration."""

    model_config = ConfigDict(frozen=True)

    replication_group: dict[str, Any] | None = None


def authorize_cache_security_group_ingress(
    cache_security_group_name: str,
    ec2_security_group_name: str,
    ec2_security_group_owner_id: str,
    region_name: str | None = None,
) -> AuthorizeCacheSecurityGroupIngressResult:
    """Authorize cache security group ingress.

    Args:
        cache_security_group_name: Cache security group name.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSecurityGroupName"] = cache_security_group_name
    kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = client.authorize_cache_security_group_ingress(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to authorize cache security group ingress") from exc
    return AuthorizeCacheSecurityGroupIngressResult(
        cache_security_group=resp.get("CacheSecurityGroup"),
    )


def batch_apply_update_action(
    service_update_name: str,
    *,
    replication_group_ids: list[str] | None = None,
    cache_cluster_ids: list[str] | None = None,
    region_name: str | None = None,
) -> BatchApplyUpdateActionResult:
    """Batch apply update action.

    Args:
        service_update_name: Service update name.
        replication_group_ids: Replication group ids.
        cache_cluster_ids: Cache cluster ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceUpdateName"] = service_update_name
    if replication_group_ids is not None:
        kwargs["ReplicationGroupIds"] = replication_group_ids
    if cache_cluster_ids is not None:
        kwargs["CacheClusterIds"] = cache_cluster_ids
    try:
        resp = client.batch_apply_update_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch apply update action") from exc
    return BatchApplyUpdateActionResult(
        processed_update_actions=resp.get("ProcessedUpdateActions"),
        unprocessed_update_actions=resp.get("UnprocessedUpdateActions"),
    )


def batch_stop_update_action(
    service_update_name: str,
    *,
    replication_group_ids: list[str] | None = None,
    cache_cluster_ids: list[str] | None = None,
    region_name: str | None = None,
) -> BatchStopUpdateActionResult:
    """Batch stop update action.

    Args:
        service_update_name: Service update name.
        replication_group_ids: Replication group ids.
        cache_cluster_ids: Cache cluster ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceUpdateName"] = service_update_name
    if replication_group_ids is not None:
        kwargs["ReplicationGroupIds"] = replication_group_ids
    if cache_cluster_ids is not None:
        kwargs["CacheClusterIds"] = cache_cluster_ids
    try:
        resp = client.batch_stop_update_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch stop update action") from exc
    return BatchStopUpdateActionResult(
        processed_update_actions=resp.get("ProcessedUpdateActions"),
        unprocessed_update_actions=resp.get("UnprocessedUpdateActions"),
    )


def complete_migration(
    replication_group_id: str,
    *,
    force: bool | None = None,
    region_name: str | None = None,
) -> CompleteMigrationResult:
    """Complete migration.

    Args:
        replication_group_id: Replication group id.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    if force is not None:
        kwargs["Force"] = force
    try:
        resp = client.complete_migration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to complete migration") from exc
    return CompleteMigrationResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def copy_serverless_cache_snapshot(
    source_serverless_cache_snapshot_name: str,
    target_serverless_cache_snapshot_name: str,
    *,
    kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CopyServerlessCacheSnapshotResult:
    """Copy serverless cache snapshot.

    Args:
        source_serverless_cache_snapshot_name: Source serverless cache snapshot name.
        target_serverless_cache_snapshot_name: Target serverless cache snapshot name.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceServerlessCacheSnapshotName"] = source_serverless_cache_snapshot_name
    kwargs["TargetServerlessCacheSnapshotName"] = target_serverless_cache_snapshot_name
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.copy_serverless_cache_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy serverless cache snapshot") from exc
    return CopyServerlessCacheSnapshotResult(
        serverless_cache_snapshot=resp.get("ServerlessCacheSnapshot"),
    )


def copy_snapshot(
    source_snapshot_name: str,
    target_snapshot_name: str,
    *,
    target_bucket: str | None = None,
    kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CopySnapshotResult:
    """Copy snapshot.

    Args:
        source_snapshot_name: Source snapshot name.
        target_snapshot_name: Target snapshot name.
        target_bucket: Target bucket.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceSnapshotName"] = source_snapshot_name
    kwargs["TargetSnapshotName"] = target_snapshot_name
    if target_bucket is not None:
        kwargs["TargetBucket"] = target_bucket
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.copy_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy snapshot") from exc
    return CopySnapshotResult(
        snapshot=resp.get("Snapshot"),
    )


def create_cache_parameter_group(
    cache_parameter_group_name: str,
    cache_parameter_group_family: str,
    description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCacheParameterGroupResult:
    """Create cache parameter group.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        cache_parameter_group_family: Cache parameter group family.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    kwargs["CacheParameterGroupFamily"] = cache_parameter_group_family
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_cache_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cache parameter group") from exc
    return CreateCacheParameterGroupResult(
        cache_parameter_group=resp.get("CacheParameterGroup"),
    )


def create_cache_security_group(
    cache_security_group_name: str,
    description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCacheSecurityGroupResult:
    """Create cache security group.

    Args:
        cache_security_group_name: Cache security group name.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSecurityGroupName"] = cache_security_group_name
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_cache_security_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create cache security group") from exc
    return CreateCacheSecurityGroupResult(
        cache_security_group=resp.get("CacheSecurityGroup"),
    )


def create_global_replication_group(
    global_replication_group_id_suffix: str,
    primary_replication_group_id: str,
    *,
    global_replication_group_description: str | None = None,
    region_name: str | None = None,
) -> CreateGlobalReplicationGroupResult:
    """Create global replication group.

    Args:
        global_replication_group_id_suffix: Global replication group id suffix.
        primary_replication_group_id: Primary replication group id.
        global_replication_group_description: Global replication group description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupIdSuffix"] = global_replication_group_id_suffix
    kwargs["PrimaryReplicationGroupId"] = primary_replication_group_id
    if global_replication_group_description is not None:
        kwargs["GlobalReplicationGroupDescription"] = global_replication_group_description
    try:
        resp = client.create_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create global replication group") from exc
    return CreateGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def create_serverless_cache(
    serverless_cache_name: str,
    engine: str,
    *,
    description: str | None = None,
    major_engine_version: str | None = None,
    cache_usage_limits: dict[str, Any] | None = None,
    kms_key_id: str | None = None,
    security_group_ids: list[str] | None = None,
    snapshot_arns_to_restore: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    user_group_id: str | None = None,
    subnet_ids: list[str] | None = None,
    snapshot_retention_limit: int | None = None,
    daily_snapshot_time: str | None = None,
    region_name: str | None = None,
) -> CreateServerlessCacheResult:
    """Create serverless cache.

    Args:
        serverless_cache_name: Serverless cache name.
        engine: Engine.
        description: Description.
        major_engine_version: Major engine version.
        cache_usage_limits: Cache usage limits.
        kms_key_id: Kms key id.
        security_group_ids: Security group ids.
        snapshot_arns_to_restore: Snapshot arns to restore.
        tags: Tags.
        user_group_id: User group id.
        subnet_ids: Subnet ids.
        snapshot_retention_limit: Snapshot retention limit.
        daily_snapshot_time: Daily snapshot time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheName"] = serverless_cache_name
    kwargs["Engine"] = engine
    if description is not None:
        kwargs["Description"] = description
    if major_engine_version is not None:
        kwargs["MajorEngineVersion"] = major_engine_version
    if cache_usage_limits is not None:
        kwargs["CacheUsageLimits"] = cache_usage_limits
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if snapshot_arns_to_restore is not None:
        kwargs["SnapshotArnsToRestore"] = snapshot_arns_to_restore
    if tags is not None:
        kwargs["Tags"] = tags
    if user_group_id is not None:
        kwargs["UserGroupId"] = user_group_id
    if subnet_ids is not None:
        kwargs["SubnetIds"] = subnet_ids
    if snapshot_retention_limit is not None:
        kwargs["SnapshotRetentionLimit"] = snapshot_retention_limit
    if daily_snapshot_time is not None:
        kwargs["DailySnapshotTime"] = daily_snapshot_time
    try:
        resp = client.create_serverless_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create serverless cache") from exc
    return CreateServerlessCacheResult(
        serverless_cache=resp.get("ServerlessCache"),
    )


def create_serverless_cache_snapshot(
    serverless_cache_snapshot_name: str,
    serverless_cache_name: str,
    *,
    kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateServerlessCacheSnapshotResult:
    """Create serverless cache snapshot.

    Args:
        serverless_cache_snapshot_name: Serverless cache snapshot name.
        serverless_cache_name: Serverless cache name.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheSnapshotName"] = serverless_cache_snapshot_name
    kwargs["ServerlessCacheName"] = serverless_cache_name
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_serverless_cache_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create serverless cache snapshot") from exc
    return CreateServerlessCacheSnapshotResult(
        serverless_cache_snapshot=resp.get("ServerlessCacheSnapshot"),
    )


def create_user(
    user_id: str,
    user_name: str,
    engine: str,
    access_string: str,
    *,
    passwords: list[str] | None = None,
    no_password_required: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    authentication_mode: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUserResult:
    """Create user.

    Args:
        user_id: User id.
        user_name: User name.
        engine: Engine.
        access_string: Access string.
        passwords: Passwords.
        no_password_required: No password required.
        tags: Tags.
        authentication_mode: Authentication mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    kwargs["UserName"] = user_name
    kwargs["Engine"] = engine
    kwargs["AccessString"] = access_string
    if passwords is not None:
        kwargs["Passwords"] = passwords
    if no_password_required is not None:
        kwargs["NoPasswordRequired"] = no_password_required
    if tags is not None:
        kwargs["Tags"] = tags
    if authentication_mode is not None:
        kwargs["AuthenticationMode"] = authentication_mode
    try:
        resp = client.create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user") from exc
    return CreateUserResult(
        user_id=resp.get("UserId"),
        user_name=resp.get("UserName"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        access_string=resp.get("AccessString"),
        user_group_ids=resp.get("UserGroupIds"),
        authentication=resp.get("Authentication"),
        arn=resp.get("ARN"),
    )


def create_user_group(
    user_group_id: str,
    engine: str,
    *,
    user_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateUserGroupResult:
    """Create user group.

    Args:
        user_group_id: User group id.
        engine: Engine.
        user_ids: User ids.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserGroupId"] = user_group_id
    kwargs["Engine"] = engine
    if user_ids is not None:
        kwargs["UserIds"] = user_ids
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_user_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user group") from exc
    return CreateUserGroupResult(
        user_group_id=resp.get("UserGroupId"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        user_ids=resp.get("UserIds"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        pending_changes=resp.get("PendingChanges"),
        replication_groups=resp.get("ReplicationGroups"),
        serverless_caches=resp.get("ServerlessCaches"),
        arn=resp.get("ARN"),
    )


def decrease_node_groups_in_global_replication_group(
    global_replication_group_id: str,
    node_group_count: int,
    apply_immediately: bool,
    *,
    global_node_groups_to_remove: list[str] | None = None,
    global_node_groups_to_retain: list[str] | None = None,
    region_name: str | None = None,
) -> DecreaseNodeGroupsInGlobalReplicationGroupResult:
    """Decrease node groups in global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        node_group_count: Node group count.
        apply_immediately: Apply immediately.
        global_node_groups_to_remove: Global node groups to remove.
        global_node_groups_to_retain: Global node groups to retain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["NodeGroupCount"] = node_group_count
    kwargs["ApplyImmediately"] = apply_immediately
    if global_node_groups_to_remove is not None:
        kwargs["GlobalNodeGroupsToRemove"] = global_node_groups_to_remove
    if global_node_groups_to_retain is not None:
        kwargs["GlobalNodeGroupsToRetain"] = global_node_groups_to_retain
    try:
        resp = client.decrease_node_groups_in_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to decrease node groups in global replication group"
        ) from exc
    return DecreaseNodeGroupsInGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def decrease_replica_count(
    replication_group_id: str,
    apply_immediately: bool,
    *,
    new_replica_count: int | None = None,
    replica_configuration: list[dict[str, Any]] | None = None,
    replicas_to_remove: list[str] | None = None,
    region_name: str | None = None,
) -> DecreaseReplicaCountResult:
    """Decrease replica count.

    Args:
        replication_group_id: Replication group id.
        apply_immediately: Apply immediately.
        new_replica_count: New replica count.
        replica_configuration: Replica configuration.
        replicas_to_remove: Replicas to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["ApplyImmediately"] = apply_immediately
    if new_replica_count is not None:
        kwargs["NewReplicaCount"] = new_replica_count
    if replica_configuration is not None:
        kwargs["ReplicaConfiguration"] = replica_configuration
    if replicas_to_remove is not None:
        kwargs["ReplicasToRemove"] = replicas_to_remove
    try:
        resp = client.decrease_replica_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to decrease replica count") from exc
    return DecreaseReplicaCountResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def delete_cache_parameter_group(
    cache_parameter_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cache parameter group.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    try:
        client.delete_cache_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cache parameter group") from exc
    return None


def delete_cache_security_group(
    cache_security_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cache security group.

    Args:
        cache_security_group_name: Cache security group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSecurityGroupName"] = cache_security_group_name
    try:
        client.delete_cache_security_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cache security group") from exc
    return None


def delete_cache_subnet_group(
    cache_subnet_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cache subnet group.

    Args:
        cache_subnet_group_name: Cache subnet group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSubnetGroupName"] = cache_subnet_group_name
    try:
        client.delete_cache_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete cache subnet group") from exc
    return None


def delete_global_replication_group(
    global_replication_group_id: str,
    retain_primary_replication_group: bool,
    region_name: str | None = None,
) -> DeleteGlobalReplicationGroupResult:
    """Delete global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        retain_primary_replication_group: Retain primary replication group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["RetainPrimaryReplicationGroup"] = retain_primary_replication_group
    try:
        resp = client.delete_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete global replication group") from exc
    return DeleteGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def delete_serverless_cache(
    serverless_cache_name: str,
    *,
    final_snapshot_name: str | None = None,
    region_name: str | None = None,
) -> DeleteServerlessCacheResult:
    """Delete serverless cache.

    Args:
        serverless_cache_name: Serverless cache name.
        final_snapshot_name: Final snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheName"] = serverless_cache_name
    if final_snapshot_name is not None:
        kwargs["FinalSnapshotName"] = final_snapshot_name
    try:
        resp = client.delete_serverless_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete serverless cache") from exc
    return DeleteServerlessCacheResult(
        serverless_cache=resp.get("ServerlessCache"),
    )


def delete_serverless_cache_snapshot(
    serverless_cache_snapshot_name: str,
    region_name: str | None = None,
) -> DeleteServerlessCacheSnapshotResult:
    """Delete serverless cache snapshot.

    Args:
        serverless_cache_snapshot_name: Serverless cache snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheSnapshotName"] = serverless_cache_snapshot_name
    try:
        resp = client.delete_serverless_cache_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete serverless cache snapshot") from exc
    return DeleteServerlessCacheSnapshotResult(
        serverless_cache_snapshot=resp.get("ServerlessCacheSnapshot"),
    )


def delete_user(
    user_id: str,
    region_name: str | None = None,
) -> DeleteUserResult:
    """Delete user.

    Args:
        user_id: User id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    try:
        resp = client.delete_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user") from exc
    return DeleteUserResult(
        user_id=resp.get("UserId"),
        user_name=resp.get("UserName"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        access_string=resp.get("AccessString"),
        user_group_ids=resp.get("UserGroupIds"),
        authentication=resp.get("Authentication"),
        arn=resp.get("ARN"),
    )


def delete_user_group(
    user_group_id: str,
    region_name: str | None = None,
) -> DeleteUserGroupResult:
    """Delete user group.

    Args:
        user_group_id: User group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserGroupId"] = user_group_id
    try:
        resp = client.delete_user_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user group") from exc
    return DeleteUserGroupResult(
        user_group_id=resp.get("UserGroupId"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        user_ids=resp.get("UserIds"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        pending_changes=resp.get("PendingChanges"),
        replication_groups=resp.get("ReplicationGroups"),
        serverless_caches=resp.get("ServerlessCaches"),
        arn=resp.get("ARN"),
    )


def describe_cache_engine_versions(
    *,
    engine: str | None = None,
    engine_version: str | None = None,
    cache_parameter_group_family: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    default_only: bool | None = None,
    region_name: str | None = None,
) -> DescribeCacheEngineVersionsResult:
    """Describe cache engine versions.

    Args:
        engine: Engine.
        engine_version: Engine version.
        cache_parameter_group_family: Cache parameter group family.
        max_records: Max records.
        marker: Marker.
        default_only: Default only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if cache_parameter_group_family is not None:
        kwargs["CacheParameterGroupFamily"] = cache_parameter_group_family
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if default_only is not None:
        kwargs["DefaultOnly"] = default_only
    try:
        resp = client.describe_cache_engine_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache engine versions") from exc
    return DescribeCacheEngineVersionsResult(
        marker=resp.get("Marker"),
        cache_engine_versions=resp.get("CacheEngineVersions"),
    )


def describe_cache_parameter_groups(
    *,
    cache_parameter_group_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCacheParameterGroupsResult:
    """Describe cache parameter groups.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if cache_parameter_group_name is not None:
        kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_cache_parameter_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache parameter groups") from exc
    return DescribeCacheParameterGroupsResult(
        marker=resp.get("Marker"),
        cache_parameter_groups=resp.get("CacheParameterGroups"),
    )


def describe_cache_parameters(
    cache_parameter_group_name: str,
    *,
    source: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCacheParametersResult:
    """Describe cache parameters.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        source: Source.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    if source is not None:
        kwargs["Source"] = source
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_cache_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache parameters") from exc
    return DescribeCacheParametersResult(
        marker=resp.get("Marker"),
        parameters=resp.get("Parameters"),
        cache_node_type_specific_parameters=resp.get("CacheNodeTypeSpecificParameters"),
    )


def describe_cache_security_groups(
    *,
    cache_security_group_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCacheSecurityGroupsResult:
    """Describe cache security groups.

    Args:
        cache_security_group_name: Cache security group name.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if cache_security_group_name is not None:
        kwargs["CacheSecurityGroupName"] = cache_security_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_cache_security_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cache security groups") from exc
    return DescribeCacheSecurityGroupsResult(
        marker=resp.get("Marker"),
        cache_security_groups=resp.get("CacheSecurityGroups"),
    )


def describe_engine_default_parameters(
    cache_parameter_group_family: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEngineDefaultParametersResult:
    """Describe engine default parameters.

    Args:
        cache_parameter_group_family: Cache parameter group family.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupFamily"] = cache_parameter_group_family
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_engine_default_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe engine default parameters") from exc
    return DescribeEngineDefaultParametersResult(
        engine_defaults=resp.get("EngineDefaults"),
    )


def describe_events(
    *,
    source_identifier: str | None = None,
    source_type: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    duration: int | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEventsResult:
    """Describe events.

    Args:
        source_identifier: Source identifier.
        source_type: Source type.
        start_time: Start time.
        end_time: End time.
        duration: Duration.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if source_identifier is not None:
        kwargs["SourceIdentifier"] = source_identifier
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if duration is not None:
        kwargs["Duration"] = duration
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        marker=resp.get("Marker"),
        events=resp.get("Events"),
    )


def describe_global_replication_groups(
    *,
    global_replication_group_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    show_member_info: bool | None = None,
    region_name: str | None = None,
) -> DescribeGlobalReplicationGroupsResult:
    """Describe global replication groups.

    Args:
        global_replication_group_id: Global replication group id.
        max_records: Max records.
        marker: Marker.
        show_member_info: Show member info.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if global_replication_group_id is not None:
        kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if show_member_info is not None:
        kwargs["ShowMemberInfo"] = show_member_info
    try:
        resp = client.describe_global_replication_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe global replication groups") from exc
    return DescribeGlobalReplicationGroupsResult(
        marker=resp.get("Marker"),
        global_replication_groups=resp.get("GlobalReplicationGroups"),
    )


def describe_reserved_cache_nodes(
    *,
    reserved_cache_node_id: str | None = None,
    reserved_cache_nodes_offering_id: str | None = None,
    cache_node_type: str | None = None,
    duration: str | None = None,
    product_description: str | None = None,
    offering_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedCacheNodesResult:
    """Describe reserved cache nodes.

    Args:
        reserved_cache_node_id: Reserved cache node id.
        reserved_cache_nodes_offering_id: Reserved cache nodes offering id.
        cache_node_type: Cache node type.
        duration: Duration.
        product_description: Product description.
        offering_type: Offering type.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_cache_node_id is not None:
        kwargs["ReservedCacheNodeId"] = reserved_cache_node_id
    if reserved_cache_nodes_offering_id is not None:
        kwargs["ReservedCacheNodesOfferingId"] = reserved_cache_nodes_offering_id
    if cache_node_type is not None:
        kwargs["CacheNodeType"] = cache_node_type
    if duration is not None:
        kwargs["Duration"] = duration
    if product_description is not None:
        kwargs["ProductDescription"] = product_description
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_reserved_cache_nodes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved cache nodes") from exc
    return DescribeReservedCacheNodesResult(
        marker=resp.get("Marker"),
        reserved_cache_nodes=resp.get("ReservedCacheNodes"),
    )


def describe_reserved_cache_nodes_offerings(
    *,
    reserved_cache_nodes_offering_id: str | None = None,
    cache_node_type: str | None = None,
    duration: str | None = None,
    product_description: str | None = None,
    offering_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedCacheNodesOfferingsResult:
    """Describe reserved cache nodes offerings.

    Args:
        reserved_cache_nodes_offering_id: Reserved cache nodes offering id.
        cache_node_type: Cache node type.
        duration: Duration.
        product_description: Product description.
        offering_type: Offering type.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_cache_nodes_offering_id is not None:
        kwargs["ReservedCacheNodesOfferingId"] = reserved_cache_nodes_offering_id
    if cache_node_type is not None:
        kwargs["CacheNodeType"] = cache_node_type
    if duration is not None:
        kwargs["Duration"] = duration
    if product_description is not None:
        kwargs["ProductDescription"] = product_description
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_reserved_cache_nodes_offerings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved cache nodes offerings") from exc
    return DescribeReservedCacheNodesOfferingsResult(
        marker=resp.get("Marker"),
        reserved_cache_nodes_offerings=resp.get("ReservedCacheNodesOfferings"),
    )


def describe_serverless_cache_snapshots(
    *,
    serverless_cache_name: str | None = None,
    serverless_cache_snapshot_name: str | None = None,
    snapshot_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeServerlessCacheSnapshotsResult:
    """Describe serverless cache snapshots.

    Args:
        serverless_cache_name: Serverless cache name.
        serverless_cache_snapshot_name: Serverless cache snapshot name.
        snapshot_type: Snapshot type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if serverless_cache_name is not None:
        kwargs["ServerlessCacheName"] = serverless_cache_name
    if serverless_cache_snapshot_name is not None:
        kwargs["ServerlessCacheSnapshotName"] = serverless_cache_snapshot_name
    if snapshot_type is not None:
        kwargs["SnapshotType"] = snapshot_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_serverless_cache_snapshots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe serverless cache snapshots") from exc
    return DescribeServerlessCacheSnapshotsResult(
        next_token=resp.get("NextToken"),
        serverless_cache_snapshots=resp.get("ServerlessCacheSnapshots"),
    )


def describe_serverless_caches(
    *,
    serverless_cache_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeServerlessCachesResult:
    """Describe serverless caches.

    Args:
        serverless_cache_name: Serverless cache name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if serverless_cache_name is not None:
        kwargs["ServerlessCacheName"] = serverless_cache_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_serverless_caches(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe serverless caches") from exc
    return DescribeServerlessCachesResult(
        next_token=resp.get("NextToken"),
        serverless_caches=resp.get("ServerlessCaches"),
    )


def describe_service_updates(
    *,
    service_update_name: str | None = None,
    service_update_status: list[str] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeServiceUpdatesResult:
    """Describe service updates.

    Args:
        service_update_name: Service update name.
        service_update_status: Service update status.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if service_update_name is not None:
        kwargs["ServiceUpdateName"] = service_update_name
    if service_update_status is not None:
        kwargs["ServiceUpdateStatus"] = service_update_status
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_service_updates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe service updates") from exc
    return DescribeServiceUpdatesResult(
        marker=resp.get("Marker"),
        service_updates=resp.get("ServiceUpdates"),
    )


def describe_update_actions(
    *,
    service_update_name: str | None = None,
    replication_group_ids: list[str] | None = None,
    cache_cluster_ids: list[str] | None = None,
    engine: str | None = None,
    service_update_status: list[str] | None = None,
    service_update_time_range: dict[str, Any] | None = None,
    update_action_status: list[str] | None = None,
    show_node_level_update_status: bool | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeUpdateActionsResult:
    """Describe update actions.

    Args:
        service_update_name: Service update name.
        replication_group_ids: Replication group ids.
        cache_cluster_ids: Cache cluster ids.
        engine: Engine.
        service_update_status: Service update status.
        service_update_time_range: Service update time range.
        update_action_status: Update action status.
        show_node_level_update_status: Show node level update status.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if service_update_name is not None:
        kwargs["ServiceUpdateName"] = service_update_name
    if replication_group_ids is not None:
        kwargs["ReplicationGroupIds"] = replication_group_ids
    if cache_cluster_ids is not None:
        kwargs["CacheClusterIds"] = cache_cluster_ids
    if engine is not None:
        kwargs["Engine"] = engine
    if service_update_status is not None:
        kwargs["ServiceUpdateStatus"] = service_update_status
    if service_update_time_range is not None:
        kwargs["ServiceUpdateTimeRange"] = service_update_time_range
    if update_action_status is not None:
        kwargs["UpdateActionStatus"] = update_action_status
    if show_node_level_update_status is not None:
        kwargs["ShowNodeLevelUpdateStatus"] = show_node_level_update_status
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_update_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe update actions") from exc
    return DescribeUpdateActionsResult(
        marker=resp.get("Marker"),
        update_actions=resp.get("UpdateActions"),
    )


def describe_user_groups(
    *,
    user_group_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeUserGroupsResult:
    """Describe user groups.

    Args:
        user_group_id: User group id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if user_group_id is not None:
        kwargs["UserGroupId"] = user_group_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_user_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user groups") from exc
    return DescribeUserGroupsResult(
        user_groups=resp.get("UserGroups"),
        marker=resp.get("Marker"),
    )


def describe_users(
    *,
    engine: str | None = None,
    user_id: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeUsersResult:
    """Describe users.

    Args:
        engine: Engine.
        user_id: User id.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if engine is not None:
        kwargs["Engine"] = engine
    if user_id is not None:
        kwargs["UserId"] = user_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe users") from exc
    return DescribeUsersResult(
        users=resp.get("Users"),
        marker=resp.get("Marker"),
    )


def disassociate_global_replication_group(
    global_replication_group_id: str,
    replication_group_id: str,
    replication_group_region: str,
    region_name: str | None = None,
) -> DisassociateGlobalReplicationGroupResult:
    """Disassociate global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        replication_group_id: Replication group id.
        replication_group_region: Replication group region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["ReplicationGroupRegion"] = replication_group_region
    try:
        resp = client.disassociate_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate global replication group") from exc
    return DisassociateGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def export_serverless_cache_snapshot(
    serverless_cache_snapshot_name: str,
    s3_bucket_name: str,
    region_name: str | None = None,
) -> ExportServerlessCacheSnapshotResult:
    """Export serverless cache snapshot.

    Args:
        serverless_cache_snapshot_name: Serverless cache snapshot name.
        s3_bucket_name: S3 bucket name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheSnapshotName"] = serverless_cache_snapshot_name
    kwargs["S3BucketName"] = s3_bucket_name
    try:
        resp = client.export_serverless_cache_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to export serverless cache snapshot") from exc
    return ExportServerlessCacheSnapshotResult(
        serverless_cache_snapshot=resp.get("ServerlessCacheSnapshot"),
    )


def failover_global_replication_group(
    global_replication_group_id: str,
    primary_region: str,
    primary_replication_group_id: str,
    region_name: str | None = None,
) -> FailoverGlobalReplicationGroupResult:
    """Failover global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        primary_region: Primary region.
        primary_replication_group_id: Primary replication group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["PrimaryRegion"] = primary_region
    kwargs["PrimaryReplicationGroupId"] = primary_replication_group_id
    try:
        resp = client.failover_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to failover global replication group") from exc
    return FailoverGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def increase_node_groups_in_global_replication_group(
    global_replication_group_id: str,
    node_group_count: int,
    apply_immediately: bool,
    *,
    regional_configurations: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> IncreaseNodeGroupsInGlobalReplicationGroupResult:
    """Increase node groups in global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        node_group_count: Node group count.
        apply_immediately: Apply immediately.
        regional_configurations: Regional configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["NodeGroupCount"] = node_group_count
    kwargs["ApplyImmediately"] = apply_immediately
    if regional_configurations is not None:
        kwargs["RegionalConfigurations"] = regional_configurations
    try:
        resp = client.increase_node_groups_in_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to increase node groups in global replication group"
        ) from exc
    return IncreaseNodeGroupsInGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def increase_replica_count(
    replication_group_id: str,
    apply_immediately: bool,
    *,
    new_replica_count: int | None = None,
    replica_configuration: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> IncreaseReplicaCountResult:
    """Increase replica count.

    Args:
        replication_group_id: Replication group id.
        apply_immediately: Apply immediately.
        new_replica_count: New replica count.
        replica_configuration: Replica configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["ApplyImmediately"] = apply_immediately
    if new_replica_count is not None:
        kwargs["NewReplicaCount"] = new_replica_count
    if replica_configuration is not None:
        kwargs["ReplicaConfiguration"] = replica_configuration
    try:
        resp = client.increase_replica_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to increase replica count") from exc
    return IncreaseReplicaCountResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def list_allowed_node_type_modifications(
    *,
    cache_cluster_id: str | None = None,
    replication_group_id: str | None = None,
    region_name: str | None = None,
) -> ListAllowedNodeTypeModificationsResult:
    """List allowed node type modifications.

    Args:
        cache_cluster_id: Cache cluster id.
        replication_group_id: Replication group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    if cache_cluster_id is not None:
        kwargs["CacheClusterId"] = cache_cluster_id
    if replication_group_id is not None:
        kwargs["ReplicationGroupId"] = replication_group_id
    try:
        resp = client.list_allowed_node_type_modifications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list allowed node type modifications") from exc
    return ListAllowedNodeTypeModificationsResult(
        scale_up_modifications=resp.get("ScaleUpModifications"),
        scale_down_modifications=resp.get("ScaleDownModifications"),
    )


def modify_cache_parameter_group(
    cache_parameter_group_name: str,
    parameter_name_values: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyCacheParameterGroupResult:
    """Modify cache parameter group.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        parameter_name_values: Parameter name values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    kwargs["ParameterNameValues"] = parameter_name_values
    try:
        resp = client.modify_cache_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify cache parameter group") from exc
    return ModifyCacheParameterGroupResult(
        cache_parameter_group_name=resp.get("CacheParameterGroupName"),
    )


def modify_cache_subnet_group(
    cache_subnet_group_name: str,
    *,
    cache_subnet_group_description: str | None = None,
    subnet_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyCacheSubnetGroupResult:
    """Modify cache subnet group.

    Args:
        cache_subnet_group_name: Cache subnet group name.
        cache_subnet_group_description: Cache subnet group description.
        subnet_ids: Subnet ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSubnetGroupName"] = cache_subnet_group_name
    if cache_subnet_group_description is not None:
        kwargs["CacheSubnetGroupDescription"] = cache_subnet_group_description
    if subnet_ids is not None:
        kwargs["SubnetIds"] = subnet_ids
    try:
        resp = client.modify_cache_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify cache subnet group") from exc
    return ModifyCacheSubnetGroupResult(
        cache_subnet_group=resp.get("CacheSubnetGroup"),
    )


def modify_global_replication_group(
    global_replication_group_id: str,
    apply_immediately: bool,
    *,
    cache_node_type: str | None = None,
    engine: str | None = None,
    engine_version: str | None = None,
    cache_parameter_group_name: str | None = None,
    global_replication_group_description: str | None = None,
    automatic_failover_enabled: bool | None = None,
    region_name: str | None = None,
) -> ModifyGlobalReplicationGroupResult:
    """Modify global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        apply_immediately: Apply immediately.
        cache_node_type: Cache node type.
        engine: Engine.
        engine_version: Engine version.
        cache_parameter_group_name: Cache parameter group name.
        global_replication_group_description: Global replication group description.
        automatic_failover_enabled: Automatic failover enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["ApplyImmediately"] = apply_immediately
    if cache_node_type is not None:
        kwargs["CacheNodeType"] = cache_node_type
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if cache_parameter_group_name is not None:
        kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    if global_replication_group_description is not None:
        kwargs["GlobalReplicationGroupDescription"] = global_replication_group_description
    if automatic_failover_enabled is not None:
        kwargs["AutomaticFailoverEnabled"] = automatic_failover_enabled
    try:
        resp = client.modify_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify global replication group") from exc
    return ModifyGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def modify_replication_group_shard_configuration(
    replication_group_id: str,
    node_group_count: int,
    apply_immediately: bool,
    *,
    resharding_configuration: list[dict[str, Any]] | None = None,
    node_groups_to_remove: list[str] | None = None,
    node_groups_to_retain: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyReplicationGroupShardConfigurationResult:
    """Modify replication group shard configuration.

    Args:
        replication_group_id: Replication group id.
        node_group_count: Node group count.
        apply_immediately: Apply immediately.
        resharding_configuration: Resharding configuration.
        node_groups_to_remove: Node groups to remove.
        node_groups_to_retain: Node groups to retain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["NodeGroupCount"] = node_group_count
    kwargs["ApplyImmediately"] = apply_immediately
    if resharding_configuration is not None:
        kwargs["ReshardingConfiguration"] = resharding_configuration
    if node_groups_to_remove is not None:
        kwargs["NodeGroupsToRemove"] = node_groups_to_remove
    if node_groups_to_retain is not None:
        kwargs["NodeGroupsToRetain"] = node_groups_to_retain
    try:
        resp = client.modify_replication_group_shard_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify replication group shard configuration") from exc
    return ModifyReplicationGroupShardConfigurationResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def modify_serverless_cache(
    serverless_cache_name: str,
    *,
    description: str | None = None,
    cache_usage_limits: dict[str, Any] | None = None,
    remove_user_group: bool | None = None,
    user_group_id: str | None = None,
    security_group_ids: list[str] | None = None,
    snapshot_retention_limit: int | None = None,
    daily_snapshot_time: str | None = None,
    engine: str | None = None,
    major_engine_version: str | None = None,
    region_name: str | None = None,
) -> ModifyServerlessCacheResult:
    """Modify serverless cache.

    Args:
        serverless_cache_name: Serverless cache name.
        description: Description.
        cache_usage_limits: Cache usage limits.
        remove_user_group: Remove user group.
        user_group_id: User group id.
        security_group_ids: Security group ids.
        snapshot_retention_limit: Snapshot retention limit.
        daily_snapshot_time: Daily snapshot time.
        engine: Engine.
        major_engine_version: Major engine version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerlessCacheName"] = serverless_cache_name
    if description is not None:
        kwargs["Description"] = description
    if cache_usage_limits is not None:
        kwargs["CacheUsageLimits"] = cache_usage_limits
    if remove_user_group is not None:
        kwargs["RemoveUserGroup"] = remove_user_group
    if user_group_id is not None:
        kwargs["UserGroupId"] = user_group_id
    if security_group_ids is not None:
        kwargs["SecurityGroupIds"] = security_group_ids
    if snapshot_retention_limit is not None:
        kwargs["SnapshotRetentionLimit"] = snapshot_retention_limit
    if daily_snapshot_time is not None:
        kwargs["DailySnapshotTime"] = daily_snapshot_time
    if engine is not None:
        kwargs["Engine"] = engine
    if major_engine_version is not None:
        kwargs["MajorEngineVersion"] = major_engine_version
    try:
        resp = client.modify_serverless_cache(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify serverless cache") from exc
    return ModifyServerlessCacheResult(
        serverless_cache=resp.get("ServerlessCache"),
    )


def modify_user(
    user_id: str,
    *,
    access_string: str | None = None,
    append_access_string: str | None = None,
    passwords: list[str] | None = None,
    no_password_required: bool | None = None,
    authentication_mode: dict[str, Any] | None = None,
    engine: str | None = None,
    region_name: str | None = None,
) -> ModifyUserResult:
    """Modify user.

    Args:
        user_id: User id.
        access_string: Access string.
        append_access_string: Append access string.
        passwords: Passwords.
        no_password_required: No password required.
        authentication_mode: Authentication mode.
        engine: Engine.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    if access_string is not None:
        kwargs["AccessString"] = access_string
    if append_access_string is not None:
        kwargs["AppendAccessString"] = append_access_string
    if passwords is not None:
        kwargs["Passwords"] = passwords
    if no_password_required is not None:
        kwargs["NoPasswordRequired"] = no_password_required
    if authentication_mode is not None:
        kwargs["AuthenticationMode"] = authentication_mode
    if engine is not None:
        kwargs["Engine"] = engine
    try:
        resp = client.modify_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify user") from exc
    return ModifyUserResult(
        user_id=resp.get("UserId"),
        user_name=resp.get("UserName"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        access_string=resp.get("AccessString"),
        user_group_ids=resp.get("UserGroupIds"),
        authentication=resp.get("Authentication"),
        arn=resp.get("ARN"),
    )


def modify_user_group(
    user_group_id: str,
    *,
    user_ids_to_add: list[str] | None = None,
    user_ids_to_remove: list[str] | None = None,
    engine: str | None = None,
    region_name: str | None = None,
) -> ModifyUserGroupResult:
    """Modify user group.

    Args:
        user_group_id: User group id.
        user_ids_to_add: User ids to add.
        user_ids_to_remove: User ids to remove.
        engine: Engine.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserGroupId"] = user_group_id
    if user_ids_to_add is not None:
        kwargs["UserIdsToAdd"] = user_ids_to_add
    if user_ids_to_remove is not None:
        kwargs["UserIdsToRemove"] = user_ids_to_remove
    if engine is not None:
        kwargs["Engine"] = engine
    try:
        resp = client.modify_user_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify user group") from exc
    return ModifyUserGroupResult(
        user_group_id=resp.get("UserGroupId"),
        status=resp.get("Status"),
        engine=resp.get("Engine"),
        user_ids=resp.get("UserIds"),
        minimum_engine_version=resp.get("MinimumEngineVersion"),
        pending_changes=resp.get("PendingChanges"),
        replication_groups=resp.get("ReplicationGroups"),
        serverless_caches=resp.get("ServerlessCaches"),
        arn=resp.get("ARN"),
    )


def purchase_reserved_cache_nodes_offering(
    reserved_cache_nodes_offering_id: str,
    *,
    reserved_cache_node_id: str | None = None,
    cache_node_count: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PurchaseReservedCacheNodesOfferingResult:
    """Purchase reserved cache nodes offering.

    Args:
        reserved_cache_nodes_offering_id: Reserved cache nodes offering id.
        reserved_cache_node_id: Reserved cache node id.
        cache_node_count: Cache node count.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedCacheNodesOfferingId"] = reserved_cache_nodes_offering_id
    if reserved_cache_node_id is not None:
        kwargs["ReservedCacheNodeId"] = reserved_cache_node_id
    if cache_node_count is not None:
        kwargs["CacheNodeCount"] = cache_node_count
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.purchase_reserved_cache_nodes_offering(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to purchase reserved cache nodes offering") from exc
    return PurchaseReservedCacheNodesOfferingResult(
        reserved_cache_node=resp.get("ReservedCacheNode"),
    )


def rebalance_slots_in_global_replication_group(
    global_replication_group_id: str,
    apply_immediately: bool,
    region_name: str | None = None,
) -> RebalanceSlotsInGlobalReplicationGroupResult:
    """Rebalance slots in global replication group.

    Args:
        global_replication_group_id: Global replication group id.
        apply_immediately: Apply immediately.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalReplicationGroupId"] = global_replication_group_id
    kwargs["ApplyImmediately"] = apply_immediately
    try:
        resp = client.rebalance_slots_in_global_replication_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to rebalance slots in global replication group") from exc
    return RebalanceSlotsInGlobalReplicationGroupResult(
        global_replication_group=resp.get("GlobalReplicationGroup"),
    )


def remove_tags_from_resource(
    resource_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> RemoveTagsFromResourceResult:
    """Remove tags from resource.

    Args:
        resource_name: Resource name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["TagKeys"] = tag_keys
    try:
        resp = client.remove_tags_from_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return RemoveTagsFromResourceResult(
        tag_list=resp.get("TagList"),
    )


def reset_cache_parameter_group(
    cache_parameter_group_name: str,
    *,
    reset_all_parameters: bool | None = None,
    parameter_name_values: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ResetCacheParameterGroupResult:
    """Reset cache parameter group.

    Args:
        cache_parameter_group_name: Cache parameter group name.
        reset_all_parameters: Reset all parameters.
        parameter_name_values: Parameter name values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheParameterGroupName"] = cache_parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameter_name_values is not None:
        kwargs["ParameterNameValues"] = parameter_name_values
    try:
        resp = client.reset_cache_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reset cache parameter group") from exc
    return ResetCacheParameterGroupResult(
        cache_parameter_group_name=resp.get("CacheParameterGroupName"),
    )


def revoke_cache_security_group_ingress(
    cache_security_group_name: str,
    ec2_security_group_name: str,
    ec2_security_group_owner_id: str,
    region_name: str | None = None,
) -> RevokeCacheSecurityGroupIngressResult:
    """Revoke cache security group ingress.

    Args:
        cache_security_group_name: Cache security group name.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CacheSecurityGroupName"] = cache_security_group_name
    kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = client.revoke_cache_security_group_ingress(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to revoke cache security group ingress") from exc
    return RevokeCacheSecurityGroupIngressResult(
        cache_security_group=resp.get("CacheSecurityGroup"),
    )


def run_failover(
    replication_group_id: str,
    node_group_id: str,
    region_name: str | None = None,
) -> RunFailoverResult:
    """Run failover.

    Args:
        replication_group_id: Replication group id.
        node_group_id: Node group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["NodeGroupId"] = node_group_id
    try:
        resp = client.test_failover(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run failover") from exc
    return RunFailoverResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def run_migration(
    replication_group_id: str,
    customer_node_endpoint_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> RunMigrationResult:
    """Run migration.

    Args:
        replication_group_id: Replication group id.
        customer_node_endpoint_list: Customer node endpoint list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["CustomerNodeEndpointList"] = customer_node_endpoint_list
    try:
        resp = client.test_migration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run migration") from exc
    return RunMigrationResult(
        replication_group=resp.get("ReplicationGroup"),
    )


def start_migration(
    replication_group_id: str,
    customer_node_endpoint_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> StartMigrationResult:
    """Start migration.

    Args:
        replication_group_id: Replication group id.
        customer_node_endpoint_list: Customer node endpoint list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("elasticache", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicationGroupId"] = replication_group_id
    kwargs["CustomerNodeEndpointList"] = customer_node_endpoint_list
    try:
        resp = client.start_migration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start migration") from exc
    return StartMigrationResult(
        replication_group=resp.get("ReplicationGroup"),
    )
