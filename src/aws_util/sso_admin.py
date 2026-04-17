"""aws_util.sso_admin — AWS SSO Admin (IAM Identity Center) utilities.

Provides high-level helpers for managing AWS IAM Identity Center instances,
permission sets, managed/inline policies, and account assignments.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AccountAssignmentResult",
    "AccountAssignmentStatusResult",
    "CreateApplicationResult",
    "CreateTrustedTokenIssuerResult",
    "DescribeAccountAssignmentCreationStatusResult",
    "DescribeAccountAssignmentDeletionStatusResult",
    "DescribeApplicationAssignmentResult",
    "DescribeApplicationProviderResult",
    "DescribeApplicationResult",
    "DescribeInstanceAccessControlAttributeConfigurationResult",
    "DescribePermissionSetProvisioningStatusResult",
    "DescribeTrustedTokenIssuerResult",
    "GetApplicationAccessScopeResult",
    "GetApplicationAssignmentConfigurationResult",
    "GetApplicationAuthenticationMethodResult",
    "GetApplicationGrantResult",
    "GetApplicationSessionConfigurationResult",
    "GetPermissionsBoundaryForPermissionSetResult",
    "InstanceResult",
    "ListAccountAssignmentCreationStatusResult",
    "ListAccountAssignmentDeletionStatusResult",
    "ListAccountAssignmentsForPrincipalResult",
    "ListApplicationAccessScopesResult",
    "ListApplicationAssignmentsForPrincipalResult",
    "ListApplicationAssignmentsResult",
    "ListApplicationAuthenticationMethodsResult",
    "ListApplicationGrantsResult",
    "ListApplicationProvidersResult",
    "ListApplicationsResult",
    "ListCustomerManagedPolicyReferencesInPermissionSetResult",
    "ListPermissionSetProvisioningStatusResult",
    "ListPermissionSetsProvisionedToAccountResult",
    "ListTagsForResourceResult",
    "ListTrustedTokenIssuersResult",
    "ManagedPolicyResult",
    "PermissionSetResult",
    "ProvisionStatusResult",
    "attach_customer_managed_policy_reference_to_permission_set",
    "attach_managed_policy_to_permission_set",
    "create_account_assignment",
    "create_application",
    "create_application_assignment",
    "create_instance",
    "create_instance_access_control_attribute_configuration",
    "create_permission_set",
    "create_trusted_token_issuer",
    "delete_account_assignment",
    "delete_application",
    "delete_application_access_scope",
    "delete_application_assignment",
    "delete_application_authentication_method",
    "delete_application_grant",
    "delete_inline_policy_from_permission_set",
    "delete_instance",
    "delete_instance_access_control_attribute_configuration",
    "delete_permission_set",
    "delete_permissions_boundary_from_permission_set",
    "delete_trusted_token_issuer",
    "describe_account_assignment_creation_status",
    "describe_account_assignment_deletion_status",
    "describe_application",
    "describe_application_assignment",
    "describe_application_provider",
    "describe_instance",
    "describe_instance_access_control_attribute_configuration",
    "describe_permission_set",
    "describe_permission_set_provisioning_status",
    "describe_trusted_token_issuer",
    "detach_customer_managed_policy_reference_from_permission_set",
    "detach_managed_policy_from_permission_set",
    "get_application_access_scope",
    "get_application_assignment_configuration",
    "get_application_authentication_method",
    "get_application_grant",
    "get_application_session_configuration",
    "get_inline_policy_for_permission_set",
    "get_permissions_boundary_for_permission_set",
    "list_account_assignment_creation_status",
    "list_account_assignment_deletion_status",
    "list_account_assignments",
    "list_account_assignments_for_principal",
    "list_accounts_for_provisioned_permission_set",
    "list_application_access_scopes",
    "list_application_assignments",
    "list_application_assignments_for_principal",
    "list_application_authentication_methods",
    "list_application_grants",
    "list_application_providers",
    "list_applications",
    "list_customer_managed_policy_references_in_permission_set",
    "list_instances",
    "list_managed_policies_in_permission_set",
    "list_permission_set_provisioning_status",
    "list_permission_sets",
    "list_permission_sets_provisioned_to_account",
    "list_tags_for_resource",
    "list_trusted_token_issuers",
    "provision_permission_set",
    "put_application_access_scope",
    "put_application_assignment_configuration",
    "put_application_authentication_method",
    "put_application_grant",
    "put_application_session_configuration",
    "put_inline_policy_to_permission_set",
    "put_permissions_boundary_to_permission_set",
    "tag_resource",
    "untag_resource",
    "update_application",
    "update_instance",
    "update_instance_access_control_attribute_configuration",
    "update_permission_set",
    "update_trusted_token_issuer",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class InstanceResult(BaseModel):
    """Metadata for an IAM Identity Center instance."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    instance_arn: str = ""
    identity_store_id: str = ""
    name: str = ""
    status: str = ""
    owner_account_id: str = ""
    created_date: Any = None
    extra: dict[str, Any] = {}


class PermissionSetResult(BaseModel):
    """Metadata for a permission set."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    permission_set_arn: str = ""
    name: str = ""
    description: str = ""
    session_duration: str = ""
    relay_state: str = ""
    created_date: Any = None
    extra: dict[str, Any] = {}


class ManagedPolicyResult(BaseModel):
    """Metadata for a managed policy attached to a permission set."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str = ""
    arn: str = ""
    extra: dict[str, Any] = {}


class AccountAssignmentResult(BaseModel):
    """Metadata for an account assignment."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    account_id: str = ""
    permission_set_arn: str = ""
    principal_type: str = ""
    principal_id: str = ""
    extra: dict[str, Any] = {}


class AccountAssignmentStatusResult(BaseModel):
    """Status of a create/delete account assignment operation."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    status: str = ""
    request_id: str = ""
    failure_reason: str = ""
    target_id: str = ""
    target_type: str = ""
    permission_set_arn: str = ""
    principal_type: str = ""
    principal_id: str = ""
    created_date: Any = None
    extra: dict[str, Any] = {}


