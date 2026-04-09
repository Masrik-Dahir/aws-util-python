"""Native async DocumentDB utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.documentdb import (
    AddSourceIdentifierToSubscriptionResult,
    ApplyPendingMaintenanceActionResult,
    ClusterResult,
    ClusterSnapshotResult,
    CopyDbClusterParameterGroupResult,
    CreateDbClusterParameterGroupResult,
    CreateDbSubnetGroupResult,
    CreateEventSubscriptionResult,
    CreateGlobalClusterResult,
    DeleteEventSubscriptionResult,
    DeleteGlobalClusterResult,
    DescribeCertificatesResult,
    DescribeDbClusterParameterGroupsResult,
    DescribeDbClusterParametersResult,
    DescribeDbClusterSnapshotAttributesResult,
    DescribeDbEngineVersionsResult,
    DescribeDbSubnetGroupsResult,
    DescribeEngineDefaultClusterParametersResult,
    DescribeEventCategoriesResult,
    DescribeEventsResult,
    DescribeEventSubscriptionsResult,
    DescribeGlobalClustersResult,
    DescribeOrderableDbInstanceOptionsResult,
    DescribePendingMaintenanceActionsResult,
    FailoverGlobalClusterResult,
    InstanceResult,
    ListTagsForResourceResult,
    ModifyDbClusterParameterGroupResult,
    ModifyDbClusterSnapshotAttributeResult,
    ModifyDbSubnetGroupResult,
    ModifyEventSubscriptionResult,
    ModifyGlobalClusterResult,
    RemoveFromGlobalClusterResult,
    RemoveSourceIdentifierFromSubscriptionResult,
    ResetDbClusterParameterGroupResult,
    RestoreDbClusterToPointInTimeResult,
    StartDbClusterResult,
    StopDbClusterResult,
    SwitchoverGlobalClusterResult,
    _parse_cluster,
    _parse_instance,
    _parse_snapshot,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error

__all__ = [
    "AddSourceIdentifierToSubscriptionResult",
    "ApplyPendingMaintenanceActionResult",
    "ClusterResult",
    "ClusterSnapshotResult",
    "CopyDbClusterParameterGroupResult",
    "CreateDbClusterParameterGroupResult",
    "CreateDbSubnetGroupResult",
    "CreateEventSubscriptionResult",
    "CreateGlobalClusterResult",
    "DeleteEventSubscriptionResult",
    "DeleteGlobalClusterResult",
    "DescribeCertificatesResult",
    "DescribeDbClusterParameterGroupsResult",
    "DescribeDbClusterParametersResult",
    "DescribeDbClusterSnapshotAttributesResult",
    "DescribeDbEngineVersionsResult",
    "DescribeDbSubnetGroupsResult",
    "DescribeEngineDefaultClusterParametersResult",
    "DescribeEventCategoriesResult",
    "DescribeEventSubscriptionsResult",
    "DescribeEventsResult",
    "DescribeGlobalClustersResult",
    "DescribeOrderableDbInstanceOptionsResult",
    "DescribePendingMaintenanceActionsResult",
    "FailoverGlobalClusterResult",
    "InstanceResult",
    "ListTagsForResourceResult",
    "ModifyDbClusterParameterGroupResult",
    "ModifyDbClusterSnapshotAttributeResult",
    "ModifyDbSubnetGroupResult",
    "ModifyEventSubscriptionResult",
    "ModifyGlobalClusterResult",
    "RemoveFromGlobalClusterResult",
    "RemoveSourceIdentifierFromSubscriptionResult",
    "ResetDbClusterParameterGroupResult",
    "RestoreDbClusterToPointInTimeResult",
    "StartDbClusterResult",
    "StopDbClusterResult",
    "SwitchoverGlobalClusterResult",
    "add_source_identifier_to_subscription",
    "add_tags_to_resource",
    "apply_pending_maintenance_action",
    "copy_db_cluster_parameter_group",
    "copy_db_cluster_snapshot",
    "create_db_cluster",
    "create_db_cluster_parameter_group",
    "create_db_cluster_snapshot",
    "create_db_instance",
    "create_db_subnet_group",
    "create_event_subscription",
    "create_global_cluster",
    "delete_db_cluster",
    "delete_db_cluster_parameter_group",
    "delete_db_cluster_snapshot",
    "delete_db_instance",
    "delete_db_subnet_group",
    "delete_event_subscription",
    "delete_global_cluster",
    "describe_certificates",
    "describe_db_cluster_parameter_groups",
    "describe_db_cluster_parameters",
    "describe_db_cluster_snapshot_attributes",
    "describe_db_cluster_snapshots",
    "describe_db_clusters",
    "describe_db_engine_versions",
    "describe_db_instances",
    "describe_db_subnet_groups",
    "describe_engine_default_cluster_parameters",
    "describe_event_categories",
    "describe_event_subscriptions",
    "describe_events",
    "describe_global_clusters",
    "describe_orderable_db_instance_options",
    "describe_pending_maintenance_actions",
    "failover_db_cluster",
    "failover_global_cluster",
    "list_tags_for_resource",
    "modify_db_cluster",
    "modify_db_cluster_parameter_group",
    "modify_db_cluster_snapshot_attribute",
    "modify_db_instance",
    "modify_db_subnet_group",
    "modify_event_subscription",
    "modify_global_cluster",
    "reboot_db_instance",
    "remove_from_global_cluster",
    "remove_source_identifier_from_subscription",
    "remove_tags_from_resource",
    "reset_db_cluster_parameter_group",
    "restore_db_cluster_from_snapshot",
    "restore_db_cluster_to_point_in_time",
    "start_db_cluster",
    "stop_db_cluster",
    "switchover_global_cluster",
    "wait_for_db_cluster",
    "wait_for_db_instance",
]


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def create_db_cluster(
    db_cluster_identifier: str,
    *,
    engine: str = "docdb",
    engine_version: str | None = None,
    master_username: str = "docdbadmin",
    master_user_password: str = "changeme123",
    db_subnet_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Create a new DocumentDB cluster.

    Args:
        db_cluster_identifier: Unique cluster identifier.
        engine: Database engine (default ``"docdb"``).
        engine_version: Engine version.
        master_username: Master user name.
        master_user_password: Master user password.
        db_subnet_group_name: Subnet group for the cluster.
        vpc_security_group_ids: VPC security group IDs.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
        "Engine": engine,
        "MasterUsername": master_username,
        "MasterUserPassword": master_user_password,
    }
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create DB cluster {db_cluster_identifier!r}") from exc
    return _parse_cluster(resp["DBCluster"])


async def describe_db_clusters(
    *,
    db_cluster_identifier: str | None = None,
    region_name: str | None = None,
) -> list[ClusterResult]:
    """Describe one or more DocumentDB clusters.

    Args:
        db_cluster_identifier: Specific cluster ID. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    clusters: list[ClusterResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeDBClusters", **kwargs)
            for item in resp.get("DBClusters", []):
                clusters.append(_parse_cluster(item))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_clusters failed") from exc
    return clusters


async def modify_db_cluster(
    db_cluster_identifier: str,
    *,
    engine_version: str | None = None,
    master_user_password: str | None = None,
    apply_immediately: bool = True,
    region_name: str | None = None,
) -> ClusterResult:
    """Modify an existing DocumentDB cluster.

    Args:
        db_cluster_identifier: Cluster identifier.
        engine_version: New engine version.
        master_user_password: New master password.
        apply_immediately: Apply changes immediately.
        region_name: AWS region override.

    Returns:
        The modified :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
        "ApplyImmediately": apply_immediately,
    }
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    try:
        resp = await client.call("ModifyDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to modify DB cluster {db_cluster_identifier!r}") from exc
    return _parse_cluster(resp["DBCluster"])


async def delete_db_cluster(
    db_cluster_identifier: str,
    *,
    skip_final_snapshot: bool = True,
    final_db_snapshot_identifier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete a DocumentDB cluster.

    Args:
        db_cluster_identifier: Cluster identifier.
        skip_final_snapshot: Skip the final snapshot on deletion.
        final_db_snapshot_identifier: Snapshot name if not skipping.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
        "SkipFinalSnapshot": skip_final_snapshot,
    }
    if final_db_snapshot_identifier is not None:
        kwargs["FinalDBSnapshotIdentifier"] = final_db_snapshot_identifier
    try:
        await client.call("DeleteDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete DB cluster {db_cluster_identifier!r}") from exc


async def failover_db_cluster(
    db_cluster_identifier: str,
    *,
    target_db_instance_identifier: str | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Initiate a failover for a DocumentDB cluster.

    Args:
        db_cluster_identifier: Cluster identifier.
        target_db_instance_identifier: Instance to promote to primary.
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` after failover initiation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
    }
    if target_db_instance_identifier is not None:
        kwargs["TargetDBInstanceIdentifier"] = target_db_instance_identifier
    try:
        resp = await client.call("FailoverDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to failover DB cluster {db_cluster_identifier!r}"
        ) from exc
    return _parse_cluster(resp["DBCluster"])


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


async def create_db_instance(
    db_instance_identifier: str,
    *,
    db_cluster_identifier: str,
    db_instance_class: str = "db.r5.large",
    engine: str = "docdb",
    availability_zone: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> InstanceResult:
    """Create a new DocumentDB instance within a cluster.

    Args:
        db_instance_identifier: Unique instance identifier.
        db_cluster_identifier: Cluster to add the instance to.
        db_instance_class: Instance class.
        engine: Database engine (default ``"docdb"``).
        availability_zone: Preferred availability zone.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBInstanceIdentifier": db_instance_identifier,
        "DBClusterIdentifier": db_cluster_identifier,
        "DBInstanceClass": db_instance_class,
        "Engine": engine,
    }
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateDBInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to create DB instance {db_instance_identifier!r}"
        ) from exc
    return _parse_instance(resp["DBInstance"])


