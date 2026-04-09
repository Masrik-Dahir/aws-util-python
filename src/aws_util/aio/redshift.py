"""Native async Redshift utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time as _time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import (
    AwsServiceError,
    AwsTimeoutError,
    wrap_aws_error,
)
from aws_util.redshift import (
    AcceptReservedNodeExchangeResult,
    AddPartnerResult,
    AssociateDataShareConsumerResult,
    AuthorizeClusterSecurityGroupIngressResult,
    AuthorizeDataShareResult,
    AuthorizeEndpointAccessResult,
    AuthorizeSnapshotAccessResult,
    BatchDeleteClusterSnapshotsResult,
    BatchModifyClusterSnapshotsResult,
    CancelResizeResult,
    ClusterResult,
    CopyClusterSnapshotResult,
    CreateAuthenticationProfileResult,
    CreateClusterSecurityGroupResult,
    CreateCustomDomainAssociationResult,
    CreateEndpointAccessResult,
    CreateEventSubscriptionResult,
    CreateHsmClientCertificateResult,
    CreateHsmConfigurationResult,
    CreateIntegrationResult,
    CreateRedshiftIdcApplicationResult,
    CreateScheduledActionResult,
    CreateSnapshotCopyGrantResult,
    CreateSnapshotScheduleResult,
    CreateUsageLimitResult,
    DeauthorizeDataShareResult,
    DeleteAuthenticationProfileResult,
    DeleteEndpointAccessResult,
    DeleteIntegrationResult,
    DeletePartnerResult,
    DeregisterNamespaceResult,
    DescribeAccountAttributesResult,
    DescribeAuthenticationProfilesResult,
    DescribeClusterDbRevisionsResult,
    DescribeClusterParameterGroupsResult,
    DescribeClusterParametersResult,
    DescribeClusterSecurityGroupsResult,
    DescribeClusterSubnetGroupsResult,
    DescribeClusterTracksResult,
    DescribeClusterVersionsResult,
    DescribeCustomDomainAssociationsResult,
    DescribeDataSharesForConsumerResult,
    DescribeDataSharesForProducerResult,
    DescribeDataSharesResult,
    DescribeDefaultClusterParametersResult,
    DescribeEndpointAccessResult,
    DescribeEndpointAuthorizationResult,
    DescribeEventCategoriesResult,
    DescribeEventsResult,
    DescribeEventSubscriptionsResult,
    DescribeHsmClientCertificatesResult,
    DescribeHsmConfigurationsResult,
    DescribeInboundIntegrationsResult,
    DescribeIntegrationsResult,
    DescribeNodeConfigurationOptionsResult,
    DescribeOrderableClusterOptionsResult,
    DescribePartnersResult,
    DescribeRedshiftIdcApplicationsResult,
    DescribeReservedNodeExchangeStatusResult,
    DescribeReservedNodeOfferingsResult,
    DescribeReservedNodesResult,
    DescribeResizeResult,
    DescribeScheduledActionsResult,
    DescribeSnapshotCopyGrantsResult,
    DescribeSnapshotSchedulesResult,
    DescribeStorageResult,
    DescribeTableRestoreStatusResult,
    DescribeTagsResult,
    DescribeUsageLimitsResult,
    DisableSnapshotCopyResult,
    DisassociateDataShareConsumerResult,
    EnableSnapshotCopyResult,
    FailoverPrimaryComputeResult,
    GetClusterCredentialsResult,
    GetClusterCredentialsWithIamResult,
    GetIdentityCenterAuthTokenResult,
    GetReservedNodeExchangeConfigurationOptionsResult,
    GetReservedNodeExchangeOfferingsResult,
    GetResourcePolicyResult,
    ListRecommendationsResult,
    LoggingStatus,
    ModifyAquaConfigurationResult,
    ModifyAuthenticationProfileResult,
    ModifyClusterDbRevisionResult,
    ModifyClusterIamRolesResult,
    ModifyClusterMaintenanceResult,
    ModifyClusterParameterGroupResult,
    ModifyClusterSnapshotResult,
    ModifyClusterSubnetGroupResult,
    ModifyCustomDomainAssociationResult,
    ModifyEndpointAccessResult,
    ModifyEventSubscriptionResult,
    ModifyIntegrationResult,
    ModifyRedshiftIdcApplicationResult,
    ModifyScheduledActionResult,
    ModifySnapshotCopyRetentionPeriodResult,
    ModifySnapshotScheduleResult,
    ModifyUsageLimitResult,
    ParameterGroupResult,
    PauseClusterResult,
    PurchaseReservedNodeOfferingResult,
    PutResourcePolicyResult,
    RegisterNamespaceResult,
    RejectDataShareResult,
    ResetClusterParameterGroupResult,
    ResizeClusterResult,
    RestoreTableFromClusterSnapshotResult,
    ResumeClusterResult,
    RevokeClusterSecurityGroupIngressResult,
    RevokeEndpointAccessResult,
    RevokeSnapshotAccessResult,
    RotateEncryptionKeyResult,
    SnapshotResult,
    SubnetGroupResult,
    UpdatePartnerStatusResult,
    _parse_cluster,
    _parse_snapshot,
)

__all__ = [
    "AcceptReservedNodeExchangeResult",
    "AddPartnerResult",
    "AssociateDataShareConsumerResult",
    "AuthorizeClusterSecurityGroupIngressResult",
    "AuthorizeDataShareResult",
    "AuthorizeEndpointAccessResult",
    "AuthorizeSnapshotAccessResult",
    "BatchDeleteClusterSnapshotsResult",
    "BatchModifyClusterSnapshotsResult",
    "CancelResizeResult",
    "ClusterResult",
    "CopyClusterSnapshotResult",
    "CreateAuthenticationProfileResult",
    "CreateClusterSecurityGroupResult",
    "CreateCustomDomainAssociationResult",
    "CreateEndpointAccessResult",
    "CreateEventSubscriptionResult",
    "CreateHsmClientCertificateResult",
    "CreateHsmConfigurationResult",
    "CreateIntegrationResult",
    "CreateRedshiftIdcApplicationResult",
    "CreateScheduledActionResult",
    "CreateSnapshotCopyGrantResult",
    "CreateSnapshotScheduleResult",
    "CreateUsageLimitResult",
    "DeauthorizeDataShareResult",
    "DeleteAuthenticationProfileResult",
    "DeleteEndpointAccessResult",
    "DeleteIntegrationResult",
    "DeletePartnerResult",
    "DeregisterNamespaceResult",
    "DescribeAccountAttributesResult",
    "DescribeAuthenticationProfilesResult",
    "DescribeClusterDbRevisionsResult",
    "DescribeClusterParameterGroupsResult",
    "DescribeClusterParametersResult",
    "DescribeClusterSecurityGroupsResult",
    "DescribeClusterSubnetGroupsResult",
    "DescribeClusterTracksResult",
    "DescribeClusterVersionsResult",
    "DescribeCustomDomainAssociationsResult",
    "DescribeDataSharesForConsumerResult",
    "DescribeDataSharesForProducerResult",
    "DescribeDataSharesResult",
    "DescribeDefaultClusterParametersResult",
    "DescribeEndpointAccessResult",
    "DescribeEndpointAuthorizationResult",
    "DescribeEventCategoriesResult",
    "DescribeEventSubscriptionsResult",
    "DescribeEventsResult",
    "DescribeHsmClientCertificatesResult",
    "DescribeHsmConfigurationsResult",
    "DescribeInboundIntegrationsResult",
    "DescribeIntegrationsResult",
    "DescribeNodeConfigurationOptionsResult",
    "DescribeOrderableClusterOptionsResult",
    "DescribePartnersResult",
    "DescribeRedshiftIdcApplicationsResult",
    "DescribeReservedNodeExchangeStatusResult",
    "DescribeReservedNodeOfferingsResult",
    "DescribeReservedNodesResult",
    "DescribeResizeResult",
    "DescribeScheduledActionsResult",
    "DescribeSnapshotCopyGrantsResult",
    "DescribeSnapshotSchedulesResult",
    "DescribeStorageResult",
    "DescribeTableRestoreStatusResult",
    "DescribeTagsResult",
    "DescribeUsageLimitsResult",
    "DisableSnapshotCopyResult",
    "DisassociateDataShareConsumerResult",
    "EnableSnapshotCopyResult",
    "FailoverPrimaryComputeResult",
    "GetClusterCredentialsResult",
    "GetClusterCredentialsWithIamResult",
    "GetIdentityCenterAuthTokenResult",
    "GetReservedNodeExchangeConfigurationOptionsResult",
    "GetReservedNodeExchangeOfferingsResult",
    "GetResourcePolicyResult",
    "ListRecommendationsResult",
    "LoggingStatus",
    "ModifyAquaConfigurationResult",
    "ModifyAuthenticationProfileResult",
    "ModifyClusterDbRevisionResult",
    "ModifyClusterIamRolesResult",
    "ModifyClusterMaintenanceResult",
    "ModifyClusterParameterGroupResult",
    "ModifyClusterSnapshotResult",
    "ModifyClusterSubnetGroupResult",
    "ModifyCustomDomainAssociationResult",
    "ModifyEndpointAccessResult",
    "ModifyEventSubscriptionResult",
    "ModifyIntegrationResult",
    "ModifyRedshiftIdcApplicationResult",
    "ModifyScheduledActionResult",
    "ModifySnapshotCopyRetentionPeriodResult",
    "ModifySnapshotScheduleResult",
    "ModifyUsageLimitResult",
    "ParameterGroupResult",
    "PauseClusterResult",
    "PurchaseReservedNodeOfferingResult",
    "PutResourcePolicyResult",
    "RegisterNamespaceResult",
    "RejectDataShareResult",
    "ResetClusterParameterGroupResult",
    "ResizeClusterResult",
    "RestoreTableFromClusterSnapshotResult",
    "ResumeClusterResult",
    "RevokeClusterSecurityGroupIngressResult",
    "RevokeEndpointAccessResult",
    "RevokeSnapshotAccessResult",
    "RotateEncryptionKeyResult",
    "SnapshotResult",
    "SubnetGroupResult",
    "UpdatePartnerStatusResult",
    "accept_reserved_node_exchange",
    "add_partner",
    "associate_data_share_consumer",
    "authorize_cluster_security_group_ingress",
    "authorize_data_share",
    "authorize_endpoint_access",
    "authorize_snapshot_access",
    "batch_delete_cluster_snapshots",
    "batch_modify_cluster_snapshots",
    "cancel_resize",
    "copy_cluster_snapshot",
    "create_authentication_profile",
    "create_cluster",
    "create_cluster_parameter_group",
    "create_cluster_security_group",
    "create_cluster_snapshot",
    "create_cluster_subnet_group",
    "create_custom_domain_association",
    "create_endpoint_access",
    "create_event_subscription",
    "create_hsm_client_certificate",
    "create_hsm_configuration",
    "create_integration",
    "create_redshift_idc_application",
    "create_scheduled_action",
    "create_snapshot_copy_grant",
    "create_snapshot_schedule",
    "create_tags",
    "create_usage_limit",
    "deauthorize_data_share",
    "delete_authentication_profile",
    "delete_cluster",
    "delete_cluster_parameter_group",
    "delete_cluster_security_group",
    "delete_cluster_snapshot",
    "delete_cluster_subnet_group",
    "delete_custom_domain_association",
    "delete_endpoint_access",
    "delete_event_subscription",
    "delete_hsm_client_certificate",
    "delete_hsm_configuration",
    "delete_integration",
    "delete_partner",
    "delete_redshift_idc_application",
    "delete_resource_policy",
    "delete_scheduled_action",
    "delete_snapshot_copy_grant",
    "delete_snapshot_schedule",
    "delete_tags",
    "delete_usage_limit",
    "deregister_namespace",
    "describe_account_attributes",
    "describe_authentication_profiles",
    "describe_cluster_db_revisions",
    "describe_cluster_parameter_groups",
    "describe_cluster_parameters",
    "describe_cluster_security_groups",
    "describe_cluster_snapshots",
    "describe_cluster_subnet_groups",
    "describe_cluster_tracks",
    "describe_cluster_versions",
    "describe_clusters",
    "describe_custom_domain_associations",
    "describe_data_shares",
    "describe_data_shares_for_consumer",
    "describe_data_shares_for_producer",
    "describe_default_cluster_parameters",
    "describe_endpoint_access",
    "describe_endpoint_authorization",
    "describe_event_categories",
    "describe_event_subscriptions",
    "describe_events",
    "describe_hsm_client_certificates",
    "describe_hsm_configurations",
    "describe_inbound_integrations",
    "describe_integrations",
    "describe_logging_status",
    "describe_node_configuration_options",
    "describe_orderable_cluster_options",
    "describe_partners",
    "describe_redshift_idc_applications",
    "describe_reserved_node_exchange_status",
    "describe_reserved_node_offerings",
    "describe_reserved_nodes",
    "describe_resize",
    "describe_scheduled_actions",
    "describe_snapshot_copy_grants",
    "describe_snapshot_schedules",
    "describe_storage",
    "describe_table_restore_status",
    "describe_tags",
    "describe_usage_limits",
    "disable_logging",
    "disable_snapshot_copy",
    "disassociate_data_share_consumer",
    "enable_logging",
    "enable_snapshot_copy",
    "failover_primary_compute",
    "get_cluster_credentials",
    "get_cluster_credentials_with_iam",
    "get_identity_center_auth_token",
    "get_reserved_node_exchange_configuration_options",
    "get_reserved_node_exchange_offerings",
    "get_resource_policy",
    "list_recommendations",
    "modify_aqua_configuration",
    "modify_authentication_profile",
    "modify_cluster",
    "modify_cluster_db_revision",
    "modify_cluster_iam_roles",
    "modify_cluster_maintenance",
    "modify_cluster_parameter_group",
    "modify_cluster_snapshot",
    "modify_cluster_snapshot_schedule",
    "modify_cluster_subnet_group",
    "modify_custom_domain_association",
    "modify_endpoint_access",
    "modify_event_subscription",
    "modify_integration",
    "modify_redshift_idc_application",
    "modify_scheduled_action",
    "modify_snapshot_copy_retention_period",
    "modify_snapshot_schedule",
    "modify_usage_limit",
    "pause_cluster",
    "purchase_reserved_node_offering",
    "put_resource_policy",
    "reboot_cluster",
    "register_namespace",
    "reject_data_share",
    "reset_cluster_parameter_group",
    "resize_cluster",
    "restore_from_cluster_snapshot",
    "restore_table_from_cluster_snapshot",
    "resume_cluster",
    "revoke_cluster_security_group_ingress",
    "revoke_endpoint_access",
    "revoke_snapshot_access",
    "rotate_encryption_key",
    "update_partner_status",
    "wait_for_cluster",
]


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def create_cluster(
    cluster_identifier: str,
    node_type: str,
    master_username: str,
    master_user_password: str,
    db_name: str = "dev",
    cluster_type: str = "single-node",
    number_of_nodes: int = 1,
    publicly_accessible: bool = False,
    encrypted: bool = False,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
    **extra: Any,
) -> ClusterResult:
    """Create a new Redshift cluster.

    Args:
        cluster_identifier: Unique identifier for the cluster.
        node_type: Node type (e.g. ``"dc2.large"``).
        master_username: Master user name.
        master_user_password: Master user password.
        db_name: Initial database name (default ``"dev"``).
        cluster_type: ``"single-node"`` or ``"multi-node"``.
        number_of_nodes: Number of compute nodes (multi-node only).
        publicly_accessible: Whether the cluster is publicly accessible.
        encrypted: Whether the cluster is encrypted at rest.
        tags: Optional key/value tags.
        region_name: AWS region override.
        **extra: Additional parameters.

    Returns:
        A :class:`ClusterResult` describing the new cluster.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ClusterIdentifier": cluster_identifier,
        "NodeType": node_type,
        "MasterUsername": master_username,
        "MasterUserPassword": master_user_password,
        "DBName": db_name,
        "ClusterType": cluster_type,
        "NumberOfNodes": number_of_nodes,
        "PubliclyAccessible": publicly_accessible,
        "Encrypted": encrypted,
        **extra,
    }
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create Redshift cluster {cluster_identifier!r}",
        ) from exc
    return _parse_cluster(resp["Cluster"])