class ProvisionStatusResult(BaseModel):
    """Status of a permission set provisioning operation."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    status: str = ""
    request_id: str = ""
    account_id: str = ""
    permission_set_arn: str = ""
    failure_reason: str = ""
    created_date: Any = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

_INSTANCE_KEYS = {
    "InstanceArn",
    "IdentityStoreId",
    "Name",
    "Status",
    "OwnerAccountId",
    "CreatedDate",
}


def _parse_instance(data: dict[str, Any]) -> InstanceResult:
    """Parse a raw Instance dict into a model."""
    return InstanceResult(
        instance_arn=data.get("InstanceArn", ""),
        identity_store_id=data.get("IdentityStoreId", ""),
        name=data.get("Name", ""),
        status=data.get("Status", ""),
        owner_account_id=data.get("OwnerAccountId", ""),
        created_date=data.get("CreatedDate"),
        extra={k: v for k, v in data.items() if k not in _INSTANCE_KEYS},
    )


_PERMISSION_SET_KEYS = {
    "PermissionSetArn",
    "Name",
    "Description",
    "SessionDuration",
    "RelayState",
    "CreatedDate",
}


def _parse_permission_set(
    data: dict[str, Any],
) -> PermissionSetResult:
    """Parse a raw PermissionSet dict into a model."""
    return PermissionSetResult(
        permission_set_arn=data.get("PermissionSetArn", ""),
        name=data.get("Name", ""),
        description=data.get("Description", ""),
        session_duration=data.get("SessionDuration", ""),
        relay_state=data.get("RelayState", ""),
        created_date=data.get("CreatedDate"),
        extra={k: v for k, v in data.items() if k not in _PERMISSION_SET_KEYS},
    )


_MANAGED_POLICY_KEYS = {"Name", "Arn"}


def _parse_managed_policy(
    data: dict[str, Any],
) -> ManagedPolicyResult:
    """Parse a raw managed policy attachment dict into a model."""
    return ManagedPolicyResult(
        name=data.get("Name", ""),
        arn=data.get("Arn", ""),
        extra={k: v for k, v in data.items() if k not in _MANAGED_POLICY_KEYS},
    )


_ACCOUNT_ASSIGNMENT_KEYS = {
    "AccountId",
    "PermissionSetArn",
    "PrincipalType",
    "PrincipalId",
}


def _parse_account_assignment(
    data: dict[str, Any],
) -> AccountAssignmentResult:
    """Parse a raw AccountAssignment dict into a model."""
    return AccountAssignmentResult(
        account_id=data.get("AccountId", ""),
        permission_set_arn=data.get("PermissionSetArn", ""),
        principal_type=data.get("PrincipalType", ""),
        principal_id=data.get("PrincipalId", ""),
        extra={k: v for k, v in data.items() if k not in _ACCOUNT_ASSIGNMENT_KEYS},
    )


_ASSIGNMENT_STATUS_KEYS = {
    "Status",
    "RequestId",
    "FailureReason",
    "TargetId",
    "TargetType",
    "PermissionSetArn",
    "PrincipalType",
    "PrincipalId",
    "CreatedDate",
}


def _parse_assignment_status(
    data: dict[str, Any],
) -> AccountAssignmentStatusResult:
    """Parse a raw AccountAssignmentOperationStatus dict."""
    return AccountAssignmentStatusResult(
        status=data.get("Status", ""),
        request_id=data.get("RequestId", ""),
        failure_reason=data.get("FailureReason", ""),
        target_id=data.get("TargetId", ""),
        target_type=data.get("TargetType", ""),
        permission_set_arn=data.get("PermissionSetArn", ""),
        principal_type=data.get("PrincipalType", ""),
        principal_id=data.get("PrincipalId", ""),
        created_date=data.get("CreatedDate"),
        extra={k: v for k, v in data.items() if k not in _ASSIGNMENT_STATUS_KEYS},
    )


_PROVISION_STATUS_KEYS = {
    "Status",
    "RequestId",
    "AccountId",
    "PermissionSetArn",
    "FailureReason",
    "CreatedDate",
}


def _parse_provision_status(
    data: dict[str, Any],
) -> ProvisionStatusResult:
    """Parse a raw PermissionSetProvisioningStatus dict."""
    return ProvisionStatusResult(
        status=data.get("Status", ""),
        request_id=data.get("RequestId", ""),
        account_id=data.get("AccountId", ""),
        permission_set_arn=data.get("PermissionSetArn", ""),
        failure_reason=data.get("FailureReason", ""),
        created_date=data.get("CreatedDate"),
        extra={k: v for k, v in data.items() if k not in _PROVISION_STATUS_KEYS},
    )


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


def create_instance(
    *,
    name: str | None = None,
    region_name: str | None = None,
) -> InstanceResult:
    """Create an IAM Identity Center instance.

    Args:
        name: Optional friendly name for the instance.
        region_name: AWS region override.

    Returns:
        An :class:`InstanceResult` for the new instance.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = client.create_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_instance failed") from exc
    return _parse_instance(resp)


def list_instances(
    *,
    region_name: str | None = None,
) -> list[InstanceResult]:
    """List all IAM Identity Center instances.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`InstanceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    results: list[InstanceResult] = []
    try:
        paginator = client.get_paginator("list_instances")
        for page in paginator.paginate():
            for inst in page.get("Instances", []):
                results.append(_parse_instance(inst))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_instances failed") from exc
    return results


def describe_instance(
    instance_arn: str,
    *,
    region_name: str | None = None,
) -> InstanceResult:
    """Describe an IAM Identity Center instance.

    Args:
        instance_arn: The ARN of the SSO instance.
        region_name: AWS region override.

    Returns:
        An :class:`InstanceResult` describing the instance.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        resp = client.describe_instance(
            InstanceArn=instance_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_instance failed for {instance_arn!r}",
        ) from exc
    return _parse_instance(resp)


def delete_instance(
    instance_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an IAM Identity Center instance.

    Args:
        instance_arn: The ARN of the SSO instance to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.delete_instance(InstanceArn=instance_arn)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_instance failed for {instance_arn!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Permission set operations
# ---------------------------------------------------------------------------


def create_permission_set(
    instance_arn: str,
    name: str,
    *,
    description: str = "",
    session_duration: str = "PT1H",
    relay_state: str | None = None,
    region_name: str | None = None,
) -> PermissionSetResult:
    """Create a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        name: Name for the permission set.
        description: Optional description.
        session_duration: ISO 8601 duration (default ``"PT1H"``).
        relay_state: Optional relay state URL.
        region_name: AWS region override.

    Returns:
        A :class:`PermissionSetResult` for the new permission set.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "Name": name,
        "SessionDuration": session_duration,
    }
    if description:
        kwargs["Description"] = description
    if relay_state is not None:
        kwargs["RelayState"] = relay_state
    try:
        resp = client.create_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_permission_set failed for {name!r}") from exc
    return _parse_permission_set(resp["PermissionSet"])


def describe_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> PermissionSetResult:
    """Describe a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Returns:
        A :class:`PermissionSetResult` describing the permission set.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        resp = client.describe_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_permission_set failed for {permission_set_arn!r}",
        ) from exc
    return _parse_permission_set(resp["PermissionSet"])


def list_permission_sets(
    instance_arn: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List permission set ARNs for an instance.

    Args:
        instance_arn: The ARN of the SSO instance.
        region_name: AWS region override.

    Returns:
        A list of permission set ARN strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    results: list[str] = []
    try:
        paginator = client.get_paginator("list_permission_sets")
        for page in paginator.paginate(
            InstanceArn=instance_arn,
        ):
            results.extend(page.get("PermissionSets", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_permission_sets failed") from exc
    return results


def update_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    description: str | None = None,
    session_duration: str | None = None,
    relay_state: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update an existing permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set to update.
        description: New description (optional).
        session_duration: New session duration (optional).
        relay_state: New relay state URL (optional).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "PermissionSetArn": permission_set_arn,
    }
    if description is not None:
        kwargs["Description"] = description
    if session_duration is not None:
        kwargs["SessionDuration"] = session_duration
    if relay_state is not None:
        kwargs["RelayState"] = relay_state
    try:
        client.update_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"update_permission_set failed for {permission_set_arn!r}",
        ) from exc


def delete_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.delete_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_permission_set failed for {permission_set_arn!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Managed policy operations
# ---------------------------------------------------------------------------


def attach_managed_policy_to_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    managed_policy_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Attach an AWS managed policy to a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        managed_policy_arn: The ARN of the managed policy to attach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.attach_managed_policy_to_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            ManagedPolicyArn=managed_policy_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "attach_managed_policy_to_permission_set failed",
        ) from exc


def detach_managed_policy_from_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    managed_policy_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Detach an AWS managed policy from a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        managed_policy_arn: The ARN of the managed policy to detach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.detach_managed_policy_from_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            ManagedPolicyArn=managed_policy_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "detach_managed_policy_from_permission_set failed",
        ) from exc


def list_managed_policies_in_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> list[ManagedPolicyResult]:
    """List managed policies attached to a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Returns:
        A list of :class:`ManagedPolicyResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    results: list[ManagedPolicyResult] = []
    try:
        paginator = client.get_paginator("list_managed_policies_in_permission_set")
        for page in paginator.paginate(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        ):
            for pol in page.get("AttachedManagedPolicies", []):
                results.append(_parse_managed_policy(pol))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "list_managed_policies_in_permission_set failed",
        ) from exc
    return results


# ---------------------------------------------------------------------------
# Inline policy operations
# ---------------------------------------------------------------------------


def put_inline_policy_to_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    inline_policy: str,
    *,
    region_name: str | None = None,
) -> None:
    """Put an inline policy on a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        inline_policy: JSON policy document string.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.put_inline_policy_to_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            InlinePolicy=inline_policy,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "put_inline_policy_to_permission_set failed",
        ) from exc


def get_inline_policy_for_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> str:
    """Get the inline policy for a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Returns:
        The JSON inline policy document string, or ``""`` if none.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        resp = client.get_inline_policy_for_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "get_inline_policy_for_permission_set failed",
        ) from exc
    return resp.get("InlinePolicy", "")


def delete_inline_policy_from_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete the inline policy from a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        client.delete_inline_policy_from_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "delete_inline_policy_from_permission_set failed",
        ) from exc


# ---------------------------------------------------------------------------
# Account assignment operations
# ---------------------------------------------------------------------------


def create_account_assignment(
    instance_arn: str,
    target_id: str,
    target_type: str,
    permission_set_arn: str,
    principal_type: str,
    principal_id: str,
    *,
    region_name: str | None = None,
) -> AccountAssignmentStatusResult:
    """Create an account assignment.

    Args:
        instance_arn: The ARN of the SSO instance.
        target_id: The AWS account ID.
        target_type: ``"AWS_ACCOUNT"``.
        permission_set_arn: The ARN of the permission set.
        principal_type: ``"USER"`` or ``"GROUP"``.
        principal_id: The principal ID.
        region_name: AWS region override.

    Returns:
        An :class:`AccountAssignmentStatusResult` for the operation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        resp = client.create_account_assignment(
            InstanceArn=instance_arn,
            TargetId=target_id,
            TargetType=target_type,
            PermissionSetArn=permission_set_arn,
            PrincipalType=principal_type,
            PrincipalId=principal_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_account_assignment failed") from exc
    return _parse_assignment_status(resp.get("AccountAssignmentCreationStatus", {}))


def list_account_assignments(
    instance_arn: str,
    account_id: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> list[AccountAssignmentResult]:
    """List account assignments for a permission set and account.

    Args:
        instance_arn: The ARN of the SSO instance.
        account_id: The AWS account ID.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Returns:
        A list of :class:`AccountAssignmentResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    results: list[AccountAssignmentResult] = []
    try:
        paginator = client.get_paginator("list_account_assignments")
        for page in paginator.paginate(
            InstanceArn=instance_arn,
            AccountId=account_id,
            PermissionSetArn=permission_set_arn,
        ):
            for aa in page.get("AccountAssignments", []):
                results.append(_parse_account_assignment(aa))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_account_assignments failed") from exc
    return results


def delete_account_assignment(
    instance_arn: str,
    target_id: str,
    target_type: str,
    permission_set_arn: str,
    principal_type: str,
    principal_id: str,
    *,
    region_name: str | None = None,
) -> AccountAssignmentStatusResult:
    """Delete an account assignment.

    Args:
        instance_arn: The ARN of the SSO instance.
        target_id: The AWS account ID.
        target_type: ``"AWS_ACCOUNT"``.
        permission_set_arn: The ARN of the permission set.
        principal_type: ``"USER"`` or ``"GROUP"``.
        principal_id: The principal ID.
        region_name: AWS region override.

    Returns:
        An :class:`AccountAssignmentStatusResult` for the operation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    try:
        resp = client.delete_account_assignment(
            InstanceArn=instance_arn,
            TargetId=target_id,
            TargetType=target_type,
            PermissionSetArn=permission_set_arn,
            PrincipalType=principal_type,
            PrincipalId=principal_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_account_assignment failed") from exc
    return _parse_assignment_status(resp.get("AccountAssignmentDeletionStatus", {}))


def list_accounts_for_provisioned_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    provisioning_status: str = "LATEST_PERMISSION_SET_PROVISIONED",
    region_name: str | None = None,
) -> list[str]:
    """List account IDs for a provisioned permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        provisioning_status: Filter by provisioning status.
        region_name: AWS region override.

    Returns:
        A list of AWS account ID strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    results: list[str] = []
    try:
        paginator = client.get_paginator("list_accounts_for_provisioned_permission_set")
        for page in paginator.paginate(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            ProvisioningStatus=provisioning_status,
        ):
            results.extend(page.get("AccountIds", []))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "list_accounts_for_provisioned_permission_set failed",
        ) from exc
    return results


def provision_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    target_type: str = "ALL_PROVISIONED_ACCOUNTS",
    *,
    target_id: str | None = None,
    region_name: str | None = None,
) -> ProvisionStatusResult:
    """Provision a permission set to accounts.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        target_type: ``"ALL_PROVISIONED_ACCOUNTS"`` or
            ``"AWS_ACCOUNT"``.
        target_id: Account ID when ``target_type`` is
            ``"AWS_ACCOUNT"``.
        region_name: AWS region override.

    Returns:
        A :class:`ProvisionStatusResult` for the operation.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "PermissionSetArn": permission_set_arn,
        "TargetType": target_type,
    }
    if target_id is not None:
        kwargs["TargetId"] = target_id
    try:
        resp = client.provision_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "provision_permission_set failed") from exc
    return _parse_provision_status(resp.get("PermissionSetProvisioningStatus", {}))


class CreateApplicationResult(BaseModel):
    """Result of create_application."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None


class CreateTrustedTokenIssuerResult(BaseModel):
    """Result of create_trusted_token_issuer."""

    model_config = ConfigDict(frozen=True)

    trusted_token_issuer_arn: str | None = None


class DescribeAccountAssignmentCreationStatusResult(BaseModel):
    """Result of describe_account_assignment_creation_status."""

    model_config = ConfigDict(frozen=True)

    account_assignment_creation_status: dict[str, Any] | None = None


class DescribeAccountAssignmentDeletionStatusResult(BaseModel):
    """Result of describe_account_assignment_deletion_status."""

    model_config = ConfigDict(frozen=True)

    account_assignment_deletion_status: dict[str, Any] | None = None


class DescribeApplicationResult(BaseModel):
    """Result of describe_application."""

    model_config = ConfigDict(frozen=True)

    application_arn: str | None = None
    application_provider_arn: str | None = None
    name: str | None = None
    application_account: str | None = None
    instance_arn: str | None = None
    status: str | None = None
    portal_options: dict[str, Any] | None = None
    description: str | None = None
    created_date: str | None = None


class DescribeApplicationAssignmentResult(BaseModel):
    """Result of describe_application_assignment."""

    model_config = ConfigDict(frozen=True)

    principal_type: str | None = None
    principal_id: str | None = None
    application_arn: str | None = None


class DescribeApplicationProviderResult(BaseModel):
    """Result of describe_application_provider."""

    model_config = ConfigDict(frozen=True)

    application_provider_arn: str | None = None
    federation_protocol: str | None = None
    display_data: dict[str, Any] | None = None
    resource_server_config: dict[str, Any] | None = None


class DescribeInstanceAccessControlAttributeConfigurationResult(BaseModel):
    """Result of describe_instance_access_control_attribute_configuration."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    status_reason: str | None = None
    instance_access_control_attribute_configuration: dict[str, Any] | None = None


class DescribePermissionSetProvisioningStatusResult(BaseModel):
    """Result of describe_permission_set_provisioning_status."""

    model_config = ConfigDict(frozen=True)

    permission_set_provisioning_status: dict[str, Any] | None = None


class DescribeTrustedTokenIssuerResult(BaseModel):
    """Result of describe_trusted_token_issuer."""

    model_config = ConfigDict(frozen=True)

    trusted_token_issuer_arn: str | None = None
    name: str | None = None
    trusted_token_issuer_type: str | None = None
    trusted_token_issuer_configuration: dict[str, Any] | None = None


class GetApplicationAccessScopeResult(BaseModel):
    """Result of get_application_access_scope."""

    model_config = ConfigDict(frozen=True)

    scope: str | None = None
    authorized_targets: list[str] | None = None


class GetApplicationAssignmentConfigurationResult(BaseModel):
    """Result of get_application_assignment_configuration."""

    model_config = ConfigDict(frozen=True)

    assignment_required: bool | None = None


class GetApplicationAuthenticationMethodResult(BaseModel):
    """Result of get_application_authentication_method."""

    model_config = ConfigDict(frozen=True)

    authentication_method: dict[str, Any] | None = None


class GetApplicationGrantResult(BaseModel):
    """Result of get_application_grant."""

    model_config = ConfigDict(frozen=True)

    grant: dict[str, Any] | None = None


class GetApplicationSessionConfigurationResult(BaseModel):
    """Result of get_application_session_configuration."""

    model_config = ConfigDict(frozen=True)

    user_background_session_application_status: str | None = None


class GetPermissionsBoundaryForPermissionSetResult(BaseModel):
    """Result of get_permissions_boundary_for_permission_set."""

    model_config = ConfigDict(frozen=True)

    permissions_boundary: dict[str, Any] | None = None


