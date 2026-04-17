"""Native async Neptune utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error
from aws_util.neptune import (
    AddSourceIdentifierToSubscriptionResult,
    ApplyPendingMaintenanceActionResult,
    CopyDbClusterParameterGroupResult,
    CopyDbClusterSnapshotResult,
    CopyDbParameterGroupResult,
    CreateDbClusterEndpointResult,
    CreateDbClusterParameterGroupResult,
    CreateDbParameterGroupResult,
    CreateDbSubnetGroupResult,
    CreateEventSubscriptionResult,
    CreateGlobalClusterResult,
    DeleteDbClusterEndpointResult,
    DeleteDbClusterSnapshotResult,
    DeleteEventSubscriptionResult,
    DeleteGlobalClusterResult,
    DescribeDbClusterEndpointsResult,
    DescribeDbClusterParameterGroupsResult,
    DescribeDbClusterParametersResult,
    DescribeDbClusterSnapshotAttributesResult,
    DescribeDbEngineVersionsResult,
    DescribeDbParameterGroupsResult,
    DescribeDbParametersResult,
    DescribeDbSubnetGroupsResult,
    DescribeEngineDefaultClusterParametersResult,
    DescribeEngineDefaultParametersResult,
    DescribeEventCategoriesResult,
    DescribeEventsResult,
    DescribeEventSubscriptionsResult,
    DescribeGlobalClustersResult,
    DescribeOrderableDbInstanceOptionsResult,
    DescribePendingMaintenanceActionsResult,
    DescribeValidDbInstanceModificationsResult,
    FailoverGlobalClusterResult,
    ListTagsForResourceResult,
    ModifyDbClusterEndpointResult,
    ModifyDbClusterParameterGroupResult,
    ModifyDbClusterSnapshotAttributeResult,
    ModifyDbParameterGroupResult,
    ModifyDbSubnetGroupResult,
    ModifyEventSubscriptionResult,
    ModifyGlobalClusterResult,
    NeptuneCluster,
    NeptuneClusterSnapshot,
    NeptuneInstance,
    PromoteReadReplicaDbClusterResult,
    RebootDbInstanceResult,
    RemoveFromGlobalClusterResult,
    RemoveSourceIdentifierFromSubscriptionResult,
    ResetDbClusterParameterGroupResult,
    ResetDbParameterGroupResult,
    RestoreDbClusterFromSnapshotResult,
    RestoreDbClusterToPointInTimeResult,
    StartDbClusterResult,
    StopDbClusterResult,
    SwitchoverGlobalClusterResult,
    _parse_cluster,
    _parse_cluster_snapshot,
    _parse_instance,
)

__all__ = [
    "AddSourceIdentifierToSubscriptionResult",
    "ApplyPendingMaintenanceActionResult",
    "CopyDbClusterParameterGroupResult",
    "CopyDbClusterSnapshotResult",
    "CopyDbParameterGroupResult",
    "CreateDbClusterEndpointResult",
    "CreateDbClusterParameterGroupResult",
    "CreateDbParameterGroupResult",
    "CreateDbSubnetGroupResult",
    "CreateEventSubscriptionResult",
    "CreateGlobalClusterResult",
    "DeleteDbClusterEndpointResult",
    "DeleteDbClusterSnapshotResult",
    "DeleteEventSubscriptionResult",
    "DeleteGlobalClusterResult",
    "DescribeDbClusterEndpointsResult",
    "DescribeDbClusterParameterGroupsResult",
    "DescribeDbClusterParametersResult",
    "DescribeDbClusterSnapshotAttributesResult",
    "DescribeDbEngineVersionsResult",
    "DescribeDbParameterGroupsResult",
    "DescribeDbParametersResult",
    "DescribeDbSubnetGroupsResult",
    "DescribeEngineDefaultClusterParametersResult",
    "DescribeEngineDefaultParametersResult",
    "DescribeEventCategoriesResult",
    "DescribeEventSubscriptionsResult",
    "DescribeEventsResult",
    "DescribeGlobalClustersResult",
    "DescribeOrderableDbInstanceOptionsResult",
    "DescribePendingMaintenanceActionsResult",
    "DescribeValidDbInstanceModificationsResult",
    "FailoverGlobalClusterResult",
    "ListTagsForResourceResult",
    "ModifyDbClusterEndpointResult",
    "ModifyDbClusterParameterGroupResult",
    "ModifyDbClusterSnapshotAttributeResult",
    "ModifyDbParameterGroupResult",
    "ModifyDbSubnetGroupResult",
    "ModifyEventSubscriptionResult",
    "ModifyGlobalClusterResult",
    "NeptuneCluster",
    "NeptuneClusterSnapshot",
    "NeptuneInstance",
    "PromoteReadReplicaDbClusterResult",
    "RebootDbInstanceResult",
    "RemoveFromGlobalClusterResult",
    "RemoveSourceIdentifierFromSubscriptionResult",
    "ResetDbClusterParameterGroupResult",
    "ResetDbParameterGroupResult",
    "RestoreDbClusterFromSnapshotResult",
    "RestoreDbClusterToPointInTimeResult",
    "StartDbClusterResult",
    "StopDbClusterResult",
    "SwitchoverGlobalClusterResult",
    "add_role_to_db_cluster",
    "add_source_identifier_to_subscription",
    "add_tags_to_resource",
    "apply_pending_maintenance_action",
    "copy_db_cluster_parameter_group",
    "copy_db_cluster_snapshot",
    "copy_db_parameter_group",
    "create_db_cluster",
    "create_db_cluster_endpoint",
    "create_db_cluster_parameter_group",
    "create_db_cluster_snapshot",
    "create_db_instance",
    "create_db_parameter_group",
    "create_db_subnet_group",
    "create_event_subscription",
    "create_global_cluster",
    "delete_db_cluster",
    "delete_db_cluster_endpoint",
    "delete_db_cluster_parameter_group",
    "delete_db_cluster_snapshot",
    "delete_db_instance",
    "delete_db_parameter_group",
    "delete_db_subnet_group",
    "delete_event_subscription",
    "delete_global_cluster",
    "describe_db_cluster_endpoints",
    "describe_db_cluster_parameter_groups",
    "describe_db_cluster_parameters",
    "describe_db_cluster_snapshot_attributes",
    "describe_db_cluster_snapshots",
    "describe_db_clusters",
    "describe_db_engine_versions",
    "describe_db_instances",
    "describe_db_parameter_groups",
    "describe_db_parameters",
    "describe_db_subnet_groups",
    "describe_engine_default_cluster_parameters",
    "describe_engine_default_parameters",
    "describe_event_categories",
    "describe_event_subscriptions",
    "describe_events",
    "describe_global_clusters",
    "describe_orderable_db_instance_options",
    "describe_pending_maintenance_actions",
    "describe_valid_db_instance_modifications",
    "failover_db_cluster",
    "failover_global_cluster",
    "list_tags_for_resource",
    "modify_db_cluster",
    "modify_db_cluster_endpoint",
    "modify_db_cluster_parameter_group",
    "modify_db_cluster_snapshot_attribute",
    "modify_db_instance",
    "modify_db_parameter_group",
    "modify_db_subnet_group",
    "modify_event_subscription",
    "modify_global_cluster",
    "promote_read_replica_db_cluster",
    "reboot_db_instance",
    "remove_from_global_cluster",
    "remove_role_from_db_cluster",
    "remove_source_identifier_from_subscription",
    "remove_tags_from_resource",
    "reset_db_cluster_parameter_group",
    "reset_db_parameter_group",
    "restore_db_cluster_from_snapshot",
    "restore_db_cluster_to_point_in_time",
    "start_db_cluster",
    "stop_db_cluster",
    "switchover_global_cluster",
    "wait_for_db_cluster",
]


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def create_db_cluster(
    db_cluster_identifier: str,
    engine: str = "neptune",
    *,
    engine_version: str | None = None,
    region_name: str | None = None,
    **kwargs: Any,
) -> NeptuneCluster:
    """Create a Neptune DB cluster.

    Args:
        db_cluster_identifier: Unique identifier for the cluster.
        engine: Database engine (default ``"neptune"``).
        engine_version: Engine version string.
        region_name: AWS region override.
        **kwargs: Additional CreateDBCluster parameters.

    Returns:
        The created :class:`NeptuneCluster`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
        "Engine": engine,
        **kwargs,
    }
    if engine_version is not None:
        params["EngineVersion"] = engine_version
    try:
        resp = await client.call("CreateDBCluster", **params)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_db_cluster failed") from exc
    return _parse_cluster(resp["DBCluster"])