async def describe_clusters(
    cluster_identifier: str | None = None,
    region_name: str | None = None,
) -> list[ClusterResult]:
    """Describe one or all Redshift clusters.

    Args:
        cluster_identifier: Specific cluster identifier.  ``None``
            returns all clusters.
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier:
        kwargs["ClusterIdentifier"] = cluster_identifier

    clusters: list[ClusterResult] = []
    try:
        marker: str | None = None
        while True:
            if marker:
                kwargs["Marker"] = marker
            resp = await client.call("DescribeClusters", **kwargs)
            for raw in resp.get("Clusters", []):
                clusters.append(_parse_cluster(raw))
            marker = resp.get("Marker")
            if not marker:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_clusters failed") from exc
    return clusters


async def delete_cluster(
    cluster_identifier: str,
    skip_final_snapshot: bool = True,
    final_snapshot_identifier: str | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Delete a Redshift cluster.

    Args:
        cluster_identifier: Identifier of the cluster to delete.
        skip_final_snapshot: If ``True``, no final snapshot is taken.
        final_snapshot_identifier: Identifier for the final snapshot
            (required when *skip_final_snapshot* is ``False``).
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult` describing the cluster being deleted.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ClusterIdentifier": cluster_identifier,
        "SkipFinalClusterSnapshot": skip_final_snapshot,
    }
    if final_snapshot_identifier:
        kwargs["FinalClusterSnapshotIdentifier"] = final_snapshot_identifier
    try:
        resp = await client.call("DeleteCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete Redshift cluster {cluster_identifier!r}",
        ) from exc
    return _parse_cluster(resp["Cluster"])


async def modify_cluster(
    cluster_identifier: str,
    region_name: str | None = None,
    **modifications: Any,
) -> ClusterResult:
    """Modify an existing Redshift cluster.

    Args:
        cluster_identifier: Identifier of the cluster to modify.
        region_name: AWS region override.
        **modifications: Keyword arguments forwarded to the boto3
            ``ModifyCluster`` API.

    Returns:
        A :class:`ClusterResult` with the updated cluster metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    try:
        resp = await client.call(
            "ModifyCluster",
            ClusterIdentifier=cluster_identifier,
            **modifications,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to modify Redshift cluster {cluster_identifier!r}",
        ) from exc
    return _parse_cluster(resp["Cluster"])


async def reboot_cluster(
    cluster_identifier: str,
    region_name: str | None = None,
) -> ClusterResult:
    """Reboot a Redshift cluster.

    Args:
        cluster_identifier: Identifier of the cluster to reboot.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult` describing the rebooting cluster.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    try:
        resp = await client.call(
            "RebootCluster",
            ClusterIdentifier=cluster_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to reboot Redshift cluster {cluster_identifier!r}",
        ) from exc
    return _parse_cluster(resp["Cluster"])


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def create_cluster_snapshot(
    snapshot_identifier: str,
    cluster_identifier: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> SnapshotResult:
    """Create a manual snapshot of a Redshift cluster.

    Args:
        snapshot_identifier: Identifier for the new snapshot.
        cluster_identifier: Source cluster identifier.
        tags: Optional key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`SnapshotResult` for the new snapshot.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "SnapshotIdentifier": snapshot_identifier,
        "ClusterIdentifier": cluster_identifier,
    }
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create snapshot {snapshot_identifier!r}",
        ) from exc
    return _parse_snapshot(resp["Snapshot"])