class ListAccountAssignmentCreationStatusResult(BaseModel):
    """Result of list_account_assignment_creation_status."""

    model_config = ConfigDict(frozen=True)

    account_assignments_creation_status: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAccountAssignmentDeletionStatusResult(BaseModel):
    """Result of list_account_assignment_deletion_status."""

    model_config = ConfigDict(frozen=True)

    account_assignments_deletion_status: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAccountAssignmentsForPrincipalResult(BaseModel):
    """Result of list_account_assignments_for_principal."""

    model_config = ConfigDict(frozen=True)

    account_assignments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationAccessScopesResult(BaseModel):
    """Result of list_application_access_scopes."""

    model_config = ConfigDict(frozen=True)

    scopes: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationAssignmentsResult(BaseModel):
    """Result of list_application_assignments."""

    model_config = ConfigDict(frozen=True)

    application_assignments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationAssignmentsForPrincipalResult(BaseModel):
    """Result of list_application_assignments_for_principal."""

    model_config = ConfigDict(frozen=True)

    application_assignments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationAuthenticationMethodsResult(BaseModel):
    """Result of list_application_authentication_methods."""

    model_config = ConfigDict(frozen=True)

    authentication_methods: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationGrantsResult(BaseModel):
    """Result of list_application_grants."""

    model_config = ConfigDict(frozen=True)

    grants: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationProvidersResult(BaseModel):
    """Result of list_application_providers."""

    model_config = ConfigDict(frozen=True)

    application_providers: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApplicationsResult(BaseModel):
    """Result of list_applications."""

    model_config = ConfigDict(frozen=True)

    applications: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListCustomerManagedPolicyReferencesInPermissionSetResult(BaseModel):
    """Result of list_customer_managed_policy_references_in_permission_set."""

    model_config = ConfigDict(frozen=True)

    customer_managed_policy_references: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPermissionSetProvisioningStatusResult(BaseModel):
    """Result of list_permission_set_provisioning_status."""

    model_config = ConfigDict(frozen=True)

    permission_sets_provisioning_status: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPermissionSetsProvisionedToAccountResult(BaseModel):
    """Result of list_permission_sets_provisioned_to_account."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    permission_sets: list[str] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTrustedTokenIssuersResult(BaseModel):
    """Result of list_trusted_token_issuers."""

    model_config = ConfigDict(frozen=True)

    trusted_token_issuers: list[dict[str, Any]] | None = None
    next_token: str | None = None


def attach_customer_managed_policy_reference_to_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    customer_managed_policy_reference: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Attach customer managed policy reference to permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        customer_managed_policy_reference: Customer managed policy reference.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["CustomerManagedPolicyReference"] = customer_managed_policy_reference
    try:
        client.attach_customer_managed_policy_reference_to_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to attach customer managed policy reference to permission set"
        ) from exc
    return None


def create_application(
    instance_arn: str,
    application_provider_arn: str,
    name: str,
    *,
    description: str | None = None,
    portal_options: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    status: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateApplicationResult:
    """Create application.

    Args:
        instance_arn: Instance arn.
        application_provider_arn: Application provider arn.
        name: Name.
        description: Description.
        portal_options: Portal options.
        tags: Tags.
        status: Status.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["ApplicationProviderArn"] = application_provider_arn
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if portal_options is not None:
        kwargs["PortalOptions"] = portal_options
    if tags is not None:
        kwargs["Tags"] = tags
    if status is not None:
        kwargs["Status"] = status
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create application") from exc
    return CreateApplicationResult(
        application_arn=resp.get("ApplicationArn"),
    )


def create_application_assignment(
    application_arn: str,
    principal_id: str,
    principal_type: str,
    region_name: str | None = None,
) -> None:
    """Create application assignment.

    Args:
        application_arn: Application arn.
        principal_id: Principal id.
        principal_type: Principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        client.create_application_assignment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create application assignment") from exc
    return None


def create_instance_access_control_attribute_configuration(
    instance_arn: str,
    instance_access_control_attribute_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Create instance access control attribute configuration.

    Args:
        instance_arn: Instance arn.
        instance_access_control_attribute_configuration: Instance access control attribute configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["InstanceAccessControlAttributeConfiguration"] = (
        instance_access_control_attribute_configuration
    )
    try:
        client.create_instance_access_control_attribute_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to create instance access control attribute configuration"
        ) from exc
    return None


def create_trusted_token_issuer(
    instance_arn: str,
    name: str,
    trusted_token_issuer_type: str,
    trusted_token_issuer_configuration: dict[str, Any],
    *,
    client_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTrustedTokenIssuerResult:
    """Create trusted token issuer.

    Args:
        instance_arn: Instance arn.
        name: Name.
        trusted_token_issuer_type: Trusted token issuer type.
        trusted_token_issuer_configuration: Trusted token issuer configuration.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["Name"] = name
    kwargs["TrustedTokenIssuerType"] = trusted_token_issuer_type
    kwargs["TrustedTokenIssuerConfiguration"] = trusted_token_issuer_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_trusted_token_issuer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create trusted token issuer") from exc
    return CreateTrustedTokenIssuerResult(
        trusted_token_issuer_arn=resp.get("TrustedTokenIssuerArn"),
    )


def delete_application(
    application_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete application.

    Args:
        application_arn: Application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        client.delete_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application") from exc
    return None


def delete_application_access_scope(
    application_arn: str,
    scope: str,
    region_name: str | None = None,
) -> None:
    """Delete application access scope.

    Args:
        application_arn: Application arn.
        scope: Scope.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["Scope"] = scope
    try:
        client.delete_application_access_scope(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application access scope") from exc
    return None


def delete_application_assignment(
    application_arn: str,
    principal_id: str,
    principal_type: str,
    region_name: str | None = None,
) -> None:
    """Delete application assignment.

    Args:
        application_arn: Application arn.
        principal_id: Principal id.
        principal_type: Principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        client.delete_application_assignment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application assignment") from exc
    return None


def delete_application_authentication_method(
    application_arn: str,
    authentication_method_type: str,
    region_name: str | None = None,
) -> None:
    """Delete application authentication method.

    Args:
        application_arn: Application arn.
        authentication_method_type: Authentication method type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    try:
        client.delete_application_authentication_method(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application authentication method") from exc
    return None


def delete_application_grant(
    application_arn: str,
    grant_type: str,
    region_name: str | None = None,
) -> None:
    """Delete application grant.

    Args:
        application_arn: Application arn.
        grant_type: Grant type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    try:
        client.delete_application_grant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete application grant") from exc
    return None


def delete_instance_access_control_attribute_configuration(
    instance_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete instance access control attribute configuration.

    Args:
        instance_arn: Instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    try:
        client.delete_instance_access_control_attribute_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete instance access control attribute configuration"
        ) from exc
    return None


def delete_permissions_boundary_from_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete permissions boundary from permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    try:
        client.delete_permissions_boundary_from_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to delete permissions boundary from permission set"
        ) from exc
    return None


def delete_trusted_token_issuer(
    trusted_token_issuer_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete trusted token issuer.

    Args:
        trusted_token_issuer_arn: Trusted token issuer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    try:
        client.delete_trusted_token_issuer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete trusted token issuer") from exc
    return None


def describe_account_assignment_creation_status(
    instance_arn: str,
    account_assignment_creation_request_id: str,
    region_name: str | None = None,
) -> DescribeAccountAssignmentCreationStatusResult:
    """Describe account assignment creation status.

    Args:
        instance_arn: Instance arn.
        account_assignment_creation_request_id: Account assignment creation request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["AccountAssignmentCreationRequestId"] = account_assignment_creation_request_id
    try:
        resp = client.describe_account_assignment_creation_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account assignment creation status") from exc
    return DescribeAccountAssignmentCreationStatusResult(
        account_assignment_creation_status=resp.get("AccountAssignmentCreationStatus"),
    )


def describe_account_assignment_deletion_status(
    instance_arn: str,
    account_assignment_deletion_request_id: str,
    region_name: str | None = None,
) -> DescribeAccountAssignmentDeletionStatusResult:
    """Describe account assignment deletion status.

    Args:
        instance_arn: Instance arn.
        account_assignment_deletion_request_id: Account assignment deletion request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["AccountAssignmentDeletionRequestId"] = account_assignment_deletion_request_id
    try:
        resp = client.describe_account_assignment_deletion_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe account assignment deletion status") from exc
    return DescribeAccountAssignmentDeletionStatusResult(
        account_assignment_deletion_status=resp.get("AccountAssignmentDeletionStatus"),
    )


def describe_application(
    application_arn: str,
    region_name: str | None = None,
) -> DescribeApplicationResult:
    """Describe application.

    Args:
        application_arn: Application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = client.describe_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application") from exc
    return DescribeApplicationResult(
        application_arn=resp.get("ApplicationArn"),
        application_provider_arn=resp.get("ApplicationProviderArn"),
        name=resp.get("Name"),
        application_account=resp.get("ApplicationAccount"),
        instance_arn=resp.get("InstanceArn"),
        status=resp.get("Status"),
        portal_options=resp.get("PortalOptions"),
        description=resp.get("Description"),
        created_date=resp.get("CreatedDate"),
    )


def describe_application_assignment(
    application_arn: str,
    principal_id: str,
    principal_type: str,
    region_name: str | None = None,
) -> DescribeApplicationAssignmentResult:
    """Describe application assignment.

    Args:
        application_arn: Application arn.
        principal_id: Principal id.
        principal_type: Principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        resp = client.describe_application_assignment(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application assignment") from exc
    return DescribeApplicationAssignmentResult(
        principal_type=resp.get("PrincipalType"),
        principal_id=resp.get("PrincipalId"),
        application_arn=resp.get("ApplicationArn"),
    )


def describe_application_provider(
    application_provider_arn: str,
    region_name: str | None = None,
) -> DescribeApplicationProviderResult:
    """Describe application provider.

    Args:
        application_provider_arn: Application provider arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationProviderArn"] = application_provider_arn
    try:
        resp = client.describe_application_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe application provider") from exc
    return DescribeApplicationProviderResult(
        application_provider_arn=resp.get("ApplicationProviderArn"),
        federation_protocol=resp.get("FederationProtocol"),
        display_data=resp.get("DisplayData"),
        resource_server_config=resp.get("ResourceServerConfig"),
    )


def describe_instance_access_control_attribute_configuration(
    instance_arn: str,
    region_name: str | None = None,
) -> DescribeInstanceAccessControlAttributeConfigurationResult:
    """Describe instance access control attribute configuration.

    Args:
        instance_arn: Instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    try:
        resp = client.describe_instance_access_control_attribute_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe instance access control attribute configuration"
        ) from exc
    return DescribeInstanceAccessControlAttributeConfigurationResult(
        status=resp.get("Status"),
        status_reason=resp.get("StatusReason"),
        instance_access_control_attribute_configuration=resp.get(
            "InstanceAccessControlAttributeConfiguration"
        ),
    )


def describe_permission_set_provisioning_status(
    instance_arn: str,
    provision_permission_set_request_id: str,
    region_name: str | None = None,
) -> DescribePermissionSetProvisioningStatusResult:
    """Describe permission set provisioning status.

    Args:
        instance_arn: Instance arn.
        provision_permission_set_request_id: Provision permission set request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["ProvisionPermissionSetRequestId"] = provision_permission_set_request_id
    try:
        resp = client.describe_permission_set_provisioning_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe permission set provisioning status") from exc
    return DescribePermissionSetProvisioningStatusResult(
        permission_set_provisioning_status=resp.get("PermissionSetProvisioningStatus"),
    )


def describe_trusted_token_issuer(
    trusted_token_issuer_arn: str,
    region_name: str | None = None,
) -> DescribeTrustedTokenIssuerResult:
    """Describe trusted token issuer.

    Args:
        trusted_token_issuer_arn: Trusted token issuer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    try:
        resp = client.describe_trusted_token_issuer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe trusted token issuer") from exc
    return DescribeTrustedTokenIssuerResult(
        trusted_token_issuer_arn=resp.get("TrustedTokenIssuerArn"),
        name=resp.get("Name"),
        trusted_token_issuer_type=resp.get("TrustedTokenIssuerType"),
        trusted_token_issuer_configuration=resp.get("TrustedTokenIssuerConfiguration"),
    )


def detach_customer_managed_policy_reference_from_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    customer_managed_policy_reference: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Detach customer managed policy reference from permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        customer_managed_policy_reference: Customer managed policy reference.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["CustomerManagedPolicyReference"] = customer_managed_policy_reference
    try:
        client.detach_customer_managed_policy_reference_from_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to detach customer managed policy reference from permission set"
        ) from exc
    return None


def get_application_access_scope(
    application_arn: str,
    scope: str,
    region_name: str | None = None,
) -> GetApplicationAccessScopeResult:
    """Get application access scope.

    Args:
        application_arn: Application arn.
        scope: Scope.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["Scope"] = scope
    try:
        resp = client.get_application_access_scope(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get application access scope") from exc
    return GetApplicationAccessScopeResult(
        scope=resp.get("Scope"),
        authorized_targets=resp.get("AuthorizedTargets"),
    )


def get_application_assignment_configuration(
    application_arn: str,
    region_name: str | None = None,
) -> GetApplicationAssignmentConfigurationResult:
    """Get application assignment configuration.

    Args:
        application_arn: Application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = client.get_application_assignment_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get application assignment configuration") from exc
    return GetApplicationAssignmentConfigurationResult(
        assignment_required=resp.get("AssignmentRequired"),
    )


def get_application_authentication_method(
    application_arn: str,
    authentication_method_type: str,
    region_name: str | None = None,
) -> GetApplicationAuthenticationMethodResult:
    """Get application authentication method.

    Args:
        application_arn: Application arn.
        authentication_method_type: Authentication method type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    try:
        resp = client.get_application_authentication_method(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get application authentication method") from exc
    return GetApplicationAuthenticationMethodResult(
        authentication_method=resp.get("AuthenticationMethod"),
    )


def get_application_grant(
    application_arn: str,
    grant_type: str,
    region_name: str | None = None,
) -> GetApplicationGrantResult:
    """Get application grant.

    Args:
        application_arn: Application arn.
        grant_type: Grant type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    try:
        resp = client.get_application_grant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get application grant") from exc
    return GetApplicationGrantResult(
        grant=resp.get("Grant"),
    )


def get_application_session_configuration(
    application_arn: str,
    region_name: str | None = None,
) -> GetApplicationSessionConfigurationResult:
    """Get application session configuration.

    Args:
        application_arn: Application arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = client.get_application_session_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get application session configuration") from exc
    return GetApplicationSessionConfigurationResult(
        user_background_session_application_status=resp.get(
            "UserBackgroundSessionApplicationStatus"
        ),
    )


def get_permissions_boundary_for_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    region_name: str | None = None,
) -> GetPermissionsBoundaryForPermissionSetResult:
    """Get permissions boundary for permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    try:
        resp = client.get_permissions_boundary_for_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get permissions boundary for permission set") from exc
    return GetPermissionsBoundaryForPermissionSetResult(
        permissions_boundary=resp.get("PermissionsBoundary"),
    )