async def describe_db_clusters(
    db_cluster_identifier: str | None = None,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[NeptuneCluster]:
    """Describe Neptune DB clusters.

    Args:
        db_cluster_identifier: Filter to a single cluster.
        region_name: AWS region override.
        **kwargs: Additional DescribeDBClusters parameters.

    Returns:
        A list of :class:`NeptuneCluster` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {**kwargs}
    if db_cluster_identifier is not None:
        params["DBClusterIdentifier"] = db_cluster_identifier
    clusters: list[NeptuneCluster] = []
    try:
        token: str | None = None
        while True:
            if token:
                params["Marker"] = token
            resp = await client.call("DescribeDBClusters", **params)
            for c in resp.get("DBClusters", []):
                clusters.append(_parse_cluster(c))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_clusters failed") from exc
    return clusters


async def modify_db_cluster(
    db_cluster_identifier: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> NeptuneCluster:
    """Modify a Neptune DB cluster.

    Args:
        db_cluster_identifier: The cluster to modify.
        region_name: AWS region override.
        **kwargs: Additional ModifyDBCluster parameters.

    Returns:
        The modified :class:`NeptuneCluster`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    try:
        resp = await client.call(
            "ModifyDBCluster",
            DBClusterIdentifier=db_cluster_identifier,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_db_cluster failed") from exc
    return _parse_cluster(resp["DBCluster"])


async def delete_db_cluster(
    db_cluster_identifier: str,
    *,
    skip_final_snapshot: bool = True,
    region_name: str | None = None,
    **kwargs: Any,
) -> None:
    """Delete a Neptune DB cluster.

    Args:
        db_cluster_identifier: The cluster to delete.
        skip_final_snapshot: Skip final snapshot on deletion.
        region_name: AWS region override.
        **kwargs: Additional DeleteDBCluster parameters.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    try:
        await client.call(
            "DeleteDBCluster",
            DBClusterIdentifier=db_cluster_identifier,
            SkipFinalSnapshot=skip_final_snapshot,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_db_cluster failed") from exc


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


async def create_db_instance(
    db_instance_identifier: str,
    db_instance_class: str,
    engine: str = "neptune",
    *,
    db_cluster_identifier: str | None = None,
    region_name: str | None = None,
    **kwargs: Any,
) -> NeptuneInstance:
    """Create a Neptune DB instance.

    Args:
        db_instance_identifier: Unique identifier for the instance.
        db_instance_class: Instance class (e.g. ``"db.r5.large"``).
        engine: Database engine (default ``"neptune"``).
        db_cluster_identifier: Parent cluster.
        region_name: AWS region override.
        **kwargs: Additional CreateDBInstance parameters.

    Returns:
        The created :class:`NeptuneInstance`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {
        "DBInstanceIdentifier": db_instance_identifier,
        "DBInstanceClass": db_instance_class,
        "Engine": engine,
        **kwargs,
    }
    if db_cluster_identifier is not None:
        params["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = await client.call("CreateDBInstance", **params)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_db_instance failed") from exc
    return _parse_instance(resp["DBInstance"])


async def describe_db_instances(
    db_instance_identifier: str | None = None,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[NeptuneInstance]:
    """Describe Neptune DB instances.

    Args:
        db_instance_identifier: Filter to a single instance.
        region_name: AWS region override.
        **kwargs: Additional DescribeDBInstances parameters.

    Returns:
        A list of :class:`NeptuneInstance` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {**kwargs}
    if db_instance_identifier is not None:
        params["DBInstanceIdentifier"] = db_instance_identifier
    instances: list[NeptuneInstance] = []
    try:
        token: str | None = None
        while True:
            if token:
                params["Marker"] = token
            resp = await client.call("DescribeDBInstances", **params)
            for inst in resp.get("DBInstances", []):
                instances.append(_parse_instance(inst))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_instances failed") from exc
    return instances


async def modify_db_instance(
    db_instance_identifier: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> NeptuneInstance:
    """Modify a Neptune DB instance.

    Args:
        db_instance_identifier: The instance to modify.
        region_name: AWS region override.
        **kwargs: Additional ModifyDBInstance parameters.

    Returns:
        The modified :class:`NeptuneInstance`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    try:
        resp = await client.call(
            "ModifyDBInstance",
            DBInstanceIdentifier=db_instance_identifier,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "modify_db_instance failed") from exc
    return _parse_instance(resp["DBInstance"])


async def delete_db_instance(
    db_instance_identifier: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> None:
    """Delete a Neptune DB instance.

    Args:
        db_instance_identifier: The instance to delete.
        region_name: AWS region override.
        **kwargs: Additional DeleteDBInstance parameters.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    try:
        await client.call(
            "DeleteDBInstance",
            DBInstanceIdentifier=db_instance_identifier,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_db_instance failed") from exc


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def create_db_cluster_snapshot(
    db_cluster_snapshot_identifier: str,
    db_cluster_identifier: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> NeptuneClusterSnapshot:
    """Create a Neptune DB cluster snapshot.

    Args:
        db_cluster_snapshot_identifier: Identifier for the snapshot.
        db_cluster_identifier: Source cluster.
        region_name: AWS region override.
        **kwargs: Additional CreateDBClusterSnapshot parameters.

    Returns:
        The created :class:`NeptuneClusterSnapshot`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    try:
        resp = await client.call(
            "CreateDBClusterSnapshot",
            DBClusterSnapshotIdentifier=db_cluster_snapshot_identifier,
            DBClusterIdentifier=db_cluster_identifier,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "create_db_cluster_snapshot failed") from exc
    return _parse_cluster_snapshot(resp["DBClusterSnapshot"])


async def describe_db_cluster_snapshots(
    db_cluster_identifier: str | None = None,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[NeptuneClusterSnapshot]:
    """Describe Neptune DB cluster snapshots.

    Args:
        db_cluster_identifier: Filter to snapshots of a specific cluster.
        region_name: AWS region override.
        **kwargs: Additional DescribeDBClusterSnapshots parameters.

    Returns:
        A list of :class:`NeptuneClusterSnapshot` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {**kwargs}
    if db_cluster_identifier is not None:
        params["DBClusterIdentifier"] = db_cluster_identifier
    snapshots: list[NeptuneClusterSnapshot] = []
    try:
        token: str | None = None
        while True:
            if token:
                params["Marker"] = token
            resp = await client.call("DescribeDBClusterSnapshots", **params)
            for s in resp.get("DBClusterSnapshots", []):
                snapshots.append(_parse_cluster_snapshot(s))
            token = resp.get("Marker")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_db_cluster_snapshots failed") from exc
    return snapshots


# ---------------------------------------------------------------------------
# Failover & polling
# ---------------------------------------------------------------------------


async def failover_db_cluster(
    db_cluster_identifier: str,
    *,
    target_db_instance_identifier: str | None = None,
    region_name: str | None = None,
) -> NeptuneCluster:
    """Initiate a failover for a Neptune DB cluster.

    Args:
        db_cluster_identifier: The cluster to failover.
        target_db_instance_identifier: Optional preferred failover target.
        region_name: AWS region override.

    Returns:
        The :class:`NeptuneCluster` after failover initiation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    params: dict[str, Any] = {
        "DBClusterIdentifier": db_cluster_identifier,
    }
    if target_db_instance_identifier is not None:
        params["TargetDBInstanceIdentifier"] = target_db_instance_identifier
    try:
        resp = await client.call("FailoverDBCluster", **params)
    except Exception as exc:
        raise wrap_aws_error(exc, "failover_db_cluster failed") from exc
    return _parse_cluster(resp["DBCluster"])


async def wait_for_db_cluster(
    db_cluster_identifier: str,
    target_status: str = "available",
    *,
    timeout: float = 1200.0,
    poll_interval: float = 20.0,
    region_name: str | None = None,
) -> NeptuneCluster:
    """Poll until a Neptune DB cluster reaches the desired status.

    Args:
        db_cluster_identifier: The cluster to poll.
        target_status: Desired status (default ``"available"``).
        timeout: Maximum seconds to wait.
        poll_interval: Seconds between polls.
        region_name: AWS region override.

    Returns:
        The :class:`NeptuneCluster` in the target status.

    Raises:
        TimeoutError: If the cluster does not reach the target status in time.
        RuntimeError: If the cluster is not found.
    """
    deadline = time.monotonic() + timeout
    while True:
        clusters = await describe_db_clusters(db_cluster_identifier, region_name=region_name)
        if not clusters:
            raise AwsServiceError(f"Neptune cluster {db_cluster_identifier!r} not found")
        cluster = clusters[0]
        if cluster.status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Neptune cluster {db_cluster_identifier!r} did not reach "
                f"{target_status!r} within {timeout}s "
                f"(current: {cluster.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def add_role_to_db_cluster(
    db_cluster_identifier: str,
    role_arn: str,
    *,
    feature_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Add role to db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        role_arn: Role arn.
        feature_name: Feature name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["RoleArn"] = role_arn
    if feature_name is not None:
        kwargs["FeatureName"] = feature_name
    try:
        await client.call("AddRoleToDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add role to db cluster") from exc
    return None


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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def copy_db_cluster_snapshot(
    source_db_cluster_snapshot_identifier: str,
    target_db_cluster_snapshot_identifier: str,
    *,
    kms_key_id: str | None = None,
    pre_signed_url: str | None = None,
    copy_tags: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    source_region: str | None = None,
    region_name: str | None = None,
) -> CopyDbClusterSnapshotResult:
    """Copy db cluster snapshot.

    Args:
        source_db_cluster_snapshot_identifier: Source db cluster snapshot identifier.
        target_db_cluster_snapshot_identifier: Target db cluster snapshot identifier.
        kms_key_id: Kms key id.
        pre_signed_url: Pre signed url.
        copy_tags: Copy tags.
        tags: Tags.
        source_region: Source region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBClusterSnapshotIdentifier"] = source_db_cluster_snapshot_identifier
    kwargs["TargetDBClusterSnapshotIdentifier"] = target_db_cluster_snapshot_identifier
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if pre_signed_url is not None:
        kwargs["PreSignedUrl"] = pre_signed_url
    if copy_tags is not None:
        kwargs["CopyTags"] = copy_tags
    if tags is not None:
        kwargs["Tags"] = tags
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    try:
        resp = await client.call("CopyDBClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy db cluster snapshot") from exc
    return CopyDbClusterSnapshotResult(
        db_cluster_snapshot=resp.get("DBClusterSnapshot"),
    )


async def copy_db_parameter_group(
    source_db_parameter_group_identifier: str,
    target_db_parameter_group_identifier: str,
    target_db_parameter_group_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CopyDbParameterGroupResult:
    """Copy db parameter group.

    Args:
        source_db_parameter_group_identifier: Source db parameter group identifier.
        target_db_parameter_group_identifier: Target db parameter group identifier.
        target_db_parameter_group_description: Target db parameter group description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBParameterGroupIdentifier"] = source_db_parameter_group_identifier
    kwargs["TargetDBParameterGroupIdentifier"] = target_db_parameter_group_identifier
    kwargs["TargetDBParameterGroupDescription"] = target_db_parameter_group_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CopyDBParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy db parameter group") from exc
    return CopyDbParameterGroupResult(
        db_parameter_group=resp.get("DBParameterGroup"),
    )


async def create_db_cluster_endpoint(
    db_cluster_identifier: str,
    db_cluster_endpoint_identifier: str,
    endpoint_type: str,
    *,
    static_members: list[str] | None = None,
    excluded_members: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbClusterEndpointResult:
    """Create db cluster endpoint.

    Args:
        db_cluster_identifier: Db cluster identifier.
        db_cluster_endpoint_identifier: Db cluster endpoint identifier.
        endpoint_type: Endpoint type.
        static_members: Static members.
        excluded_members: Excluded members.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    kwargs["EndpointType"] = endpoint_type
    if static_members is not None:
        kwargs["StaticMembers"] = static_members
    if excluded_members is not None:
        kwargs["ExcludedMembers"] = excluded_members
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDBClusterEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create db cluster endpoint") from exc
    return CreateDbClusterEndpointResult(
        db_cluster_endpoint_identifier=resp.get("DBClusterEndpointIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        db_cluster_endpoint_resource_identifier=resp.get("DBClusterEndpointResourceIdentifier"),
        endpoint=resp.get("Endpoint"),
        status=resp.get("Status"),
        endpoint_type=resp.get("EndpointType"),
        custom_endpoint_type=resp.get("CustomEndpointType"),
        static_members=resp.get("StaticMembers"),
        excluded_members=resp.get("ExcludedMembers"),
        db_cluster_endpoint_arn=resp.get("DBClusterEndpointArn"),
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
    client = async_client("neptune", region_name)
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


async def create_db_parameter_group(
    db_parameter_group_name: str,
    db_parameter_group_family: str,
    description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbParameterGroupResult:
    """Create db parameter group.

    Args:
        db_parameter_group_name: Db parameter group name.
        db_parameter_group_family: Db parameter group family.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDBParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create db parameter group") from exc
    return CreateDbParameterGroupResult(
        db_parameter_group=resp.get("DBParameterGroup"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
        storage_encrypted: Storage encrypted.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
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
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    try:
        resp = await client.call("CreateGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create global cluster") from exc
    return CreateGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def delete_db_cluster_endpoint(
    db_cluster_endpoint_identifier: str,
    region_name: str | None = None,
) -> DeleteDbClusterEndpointResult:
    """Delete db cluster endpoint.

    Args:
        db_cluster_endpoint_identifier: Db cluster endpoint identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    try:
        resp = await client.call("DeleteDBClusterEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster endpoint") from exc
    return DeleteDbClusterEndpointResult(
        db_cluster_endpoint_identifier=resp.get("DBClusterEndpointIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        db_cluster_endpoint_resource_identifier=resp.get("DBClusterEndpointResourceIdentifier"),
        endpoint=resp.get("Endpoint"),
        status=resp.get("Status"),
        endpoint_type=resp.get("EndpointType"),
        custom_endpoint_type=resp.get("CustomEndpointType"),
        static_members=resp.get("StaticMembers"),
        excluded_members=resp.get("ExcludedMembers"),
        db_cluster_endpoint_arn=resp.get("DBClusterEndpointArn"),
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
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    try:
        await client.call("DeleteDBClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster parameter group") from exc
    return None


async def delete_db_cluster_snapshot(
    db_cluster_snapshot_identifier: str,
    region_name: str | None = None,
) -> DeleteDbClusterSnapshotResult:
    """Delete db cluster snapshot.

    Args:
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    try:
        resp = await client.call("DeleteDBClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster snapshot") from exc
    return DeleteDbClusterSnapshotResult(
        db_cluster_snapshot=resp.get("DBClusterSnapshot"),
    )


async def delete_db_parameter_group(
    db_parameter_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete db parameter group.

    Args:
        db_parameter_group_name: Db parameter group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    try:
        await client.call("DeleteDBParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete db parameter group") from exc
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    try:
        resp = await client.call("DeleteGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete global cluster") from exc
    return DeleteGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def describe_db_cluster_endpoints(
    *,
    db_cluster_identifier: str | None = None,
    db_cluster_endpoint_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterEndpointsResult:
    """Describe db cluster endpoints.

    Args:
        db_cluster_identifier: Db cluster identifier.
        db_cluster_endpoint_identifier: Db cluster endpoint identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if db_cluster_endpoint_identifier is not None:
        kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBClusterEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster endpoints") from exc
    return DescribeDbClusterEndpointsResult(
        marker=resp.get("Marker"),
        db_cluster_endpoints=resp.get("DBClusterEndpoints"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def describe_db_parameter_groups(
    *,
    db_parameter_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbParameterGroupsResult:
    """Describe db parameter groups.

    Args:
        db_parameter_group_name: Db parameter group name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBParameterGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db parameter groups") from exc
    return DescribeDbParameterGroupsResult(
        marker=resp.get("Marker"),
        db_parameter_groups=resp.get("DBParameterGroups"),
    )


async def describe_db_parameters(
    db_parameter_group_name: str,
    *,
    source: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbParametersResult:
    """Describe db parameters.

    Args:
        db_parameter_group_name: Db parameter group name.
        source: Source.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    if source is not None:
        kwargs["Source"] = source
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDBParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe db parameters") from exc
    return DescribeDbParametersResult(
        parameters=resp.get("Parameters"),
        marker=resp.get("Marker"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def describe_engine_default_parameters(
    db_parameter_group_family: str,
    *,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEngineDefaultParametersResult:
    """Describe engine default parameters.

    Args:
        db_parameter_group_family: Db parameter group family.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEngineDefaultParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe engine default parameters") from exc
    return DescribeEngineDefaultParametersResult(
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeGlobalClustersResult:
    """Describe global clusters.

    Args:
        global_cluster_identifier: Global cluster identifier.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    if global_cluster_identifier is not None:
        kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def describe_valid_db_instance_modifications(
    db_instance_identifier: str,
    region_name: str | None = None,
) -> DescribeValidDbInstanceModificationsResult:
    """Describe valid db instance modifications.

    Args:
        db_instance_identifier: Db instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    try:
        resp = await client.call("DescribeValidDBInstanceModifications", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe valid db instance modifications") from exc
    return DescribeValidDbInstanceModificationsResult(
        valid_db_instance_modifications_message=resp.get("ValidDBInstanceModificationsMessage"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def modify_db_cluster_endpoint(
    db_cluster_endpoint_identifier: str,
    *,
    endpoint_type: str | None = None,
    static_members: list[str] | None = None,
    excluded_members: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyDbClusterEndpointResult:
    """Modify db cluster endpoint.

    Args:
        db_cluster_endpoint_identifier: Db cluster endpoint identifier.
        endpoint_type: Endpoint type.
        static_members: Static members.
        excluded_members: Excluded members.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    if endpoint_type is not None:
        kwargs["EndpointType"] = endpoint_type
    if static_members is not None:
        kwargs["StaticMembers"] = static_members
    if excluded_members is not None:
        kwargs["ExcludedMembers"] = excluded_members
    try:
        resp = await client.call("ModifyDBClusterEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster endpoint") from exc
    return ModifyDbClusterEndpointResult(
        db_cluster_endpoint_identifier=resp.get("DBClusterEndpointIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        db_cluster_endpoint_resource_identifier=resp.get("DBClusterEndpointResourceIdentifier"),
        endpoint=resp.get("Endpoint"),
        status=resp.get("Status"),
        endpoint_type=resp.get("EndpointType"),
        custom_endpoint_type=resp.get("CustomEndpointType"),
        static_members=resp.get("StaticMembers"),
        excluded_members=resp.get("ExcludedMembers"),
        db_cluster_endpoint_arn=resp.get("DBClusterEndpointArn"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def modify_db_parameter_group(
    db_parameter_group_name: str,
    parameters: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyDbParameterGroupResult:
    """Modify db parameter group.

    Args:
        db_parameter_group_name: Db parameter group name.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ModifyDBParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify db parameter group") from exc
    return ModifyDbParameterGroupResult(
        db_parameter_group_name=resp.get("DBParameterGroupName"),
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    engine_version: str | None = None,
    allow_major_version_upgrade: bool | None = None,
    region_name: str | None = None,
) -> ModifyGlobalClusterResult:
    """Modify global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        new_global_cluster_identifier: New global cluster identifier.
        deletion_protection: Deletion protection.
        engine_version: Engine version.
        allow_major_version_upgrade: Allow major version upgrade.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if new_global_cluster_identifier is not None:
        kwargs["NewGlobalClusterIdentifier"] = new_global_cluster_identifier
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if allow_major_version_upgrade is not None:
        kwargs["AllowMajorVersionUpgrade"] = allow_major_version_upgrade
    try:
        resp = await client.call("ModifyGlobalCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify global cluster") from exc
    return ModifyGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


async def promote_read_replica_db_cluster(
    db_cluster_identifier: str,
    region_name: str | None = None,
) -> PromoteReadReplicaDbClusterResult:
    """Promote read replica db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = await client.call("PromoteReadReplicaDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to promote read replica db cluster") from exc
    return PromoteReadReplicaDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


async def reboot_db_instance(
    db_instance_identifier: str,
    *,
    force_failover: bool | None = None,
    region_name: str | None = None,
) -> RebootDbInstanceResult:
    """Reboot db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        force_failover: Force failover.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if force_failover is not None:
        kwargs["ForceFailover"] = force_failover
    try:
        resp = await client.call("RebootDBInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reboot db instance") from exc
    return RebootDbInstanceResult(
        db_instance=resp.get("DBInstance"),
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
    client = async_client("neptune", region_name)
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


async def remove_role_from_db_cluster(
    db_cluster_identifier: str,
    role_arn: str,
    *,
    feature_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove role from db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        role_arn: Role arn.
        feature_name: Feature name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["RoleArn"] = role_arn
    if feature_name is not None:
        kwargs["FeatureName"] = feature_name
    try:
        await client.call("RemoveRoleFromDBCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove role from db cluster") from exc
    return None


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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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


async def reset_db_parameter_group(
    db_parameter_group_name: str,
    *,
    reset_all_parameters: bool | None = None,
    parameters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ResetDbParameterGroupResult:
    """Reset db parameter group.

    Args:
        db_parameter_group_name: Db parameter group name.
        reset_all_parameters: Reset all parameters.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ResetDBParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset db parameter group") from exc
    return ResetDbParameterGroupResult(
        db_parameter_group_name=resp.get("DBParameterGroupName"),
    )


async def restore_db_cluster_from_snapshot(
    db_cluster_identifier: str,
    snapshot_identifier: str,
    engine: str,
    *,
    availability_zones: list[str] | None = None,
    engine_version: str | None = None,
    port: int | None = None,
    db_subnet_group_name: str | None = None,
    database_name: str | None = None,
    option_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    kms_key_id: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    db_cluster_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    storage_type: str | None = None,
    region_name: str | None = None,
) -> RestoreDbClusterFromSnapshotResult:
    """Restore db cluster from snapshot.

    Args:
        db_cluster_identifier: Db cluster identifier.
        snapshot_identifier: Snapshot identifier.
        engine: Engine.
        availability_zones: Availability zones.
        engine_version: Engine version.
        port: Port.
        db_subnet_group_name: Db subnet group name.
        database_name: Database name.
        option_group_name: Option group name.
        vpc_security_group_ids: Vpc security group ids.
        tags: Tags.
        kms_key_id: Kms key id.
        enable_iam_database_authentication: Enable iam database authentication.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        deletion_protection: Deletion protection.
        copy_tags_to_snapshot: Copy tags to snapshot.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        storage_type: Storage type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["SnapshotIdentifier"] = snapshot_identifier
    kwargs["Engine"] = engine
    if availability_zones is not None:
        kwargs["AvailabilityZones"] = availability_zones
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if port is not None:
        kwargs["Port"] = port
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if tags is not None:
        kwargs["Tags"] = tags
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    try:
        resp = await client.call("RestoreDBClusterFromSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore db cluster from snapshot") from exc
    return RestoreDbClusterFromSnapshotResult(
        db_cluster=resp.get("DBCluster"),
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
    option_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    kms_key_id: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    db_cluster_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    storage_type: str | None = None,
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
        option_group_name: Option group name.
        vpc_security_group_ids: Vpc security group ids.
        tags: Tags.
        kms_key_id: Kms key id.
        enable_iam_database_authentication: Enable iam database authentication.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        deletion_protection: Deletion protection.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        storage_type: Storage type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("neptune", region_name)
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
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if tags is not None:
        kwargs["Tags"] = tags
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
    client = async_client("neptune", region_name)
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