async def describe_db_instances(
    *,
    db_instance_identifier: str | None = None,
    region_name: str | None = None,
) -> list[InstanceResult]:
    """Describe one or more DocumentDB instances.

    Args:
        db_instance_identifier: Specific instance ID. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if db_instance_identifier is not None:
        kwargs["DBInstanceIdentifier"] = db_instance_identifier
    instances: list[InstanceResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeDBInstances", **kwargs)
            for item in resp.get("DBInstances", []):
                instances.append(_parse_instance(item))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_instances failed") from exc
    return instances


async def modify_db_instance(
    db_instance_identifier: str,
    *,
    db_instance_class: str | None = None,
    apply_immediately: bool = True,
    region_name: str | None = None,
) -> InstanceResult:
    """Modify an existing DocumentDB instance.

    Args:
        db_instance_identifier: Instance identifier.
        db_instance_class: New instance class.
        apply_immediately: Apply changes immediately.
        region_name: AWS region override.

    Returns:
        The modified :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBInstanceIdentifier": db_instance_identifier,
        "ApplyImmediately": apply_immediately,
    }
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    try:
        resp = await client.call("ModifyDBInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to modify DB instance {db_instance_identifier!r}"
        ) from exc
    return _parse_instance(resp["DBInstance"])


async def delete_db_instance(
    db_instance_identifier: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a DocumentDB instance.

    Args:
        db_instance_identifier: Instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    try:
        await client.call(
            "DeleteDBInstance",
            DBInstanceIdentifier=db_instance_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to delete DB instance {db_instance_identifier!r}"
        ) from exc


async def reboot_db_instance(
    db_instance_identifier: str,
    *,
    force_failover: bool = False,
    region_name: str | None = None,
) -> InstanceResult:
    """Reboot a DocumentDB instance.

    Args:
        db_instance_identifier: Instance identifier.
        force_failover: Force a failover during reboot.
        region_name: AWS region override.

    Returns:
        The :class:`InstanceResult` after reboot initiation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    try:
        resp = await client.call(
            "RebootDBInstance",
            DBInstanceIdentifier=db_instance_identifier,
            ForceFailover=force_failover,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to reboot DB instance {db_instance_identifier!r}"
        ) from exc
    return _parse_instance(resp["DBInstance"])


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def create_db_cluster_snapshot(
    db_cluster_snapshot_identifier: str,
    *,
    db_cluster_identifier: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterSnapshotResult:
    """Create a snapshot of a DocumentDB cluster.

    Args:
        db_cluster_snapshot_identifier: Unique snapshot identifier.
        db_cluster_identifier: Source cluster identifier.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The newly created :class:`ClusterSnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterSnapshotIdentifier": db_cluster_snapshot_identifier,
        "DBClusterIdentifier": db_cluster_identifier,
    }
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateDBClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create DB cluster snapshot {db_cluster_snapshot_identifier!r}",
        ) from exc
    return _parse_snapshot(resp["DBClusterSnapshot"])


async def describe_db_cluster_snapshots(
    *,
    db_cluster_snapshot_identifier: str | None = None,
    db_cluster_identifier: str | None = None,
    region_name: str | None = None,
) -> list[ClusterSnapshotResult]:
    """Describe one or more DocumentDB cluster snapshots.

    Args:
        db_cluster_snapshot_identifier: Specific snapshot ID.
        db_cluster_identifier: Filter by source cluster.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterSnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_snapshot_identifier is not None:
        kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    snapshots: list[ClusterSnapshotResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["Marker"] = token
            resp = await client.call("DescribeDBClusterSnapshots", **kwargs)
            for item in resp.get("DBClusterSnapshots", []):
                snapshots.append(_parse_snapshot(item))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_cluster_snapshots failed") from exc
    return snapshots


async def copy_db_cluster_snapshot(
    source_identifier: str,
    target_identifier: str,
    *,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterSnapshotResult:
    """Copy a DocumentDB cluster snapshot.

    Args:
        source_identifier: Source snapshot identifier.
        target_identifier: Target snapshot identifier.
        tags: Key/value tags for the copy.
        region_name: AWS region override.

    Returns:
        The copied :class:`ClusterSnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "SourceDBClusterSnapshotIdentifier": source_identifier,
        "TargetDBClusterSnapshotIdentifier": target_identifier,
    }
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CopyDBClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to copy DB cluster snapshot {source_identifier!r}",
        ) from exc
    return _parse_snapshot(resp["DBClusterSnapshot"])


