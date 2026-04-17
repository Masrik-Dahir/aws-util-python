"""Native async SSO Admin utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.sso_admin import (
    AccountAssignmentResult,
    AccountAssignmentStatusResult,
    CreateApplicationResult,
    CreateTrustedTokenIssuerResult,
    DescribeAccountAssignmentCreationStatusResult,
    DescribeAccountAssignmentDeletionStatusResult,
    DescribeApplicationAssignmentResult,
    DescribeApplicationProviderResult,
    DescribeApplicationResult,
    DescribeInstanceAccessControlAttributeConfigurationResult,
    DescribePermissionSetProvisioningStatusResult,
    DescribeTrustedTokenIssuerResult,
    GetApplicationAccessScopeResult,
    GetApplicationAssignmentConfigurationResult,
    GetApplicationAuthenticationMethodResult,
    GetApplicationGrantResult,
    GetApplicationSessionConfigurationResult,
    GetPermissionsBoundaryForPermissionSetResult,
    InstanceResult,
    ListAccountAssignmentCreationStatusResult,
    ListAccountAssignmentDeletionStatusResult,
    ListAccountAssignmentsForPrincipalResult,
    ListApplicationAccessScopesResult,
    ListApplicationAssignmentsForPrincipalResult,
    ListApplicationAssignmentsResult,
    ListApplicationAuthenticationMethodsResult,
    ListApplicationGrantsResult,
    ListApplicationProvidersResult,
    ListApplicationsResult,
    ListCustomerManagedPolicyReferencesInPermissionSetResult,
    ListPermissionSetProvisioningStatusResult,
    ListPermissionSetsProvisionedToAccountResult,
    ListTagsForResourceResult,
    ListTrustedTokenIssuersResult,
    ManagedPolicyResult,
    PermissionSetResult,
    ProvisionStatusResult,
    _parse_account_assignment,
    _parse_assignment_status,
    _parse_instance,
    _parse_managed_policy,
    _parse_permission_set,
    _parse_provision_status,
)

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


async def create_instance(
    *,
    name: str | None = None,
    region_name: str | None = None,
) -> InstanceResult:
    """Create an IAM Identity Center instance.

    Args:
        name: Optional friendly name.
        region_name: AWS region override.

    Returns:
        An :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = await client.call("CreateInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_instance failed") from exc
    return _parse_instance(resp)


