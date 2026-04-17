"""aws_util.redshift_serverless — Amazon Redshift Serverless utilities.

Provides convenience wrappers around Redshift Serverless namespace and
workgroup management operations with Pydantic-modelled results.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ConvertRecoveryPointToSnapshotResult",
    "CreateCustomDomainAssociationResult",
    "CreateEndpointAccessResult",
    "CreateReservationResult",
    "CreateScheduledActionResult",
    "CreateSnapshotCopyConfigurationResult",
    "CreateSnapshotResult",
    "CreateUsageLimitResult",
    "DeleteEndpointAccessResult",
    "DeleteScheduledActionResult",
    "DeleteSnapshotCopyConfigurationResult",
    "DeleteSnapshotResult",
    "DeleteUsageLimitResult",
    "GetCredentialsResult",
    "GetCustomDomainAssociationResult",
    "GetEndpointAccessResult",
    "GetRecoveryPointResult",
    "GetReservationOfferingResult",
    "GetReservationResult",
    "GetResourcePolicyResult",
    "GetScheduledActionResult",
    "GetSnapshotResult",
    "GetTableRestoreStatusResult",
    "GetTrackResult",
    "GetUsageLimitResult",
    "ListCustomDomainAssociationsResult",
    "ListEndpointAccessResult",
    "ListManagedWorkgroupsResult",
    "ListRecoveryPointsResult",
    "ListReservationOfferingsResult",
    "ListReservationsResult",
    "ListScheduledActionsResult",
    "ListSnapshotCopyConfigurationsResult",
    "ListSnapshotsResult",
    "ListTableRestoreStatusResult",
    "ListTagsForResourceResult",
    "ListTracksResult",
    "ListUsageLimitsResult",
    "NamespaceResult",
    "PutResourcePolicyResult",
    "RestoreFromRecoveryPointResult",
    "RestoreFromSnapshotResult",
    "RestoreTableFromRecoveryPointResult",
    "RestoreTableFromSnapshotResult",
    "UpdateCustomDomainAssociationResult",
    "UpdateEndpointAccessResult",
    "UpdateScheduledActionResult",
    "UpdateSnapshotCopyConfigurationResult",
    "UpdateSnapshotResult",
    "UpdateUsageLimitResult",
    "WorkgroupResult",
    "convert_recovery_point_to_snapshot",
    "create_custom_domain_association",
    "create_endpoint_access",
    "create_namespace",
    "create_reservation",
    "create_scheduled_action",
    "create_snapshot",
    "create_snapshot_copy_configuration",
    "create_usage_limit",
    "create_workgroup",
    "delete_custom_domain_association",
    "delete_endpoint_access",
    "delete_namespace",
    "delete_resource_policy",
    "delete_scheduled_action",
    "delete_snapshot",
    "delete_snapshot_copy_configuration",
    "delete_usage_limit",
    "delete_workgroup",
    "get_credentials",
    "get_custom_domain_association",
    "get_endpoint_access",
    "get_namespace",
    "get_recovery_point",
    "get_reservation",
    "get_reservation_offering",
    "get_resource_policy",
    "get_scheduled_action",
    "get_snapshot",
    "get_table_restore_status",
    "get_track",
    "get_usage_limit",
    "get_workgroup",
    "list_custom_domain_associations",
    "list_endpoint_access",
    "list_managed_workgroups",
    "list_namespaces",
    "list_recovery_points",
    "list_reservation_offerings",
    "list_reservations",
    "list_scheduled_actions",
    "list_snapshot_copy_configurations",
    "list_snapshots",
    "list_table_restore_status",
    "list_tags_for_resource",
    "list_tracks",
    "list_usage_limits",
    "list_workgroups",
    "put_resource_policy",
    "restore_from_recovery_point",
    "restore_from_snapshot",
    "restore_table_from_recovery_point",
    "restore_table_from_snapshot",
    "tag_resource",
    "untag_resource",
    "update_custom_domain_association",
    "update_endpoint_access",
    "update_namespace",
    "update_scheduled_action",
    "update_snapshot",
    "update_snapshot_copy_configuration",
    "update_usage_limit",
    "update_workgroup",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class NamespaceResult(BaseModel):
    """Metadata for a Redshift Serverless namespace."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    namespace_name: str
    namespace_id: str = ""
    namespace_arn: str = ""
    status: str = ""
    admin_username: str | None = None
    db_name: str | None = None
    creation_date: str | None = None
    iam_roles: list[str] = []
    extra: dict[str, Any] = {}