async def delete_db_cluster_snapshot(
    db_cluster_snapshot_identifier: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a DocumentDB cluster snapshot.

    Args:
        db_cluster_snapshot_identifier: Snapshot identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    try:
        await client.call(
            "DeleteDBClusterSnapshot",
            DBClusterSnapshotIdentifier=db_cluster_snapshot_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete DB cluster snapshot {db_cluster_snapshot_identifier!r}",
        ) from exc


async def restore_db_cluster_from_snapshot(
    db_cluster_identifier: str,
    *,
    snapshot_identifier: str,
    engine: str = "docdb",
    vpc_security_group_ids: list[str] | None = None,
    db_subnet_group_name: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Restore a DocumentDB cluster from a snapshot.

    Args:
        db_cluster_identifier: New cluster identifier.
        snapshot_identifier: Snapshot to restore from.
        engine: Database engine (default ``"docdb"``).
        vpc_security_group_ids: VPC security group IDs.
        db_subnet_group_name: Subnet group name.
        tags: Key/value tags.
        region_name: AWS region override.

    Returns:
        The restored :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
        "SnapshotIdentifier": snapshot_identifier,
        "Engine": engine,
    }
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if tags is not None:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("RestoreDBClusterFromSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to restore DB cluster from snapshot {snapshot_identifier!r}",
        ) from exc
    return _parse_cluster(resp["DBCluster"])


# ---------------------------------------------------------------------------
# Wait / polling helpers
# ---------------------------------------------------------------------------


async def wait_for_db_cluster(
    db_cluster_identifier: str,
    *,
    target_status: str = "available",
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until a DocumentDB cluster reaches the target status.

    Args:
        db_cluster_identifier: Cluster identifier.
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
        clusters = await describe_db_clusters(
            db_cluster_identifier=db_cluster_identifier,
            region_name=region_name,
        )
        if not clusters:
            raise AwsServiceError(f"DB cluster {db_cluster_identifier!r} not found")
        cluster = clusters[0]
        if cluster.status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"DB cluster {db_cluster_identifier!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {cluster.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def wait_for_db_instance(
    db_instance_identifier: str,
    *,
    target_status: str = "available",
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> InstanceResult:
    """Poll until a DocumentDB instance reaches the target status.

    Args:
        db_instance_identifier: Instance identifier.
        target_status: Desired status (default ``"available"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`InstanceResult` in the target status.

    Raises:
        TimeoutError: If the instance does not reach *target_status* in time.
        RuntimeError: If the instance is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        instances = await describe_db_instances(
            db_instance_identifier=db_instance_identifier,
            region_name=region_name,
        )
        if not instances:
            raise AwsServiceError(f"DB instance {db_instance_identifier!r} not found")
        instance = instances[0]
        if instance.status == target_status:
            return instance
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"DB instance {db_instance_identifier!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {instance.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def add_source_identifier_to_subscription(
    subscription_name: str,
    source_identifier: str,
    region_name: str | None = None,
) -> AddSourceIdentifierToSubscriptionResult:
    """Add source identifier to subscription.

    Args:
        subscription_name: Subscription name.
        source_identifier: Source identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SourceIdentifier"] = source_identifier
    try:
        resp = await client.call("AddSourceIdentifierToSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add source identifier to subscription") from exc
    return AddSourceIdentifierToSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def add_tags_to_resource(
    resource_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags to resource.

    Args:
        resource_name: Resource name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["Tags"] = tags
    try:
        await client.call("AddTagsToResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags to resource") from exc
    return None


async def apply_pending_maintenance_action(
    resource_identifier: str,
    apply_action: str,
    opt_in_type: str,
    region_name: str | None = None,
) -> ApplyPendingMaintenanceActionResult:
    """Apply pending maintenance action.

    Args:
        resource_identifier: Resource identifier.
        apply_action: Apply action.
        opt_in_type: Opt in type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceIdentifier"] = resource_identifier
    kwargs["ApplyAction"] = apply_action
    kwargs["OptInType"] = opt_in_type
    try:
        resp = await client.call("ApplyPendingMaintenanceAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to apply pending maintenance action") from exc
    return ApplyPendingMaintenanceActionResult(
        resource_pending_maintenance_actions=resp.get("ResourcePendingMaintenanceActions"),
    )


async def copy_db_cluster_parameter_group(
    source_db_cluster_parameter_group_identifier: str,
    target_db_cluster_parameter_group_identifier: str,
    target_db_cluster_parameter_group_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CopyDbClusterParameterGroupResult:
    """Copy db cluster parameter group.

    Args:
        source_db_cluster_parameter_group_identifier: Source db cluster parameter group identifier.
        target_db_cluster_parameter_group_identifier: Target db cluster parameter group identifier.
        target_db_cluster_parameter_group_description: Target db cluster parameter group description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBClusterParameterGroupIdentifier"] = source_db_cluster_parameter_group_identifier
    kwargs["TargetDBClusterParameterGroupIdentifier"] = target_db_cluster_parameter_group_identifier
    kwargs["TargetDBClusterParameterGroupDescription"] = (
        target_db_cluster_parameter_group_description
    )
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CopyDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy db cluster parameter group") from exc
    return CopyDbClusterParameterGroupResult(
        db_cluster_parameter_group=resp.get("DBClusterParameterGroup"),
    )


async def create_db_cluster_parameter_group(
    db_cluster_parameter_group_name: str,
    db_parameter_group_family: str,
    description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbClusterParameterGroupResult:
    """Create db cluster parameter group.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        db_parameter_group_family: Db parameter group family.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create db cluster parameter group") from exc
    return CreateDbClusterParameterGroupResult(
        db_cluster_parameter_group=resp.get("DBClusterParameterGroup"),
    )


async def create_db_subnet_group(
    db_subnet_group_name: str,
    db_subnet_group_description: str,
    subnet_ids: list[str],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbSubnetGroupResult:
    """Create db subnet group.

    Args:
        db_subnet_group_name: Db subnet group name.
        db_subnet_group_description: Db subnet group description.
        subnet_ids: Subnet ids.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    kwargs["DBSubnetGroupDescription"] = db_subnet_group_description
    kwargs["SubnetIds"] = subnet_ids
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDBSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create db subnet group") from exc
    return CreateDbSubnetGroupResult(
        db_subnet_group=resp.get("DBSubnetGroup"),
    )


async def create_event_subscription(
    subscription_name: str,
    sns_topic_arn: str,
    *,
    source_type: str | None = None,
    event_categories: list[str] | None = None,
    source_ids: list[str] | None = None,
    enabled: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateEventSubscriptionResult:
    """Create event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        event_categories: Event categories.
        source_ids: Source ids.
        enabled: Enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if source_ids is not None:
        kwargs["SourceIds"] = source_ids
    if enabled is not None:
        kwargs["Enabled"] = enabled
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create event subscription") from exc
    return CreateEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def create_global_cluster(
    global_cluster_identifier: str,
    *,
    source_db_cluster_identifier: str | None = None,
    engine: str | None = None,
    engine_version: str | None = None,
    deletion_protection: bool | None = None,
    database_name: str | None = None,
    storage_encrypted: bool | None = None,
    region_name: str | None = None,
) -> CreateGlobalClusterResult:
    """Create global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        source_db_cluster_identifier: Source db cluster identifier.
        engine: Engine.
        engine_version: Engine version.
        deletion_protection: Deletion protection.
        database_name: Database name.
        storage_encrypted: Storage encrypted.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if source_db_cluster_identifier is not None:
        kwargs["SourceDBClusterIdentifier"] = source_db_cluster_identifier
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    try:
        resp = await client.call("CreateGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create global cluster") from exc
    return CreateGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def delete_db_cluster_parameter_group(
    db_cluster_parameter_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete db cluster parameter group.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    try:
        await client.call("DeleteDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster parameter group") from exc
    return None


async def delete_db_subnet_group(
    db_subnet_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete db subnet group.

    Args:
        db_subnet_group_name: Db subnet group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    try:
        await client.call("DeleteDBSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db subnet group") from exc
    return None


async def delete_event_subscription(
    subscription_name: str,
    region_name: str | None = None,
) -> DeleteEventSubscriptionResult:
    """Delete event subscription.

    Args:
        subscription_name: Subscription name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    try:
        resp = await client.call("DeleteEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete event subscription") from exc
    return DeleteEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def delete_global_cluster(
    global_cluster_identifier: str,
    region_name: str | None = None,
) -> DeleteGlobalClusterResult:
    """Delete global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    try:
        resp = await client.call("DeleteGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete global cluster") from exc
    return DeleteGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def describe_certificates(
    *,
    certificate_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCertificatesResult:
    """Describe certificates.

    Args:
        certificate_identifier: Certificate identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if certificate_identifier is not None:
        kwargs["CertificateIdentifier"] = certificate_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe certificates") from exc
    return DescribeCertificatesResult(
        certificates=resp.get("Certificates"),
        marker=resp.get("Marker"),
    )


async def describe_db_cluster_parameter_groups(
    *,
    db_cluster_parameter_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterParameterGroupsResult:
    """Describe db cluster parameter groups.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBClusterParameterGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster parameter groups") from exc
    return DescribeDbClusterParameterGroupsResult(
        marker=resp.get("Marker"),
        db_cluster_parameter_groups=resp.get("DBClusterParameterGroups"),
    )


async def describe_db_cluster_parameters(
    db_cluster_parameter_group_name: str,
    *,
    source: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterParametersResult:
    """Describe db cluster parameters.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        source: Source.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if source is not None:
        kwargs["Source"] = source
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBClusterParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster parameters") from exc
    return DescribeDbClusterParametersResult(
        parameters=resp.get("Parameters"),
        marker=resp.get("Marker"),
    )


async def describe_db_cluster_snapshot_attributes(
    db_cluster_snapshot_identifier: str,
    region_name: str | None = None,
) -> DescribeDbClusterSnapshotAttributesResult:
    """Describe db cluster snapshot attributes.

    Args:
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    try:
        resp = await client.call("DescribeDBClusterSnapshotAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster snapshot attributes") from exc
    return DescribeDbClusterSnapshotAttributesResult(
        db_cluster_snapshot_attributes_result=resp.get("DBClusterSnapshotAttributesResult"),
    )


async def describe_db_engine_versions(
    *,
    engine: str | None = None,
    engine_version: str | None = None,
    db_parameter_group_family: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    default_only: bool | None = None,
    list_supported_character_sets: bool | None = None,
    list_supported_timezones: bool | None = None,
    region_name: str | None = None,
) -> DescribeDbEngineVersionsResult:
    """Describe db engine versions.

    Args:
        engine: Engine.
        engine_version: Engine version.
        db_parameter_group_family: Db parameter group family.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        default_only: Default only.
        list_supported_character_sets: List supported character sets.
        list_supported_timezones: List supported timezones.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if db_parameter_group_family is not None:
        kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if default_only is not None:
        kwargs["DefaultOnly"] = default_only
    if list_supported_character_sets is not None:
        kwargs["ListSupportedCharacterSets"] = list_supported_character_sets
    if list_supported_timezones is not None:
        kwargs["ListSupportedTimezones"] = list_supported_timezones
    try:
        resp = await client.call("DescribeDBEngineVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db engine versions") from exc
    return DescribeDbEngineVersionsResult(
        marker=resp.get("Marker"),
        db_engine_versions=resp.get("DBEngineVersions"),
    )


async def describe_db_subnet_groups(
    *,
    db_subnet_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbSubnetGroupsResult:
    """Describe db subnet groups.

    Args:
        db_subnet_group_name: Db subnet group name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBSubnetGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db subnet groups") from exc
    return DescribeDbSubnetGroupsResult(
        marker=resp.get("Marker"),
        db_subnet_groups=resp.get("DBSubnetGroups"),
    )


async def describe_engine_default_cluster_parameters(
    db_parameter_group_family: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEngineDefaultClusterParametersResult:
    """Describe engine default cluster parameters.

    Args:
        db_parameter_group_family: Db parameter group family.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEngineDefaultClusterParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe engine default cluster parameters") from exc
    return DescribeEngineDefaultClusterParametersResult(
        engine_defaults=resp.get("EngineDefaults"),
    )


async def describe_event_categories(
    *,
    source_type: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeEventCategoriesResult:
    """Describe event categories.

    Args:
        source_type: Source type.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeEventCategories", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event categories") from exc
    return DescribeEventCategoriesResult(
        event_categories_map_list=resp.get("EventCategoriesMapList"),
    )


async def describe_event_subscriptions(
    *,
    subscription_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEventSubscriptionsResult:
    """Describe event subscriptions.

    Args:
        subscription_name: Subscription name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if subscription_name is not None:
        kwargs["SubscriptionName"] = subscription_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEventSubscriptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event subscriptions") from exc
    return DescribeEventSubscriptionsResult(
        marker=resp.get("Marker"),
        event_subscriptions_list=resp.get("EventSubscriptionsList"),
    )


async def describe_events(
    *,
    source_identifier: str | None = None,
    source_type: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    duration: int | None = None,
    event_categories: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
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
        event_categories: Event categories.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
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
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        marker=resp.get("Marker"),
        events=resp.get("Events"),
    )


async def describe_global_clusters(
    *,
    global_cluster_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeGlobalClustersResult:
    """Describe global clusters.

    Args:
        global_cluster_identifier: Global cluster identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if global_cluster_identifier is not None:
        kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeGlobalClusters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe global clusters") from exc
    return DescribeGlobalClustersResult(
        marker=resp.get("Marker"),
        global_clusters=resp.get("GlobalClusters"),
    )


async def describe_orderable_db_instance_options(
    engine: str,
    *,
    engine_version: str | None = None,
    db_instance_class: str | None = None,
    license_model: str | None = None,
    vpc: bool | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeOrderableDbInstanceOptionsResult:
    """Describe orderable db instance options.

    Args:
        engine: Engine.
        engine_version: Engine version.
        db_instance_class: Db instance class.
        license_model: License model.
        vpc: Vpc.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if vpc is not None:
        kwargs["Vpc"] = vpc
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeOrderableDBInstanceOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe orderable db instance options") from exc
    return DescribeOrderableDbInstanceOptionsResult(
        orderable_db_instance_options=resp.get("OrderableDBInstanceOptions"),
        marker=resp.get("Marker"),
    )


async def describe_pending_maintenance_actions(
    *,
    resource_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribePendingMaintenanceActionsResult:
    """Describe pending maintenance actions.

    Args:
        resource_identifier: Resource identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    if resource_identifier is not None:
        kwargs["ResourceIdentifier"] = resource_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribePendingMaintenanceActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe pending maintenance actions") from exc
    return DescribePendingMaintenanceActionsResult(
        pending_maintenance_actions=resp.get("PendingMaintenanceActions"),
        marker=resp.get("Marker"),
    )


async def failover_global_cluster(
    global_cluster_identifier: str,
    target_db_cluster_identifier: str,
    *,
    allow_data_loss: bool | None = None,
    switchover: bool | None = None,
    region_name: str | None = None,
) -> FailoverGlobalClusterResult:
    """Failover global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        target_db_cluster_identifier: Target db cluster identifier.
        allow_data_loss: Allow data loss.
        switchover: Switchover.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["TargetDbClusterIdentifier"] = target_db_cluster_identifier
    if allow_data_loss is not None:
        kwargs["AllowDataLoss"] = allow_data_loss
    if switchover is not None:
        kwargs["Switchover"] = switchover
    try:
        resp = await client.call("FailoverGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to failover global cluster") from exc
    return FailoverGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def list_tags_for_resource(
    resource_name: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_name: Resource name.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tag_list=resp.get("TagList"),
    )


async def modify_db_cluster_parameter_group(
    db_cluster_parameter_group_name: str,
    parameters: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyDbClusterParameterGroupResult:
    """Modify db cluster parameter group.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ModifyDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster parameter group") from exc
    return ModifyDbClusterParameterGroupResult(
        db_cluster_parameter_group_name=resp.get("DBClusterParameterGroupName"),
    )


async def modify_db_cluster_snapshot_attribute(
    db_cluster_snapshot_identifier: str,
    attribute_name: str,
    *,
    values_to_add: list[str] | None = None,
    values_to_remove: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyDbClusterSnapshotAttributeResult:
    """Modify db cluster snapshot attribute.

    Args:
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        attribute_name: Attribute name.
        values_to_add: Values to add.
        values_to_remove: Values to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    kwargs["AttributeName"] = attribute_name
    if values_to_add is not None:
        kwargs["ValuesToAdd"] = values_to_add
    if values_to_remove is not None:
        kwargs["ValuesToRemove"] = values_to_remove
    try:
        resp = await client.call("ModifyDBClusterSnapshotAttribute", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster snapshot attribute") from exc
    return ModifyDbClusterSnapshotAttributeResult(
        db_cluster_snapshot_attributes_result=resp.get("DBClusterSnapshotAttributesResult"),
    )


async def modify_db_subnet_group(
    db_subnet_group_name: str,
    subnet_ids: list[str],
    *,
    db_subnet_group_description: str | None = None,
    region_name: str | None = None,
) -> ModifyDbSubnetGroupResult:
    """Modify db subnet group.

    Args:
        db_subnet_group_name: Db subnet group name.
        subnet_ids: Subnet ids.
        db_subnet_group_description: Db subnet group description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    kwargs["SubnetIds"] = subnet_ids
    if db_subnet_group_description is not None:
        kwargs["DBSubnetGroupDescription"] = db_subnet_group_description
    try:
        resp = await client.call("ModifyDBSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify db subnet group") from exc
    return ModifyDbSubnetGroupResult(
        db_subnet_group=resp.get("DBSubnetGroup"),
    )


async def modify_event_subscription(
    subscription_name: str,
    *,
    sns_topic_arn: str | None = None,
    source_type: str | None = None,
    event_categories: list[str] | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> ModifyEventSubscriptionResult:
    """Modify event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        event_categories: Event categories.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    if sns_topic_arn is not None:
        kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = await client.call("ModifyEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify event subscription") from exc
    return ModifyEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def modify_global_cluster(
    global_cluster_identifier: str,
    *,
    new_global_cluster_identifier: str | None = None,
    deletion_protection: bool | None = None,
    region_name: str | None = None,
) -> ModifyGlobalClusterResult:
    """Modify global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        new_global_cluster_identifier: New global cluster identifier.
        deletion_protection: Deletion protection.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if new_global_cluster_identifier is not None:
        kwargs["NewGlobalClusterIdentifier"] = new_global_cluster_identifier
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    try:
        resp = await client.call("ModifyGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify global cluster") from exc
    return ModifyGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def remove_from_global_cluster(
    global_cluster_identifier: str,
    db_cluster_identifier: str,
    region_name: str | None = None,
) -> RemoveFromGlobalClusterResult:
    """Remove from global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        db_cluster_identifier: Db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["DbClusterIdentifier"] = db_cluster_identifier
    try:
        resp = await client.call("RemoveFromGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove from global cluster") from exc
    return RemoveFromGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def remove_source_identifier_from_subscription(
    subscription_name: str,
    source_identifier: str,
    region_name: str | None = None,
) -> RemoveSourceIdentifierFromSubscriptionResult:
    """Remove source identifier from subscription.

    Args:
        subscription_name: Subscription name.
        source_identifier: Source identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SourceIdentifier"] = source_identifier
    try:
        resp = await client.call("RemoveSourceIdentifierFromSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove source identifier from subscription") from exc
    return RemoveSourceIdentifierFromSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def remove_tags_from_resource(
    resource_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Remove tags from resource.

    Args:
        resource_name: Resource name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("RemoveTagsFromResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return None


async def reset_db_cluster_parameter_group(
    db_cluster_parameter_group_name: str,
    *,
    reset_all_parameters: bool | None = None,
    parameters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ResetDbClusterParameterGroupResult:
    """Reset db cluster parameter group.

    Args:
        db_cluster_parameter_group_name: Db cluster parameter group name.
        reset_all_parameters: Reset all parameters.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ResetDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset db cluster parameter group") from exc
    return ResetDbClusterParameterGroupResult(
        db_cluster_parameter_group_name=resp.get("DBClusterParameterGroupName"),
    )


async def restore_db_cluster_to_point_in_time(
    db_cluster_identifier: str,
    source_db_cluster_identifier: str,
    *,
    restore_type: str | None = None,
    restore_to_time: str | None = None,
    use_latest_restorable_time: bool | None = None,
    port: int | None = None,
    db_subnet_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    kms_key_id: str | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    deletion_protection: bool | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    storage_type: str | None = None,
    network_type: str | None = None,
    region_name: str | None = None,
) -> RestoreDbClusterToPointInTimeResult:
    """Restore db cluster to point in time.

    Args:
        db_cluster_identifier: Db cluster identifier.
        source_db_cluster_identifier: Source db cluster identifier.
        restore_type: Restore type.
        restore_to_time: Restore to time.
        use_latest_restorable_time: Use latest restorable time.
        port: Port.
        db_subnet_group_name: Db subnet group name.
        vpc_security_group_ids: Vpc security group ids.
        tags: Tags.
        kms_key_id: Kms key id.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        deletion_protection: Deletion protection.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        storage_type: Storage type.
        network_type: Network type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["SourceDBClusterIdentifier"] = source_db_cluster_identifier
    if restore_type is not None:
        kwargs["RestoreType"] = restore_type
    if restore_to_time is not None:
        kwargs["RestoreToTime"] = restore_to_time
    if use_latest_restorable_time is not None:
        kwargs["UseLatestRestorableTime"] = use_latest_restorable_time
    if port is not None:
        kwargs["Port"] = port
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if tags is not None:
        kwargs["Tags"] = tags
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    try:
        resp = await client.call("RestoreDBClusterToPointInTime", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore db cluster to point in time") from exc
    return RestoreDbClusterToPointInTimeResult(
        db_cluster=resp.get("DBCluster"),
    )


async def start_db_cluster(
    db_cluster_identifier: str,
    region_name: str | None = None,
) -> StartDbClusterResult:
    """Start db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = await client.call("StartDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start db cluster") from exc
    return StartDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


async def stop_db_cluster(
    db_cluster_identifier: str,
    region_name: str | None = None,
) -> StopDbClusterResult:
    """Stop db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = await client.call("StopDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop db cluster") from exc
    return StopDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


async def switchover_global_cluster(
    global_cluster_identifier: str,
    target_db_cluster_identifier: str,
    region_name: str | None = None,
) -> SwitchoverGlobalClusterResult:
    """Switchover global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        target_db_cluster_identifier: Target db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("docdb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["TargetDbClusterIdentifier"] = target_db_cluster_identifier
    try:
        resp = await client.call("SwitchoverGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to switchover global cluster") from exc
    return SwitchoverGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )
