from __future__ import annotations

from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "AddSourceIdentifierToSubscriptionResult",
    "ApplyPendingMaintenanceActionResult",
    "AuthorizeDbSecurityGroupIngressResult",
    "BacktrackDbClusterResult",
    "CancelExportTaskResult",
    "CopyDbClusterParameterGroupResult",
    "CopyDbClusterSnapshotResult",
    "CopyDbParameterGroupResult",
    "CopyDbSnapshotResult",
    "CopyOptionGroupResult",
    "CreateBlueGreenDeploymentResult",
    "CreateCustomDbEngineVersionResult",
    "CreateDbClusterEndpointResult",
    "CreateDbClusterParameterGroupResult",
    "CreateDbClusterResult",
    "CreateDbClusterSnapshotResult",
    "CreateDbInstanceReadReplicaResult",
    "CreateDbInstanceResult",
    "CreateDbParameterGroupResult",
    "CreateDbProxyEndpointResult",
    "CreateDbProxyResult",
    "CreateDbSecurityGroupResult",
    "CreateDbShardGroupResult",
    "CreateDbSubnetGroupResult",
    "CreateEventSubscriptionResult",
    "CreateGlobalClusterResult",
    "CreateIntegrationResult",
    "CreateOptionGroupResult",
    "CreateTenantDatabaseResult",
    "DeleteBlueGreenDeploymentResult",
    "DeleteCustomDbEngineVersionResult",
    "DeleteDbClusterAutomatedBackupResult",
    "DeleteDbClusterEndpointResult",
    "DeleteDbClusterResult",
    "DeleteDbClusterSnapshotResult",
    "DeleteDbInstanceAutomatedBackupResult",
    "DeleteDbInstanceResult",
    "DeleteDbProxyEndpointResult",
    "DeleteDbProxyResult",
    "DeleteDbShardGroupResult",
    "DeleteEventSubscriptionResult",
    "DeleteGlobalClusterResult",
    "DeleteIntegrationResult",
    "DeleteTenantDatabaseResult",
    "DescribeAccountAttributesResult",
    "DescribeBlueGreenDeploymentsResult",
    "DescribeCertificatesResult",
    "DescribeDbClusterAutomatedBackupsResult",
    "DescribeDbClusterBacktracksResult",
    "DescribeDbClusterEndpointsResult",
    "DescribeDbClusterParameterGroupsResult",
    "DescribeDbClusterParametersResult",
    "DescribeDbClusterSnapshotAttributesResult",
    "DescribeDbClusterSnapshotsResult",
    "DescribeDbClustersResult",
    "DescribeDbEngineVersionsResult",
    "DescribeDbInstanceAutomatedBackupsResult",
    "DescribeDbLogFilesResult",
    "DescribeDbMajorEngineVersionsResult",
    "DescribeDbParameterGroupsResult",
    "DescribeDbParametersResult",
    "DescribeDbProxiesResult",
    "DescribeDbProxyEndpointsResult",
    "DescribeDbProxyTargetGroupsResult",
    "DescribeDbProxyTargetsResult",
    "DescribeDbRecommendationsResult",
    "DescribeDbSecurityGroupsResult",
    "DescribeDbShardGroupsResult",
    "DescribeDbSnapshotAttributesResult",
    "DescribeDbSnapshotTenantDatabasesResult",
    "DescribeDbSubnetGroupsResult",
    "DescribeEngineDefaultClusterParametersResult",
    "DescribeEngineDefaultParametersResult",
    "DescribeEventCategoriesResult",
    "DescribeEventSubscriptionsResult",
    "DescribeEventsResult",
    "DescribeExportTasksResult",
    "DescribeGlobalClustersResult",
    "DescribeIntegrationsResult",
    "DescribeOptionGroupOptionsResult",
    "DescribeOptionGroupsResult",
    "DescribeOrderableDbInstanceOptionsResult",
    "DescribePendingMaintenanceActionsResult",
    "DescribeReservedDbInstancesOfferingsResult",
    "DescribeReservedDbInstancesResult",
    "DescribeSourceRegionsResult",
    "DescribeTenantDatabasesResult",
    "DescribeValidDbInstanceModificationsResult",
    "DisableHttpEndpointResult",
    "DownloadDbLogFilePortionResult",
    "EnableHttpEndpointResult",
    "FailoverDbClusterResult",
    "FailoverGlobalClusterResult",
    "ListTagsForResourceResult",
    "ModifyActivityStreamResult",
    "ModifyCertificatesResult",
    "ModifyCurrentDbClusterCapacityResult",
    "ModifyCustomDbEngineVersionResult",
    "ModifyDbClusterEndpointResult",
    "ModifyDbClusterParameterGroupResult",
    "ModifyDbClusterResult",
    "ModifyDbClusterSnapshotAttributeResult",
    "ModifyDbInstanceResult",
    "ModifyDbParameterGroupResult",
    "ModifyDbProxyEndpointResult",
    "ModifyDbProxyResult",
    "ModifyDbProxyTargetGroupResult",
    "ModifyDbRecommendationResult",
    "ModifyDbShardGroupResult",
    "ModifyDbSnapshotAttributeResult",
    "ModifyDbSnapshotResult",
    "ModifyDbSubnetGroupResult",
    "ModifyEventSubscriptionResult",
    "ModifyGlobalClusterResult",
    "ModifyIntegrationResult",
    "ModifyOptionGroupResult",
    "ModifyTenantDatabaseResult",
    "PromoteReadReplicaDbClusterResult",
    "PromoteReadReplicaResult",
    "PurchaseReservedDbInstancesOfferingResult",
    "RDSInstance",
    "RDSSnapshot",
    "RebootDbClusterResult",
    "RebootDbInstanceResult",
    "RebootDbShardGroupResult",
    "RegisterDbProxyTargetsResult",
    "RemoveFromGlobalClusterResult",
    "RemoveSourceIdentifierFromSubscriptionResult",
    "ResetDbClusterParameterGroupResult",
    "ResetDbParameterGroupResult",
    "RestoreDbClusterFromS3Result",
    "RestoreDbClusterFromSnapshotResult",
    "RestoreDbClusterToPointInTimeResult",
    "RestoreDbInstanceFromDbSnapshotResult",
    "RestoreDbInstanceFromS3Result",
    "RestoreDbInstanceToPointInTimeResult",
    "RevokeDbSecurityGroupIngressResult",
    "StartActivityStreamResult",
    "StartDbClusterResult",
    "StartDbInstanceAutomatedBackupsReplicationResult",
    "StartExportTaskResult",
    "StopActivityStreamResult",
    "StopDbClusterResult",
    "StopDbInstanceAutomatedBackupsReplicationResult",
    "SwitchoverBlueGreenDeploymentResult",
    "SwitchoverGlobalClusterResult",
    "SwitchoverReadReplicaResult",
    "add_role_to_db_cluster",
    "add_role_to_db_instance",
    "add_source_identifier_to_subscription",
    "add_tags_to_resource",
    "apply_pending_maintenance_action",
    "authorize_db_security_group_ingress",
    "backtrack_db_cluster",
    "cancel_export_task",
    "copy_db_cluster_parameter_group",
    "copy_db_cluster_snapshot",
    "copy_db_parameter_group",
    "copy_db_snapshot",
    "copy_option_group",
    "create_blue_green_deployment",
    "create_custom_db_engine_version",
    "create_db_cluster",
    "create_db_cluster_endpoint",
    "create_db_cluster_parameter_group",
    "create_db_cluster_snapshot",
    "create_db_instance",
    "create_db_instance_read_replica",
    "create_db_parameter_group",
    "create_db_proxy",
    "create_db_proxy_endpoint",
    "create_db_security_group",
    "create_db_shard_group",
    "create_db_snapshot",
    "create_db_subnet_group",
    "create_event_subscription",
    "create_global_cluster",
    "create_integration",
    "create_option_group",
    "create_tenant_database",
    "delete_blue_green_deployment",
    "delete_custom_db_engine_version",
    "delete_db_cluster",
    "delete_db_cluster_automated_backup",
    "delete_db_cluster_endpoint",
    "delete_db_cluster_parameter_group",
    "delete_db_cluster_snapshot",
    "delete_db_instance",
    "delete_db_instance_automated_backup",
    "delete_db_parameter_group",
    "delete_db_proxy",
    "delete_db_proxy_endpoint",
    "delete_db_security_group",
    "delete_db_shard_group",
    "delete_db_snapshot",
    "delete_db_subnet_group",
    "delete_event_subscription",
    "delete_global_cluster",
    "delete_integration",
    "delete_option_group",
    "delete_tenant_database",
    "deregister_db_proxy_targets",
    "describe_account_attributes",
    "describe_blue_green_deployments",
    "describe_certificates",
    "describe_db_cluster_automated_backups",
    "describe_db_cluster_backtracks",
    "describe_db_cluster_endpoints",
    "describe_db_cluster_parameter_groups",
    "describe_db_cluster_parameters",
    "describe_db_cluster_snapshot_attributes",
    "describe_db_cluster_snapshots",
    "describe_db_clusters",
    "describe_db_engine_versions",
    "describe_db_instance_automated_backups",
    "describe_db_instances",
    "describe_db_log_files",
    "describe_db_major_engine_versions",
    "describe_db_parameter_groups",
    "describe_db_parameters",
    "describe_db_proxies",
    "describe_db_proxy_endpoints",
    "describe_db_proxy_target_groups",
    "describe_db_proxy_targets",
    "describe_db_recommendations",
    "describe_db_security_groups",
    "describe_db_shard_groups",
    "describe_db_snapshot_attributes",
    "describe_db_snapshot_tenant_databases",
    "describe_db_snapshots",
    "describe_db_subnet_groups",
    "describe_engine_default_cluster_parameters",
    "describe_engine_default_parameters",
    "describe_event_categories",
    "describe_event_subscriptions",
    "describe_events",
    "describe_export_tasks",
    "describe_global_clusters",
    "describe_integrations",
    "describe_option_group_options",
    "describe_option_groups",
    "describe_orderable_db_instance_options",
    "describe_pending_maintenance_actions",
    "describe_reserved_db_instances",
    "describe_reserved_db_instances_offerings",
    "describe_source_regions",
    "describe_tenant_databases",
    "describe_valid_db_instance_modifications",
    "disable_http_endpoint",
    "download_db_log_file_portion",
    "enable_http_endpoint",
    "failover_db_cluster",
    "failover_global_cluster",
    "get_db_instance",
    "list_tags_for_resource",
    "modify_activity_stream",
    "modify_certificates",
    "modify_current_db_cluster_capacity",
    "modify_custom_db_engine_version",
    "modify_db_cluster",
    "modify_db_cluster_endpoint",
    "modify_db_cluster_parameter_group",
    "modify_db_cluster_snapshot_attribute",
    "modify_db_instance",
    "modify_db_parameter_group",
    "modify_db_proxy",
    "modify_db_proxy_endpoint",
    "modify_db_proxy_target_group",
    "modify_db_recommendation",
    "modify_db_shard_group",
    "modify_db_snapshot",
    "modify_db_snapshot_attribute",
    "modify_db_subnet_group",
    "modify_event_subscription",
    "modify_global_cluster",
    "modify_integration",
    "modify_option_group",
    "modify_tenant_database",
    "promote_read_replica",
    "promote_read_replica_db_cluster",
    "purchase_reserved_db_instances_offering",
    "reboot_db_cluster",
    "reboot_db_instance",
    "reboot_db_shard_group",
    "register_db_proxy_targets",
    "remove_from_global_cluster",
    "remove_role_from_db_cluster",
    "remove_role_from_db_instance",
    "remove_source_identifier_from_subscription",
    "remove_tags_from_resource",
    "reset_db_cluster_parameter_group",
    "reset_db_parameter_group",
    "restore_db_cluster_from_s3",
    "restore_db_cluster_from_snapshot",
    "restore_db_cluster_to_point_in_time",
    "restore_db_from_snapshot",
    "restore_db_instance_from_db_snapshot",
    "restore_db_instance_from_s3",
    "restore_db_instance_to_point_in_time",
    "revoke_db_security_group_ingress",
    "start_activity_stream",
    "start_db_cluster",
    "start_db_instance",
    "start_db_instance_automated_backups_replication",
    "start_export_task",
    "stop_activity_stream",
    "stop_db_cluster",
    "stop_db_instance",
    "stop_db_instance_automated_backups_replication",
    "switchover_blue_green_deployment",
    "switchover_global_cluster",
    "switchover_read_replica",
    "wait_for_db_instance",
    "wait_for_snapshot",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class RDSInstance(BaseModel):
    """Metadata for an RDS DB instance."""

    model_config = ConfigDict(frozen=True)

    db_instance_id: str
    db_instance_class: str
    engine: str
    engine_version: str
    status: str
    endpoint_address: str | None = None
    endpoint_port: int | None = None
    multi_az: bool = False
    storage_gb: int | None = None
    tags: dict[str, str] = {}


class RDSSnapshot(BaseModel):
    """Metadata for an RDS DB snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_id: str
    db_instance_id: str
    status: str
    snapshot_type: str
    engine: str
    allocated_storage: int | None = None
    create_time: datetime | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def describe_db_instances(
    db_instance_ids: list[str] | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> list[RDSInstance]:
    """Describe one or more RDS DB instances.

    Args:
        db_instance_ids: Specific instance IDs.  ``None`` returns all
            instances visible to the caller.
        filters: boto3-style filter list.
        region_name: AWS region override.

    Returns:
        A list of :class:`RDSInstance` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters

    instances: list[RDSInstance] = []
    try:
        paginator = client.get_paginator("describe_db_instances")
        page_kwargs: dict[str, Any] = dict(kwargs)
        if db_instance_ids:
            # Paginator does not accept multiple IDs natively; iterate
            for db_id in db_instance_ids:
                page_kwargs["DBInstanceIdentifier"] = db_id
                for page in paginator.paginate(**page_kwargs):
                    instances.extend(_parse_instances(page))
        else:
            for page in paginator.paginate(**page_kwargs):
                instances.extend(_parse_instances(page))
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_db_instances failed") from exc
    return instances


def _parse_instances(page: dict) -> list[RDSInstance]:
    result = []
    for db in page.get("DBInstances", []):
        endpoint = db.get("Endpoint", {})
        tags = {t["Key"]: t["Value"] for t in db.get("TagList", [])}
        result.append(
            RDSInstance(
                db_instance_id=db["DBInstanceIdentifier"],
                db_instance_class=db["DBInstanceClass"],
                engine=db["Engine"],
                engine_version=db["EngineVersion"],
                status=db["DBInstanceStatus"],
                endpoint_address=endpoint.get("Address"),
                endpoint_port=endpoint.get("Port"),
                multi_az=db.get("MultiAZ", False),
                storage_gb=db.get("AllocatedStorage"),
                tags=tags,
            )
        )
    return result


def get_db_instance(
    db_instance_id: str,
    region_name: str | None = None,
) -> RDSInstance | None:
    """Fetch a single RDS instance by identifier.

    Returns:
        An :class:`RDSInstance`, or ``None`` if not found.
    """
    results = describe_db_instances([db_instance_id], region_name=region_name)
    return results[0] if results else None