def list_account_assignment_creation_status(
    instance_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListAccountAssignmentCreationStatusResult:
    """List account assignment creation status.

    Args:
        instance_arn: Instance arn.
        max_results: Max results.
        next_token: Next token.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = client.list_account_assignment_creation_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list account assignment creation status") from exc
    return ListAccountAssignmentCreationStatusResult(
        account_assignments_creation_status=resp.get("AccountAssignmentsCreationStatus"),
        next_token=resp.get("NextToken"),
    )


def list_account_assignment_deletion_status(
    instance_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListAccountAssignmentDeletionStatusResult:
    """List account assignment deletion status.

    Args:
        instance_arn: Instance arn.
        max_results: Max results.
        next_token: Next token.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = client.list_account_assignment_deletion_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list account assignment deletion status") from exc
    return ListAccountAssignmentDeletionStatusResult(
        account_assignments_deletion_status=resp.get("AccountAssignmentsDeletionStatus"),
        next_token=resp.get("NextToken"),
    )


def list_account_assignments_for_principal(
    instance_arn: str,
    principal_id: str,
    principal_type: str,
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccountAssignmentsForPrincipalResult:
    """List account assignments for principal.

    Args:
        instance_arn: Instance arn.
        principal_id: Principal id.
        principal_type: Principal type.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_account_assignments_for_principal(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list account assignments for principal") from exc
    return ListAccountAssignmentsForPrincipalResult(
        account_assignments=resp.get("AccountAssignments"),
        next_token=resp.get("NextToken"),
    )


def list_application_access_scopes(
    application_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationAccessScopesResult:
    """List application access scopes.

    Args:
        application_arn: Application arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_access_scopes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application access scopes") from exc
    return ListApplicationAccessScopesResult(
        scopes=resp.get("Scopes"),
        next_token=resp.get("NextToken"),
    )


def list_application_assignments(
    application_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationAssignmentsResult:
    """List application assignments.

    Args:
        application_arn: Application arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_assignments(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application assignments") from exc
    return ListApplicationAssignmentsResult(
        application_assignments=resp.get("ApplicationAssignments"),
        next_token=resp.get("NextToken"),
    )


def list_application_assignments_for_principal(
    instance_arn: str,
    principal_id: str,
    principal_type: str,
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListApplicationAssignmentsForPrincipalResult:
    """List application assignments for principal.

    Args:
        instance_arn: Instance arn.
        principal_id: Principal id.
        principal_type: Principal type.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_application_assignments_for_principal(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application assignments for principal") from exc
    return ListApplicationAssignmentsForPrincipalResult(
        application_assignments=resp.get("ApplicationAssignments"),
        next_token=resp.get("NextToken"),
    )


def list_application_authentication_methods(
    application_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationAuthenticationMethodsResult:
    """List application authentication methods.

    Args:
        application_arn: Application arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_authentication_methods(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application authentication methods") from exc
    return ListApplicationAuthenticationMethodsResult(
        authentication_methods=resp.get("AuthenticationMethods"),
        next_token=resp.get("NextToken"),
    )


def list_application_grants(
    application_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationGrantsResult:
    """List application grants.

    Args:
        application_arn: Application arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_grants(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application grants") from exc
    return ListApplicationGrantsResult(
        grants=resp.get("Grants"),
        next_token=resp.get("NextToken"),
    )


def list_application_providers(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationProvidersResult:
    """List application providers.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_application_providers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list application providers") from exc
    return ListApplicationProvidersResult(
        application_providers=resp.get("ApplicationProviders"),
        next_token=resp.get("NextToken"),
    )


def list_applications(
    instance_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListApplicationsResult:
    """List applications.

    Args:
        instance_arn: Instance arn.
        max_results: Max results.
        next_token: Next token.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = client.list_applications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list applications") from exc
    return ListApplicationsResult(
        applications=resp.get("Applications"),
        next_token=resp.get("NextToken"),
    )


def list_customer_managed_policy_references_in_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCustomerManagedPolicyReferencesInPermissionSetResult:
    """List customer managed policy references in permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_customer_managed_policy_references_in_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list customer managed policy references in permission set"
        ) from exc
    return ListCustomerManagedPolicyReferencesInPermissionSetResult(
        customer_managed_policy_references=resp.get("CustomerManagedPolicyReferences"),
        next_token=resp.get("NextToken"),
    )


def list_permission_set_provisioning_status(
    instance_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListPermissionSetProvisioningStatusResult:
    """List permission set provisioning status.

    Args:
        instance_arn: Instance arn.
        max_results: Max results.
        next_token: Next token.
        filter: Filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = client.list_permission_set_provisioning_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list permission set provisioning status") from exc
    return ListPermissionSetProvisioningStatusResult(
        permission_sets_provisioning_status=resp.get("PermissionSetsProvisioningStatus"),
        next_token=resp.get("NextToken"),
    )


def list_permission_sets_provisioned_to_account(
    instance_arn: str,
    account_id: str,
    *,
    provisioning_status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPermissionSetsProvisionedToAccountResult:
    """List permission sets provisioned to account.

    Args:
        instance_arn: Instance arn.
        account_id: Account id.
        provisioning_status: Provisioning status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["AccountId"] = account_id
    if provisioning_status is not None:
        kwargs["ProvisioningStatus"] = provisioning_status
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_permission_sets_provisioned_to_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list permission sets provisioned to account") from exc
    return ListPermissionSetsProvisionedToAccountResult(
        next_token=resp.get("NextToken"),
        permission_sets=resp.get("PermissionSets"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    instance_arn: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        instance_arn: Instance arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
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


def list_trusted_token_issuers(
    instance_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTrustedTokenIssuersResult:
    """List trusted token issuers.

    Args:
        instance_arn: Instance arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_trusted_token_issuers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list trusted token issuers") from exc
    return ListTrustedTokenIssuersResult(
        trusted_token_issuers=resp.get("TrustedTokenIssuers"),
        next_token=resp.get("NextToken"),
    )


def put_application_access_scope(
    scope: str,
    application_arn: str,
    *,
    authorized_targets: list[str] | None = None,
    region_name: str | None = None,
) -> None:
    """Put application access scope.

    Args:
        scope: Scope.
        application_arn: Application arn.
        authorized_targets: Authorized targets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Scope"] = scope
    kwargs["ApplicationArn"] = application_arn
    if authorized_targets is not None:
        kwargs["AuthorizedTargets"] = authorized_targets
    try:
        client.put_application_access_scope(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put application access scope") from exc
    return None


def put_application_assignment_configuration(
    application_arn: str,
    assignment_required: bool,
    region_name: str | None = None,
) -> None:
    """Put application assignment configuration.

    Args:
        application_arn: Application arn.
        assignment_required: Assignment required.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AssignmentRequired"] = assignment_required
    try:
        client.put_application_assignment_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put application assignment configuration") from exc
    return None


def put_application_authentication_method(
    application_arn: str,
    authentication_method_type: str,
    authentication_method: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put application authentication method.

    Args:
        application_arn: Application arn.
        authentication_method_type: Authentication method type.
        authentication_method: Authentication method.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    kwargs["AuthenticationMethod"] = authentication_method
    try:
        client.put_application_authentication_method(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put application authentication method") from exc
    return None


def put_application_grant(
    application_arn: str,
    grant_type: str,
    grant: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put application grant.

    Args:
        application_arn: Application arn.
        grant_type: Grant type.
        grant: Grant.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    kwargs["Grant"] = grant
    try:
        client.put_application_grant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put application grant") from exc
    return None


def put_application_session_configuration(
    application_arn: str,
    *,
    user_background_session_application_status: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put application session configuration.

    Args:
        application_arn: Application arn.
        user_background_session_application_status: User background session application status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if user_background_session_application_status is not None:
        kwargs["UserBackgroundSessionApplicationStatus"] = (
            user_background_session_application_status
        )
    try:
        client.put_application_session_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put application session configuration") from exc
    return None


def put_permissions_boundary_to_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    permissions_boundary: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put permissions boundary to permission set.

    Args:
        instance_arn: Instance arn.
        permission_set_arn: Permission set arn.
        permissions_boundary: Permissions boundary.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["PermissionsBoundary"] = permissions_boundary
    try:
        client.put_permissions_boundary_to_permission_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put permissions boundary to permission set") from exc
    return None


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    *,
    instance_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        instance_arn: Instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    *,
    instance_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        instance_arn: Instance arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_application(
    application_arn: str,
    *,
    name: str | None = None,
    description: str | None = None,
    status: str | None = None,
    portal_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update application.

    Args:
        application_arn: Application arn.
        name: Name.
        description: Description.
        status: Status.
        portal_options: Portal options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if status is not None:
        kwargs["Status"] = status
    if portal_options is not None:
        kwargs["PortalOptions"] = portal_options
    try:
        client.update_application(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update application") from exc
    return None


def update_instance(
    instance_arn: str,
    *,
    name: str | None = None,
    encryption_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update instance.

    Args:
        instance_arn: Instance arn.
        name: Name.
        encryption_configuration: Encryption configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if name is not None:
        kwargs["Name"] = name
    if encryption_configuration is not None:
        kwargs["EncryptionConfiguration"] = encryption_configuration
    try:
        client.update_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update instance") from exc
    return None


def update_instance_access_control_attribute_configuration(
    instance_arn: str,
    instance_access_control_attribute_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update instance access control attribute configuration.

    Args:
        instance_arn: Instance arn.
        instance_access_control_attribute_configuration: Instance access control attribute configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["InstanceAccessControlAttributeConfiguration"] = (
        instance_access_control_attribute_configuration
    )
    try:
        client.update_instance_access_control_attribute_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to update instance access control attribute configuration"
        ) from exc
    return None


def update_trusted_token_issuer(
    trusted_token_issuer_arn: str,
    *,
    name: str | None = None,
    trusted_token_issuer_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update trusted token issuer.

    Args:
        trusted_token_issuer_arn: Trusted token issuer arn.
        name: Name.
        trusted_token_issuer_configuration: Trusted token issuer configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    if name is not None:
        kwargs["Name"] = name
    if trusted_token_issuer_configuration is not None:
        kwargs["TrustedTokenIssuerConfiguration"] = trusted_token_issuer_configuration
    try:
        client.update_trusted_token_issuer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update trusted token issuer") from exc
    return None