class WorkgroupResult(BaseModel):
    """Metadata for a Redshift Serverless workgroup."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    workgroup_name: str
    workgroup_id: str = ""
    workgroup_arn: str = ""
    status: str = ""
    namespace_name: str | None = None
    base_capacity: int | None = None
    creation_date: str | None = None
    endpoint: dict[str, Any] = {}
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_NS_FIELDS = {
    "namespaceName",
    "namespaceId",
    "namespaceArn",
    "status",
    "adminUsername",
    "dbName",
    "creationDate",
    "iamRoles",
}

_WG_FIELDS = {
    "workgroupName",
    "workgroupId",
    "workgroupArn",
    "status",
    "namespaceName",
    "baseCapacity",
    "creationDate",
    "endpoint",
}


def _parse_namespace(data: dict[str, Any]) -> NamespaceResult:
    """Parse a raw Redshift Serverless namespace dict."""
    created = data.get("creationDate")
    return NamespaceResult(
        namespace_name=data.get("namespaceName", ""),
        namespace_id=data.get("namespaceId", ""),
        namespace_arn=data.get("namespaceArn", ""),
        status=data.get("status", ""),
        admin_username=data.get("adminUsername"),
        db_name=data.get("dbName"),
        creation_date=str(created) if created is not None else None,
        iam_roles=data.get("iamRoles", []),
        extra={k: v for k, v in data.items() if k not in _NS_FIELDS},
    )


def _parse_workgroup(data: dict[str, Any]) -> WorkgroupResult:
    """Parse a raw Redshift Serverless workgroup dict."""
    created = data.get("creationDate")
    return WorkgroupResult(
        workgroup_name=data.get("workgroupName", ""),
        workgroup_id=data.get("workgroupId", ""),
        workgroup_arn=data.get("workgroupArn", ""),
        status=data.get("status", ""),
        namespace_name=data.get("namespaceName"),
        base_capacity=data.get("baseCapacity"),
        creation_date=str(created) if created is not None else None,
        endpoint=data.get("endpoint", {}),
        extra={k: v for k, v in data.items() if k not in _WG_FIELDS},
    )


# ---------------------------------------------------------------------------
# Namespace operations
# ---------------------------------------------------------------------------


def create_namespace(
    namespace_name: str,
    *,
    admin_username: str | None = None,
    admin_user_password: str | None = None,
    db_name: str | None = None,
    iam_roles: list[str] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> NamespaceResult:
    """Create a Redshift Serverless namespace.

    Args:
        namespace_name: Name for the namespace.
        admin_username: Optional admin user name.
        admin_user_password: Optional admin password.
        db_name: Optional database name.
        iam_roles: Optional list of IAM role ARNs.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`NamespaceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {"namespaceName": namespace_name}
    if admin_username is not None:
        kwargs["adminUsername"] = admin_username
    if admin_user_password is not None:
        kwargs["adminUserPassword"] = admin_user_password
    if db_name is not None:
        kwargs["dbName"] = db_name
    if iam_roles is not None:
        kwargs["iamRoles"] = iam_roles
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_namespace(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_namespace failed for {namespace_name!r}") from exc
    return _parse_namespace(resp.get("namespace", {}))


def get_namespace(
    namespace_name: str,
    *,
    region_name: str | None = None,
) -> NamespaceResult:
    """Get a Redshift Serverless namespace.

    Args:
        namespace_name: Name of the namespace.
        region_name: AWS region override.

    Returns:
        A :class:`NamespaceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    try:
        resp = client.get_namespace(namespaceName=namespace_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_namespace failed for {namespace_name!r}") from exc
    return _parse_namespace(resp.get("namespace", {}))


def list_namespaces(
    *,
    region_name: str | None = None,
) -> list[NamespaceResult]:
    """List all Redshift Serverless namespaces.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`NamespaceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    namespaces: list[NamespaceResult] = []
    try:
        paginator = client.get_paginator("list_namespaces")
        for page in paginator.paginate():
            for item in page.get("namespaces", []):
                namespaces.append(_parse_namespace(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_namespaces failed") from exc
    return namespaces


def delete_namespace(
    namespace_name: str,
    *,
    final_snapshot_name: str | None = None,
    region_name: str | None = None,
) -> NamespaceResult:
    """Delete a Redshift Serverless namespace.

    Args:
        namespace_name: Name of the namespace.
        final_snapshot_name: Optional final snapshot name.
        region_name: AWS region override.

    Returns:
        A :class:`NamespaceResult` for the deleted namespace.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {"namespaceName": namespace_name}
    if final_snapshot_name is not None:
        kwargs["finalSnapshotName"] = final_snapshot_name
    try:
        resp = client.delete_namespace(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_namespace failed for {namespace_name!r}") from exc
    return _parse_namespace(resp.get("namespace", {}))


def update_namespace(
    namespace_name: str,
    *,
    admin_username: str | None = None,
    admin_user_password: str | None = None,
    iam_roles: list[str] | None = None,
    region_name: str | None = None,
) -> NamespaceResult:
    """Update a Redshift Serverless namespace.

    Args:
        namespace_name: Name of the namespace.
        admin_username: Optional new admin user name.
        admin_user_password: Optional new admin password.
        iam_roles: Optional updated list of IAM role ARNs.
        region_name: AWS region override.

    Returns:
        A :class:`NamespaceResult` with updated details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {"namespaceName": namespace_name}
    if admin_username is not None:
        kwargs["adminUsername"] = admin_username
    if admin_user_password is not None:
        kwargs["adminUserPassword"] = admin_user_password
    if iam_roles is not None:
        kwargs["iamRoles"] = iam_roles
    try:
        resp = client.update_namespace(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_namespace failed for {namespace_name!r}") from exc
    return _parse_namespace(resp.get("namespace", {}))


# ---------------------------------------------------------------------------
# Workgroup operations
# ---------------------------------------------------------------------------


def create_workgroup(
    workgroup_name: str,
    *,
    namespace_name: str,
    base_capacity: int | None = None,
    subnet_ids: list[str] | None = None,
    security_group_ids: list[str] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> WorkgroupResult:
    """Create a Redshift Serverless workgroup.

    Args:
        workgroup_name: Name for the workgroup.
        namespace_name: Name of the namespace to associate.
        base_capacity: Optional base RPU capacity.
        subnet_ids: Optional list of subnet IDs.
        security_group_ids: Optional list of security group IDs.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`WorkgroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {
        "workgroupName": workgroup_name,
        "namespaceName": namespace_name,
    }
    if base_capacity is not None:
        kwargs["baseCapacity"] = base_capacity
    if subnet_ids is not None:
        kwargs["subnetIds"] = subnet_ids
    if security_group_ids is not None:
        kwargs["securityGroupIds"] = security_group_ids
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_workgroup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_workgroup failed for {workgroup_name!r}") from exc
    return _parse_workgroup(resp.get("workgroup", {}))


def get_workgroup(
    workgroup_name: str,
    *,
    region_name: str | None = None,
) -> WorkgroupResult:
    """Get a Redshift Serverless workgroup.

    Args:
        workgroup_name: Name of the workgroup.
        region_name: AWS region override.

    Returns:
        A :class:`WorkgroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    try:
        resp = client.get_workgroup(workgroupName=workgroup_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_workgroup failed for {workgroup_name!r}") from exc
    return _parse_workgroup(resp.get("workgroup", {}))


def list_workgroups(
    *,
    region_name: str | None = None,
) -> list[WorkgroupResult]:
    """List all Redshift Serverless workgroups.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`WorkgroupResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    workgroups: list[WorkgroupResult] = []
    try:
        paginator = client.get_paginator("list_workgroups")
        for page in paginator.paginate():
            for item in page.get("workgroups", []):
                workgroups.append(_parse_workgroup(item))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_workgroups failed") from exc
    return workgroups


def delete_workgroup(
    workgroup_name: str,
    *,
    region_name: str | None = None,
) -> WorkgroupResult:
    """Delete a Redshift Serverless workgroup.

    Args:
        workgroup_name: Name of the workgroup.
        region_name: AWS region override.

    Returns:
        A :class:`WorkgroupResult` for the deleted workgroup.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    try:
        resp = client.delete_workgroup(workgroupName=workgroup_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_workgroup failed for {workgroup_name!r}") from exc
    return _parse_workgroup(resp.get("workgroup", {}))


def update_workgroup(
    workgroup_name: str,
    *,
    base_capacity: int | None = None,
    subnet_ids: list[str] | None = None,
    security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> WorkgroupResult:
    """Update a Redshift Serverless workgroup.

    Args:
        workgroup_name: Name of the workgroup.
        base_capacity: Optional updated base RPU capacity.
        subnet_ids: Optional updated subnet IDs.
        security_group_ids: Optional updated security group IDs.
        region_name: AWS region override.

    Returns:
        A :class:`WorkgroupResult` with updated details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {"workgroupName": workgroup_name}
    if base_capacity is not None:
        kwargs["baseCapacity"] = base_capacity
    if subnet_ids is not None:
        kwargs["subnetIds"] = subnet_ids
    if security_group_ids is not None:
        kwargs["securityGroupIds"] = security_group_ids
    try:
        resp = client.update_workgroup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_workgroup failed for {workgroup_name!r}") from exc
    return _parse_workgroup(resp.get("workgroup", {}))


class ConvertRecoveryPointToSnapshotResult(BaseModel):
    """Result of convert_recovery_point_to_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class CreateCustomDomainAssociationResult(BaseModel):
    """Result of create_custom_domain_association."""

    model_config = ConfigDict(frozen=True)

    custom_domain_certificate_arn: str | None = None
    custom_domain_certificate_expiry_time: str | None = None
    custom_domain_name: str | None = None
    workgroup_name: str | None = None


class CreateEndpointAccessResult(BaseModel):
    """Result of create_endpoint_access."""

    model_config = ConfigDict(frozen=True)

    endpoint: dict[str, Any] | None = None


class CreateReservationResult(BaseModel):
    """Result of create_reservation."""

    model_config = ConfigDict(frozen=True)

    reservation: dict[str, Any] | None = None


class CreateScheduledActionResult(BaseModel):
    """Result of create_scheduled_action."""

    model_config = ConfigDict(frozen=True)

    scheduled_action: dict[str, Any] | None = None


class CreateSnapshotResult(BaseModel):
    """Result of create_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class CreateSnapshotCopyConfigurationResult(BaseModel):
    """Result of create_snapshot_copy_configuration."""

    model_config = ConfigDict(frozen=True)

    snapshot_copy_configuration: dict[str, Any] | None = None


class CreateUsageLimitResult(BaseModel):
    """Result of create_usage_limit."""

    model_config = ConfigDict(frozen=True)

    usage_limit: dict[str, Any] | None = None


class DeleteEndpointAccessResult(BaseModel):
    """Result of delete_endpoint_access."""

    model_config = ConfigDict(frozen=True)

    endpoint: dict[str, Any] | None = None


class DeleteScheduledActionResult(BaseModel):
    """Result of delete_scheduled_action."""

    model_config = ConfigDict(frozen=True)

    scheduled_action: dict[str, Any] | None = None


class DeleteSnapshotResult(BaseModel):
    """Result of delete_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class DeleteSnapshotCopyConfigurationResult(BaseModel):
    """Result of delete_snapshot_copy_configuration."""

    model_config = ConfigDict(frozen=True)

    snapshot_copy_configuration: dict[str, Any] | None = None


class DeleteUsageLimitResult(BaseModel):
    """Result of delete_usage_limit."""

    model_config = ConfigDict(frozen=True)

    usage_limit: dict[str, Any] | None = None


class GetCredentialsResult(BaseModel):
    """Result of get_credentials."""

    model_config = ConfigDict(frozen=True)

    db_password: str | None = None
    db_user: str | None = None
    expiration: str | None = None
    next_refresh_time: str | None = None


class GetCustomDomainAssociationResult(BaseModel):
    """Result of get_custom_domain_association."""

    model_config = ConfigDict(frozen=True)

    custom_domain_certificate_arn: str | None = None
    custom_domain_certificate_expiry_time: str | None = None
    custom_domain_name: str | None = None
    workgroup_name: str | None = None


class GetEndpointAccessResult(BaseModel):
    """Result of get_endpoint_access."""

    model_config = ConfigDict(frozen=True)

    endpoint: dict[str, Any] | None = None


class GetRecoveryPointResult(BaseModel):
    """Result of get_recovery_point."""

    model_config = ConfigDict(frozen=True)

    recovery_point: dict[str, Any] | None = None


class GetReservationResult(BaseModel):
    """Result of get_reservation."""

    model_config = ConfigDict(frozen=True)

    reservation: dict[str, Any] | None = None


class GetReservationOfferingResult(BaseModel):
    """Result of get_reservation_offering."""

    model_config = ConfigDict(frozen=True)

    reservation_offering: dict[str, Any] | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_policy: dict[str, Any] | None = None


class GetScheduledActionResult(BaseModel):
    """Result of get_scheduled_action."""

    model_config = ConfigDict(frozen=True)

    scheduled_action: dict[str, Any] | None = None


class GetSnapshotResult(BaseModel):
    """Result of get_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class GetTableRestoreStatusResult(BaseModel):
    """Result of get_table_restore_status."""

    model_config = ConfigDict(frozen=True)

    table_restore_status: dict[str, Any] | None = None


class GetTrackResult(BaseModel):
    """Result of get_track."""

    model_config = ConfigDict(frozen=True)

    track: dict[str, Any] | None = None


class GetUsageLimitResult(BaseModel):
    """Result of get_usage_limit."""

    model_config = ConfigDict(frozen=True)

    usage_limit: dict[str, Any] | None = None


class ListCustomDomainAssociationsResult(BaseModel):
    """Result of list_custom_domain_associations."""

    model_config = ConfigDict(frozen=True)

    associations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEndpointAccessResult(BaseModel):
    """Result of list_endpoint_access."""

    model_config = ConfigDict(frozen=True)

    endpoints: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListManagedWorkgroupsResult(BaseModel):
    """Result of list_managed_workgroups."""

    model_config = ConfigDict(frozen=True)

    managed_workgroups: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRecoveryPointsResult(BaseModel):
    """Result of list_recovery_points."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    recovery_points: list[dict[str, Any]] | None = None


class ListReservationOfferingsResult(BaseModel):
    """Result of list_reservation_offerings."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reservation_offerings_list: list[dict[str, Any]] | None = None


class ListReservationsResult(BaseModel):
    """Result of list_reservations."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    reservations_list: list[dict[str, Any]] | None = None


class ListScheduledActionsResult(BaseModel):
    """Result of list_scheduled_actions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    scheduled_actions: list[dict[str, Any]] | None = None


class ListSnapshotCopyConfigurationsResult(BaseModel):
    """Result of list_snapshot_copy_configurations."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    snapshot_copy_configurations: list[dict[str, Any]] | None = None


class ListSnapshotsResult(BaseModel):
    """Result of list_snapshots."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    snapshots: list[dict[str, Any]] | None = None


class ListTableRestoreStatusResult(BaseModel):
    """Result of list_table_restore_status."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    table_restore_statuses: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class ListTracksResult(BaseModel):
    """Result of list_tracks."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    tracks: list[dict[str, Any]] | None = None


class ListUsageLimitsResult(BaseModel):
    """Result of list_usage_limits."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    usage_limits: list[dict[str, Any]] | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_policy: dict[str, Any] | None = None


class RestoreFromRecoveryPointResult(BaseModel):
    """Result of restore_from_recovery_point."""

    model_config = ConfigDict(frozen=True)

    namespace: dict[str, Any] | None = None
    recovery_point_id: str | None = None


class RestoreFromSnapshotResult(BaseModel):
    """Result of restore_from_snapshot."""

    model_config = ConfigDict(frozen=True)

    namespace: dict[str, Any] | None = None
    owner_account: str | None = None
    snapshot_name: str | None = None


class RestoreTableFromRecoveryPointResult(BaseModel):
    """Result of restore_table_from_recovery_point."""

    model_config = ConfigDict(frozen=True)

    table_restore_status: dict[str, Any] | None = None


class RestoreTableFromSnapshotResult(BaseModel):
    """Result of restore_table_from_snapshot."""

    model_config = ConfigDict(frozen=True)

    table_restore_status: dict[str, Any] | None = None


class UpdateCustomDomainAssociationResult(BaseModel):
    """Result of update_custom_domain_association."""

    model_config = ConfigDict(frozen=True)

    custom_domain_certificate_arn: str | None = None
    custom_domain_certificate_expiry_time: str | None = None
    custom_domain_name: str | None = None
    workgroup_name: str | None = None


class UpdateEndpointAccessResult(BaseModel):
    """Result of update_endpoint_access."""

    model_config = ConfigDict(frozen=True)

    endpoint: dict[str, Any] | None = None


class UpdateScheduledActionResult(BaseModel):
    """Result of update_scheduled_action."""

    model_config = ConfigDict(frozen=True)

    scheduled_action: dict[str, Any] | None = None


class UpdateSnapshotResult(BaseModel):
    """Result of update_snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot: dict[str, Any] | None = None


class UpdateSnapshotCopyConfigurationResult(BaseModel):
    """Result of update_snapshot_copy_configuration."""

    model_config = ConfigDict(frozen=True)

    snapshot_copy_configuration: dict[str, Any] | None = None


class UpdateUsageLimitResult(BaseModel):
    """Result of update_usage_limit."""

    model_config = ConfigDict(frozen=True)

    usage_limit: dict[str, Any] | None = None


def convert_recovery_point_to_snapshot(
    recovery_point_id: str,
    snapshot_name: str,
    *,
    retention_period: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ConvertRecoveryPointToSnapshotResult:
    """Convert recovery point to snapshot.

    Args:
        recovery_point_id: Recovery point id.
        snapshot_name: Snapshot name.
        retention_period: Retention period.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recoveryPointId"] = recovery_point_id
    kwargs["snapshotName"] = snapshot_name
    if retention_period is not None:
        kwargs["retentionPeriod"] = retention_period
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.convert_recovery_point_to_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to convert recovery point to snapshot") from exc
    return ConvertRecoveryPointToSnapshotResult(
        snapshot=resp.get("snapshot"),
    )


def create_custom_domain_association(
    custom_domain_certificate_arn: str,
    custom_domain_name: str,
    workgroup_name: str,
    region_name: str | None = None,
) -> CreateCustomDomainAssociationResult:
    """Create custom domain association.

    Args:
        custom_domain_certificate_arn: Custom domain certificate arn.
        custom_domain_name: Custom domain name.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customDomainCertificateArn"] = custom_domain_certificate_arn
    kwargs["customDomainName"] = custom_domain_name
    kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.create_custom_domain_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create custom domain association") from exc
    return CreateCustomDomainAssociationResult(
        custom_domain_certificate_arn=resp.get("customDomainCertificateArn"),
        custom_domain_certificate_expiry_time=resp.get("customDomainCertificateExpiryTime"),
        custom_domain_name=resp.get("customDomainName"),
        workgroup_name=resp.get("workgroupName"),
    )


def create_endpoint_access(
    endpoint_name: str,
    subnet_ids: list[str],
    workgroup_name: str,
    *,
    owner_account: str | None = None,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> CreateEndpointAccessResult:
    """Create endpoint access.

    Args:
        endpoint_name: Endpoint name.
        subnet_ids: Subnet ids.
        workgroup_name: Workgroup name.
        owner_account: Owner account.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointName"] = endpoint_name
    kwargs["subnetIds"] = subnet_ids
    kwargs["workgroupName"] = workgroup_name
    if owner_account is not None:
        kwargs["ownerAccount"] = owner_account
    if vpc_security_group_ids is not None:
        kwargs["vpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = client.create_endpoint_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create endpoint access") from exc
    return CreateEndpointAccessResult(
        endpoint=resp.get("endpoint"),
    )


def create_reservation(
    capacity: int,
    offering_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateReservationResult:
    """Create reservation.

    Args:
        capacity: Capacity.
        offering_id: Offering id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["capacity"] = capacity
    kwargs["offeringId"] = offering_id
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = client.create_reservation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create reservation") from exc
    return CreateReservationResult(
        reservation=resp.get("reservation"),
    )


def create_scheduled_action(
    namespace_name: str,
    role_arn: str,
    schedule: dict[str, Any],
    scheduled_action_name: str,
    target_action: dict[str, Any],
    *,
    enabled: bool | None = None,
    end_time: str | None = None,
    scheduled_action_description: str | None = None,
    start_time: str | None = None,
    region_name: str | None = None,
) -> CreateScheduledActionResult:
    """Create scheduled action.

    Args:
        namespace_name: Namespace name.
        role_arn: Role arn.
        schedule: Schedule.
        scheduled_action_name: Scheduled action name.
        target_action: Target action.
        enabled: Enabled.
        end_time: End time.
        scheduled_action_description: Scheduled action description.
        start_time: Start time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["roleArn"] = role_arn
    kwargs["schedule"] = schedule
    kwargs["scheduledActionName"] = scheduled_action_name
    kwargs["targetAction"] = target_action
    if enabled is not None:
        kwargs["enabled"] = enabled
    if end_time is not None:
        kwargs["endTime"] = end_time
    if scheduled_action_description is not None:
        kwargs["scheduledActionDescription"] = scheduled_action_description
    if start_time is not None:
        kwargs["startTime"] = start_time
    try:
        resp = client.create_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create scheduled action") from exc
    return CreateScheduledActionResult(
        scheduled_action=resp.get("scheduledAction"),
    )


def create_snapshot(
    namespace_name: str,
    snapshot_name: str,
    *,
    retention_period: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateSnapshotResult:
    """Create snapshot.

    Args:
        namespace_name: Namespace name.
        snapshot_name: Snapshot name.
        retention_period: Retention period.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["snapshotName"] = snapshot_name
    if retention_period is not None:
        kwargs["retentionPeriod"] = retention_period
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.create_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot") from exc
    return CreateSnapshotResult(
        snapshot=resp.get("snapshot"),
    )


def create_snapshot_copy_configuration(
    destination_region: str,
    namespace_name: str,
    *,
    destination_kms_key_id: str | None = None,
    snapshot_retention_period: int | None = None,
    region_name: str | None = None,
) -> CreateSnapshotCopyConfigurationResult:
    """Create snapshot copy configuration.

    Args:
        destination_region: Destination region.
        namespace_name: Namespace name.
        destination_kms_key_id: Destination kms key id.
        snapshot_retention_period: Snapshot retention period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["destinationRegion"] = destination_region
    kwargs["namespaceName"] = namespace_name
    if destination_kms_key_id is not None:
        kwargs["destinationKmsKeyId"] = destination_kms_key_id
    if snapshot_retention_period is not None:
        kwargs["snapshotRetentionPeriod"] = snapshot_retention_period
    try:
        resp = client.create_snapshot_copy_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create snapshot copy configuration") from exc
    return CreateSnapshotCopyConfigurationResult(
        snapshot_copy_configuration=resp.get("snapshotCopyConfiguration"),
    )


def create_usage_limit(
    amount: int,
    resource_arn: str,
    usage_type: str,
    *,
    breach_action: str | None = None,
    period: str | None = None,
    region_name: str | None = None,
) -> CreateUsageLimitResult:
    """Create usage limit.

    Args:
        amount: Amount.
        resource_arn: Resource arn.
        usage_type: Usage type.
        breach_action: Breach action.
        period: Period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["amount"] = amount
    kwargs["resourceArn"] = resource_arn
    kwargs["usageType"] = usage_type
    if breach_action is not None:
        kwargs["breachAction"] = breach_action
    if period is not None:
        kwargs["period"] = period
    try:
        resp = client.create_usage_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create usage limit") from exc
    return CreateUsageLimitResult(
        usage_limit=resp.get("usageLimit"),
    )


def delete_custom_domain_association(
    custom_domain_name: str,
    workgroup_name: str,
    region_name: str | None = None,
) -> None:
    """Delete custom domain association.

    Args:
        custom_domain_name: Custom domain name.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customDomainName"] = custom_domain_name
    kwargs["workgroupName"] = workgroup_name
    try:
        client.delete_custom_domain_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete custom domain association") from exc
    return None


def delete_endpoint_access(
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
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointName"] = endpoint_name
    try:
        resp = client.delete_endpoint_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete endpoint access") from exc
    return DeleteEndpointAccessResult(
        endpoint=resp.get("endpoint"),
    )


def delete_resource_policy(
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
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def delete_scheduled_action(
    scheduled_action_name: str,
    region_name: str | None = None,
) -> DeleteScheduledActionResult:
    """Delete scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledActionName"] = scheduled_action_name
    try:
        resp = client.delete_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduled action") from exc
    return DeleteScheduledActionResult(
        scheduled_action=resp.get("scheduledAction"),
    )


def delete_snapshot(
    snapshot_name: str,
    region_name: str | None = None,
) -> DeleteSnapshotResult:
    """Delete snapshot.

    Args:
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["snapshotName"] = snapshot_name
    try:
        resp = client.delete_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot") from exc
    return DeleteSnapshotResult(
        snapshot=resp.get("snapshot"),
    )


def delete_snapshot_copy_configuration(
    snapshot_copy_configuration_id: str,
    region_name: str | None = None,
) -> DeleteSnapshotCopyConfigurationResult:
    """Delete snapshot copy configuration.

    Args:
        snapshot_copy_configuration_id: Snapshot copy configuration id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["snapshotCopyConfigurationId"] = snapshot_copy_configuration_id
    try:
        resp = client.delete_snapshot_copy_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete snapshot copy configuration") from exc
    return DeleteSnapshotCopyConfigurationResult(
        snapshot_copy_configuration=resp.get("snapshotCopyConfiguration"),
    )


def delete_usage_limit(
    usage_limit_id: str,
    region_name: str | None = None,
) -> DeleteUsageLimitResult:
    """Delete usage limit.

    Args:
        usage_limit_id: Usage limit id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usageLimitId"] = usage_limit_id
    try:
        resp = client.delete_usage_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete usage limit") from exc
    return DeleteUsageLimitResult(
        usage_limit=resp.get("usageLimit"),
    )


def get_credentials(
    *,
    custom_domain_name: str | None = None,
    db_name: str | None = None,
    duration_seconds: int | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> GetCredentialsResult:
    """Get credentials.

    Args:
        custom_domain_name: Custom domain name.
        db_name: Db name.
        duration_seconds: Duration seconds.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if custom_domain_name is not None:
        kwargs["customDomainName"] = custom_domain_name
    if db_name is not None:
        kwargs["dbName"] = db_name
    if duration_seconds is not None:
        kwargs["durationSeconds"] = duration_seconds
    if workgroup_name is not None:
        kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.get_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get credentials") from exc
    return GetCredentialsResult(
        db_password=resp.get("dbPassword"),
        db_user=resp.get("dbUser"),
        expiration=resp.get("expiration"),
        next_refresh_time=resp.get("nextRefreshTime"),
    )


def get_custom_domain_association(
    custom_domain_name: str,
    workgroup_name: str,
    region_name: str | None = None,
) -> GetCustomDomainAssociationResult:
    """Get custom domain association.

    Args:
        custom_domain_name: Custom domain name.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customDomainName"] = custom_domain_name
    kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.get_custom_domain_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get custom domain association") from exc
    return GetCustomDomainAssociationResult(
        custom_domain_certificate_arn=resp.get("customDomainCertificateArn"),
        custom_domain_certificate_expiry_time=resp.get("customDomainCertificateExpiryTime"),
        custom_domain_name=resp.get("customDomainName"),
        workgroup_name=resp.get("workgroupName"),
    )


def get_endpoint_access(
    endpoint_name: str,
    region_name: str | None = None,
) -> GetEndpointAccessResult:
    """Get endpoint access.

    Args:
        endpoint_name: Endpoint name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointName"] = endpoint_name
    try:
        resp = client.get_endpoint_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get endpoint access") from exc
    return GetEndpointAccessResult(
        endpoint=resp.get("endpoint"),
    )


def get_recovery_point(
    recovery_point_id: str,
    region_name: str | None = None,
) -> GetRecoveryPointResult:
    """Get recovery point.

    Args:
        recovery_point_id: Recovery point id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["recoveryPointId"] = recovery_point_id
    try:
        resp = client.get_recovery_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get recovery point") from exc
    return GetRecoveryPointResult(
        recovery_point=resp.get("recoveryPoint"),
    )


def get_reservation(
    reservation_id: str,
    region_name: str | None = None,
) -> GetReservationResult:
    """Get reservation.

    Args:
        reservation_id: Reservation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["reservationId"] = reservation_id
    try:
        resp = client.get_reservation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get reservation") from exc
    return GetReservationResult(
        reservation=resp.get("reservation"),
    )


def get_reservation_offering(
    offering_id: str,
    region_name: str | None = None,
) -> GetReservationOfferingResult:
    """Get reservation offering.

    Args:
        offering_id: Offering id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["offeringId"] = offering_id
    try:
        resp = client.get_reservation_offering(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get reservation offering") from exc
    return GetReservationOfferingResult(
        reservation_offering=resp.get("reservationOffering"),
    )


def get_resource_policy(
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
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_policy=resp.get("resourcePolicy"),
    )


def get_scheduled_action(
    scheduled_action_name: str,
    region_name: str | None = None,
) -> GetScheduledActionResult:
    """Get scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledActionName"] = scheduled_action_name
    try:
        resp = client.get_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get scheduled action") from exc
    return GetScheduledActionResult(
        scheduled_action=resp.get("scheduledAction"),
    )


def get_snapshot(
    *,
    owner_account: str | None = None,
    snapshot_arn: str | None = None,
    snapshot_name: str | None = None,
    region_name: str | None = None,
) -> GetSnapshotResult:
    """Get snapshot.

    Args:
        owner_account: Owner account.
        snapshot_arn: Snapshot arn.
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if owner_account is not None:
        kwargs["ownerAccount"] = owner_account
    if snapshot_arn is not None:
        kwargs["snapshotArn"] = snapshot_arn
    if snapshot_name is not None:
        kwargs["snapshotName"] = snapshot_name
    try:
        resp = client.get_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get snapshot") from exc
    return GetSnapshotResult(
        snapshot=resp.get("snapshot"),
    )


def get_table_restore_status(
    table_restore_request_id: str,
    region_name: str | None = None,
) -> GetTableRestoreStatusResult:
    """Get table restore status.

    Args:
        table_restore_request_id: Table restore request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["tableRestoreRequestId"] = table_restore_request_id
    try:
        resp = client.get_table_restore_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get table restore status") from exc
    return GetTableRestoreStatusResult(
        table_restore_status=resp.get("tableRestoreStatus"),
    )


def get_track(
    track_name: str,
    region_name: str | None = None,
) -> GetTrackResult:
    """Get track.

    Args:
        track_name: Track name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["trackName"] = track_name
    try:
        resp = client.get_track(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get track") from exc
    return GetTrackResult(
        track=resp.get("track"),
    )


def get_usage_limit(
    usage_limit_id: str,
    region_name: str | None = None,
) -> GetUsageLimitResult:
    """Get usage limit.

    Args:
        usage_limit_id: Usage limit id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usageLimitId"] = usage_limit_id
    try:
        resp = client.get_usage_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get usage limit") from exc
    return GetUsageLimitResult(
        usage_limit=resp.get("usageLimit"),
    )


def list_custom_domain_associations(
    *,
    custom_domain_certificate_arn: str | None = None,
    custom_domain_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCustomDomainAssociationsResult:
    """List custom domain associations.

    Args:
        custom_domain_certificate_arn: Custom domain certificate arn.
        custom_domain_name: Custom domain name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if custom_domain_certificate_arn is not None:
        kwargs["customDomainCertificateArn"] = custom_domain_certificate_arn
    if custom_domain_name is not None:
        kwargs["customDomainName"] = custom_domain_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_custom_domain_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list custom domain associations") from exc
    return ListCustomDomainAssociationsResult(
        associations=resp.get("associations"),
        next_token=resp.get("nextToken"),
    )


def list_endpoint_access(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    owner_account: str | None = None,
    vpc_id: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> ListEndpointAccessResult:
    """List endpoint access.

    Args:
        max_results: Max results.
        next_token: Next token.
        owner_account: Owner account.
        vpc_id: Vpc id.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if owner_account is not None:
        kwargs["ownerAccount"] = owner_account
    if vpc_id is not None:
        kwargs["vpcId"] = vpc_id
    if workgroup_name is not None:
        kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.list_endpoint_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list endpoint access") from exc
    return ListEndpointAccessResult(
        endpoints=resp.get("endpoints"),
        next_token=resp.get("nextToken"),
    )


def list_managed_workgroups(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    source_arn: str | None = None,
    region_name: str | None = None,
) -> ListManagedWorkgroupsResult:
    """List managed workgroups.

    Args:
        max_results: Max results.
        next_token: Next token.
        source_arn: Source arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if source_arn is not None:
        kwargs["sourceArn"] = source_arn
    try:
        resp = client.list_managed_workgroups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list managed workgroups") from exc
    return ListManagedWorkgroupsResult(
        managed_workgroups=resp.get("managedWorkgroups"),
        next_token=resp.get("nextToken"),
    )


def list_recovery_points(
    *,
    end_time: str | None = None,
    max_results: int | None = None,
    namespace_arn: str | None = None,
    namespace_name: str | None = None,
    next_token: str | None = None,
    start_time: str | None = None,
    region_name: str | None = None,
) -> ListRecoveryPointsResult:
    """List recovery points.

    Args:
        end_time: End time.
        max_results: Max results.
        namespace_arn: Namespace arn.
        namespace_name: Namespace name.
        next_token: Next token.
        start_time: Start time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if end_time is not None:
        kwargs["endTime"] = end_time
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if namespace_arn is not None:
        kwargs["namespaceArn"] = namespace_arn
    if namespace_name is not None:
        kwargs["namespaceName"] = namespace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if start_time is not None:
        kwargs["startTime"] = start_time
    try:
        resp = client.list_recovery_points(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list recovery points") from exc
    return ListRecoveryPointsResult(
        next_token=resp.get("nextToken"),
        recovery_points=resp.get("recoveryPoints"),
    )


def list_reservation_offerings(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListReservationOfferingsResult:
    """List reservation offerings.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_reservation_offerings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list reservation offerings") from exc
    return ListReservationOfferingsResult(
        next_token=resp.get("nextToken"),
        reservation_offerings_list=resp.get("reservationOfferingsList"),
    )


def list_reservations(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListReservationsResult:
    """List reservations.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_reservations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list reservations") from exc
    return ListReservationsResult(
        next_token=resp.get("nextToken"),
        reservations_list=resp.get("reservationsList"),
    )


def list_scheduled_actions(
    *,
    max_results: int | None = None,
    namespace_name: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListScheduledActionsResult:
    """List scheduled actions.

    Args:
        max_results: Max results.
        namespace_name: Namespace name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if namespace_name is not None:
        kwargs["namespaceName"] = namespace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_scheduled_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list scheduled actions") from exc
    return ListScheduledActionsResult(
        next_token=resp.get("nextToken"),
        scheduled_actions=resp.get("scheduledActions"),
    )


def list_snapshot_copy_configurations(
    *,
    max_results: int | None = None,
    namespace_name: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSnapshotCopyConfigurationsResult:
    """List snapshot copy configurations.

    Args:
        max_results: Max results.
        namespace_name: Namespace name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if namespace_name is not None:
        kwargs["namespaceName"] = namespace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_snapshot_copy_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list snapshot copy configurations") from exc
    return ListSnapshotCopyConfigurationsResult(
        next_token=resp.get("nextToken"),
        snapshot_copy_configurations=resp.get("snapshotCopyConfigurations"),
    )


def list_snapshots(
    *,
    end_time: str | None = None,
    max_results: int | None = None,
    namespace_arn: str | None = None,
    namespace_name: str | None = None,
    next_token: str | None = None,
    owner_account: str | None = None,
    start_time: str | None = None,
    region_name: str | None = None,
) -> ListSnapshotsResult:
    """List snapshots.

    Args:
        end_time: End time.
        max_results: Max results.
        namespace_arn: Namespace arn.
        namespace_name: Namespace name.
        next_token: Next token.
        owner_account: Owner account.
        start_time: Start time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if end_time is not None:
        kwargs["endTime"] = end_time
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if namespace_arn is not None:
        kwargs["namespaceArn"] = namespace_arn
    if namespace_name is not None:
        kwargs["namespaceName"] = namespace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if owner_account is not None:
        kwargs["ownerAccount"] = owner_account
    if start_time is not None:
        kwargs["startTime"] = start_time
    try:
        resp = client.list_snapshots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list snapshots") from exc
    return ListSnapshotsResult(
        next_token=resp.get("nextToken"),
        snapshots=resp.get("snapshots"),
    )


def list_table_restore_status(
    *,
    max_results: int | None = None,
    namespace_name: str | None = None,
    next_token: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> ListTableRestoreStatusResult:
    """List table restore status.

    Args:
        max_results: Max results.
        namespace_name: Namespace name.
        next_token: Next token.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if namespace_name is not None:
        kwargs["namespaceName"] = namespace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if workgroup_name is not None:
        kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.list_table_restore_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list table restore status") from exc
    return ListTableRestoreStatusResult(
        next_token=resp.get("nextToken"),
        table_restore_statuses=resp.get("tableRestoreStatuses"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def list_tracks(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTracksResult:
    """List tracks.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_tracks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tracks") from exc
    return ListTracksResult(
        next_token=resp.get("nextToken"),
        tracks=resp.get("tracks"),
    )


def list_usage_limits(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    resource_arn: str | None = None,
    usage_type: str | None = None,
    region_name: str | None = None,
) -> ListUsageLimitsResult:
    """List usage limits.

    Args:
        max_results: Max results.
        next_token: Next token.
        resource_arn: Resource arn.
        usage_type: Usage type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if resource_arn is not None:
        kwargs["resourceArn"] = resource_arn
    if usage_type is not None:
        kwargs["usageType"] = usage_type
    try:
        resp = client.list_usage_limits(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list usage limits") from exc
    return ListUsageLimitsResult(
        next_token=resp.get("nextToken"),
        usage_limits=resp.get("usageLimits"),
    )


def put_resource_policy(
    policy: str,
    resource_arn: str,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        policy: Policy.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policy"] = policy
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_policy=resp.get("resourcePolicy"),
    )


def restore_from_recovery_point(
    namespace_name: str,
    recovery_point_id: str,
    workgroup_name: str,
    region_name: str | None = None,
) -> RestoreFromRecoveryPointResult:
    """Restore from recovery point.

    Args:
        namespace_name: Namespace name.
        recovery_point_id: Recovery point id.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["recoveryPointId"] = recovery_point_id
    kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.restore_from_recovery_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore from recovery point") from exc
    return RestoreFromRecoveryPointResult(
        namespace=resp.get("namespace"),
        recovery_point_id=resp.get("recoveryPointId"),
    )


def restore_from_snapshot(
    namespace_name: str,
    workgroup_name: str,
    *,
    admin_password_secret_kms_key_id: str | None = None,
    manage_admin_password: bool | None = None,
    owner_account: str | None = None,
    snapshot_arn: str | None = None,
    snapshot_name: str | None = None,
    region_name: str | None = None,
) -> RestoreFromSnapshotResult:
    """Restore from snapshot.

    Args:
        namespace_name: Namespace name.
        workgroup_name: Workgroup name.
        admin_password_secret_kms_key_id: Admin password secret kms key id.
        manage_admin_password: Manage admin password.
        owner_account: Owner account.
        snapshot_arn: Snapshot arn.
        snapshot_name: Snapshot name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["workgroupName"] = workgroup_name
    if admin_password_secret_kms_key_id is not None:
        kwargs["adminPasswordSecretKmsKeyId"] = admin_password_secret_kms_key_id
    if manage_admin_password is not None:
        kwargs["manageAdminPassword"] = manage_admin_password
    if owner_account is not None:
        kwargs["ownerAccount"] = owner_account
    if snapshot_arn is not None:
        kwargs["snapshotArn"] = snapshot_arn
    if snapshot_name is not None:
        kwargs["snapshotName"] = snapshot_name
    try:
        resp = client.restore_from_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore from snapshot") from exc
    return RestoreFromSnapshotResult(
        namespace=resp.get("namespace"),
        owner_account=resp.get("ownerAccount"),
        snapshot_name=resp.get("snapshotName"),
    )


def restore_table_from_recovery_point(
    namespace_name: str,
    new_table_name: str,
    recovery_point_id: str,
    source_database_name: str,
    source_table_name: str,
    workgroup_name: str,
    *,
    activate_case_sensitive_identifier: bool | None = None,
    source_schema_name: str | None = None,
    target_database_name: str | None = None,
    target_schema_name: str | None = None,
    region_name: str | None = None,
) -> RestoreTableFromRecoveryPointResult:
    """Restore table from recovery point.

    Args:
        namespace_name: Namespace name.
        new_table_name: New table name.
        recovery_point_id: Recovery point id.
        source_database_name: Source database name.
        source_table_name: Source table name.
        workgroup_name: Workgroup name.
        activate_case_sensitive_identifier: Activate case sensitive identifier.
        source_schema_name: Source schema name.
        target_database_name: Target database name.
        target_schema_name: Target schema name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["newTableName"] = new_table_name
    kwargs["recoveryPointId"] = recovery_point_id
    kwargs["sourceDatabaseName"] = source_database_name
    kwargs["sourceTableName"] = source_table_name
    kwargs["workgroupName"] = workgroup_name
    if activate_case_sensitive_identifier is not None:
        kwargs["activateCaseSensitiveIdentifier"] = activate_case_sensitive_identifier
    if source_schema_name is not None:
        kwargs["sourceSchemaName"] = source_schema_name
    if target_database_name is not None:
        kwargs["targetDatabaseName"] = target_database_name
    if target_schema_name is not None:
        kwargs["targetSchemaName"] = target_schema_name
    try:
        resp = client.restore_table_from_recovery_point(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore table from recovery point") from exc
    return RestoreTableFromRecoveryPointResult(
        table_restore_status=resp.get("tableRestoreStatus"),
    )


def restore_table_from_snapshot(
    namespace_name: str,
    new_table_name: str,
    snapshot_name: str,
    source_database_name: str,
    source_table_name: str,
    workgroup_name: str,
    *,
    activate_case_sensitive_identifier: bool | None = None,
    source_schema_name: str | None = None,
    target_database_name: str | None = None,
    target_schema_name: str | None = None,
    region_name: str | None = None,
) -> RestoreTableFromSnapshotResult:
    """Restore table from snapshot.

    Args:
        namespace_name: Namespace name.
        new_table_name: New table name.
        snapshot_name: Snapshot name.
        source_database_name: Source database name.
        source_table_name: Source table name.
        workgroup_name: Workgroup name.
        activate_case_sensitive_identifier: Activate case sensitive identifier.
        source_schema_name: Source schema name.
        target_database_name: Target database name.
        target_schema_name: Target schema name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespaceName"] = namespace_name
    kwargs["newTableName"] = new_table_name
    kwargs["snapshotName"] = snapshot_name
    kwargs["sourceDatabaseName"] = source_database_name
    kwargs["sourceTableName"] = source_table_name
    kwargs["workgroupName"] = workgroup_name
    if activate_case_sensitive_identifier is not None:
        kwargs["activateCaseSensitiveIdentifier"] = activate_case_sensitive_identifier
    if source_schema_name is not None:
        kwargs["sourceSchemaName"] = source_schema_name
    if target_database_name is not None:
        kwargs["targetDatabaseName"] = target_database_name
    if target_schema_name is not None:
        kwargs["targetSchemaName"] = target_schema_name
    try:
        resp = client.restore_table_from_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore table from snapshot") from exc
    return RestoreTableFromSnapshotResult(
        table_restore_status=resp.get("tableRestoreStatus"),
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
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
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
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_custom_domain_association(
    custom_domain_certificate_arn: str,
    custom_domain_name: str,
    workgroup_name: str,
    region_name: str | None = None,
) -> UpdateCustomDomainAssociationResult:
    """Update custom domain association.

    Args:
        custom_domain_certificate_arn: Custom domain certificate arn.
        custom_domain_name: Custom domain name.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["customDomainCertificateArn"] = custom_domain_certificate_arn
    kwargs["customDomainName"] = custom_domain_name
    kwargs["workgroupName"] = workgroup_name
    try:
        resp = client.update_custom_domain_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update custom domain association") from exc
    return UpdateCustomDomainAssociationResult(
        custom_domain_certificate_arn=resp.get("customDomainCertificateArn"),
        custom_domain_certificate_expiry_time=resp.get("customDomainCertificateExpiryTime"),
        custom_domain_name=resp.get("customDomainName"),
        workgroup_name=resp.get("workgroupName"),
    )


def update_endpoint_access(
    endpoint_name: str,
    *,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateEndpointAccessResult:
    """Update endpoint access.

    Args:
        endpoint_name: Endpoint name.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["endpointName"] = endpoint_name
    if vpc_security_group_ids is not None:
        kwargs["vpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = client.update_endpoint_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update endpoint access") from exc
    return UpdateEndpointAccessResult(
        endpoint=resp.get("endpoint"),
    )


def update_scheduled_action(
    scheduled_action_name: str,
    *,
    enabled: bool | None = None,
    end_time: str | None = None,
    role_arn: str | None = None,
    schedule: dict[str, Any] | None = None,
    scheduled_action_description: str | None = None,
    start_time: str | None = None,
    target_action: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateScheduledActionResult:
    """Update scheduled action.

    Args:
        scheduled_action_name: Scheduled action name.
        enabled: Enabled.
        end_time: End time.
        role_arn: Role arn.
        schedule: Schedule.
        scheduled_action_description: Scheduled action description.
        start_time: Start time.
        target_action: Target action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledActionName"] = scheduled_action_name
    if enabled is not None:
        kwargs["enabled"] = enabled
    if end_time is not None:
        kwargs["endTime"] = end_time
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if schedule is not None:
        kwargs["schedule"] = schedule
    if scheduled_action_description is not None:
        kwargs["scheduledActionDescription"] = scheduled_action_description
    if start_time is not None:
        kwargs["startTime"] = start_time
    if target_action is not None:
        kwargs["targetAction"] = target_action
    try:
        resp = client.update_scheduled_action(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update scheduled action") from exc
    return UpdateScheduledActionResult(
        scheduled_action=resp.get("scheduledAction"),
    )


def update_snapshot(
    snapshot_name: str,
    *,
    retention_period: int | None = None,
    region_name: str | None = None,
) -> UpdateSnapshotResult:
    """Update snapshot.

    Args:
        snapshot_name: Snapshot name.
        retention_period: Retention period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["snapshotName"] = snapshot_name
    if retention_period is not None:
        kwargs["retentionPeriod"] = retention_period
    try:
        resp = client.update_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update snapshot") from exc
    return UpdateSnapshotResult(
        snapshot=resp.get("snapshot"),
    )


def update_snapshot_copy_configuration(
    snapshot_copy_configuration_id: str,
    *,
    snapshot_retention_period: int | None = None,
    region_name: str | None = None,
) -> UpdateSnapshotCopyConfigurationResult:
    """Update snapshot copy configuration.

    Args:
        snapshot_copy_configuration_id: Snapshot copy configuration id.
        snapshot_retention_period: Snapshot retention period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["snapshotCopyConfigurationId"] = snapshot_copy_configuration_id
    if snapshot_retention_period is not None:
        kwargs["snapshotRetentionPeriod"] = snapshot_retention_period
    try:
        resp = client.update_snapshot_copy_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update snapshot copy configuration") from exc
    return UpdateSnapshotCopyConfigurationResult(
        snapshot_copy_configuration=resp.get("snapshotCopyConfiguration"),
    )


def update_usage_limit(
    usage_limit_id: str,
    *,
    amount: int | None = None,
    breach_action: str | None = None,
    region_name: str | None = None,
) -> UpdateUsageLimitResult:
    """Update usage limit.

    Args:
        usage_limit_id: Usage limit id.
        amount: Amount.
        breach_action: Breach action.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("redshift-serverless", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["usageLimitId"] = usage_limit_id
    if amount is not None:
        kwargs["amount"] = amount
    if breach_action is not None:
        kwargs["breachAction"] = breach_action
    try:
        resp = client.update_usage_limit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update usage limit") from exc
    return UpdateUsageLimitResult(
        usage_limit=resp.get("usageLimit"),
    )