def start_db_instance(
    db_instance_id: str,
    region_name: str | None = None,
) -> None:
    """Start a stopped RDS DB instance.

    Args:
        db_instance_id: The DB instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the start request fails.
    """
    client = get_client("rds", region_name)
    try:
        client.start_db_instance(DBInstanceIdentifier=db_instance_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start RDS instance {db_instance_id!r}") from exc


def stop_db_instance(
    db_instance_id: str,
    region_name: str | None = None,
) -> None:
    """Stop a running RDS DB instance.

    Stopped instances are not billed for compute but still incur storage costs.

    Args:
        db_instance_id: The DB instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the stop request fails.
    """
    client = get_client("rds", region_name)
    try:
        client.stop_db_instance(DBInstanceIdentifier=db_instance_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to stop RDS instance {db_instance_id!r}") from exc


def create_db_snapshot(
    db_instance_id: str,
    snapshot_id: str,
    region_name: str | None = None,
) -> RDSSnapshot:
    """Create a manual snapshot of an RDS DB instance.

    Args:
        db_instance_id: Source DB instance identifier.
        snapshot_id: Identifier for the new snapshot.
        region_name: AWS region override.

    Returns:
        The newly created :class:`RDSSnapshot`.

    Raises:
        RuntimeError: If snapshot creation fails.
    """
    client = get_client("rds", region_name)
    try:
        resp = client.create_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create snapshot for {db_instance_id!r}") from exc
    snap = resp["DBSnapshot"]
    return RDSSnapshot(
        snapshot_id=snap["DBSnapshotIdentifier"],
        db_instance_id=snap["DBInstanceIdentifier"],
        status=snap["Status"],
        snapshot_type=snap["SnapshotType"],
        engine=snap["Engine"],
        allocated_storage=snap.get("AllocatedStorage"),
        create_time=snap.get("SnapshotCreateTime"),
    )


def delete_db_snapshot(
    snapshot_id: str,
    region_name: str | None = None,
) -> None:
    """Delete a manual RDS DB snapshot.

    Args:
        snapshot_id: The snapshot identifier to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = get_client("rds", region_name)
    try:
        client.delete_db_snapshot(DBSnapshotIdentifier=snapshot_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete snapshot {snapshot_id!r}") from exc


def describe_db_snapshots(
    db_instance_id: str | None = None,
    snapshot_type: str = "manual",
    region_name: str | None = None,
) -> list[RDSSnapshot]:
    """List RDS DB snapshots, optionally filtered by instance and type.

    Args:
        db_instance_id: Filter to snapshots of a specific DB instance.
        snapshot_type: ``"manual"`` (default), ``"automated"``, or ``"shared"``.
        region_name: AWS region override.

    Returns:
        A list of :class:`RDSSnapshot` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {"SnapshotType": snapshot_type}
    if db_instance_id:
        kwargs["DBInstanceIdentifier"] = db_instance_id

    snapshots: list[RDSSnapshot] = []
    try:
        paginator = client.get_paginator("describe_db_snapshots")
        for page in paginator.paginate(**kwargs):
            for snap in page.get("DBSnapshots", []):
                snapshots.append(
                    RDSSnapshot(
                        snapshot_id=snap["DBSnapshotIdentifier"],
                        db_instance_id=snap["DBInstanceIdentifier"],
                        status=snap["Status"],
                        snapshot_type=snap["SnapshotType"],
                        engine=snap["Engine"],
                        allocated_storage=snap.get("AllocatedStorage"),
                        create_time=snap.get("SnapshotCreateTime"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_db_snapshots failed") from exc
    return snapshots


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def wait_for_db_instance(
    db_instance_id: str,
    target_status: str = "available",
    timeout: float = 1200.0,
    poll_interval: float = 20.0,
    region_name: str | None = None,
) -> RDSInstance:
    """Poll until an RDS DB instance reaches the desired status.

    Args:
        db_instance_id: The DB instance identifier.
        target_status: Target status to wait for (default ``"available"``).
            Other common values: ``"stopped"``, ``"backing-up"``,
            ``"deleting"``.
        timeout: Maximum seconds to wait (default ``1200`` / 20 min).
        poll_interval: Seconds between status checks (default ``20``).
        region_name: AWS region override.

    Returns:
        The :class:`RDSInstance` in the target status.

    Raises:
        TimeoutError: If the instance does not reach *target_status* in time.
        RuntimeError: If the instance is not found.
    """
    import time as _time

    deadline = _time.monotonic() + timeout
    while True:
        instance = get_db_instance(db_instance_id, region_name=region_name)
        if instance is None:
            raise AwsServiceError(f"DB instance {db_instance_id!r} not found")
        if instance.status == target_status:
            return instance
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"DB instance {db_instance_id!r} did not reach status "
                f"{target_status!r} within {timeout}s (current: {instance.status!r})"
            )
        _time.sleep(poll_interval)


def wait_for_snapshot(
    snapshot_id: str,
    target_status: str = "available",
    timeout: float = 1800.0,
    poll_interval: float = 30.0,
    region_name: str | None = None,
) -> RDSSnapshot:
    """Poll until an RDS snapshot reaches the desired status.

    Args:
        snapshot_id: The snapshot identifier.
        target_status: Target status (default ``"available"``).
        timeout: Maximum seconds to wait (default ``1800`` / 30 min).
        poll_interval: Seconds between checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`RDSSnapshot` in the target status.

    Raises:
        TimeoutError: If the snapshot does not become available in time.
        RuntimeError: If the snapshot is not found.
    """
    import time as _time

    deadline = _time.monotonic() + timeout
    while True:
        client = get_client("rds", region_name)
        try:
            resp = client.describe_db_snapshots(DBSnapshotIdentifier=snapshot_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"describe snapshot {snapshot_id!r} failed") from exc
        snaps = resp.get("DBSnapshots", [])
        if not snaps:
            raise AwsServiceError(f"Snapshot {snapshot_id!r} not found")
        snap = snaps[0]
        if snap["Status"] == target_status:
            return RDSSnapshot(
                snapshot_id=snap["DBSnapshotIdentifier"],
                db_instance_id=snap["DBInstanceIdentifier"],
                status=snap["Status"],
                snapshot_type=snap["SnapshotType"],
                engine=snap["Engine"],
                allocated_storage=snap.get("AllocatedStorage"),
                create_time=snap.get("SnapshotCreateTime"),
            )
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Snapshot {snapshot_id!r} did not reach status {target_status!r} within {timeout}s"
            )
        _time.sleep(poll_interval)


def restore_db_from_snapshot(
    snapshot_id: str,
    db_instance_id: str,
    db_instance_class: str,
    multi_az: bool = False,
    publicly_accessible: bool = False,
    region_name: str | None = None,
) -> RDSInstance:
    """Restore an RDS DB instance from a snapshot.

    Args:
        snapshot_id: Identifier of the source snapshot.
        db_instance_id: Identifier for the new DB instance.
        db_instance_class: Instance class for the restored DB (e.g.
            ``"db.t3.medium"``).
        multi_az: Enable Multi-AZ deployment.
        publicly_accessible: Make the instance publicly accessible.
        region_name: AWS region override.

    Returns:
        The newly created :class:`RDSInstance` (status will be
        ``"creating"`` initially — call :func:`wait_for_db_instance` to
        wait for ``"available"``).

    Raises:
        RuntimeError: If the restore fails.
    """
    client = get_client("rds", region_name)
    try:
        resp = client.restore_db_instance_from_db_snapshot(
            DBSnapshotIdentifier=snapshot_id,
            DBInstanceIdentifier=db_instance_id,
            DBInstanceClass=db_instance_class,
            MultiAZ=multi_az,
            PubliclyAccessible=publicly_accessible,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "restore_db_from_snapshot failed") from exc
    db = resp["DBInstance"]
    return RDSInstance(
        db_instance_id=db["DBInstanceIdentifier"],
        db_instance_class=db["DBInstanceClass"],
        engine=db["Engine"],
        engine_version=db["EngineVersion"],
        status=db["DBInstanceStatus"],
        multi_az=db.get("MultiAZ", False),
        storage_gb=db.get("AllocatedStorage"),
    )


class AddSourceIdentifierToSubscriptionResult(BaseModel):
    """Result of add_source_identifier_to_subscription."""

    model_config = ConfigDict(frozen=True)

    event_subscription: dict[str, Any] | None = None


class ApplyPendingMaintenanceActionResult(BaseModel):
    """Result of apply_pending_maintenance_action."""

    model_config = ConfigDict(frozen=True)

    resource_pending_maintenance_actions: dict[str, Any] | None = None


class AuthorizeDbSecurityGroupIngressResult(BaseModel):
    """Result of authorize_db_security_group_ingress."""

    model_config = ConfigDict(frozen=True)

    db_security_group: dict[str, Any] | None = None


class BacktrackDbClusterResult(BaseModel):
    """Result of backtrack_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster_identifier: str | None = None
    backtrack_identifier: str | None = None
    backtrack_to: str | None = None
    backtracked_from: str | None = None
    backtrack_request_creation_time: str | None = None
    status: str | None = None


class CancelExportTaskResult(BaseModel):
    """Result of cancel_export_task."""

    model_config = ConfigDict(frozen=True)

    export_task_identifier: str | None = None
    source_arn: str | None = None
    export_only: list[str] | None = None
    snapshot_time: str | None = None
    task_start_time: str | None = None
    task_end_time: str | None = None
    s3_bucket: str | None = None
    s3_prefix: str | None = None
    iam_role_arn: str | None = None
    kms_key_id: str | None = None
    status: str | None = None
    percent_progress: int | None = None
    total_extracted_data_in_gb: int | None = None
    failure_cause: str | None = None
    warning_message: str | None = None
    source_type: str | None = None


class CopyDbClusterParameterGroupResult(BaseModel):
    """Result of copy_db_cluster_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_cluster_parameter_group: dict[str, Any] | None = None


class CopyDbClusterSnapshotResult(BaseModel):
    """Result of copy_db_cluster_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_cluster_snapshot: dict[str, Any] | None = None


class CopyDbParameterGroupResult(BaseModel):
    """Result of copy_db_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_parameter_group: dict[str, Any] | None = None


class CopyDbSnapshotResult(BaseModel):
    """Result of copy_db_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_snapshot: dict[str, Any] | None = None


class CopyOptionGroupResult(BaseModel):
    """Result of copy_option_group."""

    model_config = ConfigDict(frozen=True)

    option_group: dict[str, Any] | None = None


class CreateBlueGreenDeploymentResult(BaseModel):
    """Result of create_blue_green_deployment."""

    model_config = ConfigDict(frozen=True)

    blue_green_deployment: dict[str, Any] | None = None


class CreateCustomDbEngineVersionResult(BaseModel):
    """Result of create_custom_db_engine_version."""

    model_config = ConfigDict(frozen=True)

    engine: str | None = None
    major_engine_version: str | None = None
    engine_version: str | None = None
    database_installation_files_s3_bucket_name: str | None = None
    database_installation_files_s3_prefix: str | None = None
    custom_db_engine_version_manifest: str | None = None
    db_parameter_group_family: str | None = None
    db_engine_description: str | None = None
    db_engine_version_arn: str | None = None
    db_engine_version_description: str | None = None
    default_character_set: dict[str, Any] | None = None
    image: dict[str, Any] | None = None
    db_engine_media_type: str | None = None
    kms_key_id: str | None = None
    create_time: str | None = None
    supported_character_sets: list[dict[str, Any]] | None = None
    supported_nchar_character_sets: list[dict[str, Any]] | None = None
    valid_upgrade_target: list[dict[str, Any]] | None = None
    supported_timezones: list[dict[str, Any]] | None = None
    exportable_log_types: list[str] | None = None
    supports_log_exports_to_cloudwatch_logs: bool | None = None
    supports_read_replica: bool | None = None
    supported_engine_modes: list[str] | None = None
    supported_feature_names: list[str] | None = None
    status: str | None = None
    supports_parallel_query: bool | None = None
    supports_global_databases: bool | None = None
    tag_list: list[dict[str, Any]] | None = None
    supports_babelfish: bool | None = None
    supports_limitless_database: bool | None = None
    supports_certificate_rotation_without_restart: bool | None = None
    supported_ca_certificate_identifiers: list[str] | None = None
    supports_local_write_forwarding: bool | None = None
    supports_integrations: bool | None = None
    serverless_v2_features_support: dict[str, Any] | None = None


class CreateDbClusterResult(BaseModel):
    """Result of create_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class CreateDbClusterEndpointResult(BaseModel):
    """Result of create_db_cluster_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_cluster_endpoint_identifier: str | None = None
    db_cluster_identifier: str | None = None
    db_cluster_endpoint_resource_identifier: str | None = None
    endpoint: str | None = None
    status: str | None = None
    endpoint_type: str | None = None
    custom_endpoint_type: str | None = None
    static_members: list[str] | None = None
    excluded_members: list[str] | None = None
    db_cluster_endpoint_arn: str | None = None


class CreateDbClusterParameterGroupResult(BaseModel):
    """Result of create_db_cluster_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_cluster_parameter_group: dict[str, Any] | None = None


class CreateDbClusterSnapshotResult(BaseModel):
    """Result of create_db_cluster_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_cluster_snapshot: dict[str, Any] | None = None


class CreateDbInstanceResult(BaseModel):
    """Result of create_db_instance."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class CreateDbInstanceReadReplicaResult(BaseModel):
    """Result of create_db_instance_read_replica."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class CreateDbParameterGroupResult(BaseModel):
    """Result of create_db_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_parameter_group: dict[str, Any] | None = None


class CreateDbProxyResult(BaseModel):
    """Result of create_db_proxy."""

    model_config = ConfigDict(frozen=True)

    db_proxy: dict[str, Any] | None = None


class CreateDbProxyEndpointResult(BaseModel):
    """Result of create_db_proxy_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_proxy_endpoint: dict[str, Any] | None = None


class CreateDbSecurityGroupResult(BaseModel):
    """Result of create_db_security_group."""

    model_config = ConfigDict(frozen=True)

    db_security_group: dict[str, Any] | None = None


class CreateDbShardGroupResult(BaseModel):
    """Result of create_db_shard_group."""

    model_config = ConfigDict(frozen=True)

    db_shard_group_resource_id: str | None = None
    db_shard_group_identifier: str | None = None
    db_cluster_identifier: str | None = None
    max_acu: float | None = None
    min_acu: float | None = None
    compute_redundancy: int | None = None
    status: str | None = None
    publicly_accessible: bool | None = None
    endpoint: str | None = None
    db_shard_group_arn: str | None = None
    tag_list: list[dict[str, Any]] | None = None


class CreateDbSubnetGroupResult(BaseModel):
    """Result of create_db_subnet_group."""

    model_config = ConfigDict(frozen=True)

    db_subnet_group: dict[str, Any] | None = None


class CreateEventSubscriptionResult(BaseModel):
    """Result of create_event_subscription."""

    model_config = ConfigDict(frozen=True)

    event_subscription: dict[str, Any] | None = None


class CreateGlobalClusterResult(BaseModel):
    """Result of create_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class CreateIntegrationResult(BaseModel):
    """Result of create_integration."""

    model_config = ConfigDict(frozen=True)

    source_arn: str | None = None
    target_arn: str | None = None
    integration_name: str | None = None
    integration_arn: str | None = None
    kms_key_id: str | None = None
    additional_encryption_context: dict[str, Any] | None = None
    status: str | None = None
    tags: list[dict[str, Any]] | None = None
    data_filter: str | None = None
    description: str | None = None
    create_time: str | None = None
    errors: list[dict[str, Any]] | None = None


class CreateOptionGroupResult(BaseModel):
    """Result of create_option_group."""

    model_config = ConfigDict(frozen=True)

    option_group: dict[str, Any] | None = None


class CreateTenantDatabaseResult(BaseModel):
    """Result of create_tenant_database."""

    model_config = ConfigDict(frozen=True)

    tenant_database: dict[str, Any] | None = None


class DeleteBlueGreenDeploymentResult(BaseModel):
    """Result of delete_blue_green_deployment."""

    model_config = ConfigDict(frozen=True)

    blue_green_deployment: dict[str, Any] | None = None


class DeleteCustomDbEngineVersionResult(BaseModel):
    """Result of delete_custom_db_engine_version."""

    model_config = ConfigDict(frozen=True)

    engine: str | None = None
    major_engine_version: str | None = None
    engine_version: str | None = None
    database_installation_files_s3_bucket_name: str | None = None
    database_installation_files_s3_prefix: str | None = None
    custom_db_engine_version_manifest: str | None = None
    db_parameter_group_family: str | None = None
    db_engine_description: str | None = None
    db_engine_version_arn: str | None = None
    db_engine_version_description: str | None = None
    default_character_set: dict[str, Any] | None = None
    image: dict[str, Any] | None = None
    db_engine_media_type: str | None = None
    kms_key_id: str | None = None
    create_time: str | None = None
    supported_character_sets: list[dict[str, Any]] | None = None
    supported_nchar_character_sets: list[dict[str, Any]] | None = None
    valid_upgrade_target: list[dict[str, Any]] | None = None
    supported_timezones: list[dict[str, Any]] | None = None
    exportable_log_types: list[str] | None = None
    supports_log_exports_to_cloudwatch_logs: bool | None = None
    supports_read_replica: bool | None = None
    supported_engine_modes: list[str] | None = None
    supported_feature_names: list[str] | None = None
    status: str | None = None
    supports_parallel_query: bool | None = None
    supports_global_databases: bool | None = None
    tag_list: list[dict[str, Any]] | None = None
    supports_babelfish: bool | None = None
    supports_limitless_database: bool | None = None
    supports_certificate_rotation_without_restart: bool | None = None
    supported_ca_certificate_identifiers: list[str] | None = None
    supports_local_write_forwarding: bool | None = None
    supports_integrations: bool | None = None
    serverless_v2_features_support: dict[str, Any] | None = None


class DeleteDbClusterResult(BaseModel):
    """Result of delete_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class DeleteDbClusterAutomatedBackupResult(BaseModel):
    """Result of delete_db_cluster_automated_backup."""

    model_config = ConfigDict(frozen=True)

    db_cluster_automated_backup: dict[str, Any] | None = None


class DeleteDbClusterEndpointResult(BaseModel):
    """Result of delete_db_cluster_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_cluster_endpoint_identifier: str | None = None
    db_cluster_identifier: str | None = None
    db_cluster_endpoint_resource_identifier: str | None = None
    endpoint: str | None = None
    status: str | None = None
    endpoint_type: str | None = None
    custom_endpoint_type: str | None = None
    static_members: list[str] | None = None
    excluded_members: list[str] | None = None
    db_cluster_endpoint_arn: str | None = None


class DeleteDbClusterSnapshotResult(BaseModel):
    """Result of delete_db_cluster_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_cluster_snapshot: dict[str, Any] | None = None


class DeleteDbInstanceResult(BaseModel):
    """Result of delete_db_instance."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class DeleteDbInstanceAutomatedBackupResult(BaseModel):
    """Result of delete_db_instance_automated_backup."""

    model_config = ConfigDict(frozen=True)

    db_instance_automated_backup: dict[str, Any] | None = None


class DeleteDbProxyResult(BaseModel):
    """Result of delete_db_proxy."""

    model_config = ConfigDict(frozen=True)

    db_proxy: dict[str, Any] | None = None


class DeleteDbProxyEndpointResult(BaseModel):
    """Result of delete_db_proxy_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_proxy_endpoint: dict[str, Any] | None = None


class DeleteDbShardGroupResult(BaseModel):
    """Result of delete_db_shard_group."""

    model_config = ConfigDict(frozen=True)

    db_shard_group_resource_id: str | None = None
    db_shard_group_identifier: str | None = None
    db_cluster_identifier: str | None = None
    max_acu: float | None = None
    min_acu: float | None = None
    compute_redundancy: int | None = None
    status: str | None = None
    publicly_accessible: bool | None = None
    endpoint: str | None = None
    db_shard_group_arn: str | None = None
    tag_list: list[dict[str, Any]] | None = None


class DeleteEventSubscriptionResult(BaseModel):
    """Result of delete_event_subscription."""

    model_config = ConfigDict(frozen=True)

    event_subscription: dict[str, Any] | None = None


class DeleteGlobalClusterResult(BaseModel):
    """Result of delete_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class DeleteIntegrationResult(BaseModel):
    """Result of delete_integration."""

    model_config = ConfigDict(frozen=True)

    source_arn: str | None = None
    target_arn: str | None = None
    integration_name: str | None = None
    integration_arn: str | None = None
    kms_key_id: str | None = None
    additional_encryption_context: dict[str, Any] | None = None
    status: str | None = None
    tags: list[dict[str, Any]] | None = None
    data_filter: str | None = None
    description: str | None = None
    create_time: str | None = None
    errors: list[dict[str, Any]] | None = None


class DeleteTenantDatabaseResult(BaseModel):
    """Result of delete_tenant_database."""

    model_config = ConfigDict(frozen=True)

    tenant_database: dict[str, Any] | None = None


class DescribeAccountAttributesResult(BaseModel):
    """Result of describe_account_attributes."""

    model_config = ConfigDict(frozen=True)

    account_quotas: list[dict[str, Any]] | None = None


class DescribeBlueGreenDeploymentsResult(BaseModel):
    """Result of describe_blue_green_deployments."""

    model_config = ConfigDict(frozen=True)

    blue_green_deployments: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeCertificatesResult(BaseModel):
    """Result of describe_certificates."""

    model_config = ConfigDict(frozen=True)

    default_certificate_for_new_launches: str | None = None
    certificates: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbClusterAutomatedBackupsResult(BaseModel):
    """Result of describe_db_cluster_automated_backups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_cluster_automated_backups: list[dict[str, Any]] | None = None


class DescribeDbClusterBacktracksResult(BaseModel):
    """Result of describe_db_cluster_backtracks."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_cluster_backtracks: list[dict[str, Any]] | None = None


class DescribeDbClusterEndpointsResult(BaseModel):
    """Result of describe_db_cluster_endpoints."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_cluster_endpoints: list[dict[str, Any]] | None = None


class DescribeDbClusterParameterGroupsResult(BaseModel):
    """Result of describe_db_cluster_parameter_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_cluster_parameter_groups: list[dict[str, Any]] | None = None


class DescribeDbClusterParametersResult(BaseModel):
    """Result of describe_db_cluster_parameters."""

    model_config = ConfigDict(frozen=True)

    parameters: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbClusterSnapshotAttributesResult(BaseModel):
    """Result of describe_db_cluster_snapshot_attributes."""

    model_config = ConfigDict(frozen=True)

    db_cluster_snapshot_attributes_result: dict[str, Any] | None = None


class DescribeDbClusterSnapshotsResult(BaseModel):
    """Result of describe_db_cluster_snapshots."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_cluster_snapshots: list[dict[str, Any]] | None = None


class DescribeDbClustersResult(BaseModel):
    """Result of describe_db_clusters."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_clusters: list[dict[str, Any]] | None = None


class DescribeDbEngineVersionsResult(BaseModel):
    """Result of describe_db_engine_versions."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_engine_versions: list[dict[str, Any]] | None = None


class DescribeDbInstanceAutomatedBackupsResult(BaseModel):
    """Result of describe_db_instance_automated_backups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_instance_automated_backups: list[dict[str, Any]] | None = None


class DescribeDbLogFilesResult(BaseModel):
    """Result of describe_db_log_files."""

    model_config = ConfigDict(frozen=True)

    describe_db_log_files: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbMajorEngineVersionsResult(BaseModel):
    """Result of describe_db_major_engine_versions."""

    model_config = ConfigDict(frozen=True)

    db_major_engine_versions: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbParameterGroupsResult(BaseModel):
    """Result of describe_db_parameter_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_parameter_groups: list[dict[str, Any]] | None = None


class DescribeDbParametersResult(BaseModel):
    """Result of describe_db_parameters."""

    model_config = ConfigDict(frozen=True)

    parameters: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbProxiesResult(BaseModel):
    """Result of describe_db_proxies."""

    model_config = ConfigDict(frozen=True)

    db_proxies: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbProxyEndpointsResult(BaseModel):
    """Result of describe_db_proxy_endpoints."""

    model_config = ConfigDict(frozen=True)

    db_proxy_endpoints: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbProxyTargetGroupsResult(BaseModel):
    """Result of describe_db_proxy_target_groups."""

    model_config = ConfigDict(frozen=True)

    target_groups: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbProxyTargetsResult(BaseModel):
    """Result of describe_db_proxy_targets."""

    model_config = ConfigDict(frozen=True)

    targets: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbRecommendationsResult(BaseModel):
    """Result of describe_db_recommendations."""

    model_config = ConfigDict(frozen=True)

    db_recommendations: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbSecurityGroupsResult(BaseModel):
    """Result of describe_db_security_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_security_groups: list[dict[str, Any]] | None = None


class DescribeDbShardGroupsResult(BaseModel):
    """Result of describe_db_shard_groups."""

    model_config = ConfigDict(frozen=True)

    db_shard_groups: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeDbSnapshotAttributesResult(BaseModel):
    """Result of describe_db_snapshot_attributes."""

    model_config = ConfigDict(frozen=True)

    db_snapshot_attributes_result: dict[str, Any] | None = None


class DescribeDbSnapshotTenantDatabasesResult(BaseModel):
    """Result of describe_db_snapshot_tenant_databases."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_snapshot_tenant_databases: list[dict[str, Any]] | None = None


class DescribeDbSubnetGroupsResult(BaseModel):
    """Result of describe_db_subnet_groups."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    db_subnet_groups: list[dict[str, Any]] | None = None


class DescribeEngineDefaultClusterParametersResult(BaseModel):
    """Result of describe_engine_default_cluster_parameters."""

    model_config = ConfigDict(frozen=True)

    engine_defaults: dict[str, Any] | None = None


class DescribeEngineDefaultParametersResult(BaseModel):
    """Result of describe_engine_default_parameters."""

    model_config = ConfigDict(frozen=True)

    engine_defaults: dict[str, Any] | None = None


class DescribeEventCategoriesResult(BaseModel):
    """Result of describe_event_categories."""

    model_config = ConfigDict(frozen=True)

    event_categories_map_list: list[dict[str, Any]] | None = None


class DescribeEventSubscriptionsResult(BaseModel):
    """Result of describe_event_subscriptions."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    event_subscriptions_list: list[dict[str, Any]] | None = None


class DescribeEventsResult(BaseModel):
    """Result of describe_events."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    events: list[dict[str, Any]] | None = None


class DescribeExportTasksResult(BaseModel):
    """Result of describe_export_tasks."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    export_tasks: list[dict[str, Any]] | None = None


class DescribeGlobalClustersResult(BaseModel):
    """Result of describe_global_clusters."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    global_clusters: list[dict[str, Any]] | None = None


class DescribeIntegrationsResult(BaseModel):
    """Result of describe_integrations."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    integrations: list[dict[str, Any]] | None = None


class DescribeOptionGroupOptionsResult(BaseModel):
    """Result of describe_option_group_options."""

    model_config = ConfigDict(frozen=True)

    option_group_options: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeOptionGroupsResult(BaseModel):
    """Result of describe_option_groups."""

    model_config = ConfigDict(frozen=True)

    option_groups_list: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeOrderableDbInstanceOptionsResult(BaseModel):
    """Result of describe_orderable_db_instance_options."""

    model_config = ConfigDict(frozen=True)

    orderable_db_instance_options: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribePendingMaintenanceActionsResult(BaseModel):
    """Result of describe_pending_maintenance_actions."""

    model_config = ConfigDict(frozen=True)

    pending_maintenance_actions: list[dict[str, Any]] | None = None
    marker: str | None = None


class DescribeReservedDbInstancesResult(BaseModel):
    """Result of describe_reserved_db_instances."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    reserved_db_instances: list[dict[str, Any]] | None = None


class DescribeReservedDbInstancesOfferingsResult(BaseModel):
    """Result of describe_reserved_db_instances_offerings."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    reserved_db_instances_offerings: list[dict[str, Any]] | None = None


class DescribeSourceRegionsResult(BaseModel):
    """Result of describe_source_regions."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    source_regions: list[dict[str, Any]] | None = None


class DescribeTenantDatabasesResult(BaseModel):
    """Result of describe_tenant_databases."""

    model_config = ConfigDict(frozen=True)

    marker: str | None = None
    tenant_databases: list[dict[str, Any]] | None = None


class DescribeValidDbInstanceModificationsResult(BaseModel):
    """Result of describe_valid_db_instance_modifications."""

    model_config = ConfigDict(frozen=True)

    valid_db_instance_modifications_message: dict[str, Any] | None = None


class DisableHttpEndpointResult(BaseModel):
    """Result of disable_http_endpoint."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    http_endpoint_enabled: bool | None = None


class DownloadDbLogFilePortionResult(BaseModel):
    """Result of download_db_log_file_portion."""

    model_config = ConfigDict(frozen=True)

    log_file_data: str | None = None
    marker: str | None = None
    additional_data_pending: bool | None = None


class EnableHttpEndpointResult(BaseModel):
    """Result of enable_http_endpoint."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    http_endpoint_enabled: bool | None = None


class FailoverDbClusterResult(BaseModel):
    """Result of failover_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class FailoverGlobalClusterResult(BaseModel):
    """Result of failover_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tag_list: list[dict[str, Any]] | None = None


class ModifyActivityStreamResult(BaseModel):
    """Result of modify_activity_stream."""

    model_config = ConfigDict(frozen=True)

    kms_key_id: str | None = None
    kinesis_stream_name: str | None = None
    status: str | None = None
    mode: str | None = None
    engine_native_audit_fields_included: bool | None = None
    policy_status: str | None = None


class ModifyCertificatesResult(BaseModel):
    """Result of modify_certificates."""

    model_config = ConfigDict(frozen=True)

    certificate: dict[str, Any] | None = None


class ModifyCurrentDbClusterCapacityResult(BaseModel):
    """Result of modify_current_db_cluster_capacity."""

    model_config = ConfigDict(frozen=True)

    db_cluster_identifier: str | None = None
    pending_capacity: int | None = None
    current_capacity: int | None = None
    seconds_before_timeout: int | None = None
    timeout_action: str | None = None


class ModifyCustomDbEngineVersionResult(BaseModel):
    """Result of modify_custom_db_engine_version."""

    model_config = ConfigDict(frozen=True)

    engine: str | None = None
    major_engine_version: str | None = None
    engine_version: str | None = None
    database_installation_files_s3_bucket_name: str | None = None
    database_installation_files_s3_prefix: str | None = None
    custom_db_engine_version_manifest: str | None = None
    db_parameter_group_family: str | None = None
    db_engine_description: str | None = None
    db_engine_version_arn: str | None = None
    db_engine_version_description: str | None = None
    default_character_set: dict[str, Any] | None = None
    image: dict[str, Any] | None = None
    db_engine_media_type: str | None = None
    kms_key_id: str | None = None
    create_time: str | None = None
    supported_character_sets: list[dict[str, Any]] | None = None
    supported_nchar_character_sets: list[dict[str, Any]] | None = None
    valid_upgrade_target: list[dict[str, Any]] | None = None
    supported_timezones: list[dict[str, Any]] | None = None
    exportable_log_types: list[str] | None = None
    supports_log_exports_to_cloudwatch_logs: bool | None = None
    supports_read_replica: bool | None = None
    supported_engine_modes: list[str] | None = None
    supported_feature_names: list[str] | None = None
    status: str | None = None
    supports_parallel_query: bool | None = None
    supports_global_databases: bool | None = None
    tag_list: list[dict[str, Any]] | None = None
    supports_babelfish: bool | None = None
    supports_limitless_database: bool | None = None
    supports_certificate_rotation_without_restart: bool | None = None
    supported_ca_certificate_identifiers: list[str] | None = None
    supports_local_write_forwarding: bool | None = None
    supports_integrations: bool | None = None
    serverless_v2_features_support: dict[str, Any] | None = None


class ModifyDbClusterResult(BaseModel):
    """Result of modify_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class ModifyDbClusterEndpointResult(BaseModel):
    """Result of modify_db_cluster_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_cluster_endpoint_identifier: str | None = None
    db_cluster_identifier: str | None = None
    db_cluster_endpoint_resource_identifier: str | None = None
    endpoint: str | None = None
    status: str | None = None
    endpoint_type: str | None = None
    custom_endpoint_type: str | None = None
    static_members: list[str] | None = None
    excluded_members: list[str] | None = None
    db_cluster_endpoint_arn: str | None = None


class ModifyDbClusterParameterGroupResult(BaseModel):
    """Result of modify_db_cluster_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_cluster_parameter_group_name: str | None = None


class ModifyDbClusterSnapshotAttributeResult(BaseModel):
    """Result of modify_db_cluster_snapshot_attribute."""

    model_config = ConfigDict(frozen=True)

    db_cluster_snapshot_attributes_result: dict[str, Any] | None = None


class ModifyDbInstanceResult(BaseModel):
    """Result of modify_db_instance."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class ModifyDbParameterGroupResult(BaseModel):
    """Result of modify_db_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_parameter_group_name: str | None = None


class ModifyDbProxyResult(BaseModel):
    """Result of modify_db_proxy."""

    model_config = ConfigDict(frozen=True)

    db_proxy: dict[str, Any] | None = None


class ModifyDbProxyEndpointResult(BaseModel):
    """Result of modify_db_proxy_endpoint."""

    model_config = ConfigDict(frozen=True)

    db_proxy_endpoint: dict[str, Any] | None = None


class ModifyDbProxyTargetGroupResult(BaseModel):
    """Result of modify_db_proxy_target_group."""

    model_config = ConfigDict(frozen=True)

    db_proxy_target_group: dict[str, Any] | None = None


class ModifyDbRecommendationResult(BaseModel):
    """Result of modify_db_recommendation."""

    model_config = ConfigDict(frozen=True)

    db_recommendation: dict[str, Any] | None = None


class ModifyDbShardGroupResult(BaseModel):
    """Result of modify_db_shard_group."""

    model_config = ConfigDict(frozen=True)

    db_shard_group_resource_id: str | None = None
    db_shard_group_identifier: str | None = None
    db_cluster_identifier: str | None = None
    max_acu: float | None = None
    min_acu: float | None = None
    compute_redundancy: int | None = None
    status: str | None = None
    publicly_accessible: bool | None = None
    endpoint: str | None = None
    db_shard_group_arn: str | None = None
    tag_list: list[dict[str, Any]] | None = None


class ModifyDbSnapshotResult(BaseModel):
    """Result of modify_db_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_snapshot: dict[str, Any] | None = None


class ModifyDbSnapshotAttributeResult(BaseModel):
    """Result of modify_db_snapshot_attribute."""

    model_config = ConfigDict(frozen=True)

    db_snapshot_attributes_result: dict[str, Any] | None = None


class ModifyDbSubnetGroupResult(BaseModel):
    """Result of modify_db_subnet_group."""

    model_config = ConfigDict(frozen=True)

    db_subnet_group: dict[str, Any] | None = None


class ModifyEventSubscriptionResult(BaseModel):
    """Result of modify_event_subscription."""

    model_config = ConfigDict(frozen=True)

    event_subscription: dict[str, Any] | None = None


class ModifyGlobalClusterResult(BaseModel):
    """Result of modify_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class ModifyIntegrationResult(BaseModel):
    """Result of modify_integration."""

    model_config = ConfigDict(frozen=True)

    source_arn: str | None = None
    target_arn: str | None = None
    integration_name: str | None = None
    integration_arn: str | None = None
    kms_key_id: str | None = None
    additional_encryption_context: dict[str, Any] | None = None
    status: str | None = None
    tags: list[dict[str, Any]] | None = None
    data_filter: str | None = None
    description: str | None = None
    create_time: str | None = None
    errors: list[dict[str, Any]] | None = None


class ModifyOptionGroupResult(BaseModel):
    """Result of modify_option_group."""

    model_config = ConfigDict(frozen=True)

    option_group: dict[str, Any] | None = None


class ModifyTenantDatabaseResult(BaseModel):
    """Result of modify_tenant_database."""

    model_config = ConfigDict(frozen=True)

    tenant_database: dict[str, Any] | None = None


class PromoteReadReplicaResult(BaseModel):
    """Result of promote_read_replica."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class PromoteReadReplicaDbClusterResult(BaseModel):
    """Result of promote_read_replica_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class PurchaseReservedDbInstancesOfferingResult(BaseModel):
    """Result of purchase_reserved_db_instances_offering."""

    model_config = ConfigDict(frozen=True)

    reserved_db_instance: dict[str, Any] | None = None


class RebootDbClusterResult(BaseModel):
    """Result of reboot_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class RebootDbInstanceResult(BaseModel):
    """Result of reboot_db_instance."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class RebootDbShardGroupResult(BaseModel):
    """Result of reboot_db_shard_group."""

    model_config = ConfigDict(frozen=True)

    db_shard_group_resource_id: str | None = None
    db_shard_group_identifier: str | None = None
    db_cluster_identifier: str | None = None
    max_acu: float | None = None
    min_acu: float | None = None
    compute_redundancy: int | None = None
    status: str | None = None
    publicly_accessible: bool | None = None
    endpoint: str | None = None
    db_shard_group_arn: str | None = None
    tag_list: list[dict[str, Any]] | None = None


class RegisterDbProxyTargetsResult(BaseModel):
    """Result of register_db_proxy_targets."""

    model_config = ConfigDict(frozen=True)

    db_proxy_targets: list[dict[str, Any]] | None = None


class RemoveFromGlobalClusterResult(BaseModel):
    """Result of remove_from_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class RemoveSourceIdentifierFromSubscriptionResult(BaseModel):
    """Result of remove_source_identifier_from_subscription."""

    model_config = ConfigDict(frozen=True)

    event_subscription: dict[str, Any] | None = None


class ResetDbClusterParameterGroupResult(BaseModel):
    """Result of reset_db_cluster_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_cluster_parameter_group_name: str | None = None


class ResetDbParameterGroupResult(BaseModel):
    """Result of reset_db_parameter_group."""

    model_config = ConfigDict(frozen=True)

    db_parameter_group_name: str | None = None


class RestoreDbClusterFromS3Result(BaseModel):
    """Result of restore_db_cluster_from_s3."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class RestoreDbClusterFromSnapshotResult(BaseModel):
    """Result of restore_db_cluster_from_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class RestoreDbClusterToPointInTimeResult(BaseModel):
    """Result of restore_db_cluster_to_point_in_time."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class RestoreDbInstanceFromDbSnapshotResult(BaseModel):
    """Result of restore_db_instance_from_db_snapshot."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class RestoreDbInstanceFromS3Result(BaseModel):
    """Result of restore_db_instance_from_s3."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class RestoreDbInstanceToPointInTimeResult(BaseModel):
    """Result of restore_db_instance_to_point_in_time."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


class RevokeDbSecurityGroupIngressResult(BaseModel):
    """Result of revoke_db_security_group_ingress."""

    model_config = ConfigDict(frozen=True)

    db_security_group: dict[str, Any] | None = None


class StartActivityStreamResult(BaseModel):
    """Result of start_activity_stream."""

    model_config = ConfigDict(frozen=True)

    kms_key_id: str | None = None
    kinesis_stream_name: str | None = None
    status: str | None = None
    mode: str | None = None
    engine_native_audit_fields_included: bool | None = None
    apply_immediately: bool | None = None


class StartDbClusterResult(BaseModel):
    """Result of start_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class StartDbInstanceAutomatedBackupsReplicationResult(BaseModel):
    """Result of start_db_instance_automated_backups_replication."""

    model_config = ConfigDict(frozen=True)

    db_instance_automated_backup: dict[str, Any] | None = None


class StartExportTaskResult(BaseModel):
    """Result of start_export_task."""

    model_config = ConfigDict(frozen=True)

    export_task_identifier: str | None = None
    source_arn: str | None = None
    export_only: list[str] | None = None
    snapshot_time: str | None = None
    task_start_time: str | None = None
    task_end_time: str | None = None
    s3_bucket: str | None = None
    s3_prefix: str | None = None
    iam_role_arn: str | None = None
    kms_key_id: str | None = None
    status: str | None = None
    percent_progress: int | None = None
    total_extracted_data_in_gb: int | None = None
    failure_cause: str | None = None
    warning_message: str | None = None
    source_type: str | None = None


class StopActivityStreamResult(BaseModel):
    """Result of stop_activity_stream."""

    model_config = ConfigDict(frozen=True)

    kms_key_id: str | None = None
    kinesis_stream_name: str | None = None
    status: str | None = None


class StopDbClusterResult(BaseModel):
    """Result of stop_db_cluster."""

    model_config = ConfigDict(frozen=True)

    db_cluster: dict[str, Any] | None = None


class StopDbInstanceAutomatedBackupsReplicationResult(BaseModel):
    """Result of stop_db_instance_automated_backups_replication."""

    model_config = ConfigDict(frozen=True)

    db_instance_automated_backup: dict[str, Any] | None = None


class SwitchoverBlueGreenDeploymentResult(BaseModel):
    """Result of switchover_blue_green_deployment."""

    model_config = ConfigDict(frozen=True)

    blue_green_deployment: dict[str, Any] | None = None


class SwitchoverGlobalClusterResult(BaseModel):
    """Result of switchover_global_cluster."""

    model_config = ConfigDict(frozen=True)

    global_cluster: dict[str, Any] | None = None


class SwitchoverReadReplicaResult(BaseModel):
    """Result of switchover_read_replica."""

    model_config = ConfigDict(frozen=True)

    db_instance: dict[str, Any] | None = None


def add_role_to_db_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["RoleArn"] = role_arn
    if feature_name is not None:
        kwargs["FeatureName"] = feature_name
    try:
        client.add_role_to_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add role to db cluster") from exc
    return None


def add_role_to_db_instance(
    db_instance_identifier: str,
    role_arn: str,
    feature_name: str,
    region_name: str | None = None,
) -> None:
    """Add role to db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        role_arn: Role arn.
        feature_name: Feature name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["RoleArn"] = role_arn
    kwargs["FeatureName"] = feature_name
    try:
        client.add_role_to_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add role to db instance") from exc
    return None


def add_source_identifier_to_subscription(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SourceIdentifier"] = source_identifier
    try:
        resp = client.add_source_identifier_to_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add source identifier to subscription") from exc
    return AddSourceIdentifierToSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


def add_tags_to_resource(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["Tags"] = tags
    try:
        client.add_tags_to_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add tags to resource") from exc
    return None


def apply_pending_maintenance_action(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceIdentifier"] = resource_identifier
    kwargs["ApplyAction"] = apply_action
    kwargs["OptInType"] = opt_in_type
    try:
        resp = client.apply_pending_maintenance_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to apply pending maintenance action") from exc
    return ApplyPendingMaintenanceActionResult(
        resource_pending_maintenance_actions=resp.get("ResourcePendingMaintenanceActions"),
    )


def authorize_db_security_group_ingress(
    db_security_group_name: str,
    *,
    cidrip: str | None = None,
    ec2_security_group_name: str | None = None,
    ec2_security_group_id: str | None = None,
    ec2_security_group_owner_id: str | None = None,
    region_name: str | None = None,
) -> AuthorizeDbSecurityGroupIngressResult:
    """Authorize db security group ingress.

    Args:
        db_security_group_name: Db security group name.
        cidrip: Cidrip.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_id: Ec2 security group id.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSecurityGroupName"] = db_security_group_name
    if cidrip is not None:
        kwargs["CIDRIP"] = cidrip
    if ec2_security_group_name is not None:
        kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    if ec2_security_group_id is not None:
        kwargs["EC2SecurityGroupId"] = ec2_security_group_id
    if ec2_security_group_owner_id is not None:
        kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = client.authorize_db_security_group_ingress(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to authorize db security group ingress") from exc
    return AuthorizeDbSecurityGroupIngressResult(
        db_security_group=resp.get("DBSecurityGroup"),
    )


def backtrack_db_cluster(
    db_cluster_identifier: str,
    backtrack_to: str,
    *,
    force: bool | None = None,
    use_earliest_time_on_point_in_time_unavailable: bool | None = None,
    region_name: str | None = None,
) -> BacktrackDbClusterResult:
    """Backtrack db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        backtrack_to: Backtrack to.
        force: Force.
        use_earliest_time_on_point_in_time_unavailable: Use earliest time on point in time unavailable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["BacktrackTo"] = backtrack_to
    if force is not None:
        kwargs["Force"] = force
    if use_earliest_time_on_point_in_time_unavailable is not None:
        kwargs["UseEarliestTimeOnPointInTimeUnavailable"] = (
            use_earliest_time_on_point_in_time_unavailable
        )
    try:
        resp = client.backtrack_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to backtrack db cluster") from exc
    return BacktrackDbClusterResult(
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        backtrack_identifier=resp.get("BacktrackIdentifier"),
        backtrack_to=resp.get("BacktrackTo"),
        backtracked_from=resp.get("BacktrackedFrom"),
        backtrack_request_creation_time=resp.get("BacktrackRequestCreationTime"),
        status=resp.get("Status"),
    )


def cancel_export_task(
    export_task_identifier: str,
    region_name: str | None = None,
) -> CancelExportTaskResult:
    """Cancel export task.

    Args:
        export_task_identifier: Export task identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExportTaskIdentifier"] = export_task_identifier
    try:
        resp = client.cancel_export_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel export task") from exc
    return CancelExportTaskResult(
        export_task_identifier=resp.get("ExportTaskIdentifier"),
        source_arn=resp.get("SourceArn"),
        export_only=resp.get("ExportOnly"),
        snapshot_time=resp.get("SnapshotTime"),
        task_start_time=resp.get("TaskStartTime"),
        task_end_time=resp.get("TaskEndTime"),
        s3_bucket=resp.get("S3Bucket"),
        s3_prefix=resp.get("S3Prefix"),
        iam_role_arn=resp.get("IamRoleArn"),
        kms_key_id=resp.get("KmsKeyId"),
        status=resp.get("Status"),
        percent_progress=resp.get("PercentProgress"),
        total_extracted_data_in_gb=resp.get("TotalExtractedDataInGB"),
        failure_cause=resp.get("FailureCause"),
        warning_message=resp.get("WarningMessage"),
        source_type=resp.get("SourceType"),
    )


def copy_db_cluster_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBClusterParameterGroupIdentifier"] = source_db_cluster_parameter_group_identifier
    kwargs["TargetDBClusterParameterGroupIdentifier"] = target_db_cluster_parameter_group_identifier
    kwargs["TargetDBClusterParameterGroupDescription"] = (
        target_db_cluster_parameter_group_description
    )
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.copy_db_cluster_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy db cluster parameter group") from exc
    return CopyDbClusterParameterGroupResult(
        db_cluster_parameter_group=resp.get("DBClusterParameterGroup"),
    )


def copy_db_cluster_snapshot(
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
    client = get_client("rds", region_name)
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
        resp = client.copy_db_cluster_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy db cluster snapshot") from exc
    return CopyDbClusterSnapshotResult(
        db_cluster_snapshot=resp.get("DBClusterSnapshot"),
    )


def copy_db_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBParameterGroupIdentifier"] = source_db_parameter_group_identifier
    kwargs["TargetDBParameterGroupIdentifier"] = target_db_parameter_group_identifier
    kwargs["TargetDBParameterGroupDescription"] = target_db_parameter_group_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.copy_db_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy db parameter group") from exc
    return CopyDbParameterGroupResult(
        db_parameter_group=resp.get("DBParameterGroup"),
    )


def copy_db_snapshot(
    source_db_snapshot_identifier: str,
    target_db_snapshot_identifier: str,
    *,
    kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    copy_tags: bool | None = None,
    pre_signed_url: str | None = None,
    option_group_name: str | None = None,
    target_custom_availability_zone: str | None = None,
    snapshot_target: str | None = None,
    copy_option_group: bool | None = None,
    snapshot_availability_zone: str | None = None,
    source_region: str | None = None,
    region_name: str | None = None,
) -> CopyDbSnapshotResult:
    """Copy db snapshot.

    Args:
        source_db_snapshot_identifier: Source db snapshot identifier.
        target_db_snapshot_identifier: Target db snapshot identifier.
        kms_key_id: Kms key id.
        tags: Tags.
        copy_tags: Copy tags.
        pre_signed_url: Pre signed url.
        option_group_name: Option group name.
        target_custom_availability_zone: Target custom availability zone.
        snapshot_target: Snapshot target.
        copy_option_group: Copy option group.
        snapshot_availability_zone: Snapshot availability zone.
        source_region: Source region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBSnapshotIdentifier"] = source_db_snapshot_identifier
    kwargs["TargetDBSnapshotIdentifier"] = target_db_snapshot_identifier
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    if copy_tags is not None:
        kwargs["CopyTags"] = copy_tags
    if pre_signed_url is not None:
        kwargs["PreSignedUrl"] = pre_signed_url
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if target_custom_availability_zone is not None:
        kwargs["TargetCustomAvailabilityZone"] = target_custom_availability_zone
    if snapshot_target is not None:
        kwargs["SnapshotTarget"] = snapshot_target
    if copy_option_group is not None:
        kwargs["CopyOptionGroup"] = copy_option_group
    if snapshot_availability_zone is not None:
        kwargs["SnapshotAvailabilityZone"] = snapshot_availability_zone
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    try:
        resp = client.copy_db_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy db snapshot") from exc
    return CopyDbSnapshotResult(
        db_snapshot=resp.get("DBSnapshot"),
    )


def copy_option_group(
    source_option_group_identifier: str,
    target_option_group_identifier: str,
    target_option_group_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CopyOptionGroupResult:
    """Copy option group.

    Args:
        source_option_group_identifier: Source option group identifier.
        target_option_group_identifier: Target option group identifier.
        target_option_group_description: Target option group description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceOptionGroupIdentifier"] = source_option_group_identifier
    kwargs["TargetOptionGroupIdentifier"] = target_option_group_identifier
    kwargs["TargetOptionGroupDescription"] = target_option_group_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.copy_option_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to copy option group") from exc
    return CopyOptionGroupResult(
        option_group=resp.get("OptionGroup"),
    )


def create_blue_green_deployment(
    blue_green_deployment_name: str,
    source: str,
    *,
    target_engine_version: str | None = None,
    target_db_parameter_group_name: str | None = None,
    target_db_cluster_parameter_group_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    target_db_instance_class: str | None = None,
    upgrade_target_storage_config: bool | None = None,
    target_iops: int | None = None,
    target_storage_type: str | None = None,
    target_allocated_storage: int | None = None,
    target_storage_throughput: int | None = None,
    region_name: str | None = None,
) -> CreateBlueGreenDeploymentResult:
    """Create blue green deployment.

    Args:
        blue_green_deployment_name: Blue green deployment name.
        source: Source.
        target_engine_version: Target engine version.
        target_db_parameter_group_name: Target db parameter group name.
        target_db_cluster_parameter_group_name: Target db cluster parameter group name.
        tags: Tags.
        target_db_instance_class: Target db instance class.
        upgrade_target_storage_config: Upgrade target storage config.
        target_iops: Target iops.
        target_storage_type: Target storage type.
        target_allocated_storage: Target allocated storage.
        target_storage_throughput: Target storage throughput.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueGreenDeploymentName"] = blue_green_deployment_name
    kwargs["Source"] = source
    if target_engine_version is not None:
        kwargs["TargetEngineVersion"] = target_engine_version
    if target_db_parameter_group_name is not None:
        kwargs["TargetDBParameterGroupName"] = target_db_parameter_group_name
    if target_db_cluster_parameter_group_name is not None:
        kwargs["TargetDBClusterParameterGroupName"] = target_db_cluster_parameter_group_name
    if tags is not None:
        kwargs["Tags"] = tags
    if target_db_instance_class is not None:
        kwargs["TargetDBInstanceClass"] = target_db_instance_class
    if upgrade_target_storage_config is not None:
        kwargs["UpgradeTargetStorageConfig"] = upgrade_target_storage_config
    if target_iops is not None:
        kwargs["TargetIops"] = target_iops
    if target_storage_type is not None:
        kwargs["TargetStorageType"] = target_storage_type
    if target_allocated_storage is not None:
        kwargs["TargetAllocatedStorage"] = target_allocated_storage
    if target_storage_throughput is not None:
        kwargs["TargetStorageThroughput"] = target_storage_throughput
    try:
        resp = client.create_blue_green_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create blue green deployment") from exc
    return CreateBlueGreenDeploymentResult(
        blue_green_deployment=resp.get("BlueGreenDeployment"),
    )


def create_custom_db_engine_version(
    engine: str,
    engine_version: str,
    *,
    database_installation_files_s3_bucket_name: str | None = None,
    database_installation_files_s3_prefix: str | None = None,
    image_id: str | None = None,
    kms_key_id: str | None = None,
    source_custom_db_engine_version_identifier: str | None = None,
    use_aws_provided_latest_image: bool | None = None,
    description: str | None = None,
    manifest: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCustomDbEngineVersionResult:
    """Create custom db engine version.

    Args:
        engine: Engine.
        engine_version: Engine version.
        database_installation_files_s3_bucket_name: Database installation files s3 bucket name.
        database_installation_files_s3_prefix: Database installation files s3 prefix.
        image_id: Image id.
        kms_key_id: Kms key id.
        source_custom_db_engine_version_identifier: Source custom db engine version identifier.
        use_aws_provided_latest_image: Use aws provided latest image.
        description: Description.
        manifest: Manifest.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    kwargs["EngineVersion"] = engine_version
    if database_installation_files_s3_bucket_name is not None:
        kwargs["DatabaseInstallationFilesS3BucketName"] = database_installation_files_s3_bucket_name
    if database_installation_files_s3_prefix is not None:
        kwargs["DatabaseInstallationFilesS3Prefix"] = database_installation_files_s3_prefix
    if image_id is not None:
        kwargs["ImageId"] = image_id
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    if source_custom_db_engine_version_identifier is not None:
        kwargs["SourceCustomDbEngineVersionIdentifier"] = source_custom_db_engine_version_identifier
    if use_aws_provided_latest_image is not None:
        kwargs["UseAwsProvidedLatestImage"] = use_aws_provided_latest_image
    if description is not None:
        kwargs["Description"] = description
    if manifest is not None:
        kwargs["Manifest"] = manifest
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_custom_db_engine_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create custom db engine version") from exc
    return CreateCustomDbEngineVersionResult(
        engine=resp.get("Engine"),
        major_engine_version=resp.get("MajorEngineVersion"),
        engine_version=resp.get("EngineVersion"),
        database_installation_files_s3_bucket_name=resp.get(
            "DatabaseInstallationFilesS3BucketName"
        ),
        database_installation_files_s3_prefix=resp.get("DatabaseInstallationFilesS3Prefix"),
        custom_db_engine_version_manifest=resp.get("CustomDBEngineVersionManifest"),
        db_parameter_group_family=resp.get("DBParameterGroupFamily"),
        db_engine_description=resp.get("DBEngineDescription"),
        db_engine_version_arn=resp.get("DBEngineVersionArn"),
        db_engine_version_description=resp.get("DBEngineVersionDescription"),
        default_character_set=resp.get("DefaultCharacterSet"),
        image=resp.get("Image"),
        db_engine_media_type=resp.get("DBEngineMediaType"),
        kms_key_id=resp.get("KMSKeyId"),
        create_time=resp.get("CreateTime"),
        supported_character_sets=resp.get("SupportedCharacterSets"),
        supported_nchar_character_sets=resp.get("SupportedNcharCharacterSets"),
        valid_upgrade_target=resp.get("ValidUpgradeTarget"),
        supported_timezones=resp.get("SupportedTimezones"),
        exportable_log_types=resp.get("ExportableLogTypes"),
        supports_log_exports_to_cloudwatch_logs=resp.get("SupportsLogExportsToCloudwatchLogs"),
        supports_read_replica=resp.get("SupportsReadReplica"),
        supported_engine_modes=resp.get("SupportedEngineModes"),
        supported_feature_names=resp.get("SupportedFeatureNames"),
        status=resp.get("Status"),
        supports_parallel_query=resp.get("SupportsParallelQuery"),
        supports_global_databases=resp.get("SupportsGlobalDatabases"),
        tag_list=resp.get("TagList"),
        supports_babelfish=resp.get("SupportsBabelfish"),
        supports_limitless_database=resp.get("SupportsLimitlessDatabase"),
        supports_certificate_rotation_without_restart=resp.get(
            "SupportsCertificateRotationWithoutRestart"
        ),
        supported_ca_certificate_identifiers=resp.get("SupportedCACertificateIdentifiers"),
        supports_local_write_forwarding=resp.get("SupportsLocalWriteForwarding"),
        supports_integrations=resp.get("SupportsIntegrations"),
        serverless_v2_features_support=resp.get("ServerlessV2FeaturesSupport"),
    )


def create_db_cluster(
    db_cluster_identifier: str,
    engine: str,
    *,
    availability_zones: list[str] | None = None,
    backup_retention_period: int | None = None,
    character_set_name: str | None = None,
    database_name: str | None = None,
    db_cluster_parameter_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    db_subnet_group_name: str | None = None,
    engine_version: str | None = None,
    port: int | None = None,
    master_username: str | None = None,
    master_user_password: str | None = None,
    option_group_name: str | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    replication_source_identifier: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    storage_encrypted: bool | None = None,
    kms_key_id: str | None = None,
    pre_signed_url: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    backtrack_window: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    engine_mode: str | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    rds_custom_cluster_configuration: dict[str, Any] | None = None,
    db_cluster_instance_class: str | None = None,
    allocated_storage: int | None = None,
    storage_type: str | None = None,
    iops: int | None = None,
    publicly_accessible: bool | None = None,
    auto_minor_version_upgrade: bool | None = None,
    deletion_protection: bool | None = None,
    global_cluster_identifier: str | None = None,
    enable_http_endpoint: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    enable_global_write_forwarding: bool | None = None,
    network_type: str | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    enable_limitless_database: bool | None = None,
    cluster_scalability_type: str | None = None,
    db_system_id: str | None = None,
    manage_master_user_password: bool | None = None,
    enable_local_write_forwarding: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    ca_certificate_identifier: str | None = None,
    engine_lifecycle_support: str | None = None,
    master_user_authentication_type: str | None = None,
    source_region: str | None = None,
    region_name: str | None = None,
) -> CreateDbClusterResult:
    """Create db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        engine: Engine.
        availability_zones: Availability zones.
        backup_retention_period: Backup retention period.
        character_set_name: Character set name.
        database_name: Database name.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        vpc_security_group_ids: Vpc security group ids.
        db_subnet_group_name: Db subnet group name.
        engine_version: Engine version.
        port: Port.
        master_username: Master username.
        master_user_password: Master user password.
        option_group_name: Option group name.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        replication_source_identifier: Replication source identifier.
        tags: Tags.
        storage_encrypted: Storage encrypted.
        kms_key_id: Kms key id.
        pre_signed_url: Pre signed url.
        enable_iam_database_authentication: Enable iam database authentication.
        backtrack_window: Backtrack window.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        engine_mode: Engine mode.
        scaling_configuration: Scaling configuration.
        rds_custom_cluster_configuration: Rds custom cluster configuration.
        db_cluster_instance_class: Db cluster instance class.
        allocated_storage: Allocated storage.
        storage_type: Storage type.
        iops: Iops.
        publicly_accessible: Publicly accessible.
        auto_minor_version_upgrade: Auto minor version upgrade.
        deletion_protection: Deletion protection.
        global_cluster_identifier: Global cluster identifier.
        enable_http_endpoint: Enable http endpoint.
        copy_tags_to_snapshot: Copy tags to snapshot.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        enable_global_write_forwarding: Enable global write forwarding.
        network_type: Network type.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        enable_limitless_database: Enable limitless database.
        cluster_scalability_type: Cluster scalability type.
        db_system_id: Db system id.
        manage_master_user_password: Manage master user password.
        enable_local_write_forwarding: Enable local write forwarding.
        master_user_secret_kms_key_id: Master user secret kms key id.
        ca_certificate_identifier: Ca certificate identifier.
        engine_lifecycle_support: Engine lifecycle support.
        master_user_authentication_type: Master user authentication type.
        source_region: Source region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["Engine"] = engine
    if availability_zones is not None:
        kwargs["AvailabilityZones"] = availability_zones
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if character_set_name is not None:
        kwargs["CharacterSetName"] = character_set_name
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if port is not None:
        kwargs["Port"] = port
    if master_username is not None:
        kwargs["MasterUsername"] = master_username
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if replication_source_identifier is not None:
        kwargs["ReplicationSourceIdentifier"] = replication_source_identifier
    if tags is not None:
        kwargs["Tags"] = tags
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if pre_signed_url is not None:
        kwargs["PreSignedUrl"] = pre_signed_url
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if backtrack_window is not None:
        kwargs["BacktrackWindow"] = backtrack_window
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if engine_mode is not None:
        kwargs["EngineMode"] = engine_mode
    if scaling_configuration is not None:
        kwargs["ScalingConfiguration"] = scaling_configuration
    if rds_custom_cluster_configuration is not None:
        kwargs["RdsCustomClusterConfiguration"] = rds_custom_cluster_configuration
    if db_cluster_instance_class is not None:
        kwargs["DBClusterInstanceClass"] = db_cluster_instance_class
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if iops is not None:
        kwargs["Iops"] = iops
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if global_cluster_identifier is not None:
        kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if enable_http_endpoint is not None:
        kwargs["EnableHttpEndpoint"] = enable_http_endpoint
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if enable_global_write_forwarding is not None:
        kwargs["EnableGlobalWriteForwarding"] = enable_global_write_forwarding
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if enable_limitless_database is not None:
        kwargs["EnableLimitlessDatabase"] = enable_limitless_database
    if cluster_scalability_type is not None:
        kwargs["ClusterScalabilityType"] = cluster_scalability_type
    if db_system_id is not None:
        kwargs["DBSystemId"] = db_system_id
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if enable_local_write_forwarding is not None:
        kwargs["EnableLocalWriteForwarding"] = enable_local_write_forwarding
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    if master_user_authentication_type is not None:
        kwargs["MasterUserAuthenticationType"] = master_user_authentication_type
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    try:
        resp = client.create_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db cluster") from exc
    return CreateDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def create_db_cluster_endpoint(
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
    client = get_client("rds", region_name)
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
        resp = client.create_db_cluster_endpoint(**kwargs)
    except ClientError as exc:
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


def create_db_cluster_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_cluster_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db cluster parameter group") from exc
    return CreateDbClusterParameterGroupResult(
        db_cluster_parameter_group=resp.get("DBClusterParameterGroup"),
    )


def create_db_cluster_snapshot(
    db_cluster_snapshot_identifier: str,
    db_cluster_identifier: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbClusterSnapshotResult:
    """Create db cluster snapshot.

    Args:
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        db_cluster_identifier: Db cluster identifier.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_cluster_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db cluster snapshot") from exc
    return CreateDbClusterSnapshotResult(
        db_cluster_snapshot=resp.get("DBClusterSnapshot"),
    )


def create_db_instance(
    db_instance_identifier: str,
    db_instance_class: str,
    engine: str,
    *,
    db_name: str | None = None,
    allocated_storage: int | None = None,
    master_username: str | None = None,
    master_user_password: str | None = None,
    db_security_groups: list[str] | None = None,
    vpc_security_group_ids: list[str] | None = None,
    availability_zone: str | None = None,
    db_subnet_group_name: str | None = None,
    preferred_maintenance_window: str | None = None,
    db_parameter_group_name: str | None = None,
    backup_retention_period: int | None = None,
    preferred_backup_window: str | None = None,
    port: int | None = None,
    multi_az: bool | None = None,
    engine_version: str | None = None,
    auto_minor_version_upgrade: bool | None = None,
    license_model: str | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    character_set_name: str | None = None,
    nchar_character_set_name: str | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    db_cluster_identifier: str | None = None,
    storage_type: str | None = None,
    tde_credential_arn: str | None = None,
    tde_credential_password: str | None = None,
    storage_encrypted: bool | None = None,
    kms_key_id: str | None = None,
    domain: str | None = None,
    domain_fqdn: str | None = None,
    domain_ou: str | None = None,
    domain_auth_secret_arn: str | None = None,
    domain_dns_ips: list[str] | None = None,
    copy_tags_to_snapshot: bool | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    domain_iam_role_name: str | None = None,
    promotion_tier: int | None = None,
    timezone: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    deletion_protection: bool | None = None,
    max_allocated_storage: int | None = None,
    enable_customer_owned_ip: bool | None = None,
    network_type: str | None = None,
    backup_target: str | None = None,
    custom_iam_instance_profile: str | None = None,
    db_system_id: str | None = None,
    ca_certificate_identifier: str | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    multi_tenant: bool | None = None,
    dedicated_log_volume: bool | None = None,
    engine_lifecycle_support: str | None = None,
    master_user_authentication_type: str | None = None,
    region_name: str | None = None,
) -> CreateDbInstanceResult:
    """Create db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        db_instance_class: Db instance class.
        engine: Engine.
        db_name: Db name.
        allocated_storage: Allocated storage.
        master_username: Master username.
        master_user_password: Master user password.
        db_security_groups: Db security groups.
        vpc_security_group_ids: Vpc security group ids.
        availability_zone: Availability zone.
        db_subnet_group_name: Db subnet group name.
        preferred_maintenance_window: Preferred maintenance window.
        db_parameter_group_name: Db parameter group name.
        backup_retention_period: Backup retention period.
        preferred_backup_window: Preferred backup window.
        port: Port.
        multi_az: Multi az.
        engine_version: Engine version.
        auto_minor_version_upgrade: Auto minor version upgrade.
        license_model: License model.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        character_set_name: Character set name.
        nchar_character_set_name: Nchar character set name.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        db_cluster_identifier: Db cluster identifier.
        storage_type: Storage type.
        tde_credential_arn: Tde credential arn.
        tde_credential_password: Tde credential password.
        storage_encrypted: Storage encrypted.
        kms_key_id: Kms key id.
        domain: Domain.
        domain_fqdn: Domain fqdn.
        domain_ou: Domain ou.
        domain_auth_secret_arn: Domain auth secret arn.
        domain_dns_ips: Domain dns ips.
        copy_tags_to_snapshot: Copy tags to snapshot.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        domain_iam_role_name: Domain iam role name.
        promotion_tier: Promotion tier.
        timezone: Timezone.
        enable_iam_database_authentication: Enable iam database authentication.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        processor_features: Processor features.
        deletion_protection: Deletion protection.
        max_allocated_storage: Max allocated storage.
        enable_customer_owned_ip: Enable customer owned ip.
        network_type: Network type.
        backup_target: Backup target.
        custom_iam_instance_profile: Custom iam instance profile.
        db_system_id: Db system id.
        ca_certificate_identifier: Ca certificate identifier.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        multi_tenant: Multi tenant.
        dedicated_log_volume: Dedicated log volume.
        engine_lifecycle_support: Engine lifecycle support.
        master_user_authentication_type: Master user authentication type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["DBInstanceClass"] = db_instance_class
    kwargs["Engine"] = engine
    if db_name is not None:
        kwargs["DBName"] = db_name
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if master_username is not None:
        kwargs["MasterUsername"] = master_username
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if db_security_groups is not None:
        kwargs["DBSecurityGroups"] = db_security_groups
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if port is not None:
        kwargs["Port"] = port
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if character_set_name is not None:
        kwargs["CharacterSetName"] = character_set_name
    if nchar_character_set_name is not None:
        kwargs["NcharCharacterSetName"] = nchar_character_set_name
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["Tags"] = tags
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if tde_credential_arn is not None:
        kwargs["TdeCredentialArn"] = tde_credential_arn
    if tde_credential_password is not None:
        kwargs["TdeCredentialPassword"] = tde_credential_password
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_fqdn is not None:
        kwargs["DomainFqdn"] = domain_fqdn
    if domain_ou is not None:
        kwargs["DomainOu"] = domain_ou
    if domain_auth_secret_arn is not None:
        kwargs["DomainAuthSecretArn"] = domain_auth_secret_arn
    if domain_dns_ips is not None:
        kwargs["DomainDnsIps"] = domain_dns_ips
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if promotion_tier is not None:
        kwargs["PromotionTier"] = promotion_tier
    if timezone is not None:
        kwargs["Timezone"] = timezone
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if max_allocated_storage is not None:
        kwargs["MaxAllocatedStorage"] = max_allocated_storage
    if enable_customer_owned_ip is not None:
        kwargs["EnableCustomerOwnedIp"] = enable_customer_owned_ip
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if backup_target is not None:
        kwargs["BackupTarget"] = backup_target
    if custom_iam_instance_profile is not None:
        kwargs["CustomIamInstanceProfile"] = custom_iam_instance_profile
    if db_system_id is not None:
        kwargs["DBSystemId"] = db_system_id
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if multi_tenant is not None:
        kwargs["MultiTenant"] = multi_tenant
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    if master_user_authentication_type is not None:
        kwargs["MasterUserAuthenticationType"] = master_user_authentication_type
    try:
        resp = client.create_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db instance") from exc
    return CreateDbInstanceResult(
        db_instance=resp.get("DBInstance"),
    )


def create_db_instance_read_replica(
    db_instance_identifier: str,
    *,
    source_db_instance_identifier: str | None = None,
    db_instance_class: str | None = None,
    availability_zone: str | None = None,
    port: int | None = None,
    multi_az: bool | None = None,
    auto_minor_version_upgrade: bool | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    db_parameter_group_name: str | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    db_subnet_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    storage_type: str | None = None,
    copy_tags_to_snapshot: bool | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    kms_key_id: str | None = None,
    pre_signed_url: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    use_default_processor_features: bool | None = None,
    deletion_protection: bool | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    domain_fqdn: str | None = None,
    domain_ou: str | None = None,
    domain_auth_secret_arn: str | None = None,
    domain_dns_ips: list[str] | None = None,
    replica_mode: str | None = None,
    enable_customer_owned_ip: bool | None = None,
    network_type: str | None = None,
    max_allocated_storage: int | None = None,
    backup_target: str | None = None,
    custom_iam_instance_profile: str | None = None,
    allocated_storage: int | None = None,
    source_db_cluster_identifier: str | None = None,
    dedicated_log_volume: bool | None = None,
    upgrade_storage_config: bool | None = None,
    ca_certificate_identifier: str | None = None,
    source_region: str | None = None,
    region_name: str | None = None,
) -> CreateDbInstanceReadReplicaResult:
    """Create db instance read replica.

    Args:
        db_instance_identifier: Db instance identifier.
        source_db_instance_identifier: Source db instance identifier.
        db_instance_class: Db instance class.
        availability_zone: Availability zone.
        port: Port.
        multi_az: Multi az.
        auto_minor_version_upgrade: Auto minor version upgrade.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        db_parameter_group_name: Db parameter group name.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        db_subnet_group_name: Db subnet group name.
        vpc_security_group_ids: Vpc security group ids.
        storage_type: Storage type.
        copy_tags_to_snapshot: Copy tags to snapshot.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        kms_key_id: Kms key id.
        pre_signed_url: Pre signed url.
        enable_iam_database_authentication: Enable iam database authentication.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        processor_features: Processor features.
        use_default_processor_features: Use default processor features.
        deletion_protection: Deletion protection.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        domain_fqdn: Domain fqdn.
        domain_ou: Domain ou.
        domain_auth_secret_arn: Domain auth secret arn.
        domain_dns_ips: Domain dns ips.
        replica_mode: Replica mode.
        enable_customer_owned_ip: Enable customer owned ip.
        network_type: Network type.
        max_allocated_storage: Max allocated storage.
        backup_target: Backup target.
        custom_iam_instance_profile: Custom iam instance profile.
        allocated_storage: Allocated storage.
        source_db_cluster_identifier: Source db cluster identifier.
        dedicated_log_volume: Dedicated log volume.
        upgrade_storage_config: Upgrade storage config.
        ca_certificate_identifier: Ca certificate identifier.
        source_region: Source region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if source_db_instance_identifier is not None:
        kwargs["SourceDBInstanceIdentifier"] = source_db_instance_identifier
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if port is not None:
        kwargs["Port"] = port
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["Tags"] = tags
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if pre_signed_url is not None:
        kwargs["PreSignedUrl"] = pre_signed_url
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if use_default_processor_features is not None:
        kwargs["UseDefaultProcessorFeatures"] = use_default_processor_features
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if domain_fqdn is not None:
        kwargs["DomainFqdn"] = domain_fqdn
    if domain_ou is not None:
        kwargs["DomainOu"] = domain_ou
    if domain_auth_secret_arn is not None:
        kwargs["DomainAuthSecretArn"] = domain_auth_secret_arn
    if domain_dns_ips is not None:
        kwargs["DomainDnsIps"] = domain_dns_ips
    if replica_mode is not None:
        kwargs["ReplicaMode"] = replica_mode
    if enable_customer_owned_ip is not None:
        kwargs["EnableCustomerOwnedIp"] = enable_customer_owned_ip
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if max_allocated_storage is not None:
        kwargs["MaxAllocatedStorage"] = max_allocated_storage
    if backup_target is not None:
        kwargs["BackupTarget"] = backup_target
    if custom_iam_instance_profile is not None:
        kwargs["CustomIamInstanceProfile"] = custom_iam_instance_profile
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if source_db_cluster_identifier is not None:
        kwargs["SourceDBClusterIdentifier"] = source_db_cluster_identifier
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if upgrade_storage_config is not None:
        kwargs["UpgradeStorageConfig"] = upgrade_storage_config
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    try:
        resp = client.create_db_instance_read_replica(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db instance read replica") from exc
    return CreateDbInstanceReadReplicaResult(
        db_instance=resp.get("DBInstance"),
    )


def create_db_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db parameter group") from exc
    return CreateDbParameterGroupResult(
        db_parameter_group=resp.get("DBParameterGroup"),
    )


def create_db_proxy(
    db_proxy_name: str,
    engine_family: str,
    role_arn: str,
    vpc_subnet_ids: list[str],
    *,
    default_auth_scheme: str | None = None,
    auth: list[dict[str, Any]] | None = None,
    vpc_security_group_ids: list[str] | None = None,
    require_tls: bool | None = None,
    idle_client_timeout: int | None = None,
    debug_logging: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    endpoint_network_type: str | None = None,
    target_connection_network_type: str | None = None,
    region_name: str | None = None,
) -> CreateDbProxyResult:
    """Create db proxy.

    Args:
        db_proxy_name: Db proxy name.
        engine_family: Engine family.
        role_arn: Role arn.
        vpc_subnet_ids: Vpc subnet ids.
        default_auth_scheme: Default auth scheme.
        auth: Auth.
        vpc_security_group_ids: Vpc security group ids.
        require_tls: Require tls.
        idle_client_timeout: Idle client timeout.
        debug_logging: Debug logging.
        tags: Tags.
        endpoint_network_type: Endpoint network type.
        target_connection_network_type: Target connection network type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    kwargs["EngineFamily"] = engine_family
    kwargs["RoleArn"] = role_arn
    kwargs["VpcSubnetIds"] = vpc_subnet_ids
    if default_auth_scheme is not None:
        kwargs["DefaultAuthScheme"] = default_auth_scheme
    if auth is not None:
        kwargs["Auth"] = auth
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if require_tls is not None:
        kwargs["RequireTLS"] = require_tls
    if idle_client_timeout is not None:
        kwargs["IdleClientTimeout"] = idle_client_timeout
    if debug_logging is not None:
        kwargs["DebugLogging"] = debug_logging
    if tags is not None:
        kwargs["Tags"] = tags
    if endpoint_network_type is not None:
        kwargs["EndpointNetworkType"] = endpoint_network_type
    if target_connection_network_type is not None:
        kwargs["TargetConnectionNetworkType"] = target_connection_network_type
    try:
        resp = client.create_db_proxy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db proxy") from exc
    return CreateDbProxyResult(
        db_proxy=resp.get("DBProxy"),
    )


def create_db_proxy_endpoint(
    db_proxy_name: str,
    db_proxy_endpoint_name: str,
    vpc_subnet_ids: list[str],
    *,
    vpc_security_group_ids: list[str] | None = None,
    target_role: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    endpoint_network_type: str | None = None,
    region_name: str | None = None,
) -> CreateDbProxyEndpointResult:
    """Create db proxy endpoint.

    Args:
        db_proxy_name: Db proxy name.
        db_proxy_endpoint_name: Db proxy endpoint name.
        vpc_subnet_ids: Vpc subnet ids.
        vpc_security_group_ids: Vpc security group ids.
        target_role: Target role.
        tags: Tags.
        endpoint_network_type: Endpoint network type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    kwargs["DBProxyEndpointName"] = db_proxy_endpoint_name
    kwargs["VpcSubnetIds"] = vpc_subnet_ids
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if target_role is not None:
        kwargs["TargetRole"] = target_role
    if tags is not None:
        kwargs["Tags"] = tags
    if endpoint_network_type is not None:
        kwargs["EndpointNetworkType"] = endpoint_network_type
    try:
        resp = client.create_db_proxy_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db proxy endpoint") from exc
    return CreateDbProxyEndpointResult(
        db_proxy_endpoint=resp.get("DBProxyEndpoint"),
    )


def create_db_security_group(
    db_security_group_name: str,
    db_security_group_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbSecurityGroupResult:
    """Create db security group.

    Args:
        db_security_group_name: Db security group name.
        db_security_group_description: Db security group description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSecurityGroupName"] = db_security_group_name
    kwargs["DBSecurityGroupDescription"] = db_security_group_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_security_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db security group") from exc
    return CreateDbSecurityGroupResult(
        db_security_group=resp.get("DBSecurityGroup"),
    )


def create_db_shard_group(
    db_shard_group_identifier: str,
    db_cluster_identifier: str,
    max_acu: float,
    *,
    compute_redundancy: int | None = None,
    min_acu: float | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDbShardGroupResult:
    """Create db shard group.

    Args:
        db_shard_group_identifier: Db shard group identifier.
        db_cluster_identifier: Db cluster identifier.
        max_acu: Max acu.
        compute_redundancy: Compute redundancy.
        min_acu: Min acu.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBShardGroupIdentifier"] = db_shard_group_identifier
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["MaxACU"] = max_acu
    if compute_redundancy is not None:
        kwargs["ComputeRedundancy"] = compute_redundancy
    if min_acu is not None:
        kwargs["MinACU"] = min_acu
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_shard_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db shard group") from exc
    return CreateDbShardGroupResult(
        db_shard_group_resource_id=resp.get("DBShardGroupResourceId"),
        db_shard_group_identifier=resp.get("DBShardGroupIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        max_acu=resp.get("MaxACU"),
        min_acu=resp.get("MinACU"),
        compute_redundancy=resp.get("ComputeRedundancy"),
        status=resp.get("Status"),
        publicly_accessible=resp.get("PubliclyAccessible"),
        endpoint=resp.get("Endpoint"),
        db_shard_group_arn=resp.get("DBShardGroupArn"),
        tag_list=resp.get("TagList"),
    )


def create_db_subnet_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    kwargs["DBSubnetGroupDescription"] = db_subnet_group_description
    kwargs["SubnetIds"] = subnet_ids
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_db_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create db subnet group") from exc
    return CreateDbSubnetGroupResult(
        db_subnet_group=resp.get("DBSubnetGroup"),
    )


def create_event_subscription(
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
    client = get_client("rds", region_name)
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
        resp = client.create_event_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create event subscription") from exc
    return CreateEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


def create_global_cluster(
    global_cluster_identifier: str,
    *,
    source_db_cluster_identifier: str | None = None,
    engine: str | None = None,
    engine_version: str | None = None,
    engine_lifecycle_support: str | None = None,
    deletion_protection: bool | None = None,
    database_name: str | None = None,
    storage_encrypted: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateGlobalClusterResult:
    """Create global cluster.

    Args:
        global_cluster_identifier: Global cluster identifier.
        source_db_cluster_identifier: Source db cluster identifier.
        engine: Engine.
        engine_version: Engine version.
        engine_lifecycle_support: Engine lifecycle support.
        deletion_protection: Deletion protection.
        database_name: Database name.
        storage_encrypted: Storage encrypted.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    if source_db_cluster_identifier is not None:
        kwargs["SourceDBClusterIdentifier"] = source_db_cluster_identifier
    if engine is not None:
        kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create global cluster") from exc
    return CreateGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def create_integration(
    source_arn: str,
    target_arn: str,
    integration_name: str,
    *,
    kms_key_id: str | None = None,
    additional_encryption_context: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    data_filter: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateIntegrationResult:
    """Create integration.

    Args:
        source_arn: Source arn.
        target_arn: Target arn.
        integration_name: Integration name.
        kms_key_id: Kms key id.
        additional_encryption_context: Additional encryption context.
        tags: Tags.
        data_filter: Data filter.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceArn"] = source_arn
    kwargs["TargetArn"] = target_arn
    kwargs["IntegrationName"] = integration_name
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    if additional_encryption_context is not None:
        kwargs["AdditionalEncryptionContext"] = additional_encryption_context
    if tags is not None:
        kwargs["Tags"] = tags
    if data_filter is not None:
        kwargs["DataFilter"] = data_filter
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.create_integration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create integration") from exc
    return CreateIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        status=resp.get("Status"),
        tags=resp.get("Tags"),
        data_filter=resp.get("DataFilter"),
        description=resp.get("Description"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
    )


def create_option_group(
    option_group_name: str,
    engine_name: str,
    major_engine_version: str,
    option_group_description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateOptionGroupResult:
    """Create option group.

    Args:
        option_group_name: Option group name.
        engine_name: Engine name.
        major_engine_version: Major engine version.
        option_group_description: Option group description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OptionGroupName"] = option_group_name
    kwargs["EngineName"] = engine_name
    kwargs["MajorEngineVersion"] = major_engine_version
    kwargs["OptionGroupDescription"] = option_group_description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_option_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create option group") from exc
    return CreateOptionGroupResult(
        option_group=resp.get("OptionGroup"),
    )


def create_tenant_database(
    db_instance_identifier: str,
    tenant_db_name: str,
    master_username: str,
    *,
    master_user_password: str | None = None,
    character_set_name: str | None = None,
    nchar_character_set_name: str | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTenantDatabaseResult:
    """Create tenant database.

    Args:
        db_instance_identifier: Db instance identifier.
        tenant_db_name: Tenant db name.
        master_username: Master username.
        master_user_password: Master user password.
        character_set_name: Character set name.
        nchar_character_set_name: Nchar character set name.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["TenantDBName"] = tenant_db_name
    kwargs["MasterUsername"] = master_username
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if character_set_name is not None:
        kwargs["CharacterSetName"] = character_set_name
    if nchar_character_set_name is not None:
        kwargs["NcharCharacterSetName"] = nchar_character_set_name
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_tenant_database(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create tenant database") from exc
    return CreateTenantDatabaseResult(
        tenant_database=resp.get("TenantDatabase"),
    )


def delete_blue_green_deployment(
    blue_green_deployment_identifier: str,
    *,
    delete_target: bool | None = None,
    region_name: str | None = None,
) -> DeleteBlueGreenDeploymentResult:
    """Delete blue green deployment.

    Args:
        blue_green_deployment_identifier: Blue green deployment identifier.
        delete_target: Delete target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueGreenDeploymentIdentifier"] = blue_green_deployment_identifier
    if delete_target is not None:
        kwargs["DeleteTarget"] = delete_target
    try:
        resp = client.delete_blue_green_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete blue green deployment") from exc
    return DeleteBlueGreenDeploymentResult(
        blue_green_deployment=resp.get("BlueGreenDeployment"),
    )


def delete_custom_db_engine_version(
    engine: str,
    engine_version: str,
    region_name: str | None = None,
) -> DeleteCustomDbEngineVersionResult:
    """Delete custom db engine version.

    Args:
        engine: Engine.
        engine_version: Engine version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    kwargs["EngineVersion"] = engine_version
    try:
        resp = client.delete_custom_db_engine_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete custom db engine version") from exc
    return DeleteCustomDbEngineVersionResult(
        engine=resp.get("Engine"),
        major_engine_version=resp.get("MajorEngineVersion"),
        engine_version=resp.get("EngineVersion"),
        database_installation_files_s3_bucket_name=resp.get(
            "DatabaseInstallationFilesS3BucketName"
        ),
        database_installation_files_s3_prefix=resp.get("DatabaseInstallationFilesS3Prefix"),
        custom_db_engine_version_manifest=resp.get("CustomDBEngineVersionManifest"),
        db_parameter_group_family=resp.get("DBParameterGroupFamily"),
        db_engine_description=resp.get("DBEngineDescription"),
        db_engine_version_arn=resp.get("DBEngineVersionArn"),
        db_engine_version_description=resp.get("DBEngineVersionDescription"),
        default_character_set=resp.get("DefaultCharacterSet"),
        image=resp.get("Image"),
        db_engine_media_type=resp.get("DBEngineMediaType"),
        kms_key_id=resp.get("KMSKeyId"),
        create_time=resp.get("CreateTime"),
        supported_character_sets=resp.get("SupportedCharacterSets"),
        supported_nchar_character_sets=resp.get("SupportedNcharCharacterSets"),
        valid_upgrade_target=resp.get("ValidUpgradeTarget"),
        supported_timezones=resp.get("SupportedTimezones"),
        exportable_log_types=resp.get("ExportableLogTypes"),
        supports_log_exports_to_cloudwatch_logs=resp.get("SupportsLogExportsToCloudwatchLogs"),
        supports_read_replica=resp.get("SupportsReadReplica"),
        supported_engine_modes=resp.get("SupportedEngineModes"),
        supported_feature_names=resp.get("SupportedFeatureNames"),
        status=resp.get("Status"),
        supports_parallel_query=resp.get("SupportsParallelQuery"),
        supports_global_databases=resp.get("SupportsGlobalDatabases"),
        tag_list=resp.get("TagList"),
        supports_babelfish=resp.get("SupportsBabelfish"),
        supports_limitless_database=resp.get("SupportsLimitlessDatabase"),
        supports_certificate_rotation_without_restart=resp.get(
            "SupportsCertificateRotationWithoutRestart"
        ),
        supported_ca_certificate_identifiers=resp.get("SupportedCACertificateIdentifiers"),
        supports_local_write_forwarding=resp.get("SupportsLocalWriteForwarding"),
        supports_integrations=resp.get("SupportsIntegrations"),
        serverless_v2_features_support=resp.get("ServerlessV2FeaturesSupport"),
    )


def delete_db_cluster(
    db_cluster_identifier: str,
    *,
    skip_final_snapshot: bool | None = None,
    final_db_snapshot_identifier: str | None = None,
    delete_automated_backups: bool | None = None,
    region_name: str | None = None,
) -> DeleteDbClusterResult:
    """Delete db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        skip_final_snapshot: Skip final snapshot.
        final_db_snapshot_identifier: Final db snapshot identifier.
        delete_automated_backups: Delete automated backups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if skip_final_snapshot is not None:
        kwargs["SkipFinalSnapshot"] = skip_final_snapshot
    if final_db_snapshot_identifier is not None:
        kwargs["FinalDBSnapshotIdentifier"] = final_db_snapshot_identifier
    if delete_automated_backups is not None:
        kwargs["DeleteAutomatedBackups"] = delete_automated_backups
    try:
        resp = client.delete_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster") from exc
    return DeleteDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def delete_db_cluster_automated_backup(
    db_cluster_resource_id: str,
    region_name: str | None = None,
) -> DeleteDbClusterAutomatedBackupResult:
    """Delete db cluster automated backup.

    Args:
        db_cluster_resource_id: Db cluster resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DbClusterResourceId"] = db_cluster_resource_id
    try:
        resp = client.delete_db_cluster_automated_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster automated backup") from exc
    return DeleteDbClusterAutomatedBackupResult(
        db_cluster_automated_backup=resp.get("DBClusterAutomatedBackup"),
    )


def delete_db_cluster_endpoint(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    try:
        resp = client.delete_db_cluster_endpoint(**kwargs)
    except ClientError as exc:
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


def delete_db_cluster_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    try:
        client.delete_db_cluster_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster parameter group") from exc
    return None


def delete_db_cluster_snapshot(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    try:
        resp = client.delete_db_cluster_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db cluster snapshot") from exc
    return DeleteDbClusterSnapshotResult(
        db_cluster_snapshot=resp.get("DBClusterSnapshot"),
    )


def delete_db_instance(
    db_instance_identifier: str,
    *,
    skip_final_snapshot: bool | None = None,
    final_db_snapshot_identifier: str | None = None,
    delete_automated_backups: bool | None = None,
    region_name: str | None = None,
) -> DeleteDbInstanceResult:
    """Delete db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        skip_final_snapshot: Skip final snapshot.
        final_db_snapshot_identifier: Final db snapshot identifier.
        delete_automated_backups: Delete automated backups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if skip_final_snapshot is not None:
        kwargs["SkipFinalSnapshot"] = skip_final_snapshot
    if final_db_snapshot_identifier is not None:
        kwargs["FinalDBSnapshotIdentifier"] = final_db_snapshot_identifier
    if delete_automated_backups is not None:
        kwargs["DeleteAutomatedBackups"] = delete_automated_backups
    try:
        resp = client.delete_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db instance") from exc
    return DeleteDbInstanceResult(
        db_instance=resp.get("DBInstance"),
    )


def delete_db_instance_automated_backup(
    *,
    dbi_resource_id: str | None = None,
    db_instance_automated_backups_arn: str | None = None,
    region_name: str | None = None,
) -> DeleteDbInstanceAutomatedBackupResult:
    """Delete db instance automated backup.

    Args:
        dbi_resource_id: Dbi resource id.
        db_instance_automated_backups_arn: Db instance automated backups arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if dbi_resource_id is not None:
        kwargs["DbiResourceId"] = dbi_resource_id
    if db_instance_automated_backups_arn is not None:
        kwargs["DBInstanceAutomatedBackupsArn"] = db_instance_automated_backups_arn
    try:
        resp = client.delete_db_instance_automated_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db instance automated backup") from exc
    return DeleteDbInstanceAutomatedBackupResult(
        db_instance_automated_backup=resp.get("DBInstanceAutomatedBackup"),
    )


def delete_db_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    try:
        client.delete_db_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db parameter group") from exc
    return None


def delete_db_proxy(
    db_proxy_name: str,
    region_name: str | None = None,
) -> DeleteDbProxyResult:
    """Delete db proxy.

    Args:
        db_proxy_name: Db proxy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    try:
        resp = client.delete_db_proxy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db proxy") from exc
    return DeleteDbProxyResult(
        db_proxy=resp.get("DBProxy"),
    )


def delete_db_proxy_endpoint(
    db_proxy_endpoint_name: str,
    region_name: str | None = None,
) -> DeleteDbProxyEndpointResult:
    """Delete db proxy endpoint.

    Args:
        db_proxy_endpoint_name: Db proxy endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyEndpointName"] = db_proxy_endpoint_name
    try:
        resp = client.delete_db_proxy_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db proxy endpoint") from exc
    return DeleteDbProxyEndpointResult(
        db_proxy_endpoint=resp.get("DBProxyEndpoint"),
    )


def delete_db_security_group(
    db_security_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete db security group.

    Args:
        db_security_group_name: Db security group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSecurityGroupName"] = db_security_group_name
    try:
        client.delete_db_security_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db security group") from exc
    return None


def delete_db_shard_group(
    db_shard_group_identifier: str,
    region_name: str | None = None,
) -> DeleteDbShardGroupResult:
    """Delete db shard group.

    Args:
        db_shard_group_identifier: Db shard group identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBShardGroupIdentifier"] = db_shard_group_identifier
    try:
        resp = client.delete_db_shard_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db shard group") from exc
    return DeleteDbShardGroupResult(
        db_shard_group_resource_id=resp.get("DBShardGroupResourceId"),
        db_shard_group_identifier=resp.get("DBShardGroupIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        max_acu=resp.get("MaxACU"),
        min_acu=resp.get("MinACU"),
        compute_redundancy=resp.get("ComputeRedundancy"),
        status=resp.get("Status"),
        publicly_accessible=resp.get("PubliclyAccessible"),
        endpoint=resp.get("Endpoint"),
        db_shard_group_arn=resp.get("DBShardGroupArn"),
        tag_list=resp.get("TagList"),
    )


def delete_db_subnet_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    try:
        client.delete_db_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete db subnet group") from exc
    return None


def delete_event_subscription(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    try:
        resp = client.delete_event_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete event subscription") from exc
    return DeleteEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


def delete_global_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    try:
        resp = client.delete_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete global cluster") from exc
    return DeleteGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def delete_integration(
    integration_identifier: str,
    region_name: str | None = None,
) -> DeleteIntegrationResult:
    """Delete integration.

    Args:
        integration_identifier: Integration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationIdentifier"] = integration_identifier
    try:
        resp = client.delete_integration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete integration") from exc
    return DeleteIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        status=resp.get("Status"),
        tags=resp.get("Tags"),
        data_filter=resp.get("DataFilter"),
        description=resp.get("Description"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
    )


def delete_option_group(
    option_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete option group.

    Args:
        option_group_name: Option group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OptionGroupName"] = option_group_name
    try:
        client.delete_option_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete option group") from exc
    return None


def delete_tenant_database(
    db_instance_identifier: str,
    tenant_db_name: str,
    *,
    skip_final_snapshot: bool | None = None,
    final_db_snapshot_identifier: str | None = None,
    region_name: str | None = None,
) -> DeleteTenantDatabaseResult:
    """Delete tenant database.

    Args:
        db_instance_identifier: Db instance identifier.
        tenant_db_name: Tenant db name.
        skip_final_snapshot: Skip final snapshot.
        final_db_snapshot_identifier: Final db snapshot identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["TenantDBName"] = tenant_db_name
    if skip_final_snapshot is not None:
        kwargs["SkipFinalSnapshot"] = skip_final_snapshot
    if final_db_snapshot_identifier is not None:
        kwargs["FinalDBSnapshotIdentifier"] = final_db_snapshot_identifier
    try:
        resp = client.delete_tenant_database(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete tenant database") from exc
    return DeleteTenantDatabaseResult(
        tenant_database=resp.get("TenantDatabase"),
    )


def deregister_db_proxy_targets(
    db_proxy_name: str,
    *,
    target_group_name: str | None = None,
    db_instance_identifiers: list[str] | None = None,
    db_cluster_identifiers: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Deregister db proxy targets.

    Args:
        db_proxy_name: Db proxy name.
        target_group_name: Target group name.
        db_instance_identifiers: Db instance identifiers.
        db_cluster_identifiers: Db cluster identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    if target_group_name is not None:
        kwargs["TargetGroupName"] = target_group_name
    if db_instance_identifiers is not None:
        kwargs["DBInstanceIdentifiers"] = db_instance_identifiers
    if db_cluster_identifiers is not None:
        kwargs["DBClusterIdentifiers"] = db_cluster_identifiers
    try:
        client.deregister_db_proxy_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister db proxy targets") from exc
    return None


def describe_account_attributes(
    region_name: str | None = None,
) -> DescribeAccountAttributesResult:
    """Describe account attributes.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_account_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account attributes") from exc
    return DescribeAccountAttributesResult(
        account_quotas=resp.get("AccountQuotas"),
    )


def describe_blue_green_deployments(
    *,
    blue_green_deployment_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeBlueGreenDeploymentsResult:
    """Describe blue green deployments.

    Args:
        blue_green_deployment_identifier: Blue green deployment identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if blue_green_deployment_identifier is not None:
        kwargs["BlueGreenDeploymentIdentifier"] = blue_green_deployment_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_blue_green_deployments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe blue green deployments") from exc
    return DescribeBlueGreenDeploymentsResult(
        blue_green_deployments=resp.get("BlueGreenDeployments"),
        marker=resp.get("Marker"),
    )


def describe_certificates(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_certificates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe certificates") from exc
    return DescribeCertificatesResult(
        default_certificate_for_new_launches=resp.get("DefaultCertificateForNewLaunches"),
        certificates=resp.get("Certificates"),
        marker=resp.get("Marker"),
    )


def describe_db_cluster_automated_backups(
    *,
    db_cluster_resource_id: str | None = None,
    db_cluster_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterAutomatedBackupsResult:
    """Describe db cluster automated backups.

    Args:
        db_cluster_resource_id: Db cluster resource id.
        db_cluster_identifier: Db cluster identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_resource_id is not None:
        kwargs["DbClusterResourceId"] = db_cluster_resource_id
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_db_cluster_automated_backups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster automated backups") from exc
    return DescribeDbClusterAutomatedBackupsResult(
        marker=resp.get("Marker"),
        db_cluster_automated_backups=resp.get("DBClusterAutomatedBackups"),
    )


def describe_db_cluster_backtracks(
    db_cluster_identifier: str,
    *,
    backtrack_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterBacktracksResult:
    """Describe db cluster backtracks.

    Args:
        db_cluster_identifier: Db cluster identifier.
        backtrack_identifier: Backtrack identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if backtrack_identifier is not None:
        kwargs["BacktrackIdentifier"] = backtrack_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_db_cluster_backtracks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster backtracks") from exc
    return DescribeDbClusterBacktracksResult(
        marker=resp.get("Marker"),
        db_cluster_backtracks=resp.get("DBClusterBacktracks"),
    )


def describe_db_cluster_endpoints(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_cluster_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster endpoints") from exc
    return DescribeDbClusterEndpointsResult(
        marker=resp.get("Marker"),
        db_cluster_endpoints=resp.get("DBClusterEndpoints"),
    )


def describe_db_cluster_parameter_groups(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_cluster_parameter_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster parameter groups") from exc
    return DescribeDbClusterParameterGroupsResult(
        marker=resp.get("Marker"),
        db_cluster_parameter_groups=resp.get("DBClusterParameterGroups"),
    )


def describe_db_cluster_parameters(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_cluster_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster parameters") from exc
    return DescribeDbClusterParametersResult(
        parameters=resp.get("Parameters"),
        marker=resp.get("Marker"),
    )


def describe_db_cluster_snapshot_attributes(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    try:
        resp = client.describe_db_cluster_snapshot_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster snapshot attributes") from exc
    return DescribeDbClusterSnapshotAttributesResult(
        db_cluster_snapshot_attributes_result=resp.get("DBClusterSnapshotAttributesResult"),
    )


def describe_db_cluster_snapshots(
    *,
    db_cluster_identifier: str | None = None,
    db_cluster_snapshot_identifier: str | None = None,
    snapshot_type: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    include_shared: bool | None = None,
    include_public: bool | None = None,
    db_cluster_resource_id: str | None = None,
    region_name: str | None = None,
) -> DescribeDbClusterSnapshotsResult:
    """Describe db cluster snapshots.

    Args:
        db_cluster_identifier: Db cluster identifier.
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        snapshot_type: Snapshot type.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        include_shared: Include shared.
        include_public: Include public.
        db_cluster_resource_id: Db cluster resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if db_cluster_snapshot_identifier is not None:
        kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    if snapshot_type is not None:
        kwargs["SnapshotType"] = snapshot_type
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if include_shared is not None:
        kwargs["IncludeShared"] = include_shared
    if include_public is not None:
        kwargs["IncludePublic"] = include_public
    if db_cluster_resource_id is not None:
        kwargs["DbClusterResourceId"] = db_cluster_resource_id
    try:
        resp = client.describe_db_cluster_snapshots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db cluster snapshots") from exc
    return DescribeDbClusterSnapshotsResult(
        marker=resp.get("Marker"),
        db_cluster_snapshots=resp.get("DBClusterSnapshots"),
    )


def describe_db_clusters(
    *,
    db_cluster_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    include_shared: bool | None = None,
    region_name: str | None = None,
) -> DescribeDbClustersResult:
    """Describe db clusters.

    Args:
        db_cluster_identifier: Db cluster identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        include_shared: Include shared.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_cluster_identifier is not None:
        kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if include_shared is not None:
        kwargs["IncludeShared"] = include_shared
    try:
        resp = client.describe_db_clusters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db clusters") from exc
    return DescribeDbClustersResult(
        marker=resp.get("Marker"),
        db_clusters=resp.get("DBClusters"),
    )


def describe_db_engine_versions(
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
    include_all: bool | None = None,
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
        include_all: Include all.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
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
    if include_all is not None:
        kwargs["IncludeAll"] = include_all
    try:
        resp = client.describe_db_engine_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db engine versions") from exc
    return DescribeDbEngineVersionsResult(
        marker=resp.get("Marker"),
        db_engine_versions=resp.get("DBEngineVersions"),
    )


def describe_db_instance_automated_backups(
    *,
    dbi_resource_id: str | None = None,
    db_instance_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    db_instance_automated_backups_arn: str | None = None,
    region_name: str | None = None,
) -> DescribeDbInstanceAutomatedBackupsResult:
    """Describe db instance automated backups.

    Args:
        dbi_resource_id: Dbi resource id.
        db_instance_identifier: Db instance identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        db_instance_automated_backups_arn: Db instance automated backups arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if dbi_resource_id is not None:
        kwargs["DbiResourceId"] = dbi_resource_id
    if db_instance_identifier is not None:
        kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if db_instance_automated_backups_arn is not None:
        kwargs["DBInstanceAutomatedBackupsArn"] = db_instance_automated_backups_arn
    try:
        resp = client.describe_db_instance_automated_backups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db instance automated backups") from exc
    return DescribeDbInstanceAutomatedBackupsResult(
        marker=resp.get("Marker"),
        db_instance_automated_backups=resp.get("DBInstanceAutomatedBackups"),
    )


def describe_db_log_files(
    db_instance_identifier: str,
    *,
    filename_contains: str | None = None,
    file_last_written: int | None = None,
    file_size: int | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbLogFilesResult:
    """Describe db log files.

    Args:
        db_instance_identifier: Db instance identifier.
        filename_contains: Filename contains.
        file_last_written: File last written.
        file_size: File size.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if filename_contains is not None:
        kwargs["FilenameContains"] = filename_contains
    if file_last_written is not None:
        kwargs["FileLastWritten"] = file_last_written
    if file_size is not None:
        kwargs["FileSize"] = file_size
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_db_log_files(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db log files") from exc
    return DescribeDbLogFilesResult(
        describe_db_log_files=resp.get("DescribeDBLogFiles"),
        marker=resp.get("Marker"),
    )


def describe_db_major_engine_versions(
    *,
    engine: str | None = None,
    major_engine_version: str | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbMajorEngineVersionsResult:
    """Describe db major engine versions.

    Args:
        engine: Engine.
        major_engine_version: Major engine version.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if engine is not None:
        kwargs["Engine"] = engine
    if major_engine_version is not None:
        kwargs["MajorEngineVersion"] = major_engine_version
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_major_engine_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db major engine versions") from exc
    return DescribeDbMajorEngineVersionsResult(
        db_major_engine_versions=resp.get("DBMajorEngineVersions"),
        marker=resp.get("Marker"),
    )


def describe_db_parameter_groups(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_parameter_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db parameter groups") from exc
    return DescribeDbParameterGroupsResult(
        marker=resp.get("Marker"),
        db_parameter_groups=resp.get("DBParameterGroups"),
    )


def describe_db_parameters(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db parameters") from exc
    return DescribeDbParametersResult(
        parameters=resp.get("Parameters"),
        marker=resp.get("Marker"),
    )


def describe_db_proxies(
    *,
    db_proxy_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbProxiesResult:
    """Describe db proxies.

    Args:
        db_proxy_name: Db proxy name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_proxy_name is not None:
        kwargs["DBProxyName"] = db_proxy_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_proxies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db proxies") from exc
    return DescribeDbProxiesResult(
        db_proxies=resp.get("DBProxies"),
        marker=resp.get("Marker"),
    )


def describe_db_proxy_endpoints(
    *,
    db_proxy_name: str | None = None,
    db_proxy_endpoint_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbProxyEndpointsResult:
    """Describe db proxy endpoints.

    Args:
        db_proxy_name: Db proxy name.
        db_proxy_endpoint_name: Db proxy endpoint name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_proxy_name is not None:
        kwargs["DBProxyName"] = db_proxy_name
    if db_proxy_endpoint_name is not None:
        kwargs["DBProxyEndpointName"] = db_proxy_endpoint_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_proxy_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db proxy endpoints") from exc
    return DescribeDbProxyEndpointsResult(
        db_proxy_endpoints=resp.get("DBProxyEndpoints"),
        marker=resp.get("Marker"),
    )


def describe_db_proxy_target_groups(
    db_proxy_name: str,
    *,
    target_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbProxyTargetGroupsResult:
    """Describe db proxy target groups.

    Args:
        db_proxy_name: Db proxy name.
        target_group_name: Target group name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    if target_group_name is not None:
        kwargs["TargetGroupName"] = target_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_proxy_target_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db proxy target groups") from exc
    return DescribeDbProxyTargetGroupsResult(
        target_groups=resp.get("TargetGroups"),
        marker=resp.get("Marker"),
    )


def describe_db_proxy_targets(
    db_proxy_name: str,
    *,
    target_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbProxyTargetsResult:
    """Describe db proxy targets.

    Args:
        db_proxy_name: Db proxy name.
        target_group_name: Target group name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    if target_group_name is not None:
        kwargs["TargetGroupName"] = target_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_proxy_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db proxy targets") from exc
    return DescribeDbProxyTargetsResult(
        targets=resp.get("Targets"),
        marker=resp.get("Marker"),
    )


def describe_db_recommendations(
    *,
    last_updated_after: str | None = None,
    last_updated_before: str | None = None,
    locale: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbRecommendationsResult:
    """Describe db recommendations.

    Args:
        last_updated_after: Last updated after.
        last_updated_before: Last updated before.
        locale: Locale.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if last_updated_after is not None:
        kwargs["LastUpdatedAfter"] = last_updated_after
    if last_updated_before is not None:
        kwargs["LastUpdatedBefore"] = last_updated_before
    if locale is not None:
        kwargs["Locale"] = locale
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_db_recommendations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db recommendations") from exc
    return DescribeDbRecommendationsResult(
        db_recommendations=resp.get("DBRecommendations"),
        marker=resp.get("Marker"),
    )


def describe_db_security_groups(
    *,
    db_security_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDbSecurityGroupsResult:
    """Describe db security groups.

    Args:
        db_security_group_name: Db security group name.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_security_group_name is not None:
        kwargs["DBSecurityGroupName"] = db_security_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_db_security_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db security groups") from exc
    return DescribeDbSecurityGroupsResult(
        marker=resp.get("Marker"),
        db_security_groups=resp.get("DBSecurityGroups"),
    )


def describe_db_shard_groups(
    *,
    db_shard_group_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeDbShardGroupsResult:
    """Describe db shard groups.

    Args:
        db_shard_group_identifier: Db shard group identifier.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_shard_group_identifier is not None:
        kwargs["DBShardGroupIdentifier"] = db_shard_group_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_db_shard_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db shard groups") from exc
    return DescribeDbShardGroupsResult(
        db_shard_groups=resp.get("DBShardGroups"),
        marker=resp.get("Marker"),
    )


def describe_db_snapshot_attributes(
    db_snapshot_identifier: str,
    region_name: str | None = None,
) -> DescribeDbSnapshotAttributesResult:
    """Describe db snapshot attributes.

    Args:
        db_snapshot_identifier: Db snapshot identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSnapshotIdentifier"] = db_snapshot_identifier
    try:
        resp = client.describe_db_snapshot_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db snapshot attributes") from exc
    return DescribeDbSnapshotAttributesResult(
        db_snapshot_attributes_result=resp.get("DBSnapshotAttributesResult"),
    )


def describe_db_snapshot_tenant_databases(
    *,
    db_instance_identifier: str | None = None,
    db_snapshot_identifier: str | None = None,
    snapshot_type: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    dbi_resource_id: str | None = None,
    region_name: str | None = None,
) -> DescribeDbSnapshotTenantDatabasesResult:
    """Describe db snapshot tenant databases.

    Args:
        db_instance_identifier: Db instance identifier.
        db_snapshot_identifier: Db snapshot identifier.
        snapshot_type: Snapshot type.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        dbi_resource_id: Dbi resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_instance_identifier is not None:
        kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if db_snapshot_identifier is not None:
        kwargs["DBSnapshotIdentifier"] = db_snapshot_identifier
    if snapshot_type is not None:
        kwargs["SnapshotType"] = snapshot_type
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if dbi_resource_id is not None:
        kwargs["DbiResourceId"] = dbi_resource_id
    try:
        resp = client.describe_db_snapshot_tenant_databases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db snapshot tenant databases") from exc
    return DescribeDbSnapshotTenantDatabasesResult(
        marker=resp.get("Marker"),
        db_snapshot_tenant_databases=resp.get("DBSnapshotTenantDatabases"),
    )


def describe_db_subnet_groups(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_db_subnet_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe db subnet groups") from exc
    return DescribeDbSubnetGroupsResult(
        marker=resp.get("Marker"),
        db_subnet_groups=resp.get("DBSubnetGroups"),
    )


def describe_engine_default_cluster_parameters(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_engine_default_cluster_parameters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe engine default cluster parameters") from exc
    return DescribeEngineDefaultClusterParametersResult(
        engine_defaults=resp.get("EngineDefaults"),
    )


def describe_engine_default_parameters(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupFamily"] = db_parameter_group_family
    if filters is not None:
        kwargs["Filters"] = filters
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


def describe_event_categories(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.describe_event_categories(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe event categories") from exc
    return DescribeEventCategoriesResult(
        event_categories_map_list=resp.get("EventCategoriesMapList"),
    )


def describe_event_subscriptions(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_event_subscriptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe event subscriptions") from exc
    return DescribeEventSubscriptionsResult(
        marker=resp.get("Marker"),
        event_subscriptions_list=resp.get("EventSubscriptionsList"),
    )


def describe_events(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        marker=resp.get("Marker"),
        events=resp.get("Events"),
    )


def describe_export_tasks(
    *,
    export_task_identifier: str | None = None,
    source_arn: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    source_type: str | None = None,
    region_name: str | None = None,
) -> DescribeExportTasksResult:
    """Describe export tasks.

    Args:
        export_task_identifier: Export task identifier.
        source_arn: Source arn.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        source_type: Source type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if export_task_identifier is not None:
        kwargs["ExportTaskIdentifier"] = export_task_identifier
    if source_arn is not None:
        kwargs["SourceArn"] = source_arn
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if source_type is not None:
        kwargs["SourceType"] = source_type
    try:
        resp = client.describe_export_tasks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe export tasks") from exc
    return DescribeExportTasksResult(
        marker=resp.get("Marker"),
        export_tasks=resp.get("ExportTasks"),
    )


def describe_global_clusters(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_global_clusters(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe global clusters") from exc
    return DescribeGlobalClustersResult(
        marker=resp.get("Marker"),
        global_clusters=resp.get("GlobalClusters"),
    )


def describe_integrations(
    *,
    integration_identifier: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeIntegrationsResult:
    """Describe integrations.

    Args:
        integration_identifier: Integration identifier.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if integration_identifier is not None:
        kwargs["IntegrationIdentifier"] = integration_identifier
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_integrations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe integrations") from exc
    return DescribeIntegrationsResult(
        marker=resp.get("Marker"),
        integrations=resp.get("Integrations"),
    )


def describe_option_group_options(
    engine_name: str,
    *,
    major_engine_version: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeOptionGroupOptionsResult:
    """Describe option group options.

    Args:
        engine_name: Engine name.
        major_engine_version: Major engine version.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EngineName"] = engine_name
    if major_engine_version is not None:
        kwargs["MajorEngineVersion"] = major_engine_version
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_option_group_options(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe option group options") from exc
    return DescribeOptionGroupOptionsResult(
        option_group_options=resp.get("OptionGroupOptions"),
        marker=resp.get("Marker"),
    )


def describe_option_groups(
    *,
    option_group_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    engine_name: str | None = None,
    major_engine_version: str | None = None,
    region_name: str | None = None,
) -> DescribeOptionGroupsResult:
    """Describe option groups.

    Args:
        option_group_name: Option group name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        engine_name: Engine name.
        major_engine_version: Major engine version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if engine_name is not None:
        kwargs["EngineName"] = engine_name
    if major_engine_version is not None:
        kwargs["MajorEngineVersion"] = major_engine_version
    try:
        resp = client.describe_option_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe option groups") from exc
    return DescribeOptionGroupsResult(
        option_groups_list=resp.get("OptionGroupsList"),
        marker=resp.get("Marker"),
    )


def describe_orderable_db_instance_options(
    engine: str,
    *,
    engine_version: str | None = None,
    db_instance_class: str | None = None,
    license_model: str | None = None,
    availability_zone_group: str | None = None,
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
        availability_zone_group: Availability zone group.
        vpc: Vpc.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if availability_zone_group is not None:
        kwargs["AvailabilityZoneGroup"] = availability_zone_group
    if vpc is not None:
        kwargs["Vpc"] = vpc
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_orderable_db_instance_options(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe orderable db instance options") from exc
    return DescribeOrderableDbInstanceOptionsResult(
        orderable_db_instance_options=resp.get("OrderableDBInstanceOptions"),
        marker=resp.get("Marker"),
    )


def describe_pending_maintenance_actions(
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
    client = get_client("rds", region_name)
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
        resp = client.describe_pending_maintenance_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pending maintenance actions") from exc
    return DescribePendingMaintenanceActionsResult(
        pending_maintenance_actions=resp.get("PendingMaintenanceActions"),
        marker=resp.get("Marker"),
    )


def describe_reserved_db_instances(
    *,
    reserved_db_instance_id: str | None = None,
    reserved_db_instances_offering_id: str | None = None,
    db_instance_class: str | None = None,
    duration: str | None = None,
    product_description: str | None = None,
    offering_type: str | None = None,
    multi_az: bool | None = None,
    lease_id: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedDbInstancesResult:
    """Describe reserved db instances.

    Args:
        reserved_db_instance_id: Reserved db instance id.
        reserved_db_instances_offering_id: Reserved db instances offering id.
        db_instance_class: Db instance class.
        duration: Duration.
        product_description: Product description.
        offering_type: Offering type.
        multi_az: Multi az.
        lease_id: Lease id.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_db_instance_id is not None:
        kwargs["ReservedDBInstanceId"] = reserved_db_instance_id
    if reserved_db_instances_offering_id is not None:
        kwargs["ReservedDBInstancesOfferingId"] = reserved_db_instances_offering_id
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if duration is not None:
        kwargs["Duration"] = duration
    if product_description is not None:
        kwargs["ProductDescription"] = product_description
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if lease_id is not None:
        kwargs["LeaseId"] = lease_id
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_reserved_db_instances(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved db instances") from exc
    return DescribeReservedDbInstancesResult(
        marker=resp.get("Marker"),
        reserved_db_instances=resp.get("ReservedDBInstances"),
    )


def describe_reserved_db_instances_offerings(
    *,
    reserved_db_instances_offering_id: str | None = None,
    db_instance_class: str | None = None,
    duration: str | None = None,
    product_description: str | None = None,
    offering_type: str | None = None,
    multi_az: bool | None = None,
    filters: list[dict[str, Any]] | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedDbInstancesOfferingsResult:
    """Describe reserved db instances offerings.

    Args:
        reserved_db_instances_offering_id: Reserved db instances offering id.
        db_instance_class: Db instance class.
        duration: Duration.
        product_description: Product description.
        offering_type: Offering type.
        multi_az: Multi az.
        filters: Filters.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_db_instances_offering_id is not None:
        kwargs["ReservedDBInstancesOfferingId"] = reserved_db_instances_offering_id
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if duration is not None:
        kwargs["Duration"] = duration
    if product_description is not None:
        kwargs["ProductDescription"] = product_description
    if offering_type is not None:
        kwargs["OfferingType"] = offering_type
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if filters is not None:
        kwargs["Filters"] = filters
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = client.describe_reserved_db_instances_offerings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved db instances offerings") from exc
    return DescribeReservedDbInstancesOfferingsResult(
        marker=resp.get("Marker"),
        reserved_db_instances_offerings=resp.get("ReservedDBInstancesOfferings"),
    )


def describe_source_regions(
    *,
    target_region_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeSourceRegionsResult:
    """Describe source regions.

    Args:
        target_region_name: Target region name.
        max_records: Max records.
        marker: Marker.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if target_region_name is not None:
        kwargs["RegionName"] = target_region_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.describe_source_regions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe source regions") from exc
    return DescribeSourceRegionsResult(
        marker=resp.get("Marker"),
        source_regions=resp.get("SourceRegions"),
    )


def describe_tenant_databases(
    *,
    db_instance_identifier: str | None = None,
    tenant_db_name: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeTenantDatabasesResult:
    """Describe tenant databases.

    Args:
        db_instance_identifier: Db instance identifier.
        tenant_db_name: Tenant db name.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if db_instance_identifier is not None:
        kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if tenant_db_name is not None:
        kwargs["TenantDBName"] = tenant_db_name
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = client.describe_tenant_databases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe tenant databases") from exc
    return DescribeTenantDatabasesResult(
        marker=resp.get("Marker"),
        tenant_databases=resp.get("TenantDatabases"),
    )


def describe_valid_db_instance_modifications(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    try:
        resp = client.describe_valid_db_instance_modifications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe valid db instance modifications") from exc
    return DescribeValidDbInstanceModificationsResult(
        valid_db_instance_modifications_message=resp.get("ValidDBInstanceModificationsMessage"),
    )


def disable_http_endpoint(
    resource_arn: str,
    region_name: str | None = None,
) -> DisableHttpEndpointResult:
    """Disable http endpoint.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.disable_http_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable http endpoint") from exc
    return DisableHttpEndpointResult(
        resource_arn=resp.get("ResourceArn"),
        http_endpoint_enabled=resp.get("HttpEndpointEnabled"),
    )


def download_db_log_file_portion(
    db_instance_identifier: str,
    log_file_name: str,
    *,
    marker: str | None = None,
    number_of_lines: int | None = None,
    region_name: str | None = None,
) -> DownloadDbLogFilePortionResult:
    """Download db log file portion.

    Args:
        db_instance_identifier: Db instance identifier.
        log_file_name: Log file name.
        marker: Marker.
        number_of_lines: Number of lines.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["LogFileName"] = log_file_name
    if marker is not None:
        kwargs["Marker"] = marker
    if number_of_lines is not None:
        kwargs["NumberOfLines"] = number_of_lines
    try:
        resp = client.download_db_log_file_portion(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to download db log file portion") from exc
    return DownloadDbLogFilePortionResult(
        log_file_data=resp.get("LogFileData"),
        marker=resp.get("Marker"),
        additional_data_pending=resp.get("AdditionalDataPending"),
    )


def enable_http_endpoint(
    resource_arn: str,
    region_name: str | None = None,
) -> EnableHttpEndpointResult:
    """Enable http endpoint.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.enable_http_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable http endpoint") from exc
    return EnableHttpEndpointResult(
        resource_arn=resp.get("ResourceArn"),
        http_endpoint_enabled=resp.get("HttpEndpointEnabled"),
    )


def failover_db_cluster(
    db_cluster_identifier: str,
    *,
    target_db_instance_identifier: str | None = None,
    region_name: str | None = None,
) -> FailoverDbClusterResult:
    """Failover db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        target_db_instance_identifier: Target db instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if target_db_instance_identifier is not None:
        kwargs["TargetDBInstanceIdentifier"] = target_db_instance_identifier
    try:
        resp = client.failover_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to failover db cluster") from exc
    return FailoverDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def failover_global_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["TargetDbClusterIdentifier"] = target_db_cluster_identifier
    if allow_data_loss is not None:
        kwargs["AllowDataLoss"] = allow_data_loss
    if switchover is not None:
        kwargs["Switchover"] = switchover
    try:
        resp = client.failover_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to failover global cluster") from exc
    return FailoverGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def list_tags_for_resource(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tag_list=resp.get("TagList"),
    )


def modify_activity_stream(
    *,
    resource_arn: str | None = None,
    audit_policy_state: str | None = None,
    region_name: str | None = None,
) -> ModifyActivityStreamResult:
    """Modify activity stream.

    Args:
        resource_arn: Resource arn.
        audit_policy_state: Audit policy state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if resource_arn is not None:
        kwargs["ResourceArn"] = resource_arn
    if audit_policy_state is not None:
        kwargs["AuditPolicyState"] = audit_policy_state
    try:
        resp = client.modify_activity_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify activity stream") from exc
    return ModifyActivityStreamResult(
        kms_key_id=resp.get("KmsKeyId"),
        kinesis_stream_name=resp.get("KinesisStreamName"),
        status=resp.get("Status"),
        mode=resp.get("Mode"),
        engine_native_audit_fields_included=resp.get("EngineNativeAuditFieldsIncluded"),
        policy_status=resp.get("PolicyStatus"),
    )


def modify_certificates(
    *,
    certificate_identifier: str | None = None,
    remove_customer_override: bool | None = None,
    region_name: str | None = None,
) -> ModifyCertificatesResult:
    """Modify certificates.

    Args:
        certificate_identifier: Certificate identifier.
        remove_customer_override: Remove customer override.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    if certificate_identifier is not None:
        kwargs["CertificateIdentifier"] = certificate_identifier
    if remove_customer_override is not None:
        kwargs["RemoveCustomerOverride"] = remove_customer_override
    try:
        resp = client.modify_certificates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify certificates") from exc
    return ModifyCertificatesResult(
        certificate=resp.get("Certificate"),
    )


def modify_current_db_cluster_capacity(
    db_cluster_identifier: str,
    *,
    capacity: int | None = None,
    seconds_before_timeout: int | None = None,
    timeout_action: str | None = None,
    region_name: str | None = None,
) -> ModifyCurrentDbClusterCapacityResult:
    """Modify current db cluster capacity.

    Args:
        db_cluster_identifier: Db cluster identifier.
        capacity: Capacity.
        seconds_before_timeout: Seconds before timeout.
        timeout_action: Timeout action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if capacity is not None:
        kwargs["Capacity"] = capacity
    if seconds_before_timeout is not None:
        kwargs["SecondsBeforeTimeout"] = seconds_before_timeout
    if timeout_action is not None:
        kwargs["TimeoutAction"] = timeout_action
    try:
        resp = client.modify_current_db_cluster_capacity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify current db cluster capacity") from exc
    return ModifyCurrentDbClusterCapacityResult(
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        pending_capacity=resp.get("PendingCapacity"),
        current_capacity=resp.get("CurrentCapacity"),
        seconds_before_timeout=resp.get("SecondsBeforeTimeout"),
        timeout_action=resp.get("TimeoutAction"),
    )


def modify_custom_db_engine_version(
    engine: str,
    engine_version: str,
    *,
    description: str | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> ModifyCustomDbEngineVersionResult:
    """Modify custom db engine version.

    Args:
        engine: Engine.
        engine_version: Engine version.
        description: Description.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Engine"] = engine
    kwargs["EngineVersion"] = engine_version
    if description is not None:
        kwargs["Description"] = description
    if status is not None:
        kwargs["Status"] = status
    try:
        resp = client.modify_custom_db_engine_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify custom db engine version") from exc
    return ModifyCustomDbEngineVersionResult(
        engine=resp.get("Engine"),
        major_engine_version=resp.get("MajorEngineVersion"),
        engine_version=resp.get("EngineVersion"),
        database_installation_files_s3_bucket_name=resp.get(
            "DatabaseInstallationFilesS3BucketName"
        ),
        database_installation_files_s3_prefix=resp.get("DatabaseInstallationFilesS3Prefix"),
        custom_db_engine_version_manifest=resp.get("CustomDBEngineVersionManifest"),
        db_parameter_group_family=resp.get("DBParameterGroupFamily"),
        db_engine_description=resp.get("DBEngineDescription"),
        db_engine_version_arn=resp.get("DBEngineVersionArn"),
        db_engine_version_description=resp.get("DBEngineVersionDescription"),
        default_character_set=resp.get("DefaultCharacterSet"),
        image=resp.get("Image"),
        db_engine_media_type=resp.get("DBEngineMediaType"),
        kms_key_id=resp.get("KMSKeyId"),
        create_time=resp.get("CreateTime"),
        supported_character_sets=resp.get("SupportedCharacterSets"),
        supported_nchar_character_sets=resp.get("SupportedNcharCharacterSets"),
        valid_upgrade_target=resp.get("ValidUpgradeTarget"),
        supported_timezones=resp.get("SupportedTimezones"),
        exportable_log_types=resp.get("ExportableLogTypes"),
        supports_log_exports_to_cloudwatch_logs=resp.get("SupportsLogExportsToCloudwatchLogs"),
        supports_read_replica=resp.get("SupportsReadReplica"),
        supported_engine_modes=resp.get("SupportedEngineModes"),
        supported_feature_names=resp.get("SupportedFeatureNames"),
        status=resp.get("Status"),
        supports_parallel_query=resp.get("SupportsParallelQuery"),
        supports_global_databases=resp.get("SupportsGlobalDatabases"),
        tag_list=resp.get("TagList"),
        supports_babelfish=resp.get("SupportsBabelfish"),
        supports_limitless_database=resp.get("SupportsLimitlessDatabase"),
        supports_certificate_rotation_without_restart=resp.get(
            "SupportsCertificateRotationWithoutRestart"
        ),
        supported_ca_certificate_identifiers=resp.get("SupportedCACertificateIdentifiers"),
        supports_local_write_forwarding=resp.get("SupportsLocalWriteForwarding"),
        supports_integrations=resp.get("SupportsIntegrations"),
        serverless_v2_features_support=resp.get("ServerlessV2FeaturesSupport"),
    )


def modify_db_cluster(
    db_cluster_identifier: str,
    *,
    new_db_cluster_identifier: str | None = None,
    apply_immediately: bool | None = None,
    backup_retention_period: int | None = None,
    db_cluster_parameter_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    port: int | None = None,
    master_user_password: str | None = None,
    option_group_name: str | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    backtrack_window: int | None = None,
    cloudwatch_logs_export_configuration: dict[str, Any] | None = None,
    engine_version: str | None = None,
    allow_major_version_upgrade: bool | None = None,
    db_instance_parameter_group_name: str | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    deletion_protection: bool | None = None,
    enable_http_endpoint: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    enable_global_write_forwarding: bool | None = None,
    db_cluster_instance_class: str | None = None,
    allocated_storage: int | None = None,
    storage_type: str | None = None,
    iops: int | None = None,
    auto_minor_version_upgrade: bool | None = None,
    network_type: str | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    manage_master_user_password: bool | None = None,
    rotate_master_user_password: bool | None = None,
    enable_local_write_forwarding: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    engine_mode: str | None = None,
    allow_engine_mode_change: bool | None = None,
    aws_backup_recovery_point_arn: str | None = None,
    enable_limitless_database: bool | None = None,
    ca_certificate_identifier: str | None = None,
    master_user_authentication_type: str | None = None,
    region_name: str | None = None,
) -> ModifyDbClusterResult:
    """Modify db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        new_db_cluster_identifier: New db cluster identifier.
        apply_immediately: Apply immediately.
        backup_retention_period: Backup retention period.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        vpc_security_group_ids: Vpc security group ids.
        port: Port.
        master_user_password: Master user password.
        option_group_name: Option group name.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        enable_iam_database_authentication: Enable iam database authentication.
        backtrack_window: Backtrack window.
        cloudwatch_logs_export_configuration: Cloudwatch logs export configuration.
        engine_version: Engine version.
        allow_major_version_upgrade: Allow major version upgrade.
        db_instance_parameter_group_name: Db instance parameter group name.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        scaling_configuration: Scaling configuration.
        deletion_protection: Deletion protection.
        enable_http_endpoint: Enable http endpoint.
        copy_tags_to_snapshot: Copy tags to snapshot.
        enable_global_write_forwarding: Enable global write forwarding.
        db_cluster_instance_class: Db cluster instance class.
        allocated_storage: Allocated storage.
        storage_type: Storage type.
        iops: Iops.
        auto_minor_version_upgrade: Auto minor version upgrade.
        network_type: Network type.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        manage_master_user_password: Manage master user password.
        rotate_master_user_password: Rotate master user password.
        enable_local_write_forwarding: Enable local write forwarding.
        master_user_secret_kms_key_id: Master user secret kms key id.
        engine_mode: Engine mode.
        allow_engine_mode_change: Allow engine mode change.
        aws_backup_recovery_point_arn: Aws backup recovery point arn.
        enable_limitless_database: Enable limitless database.
        ca_certificate_identifier: Ca certificate identifier.
        master_user_authentication_type: Master user authentication type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if new_db_cluster_identifier is not None:
        kwargs["NewDBClusterIdentifier"] = new_db_cluster_identifier
    if apply_immediately is not None:
        kwargs["ApplyImmediately"] = apply_immediately
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if port is not None:
        kwargs["Port"] = port
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if backtrack_window is not None:
        kwargs["BacktrackWindow"] = backtrack_window
    if cloudwatch_logs_export_configuration is not None:
        kwargs["CloudwatchLogsExportConfiguration"] = cloudwatch_logs_export_configuration
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if allow_major_version_upgrade is not None:
        kwargs["AllowMajorVersionUpgrade"] = allow_major_version_upgrade
    if db_instance_parameter_group_name is not None:
        kwargs["DBInstanceParameterGroupName"] = db_instance_parameter_group_name
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if scaling_configuration is not None:
        kwargs["ScalingConfiguration"] = scaling_configuration
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if enable_http_endpoint is not None:
        kwargs["EnableHttpEndpoint"] = enable_http_endpoint
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if enable_global_write_forwarding is not None:
        kwargs["EnableGlobalWriteForwarding"] = enable_global_write_forwarding
    if db_cluster_instance_class is not None:
        kwargs["DBClusterInstanceClass"] = db_cluster_instance_class
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if iops is not None:
        kwargs["Iops"] = iops
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if rotate_master_user_password is not None:
        kwargs["RotateMasterUserPassword"] = rotate_master_user_password
    if enable_local_write_forwarding is not None:
        kwargs["EnableLocalWriteForwarding"] = enable_local_write_forwarding
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if engine_mode is not None:
        kwargs["EngineMode"] = engine_mode
    if allow_engine_mode_change is not None:
        kwargs["AllowEngineModeChange"] = allow_engine_mode_change
    if aws_backup_recovery_point_arn is not None:
        kwargs["AwsBackupRecoveryPointArn"] = aws_backup_recovery_point_arn
    if enable_limitless_database is not None:
        kwargs["EnableLimitlessDatabase"] = enable_limitless_database
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if master_user_authentication_type is not None:
        kwargs["MasterUserAuthenticationType"] = master_user_authentication_type
    try:
        resp = client.modify_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster") from exc
    return ModifyDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def modify_db_cluster_endpoint(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterEndpointIdentifier"] = db_cluster_endpoint_identifier
    if endpoint_type is not None:
        kwargs["EndpointType"] = endpoint_type
    if static_members is not None:
        kwargs["StaticMembers"] = static_members
    if excluded_members is not None:
        kwargs["ExcludedMembers"] = excluded_members
    try:
        resp = client.modify_db_cluster_endpoint(**kwargs)
    except ClientError as exc:
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


def modify_db_cluster_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    kwargs["Parameters"] = parameters
    try:
        resp = client.modify_db_cluster_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster parameter group") from exc
    return ModifyDbClusterParameterGroupResult(
        db_cluster_parameter_group_name=resp.get("DBClusterParameterGroupName"),
    )


def modify_db_cluster_snapshot_attribute(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    kwargs["AttributeName"] = attribute_name
    if values_to_add is not None:
        kwargs["ValuesToAdd"] = values_to_add
    if values_to_remove is not None:
        kwargs["ValuesToRemove"] = values_to_remove
    try:
        resp = client.modify_db_cluster_snapshot_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db cluster snapshot attribute") from exc
    return ModifyDbClusterSnapshotAttributeResult(
        db_cluster_snapshot_attributes_result=resp.get("DBClusterSnapshotAttributesResult"),
    )


def modify_db_instance(
    db_instance_identifier: str,
    *,
    allocated_storage: int | None = None,
    db_instance_class: str | None = None,
    db_subnet_group_name: str | None = None,
    db_security_groups: list[str] | None = None,
    vpc_security_group_ids: list[str] | None = None,
    apply_immediately: bool | None = None,
    master_user_password: str | None = None,
    db_parameter_group_name: str | None = None,
    backup_retention_period: int | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    multi_az: bool | None = None,
    engine_version: str | None = None,
    allow_major_version_upgrade: bool | None = None,
    auto_minor_version_upgrade: bool | None = None,
    license_model: str | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    new_db_instance_identifier: str | None = None,
    storage_type: str | None = None,
    tde_credential_arn: str | None = None,
    tde_credential_password: str | None = None,
    ca_certificate_identifier: str | None = None,
    domain: str | None = None,
    domain_fqdn: str | None = None,
    domain_ou: str | None = None,
    domain_auth_secret_arn: str | None = None,
    domain_dns_ips: list[str] | None = None,
    disable_domain: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    monitoring_interval: int | None = None,
    db_port_number: int | None = None,
    publicly_accessible: bool | None = None,
    monitoring_role_arn: str | None = None,
    domain_iam_role_name: str | None = None,
    promotion_tier: int | None = None,
    enable_iam_database_authentication: bool | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    cloudwatch_logs_export_configuration: dict[str, Any] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    use_default_processor_features: bool | None = None,
    deletion_protection: bool | None = None,
    max_allocated_storage: int | None = None,
    certificate_rotation_restart: bool | None = None,
    replica_mode: str | None = None,
    automation_mode: str | None = None,
    resume_full_automation_mode_minutes: int | None = None,
    enable_customer_owned_ip: bool | None = None,
    network_type: str | None = None,
    aws_backup_recovery_point_arn: str | None = None,
    manage_master_user_password: bool | None = None,
    rotate_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    multi_tenant: bool | None = None,
    dedicated_log_volume: bool | None = None,
    engine: str | None = None,
    master_user_authentication_type: str | None = None,
    region_name: str | None = None,
) -> ModifyDbInstanceResult:
    """Modify db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        allocated_storage: Allocated storage.
        db_instance_class: Db instance class.
        db_subnet_group_name: Db subnet group name.
        db_security_groups: Db security groups.
        vpc_security_group_ids: Vpc security group ids.
        apply_immediately: Apply immediately.
        master_user_password: Master user password.
        db_parameter_group_name: Db parameter group name.
        backup_retention_period: Backup retention period.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        multi_az: Multi az.
        engine_version: Engine version.
        allow_major_version_upgrade: Allow major version upgrade.
        auto_minor_version_upgrade: Auto minor version upgrade.
        license_model: License model.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        new_db_instance_identifier: New db instance identifier.
        storage_type: Storage type.
        tde_credential_arn: Tde credential arn.
        tde_credential_password: Tde credential password.
        ca_certificate_identifier: Ca certificate identifier.
        domain: Domain.
        domain_fqdn: Domain fqdn.
        domain_ou: Domain ou.
        domain_auth_secret_arn: Domain auth secret arn.
        domain_dns_ips: Domain dns ips.
        disable_domain: Disable domain.
        copy_tags_to_snapshot: Copy tags to snapshot.
        monitoring_interval: Monitoring interval.
        db_port_number: Db port number.
        publicly_accessible: Publicly accessible.
        monitoring_role_arn: Monitoring role arn.
        domain_iam_role_name: Domain iam role name.
        promotion_tier: Promotion tier.
        enable_iam_database_authentication: Enable iam database authentication.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        cloudwatch_logs_export_configuration: Cloudwatch logs export configuration.
        processor_features: Processor features.
        use_default_processor_features: Use default processor features.
        deletion_protection: Deletion protection.
        max_allocated_storage: Max allocated storage.
        certificate_rotation_restart: Certificate rotation restart.
        replica_mode: Replica mode.
        automation_mode: Automation mode.
        resume_full_automation_mode_minutes: Resume full automation mode minutes.
        enable_customer_owned_ip: Enable customer owned ip.
        network_type: Network type.
        aws_backup_recovery_point_arn: Aws backup recovery point arn.
        manage_master_user_password: Manage master user password.
        rotate_master_user_password: Rotate master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        multi_tenant: Multi tenant.
        dedicated_log_volume: Dedicated log volume.
        engine: Engine.
        master_user_authentication_type: Master user authentication type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if db_security_groups is not None:
        kwargs["DBSecurityGroups"] = db_security_groups
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if apply_immediately is not None:
        kwargs["ApplyImmediately"] = apply_immediately
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if allow_major_version_upgrade is not None:
        kwargs["AllowMajorVersionUpgrade"] = allow_major_version_upgrade
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if new_db_instance_identifier is not None:
        kwargs["NewDBInstanceIdentifier"] = new_db_instance_identifier
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if tde_credential_arn is not None:
        kwargs["TdeCredentialArn"] = tde_credential_arn
    if tde_credential_password is not None:
        kwargs["TdeCredentialPassword"] = tde_credential_password
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_fqdn is not None:
        kwargs["DomainFqdn"] = domain_fqdn
    if domain_ou is not None:
        kwargs["DomainOu"] = domain_ou
    if domain_auth_secret_arn is not None:
        kwargs["DomainAuthSecretArn"] = domain_auth_secret_arn
    if domain_dns_ips is not None:
        kwargs["DomainDnsIps"] = domain_dns_ips
    if disable_domain is not None:
        kwargs["DisableDomain"] = disable_domain
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if db_port_number is not None:
        kwargs["DBPortNumber"] = db_port_number
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if promotion_tier is not None:
        kwargs["PromotionTier"] = promotion_tier
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if cloudwatch_logs_export_configuration is not None:
        kwargs["CloudwatchLogsExportConfiguration"] = cloudwatch_logs_export_configuration
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if use_default_processor_features is not None:
        kwargs["UseDefaultProcessorFeatures"] = use_default_processor_features
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if max_allocated_storage is not None:
        kwargs["MaxAllocatedStorage"] = max_allocated_storage
    if certificate_rotation_restart is not None:
        kwargs["CertificateRotationRestart"] = certificate_rotation_restart
    if replica_mode is not None:
        kwargs["ReplicaMode"] = replica_mode
    if automation_mode is not None:
        kwargs["AutomationMode"] = automation_mode
    if resume_full_automation_mode_minutes is not None:
        kwargs["ResumeFullAutomationModeMinutes"] = resume_full_automation_mode_minutes
    if enable_customer_owned_ip is not None:
        kwargs["EnableCustomerOwnedIp"] = enable_customer_owned_ip
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if aws_backup_recovery_point_arn is not None:
        kwargs["AwsBackupRecoveryPointArn"] = aws_backup_recovery_point_arn
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if rotate_master_user_password is not None:
        kwargs["RotateMasterUserPassword"] = rotate_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if multi_tenant is not None:
        kwargs["MultiTenant"] = multi_tenant
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if engine is not None:
        kwargs["Engine"] = engine
    if master_user_authentication_type is not None:
        kwargs["MasterUserAuthenticationType"] = master_user_authentication_type
    try:
        resp = client.modify_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db instance") from exc
    return ModifyDbInstanceResult(
        db_instance=resp.get("DBInstance"),
    )


def modify_db_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    kwargs["Parameters"] = parameters
    try:
        resp = client.modify_db_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db parameter group") from exc
    return ModifyDbParameterGroupResult(
        db_parameter_group_name=resp.get("DBParameterGroupName"),
    )


def modify_db_proxy(
    db_proxy_name: str,
    *,
    new_db_proxy_name: str | None = None,
    default_auth_scheme: str | None = None,
    auth: list[dict[str, Any]] | None = None,
    require_tls: bool | None = None,
    idle_client_timeout: int | None = None,
    debug_logging: bool | None = None,
    role_arn: str | None = None,
    security_groups: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyDbProxyResult:
    """Modify db proxy.

    Args:
        db_proxy_name: Db proxy name.
        new_db_proxy_name: New db proxy name.
        default_auth_scheme: Default auth scheme.
        auth: Auth.
        require_tls: Require tls.
        idle_client_timeout: Idle client timeout.
        debug_logging: Debug logging.
        role_arn: Role arn.
        security_groups: Security groups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    if new_db_proxy_name is not None:
        kwargs["NewDBProxyName"] = new_db_proxy_name
    if default_auth_scheme is not None:
        kwargs["DefaultAuthScheme"] = default_auth_scheme
    if auth is not None:
        kwargs["Auth"] = auth
    if require_tls is not None:
        kwargs["RequireTLS"] = require_tls
    if idle_client_timeout is not None:
        kwargs["IdleClientTimeout"] = idle_client_timeout
    if debug_logging is not None:
        kwargs["DebugLogging"] = debug_logging
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    if security_groups is not None:
        kwargs["SecurityGroups"] = security_groups
    try:
        resp = client.modify_db_proxy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db proxy") from exc
    return ModifyDbProxyResult(
        db_proxy=resp.get("DBProxy"),
    )


def modify_db_proxy_endpoint(
    db_proxy_endpoint_name: str,
    *,
    new_db_proxy_endpoint_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyDbProxyEndpointResult:
    """Modify db proxy endpoint.

    Args:
        db_proxy_endpoint_name: Db proxy endpoint name.
        new_db_proxy_endpoint_name: New db proxy endpoint name.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyEndpointName"] = db_proxy_endpoint_name
    if new_db_proxy_endpoint_name is not None:
        kwargs["NewDBProxyEndpointName"] = new_db_proxy_endpoint_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = client.modify_db_proxy_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db proxy endpoint") from exc
    return ModifyDbProxyEndpointResult(
        db_proxy_endpoint=resp.get("DBProxyEndpoint"),
    )


def modify_db_proxy_target_group(
    target_group_name: str,
    db_proxy_name: str,
    *,
    connection_pool_config: dict[str, Any] | None = None,
    new_name: str | None = None,
    region_name: str | None = None,
) -> ModifyDbProxyTargetGroupResult:
    """Modify db proxy target group.

    Args:
        target_group_name: Target group name.
        db_proxy_name: Db proxy name.
        connection_pool_config: Connection pool config.
        new_name: New name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetGroupName"] = target_group_name
    kwargs["DBProxyName"] = db_proxy_name
    if connection_pool_config is not None:
        kwargs["ConnectionPoolConfig"] = connection_pool_config
    if new_name is not None:
        kwargs["NewName"] = new_name
    try:
        resp = client.modify_db_proxy_target_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db proxy target group") from exc
    return ModifyDbProxyTargetGroupResult(
        db_proxy_target_group=resp.get("DBProxyTargetGroup"),
    )


def modify_db_recommendation(
    recommendation_id: str,
    *,
    locale: str | None = None,
    status: str | None = None,
    recommended_action_updates: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ModifyDbRecommendationResult:
    """Modify db recommendation.

    Args:
        recommendation_id: Recommendation id.
        locale: Locale.
        status: Status.
        recommended_action_updates: Recommended action updates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RecommendationId"] = recommendation_id
    if locale is not None:
        kwargs["Locale"] = locale
    if status is not None:
        kwargs["Status"] = status
    if recommended_action_updates is not None:
        kwargs["RecommendedActionUpdates"] = recommended_action_updates
    try:
        resp = client.modify_db_recommendation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db recommendation") from exc
    return ModifyDbRecommendationResult(
        db_recommendation=resp.get("DBRecommendation"),
    )


def modify_db_shard_group(
    db_shard_group_identifier: str,
    *,
    max_acu: float | None = None,
    min_acu: float | None = None,
    compute_redundancy: int | None = None,
    region_name: str | None = None,
) -> ModifyDbShardGroupResult:
    """Modify db shard group.

    Args:
        db_shard_group_identifier: Db shard group identifier.
        max_acu: Max acu.
        min_acu: Min acu.
        compute_redundancy: Compute redundancy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBShardGroupIdentifier"] = db_shard_group_identifier
    if max_acu is not None:
        kwargs["MaxACU"] = max_acu
    if min_acu is not None:
        kwargs["MinACU"] = min_acu
    if compute_redundancy is not None:
        kwargs["ComputeRedundancy"] = compute_redundancy
    try:
        resp = client.modify_db_shard_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db shard group") from exc
    return ModifyDbShardGroupResult(
        db_shard_group_resource_id=resp.get("DBShardGroupResourceId"),
        db_shard_group_identifier=resp.get("DBShardGroupIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        max_acu=resp.get("MaxACU"),
        min_acu=resp.get("MinACU"),
        compute_redundancy=resp.get("ComputeRedundancy"),
        status=resp.get("Status"),
        publicly_accessible=resp.get("PubliclyAccessible"),
        endpoint=resp.get("Endpoint"),
        db_shard_group_arn=resp.get("DBShardGroupArn"),
        tag_list=resp.get("TagList"),
    )


def modify_db_snapshot(
    db_snapshot_identifier: str,
    *,
    engine_version: str | None = None,
    option_group_name: str | None = None,
    region_name: str | None = None,
) -> ModifyDbSnapshotResult:
    """Modify db snapshot.

    Args:
        db_snapshot_identifier: Db snapshot identifier.
        engine_version: Engine version.
        option_group_name: Option group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSnapshotIdentifier"] = db_snapshot_identifier
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    try:
        resp = client.modify_db_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db snapshot") from exc
    return ModifyDbSnapshotResult(
        db_snapshot=resp.get("DBSnapshot"),
    )


def modify_db_snapshot_attribute(
    db_snapshot_identifier: str,
    attribute_name: str,
    *,
    values_to_add: list[str] | None = None,
    values_to_remove: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyDbSnapshotAttributeResult:
    """Modify db snapshot attribute.

    Args:
        db_snapshot_identifier: Db snapshot identifier.
        attribute_name: Attribute name.
        values_to_add: Values to add.
        values_to_remove: Values to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSnapshotIdentifier"] = db_snapshot_identifier
    kwargs["AttributeName"] = attribute_name
    if values_to_add is not None:
        kwargs["ValuesToAdd"] = values_to_add
    if values_to_remove is not None:
        kwargs["ValuesToRemove"] = values_to_remove
    try:
        resp = client.modify_db_snapshot_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db snapshot attribute") from exc
    return ModifyDbSnapshotAttributeResult(
        db_snapshot_attributes_result=resp.get("DBSnapshotAttributesResult"),
    )


def modify_db_subnet_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSubnetGroupName"] = db_subnet_group_name
    kwargs["SubnetIds"] = subnet_ids
    if db_subnet_group_description is not None:
        kwargs["DBSubnetGroupDescription"] = db_subnet_group_description
    try:
        resp = client.modify_db_subnet_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify db subnet group") from exc
    return ModifyDbSubnetGroupResult(
        db_subnet_group=resp.get("DBSubnetGroup"),
    )


def modify_event_subscription(
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
    client = get_client("rds", region_name)
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
        resp = client.modify_event_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify event subscription") from exc
    return ModifyEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


def modify_global_cluster(
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
    client = get_client("rds", region_name)
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
        resp = client.modify_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify global cluster") from exc
    return ModifyGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def modify_integration(
    integration_identifier: str,
    *,
    integration_name: str | None = None,
    data_filter: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> ModifyIntegrationResult:
    """Modify integration.

    Args:
        integration_identifier: Integration identifier.
        integration_name: Integration name.
        data_filter: Data filter.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationIdentifier"] = integration_identifier
    if integration_name is not None:
        kwargs["IntegrationName"] = integration_name
    if data_filter is not None:
        kwargs["DataFilter"] = data_filter
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.modify_integration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify integration") from exc
    return ModifyIntegrationResult(
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        integration_name=resp.get("IntegrationName"),
        integration_arn=resp.get("IntegrationArn"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        status=resp.get("Status"),
        tags=resp.get("Tags"),
        data_filter=resp.get("DataFilter"),
        description=resp.get("Description"),
        create_time=resp.get("CreateTime"),
        errors=resp.get("Errors"),
    )


def modify_option_group(
    option_group_name: str,
    *,
    options_to_include: list[dict[str, Any]] | None = None,
    options_to_remove: list[str] | None = None,
    apply_immediately: bool | None = None,
    region_name: str | None = None,
) -> ModifyOptionGroupResult:
    """Modify option group.

    Args:
        option_group_name: Option group name.
        options_to_include: Options to include.
        options_to_remove: Options to remove.
        apply_immediately: Apply immediately.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OptionGroupName"] = option_group_name
    if options_to_include is not None:
        kwargs["OptionsToInclude"] = options_to_include
    if options_to_remove is not None:
        kwargs["OptionsToRemove"] = options_to_remove
    if apply_immediately is not None:
        kwargs["ApplyImmediately"] = apply_immediately
    try:
        resp = client.modify_option_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify option group") from exc
    return ModifyOptionGroupResult(
        option_group=resp.get("OptionGroup"),
    )


def modify_tenant_database(
    db_instance_identifier: str,
    tenant_db_name: str,
    *,
    master_user_password: str | None = None,
    new_tenant_db_name: str | None = None,
    manage_master_user_password: bool | None = None,
    rotate_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    region_name: str | None = None,
) -> ModifyTenantDatabaseResult:
    """Modify tenant database.

    Args:
        db_instance_identifier: Db instance identifier.
        tenant_db_name: Tenant db name.
        master_user_password: Master user password.
        new_tenant_db_name: New tenant db name.
        manage_master_user_password: Manage master user password.
        rotate_master_user_password: Rotate master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["TenantDBName"] = tenant_db_name
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if new_tenant_db_name is not None:
        kwargs["NewTenantDBName"] = new_tenant_db_name
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if rotate_master_user_password is not None:
        kwargs["RotateMasterUserPassword"] = rotate_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    try:
        resp = client.modify_tenant_database(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to modify tenant database") from exc
    return ModifyTenantDatabaseResult(
        tenant_database=resp.get("TenantDatabase"),
    )


def promote_read_replica(
    db_instance_identifier: str,
    *,
    backup_retention_period: int | None = None,
    preferred_backup_window: str | None = None,
    region_name: str | None = None,
) -> PromoteReadReplicaResult:
    """Promote read replica.

    Args:
        db_instance_identifier: Db instance identifier.
        backup_retention_period: Backup retention period.
        preferred_backup_window: Preferred backup window.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    try:
        resp = client.promote_read_replica(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to promote read replica") from exc
    return PromoteReadReplicaResult(
        db_instance=resp.get("DBInstance"),
    )


def promote_read_replica_db_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = client.promote_read_replica_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to promote read replica db cluster") from exc
    return PromoteReadReplicaDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def purchase_reserved_db_instances_offering(
    reserved_db_instances_offering_id: str,
    *,
    reserved_db_instance_id: str | None = None,
    db_instance_count: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PurchaseReservedDbInstancesOfferingResult:
    """Purchase reserved db instances offering.

    Args:
        reserved_db_instances_offering_id: Reserved db instances offering id.
        reserved_db_instance_id: Reserved db instance id.
        db_instance_count: Db instance count.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedDBInstancesOfferingId"] = reserved_db_instances_offering_id
    if reserved_db_instance_id is not None:
        kwargs["ReservedDBInstanceId"] = reserved_db_instance_id
    if db_instance_count is not None:
        kwargs["DBInstanceCount"] = db_instance_count
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.purchase_reserved_db_instances_offering(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to purchase reserved db instances offering") from exc
    return PurchaseReservedDbInstancesOfferingResult(
        reserved_db_instance=resp.get("ReservedDBInstance"),
    )


def reboot_db_cluster(
    db_cluster_identifier: str,
    region_name: str | None = None,
) -> RebootDbClusterResult:
    """Reboot db cluster.

    Args:
        db_cluster_identifier: Db cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = client.reboot_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reboot db cluster") from exc
    return RebootDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def reboot_db_instance(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if force_failover is not None:
        kwargs["ForceFailover"] = force_failover
    try:
        resp = client.reboot_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reboot db instance") from exc
    return RebootDbInstanceResult(
        db_instance=resp.get("DBInstance"),
    )


def reboot_db_shard_group(
    db_shard_group_identifier: str,
    region_name: str | None = None,
) -> RebootDbShardGroupResult:
    """Reboot db shard group.

    Args:
        db_shard_group_identifier: Db shard group identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBShardGroupIdentifier"] = db_shard_group_identifier
    try:
        resp = client.reboot_db_shard_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reboot db shard group") from exc
    return RebootDbShardGroupResult(
        db_shard_group_resource_id=resp.get("DBShardGroupResourceId"),
        db_shard_group_identifier=resp.get("DBShardGroupIdentifier"),
        db_cluster_identifier=resp.get("DBClusterIdentifier"),
        max_acu=resp.get("MaxACU"),
        min_acu=resp.get("MinACU"),
        compute_redundancy=resp.get("ComputeRedundancy"),
        status=resp.get("Status"),
        publicly_accessible=resp.get("PubliclyAccessible"),
        endpoint=resp.get("Endpoint"),
        db_shard_group_arn=resp.get("DBShardGroupArn"),
        tag_list=resp.get("TagList"),
    )


def register_db_proxy_targets(
    db_proxy_name: str,
    *,
    target_group_name: str | None = None,
    db_instance_identifiers: list[str] | None = None,
    db_cluster_identifiers: list[str] | None = None,
    region_name: str | None = None,
) -> RegisterDbProxyTargetsResult:
    """Register db proxy targets.

    Args:
        db_proxy_name: Db proxy name.
        target_group_name: Target group name.
        db_instance_identifiers: Db instance identifiers.
        db_cluster_identifiers: Db cluster identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBProxyName"] = db_proxy_name
    if target_group_name is not None:
        kwargs["TargetGroupName"] = target_group_name
    if db_instance_identifiers is not None:
        kwargs["DBInstanceIdentifiers"] = db_instance_identifiers
    if db_cluster_identifiers is not None:
        kwargs["DBClusterIdentifiers"] = db_cluster_identifiers
    try:
        resp = client.register_db_proxy_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register db proxy targets") from exc
    return RegisterDbProxyTargetsResult(
        db_proxy_targets=resp.get("DBProxyTargets"),
    )


def remove_from_global_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["DbClusterIdentifier"] = db_cluster_identifier
    try:
        resp = client.remove_from_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove from global cluster") from exc
    return RemoveFromGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def remove_role_from_db_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["RoleArn"] = role_arn
    if feature_name is not None:
        kwargs["FeatureName"] = feature_name
    try:
        client.remove_role_from_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove role from db cluster") from exc
    return None


def remove_role_from_db_instance(
    db_instance_identifier: str,
    role_arn: str,
    feature_name: str,
    region_name: str | None = None,
) -> None:
    """Remove role from db instance.

    Args:
        db_instance_identifier: Db instance identifier.
        role_arn: Role arn.
        feature_name: Feature name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["RoleArn"] = role_arn
    kwargs["FeatureName"] = feature_name
    try:
        client.remove_role_from_db_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove role from db instance") from exc
    return None


def remove_source_identifier_from_subscription(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SourceIdentifier"] = source_identifier
    try:
        resp = client.remove_source_identifier_from_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove source identifier from subscription") from exc
    return RemoveSourceIdentifierFromSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


def remove_tags_from_resource(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["TagKeys"] = tag_keys
    try:
        client.remove_tags_from_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from resource") from exc
    return None


def reset_db_cluster_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = client.reset_db_cluster_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reset db cluster parameter group") from exc
    return ResetDbClusterParameterGroupResult(
        db_cluster_parameter_group_name=resp.get("DBClusterParameterGroupName"),
    )


def reset_db_parameter_group(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBParameterGroupName"] = db_parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = client.reset_db_parameter_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to reset db parameter group") from exc
    return ResetDbParameterGroupResult(
        db_parameter_group_name=resp.get("DBParameterGroupName"),
    )


def restore_db_cluster_from_s3(
    db_cluster_identifier: str,
    engine: str,
    master_username: str,
    source_engine: str,
    source_engine_version: str,
    s3_bucket_name: str,
    s3_ingestion_role_arn: str,
    *,
    availability_zones: list[str] | None = None,
    backup_retention_period: int | None = None,
    character_set_name: str | None = None,
    database_name: str | None = None,
    db_cluster_parameter_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    db_subnet_group_name: str | None = None,
    engine_version: str | None = None,
    port: int | None = None,
    master_user_password: str | None = None,
    option_group_name: str | None = None,
    preferred_backup_window: str | None = None,
    preferred_maintenance_window: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    storage_encrypted: bool | None = None,
    kms_key_id: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    s3_prefix: str | None = None,
    backtrack_window: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    deletion_protection: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    storage_type: str | None = None,
    network_type: str | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    engine_lifecycle_support: str | None = None,
    region_name: str | None = None,
) -> RestoreDbClusterFromS3Result:
    """Restore db cluster from s3.

    Args:
        db_cluster_identifier: Db cluster identifier.
        engine: Engine.
        master_username: Master username.
        source_engine: Source engine.
        source_engine_version: Source engine version.
        s3_bucket_name: S3 bucket name.
        s3_ingestion_role_arn: S3 ingestion role arn.
        availability_zones: Availability zones.
        backup_retention_period: Backup retention period.
        character_set_name: Character set name.
        database_name: Database name.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        vpc_security_group_ids: Vpc security group ids.
        db_subnet_group_name: Db subnet group name.
        engine_version: Engine version.
        port: Port.
        master_user_password: Master user password.
        option_group_name: Option group name.
        preferred_backup_window: Preferred backup window.
        preferred_maintenance_window: Preferred maintenance window.
        tags: Tags.
        storage_encrypted: Storage encrypted.
        kms_key_id: Kms key id.
        enable_iam_database_authentication: Enable iam database authentication.
        s3_prefix: S3 prefix.
        backtrack_window: Backtrack window.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        deletion_protection: Deletion protection.
        copy_tags_to_snapshot: Copy tags to snapshot.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        storage_type: Storage type.
        network_type: Network type.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        engine_lifecycle_support: Engine lifecycle support.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    kwargs["Engine"] = engine
    kwargs["MasterUsername"] = master_username
    kwargs["SourceEngine"] = source_engine
    kwargs["SourceEngineVersion"] = source_engine_version
    kwargs["S3BucketName"] = s3_bucket_name
    kwargs["S3IngestionRoleArn"] = s3_ingestion_role_arn
    if availability_zones is not None:
        kwargs["AvailabilityZones"] = availability_zones
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if character_set_name is not None:
        kwargs["CharacterSetName"] = character_set_name
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if port is not None:
        kwargs["Port"] = port
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if tags is not None:
        kwargs["Tags"] = tags
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if s3_prefix is not None:
        kwargs["S3Prefix"] = s3_prefix
    if backtrack_window is not None:
        kwargs["BacktrackWindow"] = backtrack_window
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    try:
        resp = client.restore_db_cluster_from_s3(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db cluster from s3") from exc
    return RestoreDbClusterFromS3Result(
        db_cluster=resp.get("DBCluster"),
    )


def restore_db_cluster_from_snapshot(
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
    backtrack_window: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    engine_mode: str | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    db_cluster_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    db_cluster_instance_class: str | None = None,
    storage_type: str | None = None,
    iops: int | None = None,
    publicly_accessible: bool | None = None,
    network_type: str | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    rds_custom_cluster_configuration: dict[str, Any] | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    engine_lifecycle_support: str | None = None,
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
        backtrack_window: Backtrack window.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        engine_mode: Engine mode.
        scaling_configuration: Scaling configuration.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        deletion_protection: Deletion protection.
        copy_tags_to_snapshot: Copy tags to snapshot.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        db_cluster_instance_class: Db cluster instance class.
        storage_type: Storage type.
        iops: Iops.
        publicly_accessible: Publicly accessible.
        network_type: Network type.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        rds_custom_cluster_configuration: Rds custom cluster configuration.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        engine_lifecycle_support: Engine lifecycle support.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
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
    if backtrack_window is not None:
        kwargs["BacktrackWindow"] = backtrack_window
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if engine_mode is not None:
        kwargs["EngineMode"] = engine_mode
    if scaling_configuration is not None:
        kwargs["ScalingConfiguration"] = scaling_configuration
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if db_cluster_instance_class is not None:
        kwargs["DBClusterInstanceClass"] = db_cluster_instance_class
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if iops is not None:
        kwargs["Iops"] = iops
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if rds_custom_cluster_configuration is not None:
        kwargs["RdsCustomClusterConfiguration"] = rds_custom_cluster_configuration
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    try:
        resp = client.restore_db_cluster_from_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db cluster from snapshot") from exc
    return RestoreDbClusterFromSnapshotResult(
        db_cluster=resp.get("DBCluster"),
    )


def restore_db_cluster_to_point_in_time(
    db_cluster_identifier: str,
    *,
    restore_type: str | None = None,
    source_db_cluster_identifier: str | None = None,
    restore_to_time: str | None = None,
    use_latest_restorable_time: bool | None = None,
    port: int | None = None,
    db_subnet_group_name: str | None = None,
    option_group_name: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    kms_key_id: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    backtrack_window: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    db_cluster_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    copy_tags_to_snapshot: bool | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    db_cluster_instance_class: str | None = None,
    storage_type: str | None = None,
    publicly_accessible: bool | None = None,
    iops: int | None = None,
    network_type: str | None = None,
    source_db_cluster_resource_id: str | None = None,
    serverless_v2_scaling_configuration: dict[str, Any] | None = None,
    scaling_configuration: dict[str, Any] | None = None,
    engine_mode: str | None = None,
    rds_custom_cluster_configuration: dict[str, Any] | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    engine_lifecycle_support: str | None = None,
    region_name: str | None = None,
) -> RestoreDbClusterToPointInTimeResult:
    """Restore db cluster to point in time.

    Args:
        db_cluster_identifier: Db cluster identifier.
        restore_type: Restore type.
        source_db_cluster_identifier: Source db cluster identifier.
        restore_to_time: Restore to time.
        use_latest_restorable_time: Use latest restorable time.
        port: Port.
        db_subnet_group_name: Db subnet group name.
        option_group_name: Option group name.
        vpc_security_group_ids: Vpc security group ids.
        tags: Tags.
        kms_key_id: Kms key id.
        enable_iam_database_authentication: Enable iam database authentication.
        backtrack_window: Backtrack window.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        db_cluster_parameter_group_name: Db cluster parameter group name.
        deletion_protection: Deletion protection.
        copy_tags_to_snapshot: Copy tags to snapshot.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        db_cluster_instance_class: Db cluster instance class.
        storage_type: Storage type.
        publicly_accessible: Publicly accessible.
        iops: Iops.
        network_type: Network type.
        source_db_cluster_resource_id: Source db cluster resource id.
        serverless_v2_scaling_configuration: Serverless v2 scaling configuration.
        scaling_configuration: Scaling configuration.
        engine_mode: Engine mode.
        rds_custom_cluster_configuration: Rds custom cluster configuration.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        engine_lifecycle_support: Engine lifecycle support.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    if restore_type is not None:
        kwargs["RestoreType"] = restore_type
    if source_db_cluster_identifier is not None:
        kwargs["SourceDBClusterIdentifier"] = source_db_cluster_identifier
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
    if backtrack_window is not None:
        kwargs["BacktrackWindow"] = backtrack_window
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if db_cluster_parameter_group_name is not None:
        kwargs["DBClusterParameterGroupName"] = db_cluster_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if db_cluster_instance_class is not None:
        kwargs["DBClusterInstanceClass"] = db_cluster_instance_class
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if iops is not None:
        kwargs["Iops"] = iops
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if source_db_cluster_resource_id is not None:
        kwargs["SourceDbClusterResourceId"] = source_db_cluster_resource_id
    if serverless_v2_scaling_configuration is not None:
        kwargs["ServerlessV2ScalingConfiguration"] = serverless_v2_scaling_configuration
    if scaling_configuration is not None:
        kwargs["ScalingConfiguration"] = scaling_configuration
    if engine_mode is not None:
        kwargs["EngineMode"] = engine_mode
    if rds_custom_cluster_configuration is not None:
        kwargs["RdsCustomClusterConfiguration"] = rds_custom_cluster_configuration
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    try:
        resp = client.restore_db_cluster_to_point_in_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db cluster to point in time") from exc
    return RestoreDbClusterToPointInTimeResult(
        db_cluster=resp.get("DBCluster"),
    )


def restore_db_instance_from_db_snapshot(
    db_instance_identifier: str,
    *,
    db_snapshot_identifier: str | None = None,
    db_instance_class: str | None = None,
    port: int | None = None,
    availability_zone: str | None = None,
    db_subnet_group_name: str | None = None,
    multi_az: bool | None = None,
    publicly_accessible: bool | None = None,
    auto_minor_version_upgrade: bool | None = None,
    license_model: str | None = None,
    db_name: str | None = None,
    engine: str | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    storage_type: str | None = None,
    tde_credential_arn: str | None = None,
    tde_credential_password: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    domain: str | None = None,
    domain_fqdn: str | None = None,
    domain_ou: str | None = None,
    domain_auth_secret_arn: str | None = None,
    domain_dns_ips: list[str] | None = None,
    copy_tags_to_snapshot: bool | None = None,
    domain_iam_role_name: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    use_default_processor_features: bool | None = None,
    db_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    enable_customer_owned_ip: bool | None = None,
    network_type: str | None = None,
    backup_target: str | None = None,
    custom_iam_instance_profile: str | None = None,
    allocated_storage: int | None = None,
    db_cluster_snapshot_identifier: str | None = None,
    dedicated_log_volume: bool | None = None,
    ca_certificate_identifier: str | None = None,
    engine_lifecycle_support: str | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    region_name: str | None = None,
) -> RestoreDbInstanceFromDbSnapshotResult:
    """Restore db instance from db snapshot.

    Args:
        db_instance_identifier: Db instance identifier.
        db_snapshot_identifier: Db snapshot identifier.
        db_instance_class: Db instance class.
        port: Port.
        availability_zone: Availability zone.
        db_subnet_group_name: Db subnet group name.
        multi_az: Multi az.
        publicly_accessible: Publicly accessible.
        auto_minor_version_upgrade: Auto minor version upgrade.
        license_model: License model.
        db_name: Db name.
        engine: Engine.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        tags: Tags.
        storage_type: Storage type.
        tde_credential_arn: Tde credential arn.
        tde_credential_password: Tde credential password.
        vpc_security_group_ids: Vpc security group ids.
        domain: Domain.
        domain_fqdn: Domain fqdn.
        domain_ou: Domain ou.
        domain_auth_secret_arn: Domain auth secret arn.
        domain_dns_ips: Domain dns ips.
        copy_tags_to_snapshot: Copy tags to snapshot.
        domain_iam_role_name: Domain iam role name.
        enable_iam_database_authentication: Enable iam database authentication.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        processor_features: Processor features.
        use_default_processor_features: Use default processor features.
        db_parameter_group_name: Db parameter group name.
        deletion_protection: Deletion protection.
        enable_customer_owned_ip: Enable customer owned ip.
        network_type: Network type.
        backup_target: Backup target.
        custom_iam_instance_profile: Custom iam instance profile.
        allocated_storage: Allocated storage.
        db_cluster_snapshot_identifier: Db cluster snapshot identifier.
        dedicated_log_volume: Dedicated log volume.
        ca_certificate_identifier: Ca certificate identifier.
        engine_lifecycle_support: Engine lifecycle support.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    if db_snapshot_identifier is not None:
        kwargs["DBSnapshotIdentifier"] = db_snapshot_identifier
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if port is not None:
        kwargs["Port"] = port
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if db_name is not None:
        kwargs["DBName"] = db_name
    if engine is not None:
        kwargs["Engine"] = engine
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if tags is not None:
        kwargs["Tags"] = tags
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if tde_credential_arn is not None:
        kwargs["TdeCredentialArn"] = tde_credential_arn
    if tde_credential_password is not None:
        kwargs["TdeCredentialPassword"] = tde_credential_password
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_fqdn is not None:
        kwargs["DomainFqdn"] = domain_fqdn
    if domain_ou is not None:
        kwargs["DomainOu"] = domain_ou
    if domain_auth_secret_arn is not None:
        kwargs["DomainAuthSecretArn"] = domain_auth_secret_arn
    if domain_dns_ips is not None:
        kwargs["DomainDnsIps"] = domain_dns_ips
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if use_default_processor_features is not None:
        kwargs["UseDefaultProcessorFeatures"] = use_default_processor_features
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if enable_customer_owned_ip is not None:
        kwargs["EnableCustomerOwnedIp"] = enable_customer_owned_ip
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if backup_target is not None:
        kwargs["BackupTarget"] = backup_target
    if custom_iam_instance_profile is not None:
        kwargs["CustomIamInstanceProfile"] = custom_iam_instance_profile
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if db_cluster_snapshot_identifier is not None:
        kwargs["DBClusterSnapshotIdentifier"] = db_cluster_snapshot_identifier
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    try:
        resp = client.restore_db_instance_from_db_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db instance from db snapshot") from exc
    return RestoreDbInstanceFromDbSnapshotResult(
        db_instance=resp.get("DBInstance"),
    )


def restore_db_instance_from_s3(
    db_instance_identifier: str,
    db_instance_class: str,
    engine: str,
    source_engine: str,
    source_engine_version: str,
    s3_bucket_name: str,
    s3_ingestion_role_arn: str,
    *,
    db_name: str | None = None,
    allocated_storage: int | None = None,
    master_username: str | None = None,
    master_user_password: str | None = None,
    db_security_groups: list[str] | None = None,
    vpc_security_group_ids: list[str] | None = None,
    availability_zone: str | None = None,
    db_subnet_group_name: str | None = None,
    preferred_maintenance_window: str | None = None,
    db_parameter_group_name: str | None = None,
    backup_retention_period: int | None = None,
    preferred_backup_window: str | None = None,
    port: int | None = None,
    multi_az: bool | None = None,
    engine_version: str | None = None,
    auto_minor_version_upgrade: bool | None = None,
    license_model: str | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    publicly_accessible: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    storage_type: str | None = None,
    storage_encrypted: bool | None = None,
    kms_key_id: str | None = None,
    copy_tags_to_snapshot: bool | None = None,
    monitoring_interval: int | None = None,
    monitoring_role_arn: str | None = None,
    enable_iam_database_authentication: bool | None = None,
    s3_prefix: str | None = None,
    database_insights_mode: str | None = None,
    enable_performance_insights: bool | None = None,
    performance_insights_kms_key_id: str | None = None,
    performance_insights_retention_period: int | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    use_default_processor_features: bool | None = None,
    deletion_protection: bool | None = None,
    max_allocated_storage: int | None = None,
    network_type: str | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    dedicated_log_volume: bool | None = None,
    ca_certificate_identifier: str | None = None,
    engine_lifecycle_support: str | None = None,
    region_name: str | None = None,
) -> RestoreDbInstanceFromS3Result:
    """Restore db instance from s3.

    Args:
        db_instance_identifier: Db instance identifier.
        db_instance_class: Db instance class.
        engine: Engine.
        source_engine: Source engine.
        source_engine_version: Source engine version.
        s3_bucket_name: S3 bucket name.
        s3_ingestion_role_arn: S3 ingestion role arn.
        db_name: Db name.
        allocated_storage: Allocated storage.
        master_username: Master username.
        master_user_password: Master user password.
        db_security_groups: Db security groups.
        vpc_security_group_ids: Vpc security group ids.
        availability_zone: Availability zone.
        db_subnet_group_name: Db subnet group name.
        preferred_maintenance_window: Preferred maintenance window.
        db_parameter_group_name: Db parameter group name.
        backup_retention_period: Backup retention period.
        preferred_backup_window: Preferred backup window.
        port: Port.
        multi_az: Multi az.
        engine_version: Engine version.
        auto_minor_version_upgrade: Auto minor version upgrade.
        license_model: License model.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        publicly_accessible: Publicly accessible.
        tags: Tags.
        storage_type: Storage type.
        storage_encrypted: Storage encrypted.
        kms_key_id: Kms key id.
        copy_tags_to_snapshot: Copy tags to snapshot.
        monitoring_interval: Monitoring interval.
        monitoring_role_arn: Monitoring role arn.
        enable_iam_database_authentication: Enable iam database authentication.
        s3_prefix: S3 prefix.
        database_insights_mode: Database insights mode.
        enable_performance_insights: Enable performance insights.
        performance_insights_kms_key_id: Performance insights kms key id.
        performance_insights_retention_period: Performance insights retention period.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        processor_features: Processor features.
        use_default_processor_features: Use default processor features.
        deletion_protection: Deletion protection.
        max_allocated_storage: Max allocated storage.
        network_type: Network type.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        dedicated_log_volume: Dedicated log volume.
        ca_certificate_identifier: Ca certificate identifier.
        engine_lifecycle_support: Engine lifecycle support.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    kwargs["DBInstanceClass"] = db_instance_class
    kwargs["Engine"] = engine
    kwargs["SourceEngine"] = source_engine
    kwargs["SourceEngineVersion"] = source_engine_version
    kwargs["S3BucketName"] = s3_bucket_name
    kwargs["S3IngestionRoleArn"] = s3_ingestion_role_arn
    if db_name is not None:
        kwargs["DBName"] = db_name
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if master_username is not None:
        kwargs["MasterUsername"] = master_username
    if master_user_password is not None:
        kwargs["MasterUserPassword"] = master_user_password
    if db_security_groups is not None:
        kwargs["DBSecurityGroups"] = db_security_groups
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if preferred_maintenance_window is not None:
        kwargs["PreferredMaintenanceWindow"] = preferred_maintenance_window
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if preferred_backup_window is not None:
        kwargs["PreferredBackupWindow"] = preferred_backup_window
    if port is not None:
        kwargs["Port"] = port
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if engine_version is not None:
        kwargs["EngineVersion"] = engine_version
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if tags is not None:
        kwargs["Tags"] = tags
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if storage_encrypted is not None:
        kwargs["StorageEncrypted"] = storage_encrypted
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if monitoring_interval is not None:
        kwargs["MonitoringInterval"] = monitoring_interval
    if monitoring_role_arn is not None:
        kwargs["MonitoringRoleArn"] = monitoring_role_arn
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if s3_prefix is not None:
        kwargs["S3Prefix"] = s3_prefix
    if database_insights_mode is not None:
        kwargs["DatabaseInsightsMode"] = database_insights_mode
    if enable_performance_insights is not None:
        kwargs["EnablePerformanceInsights"] = enable_performance_insights
    if performance_insights_kms_key_id is not None:
        kwargs["PerformanceInsightsKMSKeyId"] = performance_insights_kms_key_id
    if performance_insights_retention_period is not None:
        kwargs["PerformanceInsightsRetentionPeriod"] = performance_insights_retention_period
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if use_default_processor_features is not None:
        kwargs["UseDefaultProcessorFeatures"] = use_default_processor_features
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if max_allocated_storage is not None:
        kwargs["MaxAllocatedStorage"] = max_allocated_storage
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    try:
        resp = client.restore_db_instance_from_s3(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db instance from s3") from exc
    return RestoreDbInstanceFromS3Result(
        db_instance=resp.get("DBInstance"),
    )


def restore_db_instance_to_point_in_time(
    target_db_instance_identifier: str,
    *,
    source_db_instance_identifier: str | None = None,
    restore_time: str | None = None,
    use_latest_restorable_time: bool | None = None,
    db_instance_class: str | None = None,
    port: int | None = None,
    availability_zone: str | None = None,
    db_subnet_group_name: str | None = None,
    multi_az: bool | None = None,
    publicly_accessible: bool | None = None,
    auto_minor_version_upgrade: bool | None = None,
    license_model: str | None = None,
    db_name: str | None = None,
    engine: str | None = None,
    iops: int | None = None,
    storage_throughput: int | None = None,
    option_group_name: str | None = None,
    copy_tags_to_snapshot: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    storage_type: str | None = None,
    tde_credential_arn: str | None = None,
    tde_credential_password: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    domain: str | None = None,
    domain_iam_role_name: str | None = None,
    domain_fqdn: str | None = None,
    domain_ou: str | None = None,
    domain_auth_secret_arn: str | None = None,
    domain_dns_ips: list[str] | None = None,
    enable_iam_database_authentication: bool | None = None,
    enable_cloudwatch_logs_exports: list[str] | None = None,
    processor_features: list[dict[str, Any]] | None = None,
    use_default_processor_features: bool | None = None,
    db_parameter_group_name: str | None = None,
    deletion_protection: bool | None = None,
    source_dbi_resource_id: str | None = None,
    max_allocated_storage: int | None = None,
    enable_customer_owned_ip: bool | None = None,
    network_type: str | None = None,
    source_db_instance_automated_backups_arn: str | None = None,
    backup_target: str | None = None,
    custom_iam_instance_profile: str | None = None,
    allocated_storage: int | None = None,
    dedicated_log_volume: bool | None = None,
    ca_certificate_identifier: str | None = None,
    engine_lifecycle_support: str | None = None,
    manage_master_user_password: bool | None = None,
    master_user_secret_kms_key_id: str | None = None,
    region_name: str | None = None,
) -> RestoreDbInstanceToPointInTimeResult:
    """Restore db instance to point in time.

    Args:
        target_db_instance_identifier: Target db instance identifier.
        source_db_instance_identifier: Source db instance identifier.
        restore_time: Restore time.
        use_latest_restorable_time: Use latest restorable time.
        db_instance_class: Db instance class.
        port: Port.
        availability_zone: Availability zone.
        db_subnet_group_name: Db subnet group name.
        multi_az: Multi az.
        publicly_accessible: Publicly accessible.
        auto_minor_version_upgrade: Auto minor version upgrade.
        license_model: License model.
        db_name: Db name.
        engine: Engine.
        iops: Iops.
        storage_throughput: Storage throughput.
        option_group_name: Option group name.
        copy_tags_to_snapshot: Copy tags to snapshot.
        tags: Tags.
        storage_type: Storage type.
        tde_credential_arn: Tde credential arn.
        tde_credential_password: Tde credential password.
        vpc_security_group_ids: Vpc security group ids.
        domain: Domain.
        domain_iam_role_name: Domain iam role name.
        domain_fqdn: Domain fqdn.
        domain_ou: Domain ou.
        domain_auth_secret_arn: Domain auth secret arn.
        domain_dns_ips: Domain dns ips.
        enable_iam_database_authentication: Enable iam database authentication.
        enable_cloudwatch_logs_exports: Enable cloudwatch logs exports.
        processor_features: Processor features.
        use_default_processor_features: Use default processor features.
        db_parameter_group_name: Db parameter group name.
        deletion_protection: Deletion protection.
        source_dbi_resource_id: Source dbi resource id.
        max_allocated_storage: Max allocated storage.
        enable_customer_owned_ip: Enable customer owned ip.
        network_type: Network type.
        source_db_instance_automated_backups_arn: Source db instance automated backups arn.
        backup_target: Backup target.
        custom_iam_instance_profile: Custom iam instance profile.
        allocated_storage: Allocated storage.
        dedicated_log_volume: Dedicated log volume.
        ca_certificate_identifier: Ca certificate identifier.
        engine_lifecycle_support: Engine lifecycle support.
        manage_master_user_password: Manage master user password.
        master_user_secret_kms_key_id: Master user secret kms key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetDBInstanceIdentifier"] = target_db_instance_identifier
    if source_db_instance_identifier is not None:
        kwargs["SourceDBInstanceIdentifier"] = source_db_instance_identifier
    if restore_time is not None:
        kwargs["RestoreTime"] = restore_time
    if use_latest_restorable_time is not None:
        kwargs["UseLatestRestorableTime"] = use_latest_restorable_time
    if db_instance_class is not None:
        kwargs["DBInstanceClass"] = db_instance_class
    if port is not None:
        kwargs["Port"] = port
    if availability_zone is not None:
        kwargs["AvailabilityZone"] = availability_zone
    if db_subnet_group_name is not None:
        kwargs["DBSubnetGroupName"] = db_subnet_group_name
    if multi_az is not None:
        kwargs["MultiAZ"] = multi_az
    if publicly_accessible is not None:
        kwargs["PubliclyAccessible"] = publicly_accessible
    if auto_minor_version_upgrade is not None:
        kwargs["AutoMinorVersionUpgrade"] = auto_minor_version_upgrade
    if license_model is not None:
        kwargs["LicenseModel"] = license_model
    if db_name is not None:
        kwargs["DBName"] = db_name
    if engine is not None:
        kwargs["Engine"] = engine
    if iops is not None:
        kwargs["Iops"] = iops
    if storage_throughput is not None:
        kwargs["StorageThroughput"] = storage_throughput
    if option_group_name is not None:
        kwargs["OptionGroupName"] = option_group_name
    if copy_tags_to_snapshot is not None:
        kwargs["CopyTagsToSnapshot"] = copy_tags_to_snapshot
    if tags is not None:
        kwargs["Tags"] = tags
    if storage_type is not None:
        kwargs["StorageType"] = storage_type
    if tde_credential_arn is not None:
        kwargs["TdeCredentialArn"] = tde_credential_arn
    if tde_credential_password is not None:
        kwargs["TdeCredentialPassword"] = tde_credential_password
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    if domain is not None:
        kwargs["Domain"] = domain
    if domain_iam_role_name is not None:
        kwargs["DomainIAMRoleName"] = domain_iam_role_name
    if domain_fqdn is not None:
        kwargs["DomainFqdn"] = domain_fqdn
    if domain_ou is not None:
        kwargs["DomainOu"] = domain_ou
    if domain_auth_secret_arn is not None:
        kwargs["DomainAuthSecretArn"] = domain_auth_secret_arn
    if domain_dns_ips is not None:
        kwargs["DomainDnsIps"] = domain_dns_ips
    if enable_iam_database_authentication is not None:
        kwargs["EnableIAMDatabaseAuthentication"] = enable_iam_database_authentication
    if enable_cloudwatch_logs_exports is not None:
        kwargs["EnableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports
    if processor_features is not None:
        kwargs["ProcessorFeatures"] = processor_features
    if use_default_processor_features is not None:
        kwargs["UseDefaultProcessorFeatures"] = use_default_processor_features
    if db_parameter_group_name is not None:
        kwargs["DBParameterGroupName"] = db_parameter_group_name
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if source_dbi_resource_id is not None:
        kwargs["SourceDbiResourceId"] = source_dbi_resource_id
    if max_allocated_storage is not None:
        kwargs["MaxAllocatedStorage"] = max_allocated_storage
    if enable_customer_owned_ip is not None:
        kwargs["EnableCustomerOwnedIp"] = enable_customer_owned_ip
    if network_type is not None:
        kwargs["NetworkType"] = network_type
    if source_db_instance_automated_backups_arn is not None:
        kwargs["SourceDBInstanceAutomatedBackupsArn"] = source_db_instance_automated_backups_arn
    if backup_target is not None:
        kwargs["BackupTarget"] = backup_target
    if custom_iam_instance_profile is not None:
        kwargs["CustomIamInstanceProfile"] = custom_iam_instance_profile
    if allocated_storage is not None:
        kwargs["AllocatedStorage"] = allocated_storage
    if dedicated_log_volume is not None:
        kwargs["DedicatedLogVolume"] = dedicated_log_volume
    if ca_certificate_identifier is not None:
        kwargs["CACertificateIdentifier"] = ca_certificate_identifier
    if engine_lifecycle_support is not None:
        kwargs["EngineLifecycleSupport"] = engine_lifecycle_support
    if manage_master_user_password is not None:
        kwargs["ManageMasterUserPassword"] = manage_master_user_password
    if master_user_secret_kms_key_id is not None:
        kwargs["MasterUserSecretKmsKeyId"] = master_user_secret_kms_key_id
    try:
        resp = client.restore_db_instance_to_point_in_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore db instance to point in time") from exc
    return RestoreDbInstanceToPointInTimeResult(
        db_instance=resp.get("DBInstance"),
    )


def revoke_db_security_group_ingress(
    db_security_group_name: str,
    *,
    cidrip: str | None = None,
    ec2_security_group_name: str | None = None,
    ec2_security_group_id: str | None = None,
    ec2_security_group_owner_id: str | None = None,
    region_name: str | None = None,
) -> RevokeDbSecurityGroupIngressResult:
    """Revoke db security group ingress.

    Args:
        db_security_group_name: Db security group name.
        cidrip: Cidrip.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_id: Ec2 security group id.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBSecurityGroupName"] = db_security_group_name
    if cidrip is not None:
        kwargs["CIDRIP"] = cidrip
    if ec2_security_group_name is not None:
        kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    if ec2_security_group_id is not None:
        kwargs["EC2SecurityGroupId"] = ec2_security_group_id
    if ec2_security_group_owner_id is not None:
        kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = client.revoke_db_security_group_ingress(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to revoke db security group ingress") from exc
    return RevokeDbSecurityGroupIngressResult(
        db_security_group=resp.get("DBSecurityGroup"),
    )


def start_activity_stream(
    resource_arn: str,
    mode: str,
    kms_key_id: str,
    *,
    apply_immediately: bool | None = None,
    engine_native_audit_fields_included: bool | None = None,
    region_name: str | None = None,
) -> StartActivityStreamResult:
    """Start activity stream.

    Args:
        resource_arn: Resource arn.
        mode: Mode.
        kms_key_id: Kms key id.
        apply_immediately: Apply immediately.
        engine_native_audit_fields_included: Engine native audit fields included.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Mode"] = mode
    kwargs["KmsKeyId"] = kms_key_id
    if apply_immediately is not None:
        kwargs["ApplyImmediately"] = apply_immediately
    if engine_native_audit_fields_included is not None:
        kwargs["EngineNativeAuditFieldsIncluded"] = engine_native_audit_fields_included
    try:
        resp = client.start_activity_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start activity stream") from exc
    return StartActivityStreamResult(
        kms_key_id=resp.get("KmsKeyId"),
        kinesis_stream_name=resp.get("KinesisStreamName"),
        status=resp.get("Status"),
        mode=resp.get("Mode"),
        engine_native_audit_fields_included=resp.get("EngineNativeAuditFieldsIncluded"),
        apply_immediately=resp.get("ApplyImmediately"),
    )


def start_db_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = client.start_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start db cluster") from exc
    return StartDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def start_db_instance_automated_backups_replication(
    source_db_instance_arn: str,
    *,
    backup_retention_period: int | None = None,
    kms_key_id: str | None = None,
    pre_signed_url: str | None = None,
    source_region: str | None = None,
    region_name: str | None = None,
) -> StartDbInstanceAutomatedBackupsReplicationResult:
    """Start db instance automated backups replication.

    Args:
        source_db_instance_arn: Source db instance arn.
        backup_retention_period: Backup retention period.
        kms_key_id: Kms key id.
        pre_signed_url: Pre signed url.
        source_region: Source region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBInstanceArn"] = source_db_instance_arn
    if backup_retention_period is not None:
        kwargs["BackupRetentionPeriod"] = backup_retention_period
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if pre_signed_url is not None:
        kwargs["PreSignedUrl"] = pre_signed_url
    if source_region is not None:
        kwargs["SourceRegion"] = source_region
    try:
        resp = client.start_db_instance_automated_backups_replication(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to start db instance automated backups replication"
        ) from exc
    return StartDbInstanceAutomatedBackupsReplicationResult(
        db_instance_automated_backup=resp.get("DBInstanceAutomatedBackup"),
    )


def start_export_task(
    export_task_identifier: str,
    source_arn: str,
    s3_bucket_name: str,
    iam_role_arn: str,
    kms_key_id: str,
    *,
    s3_prefix: str | None = None,
    export_only: list[str] | None = None,
    region_name: str | None = None,
) -> StartExportTaskResult:
    """Start export task.

    Args:
        export_task_identifier: Export task identifier.
        source_arn: Source arn.
        s3_bucket_name: S3 bucket name.
        iam_role_arn: Iam role arn.
        kms_key_id: Kms key id.
        s3_prefix: S3 prefix.
        export_only: Export only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExportTaskIdentifier"] = export_task_identifier
    kwargs["SourceArn"] = source_arn
    kwargs["S3BucketName"] = s3_bucket_name
    kwargs["IamRoleArn"] = iam_role_arn
    kwargs["KmsKeyId"] = kms_key_id
    if s3_prefix is not None:
        kwargs["S3Prefix"] = s3_prefix
    if export_only is not None:
        kwargs["ExportOnly"] = export_only
    try:
        resp = client.start_export_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start export task") from exc
    return StartExportTaskResult(
        export_task_identifier=resp.get("ExportTaskIdentifier"),
        source_arn=resp.get("SourceArn"),
        export_only=resp.get("ExportOnly"),
        snapshot_time=resp.get("SnapshotTime"),
        task_start_time=resp.get("TaskStartTime"),
        task_end_time=resp.get("TaskEndTime"),
        s3_bucket=resp.get("S3Bucket"),
        s3_prefix=resp.get("S3Prefix"),
        iam_role_arn=resp.get("IamRoleArn"),
        kms_key_id=resp.get("KmsKeyId"),
        status=resp.get("Status"),
        percent_progress=resp.get("PercentProgress"),
        total_extracted_data_in_gb=resp.get("TotalExtractedDataInGB"),
        failure_cause=resp.get("FailureCause"),
        warning_message=resp.get("WarningMessage"),
        source_type=resp.get("SourceType"),
    )


def stop_activity_stream(
    resource_arn: str,
    *,
    apply_immediately: bool | None = None,
    region_name: str | None = None,
) -> StopActivityStreamResult:
    """Stop activity stream.

    Args:
        resource_arn: Resource arn.
        apply_immediately: Apply immediately.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if apply_immediately is not None:
        kwargs["ApplyImmediately"] = apply_immediately
    try:
        resp = client.stop_activity_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop activity stream") from exc
    return StopActivityStreamResult(
        kms_key_id=resp.get("KmsKeyId"),
        kinesis_stream_name=resp.get("KinesisStreamName"),
        status=resp.get("Status"),
    )


def stop_db_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBClusterIdentifier"] = db_cluster_identifier
    try:
        resp = client.stop_db_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop db cluster") from exc
    return StopDbClusterResult(
        db_cluster=resp.get("DBCluster"),
    )


def stop_db_instance_automated_backups_replication(
    source_db_instance_arn: str,
    region_name: str | None = None,
) -> StopDbInstanceAutomatedBackupsReplicationResult:
    """Stop db instance automated backups replication.

    Args:
        source_db_instance_arn: Source db instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceDBInstanceArn"] = source_db_instance_arn
    try:
        resp = client.stop_db_instance_automated_backups_replication(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to stop db instance automated backups replication"
        ) from exc
    return StopDbInstanceAutomatedBackupsReplicationResult(
        db_instance_automated_backup=resp.get("DBInstanceAutomatedBackup"),
    )


def switchover_blue_green_deployment(
    blue_green_deployment_identifier: str,
    *,
    switchover_timeout: int | None = None,
    region_name: str | None = None,
) -> SwitchoverBlueGreenDeploymentResult:
    """Switchover blue green deployment.

    Args:
        blue_green_deployment_identifier: Blue green deployment identifier.
        switchover_timeout: Switchover timeout.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BlueGreenDeploymentIdentifier"] = blue_green_deployment_identifier
    if switchover_timeout is not None:
        kwargs["SwitchoverTimeout"] = switchover_timeout
    try:
        resp = client.switchover_blue_green_deployment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to switchover blue green deployment") from exc
    return SwitchoverBlueGreenDeploymentResult(
        blue_green_deployment=resp.get("BlueGreenDeployment"),
    )


def switchover_global_cluster(
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
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalClusterIdentifier"] = global_cluster_identifier
    kwargs["TargetDbClusterIdentifier"] = target_db_cluster_identifier
    try:
        resp = client.switchover_global_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to switchover global cluster") from exc
    return SwitchoverGlobalClusterResult(
        global_cluster=resp.get("GlobalCluster"),
    )


def switchover_read_replica(
    db_instance_identifier: str,
    region_name: str | None = None,
) -> SwitchoverReadReplicaResult:
    """Switchover read replica.

    Args:
        db_instance_identifier: Db instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DBInstanceIdentifier"] = db_instance_identifier
    try:
        resp = client.switchover_read_replica(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to switchover read replica") from exc
    return SwitchoverReadReplicaResult(
        db_instance=resp.get("DBInstance"),
    )