async def describe_cluster_snapshots(
    cluster_identifier: str | None = None,
    snapshot_identifier: str | None = None,
    snapshot_type: str = "manual",
    region_name: str | None = None,
) -> list[SnapshotResult]:
    """List Redshift cluster snapshots.

    Args:
        cluster_identifier: Filter to a specific cluster.
        snapshot_identifier: Filter to a specific snapshot.
        snapshot_type: ``"manual"`` (default) or ``"automated"``.
        region_name: AWS region override.

    Returns:
        A list of :class:`SnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {"SnapshotType": snapshot_type}
    if cluster_identifier:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if snapshot_identifier:
        kwargs["SnapshotIdentifier"] = snapshot_identifier

    snapshots: list[SnapshotResult] = []
    try:
        marker: str | None = None
        while True:
            if marker:
                kwargs["Marker"] = marker
            resp = await client.call("DescribeClusterSnapshots", **kwargs)
            for raw in resp.get("Snapshots", []):
                snapshots.append(_parse_snapshot(raw))
            marker = resp.get("Marker")
            if not marker:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_cluster_snapshots failed") from exc
    return snapshots


async def delete_cluster_snapshot(
    snapshot_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete a manual Redshift cluster snapshot.

    Args:
        snapshot_identifier: The snapshot identifier to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("redshift", region_name)
    try:
        await client.call(
            "DeleteClusterSnapshot",
            SnapshotIdentifier=snapshot_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to delete snapshot {snapshot_identifier!r}",
        ) from exc


async def restore_from_cluster_snapshot(
    cluster_identifier: str,
    snapshot_identifier: str,
    node_type: str | None = None,
    number_of_nodes: int | None = None,
    publicly_accessible: bool = False,
    region_name: str | None = None,
    **extra: Any,
) -> ClusterResult:
    """Restore a Redshift cluster from a snapshot.

    Args:
        cluster_identifier: Identifier for the new cluster.
        snapshot_identifier: Source snapshot identifier.
        node_type: Override node type for the restored cluster.
        number_of_nodes: Override number of nodes.
        publicly_accessible: Make the cluster publicly accessible.
        region_name: AWS region override.
        **extra: Additional parameters.

    Returns:
        A :class:`ClusterResult` for the restored cluster.

    Raises:
        RuntimeError: If the restore fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ClusterIdentifier": cluster_identifier,
        "SnapshotIdentifier": snapshot_identifier,
        "PubliclyAccessible": publicly_accessible,
        **extra,
    }
    if node_type:
        kwargs["NodeType"] = node_type
    if number_of_nodes is not None:
        kwargs["NumberOfNodes"] = number_of_nodes
    try:
        resp = await client.call("RestoreFromClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "restore_from_cluster_snapshot failed") from exc
    return _parse_cluster(resp["Cluster"])


# ---------------------------------------------------------------------------
# Parameter group & subnet group
# ---------------------------------------------------------------------------


async def create_cluster_parameter_group(
    parameter_group_name: str,
    parameter_group_family: str,
    description: str,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ParameterGroupResult:
    """Create a Redshift cluster parameter group.

    Args:
        parameter_group_name: Name for the parameter group.
        parameter_group_family: Family name (e.g. ``"redshift-1.0"``).
        description: A description of the parameter group.
        tags: Optional key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`ParameterGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ParameterGroupName": parameter_group_name,
        "ParameterGroupFamily": parameter_group_family,
        "Description": description,
    }
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create parameter group {parameter_group_name!r}",
        ) from exc
    pg = resp["ClusterParameterGroup"]
    return ParameterGroupResult(
        parameter_group_name=pg["ParameterGroupName"],
        parameter_group_family=pg["ParameterGroupFamily"],
        description=pg["Description"],
    )


async def create_cluster_subnet_group(
    cluster_subnet_group_name: str,
    description: str,
    subnet_ids: list[str],
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> SubnetGroupResult:
    """Create a Redshift cluster subnet group.

    Args:
        cluster_subnet_group_name: Name for the subnet group.
        description: A description of the subnet group.
        subnet_ids: List of VPC subnet IDs.
        tags: Optional key/value tags.
        region_name: AWS region override.

    Returns:
        A :class:`SubnetGroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ClusterSubnetGroupName": cluster_subnet_group_name,
        "Description": description,
        "SubnetIds": subnet_ids,
    }
    if tags:
        kwargs["Tags"] = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        resp = await client.call("CreateClusterSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to create subnet group {cluster_subnet_group_name!r}",
        ) from exc
    sg = resp["ClusterSubnetGroup"]
    subnet_ids_out = [s["SubnetIdentifier"] for s in sg.get("Subnets", [])]
    return SubnetGroupResult(
        cluster_subnet_group_name=sg["ClusterSubnetGroupName"],
        description=sg["Description"],
        vpc_id=sg.get("VpcId"),
        subnet_ids=subnet_ids_out,
        status=sg.get("SubnetGroupStatus"),
    )


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


async def describe_logging_status(
    cluster_identifier: str,
    region_name: str | None = None,
) -> LoggingStatus:
    """Get the audit-logging status for a Redshift cluster.

    Args:
        cluster_identifier: The cluster identifier.
        region_name: AWS region override.

    Returns:
        A :class:`LoggingStatus`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    try:
        resp = await client.call(
            "DescribeLoggingStatus",
            ClusterIdentifier=cluster_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to describe logging for {cluster_identifier!r}",
        ) from exc
    return LoggingStatus(
        logging_enabled=resp.get("LoggingEnabled", False),
        bucket_name=resp.get("BucketName"),
        s3_key_prefix=resp.get("S3KeyPrefix"),
    )


async def enable_logging(
    cluster_identifier: str,
    bucket_name: str,
    s3_key_prefix: str | None = None,
    region_name: str | None = None,
) -> LoggingStatus:
    """Enable audit logging for a Redshift cluster.

    Args:
        cluster_identifier: The cluster identifier.
        bucket_name: S3 bucket to store audit logs.
        s3_key_prefix: Optional prefix for log objects.
        region_name: AWS region override.

    Returns:
        A :class:`LoggingStatus` confirming the new state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {
        "ClusterIdentifier": cluster_identifier,
        "BucketName": bucket_name,
    }
    if s3_key_prefix:
        kwargs["S3KeyPrefix"] = s3_key_prefix
    try:
        resp = await client.call("EnableLogging", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to enable logging for {cluster_identifier!r}",
        ) from exc
    return LoggingStatus(
        logging_enabled=resp.get("LoggingEnabled", False),
        bucket_name=resp.get("BucketName"),
        s3_key_prefix=resp.get("S3KeyPrefix"),
    )


async def disable_logging(
    cluster_identifier: str,
    region_name: str | None = None,
) -> LoggingStatus:
    """Disable audit logging for a Redshift cluster.

    Args:
        cluster_identifier: The cluster identifier.
        region_name: AWS region override.

    Returns:
        A :class:`LoggingStatus` confirming logging is disabled.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    try:
        resp = await client.call(
            "DisableLogging",
            ClusterIdentifier=cluster_identifier,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to disable logging for {cluster_identifier!r}",
        ) from exc
    return LoggingStatus(
        logging_enabled=resp.get("LoggingEnabled", False),
        bucket_name=resp.get("BucketName"),
        s3_key_prefix=resp.get("S3KeyPrefix"),
    )


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


async def wait_for_cluster(
    cluster_identifier: str,
    target_status: str = "available",
    timeout: float = 1200.0,
    poll_interval: float = 30.0,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until a Redshift cluster reaches the desired status.

    Args:
        cluster_identifier: The cluster identifier.
        target_status: Target status (default ``"available"``).
        timeout: Maximum seconds to wait (default ``1200`` / 20 min).
        poll_interval: Seconds between polls (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` in the target status.

    Raises:
        AwsTimeoutError: If the cluster does not reach the target
            status in time.
        AwsServiceError: If the cluster is not found.
    """
    deadline = _time.monotonic() + timeout
    while True:
        results = await describe_clusters(cluster_identifier, region_name=region_name)
        if not results:
            raise AwsServiceError(f"Cluster {cluster_identifier!r} not found")
        cluster = results[0]
        if cluster.cluster_status == target_status:
            return cluster
        if _time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {cluster_identifier!r} did not reach "
                f"status {target_status!r} within {timeout}s "
                f"(current: {cluster.cluster_status!r})"
            )
        await asyncio.sleep(poll_interval)


async def accept_reserved_node_exchange(
    reserved_node_id: str,
    target_reserved_node_offering_id: str,
    region_name: str | None = None,
) -> AcceptReservedNodeExchangeResult:
    """Accept reserved node exchange.

    Args:
        reserved_node_id: Reserved node id.
        target_reserved_node_offering_id: Target reserved node offering id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedNodeId"] = reserved_node_id
    kwargs["TargetReservedNodeOfferingId"] = target_reserved_node_offering_id
    try:
        resp = await client.call("AcceptReservedNodeExchange", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to accept reserved node exchange") from exc
    return AcceptReservedNodeExchangeResult(
        exchanged_reserved_node=resp.get("ExchangedReservedNode"),
    )


async def add_partner(
    account_id: str,
    cluster_identifier: str,
    database_name: str,
    partner_name: str,
    region_name: str | None = None,
) -> AddPartnerResult:
    """Add partner.

    Args:
        account_id: Account id.
        cluster_identifier: Cluster identifier.
        database_name: Database name.
        partner_name: Partner name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["DatabaseName"] = database_name
    kwargs["PartnerName"] = partner_name
    try:
        resp = await client.call("AddPartner", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add partner") from exc
    return AddPartnerResult(
        database_name=resp.get("DatabaseName"),
        partner_name=resp.get("PartnerName"),
    )


async def associate_data_share_consumer(
    data_share_arn: str,
    *,
    associate_entire_account: bool | None = None,
    consumer_arn: str | None = None,
    consumer_region: str | None = None,
    allow_writes: bool | None = None,
    region_name: str | None = None,
) -> AssociateDataShareConsumerResult:
    """Associate data share consumer.

    Args:
        data_share_arn: Data share arn.
        associate_entire_account: Associate entire account.
        consumer_arn: Consumer arn.
        consumer_region: Consumer region.
        allow_writes: Allow writes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataShareArn"] = data_share_arn
    if associate_entire_account is not None:
        kwargs["AssociateEntireAccount"] = associate_entire_account
    if consumer_arn is not None:
        kwargs["ConsumerArn"] = consumer_arn
    if consumer_region is not None:
        kwargs["ConsumerRegion"] = consumer_region
    if allow_writes is not None:
        kwargs["AllowWrites"] = allow_writes
    try:
        resp = await client.call("AssociateDataShareConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate data share consumer") from exc
    return AssociateDataShareConsumerResult(
        data_share_arn=resp.get("DataShareArn"),
        producer_arn=resp.get("ProducerArn"),
        allow_publicly_accessible_consumers=resp.get("AllowPubliclyAccessibleConsumers"),
        data_share_associations=resp.get("DataShareAssociations"),
        managed_by=resp.get("ManagedBy"),
        data_share_type=resp.get("DataShareType"),
    )


async def authorize_cluster_security_group_ingress(
    cluster_security_group_name: str,
    *,
    cidrip: str | None = None,
    ec2_security_group_name: str | None = None,
    ec2_security_group_owner_id: str | None = None,
    region_name: str | None = None,
) -> AuthorizeClusterSecurityGroupIngressResult:
    """Authorize cluster security group ingress.

    Args:
        cluster_security_group_name: Cluster security group name.
        cidrip: Cidrip.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSecurityGroupName"] = cluster_security_group_name
    if cidrip is not None:
        kwargs["CIDRIP"] = cidrip
    if ec2_security_group_name is not None:
        kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    if ec2_security_group_owner_id is not None:
        kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = await client.call("AuthorizeClusterSecurityGroupIngress", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to authorize cluster security group ingress") from exc
    return AuthorizeClusterSecurityGroupIngressResult(
        cluster_security_group=resp.get("ClusterSecurityGroup"),
    )


async def authorize_data_share(
    data_share_arn: str,
    consumer_identifier: str,
    *,
    allow_writes: bool | None = None,
    region_name: str | None = None,
) -> AuthorizeDataShareResult:
    """Authorize data share.

    Args:
        data_share_arn: Data share arn.
        consumer_identifier: Consumer identifier.
        allow_writes: Allow writes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataShareArn"] = data_share_arn
    kwargs["ConsumerIdentifier"] = consumer_identifier
    if allow_writes is not None:
        kwargs["AllowWrites"] = allow_writes
    try:
        resp = await client.call("AuthorizeDataShare", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to authorize data share") from exc
    return AuthorizeDataShareResult(
        data_share_arn=resp.get("DataShareArn"),
        producer_arn=resp.get("ProducerArn"),
        allow_publicly_accessible_consumers=resp.get("AllowPubliclyAccessibleConsumers"),
        data_share_associations=resp.get("DataShareAssociations"),
        managed_by=resp.get("ManagedBy"),
        data_share_type=resp.get("DataShareType"),
    )


async def authorize_endpoint_access(
    account: str,
    *,
    cluster_identifier: str | None = None,
    vpc_ids: list[str] | None = None,
    region_name: str | None = None,
) -> AuthorizeEndpointAccessResult:
    """Authorize endpoint access.

    Args:
        account: Account.
        cluster_identifier: Cluster identifier.
        vpc_ids: Vpc ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Account"] = account
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if vpc_ids is not None:
        kwargs["VpcIds"] = vpc_ids
    try:
        resp = await client.call("AuthorizeEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to authorize endpoint access") from exc
    return AuthorizeEndpointAccessResult(
        grantor=resp.get("Grantor"),
        grantee=resp.get("Grantee"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        authorize_time=resp.get("AuthorizeTime"),
        cluster_status=resp.get("ClusterStatus"),
        status=resp.get("Status"),
        allowed_all_vp_cs=resp.get("AllowedAllVPCs"),
        allowed_vp_cs=resp.get("AllowedVPCs"),
        endpoint_count=resp.get("EndpointCount"),
    )


async def authorize_snapshot_access(
    account_with_restore_access: str,
    *,
    snapshot_identifier: str | None = None,
    snapshot_arn: str | None = None,
    snapshot_cluster_identifier: str | None = None,
    region_name: str | None = None,
) -> AuthorizeSnapshotAccessResult:
    """Authorize snapshot access.

    Args:
        account_with_restore_access: Account with restore access.
        snapshot_identifier: Snapshot identifier.
        snapshot_arn: Snapshot arn.
        snapshot_cluster_identifier: Snapshot cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountWithRestoreAccess"] = account_with_restore_access
    if snapshot_identifier is not None:
        kwargs["SnapshotIdentifier"] = snapshot_identifier
    if snapshot_arn is not None:
        kwargs["SnapshotArn"] = snapshot_arn
    if snapshot_cluster_identifier is not None:
        kwargs["SnapshotClusterIdentifier"] = snapshot_cluster_identifier
    try:
        resp = await client.call("AuthorizeSnapshotAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to authorize snapshot access") from exc
    return AuthorizeSnapshotAccessResult(
        snapshot=resp.get("Snapshot"),
    )


async def batch_delete_cluster_snapshots(
    identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchDeleteClusterSnapshotsResult:
    """Batch delete cluster snapshots.

    Args:
        identifiers: Identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifiers"] = identifiers
    try:
        resp = await client.call("BatchDeleteClusterSnapshots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete cluster snapshots") from exc
    return BatchDeleteClusterSnapshotsResult(
        resources=resp.get("Resources"),
        errors=resp.get("Errors"),
    )


async def batch_modify_cluster_snapshots(
    snapshot_identifier_list: list[str],
    *,
    manual_snapshot_retention_period: int | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> BatchModifyClusterSnapshotsResult:
    """Batch modify cluster snapshots.

    Args:
        snapshot_identifier_list: Snapshot identifier list.
        manual_snapshot_retention_period: Manual snapshot retention period.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SnapshotIdentifierList"] = snapshot_identifier_list
    if manual_snapshot_retention_period is not None:
        kwargs["ManualSnapshotRetentionPeriod"] = manual_snapshot_retention_period
    if force is not None:
        kwargs["Force"] = force
    try:
        resp = await client.call("BatchModifyClusterSnapshots", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch modify cluster snapshots") from exc
    return BatchModifyClusterSnapshotsResult(
        resources=resp.get("Resources"),
        errors=resp.get("Errors"),
    )


async def cancel_resize(
    cluster_identifier: str,
    region_name: str | None = None,
) -> CancelResizeResult:
    """Cancel resize.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("CancelResize", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel resize") from exc
    return CancelResizeResult(
        target_node_type=resp.get("TargetNodeType"),
        target_number_of_nodes=resp.get("TargetNumberOfNodes"),
        target_cluster_type=resp.get("TargetClusterType"),
        status=resp.get("Status"),
        import_tables_completed=resp.get("ImportTablesCompleted"),
        import_tables_in_progress=resp.get("ImportTablesInProgress"),
        import_tables_not_started=resp.get("ImportTablesNotStarted"),
        avg_resize_rate_in_mega_bytes_per_second=resp.get("AvgResizeRateInMegaBytesPerSecond"),
        total_resize_data_in_mega_bytes=resp.get("TotalResizeDataInMegaBytes"),
        progress_in_mega_bytes=resp.get("ProgressInMegaBytes"),
        elapsed_time_in_seconds=resp.get("ElapsedTimeInSeconds"),
        estimated_time_to_completion_in_seconds=resp.get("EstimatedTimeToCompletionInSeconds"),
        resize_type=resp.get("ResizeType"),
        message=resp.get("Message"),
        target_encryption_type=resp.get("TargetEncryptionType"),
        data_transfer_progress_percent=resp.get("DataTransferProgressPercent"),
    )


async def copy_cluster_snapshot(
    source_snapshot_identifier: str,
    target_snapshot_identifier: str,
    *,
    source_snapshot_cluster_identifier: str | None = None,
    manual_snapshot_retention_period: int | None = None,
    region_name: str | None = None,
) -> CopyClusterSnapshotResult:
    """Copy cluster snapshot.

    Args:
        source_snapshot_identifier: Source snapshot identifier.
        target_snapshot_identifier: Target snapshot identifier.
        source_snapshot_cluster_identifier: Source snapshot cluster identifier.
        manual_snapshot_retention_period: Manual snapshot retention period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceSnapshotIdentifier"] = source_snapshot_identifier
    kwargs["TargetSnapshotIdentifier"] = target_snapshot_identifier
    if source_snapshot_cluster_identifier is not None:
        kwargs["SourceSnapshotClusterIdentifier"] = source_snapshot_cluster_identifier
    if manual_snapshot_retention_period is not None:
        kwargs["ManualSnapshotRetentionPeriod"] = manual_snapshot_retention_period
    try:
        resp = await client.call("CopyClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to copy cluster snapshot") from exc
    return CopyClusterSnapshotResult(
        snapshot=resp.get("Snapshot"),
    )


async def create_authentication_profile(
    authentication_profile_name: str,
    authentication_profile_content: str,
    region_name: str | None = None,
) -> CreateAuthenticationProfileResult:
    """Create authentication profile.

    Args:
        authentication_profile_name: Authentication profile name.
        authentication_profile_content: Authentication profile content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationProfileName"] = authentication_profile_name
    kwargs["AuthenticationProfileContent"] = authentication_profile_content
    try:
        resp = await client.call("CreateAuthenticationProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create authentication profile") from exc
    return CreateAuthenticationProfileResult(
        authentication_profile_name=resp.get("AuthenticationProfileName"),
        authentication_profile_content=resp.get("AuthenticationProfileContent"),
    )


async def create_cluster_security_group(
    cluster_security_group_name: str,
    description: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateClusterSecurityGroupResult:
    """Create cluster security group.

    Args:
        cluster_security_group_name: Cluster security group name.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSecurityGroupName"] = cluster_security_group_name
    kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateClusterSecurityGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cluster security group") from exc
    return CreateClusterSecurityGroupResult(
        cluster_security_group=resp.get("ClusterSecurityGroup"),
    )


async def create_custom_domain_association(
    custom_domain_name: str,
    custom_domain_certificate_arn: str,
    cluster_identifier: str,
    region_name: str | None = None,
) -> CreateCustomDomainAssociationResult:
    """Create custom domain association.

    Args:
        custom_domain_name: Custom domain name.
        custom_domain_certificate_arn: Custom domain certificate arn.
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CustomDomainName"] = custom_domain_name
    kwargs["CustomDomainCertificateArn"] = custom_domain_certificate_arn
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("CreateCustomDomainAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom domain association") from exc
    return CreateCustomDomainAssociationResult(
        custom_domain_name=resp.get("CustomDomainName"),
        custom_domain_certificate_arn=resp.get("CustomDomainCertificateArn"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        custom_domain_cert_expiry_time=resp.get("CustomDomainCertExpiryTime"),
    )


async def create_endpoint_access(
    endpoint_name: str,
    subnet_group_name: str,
    *,
    cluster_identifier: str | None = None,
    resource_owner: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> CreateEndpointAccessResult:
    """Create endpoint access.

    Args:
        endpoint_name: Endpoint name.
        subnet_group_name: Subnet group name.
        cluster_identifier: Cluster identifier.
        resource_owner: Resource owner.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    kwargs["SubnetGroupName"] = subnet_group_name
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if resource_owner is not None:
        kwargs["ResourceOwner"] = resource_owner
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = await client.call("CreateEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create endpoint access") from exc
    return CreateEndpointAccessResult(
        cluster_identifier=resp.get("ClusterIdentifier"),
        resource_owner=resp.get("ResourceOwner"),
        subnet_group_name=resp.get("SubnetGroupName"),
        endpoint_status=resp.get("EndpointStatus"),
        endpoint_name=resp.get("EndpointName"),
        endpoint_create_time=resp.get("EndpointCreateTime"),
        port=resp.get("Port"),
        address=resp.get("Address"),
        vpc_security_groups=resp.get("VpcSecurityGroups"),
        vpc_endpoint=resp.get("VpcEndpoint"),
    )


async def create_event_subscription(
    subscription_name: str,
    sns_topic_arn: str,
    *,
    source_type: str | None = None,
    source_ids: list[str] | None = None,
    event_categories: list[str] | None = None,
    severity: str | None = None,
    enabled: bool | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateEventSubscriptionResult:
    """Create event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        source_ids: Source ids.
        event_categories: Event categories.
        severity: Severity.
        enabled: Enabled.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if source_ids is not None:
        kwargs["SourceIds"] = source_ids
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if severity is not None:
        kwargs["Severity"] = severity
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


async def create_hsm_client_certificate(
    hsm_client_certificate_identifier: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateHsmClientCertificateResult:
    """Create hsm client certificate.

    Args:
        hsm_client_certificate_identifier: Hsm client certificate identifier.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HsmClientCertificateIdentifier"] = hsm_client_certificate_identifier
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateHsmClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create hsm client certificate") from exc
    return CreateHsmClientCertificateResult(
        hsm_client_certificate=resp.get("HsmClientCertificate"),
    )


async def create_hsm_configuration(
    hsm_configuration_identifier: str,
    description: str,
    hsm_ip_address: str,
    hsm_partition_name: str,
    hsm_partition_password: str,
    hsm_server_public_certificate: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateHsmConfigurationResult:
    """Create hsm configuration.

    Args:
        hsm_configuration_identifier: Hsm configuration identifier.
        description: Description.
        hsm_ip_address: Hsm ip address.
        hsm_partition_name: Hsm partition name.
        hsm_partition_password: Hsm partition password.
        hsm_server_public_certificate: Hsm server public certificate.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HsmConfigurationIdentifier"] = hsm_configuration_identifier
    kwargs["Description"] = description
    kwargs["HsmIpAddress"] = hsm_ip_address
    kwargs["HsmPartitionName"] = hsm_partition_name
    kwargs["HsmPartitionPassword"] = hsm_partition_password
    kwargs["HsmServerPublicCertificate"] = hsm_server_public_certificate
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateHsmConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create hsm configuration") from exc
    return CreateHsmConfigurationResult(
        hsm_configuration=resp.get("HsmConfiguration"),
    )


async def create_integration(
    source_arn: str,
    target_arn: str,
    integration_name: str,
    *,
    kms_key_id: str | None = None,
    tag_list: list[dict[str, Any]] | None = None,
    additional_encryption_context: dict[str, Any] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateIntegrationResult:
    """Create integration.

    Args:
        source_arn: Source arn.
        target_arn: Target arn.
        integration_name: Integration name.
        kms_key_id: Kms key id.
        tag_list: Tag list.
        additional_encryption_context: Additional encryption context.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceArn"] = source_arn
    kwargs["TargetArn"] = target_arn
    kwargs["IntegrationName"] = integration_name
    if kms_key_id is not None:
        kwargs["KMSKeyId"] = kms_key_id
    if tag_list is not None:
        kwargs["TagList"] = tag_list
    if additional_encryption_context is not None:
        kwargs["AdditionalEncryptionContext"] = additional_encryption_context
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("CreateIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create integration") from exc
    return CreateIntegrationResult(
        integration_arn=resp.get("IntegrationArn"),
        integration_name=resp.get("IntegrationName"),
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        status=resp.get("Status"),
        errors=resp.get("Errors"),
        create_time=resp.get("CreateTime"),
        description=resp.get("Description"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
    )


async def create_redshift_idc_application(
    idc_instance_arn: str,
    redshift_idc_application_name: str,
    idc_display_name: str,
    iam_role_arn: str,
    *,
    identity_namespace: str | None = None,
    authorized_token_issuer_list: list[dict[str, Any]] | None = None,
    service_integrations: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    sso_tag_keys: list[str] | None = None,
    region_name: str | None = None,
) -> CreateRedshiftIdcApplicationResult:
    """Create redshift idc application.

    Args:
        idc_instance_arn: Idc instance arn.
        redshift_idc_application_name: Redshift idc application name.
        idc_display_name: Idc display name.
        iam_role_arn: Iam role arn.
        identity_namespace: Identity namespace.
        authorized_token_issuer_list: Authorized token issuer list.
        service_integrations: Service integrations.
        tags: Tags.
        sso_tag_keys: Sso tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdcInstanceArn"] = idc_instance_arn
    kwargs["RedshiftIdcApplicationName"] = redshift_idc_application_name
    kwargs["IdcDisplayName"] = idc_display_name
    kwargs["IamRoleArn"] = iam_role_arn
    if identity_namespace is not None:
        kwargs["IdentityNamespace"] = identity_namespace
    if authorized_token_issuer_list is not None:
        kwargs["AuthorizedTokenIssuerList"] = authorized_token_issuer_list
    if service_integrations is not None:
        kwargs["ServiceIntegrations"] = service_integrations
    if tags is not None:
        kwargs["Tags"] = tags
    if sso_tag_keys is not None:
        kwargs["SsoTagKeys"] = sso_tag_keys
    try:
        resp = await client.call("CreateRedshiftIdcApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create redshift idc application") from exc
    return CreateRedshiftIdcApplicationResult(
        redshift_idc_application=resp.get("RedshiftIdcApplication"),
    )


async def create_scheduled_action(
    scheduled_action_name: str,
    target_action: dict[str, Any],
    schedule: str,
    iam_role: str,
    *,
    scheduled_action_description: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    enable: bool | None = None,
    region_name: str | None = None,
) -> CreateScheduledActionResult:
    """Create scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        target_action: Target action.
        schedule: Schedule.
        iam_role: Iam role.
        scheduled_action_description: Scheduled action description.
        start_time: Start time.
        end_time: End time.
        enable: Enable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduledActionName"] = scheduled_action_name
    kwargs["TargetAction"] = target_action
    kwargs["Schedule"] = schedule
    kwargs["IamRole"] = iam_role
    if scheduled_action_description is not None:
        kwargs["ScheduledActionDescription"] = scheduled_action_description
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if enable is not None:
        kwargs["Enable"] = enable
    try:
        resp = await client.call("CreateScheduledAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create scheduled action") from exc
    return CreateScheduledActionResult(
        scheduled_action_name=resp.get("ScheduledActionName"),
        target_action=resp.get("TargetAction"),
        schedule=resp.get("Schedule"),
        iam_role=resp.get("IamRole"),
        scheduled_action_description=resp.get("ScheduledActionDescription"),
        state=resp.get("State"),
        next_invocations=resp.get("NextInvocations"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
    )


async def create_snapshot_copy_grant(
    snapshot_copy_grant_name: str,
    *,
    kms_key_id: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateSnapshotCopyGrantResult:
    """Create snapshot copy grant.

    Args:
        snapshot_copy_grant_name: Snapshot copy grant name.
        kms_key_id: Kms key id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SnapshotCopyGrantName"] = snapshot_copy_grant_name
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateSnapshotCopyGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot copy grant") from exc
    return CreateSnapshotCopyGrantResult(
        snapshot_copy_grant=resp.get("SnapshotCopyGrant"),
    )


async def create_snapshot_schedule(
    *,
    schedule_definitions: list[str] | None = None,
    schedule_identifier: str | None = None,
    schedule_description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    next_invocations: int | None = None,
    region_name: str | None = None,
) -> CreateSnapshotScheduleResult:
    """Create snapshot schedule.

    Args:
        schedule_definitions: Schedule definitions.
        schedule_identifier: Schedule identifier.
        schedule_description: Schedule description.
        tags: Tags.
        next_invocations: Next invocations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if schedule_definitions is not None:
        kwargs["ScheduleDefinitions"] = schedule_definitions
    if schedule_identifier is not None:
        kwargs["ScheduleIdentifier"] = schedule_identifier
    if schedule_description is not None:
        kwargs["ScheduleDescription"] = schedule_description
    if tags is not None:
        kwargs["Tags"] = tags
    if next_invocations is not None:
        kwargs["NextInvocations"] = next_invocations
    try:
        resp = await client.call("CreateSnapshotSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot schedule") from exc
    return CreateSnapshotScheduleResult(
        schedule_definitions=resp.get("ScheduleDefinitions"),
        schedule_identifier=resp.get("ScheduleIdentifier"),
        schedule_description=resp.get("ScheduleDescription"),
        tags=resp.get("Tags"),
        next_invocations=resp.get("NextInvocations"),
        associated_cluster_count=resp.get("AssociatedClusterCount"),
        associated_clusters=resp.get("AssociatedClusters"),
    )


async def create_tags(
    resource_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Create tags.

    Args:
        resource_name: Resource name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["Tags"] = tags
    try:
        await client.call("CreateTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create tags") from exc
    return None


async def create_usage_limit(
    cluster_identifier: str,
    feature_type: str,
    limit_type: str,
    amount: int,
    *,
    period: str | None = None,
    breach_action: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateUsageLimitResult:
    """Create usage limit.

    Args:
        cluster_identifier: Cluster identifier.
        feature_type: Feature type.
        limit_type: Limit type.
        amount: Amount.
        period: Period.
        breach_action: Breach action.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["FeatureType"] = feature_type
    kwargs["LimitType"] = limit_type
    kwargs["Amount"] = amount
    if period is not None:
        kwargs["Period"] = period
    if breach_action is not None:
        kwargs["BreachAction"] = breach_action
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateUsageLimit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create usage limit") from exc
    return CreateUsageLimitResult(
        usage_limit_id=resp.get("UsageLimitId"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        feature_type=resp.get("FeatureType"),
        limit_type=resp.get("LimitType"),
        amount=resp.get("Amount"),
        period=resp.get("Period"),
        breach_action=resp.get("BreachAction"),
        tags=resp.get("Tags"),
    )


async def deauthorize_data_share(
    data_share_arn: str,
    consumer_identifier: str,
    region_name: str | None = None,
) -> DeauthorizeDataShareResult:
    """Deauthorize data share.

    Args:
        data_share_arn: Data share arn.
        consumer_identifier: Consumer identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataShareArn"] = data_share_arn
    kwargs["ConsumerIdentifier"] = consumer_identifier
    try:
        resp = await client.call("DeauthorizeDataShare", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deauthorize data share") from exc
    return DeauthorizeDataShareResult(
        data_share_arn=resp.get("DataShareArn"),
        producer_arn=resp.get("ProducerArn"),
        allow_publicly_accessible_consumers=resp.get("AllowPubliclyAccessibleConsumers"),
        data_share_associations=resp.get("DataShareAssociations"),
        managed_by=resp.get("ManagedBy"),
        data_share_type=resp.get("DataShareType"),
    )


async def delete_authentication_profile(
    authentication_profile_name: str,
    region_name: str | None = None,
) -> DeleteAuthenticationProfileResult:
    """Delete authentication profile.

    Args:
        authentication_profile_name: Authentication profile name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationProfileName"] = authentication_profile_name
    try:
        resp = await client.call("DeleteAuthenticationProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete authentication profile") from exc
    return DeleteAuthenticationProfileResult(
        authentication_profile_name=resp.get("AuthenticationProfileName"),
    )


async def delete_cluster_parameter_group(
    parameter_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cluster parameter group.

    Args:
        parameter_group_name: Parameter group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    try:
        await client.call("DeleteClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cluster parameter group") from exc
    return None


async def delete_cluster_security_group(
    cluster_security_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cluster security group.

    Args:
        cluster_security_group_name: Cluster security group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSecurityGroupName"] = cluster_security_group_name
    try:
        await client.call("DeleteClusterSecurityGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cluster security group") from exc
    return None


async def delete_cluster_subnet_group(
    cluster_subnet_group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete cluster subnet group.

    Args:
        cluster_subnet_group_name: Cluster subnet group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSubnetGroupName"] = cluster_subnet_group_name
    try:
        await client.call("DeleteClusterSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cluster subnet group") from exc
    return None


async def delete_custom_domain_association(
    cluster_identifier: str,
    custom_domain_name: str,
    region_name: str | None = None,
) -> None:
    """Delete custom domain association.

    Args:
        cluster_identifier: Cluster identifier.
        custom_domain_name: Custom domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["CustomDomainName"] = custom_domain_name
    try:
        await client.call("DeleteCustomDomainAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom domain association") from exc
    return None


async def delete_endpoint_access(
    endpoint_name: str,
    region_name: str | None = None,
) -> DeleteEndpointAccessResult:
    """Delete endpoint access.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    try:
        resp = await client.call("DeleteEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete endpoint access") from exc
    return DeleteEndpointAccessResult(
        cluster_identifier=resp.get("ClusterIdentifier"),
        resource_owner=resp.get("ResourceOwner"),
        subnet_group_name=resp.get("SubnetGroupName"),
        endpoint_status=resp.get("EndpointStatus"),
        endpoint_name=resp.get("EndpointName"),
        endpoint_create_time=resp.get("EndpointCreateTime"),
        port=resp.get("Port"),
        address=resp.get("Address"),
        vpc_security_groups=resp.get("VpcSecurityGroups"),
        vpc_endpoint=resp.get("VpcEndpoint"),
    )


async def delete_event_subscription(
    subscription_name: str,
    region_name: str | None = None,
) -> None:
    """Delete event subscription.

    Args:
        subscription_name: Subscription name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    try:
        await client.call("DeleteEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete event subscription") from exc
    return None


async def delete_hsm_client_certificate(
    hsm_client_certificate_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete hsm client certificate.

    Args:
        hsm_client_certificate_identifier: Hsm client certificate identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HsmClientCertificateIdentifier"] = hsm_client_certificate_identifier
    try:
        await client.call("DeleteHsmClientCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete hsm client certificate") from exc
    return None


async def delete_hsm_configuration(
    hsm_configuration_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete hsm configuration.

    Args:
        hsm_configuration_identifier: Hsm configuration identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HsmConfigurationIdentifier"] = hsm_configuration_identifier
    try:
        await client.call("DeleteHsmConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete hsm configuration") from exc
    return None


async def delete_integration(
    integration_arn: str,
    region_name: str | None = None,
) -> DeleteIntegrationResult:
    """Delete integration.

    Args:
        integration_arn: Integration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationArn"] = integration_arn
    try:
        resp = await client.call("DeleteIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete integration") from exc
    return DeleteIntegrationResult(
        integration_arn=resp.get("IntegrationArn"),
        integration_name=resp.get("IntegrationName"),
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        status=resp.get("Status"),
        errors=resp.get("Errors"),
        create_time=resp.get("CreateTime"),
        description=resp.get("Description"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
    )


async def delete_partner(
    account_id: str,
    cluster_identifier: str,
    database_name: str,
    partner_name: str,
    region_name: str | None = None,
) -> DeletePartnerResult:
    """Delete partner.

    Args:
        account_id: Account id.
        cluster_identifier: Cluster identifier.
        database_name: Database name.
        partner_name: Partner name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["DatabaseName"] = database_name
    kwargs["PartnerName"] = partner_name
    try:
        resp = await client.call("DeletePartner", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete partner") from exc
    return DeletePartnerResult(
        database_name=resp.get("DatabaseName"),
        partner_name=resp.get("PartnerName"),
    )


async def delete_redshift_idc_application(
    redshift_idc_application_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete redshift idc application.

    Args:
        redshift_idc_application_arn: Redshift idc application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RedshiftIdcApplicationArn"] = redshift_idc_application_arn
    try:
        await client.call("DeleteRedshiftIdcApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete redshift idc application") from exc
    return None


async def delete_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def delete_scheduled_action(
    scheduled_action_name: str,
    region_name: str | None = None,
) -> None:
    """Delete scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduledActionName"] = scheduled_action_name
    try:
        await client.call("DeleteScheduledAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduled action") from exc
    return None


async def delete_snapshot_copy_grant(
    snapshot_copy_grant_name: str,
    region_name: str | None = None,
) -> None:
    """Delete snapshot copy grant.

    Args:
        snapshot_copy_grant_name: Snapshot copy grant name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SnapshotCopyGrantName"] = snapshot_copy_grant_name
    try:
        await client.call("DeleteSnapshotCopyGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot copy grant") from exc
    return None


async def delete_snapshot_schedule(
    schedule_identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete snapshot schedule.

    Args:
        schedule_identifier: Schedule identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduleIdentifier"] = schedule_identifier
    try:
        await client.call("DeleteSnapshotSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot schedule") from exc
    return None


async def delete_tags(
    resource_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Delete tags.

    Args:
        resource_name: Resource name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceName"] = resource_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("DeleteTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete tags") from exc
    return None


async def delete_usage_limit(
    usage_limit_id: str,
    region_name: str | None = None,
) -> None:
    """Delete usage limit.

    Args:
        usage_limit_id: Usage limit id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UsageLimitId"] = usage_limit_id
    try:
        await client.call("DeleteUsageLimit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete usage limit") from exc
    return None


async def deregister_namespace(
    namespace_identifier: dict[str, Any],
    consumer_identifiers: list[str],
    region_name: str | None = None,
) -> DeregisterNamespaceResult:
    """Deregister namespace.

    Args:
        namespace_identifier: Namespace identifier.
        consumer_identifiers: Consumer identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamespaceIdentifier"] = namespace_identifier
    kwargs["ConsumerIdentifiers"] = consumer_identifiers
    try:
        resp = await client.call("DeregisterNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister namespace") from exc
    return DeregisterNamespaceResult(
        status=resp.get("Status"),
    )


async def describe_account_attributes(
    *,
    attribute_names: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeAccountAttributesResult:
    """Describe account attributes.

    Args:
        attribute_names: Attribute names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if attribute_names is not None:
        kwargs["AttributeNames"] = attribute_names
    try:
        resp = await client.call("DescribeAccountAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account attributes") from exc
    return DescribeAccountAttributesResult(
        account_attributes=resp.get("AccountAttributes"),
    )


async def describe_authentication_profiles(
    *,
    authentication_profile_name: str | None = None,
    region_name: str | None = None,
) -> DescribeAuthenticationProfilesResult:
    """Describe authentication profiles.

    Args:
        authentication_profile_name: Authentication profile name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if authentication_profile_name is not None:
        kwargs["AuthenticationProfileName"] = authentication_profile_name
    try:
        resp = await client.call("DescribeAuthenticationProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe authentication profiles") from exc
    return DescribeAuthenticationProfilesResult(
        authentication_profiles=resp.get("AuthenticationProfiles"),
    )


async def describe_cluster_db_revisions(
    *,
    cluster_identifier: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeClusterDbRevisionsResult:
    """Describe cluster db revisions.

    Args:
        cluster_identifier: Cluster identifier.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeClusterDbRevisions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster db revisions") from exc
    return DescribeClusterDbRevisionsResult(
        marker=resp.get("Marker"),
        cluster_db_revisions=resp.get("ClusterDbRevisions"),
    )


async def describe_cluster_parameter_groups(
    *,
    parameter_group_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeClusterParameterGroupsResult:
    """Describe cluster parameter groups.

    Args:
        parameter_group_name: Parameter group name.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if parameter_group_name is not None:
        kwargs["ParameterGroupName"] = parameter_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeClusterParameterGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster parameter groups") from exc
    return DescribeClusterParameterGroupsResult(
        marker=resp.get("Marker"),
        parameter_groups=resp.get("ParameterGroups"),
    )


async def describe_cluster_parameters(
    parameter_group_name: str,
    *,
    source: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeClusterParametersResult:
    """Describe cluster parameters.

    Args:
        parameter_group_name: Parameter group name.
        source: Source.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    if source is not None:
        kwargs["Source"] = source
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeClusterParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster parameters") from exc
    return DescribeClusterParametersResult(
        parameters=resp.get("Parameters"),
        marker=resp.get("Marker"),
    )


async def describe_cluster_security_groups(
    *,
    cluster_security_group_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeClusterSecurityGroupsResult:
    """Describe cluster security groups.

    Args:
        cluster_security_group_name: Cluster security group name.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_security_group_name is not None:
        kwargs["ClusterSecurityGroupName"] = cluster_security_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeClusterSecurityGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster security groups") from exc
    return DescribeClusterSecurityGroupsResult(
        marker=resp.get("Marker"),
        cluster_security_groups=resp.get("ClusterSecurityGroups"),
    )


async def describe_cluster_subnet_groups(
    *,
    cluster_subnet_group_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeClusterSubnetGroupsResult:
    """Describe cluster subnet groups.

    Args:
        cluster_subnet_group_name: Cluster subnet group name.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_subnet_group_name is not None:
        kwargs["ClusterSubnetGroupName"] = cluster_subnet_group_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeClusterSubnetGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster subnet groups") from exc
    return DescribeClusterSubnetGroupsResult(
        marker=resp.get("Marker"),
        cluster_subnet_groups=resp.get("ClusterSubnetGroups"),
    )


async def describe_cluster_tracks(
    *,
    maintenance_track_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeClusterTracksResult:
    """Describe cluster tracks.

    Args:
        maintenance_track_name: Maintenance track name.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if maintenance_track_name is not None:
        kwargs["MaintenanceTrackName"] = maintenance_track_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeClusterTracks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster tracks") from exc
    return DescribeClusterTracksResult(
        maintenance_tracks=resp.get("MaintenanceTracks"),
        marker=resp.get("Marker"),
    )


async def describe_cluster_versions(
    *,
    cluster_version: str | None = None,
    cluster_parameter_group_family: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeClusterVersionsResult:
    """Describe cluster versions.

    Args:
        cluster_version: Cluster version.
        cluster_parameter_group_family: Cluster parameter group family.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_version is not None:
        kwargs["ClusterVersion"] = cluster_version
    if cluster_parameter_group_family is not None:
        kwargs["ClusterParameterGroupFamily"] = cluster_parameter_group_family
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeClusterVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster versions") from exc
    return DescribeClusterVersionsResult(
        marker=resp.get("Marker"),
        cluster_versions=resp.get("ClusterVersions"),
    )


async def describe_custom_domain_associations(
    *,
    custom_domain_name: str | None = None,
    custom_domain_certificate_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeCustomDomainAssociationsResult:
    """Describe custom domain associations.

    Args:
        custom_domain_name: Custom domain name.
        custom_domain_certificate_arn: Custom domain certificate arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if custom_domain_name is not None:
        kwargs["CustomDomainName"] = custom_domain_name
    if custom_domain_certificate_arn is not None:
        kwargs["CustomDomainCertificateArn"] = custom_domain_certificate_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeCustomDomainAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe custom domain associations") from exc
    return DescribeCustomDomainAssociationsResult(
        marker=resp.get("Marker"),
        associations=resp.get("Associations"),
    )


async def describe_data_shares(
    *,
    data_share_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDataSharesResult:
    """Describe data shares.

    Args:
        data_share_arn: Data share arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if data_share_arn is not None:
        kwargs["DataShareArn"] = data_share_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDataShares", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data shares") from exc
    return DescribeDataSharesResult(
        data_shares=resp.get("DataShares"),
        marker=resp.get("Marker"),
    )


async def describe_data_shares_for_consumer(
    *,
    consumer_arn: str | None = None,
    status: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDataSharesForConsumerResult:
    """Describe data shares for consumer.

    Args:
        consumer_arn: Consumer arn.
        status: Status.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if consumer_arn is not None:
        kwargs["ConsumerArn"] = consumer_arn
    if status is not None:
        kwargs["Status"] = status
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDataSharesForConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data shares for consumer") from exc
    return DescribeDataSharesForConsumerResult(
        data_shares=resp.get("DataShares"),
        marker=resp.get("Marker"),
    )


async def describe_data_shares_for_producer(
    *,
    producer_arn: str | None = None,
    status: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDataSharesForProducerResult:
    """Describe data shares for producer.

    Args:
        producer_arn: Producer arn.
        status: Status.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if producer_arn is not None:
        kwargs["ProducerArn"] = producer_arn
    if status is not None:
        kwargs["Status"] = status
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDataSharesForProducer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe data shares for producer") from exc
    return DescribeDataSharesForProducerResult(
        data_shares=resp.get("DataShares"),
        marker=resp.get("Marker"),
    )


async def describe_default_cluster_parameters(
    parameter_group_family: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeDefaultClusterParametersResult:
    """Describe default cluster parameters.

    Args:
        parameter_group_family: Parameter group family.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupFamily"] = parameter_group_family
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeDefaultClusterParameters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe default cluster parameters") from exc
    return DescribeDefaultClusterParametersResult(
        default_cluster_parameters=resp.get("DefaultClusterParameters"),
    )


async def describe_endpoint_access(
    *,
    cluster_identifier: str | None = None,
    resource_owner: str | None = None,
    endpoint_name: str | None = None,
    vpc_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointAccessResult:
    """Describe endpoint access.

    Args:
        cluster_identifier: Cluster identifier.
        resource_owner: Resource owner.
        endpoint_name: Endpoint name.
        vpc_id: Vpc id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if resource_owner is not None:
        kwargs["ResourceOwner"] = resource_owner
    if endpoint_name is not None:
        kwargs["EndpointName"] = endpoint_name
    if vpc_id is not None:
        kwargs["VpcId"] = vpc_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint access") from exc
    return DescribeEndpointAccessResult(
        endpoint_access_list=resp.get("EndpointAccessList"),
        marker=resp.get("Marker"),
    )


async def describe_endpoint_authorization(
    *,
    cluster_identifier: str | None = None,
    account: str | None = None,
    grantee: bool | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointAuthorizationResult:
    """Describe endpoint authorization.

    Args:
        cluster_identifier: Cluster identifier.
        account: Account.
        grantee: Grantee.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if account is not None:
        kwargs["Account"] = account
    if grantee is not None:
        kwargs["Grantee"] = grantee
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeEndpointAuthorization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint authorization") from exc
    return DescribeEndpointAuthorizationResult(
        endpoint_authorization_list=resp.get("EndpointAuthorizationList"),
        marker=resp.get("Marker"),
    )


async def describe_event_categories(
    *,
    source_type: str | None = None,
    region_name: str | None = None,
) -> DescribeEventCategoriesResult:
    """Describe event categories.

    Args:
        source_type: Source type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if source_type is not None:
        kwargs["SourceType"] = source_type
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
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeEventSubscriptionsResult:
    """Describe event subscriptions.

    Args:
        subscription_name: Subscription name.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if subscription_name is not None:
        kwargs["SubscriptionName"] = subscription_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
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
    client = async_client("redshift", region_name)
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
        resp = await client.call("DescribeEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe events") from exc
    return DescribeEventsResult(
        marker=resp.get("Marker"),
        events=resp.get("Events"),
    )


async def describe_hsm_client_certificates(
    *,
    hsm_client_certificate_identifier: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeHsmClientCertificatesResult:
    """Describe hsm client certificates.

    Args:
        hsm_client_certificate_identifier: Hsm client certificate identifier.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if hsm_client_certificate_identifier is not None:
        kwargs["HsmClientCertificateIdentifier"] = hsm_client_certificate_identifier
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeHsmClientCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe hsm client certificates") from exc
    return DescribeHsmClientCertificatesResult(
        marker=resp.get("Marker"),
        hsm_client_certificates=resp.get("HsmClientCertificates"),
    )


async def describe_hsm_configurations(
    *,
    hsm_configuration_identifier: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeHsmConfigurationsResult:
    """Describe hsm configurations.

    Args:
        hsm_configuration_identifier: Hsm configuration identifier.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if hsm_configuration_identifier is not None:
        kwargs["HsmConfigurationIdentifier"] = hsm_configuration_identifier
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeHsmConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe hsm configurations") from exc
    return DescribeHsmConfigurationsResult(
        marker=resp.get("Marker"),
        hsm_configurations=resp.get("HsmConfigurations"),
    )


async def describe_inbound_integrations(
    *,
    integration_arn: str | None = None,
    target_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeInboundIntegrationsResult:
    """Describe inbound integrations.

    Args:
        integration_arn: Integration arn.
        target_arn: Target arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if integration_arn is not None:
        kwargs["IntegrationArn"] = integration_arn
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeInboundIntegrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe inbound integrations") from exc
    return DescribeInboundIntegrationsResult(
        marker=resp.get("Marker"),
        inbound_integrations=resp.get("InboundIntegrations"),
    )


async def describe_integrations(
    *,
    integration_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeIntegrationsResult:
    """Describe integrations.

    Args:
        integration_arn: Integration arn.
        max_records: Max records.
        marker: Marker.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if integration_arn is not None:
        kwargs["IntegrationArn"] = integration_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("DescribeIntegrations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe integrations") from exc
    return DescribeIntegrationsResult(
        marker=resp.get("Marker"),
        integrations=resp.get("Integrations"),
    )


async def describe_node_configuration_options(
    action_type: str,
    *,
    cluster_identifier: str | None = None,
    snapshot_identifier: str | None = None,
    snapshot_arn: str | None = None,
    owner_account: str | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeNodeConfigurationOptionsResult:
    """Describe node configuration options.

    Args:
        action_type: Action type.
        cluster_identifier: Cluster identifier.
        snapshot_identifier: Snapshot identifier.
        snapshot_arn: Snapshot arn.
        owner_account: Owner account.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionType"] = action_type
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if snapshot_identifier is not None:
        kwargs["SnapshotIdentifier"] = snapshot_identifier
    if snapshot_arn is not None:
        kwargs["SnapshotArn"] = snapshot_arn
    if owner_account is not None:
        kwargs["OwnerAccount"] = owner_account
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeNodeConfigurationOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe node configuration options") from exc
    return DescribeNodeConfigurationOptionsResult(
        node_configuration_option_list=resp.get("NodeConfigurationOptionList"),
        marker=resp.get("Marker"),
    )


async def describe_orderable_cluster_options(
    *,
    cluster_version: str | None = None,
    node_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeOrderableClusterOptionsResult:
    """Describe orderable cluster options.

    Args:
        cluster_version: Cluster version.
        node_type: Node type.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_version is not None:
        kwargs["ClusterVersion"] = cluster_version
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeOrderableClusterOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe orderable cluster options") from exc
    return DescribeOrderableClusterOptionsResult(
        orderable_cluster_options=resp.get("OrderableClusterOptions"),
        marker=resp.get("Marker"),
    )


async def describe_partners(
    account_id: str,
    cluster_identifier: str,
    *,
    database_name: str | None = None,
    partner_name: str | None = None,
    region_name: str | None = None,
) -> DescribePartnersResult:
    """Describe partners.

    Args:
        account_id: Account id.
        cluster_identifier: Cluster identifier.
        database_name: Database name.
        partner_name: Partner name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ClusterIdentifier"] = cluster_identifier
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if partner_name is not None:
        kwargs["PartnerName"] = partner_name
    try:
        resp = await client.call("DescribePartners", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe partners") from exc
    return DescribePartnersResult(
        partner_integration_info_list=resp.get("PartnerIntegrationInfoList"),
    )


async def describe_redshift_idc_applications(
    *,
    redshift_idc_application_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeRedshiftIdcApplicationsResult:
    """Describe redshift idc applications.

    Args:
        redshift_idc_application_arn: Redshift idc application arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if redshift_idc_application_arn is not None:
        kwargs["RedshiftIdcApplicationArn"] = redshift_idc_application_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeRedshiftIdcApplications", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe redshift idc applications") from exc
    return DescribeRedshiftIdcApplicationsResult(
        redshift_idc_applications=resp.get("RedshiftIdcApplications"),
        marker=resp.get("Marker"),
    )


async def describe_reserved_node_exchange_status(
    *,
    reserved_node_id: str | None = None,
    reserved_node_exchange_request_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedNodeExchangeStatusResult:
    """Describe reserved node exchange status.

    Args:
        reserved_node_id: Reserved node id.
        reserved_node_exchange_request_id: Reserved node exchange request id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_node_id is not None:
        kwargs["ReservedNodeId"] = reserved_node_id
    if reserved_node_exchange_request_id is not None:
        kwargs["ReservedNodeExchangeRequestId"] = reserved_node_exchange_request_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReservedNodeExchangeStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved node exchange status") from exc
    return DescribeReservedNodeExchangeStatusResult(
        reserved_node_exchange_status_details=resp.get("ReservedNodeExchangeStatusDetails"),
        marker=resp.get("Marker"),
    )


async def describe_reserved_node_offerings(
    *,
    reserved_node_offering_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedNodeOfferingsResult:
    """Describe reserved node offerings.

    Args:
        reserved_node_offering_id: Reserved node offering id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_node_offering_id is not None:
        kwargs["ReservedNodeOfferingId"] = reserved_node_offering_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReservedNodeOfferings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved node offerings") from exc
    return DescribeReservedNodeOfferingsResult(
        marker=resp.get("Marker"),
        reserved_node_offerings=resp.get("ReservedNodeOfferings"),
    )


async def describe_reserved_nodes(
    *,
    reserved_node_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeReservedNodesResult:
    """Describe reserved nodes.

    Args:
        reserved_node_id: Reserved node id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if reserved_node_id is not None:
        kwargs["ReservedNodeId"] = reserved_node_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeReservedNodes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe reserved nodes") from exc
    return DescribeReservedNodesResult(
        marker=resp.get("Marker"),
        reserved_nodes=resp.get("ReservedNodes"),
    )


async def describe_resize(
    cluster_identifier: str,
    region_name: str | None = None,
) -> DescribeResizeResult:
    """Describe resize.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("DescribeResize", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe resize") from exc
    return DescribeResizeResult(
        target_node_type=resp.get("TargetNodeType"),
        target_number_of_nodes=resp.get("TargetNumberOfNodes"),
        target_cluster_type=resp.get("TargetClusterType"),
        status=resp.get("Status"),
        import_tables_completed=resp.get("ImportTablesCompleted"),
        import_tables_in_progress=resp.get("ImportTablesInProgress"),
        import_tables_not_started=resp.get("ImportTablesNotStarted"),
        avg_resize_rate_in_mega_bytes_per_second=resp.get("AvgResizeRateInMegaBytesPerSecond"),
        total_resize_data_in_mega_bytes=resp.get("TotalResizeDataInMegaBytes"),
        progress_in_mega_bytes=resp.get("ProgressInMegaBytes"),
        elapsed_time_in_seconds=resp.get("ElapsedTimeInSeconds"),
        estimated_time_to_completion_in_seconds=resp.get("EstimatedTimeToCompletionInSeconds"),
        resize_type=resp.get("ResizeType"),
        message=resp.get("Message"),
        target_encryption_type=resp.get("TargetEncryptionType"),
        data_transfer_progress_percent=resp.get("DataTransferProgressPercent"),
    )


async def describe_scheduled_actions(
    *,
    scheduled_action_name: str | None = None,
    target_action_type: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    active: bool | None = None,
    filters: list[dict[str, Any]] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeScheduledActionsResult:
    """Describe scheduled actions.

    Args:
        scheduled_action_name: Scheduled action name.
        target_action_type: Target action type.
        start_time: Start time.
        end_time: End time.
        active: Active.
        filters: Filters.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if scheduled_action_name is not None:
        kwargs["ScheduledActionName"] = scheduled_action_name
    if target_action_type is not None:
        kwargs["TargetActionType"] = target_action_type
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if active is not None:
        kwargs["Active"] = active
    if filters is not None:
        kwargs["Filters"] = filters
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeScheduledActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduled actions") from exc
    return DescribeScheduledActionsResult(
        marker=resp.get("Marker"),
        scheduled_actions=resp.get("ScheduledActions"),
    )


async def describe_snapshot_copy_grants(
    *,
    snapshot_copy_grant_name: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeSnapshotCopyGrantsResult:
    """Describe snapshot copy grants.

    Args:
        snapshot_copy_grant_name: Snapshot copy grant name.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if snapshot_copy_grant_name is not None:
        kwargs["SnapshotCopyGrantName"] = snapshot_copy_grant_name
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeSnapshotCopyGrants", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe snapshot copy grants") from exc
    return DescribeSnapshotCopyGrantsResult(
        marker=resp.get("Marker"),
        snapshot_copy_grants=resp.get("SnapshotCopyGrants"),
    )


async def describe_snapshot_schedules(
    *,
    cluster_identifier: str | None = None,
    schedule_identifier: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    marker: str | None = None,
    max_records: int | None = None,
    region_name: str | None = None,
) -> DescribeSnapshotSchedulesResult:
    """Describe snapshot schedules.

    Args:
        cluster_identifier: Cluster identifier.
        schedule_identifier: Schedule identifier.
        tag_keys: Tag keys.
        tag_values: Tag values.
        marker: Marker.
        max_records: Max records.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if schedule_identifier is not None:
        kwargs["ScheduleIdentifier"] = schedule_identifier
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    if marker is not None:
        kwargs["Marker"] = marker
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    try:
        resp = await client.call("DescribeSnapshotSchedules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe snapshot schedules") from exc
    return DescribeSnapshotSchedulesResult(
        snapshot_schedules=resp.get("SnapshotSchedules"),
        marker=resp.get("Marker"),
    )


async def describe_storage(
    region_name: str | None = None,
) -> DescribeStorageResult:
    """Describe storage.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeStorage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe storage") from exc
    return DescribeStorageResult(
        total_backup_size_in_mega_bytes=resp.get("TotalBackupSizeInMegaBytes"),
        total_provisioned_storage_in_mega_bytes=resp.get("TotalProvisionedStorageInMegaBytes"),
    )


async def describe_table_restore_status(
    *,
    cluster_identifier: str | None = None,
    table_restore_request_id: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> DescribeTableRestoreStatusResult:
    """Describe table restore status.

    Args:
        cluster_identifier: Cluster identifier.
        table_restore_request_id: Table restore request id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if table_restore_request_id is not None:
        kwargs["TableRestoreRequestId"] = table_restore_request_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("DescribeTableRestoreStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe table restore status") from exc
    return DescribeTableRestoreStatusResult(
        table_restore_status_details=resp.get("TableRestoreStatusDetails"),
        marker=resp.get("Marker"),
    )


async def describe_tags(
    *,
    resource_name: str | None = None,
    resource_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeTagsResult:
    """Describe tags.

    Args:
        resource_name: Resource name.
        resource_type: Resource type.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if resource_name is not None:
        kwargs["ResourceName"] = resource_name
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe tags") from exc
    return DescribeTagsResult(
        tagged_resources=resp.get("TaggedResources"),
        marker=resp.get("Marker"),
    )


async def describe_usage_limits(
    *,
    usage_limit_id: str | None = None,
    cluster_identifier: str | None = None,
    feature_type: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    tag_keys: list[str] | None = None,
    tag_values: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeUsageLimitsResult:
    """Describe usage limits.

    Args:
        usage_limit_id: Usage limit id.
        cluster_identifier: Cluster identifier.
        feature_type: Feature type.
        max_records: Max records.
        marker: Marker.
        tag_keys: Tag keys.
        tag_values: Tag values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if usage_limit_id is not None:
        kwargs["UsageLimitId"] = usage_limit_id
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if feature_type is not None:
        kwargs["FeatureType"] = feature_type
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    if tag_keys is not None:
        kwargs["TagKeys"] = tag_keys
    if tag_values is not None:
        kwargs["TagValues"] = tag_values
    try:
        resp = await client.call("DescribeUsageLimits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe usage limits") from exc
    return DescribeUsageLimitsResult(
        usage_limits=resp.get("UsageLimits"),
        marker=resp.get("Marker"),
    )


async def disable_snapshot_copy(
    cluster_identifier: str,
    region_name: str | None = None,
) -> DisableSnapshotCopyResult:
    """Disable snapshot copy.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("DisableSnapshotCopy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable snapshot copy") from exc
    return DisableSnapshotCopyResult(
        cluster=resp.get("Cluster"),
    )


async def disassociate_data_share_consumer(
    data_share_arn: str,
    *,
    disassociate_entire_account: bool | None = None,
    consumer_arn: str | None = None,
    consumer_region: str | None = None,
    region_name: str | None = None,
) -> DisassociateDataShareConsumerResult:
    """Disassociate data share consumer.

    Args:
        data_share_arn: Data share arn.
        disassociate_entire_account: Disassociate entire account.
        consumer_arn: Consumer arn.
        consumer_region: Consumer region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataShareArn"] = data_share_arn
    if disassociate_entire_account is not None:
        kwargs["DisassociateEntireAccount"] = disassociate_entire_account
    if consumer_arn is not None:
        kwargs["ConsumerArn"] = consumer_arn
    if consumer_region is not None:
        kwargs["ConsumerRegion"] = consumer_region
    try:
        resp = await client.call("DisassociateDataShareConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate data share consumer") from exc
    return DisassociateDataShareConsumerResult(
        data_share_arn=resp.get("DataShareArn"),
        producer_arn=resp.get("ProducerArn"),
        allow_publicly_accessible_consumers=resp.get("AllowPubliclyAccessibleConsumers"),
        data_share_associations=resp.get("DataShareAssociations"),
        managed_by=resp.get("ManagedBy"),
        data_share_type=resp.get("DataShareType"),
    )


async def enable_snapshot_copy(
    cluster_identifier: str,
    destination_region: str,
    *,
    retention_period: int | None = None,
    snapshot_copy_grant_name: str | None = None,
    manual_snapshot_retention_period: int | None = None,
    region_name: str | None = None,
) -> EnableSnapshotCopyResult:
    """Enable snapshot copy.

    Args:
        cluster_identifier: Cluster identifier.
        destination_region: Destination region.
        retention_period: Retention period.
        snapshot_copy_grant_name: Snapshot copy grant name.
        manual_snapshot_retention_period: Manual snapshot retention period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["DestinationRegion"] = destination_region
    if retention_period is not None:
        kwargs["RetentionPeriod"] = retention_period
    if snapshot_copy_grant_name is not None:
        kwargs["SnapshotCopyGrantName"] = snapshot_copy_grant_name
    if manual_snapshot_retention_period is not None:
        kwargs["ManualSnapshotRetentionPeriod"] = manual_snapshot_retention_period
    try:
        resp = await client.call("EnableSnapshotCopy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable snapshot copy") from exc
    return EnableSnapshotCopyResult(
        cluster=resp.get("Cluster"),
    )


async def failover_primary_compute(
    cluster_identifier: str,
    region_name: str | None = None,
) -> FailoverPrimaryComputeResult:
    """Failover primary compute.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("FailoverPrimaryCompute", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to failover primary compute") from exc
    return FailoverPrimaryComputeResult(
        cluster=resp.get("Cluster"),
    )


async def get_cluster_credentials(
    db_user: str,
    *,
    db_name: str | None = None,
    cluster_identifier: str | None = None,
    duration_seconds: int | None = None,
    auto_create: bool | None = None,
    db_groups: list[str] | None = None,
    custom_domain_name: str | None = None,
    region_name: str | None = None,
) -> GetClusterCredentialsResult:
    """Get cluster credentials.

    Args:
        db_user: Db user.
        db_name: Db name.
        cluster_identifier: Cluster identifier.
        duration_seconds: Duration seconds.
        auto_create: Auto create.
        db_groups: Db groups.
        custom_domain_name: Custom domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DbUser"] = db_user
    if db_name is not None:
        kwargs["DbName"] = db_name
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    if auto_create is not None:
        kwargs["AutoCreate"] = auto_create
    if db_groups is not None:
        kwargs["DbGroups"] = db_groups
    if custom_domain_name is not None:
        kwargs["CustomDomainName"] = custom_domain_name
    try:
        resp = await client.call("GetClusterCredentials", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cluster credentials") from exc
    return GetClusterCredentialsResult(
        db_user=resp.get("DbUser"),
        db_password=resp.get("DbPassword"),
        expiration=resp.get("Expiration"),
    )


async def get_cluster_credentials_with_iam(
    *,
    db_name: str | None = None,
    cluster_identifier: str | None = None,
    duration_seconds: int | None = None,
    custom_domain_name: str | None = None,
    region_name: str | None = None,
) -> GetClusterCredentialsWithIamResult:
    """Get cluster credentials with iam.

    Args:
        db_name: Db name.
        cluster_identifier: Cluster identifier.
        duration_seconds: Duration seconds.
        custom_domain_name: Custom domain name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if db_name is not None:
        kwargs["DbName"] = db_name
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    if custom_domain_name is not None:
        kwargs["CustomDomainName"] = custom_domain_name
    try:
        resp = await client.call("GetClusterCredentialsWithIAM", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cluster credentials with iam") from exc
    return GetClusterCredentialsWithIamResult(
        db_user=resp.get("DbUser"),
        db_password=resp.get("DbPassword"),
        expiration=resp.get("Expiration"),
        next_refresh_time=resp.get("NextRefreshTime"),
    )


async def get_identity_center_auth_token(
    cluster_ids: list[str],
    region_name: str | None = None,
) -> GetIdentityCenterAuthTokenResult:
    """Get identity center auth token.

    Args:
        cluster_ids: Cluster ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIds"] = cluster_ids
    try:
        resp = await client.call("GetIdentityCenterAuthToken", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get identity center auth token") from exc
    return GetIdentityCenterAuthTokenResult(
        token=resp.get("Token"),
        expiration_time=resp.get("ExpirationTime"),
    )


async def get_reserved_node_exchange_configuration_options(
    action_type: str,
    *,
    cluster_identifier: str | None = None,
    snapshot_identifier: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> GetReservedNodeExchangeConfigurationOptionsResult:
    """Get reserved node exchange configuration options.

    Args:
        action_type: Action type.
        cluster_identifier: Cluster identifier.
        snapshot_identifier: Snapshot identifier.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionType"] = action_type
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if snapshot_identifier is not None:
        kwargs["SnapshotIdentifier"] = snapshot_identifier
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("GetReservedNodeExchangeConfigurationOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to get reserved node exchange configuration options"
        ) from exc
    return GetReservedNodeExchangeConfigurationOptionsResult(
        marker=resp.get("Marker"),
        reserved_node_configuration_option_list=resp.get("ReservedNodeConfigurationOptionList"),
    )


async def get_reserved_node_exchange_offerings(
    reserved_node_id: str,
    *,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> GetReservedNodeExchangeOfferingsResult:
    """Get reserved node exchange offerings.

    Args:
        reserved_node_id: Reserved node id.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedNodeId"] = reserved_node_id
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("GetReservedNodeExchangeOfferings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get reserved node exchange offerings") from exc
    return GetReservedNodeExchangeOfferingsResult(
        marker=resp.get("Marker"),
        reserved_node_offerings=resp.get("ReservedNodeOfferings"),
    )


async def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_policy=resp.get("ResourcePolicy"),
    )


async def list_recommendations(
    *,
    cluster_identifier: str | None = None,
    namespace_arn: str | None = None,
    max_records: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListRecommendationsResult:
    """List recommendations.

    Args:
        cluster_identifier: Cluster identifier.
        namespace_arn: Namespace arn.
        max_records: Max records.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if namespace_arn is not None:
        kwargs["NamespaceArn"] = namespace_arn
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("ListRecommendations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list recommendations") from exc
    return ListRecommendationsResult(
        recommendations=resp.get("Recommendations"),
        marker=resp.get("Marker"),
    )


async def modify_aqua_configuration(
    cluster_identifier: str,
    *,
    aqua_configuration_status: str | None = None,
    region_name: str | None = None,
) -> ModifyAquaConfigurationResult:
    """Modify aqua configuration.

    Args:
        cluster_identifier: Cluster identifier.
        aqua_configuration_status: Aqua configuration status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    if aqua_configuration_status is not None:
        kwargs["AquaConfigurationStatus"] = aqua_configuration_status
    try:
        resp = await client.call("ModifyAquaConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify aqua configuration") from exc
    return ModifyAquaConfigurationResult(
        aqua_configuration=resp.get("AquaConfiguration"),
    )


async def modify_authentication_profile(
    authentication_profile_name: str,
    authentication_profile_content: str,
    region_name: str | None = None,
) -> ModifyAuthenticationProfileResult:
    """Modify authentication profile.

    Args:
        authentication_profile_name: Authentication profile name.
        authentication_profile_content: Authentication profile content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationProfileName"] = authentication_profile_name
    kwargs["AuthenticationProfileContent"] = authentication_profile_content
    try:
        resp = await client.call("ModifyAuthenticationProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify authentication profile") from exc
    return ModifyAuthenticationProfileResult(
        authentication_profile_name=resp.get("AuthenticationProfileName"),
        authentication_profile_content=resp.get("AuthenticationProfileContent"),
    )


async def modify_cluster_db_revision(
    cluster_identifier: str,
    revision_target: str,
    region_name: str | None = None,
) -> ModifyClusterDbRevisionResult:
    """Modify cluster db revision.

    Args:
        cluster_identifier: Cluster identifier.
        revision_target: Revision target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["RevisionTarget"] = revision_target
    try:
        resp = await client.call("ModifyClusterDbRevision", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster db revision") from exc
    return ModifyClusterDbRevisionResult(
        cluster=resp.get("Cluster"),
    )


async def modify_cluster_iam_roles(
    cluster_identifier: str,
    *,
    add_iam_roles: list[str] | None = None,
    remove_iam_roles: list[str] | None = None,
    default_iam_role_arn: str | None = None,
    region_name: str | None = None,
) -> ModifyClusterIamRolesResult:
    """Modify cluster iam roles.

    Args:
        cluster_identifier: Cluster identifier.
        add_iam_roles: Add iam roles.
        remove_iam_roles: Remove iam roles.
        default_iam_role_arn: Default iam role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    if add_iam_roles is not None:
        kwargs["AddIamRoles"] = add_iam_roles
    if remove_iam_roles is not None:
        kwargs["RemoveIamRoles"] = remove_iam_roles
    if default_iam_role_arn is not None:
        kwargs["DefaultIamRoleArn"] = default_iam_role_arn
    try:
        resp = await client.call("ModifyClusterIamRoles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster iam roles") from exc
    return ModifyClusterIamRolesResult(
        cluster=resp.get("Cluster"),
    )


async def modify_cluster_maintenance(
    cluster_identifier: str,
    *,
    defer_maintenance: bool | None = None,
    defer_maintenance_identifier: str | None = None,
    defer_maintenance_start_time: str | None = None,
    defer_maintenance_end_time: str | None = None,
    defer_maintenance_duration: int | None = None,
    region_name: str | None = None,
) -> ModifyClusterMaintenanceResult:
    """Modify cluster maintenance.

    Args:
        cluster_identifier: Cluster identifier.
        defer_maintenance: Defer maintenance.
        defer_maintenance_identifier: Defer maintenance identifier.
        defer_maintenance_start_time: Defer maintenance start time.
        defer_maintenance_end_time: Defer maintenance end time.
        defer_maintenance_duration: Defer maintenance duration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    if defer_maintenance is not None:
        kwargs["DeferMaintenance"] = defer_maintenance
    if defer_maintenance_identifier is not None:
        kwargs["DeferMaintenanceIdentifier"] = defer_maintenance_identifier
    if defer_maintenance_start_time is not None:
        kwargs["DeferMaintenanceStartTime"] = defer_maintenance_start_time
    if defer_maintenance_end_time is not None:
        kwargs["DeferMaintenanceEndTime"] = defer_maintenance_end_time
    if defer_maintenance_duration is not None:
        kwargs["DeferMaintenanceDuration"] = defer_maintenance_duration
    try:
        resp = await client.call("ModifyClusterMaintenance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster maintenance") from exc
    return ModifyClusterMaintenanceResult(
        cluster=resp.get("Cluster"),
    )


async def modify_cluster_parameter_group(
    parameter_group_name: str,
    parameters: list[dict[str, Any]],
    region_name: str | None = None,
) -> ModifyClusterParameterGroupResult:
    """Modify cluster parameter group.

    Args:
        parameter_group_name: Parameter group name.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ModifyClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster parameter group") from exc
    return ModifyClusterParameterGroupResult(
        parameter_group_name=resp.get("ParameterGroupName"),
        parameter_group_status=resp.get("ParameterGroupStatus"),
    )


async def modify_cluster_snapshot(
    snapshot_identifier: str,
    *,
    manual_snapshot_retention_period: int | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> ModifyClusterSnapshotResult:
    """Modify cluster snapshot.

    Args:
        snapshot_identifier: Snapshot identifier.
        manual_snapshot_retention_period: Manual snapshot retention period.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SnapshotIdentifier"] = snapshot_identifier
    if manual_snapshot_retention_period is not None:
        kwargs["ManualSnapshotRetentionPeriod"] = manual_snapshot_retention_period
    if force is not None:
        kwargs["Force"] = force
    try:
        resp = await client.call("ModifyClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster snapshot") from exc
    return ModifyClusterSnapshotResult(
        snapshot=resp.get("Snapshot"),
    )


async def modify_cluster_snapshot_schedule(
    cluster_identifier: str,
    *,
    schedule_identifier: str | None = None,
    disassociate_schedule: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Modify cluster snapshot schedule.

    Args:
        cluster_identifier: Cluster identifier.
        schedule_identifier: Schedule identifier.
        disassociate_schedule: Disassociate schedule.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    if schedule_identifier is not None:
        kwargs["ScheduleIdentifier"] = schedule_identifier
    if disassociate_schedule is not None:
        kwargs["DisassociateSchedule"] = disassociate_schedule
    try:
        await client.call("ModifyClusterSnapshotSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster snapshot schedule") from exc
    return None


async def modify_cluster_subnet_group(
    cluster_subnet_group_name: str,
    subnet_ids: list[str],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> ModifyClusterSubnetGroupResult:
    """Modify cluster subnet group.

    Args:
        cluster_subnet_group_name: Cluster subnet group name.
        subnet_ids: Subnet ids.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSubnetGroupName"] = cluster_subnet_group_name
    kwargs["SubnetIds"] = subnet_ids
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("ModifyClusterSubnetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify cluster subnet group") from exc
    return ModifyClusterSubnetGroupResult(
        cluster_subnet_group=resp.get("ClusterSubnetGroup"),
    )


async def modify_custom_domain_association(
    custom_domain_name: str,
    custom_domain_certificate_arn: str,
    cluster_identifier: str,
    region_name: str | None = None,
) -> ModifyCustomDomainAssociationResult:
    """Modify custom domain association.

    Args:
        custom_domain_name: Custom domain name.
        custom_domain_certificate_arn: Custom domain certificate arn.
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CustomDomainName"] = custom_domain_name
    kwargs["CustomDomainCertificateArn"] = custom_domain_certificate_arn
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("ModifyCustomDomainAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify custom domain association") from exc
    return ModifyCustomDomainAssociationResult(
        custom_domain_name=resp.get("CustomDomainName"),
        custom_domain_certificate_arn=resp.get("CustomDomainCertificateArn"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        custom_domain_cert_expiry_time=resp.get("CustomDomainCertExpiryTime"),
    )


async def modify_endpoint_access(
    endpoint_name: str,
    *,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> ModifyEndpointAccessResult:
    """Modify endpoint access.

    Args:
        endpoint_name: Endpoint name.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EndpointName"] = endpoint_name
    if vpc_security_group_ids is not None:
        kwargs["VpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = await client.call("ModifyEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify endpoint access") from exc
    return ModifyEndpointAccessResult(
        cluster_identifier=resp.get("ClusterIdentifier"),
        resource_owner=resp.get("ResourceOwner"),
        subnet_group_name=resp.get("SubnetGroupName"),
        endpoint_status=resp.get("EndpointStatus"),
        endpoint_name=resp.get("EndpointName"),
        endpoint_create_time=resp.get("EndpointCreateTime"),
        port=resp.get("Port"),
        address=resp.get("Address"),
        vpc_security_groups=resp.get("VpcSecurityGroups"),
        vpc_endpoint=resp.get("VpcEndpoint"),
    )


async def modify_event_subscription(
    subscription_name: str,
    *,
    sns_topic_arn: str | None = None,
    source_type: str | None = None,
    source_ids: list[str] | None = None,
    event_categories: list[str] | None = None,
    severity: str | None = None,
    enabled: bool | None = None,
    region_name: str | None = None,
) -> ModifyEventSubscriptionResult:
    """Modify event subscription.

    Args:
        subscription_name: Subscription name.
        sns_topic_arn: Sns topic arn.
        source_type: Source type.
        source_ids: Source ids.
        event_categories: Event categories.
        severity: Severity.
        enabled: Enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SubscriptionName"] = subscription_name
    if sns_topic_arn is not None:
        kwargs["SnsTopicArn"] = sns_topic_arn
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if source_ids is not None:
        kwargs["SourceIds"] = source_ids
    if event_categories is not None:
        kwargs["EventCategories"] = event_categories
    if severity is not None:
        kwargs["Severity"] = severity
    if enabled is not None:
        kwargs["Enabled"] = enabled
    try:
        resp = await client.call("ModifyEventSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify event subscription") from exc
    return ModifyEventSubscriptionResult(
        event_subscription=resp.get("EventSubscription"),
    )


async def modify_integration(
    integration_arn: str,
    *,
    description: str | None = None,
    integration_name: str | None = None,
    region_name: str | None = None,
) -> ModifyIntegrationResult:
    """Modify integration.

    Args:
        integration_arn: Integration arn.
        description: Description.
        integration_name: Integration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IntegrationArn"] = integration_arn
    if description is not None:
        kwargs["Description"] = description
    if integration_name is not None:
        kwargs["IntegrationName"] = integration_name
    try:
        resp = await client.call("ModifyIntegration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify integration") from exc
    return ModifyIntegrationResult(
        integration_arn=resp.get("IntegrationArn"),
        integration_name=resp.get("IntegrationName"),
        source_arn=resp.get("SourceArn"),
        target_arn=resp.get("TargetArn"),
        status=resp.get("Status"),
        errors=resp.get("Errors"),
        create_time=resp.get("CreateTime"),
        description=resp.get("Description"),
        kms_key_id=resp.get("KMSKeyId"),
        additional_encryption_context=resp.get("AdditionalEncryptionContext"),
        tags=resp.get("Tags"),
    )


async def modify_redshift_idc_application(
    redshift_idc_application_arn: str,
    *,
    identity_namespace: str | None = None,
    iam_role_arn: str | None = None,
    idc_display_name: str | None = None,
    authorized_token_issuer_list: list[dict[str, Any]] | None = None,
    service_integrations: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ModifyRedshiftIdcApplicationResult:
    """Modify redshift idc application.

    Args:
        redshift_idc_application_arn: Redshift idc application arn.
        identity_namespace: Identity namespace.
        iam_role_arn: Iam role arn.
        idc_display_name: Idc display name.
        authorized_token_issuer_list: Authorized token issuer list.
        service_integrations: Service integrations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RedshiftIdcApplicationArn"] = redshift_idc_application_arn
    if identity_namespace is not None:
        kwargs["IdentityNamespace"] = identity_namespace
    if iam_role_arn is not None:
        kwargs["IamRoleArn"] = iam_role_arn
    if idc_display_name is not None:
        kwargs["IdcDisplayName"] = idc_display_name
    if authorized_token_issuer_list is not None:
        kwargs["AuthorizedTokenIssuerList"] = authorized_token_issuer_list
    if service_integrations is not None:
        kwargs["ServiceIntegrations"] = service_integrations
    try:
        resp = await client.call("ModifyRedshiftIdcApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify redshift idc application") from exc
    return ModifyRedshiftIdcApplicationResult(
        redshift_idc_application=resp.get("RedshiftIdcApplication"),
    )


async def modify_scheduled_action(
    scheduled_action_name: str,
    *,
    target_action: dict[str, Any] | None = None,
    schedule: str | None = None,
    iam_role: str | None = None,
    scheduled_action_description: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    enable: bool | None = None,
    region_name: str | None = None,
) -> ModifyScheduledActionResult:
    """Modify scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        target_action: Target action.
        schedule: Schedule.
        iam_role: Iam role.
        scheduled_action_description: Scheduled action description.
        start_time: Start time.
        end_time: End time.
        enable: Enable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduledActionName"] = scheduled_action_name
    if target_action is not None:
        kwargs["TargetAction"] = target_action
    if schedule is not None:
        kwargs["Schedule"] = schedule
    if iam_role is not None:
        kwargs["IamRole"] = iam_role
    if scheduled_action_description is not None:
        kwargs["ScheduledActionDescription"] = scheduled_action_description
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if enable is not None:
        kwargs["Enable"] = enable
    try:
        resp = await client.call("ModifyScheduledAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify scheduled action") from exc
    return ModifyScheduledActionResult(
        scheduled_action_name=resp.get("ScheduledActionName"),
        target_action=resp.get("TargetAction"),
        schedule=resp.get("Schedule"),
        iam_role=resp.get("IamRole"),
        scheduled_action_description=resp.get("ScheduledActionDescription"),
        state=resp.get("State"),
        next_invocations=resp.get("NextInvocations"),
        start_time=resp.get("StartTime"),
        end_time=resp.get("EndTime"),
    )


async def modify_snapshot_copy_retention_period(
    cluster_identifier: str,
    retention_period: int,
    *,
    manual: bool | None = None,
    region_name: str | None = None,
) -> ModifySnapshotCopyRetentionPeriodResult:
    """Modify snapshot copy retention period.

    Args:
        cluster_identifier: Cluster identifier.
        retention_period: Retention period.
        manual: Manual.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["RetentionPeriod"] = retention_period
    if manual is not None:
        kwargs["Manual"] = manual
    try:
        resp = await client.call("ModifySnapshotCopyRetentionPeriod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify snapshot copy retention period") from exc
    return ModifySnapshotCopyRetentionPeriodResult(
        cluster=resp.get("Cluster"),
    )


async def modify_snapshot_schedule(
    schedule_identifier: str,
    schedule_definitions: list[str],
    region_name: str | None = None,
) -> ModifySnapshotScheduleResult:
    """Modify snapshot schedule.

    Args:
        schedule_identifier: Schedule identifier.
        schedule_definitions: Schedule definitions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduleIdentifier"] = schedule_identifier
    kwargs["ScheduleDefinitions"] = schedule_definitions
    try:
        resp = await client.call("ModifySnapshotSchedule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify snapshot schedule") from exc
    return ModifySnapshotScheduleResult(
        schedule_definitions=resp.get("ScheduleDefinitions"),
        schedule_identifier=resp.get("ScheduleIdentifier"),
        schedule_description=resp.get("ScheduleDescription"),
        tags=resp.get("Tags"),
        next_invocations=resp.get("NextInvocations"),
        associated_cluster_count=resp.get("AssociatedClusterCount"),
        associated_clusters=resp.get("AssociatedClusters"),
    )


async def modify_usage_limit(
    usage_limit_id: str,
    *,
    amount: int | None = None,
    breach_action: str | None = None,
    region_name: str | None = None,
) -> ModifyUsageLimitResult:
    """Modify usage limit.

    Args:
        usage_limit_id: Usage limit id.
        amount: Amount.
        breach_action: Breach action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UsageLimitId"] = usage_limit_id
    if amount is not None:
        kwargs["Amount"] = amount
    if breach_action is not None:
        kwargs["BreachAction"] = breach_action
    try:
        resp = await client.call("ModifyUsageLimit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to modify usage limit") from exc
    return ModifyUsageLimitResult(
        usage_limit_id=resp.get("UsageLimitId"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        feature_type=resp.get("FeatureType"),
        limit_type=resp.get("LimitType"),
        amount=resp.get("Amount"),
        period=resp.get("Period"),
        breach_action=resp.get("BreachAction"),
        tags=resp.get("Tags"),
    )


async def pause_cluster(
    cluster_identifier: str,
    region_name: str | None = None,
) -> PauseClusterResult:
    """Pause cluster.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("PauseCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to pause cluster") from exc
    return PauseClusterResult(
        cluster=resp.get("Cluster"),
    )


async def purchase_reserved_node_offering(
    reserved_node_offering_id: str,
    *,
    node_count: int | None = None,
    region_name: str | None = None,
) -> PurchaseReservedNodeOfferingResult:
    """Purchase reserved node offering.

    Args:
        reserved_node_offering_id: Reserved node offering id.
        node_count: Node count.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReservedNodeOfferingId"] = reserved_node_offering_id
    if node_count is not None:
        kwargs["NodeCount"] = node_count
    try:
        resp = await client.call("PurchaseReservedNodeOffering", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to purchase reserved node offering") from exc
    return PurchaseReservedNodeOfferingResult(
        reserved_node=resp.get("ReservedNode"),
    )


async def put_resource_policy(
    resource_arn: str,
    policy: str,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Policy"] = policy
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_policy=resp.get("ResourcePolicy"),
    )


async def register_namespace(
    namespace_identifier: dict[str, Any],
    consumer_identifiers: list[str],
    region_name: str | None = None,
) -> RegisterNamespaceResult:
    """Register namespace.

    Args:
        namespace_identifier: Namespace identifier.
        consumer_identifiers: Consumer identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamespaceIdentifier"] = namespace_identifier
    kwargs["ConsumerIdentifiers"] = consumer_identifiers
    try:
        resp = await client.call("RegisterNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register namespace") from exc
    return RegisterNamespaceResult(
        status=resp.get("Status"),
    )


async def reject_data_share(
    data_share_arn: str,
    region_name: str | None = None,
) -> RejectDataShareResult:
    """Reject data share.

    Args:
        data_share_arn: Data share arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataShareArn"] = data_share_arn
    try:
        resp = await client.call("RejectDataShare", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reject data share") from exc
    return RejectDataShareResult(
        data_share_arn=resp.get("DataShareArn"),
        producer_arn=resp.get("ProducerArn"),
        allow_publicly_accessible_consumers=resp.get("AllowPubliclyAccessibleConsumers"),
        data_share_associations=resp.get("DataShareAssociations"),
        managed_by=resp.get("ManagedBy"),
        data_share_type=resp.get("DataShareType"),
    )


async def reset_cluster_parameter_group(
    parameter_group_name: str,
    *,
    reset_all_parameters: bool | None = None,
    parameters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ResetClusterParameterGroupResult:
    """Reset cluster parameter group.

    Args:
        parameter_group_name: Parameter group name.
        reset_all_parameters: Reset all parameters.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ParameterGroupName"] = parameter_group_name
    if reset_all_parameters is not None:
        kwargs["ResetAllParameters"] = reset_all_parameters
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        resp = await client.call("ResetClusterParameterGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset cluster parameter group") from exc
    return ResetClusterParameterGroupResult(
        parameter_group_name=resp.get("ParameterGroupName"),
        parameter_group_status=resp.get("ParameterGroupStatus"),
    )


async def resize_cluster(
    cluster_identifier: str,
    *,
    cluster_type: str | None = None,
    node_type: str | None = None,
    number_of_nodes: int | None = None,
    classic: bool | None = None,
    reserved_node_id: str | None = None,
    target_reserved_node_offering_id: str | None = None,
    region_name: str | None = None,
) -> ResizeClusterResult:
    """Resize cluster.

    Args:
        cluster_identifier: Cluster identifier.
        cluster_type: Cluster type.
        node_type: Node type.
        number_of_nodes: Number of nodes.
        classic: Classic.
        reserved_node_id: Reserved node id.
        target_reserved_node_offering_id: Target reserved node offering id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    if cluster_type is not None:
        kwargs["ClusterType"] = cluster_type
    if node_type is not None:
        kwargs["NodeType"] = node_type
    if number_of_nodes is not None:
        kwargs["NumberOfNodes"] = number_of_nodes
    if classic is not None:
        kwargs["Classic"] = classic
    if reserved_node_id is not None:
        kwargs["ReservedNodeId"] = reserved_node_id
    if target_reserved_node_offering_id is not None:
        kwargs["TargetReservedNodeOfferingId"] = target_reserved_node_offering_id
    try:
        resp = await client.call("ResizeCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resize cluster") from exc
    return ResizeClusterResult(
        cluster=resp.get("Cluster"),
    )


async def restore_table_from_cluster_snapshot(
    cluster_identifier: str,
    snapshot_identifier: str,
    source_database_name: str,
    source_table_name: str,
    new_table_name: str,
    *,
    source_schema_name: str | None = None,
    target_database_name: str | None = None,
    target_schema_name: str | None = None,
    enable_case_sensitive_identifier: bool | None = None,
    region_name: str | None = None,
) -> RestoreTableFromClusterSnapshotResult:
    """Restore table from cluster snapshot.

    Args:
        cluster_identifier: Cluster identifier.
        snapshot_identifier: Snapshot identifier.
        source_database_name: Source database name.
        source_table_name: Source table name.
        new_table_name: New table name.
        source_schema_name: Source schema name.
        target_database_name: Target database name.
        target_schema_name: Target schema name.
        enable_case_sensitive_identifier: Enable case sensitive identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["SnapshotIdentifier"] = snapshot_identifier
    kwargs["SourceDatabaseName"] = source_database_name
    kwargs["SourceTableName"] = source_table_name
    kwargs["NewTableName"] = new_table_name
    if source_schema_name is not None:
        kwargs["SourceSchemaName"] = source_schema_name
    if target_database_name is not None:
        kwargs["TargetDatabaseName"] = target_database_name
    if target_schema_name is not None:
        kwargs["TargetSchemaName"] = target_schema_name
    if enable_case_sensitive_identifier is not None:
        kwargs["EnableCaseSensitiveIdentifier"] = enable_case_sensitive_identifier
    try:
        resp = await client.call("RestoreTableFromClusterSnapshot", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to restore table from cluster snapshot") from exc
    return RestoreTableFromClusterSnapshotResult(
        table_restore_status=resp.get("TableRestoreStatus"),
    )


async def resume_cluster(
    cluster_identifier: str,
    region_name: str | None = None,
) -> ResumeClusterResult:
    """Resume cluster.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("ResumeCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resume cluster") from exc
    return ResumeClusterResult(
        cluster=resp.get("Cluster"),
    )


async def revoke_cluster_security_group_ingress(
    cluster_security_group_name: str,
    *,
    cidrip: str | None = None,
    ec2_security_group_name: str | None = None,
    ec2_security_group_owner_id: str | None = None,
    region_name: str | None = None,
) -> RevokeClusterSecurityGroupIngressResult:
    """Revoke cluster security group ingress.

    Args:
        cluster_security_group_name: Cluster security group name.
        cidrip: Cidrip.
        ec2_security_group_name: Ec2 security group name.
        ec2_security_group_owner_id: Ec2 security group owner id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterSecurityGroupName"] = cluster_security_group_name
    if cidrip is not None:
        kwargs["CIDRIP"] = cidrip
    if ec2_security_group_name is not None:
        kwargs["EC2SecurityGroupName"] = ec2_security_group_name
    if ec2_security_group_owner_id is not None:
        kwargs["EC2SecurityGroupOwnerId"] = ec2_security_group_owner_id
    try:
        resp = await client.call("RevokeClusterSecurityGroupIngress", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to revoke cluster security group ingress") from exc
    return RevokeClusterSecurityGroupIngressResult(
        cluster_security_group=resp.get("ClusterSecurityGroup"),
    )


async def revoke_endpoint_access(
    *,
    cluster_identifier: str | None = None,
    account: str | None = None,
    vpc_ids: list[str] | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> RevokeEndpointAccessResult:
    """Revoke endpoint access.

    Args:
        cluster_identifier: Cluster identifier.
        account: Account.
        vpc_ids: Vpc ids.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if account is not None:
        kwargs["Account"] = account
    if vpc_ids is not None:
        kwargs["VpcIds"] = vpc_ids
    if force is not None:
        kwargs["Force"] = force
    try:
        resp = await client.call("RevokeEndpointAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to revoke endpoint access") from exc
    return RevokeEndpointAccessResult(
        grantor=resp.get("Grantor"),
        grantee=resp.get("Grantee"),
        cluster_identifier=resp.get("ClusterIdentifier"),
        authorize_time=resp.get("AuthorizeTime"),
        cluster_status=resp.get("ClusterStatus"),
        status=resp.get("Status"),
        allowed_all_vp_cs=resp.get("AllowedAllVPCs"),
        allowed_vp_cs=resp.get("AllowedVPCs"),
        endpoint_count=resp.get("EndpointCount"),
    )


async def revoke_snapshot_access(
    account_with_restore_access: str,
    *,
    snapshot_identifier: str | None = None,
    snapshot_arn: str | None = None,
    snapshot_cluster_identifier: str | None = None,
    region_name: str | None = None,
) -> RevokeSnapshotAccessResult:
    """Revoke snapshot access.

    Args:
        account_with_restore_access: Account with restore access.
        snapshot_identifier: Snapshot identifier.
        snapshot_arn: Snapshot arn.
        snapshot_cluster_identifier: Snapshot cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountWithRestoreAccess"] = account_with_restore_access
    if snapshot_identifier is not None:
        kwargs["SnapshotIdentifier"] = snapshot_identifier
    if snapshot_arn is not None:
        kwargs["SnapshotArn"] = snapshot_arn
    if snapshot_cluster_identifier is not None:
        kwargs["SnapshotClusterIdentifier"] = snapshot_cluster_identifier
    try:
        resp = await client.call("RevokeSnapshotAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to revoke snapshot access") from exc
    return RevokeSnapshotAccessResult(
        snapshot=resp.get("Snapshot"),
    )


async def rotate_encryption_key(
    cluster_identifier: str,
    region_name: str | None = None,
) -> RotateEncryptionKeyResult:
    """Rotate encryption key.

    Args:
        cluster_identifier: Cluster identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterIdentifier"] = cluster_identifier
    try:
        resp = await client.call("RotateEncryptionKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to rotate encryption key") from exc
    return RotateEncryptionKeyResult(
        cluster=resp.get("Cluster"),
    )


async def update_partner_status(
    account_id: str,
    cluster_identifier: str,
    database_name: str,
    partner_name: str,
    status: str,
    *,
    status_message: str | None = None,
    region_name: str | None = None,
) -> UpdatePartnerStatusResult:
    """Update partner status.

    Args:
        account_id: Account id.
        cluster_identifier: Cluster identifier.
        database_name: Database name.
        partner_name: Partner name.
        status: Status.
        status_message: Status message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ClusterIdentifier"] = cluster_identifier
    kwargs["DatabaseName"] = database_name
    kwargs["PartnerName"] = partner_name
    kwargs["Status"] = status
    if status_message is not None:
        kwargs["StatusMessage"] = status_message
    try:
        resp = await client.call("UpdatePartnerStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update partner status") from exc
    return UpdatePartnerStatusResult(
        database_name=resp.get("DatabaseName"),
        partner_name=resp.get("PartnerName"),
    )