async def list_instances(
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
    client = async_client("sso-admin", region_name)
    results: list[InstanceResult] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = await client.call("ListInstances", **kwargs)
            for inst in resp.get("Instances", []):
                results.append(_parse_instance(inst))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_instances failed") from exc
    return results


async def describe_instance(
    instance_arn: str,
    *,
    region_name: str | None = None,
) -> InstanceResult:
    """Describe an IAM Identity Center instance.

    Args:
        instance_arn: The ARN of the SSO instance.
        region_name: AWS region override.

    Returns:
        An :class:`InstanceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        resp = await client.call("DescribeInstance", InstanceArn=instance_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_instance failed for {instance_arn!r}") from exc
    return _parse_instance(resp)


async def delete_instance(
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
    client = async_client("sso-admin", region_name)
    try:
        await client.call("DeleteInstance", InstanceArn=instance_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_instance failed for {instance_arn!r}") from exc


async def create_permission_set(
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
        session_duration: ISO 8601 duration.
        relay_state: Optional relay state URL.
        region_name: AWS region override.

    Returns:
        A :class:`PermissionSetResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("CreatePermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_permission_set failed for {name!r}") from exc
    return _parse_permission_set(resp["PermissionSet"])


async def describe_permission_set(
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
        A :class:`PermissionSetResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        resp = await client.call(
            "DescribePermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_permission_set failed for {permission_set_arn!r}",
        ) from exc
    return _parse_permission_set(resp["PermissionSet"])


async def list_permission_sets(
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
    client = async_client("sso-admin", region_name)
    results: list[str] = []
    kwargs: dict[str, Any] = {"InstanceArn": instance_arn}
    try:
        while True:
            resp = await client.call("ListPermissionSets", **kwargs)
            results.extend(resp.get("PermissionSets", []))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_permission_sets failed") from exc
    return results


async def update_permission_set(
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
        permission_set_arn: The ARN of the permission set.
        description: New description.
        session_duration: New session duration.
        relay_state: New relay state URL.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
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
        await client.call("UpdatePermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_permission_set failed for {permission_set_arn!r}",
        ) from exc


async def delete_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        await client.call(
            "DeletePermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"delete_permission_set failed for {permission_set_arn!r}",
        ) from exc


async def attach_managed_policy_to_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    managed_policy_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Attach a managed policy to a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        managed_policy_arn: The ARN of the managed policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        await client.call(
            "AttachManagedPolicyToPermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            ManagedPolicyArn=managed_policy_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "attach_managed_policy_to_permission_set failed",
        ) from exc


async def detach_managed_policy_from_permission_set(
    instance_arn: str,
    permission_set_arn: str,
    managed_policy_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Detach a managed policy from a permission set.

    Args:
        instance_arn: The ARN of the SSO instance.
        permission_set_arn: The ARN of the permission set.
        managed_policy_arn: The ARN of the managed policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        await client.call(
            "DetachManagedPolicyFromPermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            ManagedPolicyArn=managed_policy_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "detach_managed_policy_from_permission_set failed",
        ) from exc


async def list_managed_policies_in_permission_set(
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
    client = async_client("sso-admin", region_name)
    results: list[ManagedPolicyResult] = []
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "PermissionSetArn": permission_set_arn,
    }
    try:
        while True:
            resp = await client.call("ListManagedPoliciesInPermissionSet", **kwargs)
            for pol in resp.get("AttachedManagedPolicies", []):
                results.append(_parse_managed_policy(pol))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "list_managed_policies_in_permission_set failed",
        ) from exc
    return results


async def put_inline_policy_to_permission_set(
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
    client = async_client("sso-admin", region_name)
    try:
        await client.call(
            "PutInlinePolicyToPermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
            InlinePolicy=inline_policy,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "put_inline_policy_to_permission_set failed",
        ) from exc


async def get_inline_policy_for_permission_set(
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
    client = async_client("sso-admin", region_name)
    try:
        resp = await client.call(
            "GetInlinePolicyForPermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "get_inline_policy_for_permission_set failed",
        ) from exc
    return resp.get("InlinePolicy", "")


async def delete_inline_policy_from_permission_set(
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
    client = async_client("sso-admin", region_name)
    try:
        await client.call(
            "DeleteInlinePolicyFromPermissionSet",
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "delete_inline_policy_from_permission_set failed",
        ) from exc


async def create_account_assignment(
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
        An :class:`AccountAssignmentStatusResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        resp = await client.call(
            "CreateAccountAssignment",
            InstanceArn=instance_arn,
            TargetId=target_id,
            TargetType=target_type,
            PermissionSetArn=permission_set_arn,
            PrincipalType=principal_type,
            PrincipalId=principal_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "create_account_assignment failed") from exc
    return _parse_assignment_status(resp.get("AccountAssignmentCreationStatus", {}))


async def list_account_assignments(
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
    client = async_client("sso-admin", region_name)
    results: list[AccountAssignmentResult] = []
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "AccountId": account_id,
        "PermissionSetArn": permission_set_arn,
    }
    try:
        while True:
            resp = await client.call("ListAccountAssignments", **kwargs)
            for aa in resp.get("AccountAssignments", []):
                results.append(_parse_account_assignment(aa))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_account_assignments failed") from exc
    return results


async def delete_account_assignment(
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
        An :class:`AccountAssignmentStatusResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    try:
        resp = await client.call(
            "DeleteAccountAssignment",
            InstanceArn=instance_arn,
            TargetId=target_id,
            TargetType=target_type,
            PermissionSetArn=permission_set_arn,
            PrincipalType=principal_type,
            PrincipalId=principal_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_account_assignment failed") from exc
    return _parse_assignment_status(resp.get("AccountAssignmentDeletionStatus", {}))


async def list_accounts_for_provisioned_permission_set(
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
    client = async_client("sso-admin", region_name)
    results: list[str] = []
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "PermissionSetArn": permission_set_arn,
        "ProvisioningStatus": provisioning_status,
    }
    try:
        while True:
            resp = await client.call(
                "ListAccountsForProvisionedPermissionSet",
                **kwargs,
            )
            results.extend(resp.get("AccountIds", []))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "list_accounts_for_provisioned_permission_set failed",
        ) from exc
    return results


async def provision_permission_set(
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
        target_type: Target type string.
        target_id: Account ID when target_type is ``"AWS_ACCOUNT"``.
        region_name: AWS region override.

    Returns:
        A :class:`ProvisionStatusResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {
        "InstanceArn": instance_arn,
        "PermissionSetArn": permission_set_arn,
        "TargetType": target_type,
    }
    if target_id is not None:
        kwargs["TargetId"] = target_id
    try:
        resp = await client.call("ProvisionPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "provision_permission_set failed") from exc
    return _parse_provision_status(resp.get("PermissionSetProvisioningStatus", {}))


async def attach_customer_managed_policy_reference_to_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["CustomerManagedPolicyReference"] = customer_managed_policy_reference
    try:
        await client.call("AttachCustomerManagedPolicyReferenceToPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to attach customer managed policy reference to permission set"
        ) from exc
    return None


async def create_application(
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
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("CreateApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create application") from exc
    return CreateApplicationResult(
        application_arn=resp.get("ApplicationArn"),
    )


async def create_application_assignment(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        await client.call("CreateApplicationAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create application assignment") from exc
    return None


async def create_instance_access_control_attribute_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["InstanceAccessControlAttributeConfiguration"] = (
        instance_access_control_attribute_configuration
    )
    try:
        await client.call("CreateInstanceAccessControlAttributeConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to create instance access control attribute configuration"
        ) from exc
    return None


async def create_trusted_token_issuer(
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
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("CreateTrustedTokenIssuer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create trusted token issuer") from exc
    return CreateTrustedTokenIssuerResult(
        trusted_token_issuer_arn=resp.get("TrustedTokenIssuerArn"),
    )


async def delete_application(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        await client.call("DeleteApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete application") from exc
    return None


async def delete_application_access_scope(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["Scope"] = scope
    try:
        await client.call("DeleteApplicationAccessScope", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete application access scope") from exc
    return None


async def delete_application_assignment(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        await client.call("DeleteApplicationAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete application assignment") from exc
    return None


async def delete_application_authentication_method(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    try:
        await client.call("DeleteApplicationAuthenticationMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete application authentication method") from exc
    return None


async def delete_application_grant(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    try:
        await client.call("DeleteApplicationGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete application grant") from exc
    return None


async def delete_instance_access_control_attribute_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    try:
        await client.call("DeleteInstanceAccessControlAttributeConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to delete instance access control attribute configuration"
        ) from exc
    return None


async def delete_permissions_boundary_from_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    try:
        await client.call("DeletePermissionsBoundaryFromPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to delete permissions boundary from permission set"
        ) from exc
    return None


async def delete_trusted_token_issuer(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    try:
        await client.call("DeleteTrustedTokenIssuer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete trusted token issuer") from exc
    return None


async def describe_account_assignment_creation_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["AccountAssignmentCreationRequestId"] = account_assignment_creation_request_id
    try:
        resp = await client.call("DescribeAccountAssignmentCreationStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account assignment creation status") from exc
    return DescribeAccountAssignmentCreationStatusResult(
        account_assignment_creation_status=resp.get("AccountAssignmentCreationStatus"),
    )


async def describe_account_assignment_deletion_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["AccountAssignmentDeletionRequestId"] = account_assignment_deletion_request_id
    try:
        resp = await client.call("DescribeAccountAssignmentDeletionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account assignment deletion status") from exc
    return DescribeAccountAssignmentDeletionStatusResult(
        account_assignment_deletion_status=resp.get("AccountAssignmentDeletionStatus"),
    )


async def describe_application(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = await client.call("DescribeApplication", **kwargs)
    except Exception as exc:
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


async def describe_application_assignment(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["PrincipalId"] = principal_id
    kwargs["PrincipalType"] = principal_type
    try:
        resp = await client.call("DescribeApplicationAssignment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe application assignment") from exc
    return DescribeApplicationAssignmentResult(
        principal_type=resp.get("PrincipalType"),
        principal_id=resp.get("PrincipalId"),
        application_arn=resp.get("ApplicationArn"),
    )


async def describe_application_provider(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationProviderArn"] = application_provider_arn
    try:
        resp = await client.call("DescribeApplicationProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe application provider") from exc
    return DescribeApplicationProviderResult(
        application_provider_arn=resp.get("ApplicationProviderArn"),
        federation_protocol=resp.get("FederationProtocol"),
        display_data=resp.get("DisplayData"),
        resource_server_config=resp.get("ResourceServerConfig"),
    )


async def describe_instance_access_control_attribute_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    try:
        resp = await client.call("DescribeInstanceAccessControlAttributeConfiguration", **kwargs)
    except Exception as exc:
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


async def describe_permission_set_provisioning_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["ProvisionPermissionSetRequestId"] = provision_permission_set_request_id
    try:
        resp = await client.call("DescribePermissionSetProvisioningStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe permission set provisioning status") from exc
    return DescribePermissionSetProvisioningStatusResult(
        permission_set_provisioning_status=resp.get("PermissionSetProvisioningStatus"),
    )


async def describe_trusted_token_issuer(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    try:
        resp = await client.call("DescribeTrustedTokenIssuer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe trusted token issuer") from exc
    return DescribeTrustedTokenIssuerResult(
        trusted_token_issuer_arn=resp.get("TrustedTokenIssuerArn"),
        name=resp.get("Name"),
        trusted_token_issuer_type=resp.get("TrustedTokenIssuerType"),
        trusted_token_issuer_configuration=resp.get("TrustedTokenIssuerConfiguration"),
    )


async def detach_customer_managed_policy_reference_from_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["CustomerManagedPolicyReference"] = customer_managed_policy_reference
    try:
        await client.call("DetachCustomerManagedPolicyReferenceFromPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to detach customer managed policy reference from permission set"
        ) from exc
    return None


async def get_application_access_scope(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["Scope"] = scope
    try:
        resp = await client.call("GetApplicationAccessScope", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get application access scope") from exc
    return GetApplicationAccessScopeResult(
        scope=resp.get("Scope"),
        authorized_targets=resp.get("AuthorizedTargets"),
    )


async def get_application_assignment_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = await client.call("GetApplicationAssignmentConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get application assignment configuration") from exc
    return GetApplicationAssignmentConfigurationResult(
        assignment_required=resp.get("AssignmentRequired"),
    )


async def get_application_authentication_method(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    try:
        resp = await client.call("GetApplicationAuthenticationMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get application authentication method") from exc
    return GetApplicationAuthenticationMethodResult(
        authentication_method=resp.get("AuthenticationMethod"),
    )


async def get_application_grant(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    try:
        resp = await client.call("GetApplicationGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get application grant") from exc
    return GetApplicationGrantResult(
        grant=resp.get("Grant"),
    )


async def get_application_session_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    try:
        resp = await client.call("GetApplicationSessionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get application session configuration") from exc
    return GetApplicationSessionConfigurationResult(
        user_background_session_application_status=resp.get(
            "UserBackgroundSessionApplicationStatus"
        ),
    )


async def get_permissions_boundary_for_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    try:
        resp = await client.call("GetPermissionsBoundaryForPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get permissions boundary for permission set") from exc
    return GetPermissionsBoundaryForPermissionSetResult(
        permissions_boundary=resp.get("PermissionsBoundary"),
    )


async def list_account_assignment_creation_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = await client.call("ListAccountAssignmentCreationStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account assignment creation status") from exc
    return ListAccountAssignmentCreationStatusResult(
        account_assignments_creation_status=resp.get("AccountAssignmentsCreationStatus"),
        next_token=resp.get("NextToken"),
    )


async def list_account_assignment_deletion_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = await client.call("ListAccountAssignmentDeletionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account assignment deletion status") from exc
    return ListAccountAssignmentDeletionStatusResult(
        account_assignments_deletion_status=resp.get("AccountAssignmentsDeletionStatus"),
        next_token=resp.get("NextToken"),
    )


async def list_account_assignments_for_principal(
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
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("ListAccountAssignmentsForPrincipal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account assignments for principal") from exc
    return ListAccountAssignmentsForPrincipalResult(
        account_assignments=resp.get("AccountAssignments"),
        next_token=resp.get("NextToken"),
    )


async def list_application_access_scopes(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationAccessScopes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application access scopes") from exc
    return ListApplicationAccessScopesResult(
        scopes=resp.get("Scopes"),
        next_token=resp.get("NextToken"),
    )


async def list_application_assignments(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationAssignments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application assignments") from exc
    return ListApplicationAssignmentsResult(
        application_assignments=resp.get("ApplicationAssignments"),
        next_token=resp.get("NextToken"),
    )


async def list_application_assignments_for_principal(
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
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("ListApplicationAssignmentsForPrincipal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application assignments for principal") from exc
    return ListApplicationAssignmentsForPrincipalResult(
        application_assignments=resp.get("ApplicationAssignments"),
        next_token=resp.get("NextToken"),
    )


async def list_application_authentication_methods(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationAuthenticationMethods", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application authentication methods") from exc
    return ListApplicationAuthenticationMethodsResult(
        authentication_methods=resp.get("AuthenticationMethods"),
        next_token=resp.get("NextToken"),
    )


async def list_application_grants(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationGrants", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application grants") from exc
    return ListApplicationGrantsResult(
        grants=resp.get("Grants"),
        next_token=resp.get("NextToken"),
    )


async def list_application_providers(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application providers") from exc
    return ListApplicationProvidersResult(
        application_providers=resp.get("ApplicationProviders"),
        next_token=resp.get("NextToken"),
    )


async def list_applications(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = await client.call("ListApplications", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list applications") from exc
    return ListApplicationsResult(
        applications=resp.get("Applications"),
        next_token=resp.get("NextToken"),
    )


async def list_customer_managed_policy_references_in_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListCustomerManagedPolicyReferencesInPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to list customer managed policy references in permission set"
        ) from exc
    return ListCustomerManagedPolicyReferencesInPermissionSetResult(
        customer_managed_policy_references=resp.get("CustomerManagedPolicyReferences"),
        next_token=resp.get("NextToken"),
    )


async def list_permission_set_provisioning_status(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if filter is not None:
        kwargs["Filter"] = filter
    try:
        resp = await client.call("ListPermissionSetProvisioningStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list permission set provisioning status") from exc
    return ListPermissionSetProvisioningStatusResult(
        permission_sets_provisioning_status=resp.get("PermissionSetsProvisioningStatus"),
        next_token=resp.get("NextToken"),
    )


async def list_permission_sets_provisioned_to_account(
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
    client = async_client("sso-admin", region_name)
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
        resp = await client.call("ListPermissionSetsProvisionedToAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list permission sets provisioned to account") from exc
    return ListPermissionSetsProvisionedToAccountResult(
        next_token=resp.get("NextToken"),
        permission_sets=resp.get("PermissionSets"),
    )


async def list_tags_for_resource(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


async def list_trusted_token_issuers(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTrustedTokenIssuers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list trusted token issuers") from exc
    return ListTrustedTokenIssuersResult(
        trusted_token_issuers=resp.get("TrustedTokenIssuers"),
        next_token=resp.get("NextToken"),
    )


async def put_application_access_scope(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Scope"] = scope
    kwargs["ApplicationArn"] = application_arn
    if authorized_targets is not None:
        kwargs["AuthorizedTargets"] = authorized_targets
    try:
        await client.call("PutApplicationAccessScope", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put application access scope") from exc
    return None


async def put_application_assignment_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AssignmentRequired"] = assignment_required
    try:
        await client.call("PutApplicationAssignmentConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put application assignment configuration") from exc
    return None


async def put_application_authentication_method(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["AuthenticationMethodType"] = authentication_method_type
    kwargs["AuthenticationMethod"] = authentication_method
    try:
        await client.call("PutApplicationAuthenticationMethod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put application authentication method") from exc
    return None


async def put_application_grant(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    kwargs["GrantType"] = grant_type
    kwargs["Grant"] = grant
    try:
        await client.call("PutApplicationGrant", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put application grant") from exc
    return None


async def put_application_session_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ApplicationArn"] = application_arn
    if user_background_session_application_status is not None:
        kwargs["UserBackgroundSessionApplicationStatus"] = (
            user_background_session_application_status
        )
    try:
        await client.call("PutApplicationSessionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put application session configuration") from exc
    return None


async def put_permissions_boundary_to_permission_set(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["PermissionSetArn"] = permission_set_arn
    kwargs["PermissionsBoundary"] = permissions_boundary
    try:
        await client.call("PutPermissionsBoundaryToPermissionSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put permissions boundary to permission set") from exc
    return None


async def tag_resource(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    if instance_arn is not None:
        kwargs["InstanceArn"] = instance_arn
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_application(
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
    client = async_client("sso-admin", region_name)
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
        await client.call("UpdateApplication", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update application") from exc
    return None


async def update_instance(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    if name is not None:
        kwargs["Name"] = name
    if encryption_configuration is not None:
        kwargs["EncryptionConfiguration"] = encryption_configuration
    try:
        await client.call("UpdateInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update instance") from exc
    return None


async def update_instance_access_control_attribute_configuration(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceArn"] = instance_arn
    kwargs["InstanceAccessControlAttributeConfiguration"] = (
        instance_access_control_attribute_configuration
    )
    try:
        await client.call("UpdateInstanceAccessControlAttributeConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to update instance access control attribute configuration"
        ) from exc
    return None


async def update_trusted_token_issuer(
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
    client = async_client("sso-admin", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrustedTokenIssuerArn"] = trusted_token_issuer_arn
    if name is not None:
        kwargs["Name"] = name
    if trusted_token_issuer_configuration is not None:
        kwargs["TrustedTokenIssuerConfiguration"] = trusted_token_issuer_configuration
    try:
        await client.call("UpdateTrustedTokenIssuer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update trusted token issuer") from exc
    return None
